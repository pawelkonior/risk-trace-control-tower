from __future__ import annotations

from rwa_agents.schemas import RwaAnalysisRequest
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
