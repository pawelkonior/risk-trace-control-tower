from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .privacy import PiiDetectionError, ensure_no_pii

WorkflowStatus = Literal["COMPLETED", "LOOP_LIMIT_REACHED", "BLOCKED"]
FindingSeverity = Literal["info", "warning", "critical"]
FindingKind = Literal["data_quality", "risk", "validation", "guardrail", "observability"]
ActionPriority = Literal["low", "medium", "high"]


class AgentSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class RwaInputRecord(AgentSchema):
    asset_id: str = Field(min_length=3, max_length=80)
    asset_class: str = Field(min_length=1, max_length=80)
    sector: str = Field(min_length=1, max_length=80)
    exposure_amount: Decimal
    risk_weight: Decimal | None = Field(default=None, ge=Decimal("0"), le=Decimal("12"))
    rating: str | None = Field(default=None, max_length=40)
    pd: Decimal | None = None
    lgd: Decimal | None = None
    maturity_years: Decimal | None = Field(default=None, gt=Decimal("0"), le=Decimal("100"))
    approach: str | None = Field(default=None, max_length=80)

    @field_validator("asset_id")
    @classmethod
    def asset_id_must_be_anonymized(cls, value: str) -> str:
        normalized = value.strip().upper()
        allowed_prefixes = ("ASSET-", "EXPOSURE-", "PORTFOLIO-", "RWA-")
        if not normalized.startswith(allowed_prefixes):
            raise ValueError("asset_id must use an anonymized identifier prefix")
        if any(char for char in normalized if not (char.isalnum() or char in "-_")):
            raise ValueError("asset_id contains unsupported characters")
        return normalized


class RwaOutputRecord(AgentSchema):
    asset_id: str = Field(min_length=3, max_length=80)
    rwa_amount: Decimal = Field(ge=Decimal("0"))
    exposure_amount: Decimal | None = Field(default=None, gt=Decimal("0"))
    risk_weight: Decimal | None = Field(default=None, ge=Decimal("0"), le=Decimal("12"))
    approach: str | None = Field(default=None, max_length=80)

    @field_validator("asset_id")
    @classmethod
    def asset_id_must_be_anonymized(cls, value: str) -> str:
        return RwaInputRecord.asset_id_must_be_anonymized(value)


class ValidationFlag(AgentSchema):
    code: str
    severity: FindingSeverity
    message: str
    asset_id: str | None = None
    source_agent: str
    requires_human_intervention: bool = False


class ReactStep(AgentSchema):
    phase: Literal["inspect_state", "select_tool", "execute_tool", "observe_result", "emit_finding"]
    tool_name: str | None = None
    action: str
    observation: str


class AgentFinding(AgentSchema):
    agent: str
    kind: FindingKind
    severity: FindingSeverity
    title: str
    detail: str
    evidence: list[str] = Field(default_factory=list)
    react_steps: list[ReactStep] = Field(default_factory=list)


class RecommendedAction(AgentSchema):
    id: str
    label: str
    owner: str
    priority: ActionPriority
    completed: bool = False
    source_agent: str


class CommentaryViews(AgentSchema):
    executive_summary: str = ""
    cro_view: str = ""
    cfo_view: str = ""


class GuardrailResult(AgentSchema):
    stage: str
    scanner: str = "llm_guard"
    passed: bool
    blocked: bool = False
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    categories: list[str] = Field(default_factory=list)
    message: str = ""


class PromptUsage(AgentSchema):
    prompt_name: str
    prompt_version: str
    source: Literal["local_fallback", "langfuse"]
    label: str | None = None
    fetch_status: str
    fetch_latency_ms: float | None = Field(default=None, ge=0.0)


class EvaluationScore(AgentSchema):
    name: str
    value: float = Field(ge=0.0)
    comment: str


class ObservabilityMetadata(AgentSchema):
    langfuse_enabled: bool = False
    trace_id: str | None = None
    callback_handler_attached: bool = False
    checkpointer: str = "MemorySaver"
    thread_id: str
    prompt_usages: list[PromptUsage] = Field(default_factory=list)
    evaluation_scores: list[EvaluationScore] = Field(default_factory=list)
    guardrail_results: list[GuardrailResult] = Field(default_factory=list)
    guardrail_block_count: int = 0
    pii_detected: bool = False
    prompt_injection_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    node_transition_count: int = 0
    llm_call_count: int = 0
    tool_call_count: int = 0
    total_token_count: int = 0


class QuantitativeValidationItem(AgentSchema):
    asset_id: str
    expected_rwa_amount: Decimal
    reported_rwa_amount: Decimal
    variance_amount: Decimal
    variance_pct: Decimal
    passed: bool


class WorkerAnalysisResult(AgentSchema):
    agent: str
    findings: list[AgentFinding] = Field(default_factory=list)
    validation_flags: list[ValidationFlag] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    quantitative_validation: list[QuantitativeValidationItem] = Field(default_factory=list)
    react_steps: list[ReactStep] = Field(default_factory=list)


class FinalCommentary(AgentSchema):
    status: WorkflowStatus
    consensus_reached: bool
    loop_count: int
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_label: str = "RiskTrace Intelligence"
    executive_summary: str
    cro_view: str
    cfo_view: str
    data_quality_observations: list[AgentFinding] = Field(default_factory=list)
    risk_observations: list[AgentFinding] = Field(default_factory=list)
    quantitative_validation: list[QuantitativeValidationItem] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    validation_flags: list[ValidationFlag] = Field(default_factory=list)
    source_agents: list[str] = Field(default_factory=list)
    observability: ObservabilityMetadata | None = None
    messages: list[str] = Field(default_factory=list)


class RwaAnalysisRequest(AgentSchema):
    request_id: str = Field(min_length=3, max_length=120)
    loop_limit: int = Field(default=2, ge=1, le=2)
    materiality_threshold: Decimal = Field(default=Decimal("0.05"), ge=Decimal("0"))
    rwa_input_data: list[RwaInputRecord] = Field(min_length=1)
    rwa_output_results: list[RwaOutputRecord] = Field(min_length=1)

    @model_validator(mode="before")
    @classmethod
    def reject_pii_before_model_construction(cls, value: Any) -> Any:
        try:
            ensure_no_pii(value)
        except PiiDetectionError as exc:
            raise ValueError(str(exc)) from exc
        return value


class RwaAnalysisResponse(AgentSchema):
    api_version: Literal["v1"] = "v1"
    service_version: str = "0.1.0"
    request_id: str
    run_id: str
    status: WorkflowStatus
    graph_backend: str = "langgraph"
    final_commentary: FinalCommentary
    messages: list[str] = Field(default_factory=list)
    validation_flags: list[ValidationFlag] = Field(default_factory=list)
    agent_findings: list[AgentFinding] = Field(default_factory=list)
    recommended_actions: list[RecommendedAction] = Field(default_factory=list)
    commentary_views: CommentaryViews
    observability: ObservabilityMetadata
