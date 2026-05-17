from __future__ import annotations

import threading
from decimal import Decimal

from rwa_agents.config import GuardrailConfig
from rwa_agents.guardrails import GuardrailService
from rwa_agents.prompts import DATA_ANALYST_PROMPT, RISK_EXPERT_PROMPT, SUPERVISOR_PROMPT
from rwa_agents.schemas import (
    AgentFinding,
    FinalCommentary,
    QuantitativeValidationItem,
    ReactStep,
    RecommendedAction,
    RwaAnalysisRequest,
    ValidationFlag,
    WorkerAnalysisResult,
)
from rwa_agents.workflow import CHECKPOINTER, run_rwa_analysis

from .test_validation import valid_payload


def test_workflow_returns_structured_commentary_for_valid_request() -> None:
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert response.graph_backend == "langgraph"
    assert response.final_commentary.status == "COMPLETED"
    assert response.final_commentary.consensus_reached is True
    assert response.final_commentary.loop_count == 1
    assert response.final_commentary.executive_summary
    assert response.final_commentary.cro_view
    assert response.final_commentary.cfo_view
    assert response.final_commentary.quantitative_validation[0].passed is True
    assert response.observability.checkpointer == "MemorySaver"
    assert response.observability.thread_id == request.request_id
    assert response.observability.node_transition_count >= 8
    assert response.observability.tool_call_count == 2
    assert response.observability.guardrail_results
    assert {result.affected_node for result in response.observability.guardrail_results} >= {
        "RequestValidation",
        "DataAnalystAgent",
        "RiskExpertAgent",
        "AnalysisFanIn",
        "SupervisorAgent",
        "FinalOutputGuard",
    }
    assert {usage.prompt_name for usage in response.observability.prompt_usages} == {
        DATA_ANALYST_PROMPT,
        RISK_EXPERT_PROMPT,
        SUPERVISOR_PROMPT,
    }
    assert {usage.source for usage in response.observability.prompt_usages} == {"local_fallback"}


def test_workflow_records_internal_react_steps_on_structured_findings() -> None:
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.agent_findings
    for finding in response.agent_findings:
        assert [step.phase for step in finding.react_steps] == [
            "inspect_state",
            "select_tool",
            "execute_tool",
            "observe_result",
            "emit_finding",
        ]
    assert {
        step.tool_name
        for finding in response.agent_findings
        for step in finding.react_steps
        if step.tool_name
    } >= {"DataTools", "RiskTools"}


def test_analysis_phase_runs_workers_in_parallel(monkeypatch) -> None:
    barrier = threading.Barrier(2, timeout=1.0)
    barrier_results: list[bool] = []

    react_steps = [
        ReactStep(
            phase="inspect_state",
            action="inspect",
            observation="test state inspected",
        ),
        ReactStep(
            phase="select_tool",
            tool_name="TestTools",
            action="select",
            observation="test action selected",
        ),
        ReactStep(
            phase="execute_tool",
            tool_name="TestTools",
            action="execute",
            observation="test action executed",
        ),
        ReactStep(
            phase="observe_result",
            tool_name="TestTools",
            action="observe",
            observation="test result observed",
        ),
        ReactStep(
            phase="emit_finding",
            action="emit",
            observation="test finding emitted",
        ),
    ]

    def wait_for_peer() -> None:
        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            barrier_results.append(False)
        else:
            barrier_results.append(True)

    def slow_data_agent(request: RwaAnalysisRequest) -> WorkerAnalysisResult:
        wait_for_peer()
        return WorkerAnalysisResult(
            agent="DataAnalystAgent",
            findings=[
                AgentFinding(
                    agent="DataAnalystAgent",
                    kind="data_quality",
                    severity="info",
                    title="Data checks completed",
                    detail=f"{len(request.rwa_input_data)} inputs checked",
                    react_steps=react_steps,
                )
            ],
            react_steps=react_steps,
        )

    def slow_risk_agent(request: RwaAnalysisRequest) -> WorkerAnalysisResult:
        wait_for_peer()
        return WorkerAnalysisResult(
            agent="RiskExpertAgent",
            findings=[
                AgentFinding(
                    agent="RiskExpertAgent",
                    kind="validation",
                    severity="info",
                    title="Risk checks completed",
                    detail=f"{len(request.rwa_output_results)} outputs checked",
                    react_steps=react_steps,
                )
            ],
            quantitative_validation=[
                QuantitativeValidationItem(
                    asset_id="ASSET-001",
                    expected_rwa_amount=Decimal("500"),
                    reported_rwa_amount=Decimal("500"),
                    variance_amount=Decimal("0"),
                    variance_pct=Decimal("0"),
                    passed=True,
                )
            ],
            react_steps=react_steps,
        )

    monkeypatch.setattr("rwa_agents.workflow.analyze_data_quality", slow_data_agent)
    monkeypatch.setattr("rwa_agents.workflow.analyze_risk", slow_risk_agent)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert barrier_results == [True, True]


def test_workflow_uses_loop_limit_for_unresolved_critical_flags() -> None:
    payload = valid_payload()
    payload["rwa_output_results"][0]["rwa_amount"] = "700"
    request = RwaAnalysisRequest.model_validate(payload)

    response = run_rwa_analysis(request)

    assert response.status == "LOOP_LIMIT_REACHED"
    assert response.final_commentary.loop_count == 2
    assert response.final_commentary.consensus_reached is False
    assert response.validation_flags[0].code == "RWA_RECALCULATION_VARIANCE"


def test_unsafe_final_output_is_blocked_without_writing_unsafe_commentary(
    monkeypatch,
) -> None:
    payload = valid_payload()
    request = RwaAnalysisRequest.model_validate(payload)

    def unsafe_views(*args, **kwargs):
        from rwa_agents.schemas import CommentaryViews

        _ = args, kwargs
        return CommentaryViews(
            executive_summary="Contact jane.client@example.com for details.",
            cro_view="Contact jane.client@example.com for details.",
            cfo_view="Contact jane.client@example.com for details.",
        )

    monkeypatch.setattr("rwa_agents.workflow._synthesize_views", unsafe_views)

    response = run_rwa_analysis(request)

    assert response.status == "BLOCKED"
    assert response.final_commentary.status == "BLOCKED"
    assert "jane.client@example.com" not in response.final_commentary.executive_summary
    assert response.observability.guardrail_block_count >= 1


def test_final_output_guard_scans_complete_commentary_payload(monkeypatch) -> None:
    scanned_payloads: list[str] = []
    original_scan = GuardrailService.scan

    def spy_scan(self: GuardrailService, stage: str, payload: object):
        if stage == "final_output" and hasattr(payload, "model_dump_json"):
            scanned_payloads.append(payload.model_dump_json())
        return original_scan(self, stage, payload)

    monkeypatch.setattr(GuardrailService, "scan", spy_scan)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert scanned_payloads
    scanned_text = scanned_payloads[0]
    assert "executive_summary" in scanned_text
    assert "cro_view" in scanned_text
    assert "cfo_view" in scanned_text
    assert "data_quality_observations" in scanned_text
    assert "risk_observations" in scanned_text
    assert "quantitative_validation" in scanned_text
    assert "recommended_actions" in scanned_text
    assert "validation_flags" in scanned_text


def test_local_final_output_guard_blocks_unsafe_structured_fields() -> None:
    guardrails = GuardrailService(GuardrailConfig(llm_guard_enabled=False))
    unsafe_email = "jane.client@example.com"
    final = FinalCommentary(
        status="COMPLETED",
        consensus_reached=True,
        loop_count=1,
        executive_summary="Safe summary.",
        cro_view="Safe CRO view.",
        cfo_view="Safe CFO view.",
        data_quality_observations=[
            AgentFinding(
                agent="DataAnalystAgent",
                kind="data_quality",
                severity="warning",
                title="Unsafe observation",
                detail=f"Review {unsafe_email}",
            )
        ],
        risk_observations=[],
        quantitative_validation=[
            QuantitativeValidationItem(
                asset_id="ASSET-001",
                expected_rwa_amount=Decimal("500"),
                reported_rwa_amount=Decimal("500"),
                variance_amount=Decimal("0"),
                variance_pct=Decimal("0"),
                passed=True,
            )
        ],
        recommended_actions=[
            RecommendedAction(
                id="unsafe-action",
                label=f"Contact {unsafe_email}",
                owner="Risk",
                priority="high",
                source_agent="SupervisorAgent",
            )
        ],
        validation_flags=[
            ValidationFlag(
                code="UNSAFE_FLAG",
                severity="critical",
                message=f"Unsafe flag mentions {unsafe_email}",
                source_agent="SupervisorAgent",
                requires_human_intervention=True,
            )
        ],
        source_agents=["DataAnalystAgent", "RiskExpertAgent"],
    )

    result = guardrails.scan("final_output", final)

    assert result.blocked is True
    assert result.stage == "final_output"
    assert "pii" in result.categories


def test_state_is_checkpointed_by_thread_id() -> None:
    request = RwaAnalysisRequest.model_validate(valid_payload())

    run_rwa_analysis(request)

    checkpoint = CHECKPOINTER.get(request.request_id)
    assert checkpoint is not None
    assert checkpoint["request_id"] == request.request_id
