from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from .repositories import RisktraceUiRepository


def seed_risktrace_ui(session: Session) -> None:
    """Seed the database with the UI datasets and action registry."""
    repository = RisktraceUiRepository(session)
    now = datetime.now(UTC).isoformat()
    for key, payload in default_datasets(now).items():
        repository.upsert_dataset(key, payload)
    for action in default_actions():
        repository.upsert_action(**action)
    repository.commit()


def default_datasets(generated_at: str) -> dict[str, dict[str, Any]]:
    return {
        "app_context": _app_context(),
        "dashboard_snapshot": _dashboard_snapshot(generated_at),
        "lineage_trace_current": _lineage_snapshot(),
        "lineage_trace_calc-trace-7f3a9b21": _lineage_snapshot(),
        "briefing_snapshot": _briefing_snapshot(generated_at),
    }


def default_actions() -> Iterable[dict[str, Any]]:
    lineage_processing_message = (
        "Data is being processed. We will email a...k...@risktrace.com "
        "when the task is complete."
    )
    return [
        _action(
            "reporting-date", "Reporting Date", "navigation", "Reporting date selector opened."
        ),
        _action(
            "reporting-date.open",
            "Reporting Date",
            "navigation",
            "Reporting date selector opened.",
        ),
        _action("search-open", "Search", "navigation", "Search opened."),
        _action("search.open", "Search", "navigation", "Search opened."),
        _action("search.result.open", "Open Search Result", "navigation", "Search result opened."),
        _action(
            "notifications-open", "Notifications", "navigation", "Notifications drawer opened."
        ),
        _action(
            "notifications.open",
            "Notifications",
            "navigation",
            "Notifications drawer opened.",
        ),
        _action("help-open", "Help", "navigation", "Help center opened."),
        _action("help.open", "Help", "navigation", "Help center opened."),
        _action("help.topic.open", "Open Help Topic", "navigation", "Help topic opened."),
        _action("user.open", "Open User Menu", "navigation", "User menu opened."),
        _action("user.profile.open", "Open Profile", "navigation", "User profile opened."),
        _action(
            "user.preferences.open",
            "Open Preferences",
            "navigation",
            "User preferences opened.",
        ),
        _action("user.audit.open", "Open Audit Activity", "navigation", "Audit activity opened."),
        _action(
            "navigation-collapse", "Collapse Navigation", "navigation", "Navigation collapsed."
        ),
        _action(
            "navigation.collapse", "Collapse Navigation", "navigation", "Navigation collapsed."
        ),
        _action("dashboard.filter.period", "Set Period", "dashboard", "Dashboard period applied."),
        _action("dashboard.filter.set", "Set Filter", "dashboard", "Dashboard filter applied."),
        _action("dashboard.filter.reset", "Reset Filters", "dashboard", "Dashboard filters reset."),
        _action("dashboard-filter-reset", "Reset Filters", "dashboard", "Dashboard filters reset."),
        _action(
            "dashboard-export-report",
            "Export RWA Dashboard",
            "export",
            lineage_processing_message,
            job_type="dashboard-report",
        ),
        _action(
            "dashboard-evidence-pack",
            "Open Evidence Pack",
            "export",
            lineage_processing_message,
            job_type="dashboard-evidence-pack",
        ),
        _action(
            "dashboard.evidence-pack.open",
            "Open Evidence Pack",
            "export",
            lineage_processing_message,
            job_type="dashboard-evidence-pack",
        ),
        _action("dashboard-view-alerts", "View Alerts", "dashboard", "Alerts workspace opened."),
        _action("alerts.open", "View Alerts", "dashboard", "Alerts workspace opened."),
        _action("dashboard-view-exposures", "View Exposures", "dashboard", "Exposure list opened."),
        _action("exposure.open", "Open Exposure", "dashboard", "Exposure opened."),
        _action("exposure.search", "Search Exposures", "dashboard", "Exposure list opened."),
        _action(
            "dashboard-chart-details", "Chart Details", "dashboard", "Chart drill-down opened."
        ),
        _action(
            "dashboard.chart.details", "Chart Details", "dashboard", "Chart drill-down opened."
        ),
        _action(
            "lineage-export-report",
            "Export Lineage Report",
            "export",
            lineage_processing_message,
            job_type="lineage-report",
        ),
        _action("lineage-open-legend", "Lineage Legend", "lineage", "Lineage legend opened."),
        _action("lineage.legend.open", "Lineage Legend", "lineage", "Lineage legend opened."),
        _action("lineage-copy-value", "Copy Lineage Value", "lineage", "Lineage value copied."),
        _action("clipboard.copy", "Copy Value", "lineage", "Lineage value copied."),
        _action("lineage-open-artifact", "Open Artifact", "lineage", "Lineage artifact opened."),
        _action("lineage.artifact.open", "Open Artifact", "lineage", "Lineage artifact opened."),
        _action(
            "lineage-download-artifacts",
            "Download Artifacts",
            "export",
            lineage_processing_message,
            job_type="lineage-artifacts",
        ),
        _action(
            "lineage-upstream",
            "Upstream Lineage",
            "lineage",
            lineage_processing_message,
            job_type="lineage-upstream",
        ),
        _action(
            "lineage-downstream",
            "Downstream Lineage",
            "lineage",
            lineage_processing_message,
            job_type="lineage-downstream",
        ),
        _action(
            "briefing-review-rwa", "Review RWA Movement", "briefing", "RWA movement review opened."
        ),
        _action(
            "briefing.rwa-movement.review",
            "Review RWA Movement",
            "briefing",
            "RWA movement review opened.",
        ),
        _action(
            "briefing-open-workspace",
            "Open Review Workspace",
            "briefing",
            "Management review workspace opened.",
        ),
        _action(
            "briefing.review-workspace.open",
            "Open Review Workspace",
            "briefing",
            "Management review workspace opened.",
        ),
        _action(
            "briefing-export-board-pack",
            "Export Board Pack",
            "export",
            lineage_processing_message,
            job_type="board-pack",
        ),
        _action(
            "briefing-regulatory-context",
            "Regulatory Context",
            "briefing",
            "Regulatory context opened.",
        ),
        _action(
            "briefing.regulatory-context.open",
            "Regulatory Context",
            "briefing",
            "Regulatory context opened.",
        ),
        _action(
            "briefing-data-quality-report",
            "Data Quality Report",
            "briefing",
            "Data quality report opened.",
        ),
        _action(
            "briefing.data-quality-report.open",
            "Data Quality Report",
            "briefing",
            "Data quality report opened.",
        ),
        _action(
            "briefing-simulate-actions",
            "Simulate Actions",
            "briefing",
            "Management action simulation completed.",
        ),
        _action(
            "briefing.management-actions.simulate-all",
            "Simulate Actions",
            "briefing",
            "Management action simulation completed.",
        ),
        _action(
            "briefing.management-action.simulate",
            "Simulate Action",
            "briefing",
            "Management action simulation completed.",
        ),
        _action(
            "briefing-create-action-items",
            "Create Action Items",
            "briefing",
            "Action item creation workspace opened.",
        ),
        _action(
            "briefing.action-items.create",
            "Create Action Items",
            "briefing",
            "Action item creation workspace opened.",
        ),
        _action(
            "briefing-manual-review", "Manual Review", "briefing", "Manual review input opened."
        ),
        _action(
            "briefing.review.manual-open",
            "Manual Review",
            "briefing",
            "Manual review input opened.",
        ),
        _action("briefing-open-review", "Open Review", "briefing", "Review workspace opened."),
        _action("briefing.review.open", "Open Review", "briefing", "Review workspace opened."),
        _action("briefing-evidence-open", "Open Evidence", "briefing", "Evidence item opened."),
        _action("briefing.evidence.open", "Open Evidence", "briefing", "Evidence item opened."),
    ]


def _action(
    action_id: str,
    label: str,
    category: str,
    response_message: str,
    *,
    job_type: str | None = None,
) -> dict[str, Any]:
    return {
        "action_id": action_id,
        "label": label,
        "category": category,
        "response_message": response_message,
        "job_type": job_type,
        "payload": {},
    }


def _app_context() -> dict[str, Any]:
    return {
        "appName": "RiskTrace Control Tower",
        "environment": "PROD",
        "reportingDate": "2026-03-31",
        "comparisonLabel": "vs 2025-12-31",
        "user": {
            "initials": "AK",
            "name": "Anna Kowalska",
            "role": "Risk Analyst",
            "lastLogin": "2026-05-20 09:42",
        },
        "systemStatus": [
            {"label": "Data Pipeline", "value": "Healthy"},
            {"label": "Calculation Engine", "value": "Healthy"},
            {"label": "Reporting Service", "value": "Healthy"},
            {"label": "Audit Service", "value": "Healthy"},
        ],
        "reportingCalendar": {
            "reportingDate": "2026-03-31",
            "monthLabel": "March 2026",
            "lockedReason": "Reporting date is locked for the approved quarter-end close.",
            "availableDates": ["2026-03-31"],
        },
        "helpItems": [
            {
                "id": "HELP-001",
                "title": "RWA Dashboard",
                "detail": "Portfolio metrics, filters, chart drill-downs and export actions.",
                "actionId": "help.topic.open",
            },
            {
                "id": "HELP-002",
                "title": "Data Lineage",
                "detail": "Trace calculation evidence from source record to reporting layer.",
                "actionId": "help.topic.open",
            },
            {
                "id": "HELP-003",
                "title": "Management Briefing",
                "detail": "Review RWA movements, controls, simulations and board pack evidence.",
                "actionId": "help.topic.open",
            },
        ],
        "userMenu": [
            {
                "id": "USER-001",
                "label": "Profile",
                "detail": "Anna Kowalska, Risk Analyst",
                "actionId": "user.profile.open",
            },
            {
                "id": "USER-002",
                "label": "Preferences",
                "detail": "Currency, display density and notification settings",
                "actionId": "user.preferences.open",
            },
            {
                "id": "USER-003",
                "label": "Audit Activity",
                "detail": "Latest reviewed actions and exports",
                "actionId": "user.audit.open",
            },
        ],
        "notificationCount": 3,
        "homeCards": [
            {
                "view": "dashboard",
                "description": "Portfolio exposure, RWA, capital ratios and active risk alerts.",
                "metric": "2026-03-31",
                "status": "Ready",
                "tone": "blue",
            },
            {
                "view": "lineage",
                "description": "Source inputs, validation status and transformation evidence.",
                "metric": "TRACE-2026-03",
                "status": "Available",
                "tone": "teal",
            },
            {
                "view": "briefing",
                "description": "RWA movement attribution, review actions and board evidence.",
                "metric": "Board pack",
                "status": "Available",
                "tone": "purple",
            },
        ],
        "notifications": [
            {
                "id": "N-001",
                "title": "Data quality review",
                "detail": "146 records require owner confirmation before submission.",
                "tone": "amber",
                "createdAt": "2026-05-20 09:45",
                "read": False,
            },
            {
                "id": "N-002",
                "title": "Capital buffer update",
                "detail": "CET1 buffer remains above internal threshold.",
                "tone": "green",
                "createdAt": "2026-05-20 09:35",
                "read": False,
            },
            {
                "id": "N-003",
                "title": "Lineage evidence ready",
                "detail": "Calculation trace calc-trace-7f3a9b21 is fully covered.",
                "tone": "blue",
                "createdAt": "2026-05-20 09:20",
                "read": False,
            },
        ],
    }


def _dashboard_snapshot(generated_at: str) -> dict[str, Any]:
    return {
        "generatedAt": generated_at,
        "asOfDate": "2026-03-31",
        "currency": "PLN",
        "totalRwaAmount": "28.46B",
        "filters": {
            "period": "Current",
            "scenario": "Base Case",
            "businessUnit": "All",
            "currency": "PLN",
        },
        "filterOptions": {
            "periods": ["Current", "MTD", "QTD", "YTD", "Custom"],
            "scenarios": ["Base Case", "Downside", "Stress", "Recovery"],
            "businessUnits": [
                "All",
                "Corporate Banking",
                "Retail Banking",
                "Markets",
                "Treasury",
            ],
            "currencies": ["PLN", "EUR", "USD", "GBP"],
        },
        "metrics": [
            {
                "label": "TOTAL EXPOSURE",
                "value": "36,875,420,000",
                "unit": "PLN",
                "compareLabel": "vs 2025-12-31",
                "delta": "+4.32%",
                "deltaDirection": "up",
                "accent": "blue",
                "icon": "Database",
                "showInfoIcon": True,
            },
            {
                "label": "TOTAL RWA",
                "value": "28,456,780,000",
                "unit": "PLN",
                "compareLabel": "vs 2025-12-31",
                "delta": "+3.91%",
                "deltaDirection": "up",
                "accent": "purple",
                "icon": "ShieldCheck",
            },
            {
                "label": "AVERAGE RISK WEIGHT",
                "value": "77.19%",
                "compareLabel": "vs 2025-12-31",
                "delta": "-0.28 pp",
                "deltaDirection": "down",
                "accent": "teal",
                "icon": "LineChart",
            },
            {
                "label": "CET1 RATIO",
                "value": "14.62%",
                "compareLabel": "vs 2025-12-31",
                "delta": "+0.38 pp",
                "deltaDirection": "up",
                "accent": "green",
                "icon": "BarChart3",
            },
            {
                "label": "RWA DENSITY",
                "value": "77.19%",
                "compareLabel": "vs 2025-12-31",
                "delta": "-0.28 pp",
                "deltaDirection": "down",
                "accent": "amber",
                "icon": "Scale",
            },
        ],
        "capitalSummary": {
            "currency": "PLN",
            "rowsTop": [
                ["CET1 Capital", "4,159,820,000"],
                ["Tier 1 Capital", "4,482,710,000"],
                ["Total Capital", "5,102,330,000"],
            ],
            "ratios": [
                ["CET1 Ratio", "14.62%"],
                ["Tier 1 Ratio", "15.75%"],
                ["Total Capital Ratio", "17.92%"],
            ],
            "minimumRequirement": "10.50%",
            "capitalBuffer": "4.12 pp",
        },
        "topExposures": [
            {
                "id": "EXP-000128",
                "name": "Commercial Real Estate Loan",
                "amount": "850.2M",
                "pct": "3.00%",
                "bar": 100,
            },
            {
                "id": "EXP-000245",
                "name": "Corporate Loan - Manufacturing",
                "amount": "742.6M",
                "pct": "2.61%",
                "bar": 87,
            },
            {
                "id": "EXP-000367",
                "name": "Project Finance - Energy",
                "amount": "621.3M",
                "pct": "2.18%",
                "bar": 73,
            },
            {
                "id": "EXP-000589",
                "name": "Corporate Loan - Construction",
                "amount": "512.7M",
                "pct": "1.80%",
                "bar": 60,
            },
            {
                "id": "EXP-000712",
                "name": "Structured Loan",
                "amount": "498.9M",
                "pct": "1.75%",
                "bar": 59,
            },
        ],
        "exposureClass": [
            {
                "label": "Corporate",
                "pct": "44.15%",
                "amount": "12.57B",
                "value": 44.15,
                "color": "#0751D7",
            },
            {
                "label": "Retail",
                "pct": "24.68%",
                "amount": "7.02B",
                "value": 24.68,
                "color": "#1EA7A1",
            },
            {
                "label": "Mortgage",
                "pct": "18.97%",
                "amount": "5.40B",
                "value": 18.97,
                "color": "#7C4DE6",
            },
            {
                "label": "Sovereign",
                "pct": "7.53%",
                "amount": "2.14B",
                "value": 7.53,
                "color": "#F17C0F",
            },
            {
                "label": "Other",
                "pct": "4.67%",
                "amount": "1.33B",
                "value": 4.67,
                "color": "#FDB022",
            },
        ],
        "rwaTrend": [
            {"label": "", "value": 20.0},
            {"label": "Dec 2024", "value": 26.35},
            {"label": "Jan 2025", "value": 26.89},
            {"label": "Feb 2025", "value": 27.42},
            {"label": "Mar 2025", "value": 28.46},
        ],
        "ratingRwa": [
            {"rating": "AAA-AA", "amount": "3.21B", "pct": "11.28%", "bar": 34},
            {"rating": "A", "amount": "5.48B", "pct": "19.26%", "bar": 58},
            {"rating": "BBB", "amount": "9.36B", "pct": "32.90%", "bar": 100},
            {"rating": "BB", "amount": "6.14B", "pct": "21.58%", "bar": 66},
            {"rating": "B and below", "amount": "2.27B", "pct": "7.98%", "bar": 24},
            {"rating": "Unrated", "amount": "2.00B", "pct": "7.00%", "bar": 21},
        ],
        "countryRwa": [
            {"country": "Poland", "amount": "12.48B", "pct": "43.86%", "color": "#0751D7"},
            {"country": "Germany", "amount": "4.72B", "pct": "16.60%", "color": "#2F6BEF"},
            {"country": "France", "amount": "2.98B", "pct": "10.48%", "color": "#5084F1"},
            {
                "country": "Netherlands",
                "amount": "2.21B",
                "pct": "7.77%",
                "color": "#6D99F4",
            },
            {
                "country": "United States",
                "amount": "1.98B",
                "pct": "6.95%",
                "color": "#8DB4F8",
            },
            {"country": "Others", "amount": "4.09B", "pct": "14.34%", "color": "#B8D0FB"},
        ],
        "alerts": [
            {"count": 12, "label": "Policy Breaches", "tone": "red", "icon": "ShieldCheck"},
            {"count": 8, "label": "Data Quality Issues", "tone": "orange", "icon": "AlertCircle"},
            {"count": 5, "label": "Approaching Limits", "tone": "amber", "icon": "Bell"},
            {"count": 3, "label": "Information", "tone": "blue", "icon": "AlertCircle"},
        ],
    }


def _lineage_snapshot() -> dict[str, Any]:
    return {
        "trace": {
            "traceId": "calc-trace-7f3a9b21",
            "exposureId": "EXP-001",
            "sourceSystem": "LoanSystem",
            "sourceRecordId": "EXP-001",
            "inputHash": "9b7f2c3e8c4d2f6a9e...",
            "ruleVersion": "CRR3-SA-2026.1",
            "regulationReference": "CRR3 / Basel III Finalisation (EU) 2024/1623",
            "reportingDate": "2026-03-31",
            "timestamp": "2026-05-20 09:17:12",
            "rwaAmount": "10,000,000.00 PLN",
        },
        "nodes": [
            {
                "id": "source",
                "layer": "Source System",
                "title": "LoanSystem",
                "icon": "Database",
                "tone": "source",
                "details": [
                    ["Table", "corporate_exposures"],
                    ["Record ID", "EXP-001"],
                    ["Extracted", "2026-05-20 09:15:42"],
                ],
                "status": "Success",
            },
            {
                "id": "ingestion",
                "layer": "Ingestion Service",
                "title": "File Ingestion",
                "icon": "CloudUpload",
                "tone": "ingestion",
                "details": [
                    ["File", "corporate_exposures_20260331.csv"],
                    ["Batch ID", "ing-9c3e7d21"],
                    ["Ingested", "2026-05-20 09:16:03"],
                ],
                "status": "Success",
            },
            {
                "id": "validation",
                "layer": "Validation Service",
                "title": "Data Validation",
                "icon": "ShieldCheck",
                "tone": "validation",
                "details": [
                    ["Ruleset", "exposure_validation_v3.2"],
                    ["Valid Records", "12,312"],
                    ["Invalid Records", "146"],
                    ["Validated", "2026-05-20 09:16:28"],
                ],
                "status": "Success",
            },
            {
                "id": "rule",
                "layer": "Rule Engine",
                "title": "Risk Weight Engine",
                "icon": "Scale",
                "tone": "rule",
                "details": [
                    ["Rule Version", "CRR3-SA-2026.1"],
                    ["Applied", "2026-05-20 09:16:45"],
                ],
                "status": "Success",
            },
            {
                "id": "calculation",
                "layer": "Calculation Engine",
                "title": "RWA Calculation",
                "icon": "Calculator",
                "tone": "calculation",
                "details": [
                    ["Calculation ID", "calc-trace-7f3a9b21"],
                    ["Calculated", "2026-05-20 09:17:12"],
                ],
                "status": "Success",
            },
            {
                "id": "reporting",
                "layer": "Reporting Layer",
                "title": "RWA Results Store",
                "icon": "FileText",
                "tone": "reporting",
                "details": [
                    ["Table", "rwa_calculation_results"],
                    ["Stored", "2026-05-20 09:17:18"],
                ],
                "status": "Success",
            },
        ],
        "summary": [
            ["Calculation Trace ID", "calc-trace-7f3a9b21"],
            ["Reporting Date", "2026-03-31"],
            ["Source Record", "EXP-001"],
            ["Rule Version", "CRR3-SA-2026.1"],
            ["Exposure ID", "EXP-001"],
            ["RWA Amount", "10,000,000.00 PLN"],
        ],
        "transformationSteps": [
            {
                "step": 1,
                "service": "LoanSystem",
                "description": "Extract corporate exposure record",
                "inputRecords": "1",
                "outputRecords": "1",
                "duration": "00:00:02",
                "status": "Success",
                "executedAt": "2026-05-20 09:15:42",
            },
            {
                "step": 2,
                "service": "File Ingestion",
                "description": "File uploaded and parsed",
                "inputRecords": "12,458",
                "outputRecords": "12,458",
                "duration": "00:00:21",
                "status": "Success",
                "executedAt": "2026-05-20 09:16:03",
            },
            {
                "step": 3,
                "service": "Data Validation",
                "description": "Schema and business rule validation",
                "inputRecords": "12,458",
                "outputRecords": "12,312",
                "duration": "00:00:25",
                "status": "Success",
                "executedAt": "2026-05-20 09:16:28",
            },
            {
                "step": 4,
                "service": "Risk Weight Engine",
                "description": "Risk weight determination",
                "inputRecords": "12,312",
                "outputRecords": "12,312",
                "duration": "00:00:17",
                "status": "Success",
                "executedAt": "2026-05-20 09:16:45",
            },
            {
                "step": 5,
                "service": "RWA Calculation",
                "description": "RWA amount calculation",
                "inputRecords": "12,312",
                "outputRecords": "12,312",
                "duration": "00:00:27",
                "status": "Success",
                "executedAt": "2026-05-20 09:17:12",
            },
            {
                "step": 6,
                "service": "Results Store",
                "description": "Store calculation results",
                "inputRecords": "12,312",
                "outputRecords": "12,312",
                "duration": "00:00:06",
                "status": "Success",
                "executedAt": "2026-05-20 09:17:18",
            },
        ],
        "artifacts": [
            {"label": "Source File", "count": 1, "icon": "FileText"},
            {"label": "Validation Report", "count": 1, "icon": "ClipboardCheck"},
            {"label": "Applied Rules", "count": 1, "icon": "Network"},
            {"label": "Calculation Log", "count": 1, "icon": "FileClock"},
            {"label": "Result Snapshot", "count": 1, "icon": "FolderDown"},
        ],
        "totals": {
            "duration": "00:01:38",
            "totalInputRecords": "12,458",
            "totalOutputRecords": "12,312",
        },
        "directions": [
            {
                "title": "Upstream Lineage",
                "value": "LoanSystem",
                "meta": ["corporate_exposures", "EXP-001"],
                "buttonLabel": "View Full Upstream Lineage",
                "icon": "Database",
                "actionId": "lineage-upstream",
            },
            {
                "title": "Downstream Lineage",
                "value": "COREP Reporting",
                "meta": ["Template: C 07.00", "Load ID: corep-20260331-01"],
                "buttonLabel": "View Full Downstream Lineage",
                "icon": "Network",
                "actionId": "lineage-downstream",
            },
        ],
    }


def _briefing_snapshot(generated_at: str) -> dict[str, Any]:
    return {
        "generatedAt": generated_at,
        "kpis": [
            {
                "label": "Total RWA (Current)",
                "value": "28,456,780,000 PLN",
                "detail": "vs 27,421,360,000 PLN\n+1,035,420,000 PLN (+3.79%)",
                "icon": "Layers3",
                "tone": "blue",
            },
            {
                "label": "CET1 Ratio Impact",
                "value": "-0.28 pp",
                "detail": "Impact vs previous period",
                "icon": "ShieldCheck",
                "tone": "purple",
            },
            {
                "label": "Capital Buffer",
                "value": "4.12 pp",
                "detail": "Above internal threshold",
                "icon": "CheckCircle2",
                "tone": "green",
            },
            {
                "label": "Data Quality Score",
                "value": "98.8%",
                "detail": "12,312 valid / 146 rejected",
                "icon": "WalletCards",
                "tone": "blue",
            },
            {
                "label": "Confidence Score",
                "value": "87%",
                "detail": "High",
                "icon": "Target",
                "tone": "purple",
            },
        ],
        "movementAttribution": _movement_attribution(),
        "reviewPack": _review_pack(),
        "regulatoryWatch": [
            {"label": "Rule Version", "value": "CRR3-SA-DEMO-2026.1", "status": "Current"},
            {
                "label": "Reporting Framework",
                "value": "EBA Reporting Framework 4.0",
                "status": "Applicable",
            },
            {"label": "COREP Changes", "value": "No changes for 2026-03-31", "status": "OK"},
            {"label": "Regulatory Alerts", "value": "No open alerts", "status": "OK"},
        ],
        "dataQualityFindings": [
            {"label": "Rejected / Incomplete Records", "value": "146 (1.17%)"},
            {"label": "Missing External Ratings", "value": "84"},
            {"label": "Missing Collateral Links", "value": "42"},
            {"label": "Invalid LTV / Values", "value": "18"},
            {"label": "Source System Issues", "value": "2"},
        ],
        "simulatorActions": [
            {
                "action": "Fix missing ratings (146 records)",
                "impact": "-50M to -110M PLN",
                "confidence": "Medium",
                "owner": "Data Quality Team",
                "actionId": "briefing.management-action.simulate",
            },
            {
                "action": "Recognize eligible collateral (Top 20)",
                "impact": "-120M to -210M PLN",
                "confidence": "Medium",
                "owner": "Credit Risk Team",
                "actionId": "briefing.management-action.simulate",
            },
            {
                "action": "Reprice low-RORWA exposures",
                "impact": "Capital efficiency +0.14 pp",
                "confidence": "Low",
                "owner": "Business Line",
                "actionId": "briefing.management-action.simulate",
            },
            {
                "action": "Review mortgages with LTV > 80%",
                "impact": "RWA at risk 140M PLN",
                "confidence": "High",
                "owner": "Secured Lending",
                "actionId": "briefing.management-action.simulate",
            },
            {
                "action": "Optimize country risk concentrations",
                "impact": "RWA at risk 90M PLN",
                "confidence": "Medium",
                "owner": "Country Risk Team",
                "actionId": "briefing.management-action.simulate",
            },
        ],
        "evidenceItems": [
            {
                "label": "Calculation Run",
                "value": "calc-trace-7f3a9b21",
                "icon": "ClipboardList",
                "tone": "blue",
                "actionId": "briefing.evidence.open",
            },
            {
                "label": "Data Lineage",
                "value": "100% coverage",
                "icon": "GitBranch",
                "tone": "teal",
                "actionId": "briefing.evidence.open",
            },
            {
                "label": "Applied Rules",
                "value": "CRR3-SA-DEMO-2026.1",
                "icon": "FileText",
                "tone": "purple",
                "actionId": "briefing.evidence.open",
            },
            {
                "label": "Audit Log",
                "value": "View audit trail",
                "icon": "BookOpenCheck",
                "tone": "amber",
                "actionId": "briefing.evidence.open",
            },
            {
                "label": "Source Systems",
                "value": "4 systems",
                "icon": "Database",
                "tone": "red",
                "actionId": "briefing.evidence.open",
            },
            {
                "label": "Supporting Documents",
                "value": "11 documents",
                "icon": "FileArchive",
                "tone": "purple",
                "actionId": "briefing.evidence.open",
            },
        ],
        "boardPack": {
            "title": "Board Pack",
            "description": (
                "Export RWA metrics, data quality findings and traceability evidence for review."
            ),
            "icon": "FileText",
            "exportType": "board-pack",
        },
    }


def _movement_attribution() -> dict[str, Any]:
    return {
        "waterfallData": [
            _waterfall(
                "Opening\nRWA\n(Dec 31, 2025)",
                "Opening",
                "Opening RWA",
                0,
                620,
                0,
                0,
                0,
                "+620M",
                "#0751d7",
            ),
            _waterfall(
                "Portfolio\nVolume\nGrowth",
                "Portfolio",
                "Portfolio Volume Growth",
                620,
                0,
                280,
                0,
                0,
                "+280M",
                "#22a7a0",
            ),
            _waterfall(
                "Rating\nMigration",
                "Rating",
                "Rating Migration",
                900,
                0,
                140,
                0,
                0,
                "+140M",
                "#7c4de6",
            ),
            _waterfall(
                "LTV\nDeterioration",
                "LTV",
                "LTV Deterioration",
                1040,
                0,
                80,
                0,
                0,
                "+80M",
                "#f97316",
            ),
            _waterfall(
                "Data Quality\n(Fallbacks)",
                "Quality",
                "Missing Ratings (Fallback)",
                1120,
                0,
                50,
                0,
                0,
                "+50M",
                "#fdb022",
            ),
            _waterfall(
                "Collateral\nImprovement",
                "Collateral",
                "Collateral Improvement",
                1040,
                0,
                0,
                130,
                0,
                "-130M",
                "#16a34a",
            ),
            _waterfall(
                "Closing\nRWA\n(Mar 31, 2026)",
                "Closing",
                "Closing RWA",
                0,
                0,
                0,
                0,
                1040,
                "",
                "#0751d7",
            ),
        ],
        "movementDrivers": [
            {
                "driver": "Portfolio Volume Growth",
                "impact": "+620,000,000",
                "changePct": "59.8%",
                "color": "#0751d7",
            },
            {
                "driver": "Rating Migration",
                "impact": "+280,000,000",
                "changePct": "27.0%",
                "color": "#22a7a0",
            },
            {
                "driver": "LTV Deterioration",
                "impact": "+140,000,000",
                "changePct": "13.5%",
                "color": "#7c4de6",
            },
            {
                "driver": "New High-Risk Exposures",
                "impact": "+80,000,000",
                "changePct": "7.7%",
                "color": "#f97316",
            },
            {
                "driver": "Missing Ratings (Fallback)",
                "impact": "+50,000,000",
                "changePct": "4.8%",
                "color": "#fdb022",
            },
            {
                "driver": "Collateral Improvement",
                "impact": "-130,000,000",
                "changePct": "-12.6%",
                "color": "#16a34a",
            },
        ],
        "totalChange": "+1,040,000,000",
        "totalChangePct": "100.0%",
    }


def _review_pack() -> dict[str, Any]:
    return {
        "tabs": ["Summary", "Controls", "Sign-off"],
        "stats": [
            {
                "label": "Material RWA change",
                "value": "+1.04B PLN",
                "detail": "100% reconciled to drivers",
                "tone": "blue",
            },
            {
                "label": "CET1 impact",
                "value": "-0.28 pp",
                "detail": "Above internal capital buffer",
                "tone": "red",
            },
            {
                "label": "Open exceptions",
                "value": "146 records",
                "detail": "3 owner groups assigned",
                "tone": "amber",
            },
        ],
        "varianceReviewItems": [
            {
                "label": "Portfolio Volume Growth",
                "value": "+620M",
                "share": "59.8%",
                "width": 78,
                "color": "#0751d7",
            },
            {
                "label": "Rating Migration",
                "value": "+280M",
                "share": "27.0%",
                "width": 44,
                "color": "#22a7a0",
            },
            {
                "label": "LTV Deterioration",
                "value": "+140M",
                "share": "13.5%",
                "width": 28,
                "color": "#7c4de6",
            },
            {
                "label": "Missing Ratings Fallback",
                "value": "+50M",
                "share": "4.8%",
                "width": 16,
                "color": "#fdb022",
            },
        ],
        "controlChecklist": [
            {"label": "Rule version", "status": "Current", "tone": "success"},
            {"label": "COREP mapping", "status": "OK", "tone": "success"},
            {"label": "Data quality rejects", "status": "Review", "tone": "warning"},
            {"label": "Business owner notes", "status": "Pending", "tone": "neutral"},
        ],
        "manualReviewInputs": [
            {
                "label": "Risk note: Draft",
                "tone": "blue",
                "actionId": "briefing.review.manual-open",
            },
            {
                "label": "Finance sign-off",
                "tone": "amber",
                "actionId": "briefing.review.manual-open",
            },
            {
                "label": "Board pack: Ready",
                "tone": "purple",
                "actionId": "briefing.review.manual-open",
            },
        ],
    }


def _waterfall(
    label: str,
    axis_label: str,
    table_label: str,
    base: float,
    opening: float,
    increase: float,
    decrease: float,
    closing: float,
    display: str,
    color: str,
) -> dict[str, Any]:
    return {
        "label": label,
        "axisLabel": axis_label,
        "tableLabel": table_label,
        "base": base,
        "opening": opening,
        "increase": increase,
        "decrease": decrease,
        "closing": closing,
        "display": display,
        "color": color,
    }
