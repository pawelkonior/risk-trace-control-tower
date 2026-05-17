from __future__ import annotations

import threading
from decimal import Decimal

from rwa_agents.schemas import (
    AgentFinding,
    QuantitativeValidationItem,
    ReactStep,
    RwaAnalysisRequest,
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
    assert response.observability.tool_call_count == 2
    assert response.observability.guardrail_results


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


def test_state_is_checkpointed_by_thread_id() -> None:
    request = RwaAnalysisRequest.model_validate(valid_payload())

    run_rwa_analysis(request)

    checkpoint = CHECKPOINTER.get(request.request_id)
    assert checkpoint is not None
    assert checkpoint["request_id"] == request.request_id
