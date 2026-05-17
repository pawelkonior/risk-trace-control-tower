from __future__ import annotations

import warnings
from typing import Any

from langgraph.graph import END, START, StateGraph

from .checkpointing import MemorySaverCheckpoint
from .config import RwaAgentsConfig
from .guardrails import GuardrailService
from .observability import LocalObservability
from .prompts import PromptRegistry
from .schemas import (
    AgentFinding,
    CommentaryViews,
    FinalCommentary,
    RecommendedAction,
    RwaAnalysisRequest,
    RwaAnalysisResponse,
    ValidationFlag,
    WorkerAnalysisResult,
)
from .state import AgentState
from .tools import analyze_data_quality, analyze_risk
from .validation import build_agent_state

CHECKPOINTER = MemorySaverCheckpoint()


def run_rwa_analysis(request: RwaAnalysisRequest) -> RwaAnalysisResponse:
    config = RwaAgentsConfig.from_env()
    guardrails = GuardrailService(config.guardrails)
    prompts = PromptRegistry(config.langfuse)
    observability = LocalObservability(request.request_id, config.langfuse)
    observability.node("RequestValidation")
    input_guardrail = guardrails.scan("request_validation", request)
    observability.guardrail(input_guardrail)
    if input_guardrail.blocked:
        final = _blocked_commentary(request, observability, ["Input guardrail blocked request."])
        observability.finalize()
        return _response(request, final, [], [], [], CommentaryViews(), observability.metadata)

    initial_state = build_agent_state(request)
    observability.node("AgentStateBuilt")
    CHECKPOINTER.put(request.request_id, dict(initial_state))

    graph = _build_graph(request, guardrails, prompts, observability)
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
    guardrails: GuardrailService,
    prompts: PromptRegistry,
    observability: LocalObservability,
) -> Any:
    builder = StateGraph(AgentState)

    def analysis_phase(state: AgentState) -> dict:
        observability.node("AnalysisPhase")
        data_prompt, data_usage = prompts.get("data_analyst")
        risk_prompt, risk_usage = prompts.get("risk_expert")
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
        observability.tool("DataTools")
        result = analyze_data_quality(request)
        return {"data_agent_result": result}

    def risk_expert_agent(_state: AgentState) -> dict:
        observability.tool("RiskTools")
        result = analyze_risk(request)
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
        if worker_guardrail.blocked:
            return {
                "guardrail_results": [*state["guardrail_results"], worker_guardrail],
                "guardrail_blocked": True,
            }
        return {
            "messages": [*state["messages"], "Parallel LangGraph worker analysis completed."],
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
            "guardrail_results": [*state["guardrail_results"], worker_guardrail],
        }

    def supervisor_agent(state: AgentState) -> dict:
        observability.node("SupervisorAgent")
        supervisor_prompt, supervisor_usage = prompts.get("supervisor")
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
        return {
            "commentary_views": views,
            "consensus_reached": consensus_reached,
            "guardrail_results": [*state["guardrail_results"], supervisor_guardrail],
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
        # Compute all required evaluation scores
        observability.compute_final_scores(dict(state))
        final.observability = observability.metadata
        return {
            "final_commentary": final,
            "guardrail_results": [*state["guardrail_results"], final_guardrail],
            "next_agent": "FinalStructuredResponse",
        }

    def guardrail_blocked(_state: AgentState) -> dict:
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
    top_finding = findings[0].title if findings else "No material findings"
    action_count = len(actions)
    return CommentaryViews(
        executive_summary=(
            f"Submitted portfolio RWA is {total_rwa:.2f} against positive exposure "
            f"{total_exposure:.2f}. {top_finding}. Validation produced {critical_count} "
            f"critical and {warning_count} warning flags, with {action_count} "
            "recommended actions."
        ),
        cro_view=(
            f"Risk review should focus on {critical_count} critical validation flags and "
            f"{warning_count} warning indicators. Deterministic checks were completed before "
            "commentary synthesis, and unresolved critical flags keep consensus open."
        ),
        cfo_view=(
            f"Capital commentary is grounded in reported RWA of {total_rwa:.2f}. "
            f"Management actions outstanding: {action_count}. Use the validation flags to "
            "decide whether the movement is ready for executive reporting."
        ),
    )


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
