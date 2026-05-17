from __future__ import annotations

from .privacy import ensure_no_pii
from .schemas import CommentaryViews, RwaAnalysisRequest
from .state import AgentState


def build_agent_state(request: RwaAnalysisRequest) -> AgentState:
    """Create graph state only after schema and PII validation have succeeded."""
    ensure_no_pii(request)
    return AgentState(
        request_id=request.request_id,
        rwa_input_data=request.rwa_input_data,
        rwa_output_results=request.rwa_output_results,
        messages=[],
        validation_flags=[],
        agent_findings=[],
        recommended_actions=[],
        commentary_views=CommentaryViews(),
        guardrail_results=[],
        quantitative_validation=[],
        data_agent_result=None,
        risk_agent_result=None,
        loop_count=0,
        loop_limit=request.loop_limit,
        consensus_reached=False,
        final_commentary=None,
        next_agent=None,
        guardrail_blocked=False,
        llm_call_count=0,
        total_token_count=0,
    )
