from __future__ import annotations

import pytest
from pydantic import ValidationError

from rwa_agents.schemas import RwaAnalysisRequest
from rwa_agents.validation import build_agent_state


def valid_payload() -> dict:
    return {
        "request_id": "agent-test-run",
        "materiality_threshold": "0.05",
        "rwa_input_data": [
            {
                "asset_id": "ASSET-001",
                "asset_class": "Corporate",
                "sector": "Manufacturing",
                "exposure_amount": "1000",
                "risk_weight": "0.50",
                "rating": "BBB",
                "pd": "0.02",
                "lgd": "0.45",
                "maturity_years": "2.5",
                "approach": "standardized",
            }
        ],
        "rwa_output_results": [
            {
                "asset_id": "ASSET-001",
                "rwa_amount": "500",
                "approach": "standardized",
            }
        ],
    }


def test_valid_request_builds_agent_state_with_default_loop_limit() -> None:
    request = RwaAnalysisRequest.model_validate(valid_payload())

    state = build_agent_state(request)

    assert state["request_id"] == "agent-test-run"
    assert state["loop_limit"] == 2
    assert state["agent_findings"] == []
    assert state["commentary_views"].executive_summary == ""
    assert state["guardrail_results"] == []
    assert state["final_commentary"] is None
    assert state["llm_call_count"] == 0
    assert state["total_token_count"] == 0


def test_allowed_anonymized_identifiers_pass_validation() -> None:
    payload = valid_payload()
    payload["rwa_input_data"][0]["asset_id"] = "EXPOSURE-123"
    payload["rwa_output_results"][0]["asset_id"] = "EXPOSURE-123"

    request = RwaAnalysisRequest.model_validate(payload)

    assert request.rwa_input_data[0].asset_id == "EXPOSURE-123"


def test_pii_like_fields_are_rejected_before_state_build() -> None:
    payload = valid_payload()
    payload["rwa_input_data"][0]["customer_name"] = "Jane Client"

    with pytest.raises(ValidationError, match="PII-like data is not allowed"):
        RwaAnalysisRequest.model_validate(payload)


def test_pii_like_values_are_rejected_before_state_build() -> None:
    payload = valid_payload()
    payload["request_id"] = "jane.client@example.com"

    with pytest.raises(ValidationError, match="email"):
        RwaAnalysisRequest.model_validate(payload)


def test_non_anonymized_identifier_is_rejected() -> None:
    payload = valid_payload()
    payload["rwa_input_data"][0]["asset_id"] = "Jane-Client-Loan"

    with pytest.raises(ValidationError, match="anonymized identifier"):
        RwaAnalysisRequest.model_validate(payload)
