from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


def to_camel(value: str) -> str:
    """Convert Python field names to the React API camelCase contract."""
    first, *rest = value.split("_")
    return first + "".join(part.capitalize() for part in rest)


class UiSchema(BaseModel):
    """Base schema for frontend-facing RiskTrace contracts."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class UserContext(UiSchema):
    initials: str
    name: str
    role: str
    last_login: str


class SystemStatusItem(UiSchema):
    label: str
    value: str


class HomeViewSummary(UiSchema):
    view: Literal["dashboard", "lineage", "briefing"]
    description: str
    metric: str
    status: str
    tone: Literal["blue", "teal", "purple"]


class NotificationItem(UiSchema):
    id: str
    title: str
    detail: str
    tone: Literal["blue", "amber", "red", "green"]
    created_at: str
    read: bool = False


class ReportingCalendar(UiSchema):
    reporting_date: date
    month_label: str
    locked_reason: str
    available_dates: list[date]


class HelpItem(UiSchema):
    id: str
    title: str
    detail: str
    action_id: str


class UserMenuItem(UiSchema):
    id: str
    label: str
    detail: str
    action_id: str


class AppContext(UiSchema):
    app_name: str
    environment: str
    reporting_date: date
    comparison_label: str | None = None
    user: UserContext
    system_status: list[SystemStatusItem]
    home_cards: list[HomeViewSummary]
    reporting_calendar: ReportingCalendar
    help_items: list[HelpItem]
    user_menu: list[UserMenuItem]
    notification_count: int
    notifications: list[NotificationItem]


class DashboardFilters(UiSchema):
    period: str = "Current"
    scenario: str = "Base Case"
    business_unit: str = "All"
    currency: str = "PLN"


class DashboardFilterOptions(UiSchema):
    periods: list[str]
    scenarios: list[str]
    business_units: list[str]
    currencies: list[str]


class DashboardMetric(UiSchema):
    label: str
    value: str
    unit: str | None = None
    compare_label: str
    delta: str
    delta_direction: Literal["up", "down"]
    accent: Literal["blue", "purple", "teal", "green", "amber"]
    icon: str
    show_info_icon: bool | None = None


class CapitalSummary(UiSchema):
    currency: str
    rows_top: list[tuple[str, str]]
    ratios: list[tuple[str, str]]
    minimum_requirement: str
    capital_buffer: str


class TopExposure(UiSchema):
    id: str
    name: str
    amount: str
    pct: str
    bar: int


class ExposureClassPoint(UiSchema):
    label: str
    pct: str
    amount: str
    value: float
    color: str


class RwaTrendPoint(UiSchema):
    label: str
    value: float


class RatingRwaPoint(UiSchema):
    rating: str
    amount: str
    pct: str
    bar: int


class CountryRwaPoint(UiSchema):
    country: str
    amount: str
    pct: str
    color: str


class DashboardAlert(UiSchema):
    count: int
    label: str
    tone: Literal["red", "orange", "amber", "blue"]
    icon: str


class DashboardSnapshot(UiSchema):
    generated_at: datetime
    as_of_date: date
    currency: str
    total_rwa_amount: str
    filters: DashboardFilters | None = None
    filter_options: DashboardFilterOptions
    metrics: list[DashboardMetric]
    capital_summary: CapitalSummary
    top_exposures: list[TopExposure]
    exposure_class: list[ExposureClassPoint]
    rwa_trend: list[RwaTrendPoint]
    rating_rwa: list[RatingRwaPoint]
    country_rwa: list[CountryRwaPoint]
    alerts: list[DashboardAlert]


class LineageTrace(UiSchema):
    trace_id: str
    exposure_id: str
    source_system: str
    source_record_id: str
    input_hash: str
    rule_version: str
    regulation_reference: str
    reporting_date: date
    timestamp: str
    rwa_amount: str


class LineageNode(UiSchema):
    id: str
    layer: str
    title: str
    icon: str
    tone: Literal["source", "ingestion", "validation", "rule", "calculation", "reporting"]
    details: list[tuple[str, str]]
    status: str


class TransformationStep(UiSchema):
    step: int
    service: str
    description: str
    input_records: str
    output_records: str
    duration: str
    status: str
    executed_at: str


class LineageArtifact(UiSchema):
    label: str
    count: int
    icon: str


class LineageTotals(UiSchema):
    duration: str
    total_input_records: str
    total_output_records: str


class LineageDirection(UiSchema):
    title: str
    value: str
    meta: list[str]
    button_label: str
    icon: str
    action_id: str


class LineageSnapshot(UiSchema):
    trace: LineageTrace
    nodes: list[LineageNode]
    summary: list[tuple[str, str]]
    transformation_steps: list[TransformationStep]
    artifacts: list[LineageArtifact]
    totals: LineageTotals
    directions: list[LineageDirection]


class BriefingKpi(UiSchema):
    label: str
    value: str
    detail: str
    icon: str
    tone: Literal["blue", "purple", "green", "red", "amber", "teal"]


class WaterfallPoint(UiSchema):
    label: str
    axis_label: str
    table_label: str
    base: float
    opening: float
    increase: float
    decrease: float
    closing: float
    display: str
    color: str


class MovementDriver(UiSchema):
    driver: str
    impact: str
    change_pct: str
    color: str


class ReviewPackStat(UiSchema):
    label: str
    value: str
    detail: str
    tone: str


class VarianceReviewItem(UiSchema):
    label: str
    value: str
    share: str
    width: int
    color: str


class ControlChecklistItem(UiSchema):
    label: str
    status: str
    tone: Literal["success", "warning", "neutral"]


class ManualReviewInput(UiSchema):
    label: str
    tone: str
    action_id: str


class RegulatoryWatchItem(UiSchema):
    label: str
    value: str
    status: str


class DataQualityFinding(UiSchema):
    label: str
    value: str


class SimulatorAction(UiSchema):
    action: str
    impact: str
    confidence: Literal["Low", "Medium", "High"]
    owner: str
    action_id: str


class EvidenceItem(UiSchema):
    label: str
    value: str
    icon: str
    tone: Literal["blue", "purple", "green", "red", "amber", "teal"]
    action_id: str


class BoardPack(UiSchema):
    title: str
    description: str
    icon: str
    export_type: str


class CalculatedRwaRow(UiSchema):
    asset_id: str
    entity_class: str
    sector: str
    exposure_amount: str
    risk_weight: str
    rating: str | None = None
    pd: str | None = None
    lgd: str | None = None
    maturity_years: str | None = None
    rwa_amount: str
    approach: str


class MovementAttribution(UiSchema):
    waterfall_data: list[WaterfallPoint]
    movement_drivers: list[MovementDriver]
    total_change: str
    total_change_pct: str


class ManagementReviewPack(UiSchema):
    tabs: list[str]
    stats: list[ReviewPackStat]
    variance_review_items: list[VarianceReviewItem]
    control_checklist: list[ControlChecklistItem]
    manual_review_inputs: list[ManualReviewInput]


class BriefingSnapshot(UiSchema):
    generated_at: datetime
    calculated_rwa_rows: list[CalculatedRwaRow] = Field(default_factory=list)
    kpis: list[BriefingKpi]
    movement_attribution: MovementAttribution
    review_pack: ManagementReviewPack
    regulatory_watch: list[RegulatoryWatchItem]
    data_quality_findings: list[DataQualityFinding]
    simulator_actions: list[SimulatorAction]
    evidence_items: list[EvidenceItem]
    board_pack: BoardPack


class UiActionRequest(UiSchema):
    context: dict[str, Any] = Field(default_factory=dict)
    source: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class UiActionResponse(UiSchema):
    action_id: str
    status: Literal["accepted", "completed"]
    message: str
    category: str
    job_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class ExportRequest(UiSchema):
    context: dict[str, Any] = Field(default_factory=dict)
    source: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class ExportResponse(UiSchema):
    export_type: str
    status: Literal["queued", "completed"]
    job_id: str
    message: str
    created_at: datetime


class SearchResult(UiSchema):
    id: str
    title: str
    category: str
    description: str
    route: str


class SearchResponse(UiSchema):
    query: str
    results: list[SearchResult]
