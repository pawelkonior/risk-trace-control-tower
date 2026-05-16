from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from .checkpointing import MemorySaverCheckpoint
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
)
from .state import AgentState
from .tools import analyze_data_quality, analyze_risk
from .validation import build_agent_state

CHECKPOINTER = MemorySaverCheckpoint()


def run_rwa_analysis(request: RwaAnalysisRequest) -> RwaAnalysisResponse:
    guardrails = GuardrailService()
    prompts = PromptRegistry()
    observability = LocalObservability(request.request_id, prompts.langfuse_enabled)
    observability.node("RequestValidation")
    input_guardrail = guardrails.scan("request_validation", request)
    observability.guardrail(input_guardrail)
    if input_guardrail.blocked:
        final = _blocked_commentary(request, observability, ["Input guardrail blocked request."])
        return _response(request, final, [], [], [], CommentaryViews(), observability.metadata)

    state = build_agent_state(request)
    observability.node("AgentStateBuilt")
    CHECKPOINTER.put(request.request_id, dict(state))

    while state["loop_count"] < state["loop_limit"]:
        state["loop_count"] += 1
        observability.node("AnalysisPhase")
        data_prompt, data_usage = prompts.get("data_analyst")
        risk_prompt, risk_usage = prompts.get("risk_expert")
        observability.prompt(data_usage)
        observability.prompt(risk_usage)
        for stage, prompt in (
            ("data_analyst_prompt", data_prompt),
            ("risk_expert_prompt", risk_prompt),
        ):
            result = guardrails.scan(stage, prompt)
            observability.guardrail(result)
            if result.blocked:
                state["guardrail_blocked"] = True
                state["guardrail_results"].append(result)

        if state["guardrail_blocked"]:
            break

        if state["loop_count"] > 1:
            state["agent_findings"] = []
            state["validation_flags"] = []
            state["recommended_actions"] = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            data_future = executor.submit(analyze_data_quality, request)
            risk_future = executor.submit(analyze_risk, request)
            observability.tool("DataTools")
            observability.tool("RiskTools")
            data_findings, data_flags, data_actions = data_future.result()
            risk_findings, risk_flags, risk_actions, quantitative_validation = risk_future.result()

        observability.node("AnalysisFanIn")
        if _merge_agent_output(
            state,
            guardrails,
            observability,
            "data_analyst_output",
            data_findings,
            data_flags,
            data_actions,
        ) and _merge_agent_output(
            state,
            guardrails,
            observability,
            "risk_expert_output",
            risk_findings,
            risk_flags,
            risk_actions,
        ):
            state["messages"].append("Parallel worker analysis completed.")
        else:
            break

        observability.node("SupervisorAgent")
        supervisor_prompt, supervisor_usage = prompts.get("supervisor")
        observability.prompt(supervisor_usage)
        supervisor_guardrail = guardrails.scan("supervisor_prompt", supervisor_prompt)
        observability.guardrail(supervisor_guardrail)
        if supervisor_guardrail.blocked:
            state["guardrail_blocked"] = True
            break

        critical_flags = [flag for flag in state["validation_flags"] if flag.severity == "critical"]
        state["consensus_reached"] = not critical_flags
        views = _synthesize_views(
            request=request,
            findings=state["agent_findings"],
            flags=state["validation_flags"],
            actions=state["recommended_actions"],
        )
        state["commentary_views"] = views
        status = "COMPLETED" if state["consensus_reached"] else "LOOP_LIMIT_REACHED"
        if not state["consensus_reached"] and state["loop_count"] < state["loop_limit"]:
            state["next_agent"] = "AnalysisPhase"
            CHECKPOINTER.put(request.request_id, dict(state))
            continue

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
            quantitative_validation=quantitative_validation,
            recommended_actions=state["recommended_actions"],
            validation_flags=state["validation_flags"],
            source_agents=sorted({finding.agent for finding in state["agent_findings"]}),
            messages=state["messages"],
        )
        observability.node("FinalOutputGuard")
        final_guardrail = guardrails.scan("final_output", final)
        observability.guardrail(final_guardrail)
        if final_guardrail.blocked:
            state["guardrail_blocked"] = True
            break
        observability.score(
            "groundedness",
            1.0,
            "Commentary is synthesized from deterministic findings.",
        )
        observability.score("faithfulness", 1.0, "Quantitative validation used Python tools only.")
        final.observability = observability.metadata
        state["final_commentary"] = final
        CHECKPOINTER.put(request.request_id, dict(state))
        observability.node("FinalStructuredResponse")
        return _response(
            request,
            final,
            state["validation_flags"],
            state["agent_findings"],
            state["recommended_actions"],
            state["commentary_views"],
            observability.metadata,
        )

    messages = ["Guardrail blocked unsafe workflow output."]
    final = _blocked_commentary(request, observability, messages)
    state["final_commentary"] = final
    state["guardrail_blocked"] = True
    CHECKPOINTER.put(request.request_id, dict(state))
    return _response(
        request,
        final,
        state["validation_flags"],
        state["agent_findings"],
        state["recommended_actions"],
        state["commentary_views"],
        observability.metadata,
    )


def _merge_agent_output(
    state: AgentState,
    guardrails: GuardrailService,
    observability: LocalObservability,
    stage: str,
    findings: list[AgentFinding],
    flags: list[ValidationFlag],
    actions: list[RecommendedAction],
) -> bool:
    result = guardrails.scan(stage, {"findings": findings, "flags": flags, "actions": actions})
    observability.guardrail(result)
    if result.blocked:
        state["guardrail_blocked"] = True
        state["guardrail_results"].append(result)
        return False
    state["agent_findings"].extend(findings)
    state["validation_flags"].extend(flags)
    state["recommended_actions"].extend(actions)
    return True


def _synthesize_views(
    request: RwaAnalysisRequest,
    findings: list[AgentFinding],
    flags: list[ValidationFlag],
    actions: list[RecommendedAction],
) -> CommentaryViews:
    total_exposure = sum(record.exposure_amount for record in request.rwa_input_data)
    total_rwa = sum(record.rwa_amount for record in request.rwa_output_results)
    critical_count = sum(1 for flag in flags if flag.severity == "critical")
    warning_count = sum(1 for flag in flags if flag.severity == "warning")
    top_finding = findings[0].title if findings else "No material findings"
    action_count = len(actions)
    return CommentaryViews(
        executive_summary=(
            f"Submitted portfolio RWA is {total_rwa:.2f} against exposure {total_exposure:.2f}. "
            f"{top_finding}. Validation produced {critical_count} critical and "
            f"{warning_count} warning flags, with {action_count} recommended actions."
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
