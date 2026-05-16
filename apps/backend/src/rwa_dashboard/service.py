from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from .repositories import (
    RisktraceActionNotFoundError,
    RisktraceDatasetNotFoundError,
    RisktraceUiRepository,
)
from .schemas import (
    AppContext,
    BriefingSnapshot,
    DashboardFilters,
    DashboardSnapshot,
    ExportResponse,
    LineageSnapshot,
    NotificationItem,
    SearchResponse,
    SearchResult,
    UiActionRequest,
    UiActionResponse,
)


class RisktraceUiService:
    """Application service for all React-facing RiskTrace REST resources."""

    def __init__(self, repository: RisktraceUiRepository) -> None:
        self.repository = repository

    def app_context(self) -> AppContext:
        return AppContext.model_validate(self.repository.get_payload("app_context"))

    def dashboard_snapshot(self, filters: DashboardFilters) -> DashboardSnapshot:
        payload = deepcopy(self.repository.get_payload("dashboard_snapshot"))
        effective_filters = _normalize_dashboard_filters(filters, payload["filterOptions"])
        _apply_dashboard_filters(payload, effective_filters)
        payload["filters"] = effective_filters.model_dump(mode="json", by_alias=True)
        return DashboardSnapshot.model_validate(payload)

    def lineage_trace(self, trace_id: str) -> LineageSnapshot:
        key = f"lineage_trace_{trace_id}"
        return LineageSnapshot.model_validate(self.repository.get_payload(key))

    def briefing_snapshot(self) -> BriefingSnapshot:
        return BriefingSnapshot.model_validate(self.repository.get_payload("briefing_snapshot"))

    def notifications(self) -> list[NotificationItem]:
        return self.app_context().notifications

    def perform_action(self, action_id: str, request: UiActionRequest) -> UiActionResponse:
        action = self.repository.get_action(action_id)
        created_at = datetime.now(UTC)
        job_id = (
            f"{action.job_type or action.action_id}-{uuid4().hex[:10]}" if action.job_type else None
        )
        response_payload: dict[str, Any] = {
            "actionId": action.action_id,
            "status": "accepted",
            "message": action.response_message,
            "category": action.category,
            "jobId": job_id,
            "payload": action.payload,
            "createdAt": created_at.isoformat(),
        }
        self.repository.create_action_event(
            action_id=action.action_id,
            status="accepted",
            request_payload=request.model_dump(mode="json", by_alias=True),
            response_payload=response_payload,
        )
        self.repository.commit()
        return UiActionResponse.model_validate(response_payload)

    def export(self, export_type: str, request: UiActionRequest) -> ExportResponse:
        action_id = f"export:{export_type}"
        action_map = {
            "dashboard": "dashboard-export-report",
            "dashboard-report": "dashboard-export-report",
            "lineage": "lineage-export-report",
            "lineage-report": "lineage-export-report",
            "lineage-artifacts": "lineage-download-artifacts",
            "board": "briefing-export-board-pack",
            "board-pack": "briefing-export-board-pack",
        }
        action = self.repository.get_action(action_map.get(export_type, action_id))
        created_at = datetime.now(UTC)
        job_id = f"{export_type}-{uuid4().hex[:10]}"
        response_payload = {
            "exportType": export_type,
            "status": "queued",
            "jobId": job_id,
            "message": action.response_message,
            "createdAt": created_at.isoformat(),
        }
        self.repository.create_action_event(
            action_id=action.action_id,
            status="queued",
            request_payload=request.model_dump(mode="json", by_alias=True),
            response_payload=response_payload,
        )
        self.repository.commit()
        return ExportResponse.model_validate(response_payload)

    def search(self, query: str) -> SearchResponse:
        normalized_query = query.strip().lower()
        context = self.app_context()
        dashboard = self.dashboard_snapshot(DashboardFilters())
        lineage = self.lineage_trace("calc-trace-7f3a9b21")
        briefing = self.briefing_snapshot()
        candidates = [
            SearchResult(
                id="home",
                title=context.app_name,
                category="Application",
                description="Home and management console",
                route="#/home",
            ),
            *[
                SearchResult(
                    id=view.view,
                    title=view.view.title(),
                    category="View",
                    description=view.description,
                    route=f"#/{view.view}",
                )
                for view in context.home_cards
            ],
            *[
                SearchResult(
                    id=f"metric-{metric.label.lower().replace(' ', '-')}",
                    title=metric.label,
                    category="Dashboard metric",
                    description=f"{metric.value} {metric.unit or ''}".strip(),
                    route="#/dashboard",
                )
                for metric in dashboard.metrics
            ],
            *[
                SearchResult(
                    id=f"capital-{label.lower().replace(' ', '-')}",
                    title=label,
                    category="Capital summary",
                    description=value,
                    route="#/dashboard",
                )
                for label, value in [
                    *dashboard.capital_summary.rows_top,
                    *dashboard.capital_summary.ratios,
                    ("Minimum Capital Requirement", dashboard.capital_summary.minimum_requirement),
                    ("Capital Buffer", dashboard.capital_summary.capital_buffer),
                ]
            ],
            *[
                SearchResult(
                    id=f"exposure-{exposure.id}",
                    title=exposure.name,
                    category="Top exposure",
                    description=f"{exposure.amount} RWA, {exposure.pct} of portfolio",
                    route="#/dashboard",
                )
                for exposure in dashboard.top_exposures
            ],
            SearchResult(
                id=lineage.trace.trace_id,
                title=lineage.trace.trace_id,
                category="Lineage trace",
                description=f"{lineage.trace.exposure_id} from {lineage.trace.source_system}",
                route="#/lineage",
            ),
            *[
                SearchResult(
                    id=f"driver-{driver.driver.lower().replace(' ', '-')}",
                    title=driver.driver,
                    category="RWA driver",
                    description=f"{driver.impact}, {driver.change_pct} of movement",
                    route="#/briefing",
                )
                for driver in briefing.movement_attribution.movement_drivers
            ],
        ]
        if not normalized_query:
            return SearchResponse(query=query, results=candidates[:8])

        results = [
            candidate
            for candidate in candidates
            if normalized_query
            in " ".join(
                [candidate.title, candidate.category, candidate.description, candidate.route]
            ).lower()
        ]
        return SearchResponse(query=query, results=results[:12])


def not_found_message(error: RisktraceDatasetNotFoundError | RisktraceActionNotFoundError) -> str:
    return f"RiskTrace resource not found: {error.args[0]}"


SCENARIO_RWA_FACTORS = {
    "Base Case": 1.00,
    "Downside": 1.08,
    "Stress": 1.18,
    "Recovery": 0.94,
}

PERIOD_PORTFOLIO_FACTORS = {
    "Current": 1.00,
    "MTD": 0.96,
    "QTD": 0.99,
    "YTD": 1.04,
    "Custom": 0.92,
}

BUSINESS_UNIT_FACTORS = {
    "All": 1.00,
    "Corporate Banking": 0.56,
    "Retail Banking": 0.31,
    "Markets": 0.18,
    "Treasury": 0.09,
}

CURRENCY_RATES = {
    "PLN": 1.00,
    "EUR": 0.23,
    "USD": 0.25,
    "GBP": 0.20,
}

BUSINESS_EXPOSURE_WEIGHTS = {
    "All": {},
    "Corporate Banking": {"Corporate": 1.7, "Retail": 0.25, "Mortgage": 0.2, "Sovereign": 0.55},
    "Retail Banking": {"Corporate": 0.2, "Retail": 1.75, "Mortgage": 1.85, "Sovereign": 0.25},
    "Markets": {
        "Corporate": 0.65,
        "Retail": 0.15,
        "Mortgage": 0.1,
        "Sovereign": 1.65,
        "Other": 1.9,
    },
    "Treasury": {
        "Corporate": 0.25,
        "Retail": 0.05,
        "Mortgage": 0.05,
        "Sovereign": 2.7,
        "Other": 1.35,
    },
}

SCENARIO_EXPOSURE_WEIGHTS = {
    "Base Case": {},
    "Downside": {"Corporate": 1.08, "Mortgage": 1.04, "Sovereign": 0.98},
    "Stress": {"Corporate": 1.16, "Mortgage": 1.1, "Retail": 1.04, "Sovereign": 0.95},
    "Recovery": {"Corporate": 0.96, "Mortgage": 0.98, "Retail": 1.02, "Sovereign": 1.04},
}

SCENARIO_RATING_WEIGHTS = {
    "Base Case": {},
    "Downside": {"AAA-AA": 0.96, "A": 0.98, "BBB": 1.05, "BB": 1.08, "B and below": 1.14},
    "Stress": {
        "AAA-AA": 0.9,
        "A": 0.94,
        "BBB": 1.08,
        "BB": 1.16,
        "B and below": 1.28,
        "Unrated": 1.2,
    },
    "Recovery": {"AAA-AA": 1.05, "A": 1.04, "BBB": 0.98, "BB": 0.94, "B and below": 0.88},
}


def _normalize_dashboard_filters(
    filters: DashboardFilters,
    filter_options: dict[str, list[str]],
) -> DashboardFilters:
    """Keep query-string values inside the configured dashboard option sets."""
    periods = filter_options.get("periods", [])
    scenarios = filter_options.get("scenarios", [])
    business_units = filter_options.get("businessUnits", [])
    currencies = filter_options.get("currencies", [])
    return DashboardFilters(
        period=filters.period if filters.period in periods else "Current",
        scenario=filters.scenario if filters.scenario in scenarios else "Base Case",
        business_unit=(filters.business_unit if filters.business_unit in business_units else "All"),
        currency=filters.currency if filters.currency in currencies else "PLN",
    )


def _apply_dashboard_filters(payload: dict[str, Any], filters: DashboardFilters) -> None:
    scenario_factor = SCENARIO_RWA_FACTORS[filters.scenario]
    period_factor = PERIOD_PORTFOLIO_FACTORS[filters.period]
    business_factor = BUSINESS_UNIT_FACTORS[filters.business_unit]
    currency_rate = CURRENCY_RATES[filters.currency]
    portfolio_factor = period_factor * business_factor

    base_exposure = _metric_amount(payload, "TOTAL EXPOSURE")
    base_rwa = _metric_amount(payload, "TOTAL RWA")
    exposure = base_exposure * portfolio_factor
    rwa = base_rwa * portfolio_factor * scenario_factor
    exposure_display = exposure * currency_rate
    rwa_display = rwa * currency_rate
    base_risk_weight = base_rwa / base_exposure
    risk_weight = rwa / exposure if exposure else 0

    capital_summary = payload["capitalSummary"]
    base_cet1 = _summary_amount(capital_summary, "CET1 Capital")
    base_tier1 = _summary_amount(capital_summary, "Tier 1 Capital")
    base_total_capital = _summary_amount(capital_summary, "Total Capital")
    cet1 = base_cet1 * portfolio_factor
    tier1 = base_tier1 * portfolio_factor
    total_capital = base_total_capital * portfolio_factor
    cet1_ratio = cet1 / rwa if rwa else 0
    tier1_ratio = tier1 / rwa if rwa else 0
    total_capital_ratio = total_capital / rwa if rwa else 0
    minimum_requirement = _parse_percent(capital_summary["minimumRequirement"])
    capital_buffer = cet1_ratio - minimum_requirement
    compare_label = f"{filters.period} / {filters.scenario} / {filters.business_unit}"

    for metric in payload["metrics"]:
        metric["compareLabel"] = compare_label
        if metric["label"] == "TOTAL EXPOSURE":
            metric["value"] = _format_whole_money(exposure_display)
            metric["unit"] = filters.currency
            metric["delta"] = _format_percent_delta(portfolio_factor - 1)
            metric["deltaDirection"] = "up" if portfolio_factor >= 1 else "down"
        elif metric["label"] == "TOTAL RWA":
            total_rwa_delta = portfolio_factor * scenario_factor - 1
            metric["value"] = _format_whole_money(rwa_display)
            metric["unit"] = filters.currency
            metric["delta"] = _format_percent_delta(total_rwa_delta)
            metric["deltaDirection"] = "up" if total_rwa_delta >= 0 else "down"
        elif metric["label"] in {"AVERAGE RISK WEIGHT", "RWA DENSITY"}:
            metric["value"] = _format_percent(risk_weight)
            metric["delta"] = _format_pp_delta(risk_weight - base_risk_weight)
            metric["deltaDirection"] = "up" if risk_weight >= base_risk_weight else "down"
        elif metric["label"] == "CET1 RATIO":
            base_cet1_ratio = base_cet1 / base_rwa
            metric["value"] = _format_percent(cet1_ratio)
            metric["delta"] = _format_pp_delta(cet1_ratio - base_cet1_ratio)
            metric["deltaDirection"] = "up" if cet1_ratio >= base_cet1_ratio else "down"

    payload["currency"] = filters.currency
    payload["totalRwaAmount"] = _format_compact_money(rwa_display)
    capital_summary["currency"] = filters.currency
    capital_summary["rowsTop"] = [
        ["CET1 Capital", _format_whole_money(cet1 * currency_rate)],
        ["Tier 1 Capital", _format_whole_money(tier1 * currency_rate)],
        ["Total Capital", _format_whole_money(total_capital * currency_rate)],
    ]
    capital_summary["ratios"] = [
        ["CET1 Ratio", _format_percent(cet1_ratio)],
        ["Tier 1 Ratio", _format_percent(tier1_ratio)],
        ["Total Capital Ratio", _format_percent(total_capital_ratio)],
    ]
    capital_summary["capitalBuffer"] = _format_pp_value(capital_buffer)

    _scale_top_exposures(payload, filters, portfolio_factor * scenario_factor, currency_rate, rwa)
    _scale_exposure_class(payload, filters, rwa_display)
    _scale_rwa_trend(payload, portfolio_factor * scenario_factor * currency_rate)
    _scale_rating_rwa(payload, filters, rwa_display)
    _scale_country_rwa(payload, rwa_display)
    _scale_alerts(payload, filters)


def _scale_top_exposures(
    payload: dict[str, Any],
    filters: DashboardFilters,
    amount_factor: float,
    currency_rate: float,
    total_rwa: float,
) -> None:
    business_adjustment = 1 if filters.business_unit == "All" else 0.72
    scaled_rows = []
    for index, row in enumerate(payload["topExposures"]):
        amount = (
            _parse_compact_money(row["amount"])
            * amount_factor
            * currency_rate
            * business_adjustment
        )
        percent = amount / (total_rwa * currency_rate) if total_rwa else 0
        scaled_rows.append(
            {
                **row,
                "amount": _format_compact_money(amount),
                "pct": _format_percent(percent),
                "bar": 0,
                "_amount": amount,
                "_index": index,
            }
        )
    max_amount = max(row["_amount"] for row in scaled_rows) if scaled_rows else 1
    for row in scaled_rows:
        row["bar"] = round((row["_amount"] / max_amount) * 100)
        del row["_amount"]
        del row["_index"]
    payload["topExposures"] = scaled_rows


def _scale_exposure_class(
    payload: dict[str, Any],
    filters: DashboardFilters,
    total_rwa_display: float,
) -> None:
    business_weights = BUSINESS_EXPOSURE_WEIGHTS[filters.business_unit]
    scenario_weights = SCENARIO_EXPOSURE_WEIGHTS[filters.scenario]
    raw_points = []
    for row in payload["exposureClass"]:
        label = row["label"]
        raw_value = (
            float(row["value"])
            * business_weights.get(label, 1.0)
            * scenario_weights.get(label, 1.0)
        )
        raw_points.append((row, raw_value))
    raw_total = sum(value for _, value in raw_points) or 1
    for row, raw_value in raw_points:
        pct = raw_value / raw_total
        row["value"] = round(pct * 100, 2)
        row["pct"] = _format_percent(pct)
        row["amount"] = _format_compact_money(total_rwa_display * pct)


def _scale_rwa_trend(payload: dict[str, Any], trend_factor: float) -> None:
    for row in payload["rwaTrend"]:
        row["value"] = round(float(row["value"]) * trend_factor, 2)


def _scale_rating_rwa(
    payload: dict[str, Any],
    filters: DashboardFilters,
    total_rwa_display: float,
) -> None:
    scenario_weights = SCENARIO_RATING_WEIGHTS[filters.scenario]
    raw_points = []
    for row in payload["ratingRwa"]:
        rating = row["rating"]
        raw_value = _parse_compact_money(row["amount"]) * scenario_weights.get(rating, 1.0)
        raw_points.append((row, raw_value))
    raw_total = sum(value for _, value in raw_points) or 1
    max_amount = 0.0
    scaled = []
    for row, raw_value in raw_points:
        pct = raw_value / raw_total
        amount = total_rwa_display * pct
        max_amount = max(max_amount, amount)
        scaled.append((row, pct, amount))
    for row, pct, amount in scaled:
        row["amount"] = _format_compact_money(amount)
        row["pct"] = _format_percent(pct)
        row["bar"] = round((amount / max_amount) * 100) if max_amount else 0


def _scale_country_rwa(payload: dict[str, Any], total_rwa_display: float) -> None:
    raw_points = [(row, _parse_percent(row["pct"])) for row in payload["countryRwa"]]
    raw_total = sum(value for _, value in raw_points) or 1
    for row, raw_value in raw_points:
        pct = raw_value / raw_total
        row["amount"] = _format_compact_money(total_rwa_display * pct)
        row["pct"] = _format_percent(pct)


def _scale_alerts(payload: dict[str, Any], filters: DashboardFilters) -> None:
    scenario_alert_factor = {
        "Base Case": 1.0,
        "Downside": 1.3,
        "Stress": 1.75,
        "Recovery": 0.7,
    }[filters.scenario]
    business_factor = 1.0 if filters.business_unit == "All" else 0.65
    for row in payload["alerts"]:
        row["count"] = max(1, round(row["count"] * scenario_alert_factor * business_factor))


def _metric_amount(payload: dict[str, Any], label: str) -> float:
    return next(
        _parse_whole_money(row["value"]) for row in payload["metrics"] if row["label"] == label
    )


def _summary_amount(payload: dict[str, Any], label: str) -> float:
    return next(_parse_whole_money(value) for key, value in payload["rowsTop"] if key == label)


def _parse_whole_money(value: str) -> float:
    return float(value.replace(",", ""))


def _parse_compact_money(value: str) -> float:
    normalized = value.strip().replace(",", "")
    multiplier = 1.0
    if normalized.endswith("B"):
        multiplier = 1_000_000_000.0
        normalized = normalized[:-1]
    elif normalized.endswith("M"):
        multiplier = 1_000_000.0
        normalized = normalized[:-1]
    return float(normalized) * multiplier


def _parse_percent(value: str) -> float:
    return float(value.strip().removesuffix("%")) / 100


def _format_whole_money(value: float) -> str:
    return f"{round(value):,}"


def _format_compact_money(value: float) -> str:
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    return f"{value / 1_000_000:.1f}M"


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _format_percent_delta(value: float) -> str:
    return f"{value * 100:+.2f}%"


def _format_pp_delta(value: float) -> str:
    return f"{value * 100:+.2f} pp"


def _format_pp_value(value: float) -> str:
    return f"{value * 100:.2f} pp"
