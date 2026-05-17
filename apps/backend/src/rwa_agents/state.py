from __future__ import annotations

from typing import TypedDict

from .schemas import (
    AgentFinding,
    CommentaryViews,
    FinalCommentary,
    GuardrailResult,
    RecommendedAction,
    RwaInputRecord,
    RwaOutputRecord,
    ValidationFlag,
)


class AgentState(TypedDict):
    request_id: str
    rwa_input_data: list[RwaInputRecord]
    rwa_output_results: list[RwaOutputRecord]
    messages: list[str]
    validation_flags: list[ValidationFlag]
    agent_findings: list[AgentFinding]
    recommended_actions: list[RecommendedAction]
    commentary_views: CommentaryViews
    guardrail_results: list[GuardrailResult]
    loop_count: int
    loop_limit: int
    consensus_reached: bool
    final_commentary: FinalCommentary | None
    next_agent: str | None
    guardrail_blocked: bool
