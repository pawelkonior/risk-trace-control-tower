from __future__ import annotations

import logging
import warnings
from collections import Counter
from collections.abc import Iterable
from decimal import Decimal
from typing import Any, NamedTuple

from langgraph.graph import END, START, StateGraph

from .checkpointing import MemorySaverCheckpoint
from .config import RwaAgentsConfig
from .guardrails import GuardrailService
from .observability import LocalObservability
from .prompts import DATA_ANALYST_PROMPT, RISK_EXPERT_PROMPT, SUPERVISOR_PROMPT, PromptRegistry
from .schemas import (
    AgentFinding,
    CommentaryViews,
    FinalCommentary,
    GuardrailResult,
    RecommendedAction,
    RwaAnalysisRequest,
    RwaAnalysisResponse,
    ValidationFlag,
    WorkerAnalysisResult,
)
from .state import AgentState
from .tools import analyze_data_quality, analyze_risk
from .validation import build_agent_state
from .watsonx import WatsonxClient, WatsonxError, WatsonxResponse, WatsonxResponseError

logger = logging.getLogger(__name__)

CHECKPOINTER = MemorySaverCheckpoint()


def run_rwa_analysis(request: RwaAnalysisRequest) -> RwaAnalysisResponse:
    config = RwaAgentsConfig.from_env()
    guardrails = GuardrailService(config.guardrails)
    prompts = PromptRegistry(config.langfuse)
    observability = LocalObservability(request.request_id, config.langfuse)
    observability.node("RequestValidation")
    input_guardrail = guardrails.scan("request_validation", _request_validation_summary(request))
    observability.guardrail(input_guardrail)
    if input_guardrail.blocked:
        final = _blocked_commentary(request, observability, ["Input guardrail blocked request."])
        observability.finalize()
        return _response(request, final, [], [], [], CommentaryViews(), observability.metadata)

    initial_state = build_agent_state(request)
    observability.node("AgentStateBuilt")
    CHECKPOINTER.put(request.request_id, dict(initial_state))

    graph = _build_graph(request, config, guardrails, prompts, observability)
    final_state = graph.invoke(
        initial_state,
        {"configurable": {"thread_id": request.request_id}},
    )
    CHECKPOINTER.put(request.request_id, dict(final_state))
    final = final_state["final_commentary"]
    if final is None:
        final = _blocked_commentary(
            request,
            observability,
            ["Workflow ended without final commentary."],
        )

    # Finalize observability and flush to Langfuse if enabled
    observability.finalize()

    return _response(
        request,
        final,
        final_state["validation_flags"],
        final_state["agent_findings"],
        final_state["recommended_actions"],
        final_state["commentary_views"],
        observability.metadata,
    )


def _build_graph(
    request: RwaAnalysisRequest,
    config: RwaAgentsConfig,
    guardrails: GuardrailService,
    prompts: PromptRegistry,
    observability: LocalObservability,
) -> Any:
    builder = StateGraph(AgentState)

    def analysis_phase(state: AgentState) -> dict:
        observability.node("AnalysisPhase")
        data_prompt, data_usage = prompts.get(DATA_ANALYST_PROMPT)
        risk_prompt, risk_usage = prompts.get(RISK_EXPERT_PROMPT)
        observability.prompt(data_usage)
        observability.prompt(risk_usage)
        guardrail_results = []
        guardrail_blocked = False
        for stage, prompt in (
            ("data_analyst_prompt", data_prompt),
            ("risk_expert_prompt", risk_prompt),
        ):
            result = guardrails.scan(stage, prompt)
            observability.guardrail(result)
            guardrail_results.append(result)
            guardrail_blocked = guardrail_blocked or result.blocked

        return {
            "agent_findings": [],
            "validation_flags": [],
            "recommended_actions": [],
            "quantitative_validation": [],
            "data_agent_result": None,
            "risk_agent_result": None,
            "guardrail_results": [*state["guardrail_results"], *guardrail_results],
            "guardrail_blocked": guardrail_blocked,
            "loop_count": state["loop_count"] + 1,
            "next_agent": None,
        }

    def data_analyst_agent(_state: AgentState) -> dict:
        observability.node("DataAnalystAgent")
        observability.tool("DataTools")
        result = analyze_data_quality(request)
        result = _maybe_enrich_worker_with_watsonx(
            request=request,
            result=result,
            config=config,
            guardrails=guardrails,
            observability=observability,
        )
        return {"data_agent_result": result}

    def risk_expert_agent(_state: AgentState) -> dict:
        observability.node("RiskExpertAgent")
        observability.tool("RiskTools")
        result = analyze_risk(request)
        result = _maybe_enrich_worker_with_watsonx(
            request=request,
            result=result,
            config=config,
            guardrails=guardrails,
            observability=observability,
        )
        return {"risk_agent_result": result}

    def analysis_fan_in(state: AgentState) -> dict:
        observability.node("AnalysisFanIn")
        data_result = state["data_agent_result"] or WorkerAnalysisResult(agent="DataAnalystAgent")
        risk_result = state["risk_agent_result"] or WorkerAnalysisResult(agent="RiskExpertAgent")
        worker_payload = {
            "data": data_result,
            "risk": risk_result,
        }
        worker_guardrail = guardrails.scan("worker_outputs", worker_payload)
        observability.guardrail(worker_guardrail)
        worker_guardrail_results = [
            *data_result.guardrail_results,
            *risk_result.guardrail_results,
            worker_guardrail,
        ]
        worker_messages = [
            *state["messages"],
            *data_result.messages,
            *risk_result.messages,
        ]
        worker_llm_call_count = (
            state["llm_call_count"] + data_result.llm_call_count + risk_result.llm_call_count
        )
        worker_token_count = (
            state["total_token_count"]
            + data_result.total_token_count
            + risk_result.total_token_count
        )
        if (
            worker_guardrail.blocked
            or data_result.guardrail_blocked
            or risk_result.guardrail_blocked
        ):
            return {
                "messages": worker_messages,
                "guardrail_results": [*state["guardrail_results"], *worker_guardrail_results],
                "guardrail_blocked": True,
                "llm_call_count": worker_llm_call_count,
                "total_token_count": worker_token_count,
            }
        return {
            "messages": [*worker_messages, "Parallel LangGraph worker analysis completed."],
            "agent_findings": [*data_result.findings, *risk_result.findings],
            "validation_flags": [
                *data_result.validation_flags,
                *risk_result.validation_flags,
            ],
            "recommended_actions": [
                *data_result.recommended_actions,
                *risk_result.recommended_actions,
            ],
            "quantitative_validation": risk_result.quantitative_validation,
            "guardrail_results": [*state["guardrail_results"], *worker_guardrail_results],
            "llm_call_count": worker_llm_call_count,
            "total_token_count": worker_token_count,
        }

    def supervisor_agent(state: AgentState) -> dict:
        observability.node("SupervisorAgent")
        supervisor_prompt, supervisor_usage = prompts.get(SUPERVISOR_PROMPT)
        observability.prompt(supervisor_usage)
        supervisor_guardrail = guardrails.scan("supervisor_prompt", supervisor_prompt)
        observability.guardrail(supervisor_guardrail)
        if supervisor_guardrail.blocked or state["guardrail_blocked"]:
            return {
                "guardrail_results": [*state["guardrail_results"], supervisor_guardrail],
                "guardrail_blocked": True,
                "next_agent": "GuardrailBlocked",
            }
        critical_flags = [flag for flag in state["validation_flags"] if flag.severity == "critical"]
        data_complete = any(
            finding.agent == "DataAnalystAgent" for finding in state["agent_findings"]
        ) or any(flag.source_agent == "DataAnalystAgent" for flag in state["validation_flags"])
        risk_complete = bool(state["quantitative_validation"]) or any(
            finding.agent == "RiskExpertAgent" for finding in state["agent_findings"]
        )
        consensus_reached = data_complete and risk_complete and not critical_flags
        views = _synthesize_views(
            request=request,
            findings=state["agent_findings"],
            flags=state["validation_flags"],
            actions=state["recommended_actions"],
        )
        should_loop = not consensus_reached and state["loop_count"] < state["loop_limit"]
        guardrail_results = [*state["guardrail_results"], supervisor_guardrail]
        messages = state["messages"]
        llm_call_count = state["llm_call_count"]
        total_token_count = state["total_token_count"]

        if not should_loop:
            llm_result = _maybe_synthesize_with_watsonx(
                request=request,
                state=state,
                deterministic_views=views,
                consensus_reached=consensus_reached,
                config=config,
                guardrails=guardrails,
                observability=observability,
            )
            views = llm_result.views
            guardrail_results = [*guardrail_results, *llm_result.guardrail_results]
            messages = [*messages, *llm_result.messages]
            llm_call_count = llm_result.llm_call_count
            total_token_count = llm_result.total_token_count
            if llm_result.blocked:
                return {
                    "guardrail_results": guardrail_results,
                    "guardrail_blocked": True,
                    "llm_call_count": llm_call_count,
                    "total_token_count": total_token_count,
                    "next_agent": "GuardrailBlocked",
                }

        return {
            "commentary_views": views,
            "consensus_reached": consensus_reached,
            "messages": messages,
            "guardrail_results": guardrail_results,
            "llm_call_count": llm_call_count,
            "total_token_count": total_token_count,
            "next_agent": "AnalysisPhase" if should_loop else "FinalOutputGuard",
        }

    def final_output_guard(state: AgentState) -> dict:
        observability.node("FinalOutputGuard")
        status = "COMPLETED" if state["consensus_reached"] else "LOOP_LIMIT_REACHED"
        views = state["commentary_views"]
        final = FinalCommentary(
            status=status,
            consensus_reached=state["consensus_reached"],
            loop_count=state["loop_count"],
            executive_summary=views.executive_summary,
            cro_view=views.cro_view,
            cfo_view=views.cfo_view,
            data_quality_observations=[
                finding for finding in state["agent_findings"] if finding.kind == "data_quality"
            ],
            risk_observations=[
                finding
                for finding in state["agent_findings"]
                if finding.kind in {"risk", "validation"}
            ],
            quantitative_validation=state["quantitative_validation"],
            recommended_actions=state["recommended_actions"],
            validation_flags=state["validation_flags"],
            source_agents=sorted({finding.agent for finding in state["agent_findings"]}),
            messages=state["messages"],
        )
        final_guardrail = guardrails.scan("final_output", final)
        observability.guardrail(final_guardrail)
        if final_guardrail.blocked:
            return {
                "guardrail_results": [*state["guardrail_results"], final_guardrail],
                "guardrail_blocked": True,
                "next_agent": "GuardrailBlocked",
            }
        observability.metadata.llm_call_count = state["llm_call_count"]
        observability.metadata.total_token_count = state["total_token_count"]
        # Compute all required evaluation scores
        observability.compute_final_scores(dict(state))
        final.observability = observability.metadata
        return {
            "final_commentary": final,
            "guardrail_results": [*state["guardrail_results"], final_guardrail],
            "next_agent": "FinalStructuredResponse",
        }

    def guardrail_blocked(_state: AgentState) -> dict:
        observability.node("GuardrailBlocked")
        observability.metadata.llm_call_count = _state["llm_call_count"]
        observability.metadata.total_token_count = _state["total_token_count"]
        final = _blocked_commentary(
            request,
            observability,
            ["Guardrail blocked unsafe workflow output."],
        )
        return {
            "final_commentary": final,
            "guardrail_blocked": True,
            "next_agent": "FinalStructuredResponse",
        }

    def final_structured_response(_state: AgentState) -> dict:
        observability.node("FinalStructuredResponse")
        return {}

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="'asyncio.iscoroutinefunction'.*",
            category=DeprecationWarning,
        )
        builder.add_node("AnalysisPhase", analysis_phase)
        builder.add_node("DataAnalystAgent", data_analyst_agent)
        builder.add_node("RiskExpertAgent", risk_expert_agent)
        builder.add_node("AnalysisFanIn", analysis_fan_in)
        builder.add_node("SupervisorAgent", supervisor_agent)
        builder.add_node("FinalOutputGuard", final_output_guard)
        builder.add_node("GuardrailBlocked", guardrail_blocked)
        builder.add_node("FinalStructuredResponse", final_structured_response)

        builder.add_edge(START, "AnalysisPhase")
        builder.add_edge("AnalysisPhase", "DataAnalystAgent")
        builder.add_edge("AnalysisPhase", "RiskExpertAgent")
        builder.add_edge(["DataAnalystAgent", "RiskExpertAgent"], "AnalysisFanIn")
        builder.add_edge("AnalysisFanIn", "SupervisorAgent")
        builder.add_conditional_edges(
            "SupervisorAgent",
            lambda state: state["next_agent"] or "FinalOutputGuard",
            {
                "AnalysisPhase": "AnalysisPhase",
                "FinalOutputGuard": "FinalOutputGuard",
                "GuardrailBlocked": "GuardrailBlocked",
            },
        )
        builder.add_conditional_edges(
            "FinalOutputGuard",
            lambda state: state["next_agent"] or "FinalStructuredResponse",
            {
                "FinalStructuredResponse": "FinalStructuredResponse",
                "GuardrailBlocked": "GuardrailBlocked",
            },
        )
        builder.add_edge("GuardrailBlocked", "FinalStructuredResponse")
        builder.add_edge("FinalStructuredResponse", END)
        return builder.compile(checkpointer=CHECKPOINTER.langgraph_saver)


class LlmSynthesisResult(NamedTuple):
    views: CommentaryViews
    guardrail_results: list[GuardrailResult]
    blocked: bool
    llm_call_count: int
    total_token_count: int
    messages: list[str]


def _maybe_enrich_worker_with_watsonx(
    *,
    request: RwaAnalysisRequest,
    result: WorkerAnalysisResult,
    config: RwaAgentsConfig,
    guardrails: GuardrailService,
    observability: LocalObservability,
) -> WorkerAnalysisResult:
    if not config.uses_watsonx:
        return result

    if not config.watsonx_configured:
        return result.model_copy(
            update={
                "messages": [
                    *result.messages,
                    f"{result.agent} Watsonx synthesis skipped because watsonx is not configured.",
                ]
            }
        )

    stage_prefix = "data_analyst" if result.agent == "DataAnalystAgent" else "risk_expert"
    prompt = _build_worker_watsonx_prompt(request=request, result=result)
    input_guardrail = guardrails.scan(f"{stage_prefix}_llm_input", prompt)
    observability.guardrail(input_guardrail)
    if input_guardrail.blocked:
        return result.model_copy(
            update={
                "guardrail_results": [*result.guardrail_results, input_guardrail],
                "guardrail_blocked": True,
            }
        )

    try:
        watsonx_response = _new_watsonx_client(config).chat(prompt)
    except WatsonxResponseError as exc:
        token_count = _record_worker_failed_watsonx_response(
            config=config,
            observability=observability,
            error=exc,
        )
        output_guardrail = guardrails.scan(
            f"{stage_prefix}_llm_output",
            exc.raw_text or f"Malformed watsonx response for {result.agent}.",
        )
        observability.guardrail(output_guardrail)
        return result.model_copy(
            update={
                "guardrail_results": [
                    *result.guardrail_results,
                    input_guardrail,
                    output_guardrail,
                ],
                "guardrail_blocked": output_guardrail.blocked,
                "messages": [
                    *result.messages,
                    f"{result.agent} Watsonx response was not structured; tool result kept.",
                ],
                "llm_call_count": 1,
                "total_token_count": token_count,
            }
        )
    except WatsonxError as exc:
        logger.warning("%s Watsonx synthesis unavailable: %s", result.agent, type(exc).__name__)
        return result.model_copy(
            update={
                "guardrail_results": [*result.guardrail_results, input_guardrail],
                "messages": [
                    *result.messages,
                    f"{result.agent} Watsonx synthesis unavailable; tool result kept.",
                ],
            }
        )

    token_count = _record_successful_worker_watsonx_response(
        config=config,
        observability=observability,
        response=watsonx_response,
    )
    output_payload = {
        "executive_summary": watsonx_response.executive_summary,
        "cro_view": watsonx_response.cro_view,
        "cfo_view": watsonx_response.cfo_view,
    }
    output_guardrail = guardrails.scan(f"{stage_prefix}_llm_output", output_payload)
    observability.guardrail(output_guardrail)
    guardrail_results = [*result.guardrail_results, input_guardrail, output_guardrail]
    if output_guardrail.blocked:
        return result.model_copy(
            update={
                "guardrail_results": guardrail_results,
                "guardrail_blocked": True,
                "llm_call_count": 1,
                "total_token_count": token_count,
            }
        )

    finding_kind = "data_quality" if result.agent == "DataAnalystAgent" else "risk"
    finding_title = (
        "Watsonx data-quality interpretation"
        if result.agent == "DataAnalystAgent"
        else "Watsonx risk interpretation"
    )
    watsonx_finding = AgentFinding(
        agent=result.agent,
        kind=finding_kind,
        severity="info",
        title=finding_title,
        detail=watsonx_response.executive_summary,
        evidence=[
            f"model={config.watsonx.watsonx_model_id}",
            "summarized deterministic tool observations only",
        ],
        react_steps=result.react_steps,
    )
    return result.model_copy(
        update={
            "findings": [*result.findings, watsonx_finding],
            "guardrail_results": guardrail_results,
            "messages": [*result.messages, f"{result.agent} Watsonx synthesis completed."],
            "llm_call_count": 1,
            "total_token_count": token_count,
        }
    )


def _maybe_synthesize_with_watsonx(
    *,
    request: RwaAnalysisRequest,
    state: AgentState,
    deterministic_views: CommentaryViews,
    consensus_reached: bool,
    config: RwaAgentsConfig,
    guardrails: GuardrailService,
    observability: LocalObservability,
) -> LlmSynthesisResult:
    if not config.uses_watsonx:
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[],
            blocked=False,
            llm_call_count=state["llm_call_count"],
            total_token_count=state["total_token_count"],
            messages=[],
        )

    if not config.watsonx_configured:
        logger.warning(
            "Watsonx provider selected without credentials; using deterministic fallback."
        )
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[],
            blocked=False,
            llm_call_count=state["llm_call_count"],
            total_token_count=state["total_token_count"],
            messages=["Watsonx is not configured; deterministic commentary was used."],
        )

    prompt = _build_watsonx_prompt(
        request=request,
        state=state,
        deterministic_views=deterministic_views,
        consensus_reached=consensus_reached,
    )
    input_guardrail = guardrails.scan("llm_input", prompt)
    observability.guardrail(input_guardrail)
    if input_guardrail.blocked:
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[input_guardrail],
            blocked=True,
            llm_call_count=state["llm_call_count"],
            total_token_count=state["total_token_count"],
            messages=[],
        )

    try:
        watsonx_response = _new_watsonx_client(config).chat(prompt)
    except WatsonxResponseError as exc:
        llm_call_count, total_token_count = _record_failed_watsonx_response(
            state=state,
            config=config,
            observability=observability,
            error=exc,
        )
        output_guardrail = guardrails.scan(
            "llm_output",
            exc.raw_text or "Malformed watsonx response was rejected before state update.",
        )
        observability.guardrail(output_guardrail)
        if output_guardrail.blocked:
            return LlmSynthesisResult(
                views=deterministic_views,
                guardrail_results=[input_guardrail, output_guardrail],
                blocked=True,
                llm_call_count=llm_call_count,
                total_token_count=total_token_count,
                messages=[],
            )
        logger.warning("Watsonx returned malformed commentary; using deterministic fallback.")
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[input_guardrail, output_guardrail],
            blocked=False,
            llm_call_count=llm_call_count,
            total_token_count=total_token_count,
            messages=["Watsonx response was not structured; deterministic commentary was used."],
        )
    except WatsonxError as exc:
        logger.warning(
            "Watsonx synthesis unavailable; using deterministic fallback: %s",
            type(exc).__name__,
        )
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[input_guardrail],
            blocked=False,
            llm_call_count=state["llm_call_count"],
            total_token_count=state["total_token_count"],
            messages=["Watsonx synthesis unavailable; deterministic commentary was used."],
        )
    except Exception as exc:
        logger.warning(
            "Watsonx provider initialization failed; using deterministic fallback: %s",
            type(exc).__name__,
        )
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[input_guardrail],
            blocked=False,
            llm_call_count=state["llm_call_count"],
            total_token_count=state["total_token_count"],
            messages=["Watsonx synthesis unavailable; deterministic commentary was used."],
        )

    llm_call_count, total_token_count = _record_successful_watsonx_response(
        state=state,
        config=config,
        observability=observability,
        response=watsonx_response,
    )
    output_guardrail = guardrails.scan(
        "llm_output",
        {
            "executive_summary": watsonx_response.executive_summary,
            "cro_view": watsonx_response.cro_view,
            "cfo_view": watsonx_response.cfo_view,
        },
    )
    observability.guardrail(output_guardrail)
    if output_guardrail.blocked:
        return LlmSynthesisResult(
            views=deterministic_views,
            guardrail_results=[input_guardrail, output_guardrail],
            blocked=True,
            llm_call_count=llm_call_count,
            total_token_count=total_token_count,
            messages=[],
        )

    return LlmSynthesisResult(
        views=CommentaryViews(
            executive_summary=watsonx_response.executive_summary,
            cro_view=watsonx_response.cro_view,
            cfo_view=watsonx_response.cfo_view,
        ),
        guardrail_results=[input_guardrail, output_guardrail],
        blocked=False,
        llm_call_count=llm_call_count,
        total_token_count=total_token_count,
        messages=["Watsonx supervisor synthesis completed."],
    )


def _new_watsonx_client(config: RwaAgentsConfig) -> WatsonxClient:
    return WatsonxClient(
        project_id=config.watsonx.watsonx_project_id or "",
        api_key=config.watsonx.watsonx_apikey or "",
        url=config.watsonx.watsonx_url,
        model_id=config.watsonx.watsonx_model_id,
        api_version=config.watsonx.watsonx_api_version,
        max_new_tokens=config.watsonx.watsonx_max_new_tokens,
        time_limit=config.watsonx.watsonx_time_limit,
        http_timeout=config.watsonx.watsonx_http_timeout,
    )


def _record_successful_worker_watsonx_response(
    *,
    config: RwaAgentsConfig,
    observability: LocalObservability,
    response: WatsonxResponse,
) -> int:
    token_count = response.token_usage.total_tokens
    observability.llm(
        provider="watsonx",
        model_id=config.watsonx.watsonx_model_id,
        token_count=token_count,
    )
    return token_count


def _record_worker_failed_watsonx_response(
    *,
    config: RwaAgentsConfig,
    observability: LocalObservability,
    error: WatsonxResponseError,
) -> int:
    token_count = error.token_usage.total_tokens if error.token_usage is not None else 0
    observability.llm(
        provider="watsonx",
        model_id=config.watsonx.watsonx_model_id,
        token_count=token_count,
    )
    return token_count


def _record_successful_watsonx_response(
    *,
    state: AgentState,
    config: RwaAgentsConfig,
    observability: LocalObservability,
    response: WatsonxResponse,
) -> tuple[int, int]:
    token_count = response.token_usage.total_tokens
    observability.llm(
        provider="watsonx",
        model_id=config.watsonx.watsonx_model_id,
        token_count=token_count,
    )
    return state["llm_call_count"] + 1, state["total_token_count"] + token_count


def _record_failed_watsonx_response(
    *,
    state: AgentState,
    config: RwaAgentsConfig,
    observability: LocalObservability,
    error: WatsonxResponseError,
) -> tuple[int, int]:
    token_count = error.token_usage.total_tokens if error.token_usage is not None else 0
    observability.llm(
        provider="watsonx",
        model_id=config.watsonx.watsonx_model_id,
        token_count=token_count,
    )
    return state["llm_call_count"] + 1, state["total_token_count"] + token_count


def _build_worker_watsonx_prompt(
    *,
    request: RwaAnalysisRequest,
    result: WorkerAnalysisResult,
) -> str:
    severity_counts = Counter(flag.severity for flag in result.validation_flags)
    flag_code_counts = Counter(flag.code for flag in result.validation_flags)
    finding_titles = [finding.title for finding in result.findings[:8]]
    action_priorities = Counter(action.priority for action in result.recommended_actions)
    failed_validations = sum(1 for item in result.quantitative_validation if not item.passed)
    return "\n".join(
        [
            f"You are {result.agent} in a guarded RWA multi-agent workflow.",
            "Use only summarized deterministic tool observations below.",
            "Do not calculate RWA formulas; Python tools already performed quantitative checks.",
            "Do not request or infer direct customer, counterparty, account, or personal data.",
            "Return valid JSON only with executive_summary, cro_view, and cfo_view.",
            "Each returned field must be written in English as 3-5 newline-separated bullets.",
            "Start every bullet with '- ' and explain the agent's situation assessment.",
            "",
            "Summarized worker facts:",
            f"- generation_request_id: {request.request_id}",
            f"- input_record_count: {len(request.rwa_input_data)}",
            f"- output_record_count: {len(request.rwa_output_results)}",
            f"- agent: {result.agent}",
            f"- finding_count: {len(result.findings)}",
            f"- finding_titles: {finding_titles}",
            f"- validation_severity_counts: {dict(severity_counts)}",
            f"- validation_code_counts: {dict(flag_code_counts)}",
            f"- recommended_action_count: {len(result.recommended_actions)}",
            f"- recommended_action_priorities: {dict(action_priorities)}",
            f"- quantitative_validation_count: {len(result.quantitative_validation)}",
            f"- failed_quantitative_validation_count: {failed_validations}",
            "",
            "Write an agent interpretation for the supervisor with practical RWA "
            "review implications.",
            "Raw portfolio rows and direct identifiers are intentionally not provided.",
        ]
    )


def _build_watsonx_prompt(
    *,
    request: RwaAnalysisRequest,
    state: AgentState,
    deterministic_views: CommentaryViews,
    consensus_reached: bool,
) -> str:
    severity_counts = Counter(flag.severity for flag in state["validation_flags"])
    flag_code_counts = Counter(flag.code for flag in state["validation_flags"])
    action_priorities = Counter(action.priority for action in state["recommended_actions"])
    finding_titles = [finding.title for finding in state["agent_findings"][:8]]
    data_finding_summaries = _summarize_findings(
        [finding for finding in state["agent_findings"] if finding.agent == "DataAnalystAgent"]
    )
    risk_finding_summaries = _summarize_findings(
        [finding for finding in state["agent_findings"] if finding.agent == "RiskExpertAgent"]
    )
    validation_flag_summaries = _summarize_flags(state["validation_flags"])
    recommended_action_summaries = [
        f"{action.label} (owner: {action.owner}, priority: {action.priority})"
        for action in state["recommended_actions"][:8]
    ]
    total_exposure = _sum_decimal(
        record.exposure_amount for record in request.rwa_input_data if record.exposure_amount > 0
    )
    total_rwa = _sum_decimal(record.rwa_amount for record in request.rwa_output_results)
    failed_validations = sum(1 for item in state["quantitative_validation"] if not item.passed)

    return "\n".join(
        [
            "Synthesize executive-ready RWA commentary for bank reviewers.",
            "Use only the summarized facts below. Do not invent facts.",
            "Do not calculate RWA formulas; deterministic Python tools already did that.",
            "Rewrite the deterministic baseline into fresh stakeholder narrative.",
            "Do not copy deterministic baseline sentences verbatim.",
            "Use PLN as the monetary unit for RWA and exposure amounts.",
            "Avoid unsupported value judgements; stay within supplied validation facts.",
            "Return valid JSON only with executive_summary, cro_view, and cfo_view.",
            "Each JSON field must be a detailed English bullet list with 4-6 bullets.",
            "Start every bullet with '- ' and separate bullets with newline characters.",
            "Executive summary bullets should cover portfolio size, validation posture, "
            "agent findings, management implication, and reporting readiness.",
            "CRO view bullets should cover data quality, risk drivers, validation flags, "
            "controls, and required review focus.",
            "CFO view bullets should cover RWA amount, capital/reporting implication, "
            "action priorities, and financial governance readiness.",
            "",
            "Summarized deterministic facts:",
            f"- generation_request_id: {request.request_id}",
            f"- input_record_count: {len(request.rwa_input_data)}",
            f"- output_record_count: {len(request.rwa_output_results)}",
            f"- total_positive_exposure: {total_exposure:.2f}",
            f"- total_reported_rwa: {total_rwa:.2f}",
            f"- analysis_loop_count: {state['loop_count']}",
            f"- consensus_reached: {consensus_reached}",
            f"- validation_severity_counts: {dict(severity_counts)}",
            f"- validation_code_counts: {dict(flag_code_counts)}",
            f"- quantitative_validation_count: {len(state['quantitative_validation'])}",
            f"- failed_quantitative_validation_count: {failed_validations}",
            f"- finding_titles: {finding_titles}",
            f"- data_finding_summaries: {data_finding_summaries}",
            f"- risk_finding_summaries: {risk_finding_summaries}",
            f"- validation_flag_summaries: {validation_flag_summaries}",
            f"- recommended_action_count: {len(state['recommended_actions'])}",
            f"- recommended_action_priorities: {dict(action_priorities)}",
            f"- recommended_action_summaries: {recommended_action_summaries}",
            "",
            "Deterministic baseline commentary:",
            f"- executive_summary: {deterministic_views.executive_summary}",
            f"- cro_view: {deterministic_views.cro_view}",
            f"- cfo_view: {deterministic_views.cfo_view}",
            "",
            "Raw portfolio rows and direct identifiers are intentionally not provided.",
        ]
    )


def _sum_decimal(values: Iterable[Decimal]) -> Decimal:
    total = Decimal("0")
    for value in values:
        total += value
    return total


def _summarize_findings(findings: list[AgentFinding]) -> list[str]:
    return [f"{finding.title}: {finding.detail}" for finding in findings[:8]]


def _summarize_flags(flags: list[ValidationFlag]) -> list[str]:
    return [f"{flag.code} ({flag.severity}): {flag.message}" for flag in flags[:8]]


def _request_validation_summary(request: RwaAnalysisRequest) -> dict[str, Any]:
    """Build a compact anonymized request summary for guardrail scanning."""
    return {
        "request_id": request.request_id,
        "input_record_count": len(request.rwa_input_data),
        "output_record_count": len(request.rwa_output_results),
        "asset_classes": sorted({record.asset_class for record in request.rwa_input_data})[:20],
        "sectors": sorted({record.sector for record in request.rwa_input_data})[:20],
        "approaches": sorted(
            {record.approach for record in request.rwa_input_data if record.approach}
        )[:20],
        "input_fields": sorted(RwaAnalysisRequest.model_fields.keys()),
        "asset_id_prefixes": sorted(
            {record.asset_id.split("-", 1)[0] for record in request.rwa_input_data}
        ),
    }


def _synthesize_views(
    request: RwaAnalysisRequest,
    findings: list[AgentFinding],
    flags: list[ValidationFlag],
    actions: list[RecommendedAction],
) -> CommentaryViews:
    total_exposure = sum(
        record.exposure_amount for record in request.rwa_input_data if record.exposure_amount > 0
    )
    total_rwa = sum(record.rwa_amount for record in request.rwa_output_results)
    critical_count = sum(1 for flag in flags if flag.severity == "critical")
    warning_count = sum(1 for flag in flags if flag.severity == "warning")
    data_findings = [finding for finding in findings if finding.agent == "DataAnalystAgent"]
    risk_findings = [finding for finding in findings if finding.agent == "RiskExpertAgent"]
    top_finding = findings[0].title if findings else "No material findings"
    action_count = len(actions)
    failed_action_text = (
        "No open remediation actions were generated by the agents."
        if not actions
        else f"{action_count} remediation actions require ownership and tracking."
    )
    data_signal = (
        _humanize_finding(data_findings[0])
        if data_findings
        else "Data quality checks did not produce material exceptions."
    )
    risk_signal = (
        _humanize_finding(risk_findings[0])
        if risk_findings
        else "Risk review did not identify a dominant unresolved risk exception."
    )
    validation_signal = (
        "Deterministic validation completed with no critical or warning flags."
        if critical_count == 0 and warning_count == 0
        else (
            f"Deterministic validation produced {critical_count} critical and "
            f"{warning_count} warning flags."
        )
    )
    return CommentaryViews(
        executive_summary="\n".join(
            [
                (
                    f"- Submitted portfolio RWA is {total_rwa:.2f} PLN against positive "
                    f"exposure of {total_exposure:.2f} PLN."
                ),
                (
                    "- The agent workflow completed its compact DataAnalystAgent and "
                    f"RiskExpertAgent review; headline signal: {top_finding}."
                ),
                f"- {validation_signal}",
                f"- {data_signal}",
                f"- {risk_signal}",
                f"- {failed_action_text}",
            ]
        ),
        cro_view="\n".join(
            [
                f"- Data quality posture: {data_signal}",
                f"- Risk driver posture: {risk_signal}",
                f"- Validation control status: {validation_signal}",
                (
                    "- Quantitative RWA checks were performed by deterministic Python "
                    "tools before narrative synthesis."
                ),
                (
                    "- CRO attention should remain on unresolved critical flags before "
                    "consensus is treated as reporting-ready."
                    if critical_count
                    else (
                        "- CRO attention can focus on monitoring concentration and "
                        "validation evidence rather than emergency remediation."
                    )
                ),
            ]
        ),
        cfo_view="\n".join(
            [
                (
                    f"- Financial reporting baseline uses submitted RWA of "
                    f"{total_rwa:.2f} PLN and positive exposure of {total_exposure:.2f} PLN."
                ),
                f"- Management action load: {failed_action_text}",
                (
                    "- Capital reporting is not ready for clean executive sign-off until "
                    "critical validation flags are resolved."
                    if critical_count
                    else (
                        "- Capital reporting can proceed with the current validation "
                        "evidence if business owners accept the documented assumptions."
                    )
                ),
                (
                    "- The commentary does not rely on LLM-native RWA calculations; "
                    "formula validation remains deterministic and auditable."
                ),
                (
                    "- CFO review should use the validation flags and agent findings to "
                    "decide whether additional management buffer commentary is needed."
                ),
            ]
        ),
    )


def _humanize_finding(finding: AgentFinding) -> str:
    return f"{finding.title} - {finding.detail}"


def _blocked_commentary(
    request: RwaAnalysisRequest,
    observability: LocalObservability,
    messages: list[str],
) -> FinalCommentary:
    views = CommentaryViews(
        executive_summary="Commentary generation was blocked by safety controls.",
        cro_view="Guardrails prevented unsafe content from entering the workflow state.",
        cfo_view=(
            "No generated commentary is available for reporting until the blocked input "
            "is remediated."
        ),
    )
    final = FinalCommentary(
        status="BLOCKED",
        consensus_reached=False,
        loop_count=0,
        executive_summary=views.executive_summary,
        cro_view=views.cro_view,
        cfo_view=views.cfo_view,
        source_agents=[],
        messages=messages,
    )
    observability.score("safety", 1.0, "Unsafe output was blocked before response.")
    final.observability = observability.metadata
    return final


def _response(
    request: RwaAnalysisRequest,
    final: FinalCommentary,
    flags: list[ValidationFlag],
    findings: list[AgentFinding],
    actions: list[RecommendedAction],
    views: CommentaryViews,
    observability: object,
) -> RwaAnalysisResponse:
    return RwaAnalysisResponse(
        request_id=request.request_id,
        run_id=request.request_id,
        status=final.status,
        final_commentary=final,
        messages=final.messages,
        validation_flags=flags,
        agent_findings=findings,
        recommended_actions=actions,
        commentary_views=views,
        observability=observability,
    )
