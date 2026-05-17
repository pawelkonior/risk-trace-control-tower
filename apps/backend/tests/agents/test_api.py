from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from rwa_calculator.rwa_calculator.fastapi_app import create_app

from .test_validation import valid_payload


@pytest.fixture
def agent_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[TestClient]:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'agents.sqlite3'}"
    monkeypatch.setenv("RWA_DATABASE_URL", database_url)
    with TestClient(create_app()) as client:
        yield client


def test_agent_endpoint_declared_in_openapi(agent_client: TestClient) -> None:
    assert os.environ["RWA_DATABASE_URL"].startswith("sqlite+pysqlite:///")

    payload = agent_client.get("/openapi.json").json()

    assert "/v1/agents/rwa-analysis/run" in payload["paths"]
    assert "post" in payload["paths"]["/v1/agents/rwa-analysis/run"]


def test_agent_endpoint_returns_required_response_shape(agent_client: TestClient) -> None:
    response = agent_client.post("/v1/agents/rwa-analysis/run", json=valid_payload())

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "COMPLETED"
    assert payload["final_commentary"]["status"] == "COMPLETED"
    assert payload["final_commentary"]["source_label"] == "RiskTrace Intelligence"
    assert payload["final_commentary"]["recommended_actions"] == []
    assert payload["observability"]["guardrail_results"]
    assert payload["observability"]["llm_call_count"] == 0
    assert payload["observability"]["total_token_count"] == 0
    first_guardrail = payload["observability"]["guardrail_results"][0]
    assert "affected_node" in first_guardrail
    assert "sanitized_text_used" in first_guardrail
    assert "guardrail_results" in payload["observability"]
    assert "guardrail_scans" not in payload["observability"]
    assert "llm_guard_enabled" not in payload


def test_agent_endpoint_returns_stable_validation_flag_shape(agent_client: TestClient) -> None:
    request_payload = valid_payload()
    request_payload["rwa_output_results"][0]["rwa_amount"] = "625"

    response = agent_client.post("/v1/agents/rwa-analysis/run", json=request_payload)

    assert response.status_code == 200
    payload = response.json()
    flag = payload["validation_flags"][0]
    assert flag["code"] == "RWA_RECALCULATION_VARIANCE"
    assert flag["source_agent"] == "RiskExpertAgent"
    assert flag["requires_human_intervention"] is True
    assert "source" not in flag


def test_agent_endpoint_rejects_pii_as_api_validation_error(
    agent_client: TestClient,
) -> None:
    payload = valid_payload()
    payload["rwa_input_data"][0]["iban"] = "PL61109010140000071219812874"

    response = agent_client.post("/v1/agents/rwa-analysis/run", json=payload)

    assert response.status_code == 422
    assert "final_commentary" not in response.text
