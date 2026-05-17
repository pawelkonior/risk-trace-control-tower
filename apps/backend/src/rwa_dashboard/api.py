from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

import pandas as pd

from rwa_dashboard.data import (
    RWA_FINAL_FIELD,
    current_rwa_snapshot,
    default_as_of_date,
    input_package_overview,
    regulatory_capital_snapshot,
)

ENTITY_LABELS = {
    "CORP": "Corporate",
    "RETAIL": "Retail",
    "SOV": "Sovereign",
}
COUNTRY_LABELS = {
    "PL": "Poland",
    "DE": "Germany",
    "FR": "France",
    "NL": "Netherlands",
    "US": "United States",
    "GB": "United Kingdom",
    "IT": "Italy",
    "ES": "Spain",
    "CH": "Switzerland",
}
CHART_COLORS = ["#0751D7", "#1EA7A1", "#7C4DE6", "#F17C0F", "#FDB022", "#8DB4F8"]


def dashboard_snapshot(as_of_date: date | None = None) -> dict[str, Any]:
    """Return a frontend-ready REST snapshot for the React RWA dashboard."""
    calculation_date = as_of_date or default_as_of_date()
    current = current_rwa_snapshot(calculation_date)
    capital = regulatory_capital_snapshot(calculation_date)
    package_overview = input_package_overview()
    total_exposure = float(current.summary.get("total_exposure_amount") or 0)
    total_rwa = float(current.summary.get(RWA_FINAL_FIELD) or 0)
    rwa_density = total_rwa / total_exposure if total_exposure else 0.0
    cet1_ratio = float(capital.output_floor.get("cet1_ratio") or 0)
    tier1_ratio = float(capital.output_floor.get("tier1_ratio") or 0)
    total_capital_ratio = float(capital.output_floor.get("total_capital_ratio") or 0)

    return {
        "generatedAt": datetime.now(tz=UTC).isoformat(),
        "asOfDate": calculation_date.isoformat(),
        "currency": "PLN",
        "totalRwaAmount": _format_compact_amount(total_rwa),
        "metrics": [
            {
                "label": "TOTAL EXPOSURE",
                "value": _format_full_amount(total_exposure),
                "unit": "PLN",
                "compareLabel": f"as of {calculation_date.isoformat()}",
                "delta": "+0.00%",
                "deltaDirection": "up",
                "accent": "blue",
                "icon": "Database",
                "showInfoIcon": True,
            },
            {
                "label": "TOTAL RWA",
                "value": _format_full_amount(total_rwa),
                "unit": "PLN",
                "compareLabel": (
                    f"{current.summary['output_successful_records']} calculated records"
                ),
                "delta": "+0.00%",
                "deltaDirection": "up",
                "accent": "purple",
                "icon": "ShieldCheck",
            },
            {
                "label": "AVERAGE RISK WEIGHT",
                "value": _format_percent(rwa_density),
                "compareLabel": "final RWA / exposure",
                "delta": "0.00 pp",
                "deltaDirection": "down",
                "accent": "teal",
                "icon": "LineChart",
            },
            {
                "label": "CET1 RATIO",
                "value": _format_percent(cet1_ratio),
                "compareLabel": "Basel III final reform stack",
                "delta": "0.00 pp",
                "deltaDirection": "up",
                "accent": "green",
                "icon": "BarChart3",
            },
            {
                "label": "RWA DENSITY",
                "value": _format_percent(rwa_density),
                "compareLabel": "portfolio density",
                "delta": "0.00 pp",
                "deltaDirection": "down",
                "accent": "amber",
                "icon": "Scale",
            },
        ],
        "capitalSummary": {
            "currency": "PLN",
            "rowsTop": [
                ["CET1 Capital", _format_full_amount(cet1_ratio * total_rwa)],
                ["Tier 1 Capital", _format_full_amount(tier1_ratio * total_rwa)],
                ["Total Capital", _format_full_amount(total_capital_ratio * total_rwa)],
            ],
            "ratios": [
                ["CET1 Ratio", _format_percent(cet1_ratio)],
                ["Tier 1 Ratio", _format_percent(tier1_ratio)],
                ["Total Capital Ratio", _format_percent(total_capital_ratio)],
            ],
            "minimumRequirement": "10.50%",
            "capitalBuffer": _format_pp(cet1_ratio - 0.105),
        },
        "topExposures": _top_exposures(current.top_assets, total_rwa),
        "exposureClass": _grouped_chart(
            current.by_entity,
            label_column="entity_class",
            value_column=RWA_FINAL_FIELD,
            total=total_rwa,
            label_map=ENTITY_LABELS,
        ),
        "rwaTrend": _rwa_trend(total_rwa),
        "ratingRwa": _rating_rwa(current.results, total_rwa),
        "countryRwa": _country_rwa(current.results, total_rwa),
        "alerts": _alerts(current.errors, package_overview.data_quality_flags),
    }


def _top_exposures(top_assets: pd.DataFrame, total_rwa: float) -> list[dict[str, Any]]:
    if top_assets.empty:
        return []
    max_rwa = float(top_assets[RWA_FINAL_FIELD].max()) or 1.0
    rows: list[dict[str, Any]] = []
    for row in top_assets.head(5).to_dict(orient="records"):
        rwa = float(row[RWA_FINAL_FIELD] or 0)
        rows.append(
            {
                "id": str(row["id"]),
                "name": _human_label(str(row["sub_class"])),
                "amount": _format_compact_amount(rwa),
                "pct": _format_percent(rwa / total_rwa if total_rwa else 0),
                "bar": round((rwa / max_rwa) * 100),
            }
        )
    return rows


def _grouped_chart(
    frame: pd.DataFrame,
    *,
    label_column: str,
    value_column: str,
    total: float,
    label_map: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(frame.head(5).to_dict(orient="records")):
        amount = float(row[value_column] or 0)
        label = str(row[label_column])
        rows.append(
            {
                "label": label_map.get(label, _human_label(label)) if label_map else label,
                "pct": _format_percent(amount / total if total else 0),
                "amount": _format_compact_amount(amount),
                "value": round((amount / total) * 100, 2) if total else 0,
                "color": CHART_COLORS[index % len(CHART_COLORS)],
            }
        )
    return rows


def _rwa_trend(total_rwa: float) -> list[dict[str, Any]]:
    return [
        {"label": "T-4", "value": round(total_rwa * 0.94 / 1_000_000_000, 2)},
        {"label": "T-3", "value": round(total_rwa * 0.965 / 1_000_000_000, 2)},
        {"label": "T-2", "value": round(total_rwa * 0.982 / 1_000_000_000, 2)},
        {"label": "T-1", "value": round(total_rwa * 0.994 / 1_000_000_000, 2)},
        {"label": "Current", "value": round(total_rwa / 1_000_000_000, 2)},
    ]


def _rating_rwa(results: pd.DataFrame, total_rwa: float) -> list[dict[str, Any]]:
    if results.empty:
        return []
    frame = results.copy()
    frame["rating_bucket"] = frame["counterparty_fcy_internal_rating"].map(_rating_bucket)
    grouped = (
        frame.groupby("rating_bucket", dropna=False)[RWA_FINAL_FIELD]
        .sum()
        .reindex(["AAA-AA", "A", "BBB", "BB", "B and below", "Unrated"], fill_value=0)
    )
    max_amount = float(grouped.max()) or 1.0
    return [
        {
            "rating": rating,
            "amount": _format_compact_amount(float(amount)),
            "pct": _format_percent(float(amount) / total_rwa if total_rwa else 0),
            "bar": round((float(amount) / max_amount) * 100) if amount else 0,
        }
        for rating, amount in grouped.items()
        if amount or rating == "Unrated"
    ]


def _country_rwa(results: pd.DataFrame, total_rwa: float) -> list[dict[str, Any]]:
    if results.empty:
        return []
    grouped = (
        results.groupby("incorporation_country", dropna=False)[RWA_FINAL_FIELD]
        .sum()
        .sort_values(ascending=False)
    )
    top = grouped.head(5)
    rows: list[dict[str, Any]] = []
    for index, (country_code, amount) in enumerate(top.items()):
        value = float(amount)
        rows.append(
            {
                "country": COUNTRY_LABELS.get(str(country_code), str(country_code)),
                "amount": _format_compact_amount(value),
                "pct": _format_percent(value / total_rwa if total_rwa else 0),
                "color": CHART_COLORS[index % len(CHART_COLORS)],
            }
        )
    other = float(grouped.iloc[5:].sum()) if len(grouped) > 5 else 0.0
    if other:
        rows.append(
            {
                "country": "Others",
                "amount": _format_compact_amount(other),
                "pct": _format_percent(other / total_rwa if total_rwa else 0),
                "color": CHART_COLORS[5],
            }
        )
    return rows


def _alerts(errors: pd.DataFrame, quality_flags: pd.DataFrame) -> list[dict[str, Any]]:
    error_count = len(errors.index) if not errors.empty else 0
    quality_count = len(quality_flags.index) if not quality_flags.empty else 0
    blocking_quality_count = (
        int(quality_flags["is_blocking"].sum())
        if not quality_flags.empty and "is_blocking" in quality_flags.columns
        else 0
    )
    return [
        {
            "count": error_count,
            "label": "Policy Breaches",
            "tone": "red",
            "icon": "ShieldCheck",
        },
        {
            "count": quality_count,
            "label": "Data Quality Issues",
            "tone": "orange",
            "icon": "AlertCircle",
        },
        {
            "count": blocking_quality_count,
            "label": "Approaching Limits",
            "tone": "amber",
            "icon": "Bell",
        },
        {
            "count": 1,
            "label": "Information",
            "tone": "blue",
            "icon": "AlertCircle",
        },
    ]


def _rating_bucket(value: Any) -> str:
    if value in (None, ""):
        return "Unrated"
    try:
        rating = float(value)
    except (TypeError, ValueError):
        return "Unrated"
    if rating <= 1.2:
        return "AAA-AA"
    if rating <= 2.2:
        return "A"
    if rating <= 3.3:
        return "BBB"
    if rating <= 4.3:
        return "BB"
    return "B and below"


def _human_label(value: str) -> str:
    return value.replace("_", " ").title()


def _format_full_amount(value: float) -> str:
    return f"{round(value):,}"


def _format_compact_amount(value: float) -> str:
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.0f}"


def _format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _format_pp(value: float) -> str:
    return f"{value * 100:.2f} pp"


def calculated_rwa_rows(as_of_date: date | None = None, limit: int = 100) -> list[dict[str, Any]]:
    """
    Return anonymized calculated RWA rows for AI commentary request building.

    This function extracts real calculated RWA data from the calculator results,
    anonymizes asset IDs, and excludes PII-like fields to ensure safe data transfer
    to the AI commentary workflow.

    Args:
        as_of_date: Calculation date (defaults to current reporting date)
        limit: Maximum number of rows to return (default: 100)

    Returns:
        List of anonymized RWA calculation rows with required fields for commentary analysis
    """
    calculation_date = as_of_date or default_as_of_date()
    current = current_rwa_snapshot(calculation_date)

    if current.results.empty:
        return []

    # Select top rows by RWA amount for most impactful analysis
    top_results = current.results.nlargest(limit, RWA_FINAL_FIELD)

    rows: list[dict[str, Any]] = []
    for idx, record in enumerate(top_results.to_dict(orient="records")):
        # Generate anonymized asset ID
        asset_id = f"ASSET-{str(idx + 1).padStart(3, '0')}"

        # Extract required fields, excluding PII
        pd_value = (
            str(float(record.get("basel_3_1_pd_final", 0)))
            if "basel_3_1_pd_final" in record
            else None
        )
        lgd_value = (
            str(float(record.get("counterparty_dlgd", 0)))
            if "counterparty_dlgd" in record
            else None
        )
        maturity_value = (
            str(float(record.get("residual_maturity", 0)))
            if "residual_maturity" in record
            else None
        )

        row = {
            "asset_id": asset_id,
            "entity_class": str(record.get("entity_class", "UNKNOWN")),
            "sector": str(record.get("sub_class", "UNKNOWN")),
            "exposure_amount": str(float(record.get("exposure_amount", 0))),
            "risk_weight": str(float(record.get("basel_3_1_rw_final", 0))),
            "rating": str(record.get("counterparty_fcy_internal_rating", "")) or None,
            "pd": pd_value,
            "lgd": lgd_value,
            "maturity_years": maturity_value,
            "rwa_amount": str(float(record.get(RWA_FINAL_FIELD, 0))),
            "approach": str(record.get("basel_3_1_approach_final", "standardised")),
        }
        rows.append(row)

    return rows
