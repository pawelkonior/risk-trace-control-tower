from __future__ import annotations

from decimal import Decimal

from rwa_agents.schemas import RwaAnalysisRequest
from rwa_agents.tools import analyze_data_quality, analyze_risk

from .test_validation import valid_payload


def test_data_analyst_detects_data_quality_issues_with_tool_trace() -> None:
    payload = valid_payload()
    payload["rwa_input_data"] = [
        {
            "asset_id": "ASSET-001",
            "asset_class": "Corporate",
            "sector": "Manufacturing",
            "exposure_amount": "0",
            "risk_weight": None,
            "rating": None,
            "pd": None,
            "lgd": None,
            "approach": "standardized",
        },
        {
            "asset_id": "ASSET-001",
            "asset_class": "Corporate",
            "sector": "Manufacturing",
            "exposure_amount": "100",
            "risk_weight": "0.50",
            "rating": "BBB",
            "pd": "0.02",
            "lgd": "0.45",
            "approach": "standardized",
        },
        {
            "asset_id": "ASSET-002",
            "asset_class": "Retail",
            "sector": "Consumer",
            "exposure_amount": "100",
            "risk_weight": None,
            "rating": "A",
            "pd": "1.40",
            "lgd": "0.40",
            "approach": "standardized",
        },
    ]
    payload["rwa_output_results"] = [
        {
            "asset_id": "ASSET-999",
            "rwa_amount": "10",
            "approach": "standardized",
        }
    ]
    request = RwaAnalysisRequest.model_validate(payload)

    result = analyze_data_quality(request)

    codes = {flag.code for flag in result.validation_flags}
    assert {
        "DUPLICATE_ASSET_ID",
        "MISSING_OUTPUT",
        "MISSING_RISK_PARAMETER",
        "NON_POSITIVE_EXPOSURE",
        "MISSING_RATING",
        "INVALID_PD_LGD",
    }.issubset(codes)
    assert {action.id for action in result.recommended_actions} >= {
        "dq-deduplicate-assets",
        "dq-complete-calculator-output",
        "dq-complete-risk-parameters",
    }
    assert any(
        finding.title == "Exposure concentration requires review" for finding in result.findings
    )
    assert all(flag.source_agent == "DataAnalystAgent" for flag in result.validation_flags)
    critical_flags = [flag for flag in result.validation_flags if flag.severity == "critical"]
    assert all(flag.requires_human_intervention for flag in critical_flags)
    assert [step.phase for step in result.react_steps] == [
        "inspect_state",
        "select_tool",
        "execute_tool",
        "observe_result",
        "emit_finding",
    ]


def test_risk_expert_validates_rwa_deterministically_with_tool_trace() -> None:
    payload = valid_payload()
    payload["rwa_output_results"][0]["rwa_amount"] = "625"
    request = RwaAnalysisRequest.model_validate(payload)

    result = analyze_risk(request)

    assert result.quantitative_validation[0].expected_rwa_amount == Decimal("500.00")
    assert result.quantitative_validation[0].reported_rwa_amount == Decimal("625")
    assert result.quantitative_validation[0].passed is False
    assert result.validation_flags[0].code == "RWA_RECALCULATION_VARIANCE"
    assert result.validation_flags[0].source_agent == "RiskExpertAgent"
    assert result.validation_flags[0].requires_human_intervention is True
    assert result.recommended_actions[0].id == "risk-review-rwa-variance"
    assert [step.tool_name for step in result.react_steps if step.tool_name] == [
        "RiskTools",
        "RiskTools",
        "RiskTools",
    ]
