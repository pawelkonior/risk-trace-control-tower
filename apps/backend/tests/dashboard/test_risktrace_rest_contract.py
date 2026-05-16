from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from rwa_calculator.rwa_calculator.fastapi_app import create_app

RISKTRACE_OPENAPI_METHODS = {
    "/v1/app/context": {"get"},
    "/v1/dashboard/snapshot": {"get"},
    "/v1/lineage/traces/{trace_id}": {"get"},
    "/v1/briefing/snapshot": {"get"},
    "/v1/ui/actions/{action_id}": {"post"},
    "/v1/exports/{export_type}": {"get"},
    "/v1/notifications": {"get"},
    "/v1/search": {"get"},
}

RISKTRACE_ENDPOINT_CASES = [
    pytest.param(
        "GET",
        "/v1/app/context",
        "/v1/app/context",
        {},
        {200},
        id="app-context",
    ),
    pytest.param(
        "GET",
        "/v1/dashboard/snapshot",
        "/v1/dashboard/snapshot",
        {},
        {200},
        id="dashboard-snapshot",
    ),
    pytest.param(
        "GET",
        "/v1/lineage/traces/{trace_id}",
        "/v1/lineage/traces/risktrace-smoke-trace",
        {},
        {200, 404},
        id="lineage-trace",
    ),
    pytest.param(
        "GET",
        "/v1/briefing/snapshot",
        "/v1/briefing/snapshot",
        {},
        {200},
        id="briefing-snapshot",
    ),
    pytest.param(
        "POST",
        "/v1/ui/actions/{action_id}",
        "/v1/ui/actions/acknowledge-notification",
        {"json": {"source": "pytest", "parameters": {}}},
        {200, 202, 204, 404},
        id="ui-action",
    ),
    pytest.param(
        "GET",
        "/v1/exports/{export_type}",
        "/v1/exports/dashboard",
        {"headers": {"Accept": "application/json,text/csv"}},
        {200},
        id="export",
    ),
    pytest.param(
        "GET",
        "/v1/notifications",
        "/v1/notifications",
        {},
        {200},
        id="notifications",
    ),
    pytest.param(
        "GET",
        "/v1/search",
        "/v1/search",
        {"params": {"q": "capital"}},
        {200},
        id="search",
    ),
]


@pytest.fixture
def temporary_sqlite_url(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> str:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'risktrace-contract.sqlite3'}"
    monkeypatch.setenv("RWA_DATABASE_URL", database_url)
    return database_url


@pytest.fixture
def risktrace_client(temporary_sqlite_url: str) -> Iterator[TestClient]:
    _ = temporary_sqlite_url
    with TestClient(create_app()) as client:
        yield client


def test_risktrace_contract_tests_pin_database_to_temporary_sqlite(
    temporary_sqlite_url: str,
) -> None:
    assert os.environ["RWA_DATABASE_URL"] == temporary_sqlite_url
    assert temporary_sqlite_url.startswith("sqlite+pysqlite:///")


def test_risktrace_openapi_declares_planned_rest_paths(risktrace_client: TestClient) -> None:
    openapi = risktrace_client.get("/openapi.json")
    assert openapi.status_code == 200

    paths = openapi.json()["paths"]
    missing = sorted(set(RISKTRACE_OPENAPI_METHODS) - set(paths))
    if missing:
        pytest.skip(f"RiskTrace routes not wired in this backend build yet: {missing}")

    for path, expected_methods in RISKTRACE_OPENAPI_METHODS.items():
        assert expected_methods.issubset(paths[path])


@pytest.mark.parametrize(
    ("method", "route_template", "request_path", "request_kwargs", "expected_statuses"),
    RISKTRACE_ENDPOINT_CASES,
)
def test_risktrace_rest_endpoint_smoke_contract(
    risktrace_client: TestClient,
    method: str,
    route_template: str,
    request_path: str,
    request_kwargs: dict[str, Any],
    expected_statuses: set[int],
) -> None:
    if route_template not in _app_route_paths(risktrace_client):
        pytest.skip(f"{route_template} is not wired in this backend build yet")

    response = risktrace_client.request(method, request_path, **request_kwargs)

    assert response.status_code in expected_statuses
    assert response.status_code < 500
    if response.status_code == 204:
        assert not response.content
        return

    assert response.content
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        payload = response.json()
        assert isinstance(payload, dict | list)


def test_dashboard_filters_recalculate_snapshot_data(risktrace_client: TestClient) -> None:
    base_response = risktrace_client.get("/v1/dashboard/snapshot")
    filtered_response = risktrace_client.get(
        "/v1/dashboard/snapshot",
        params={
            "period": "YTD",
            "scenario": "Stress",
            "businessUnit": "Corporate Banking",
            "currency": "EUR",
        },
    )

    assert base_response.status_code == 200
    assert filtered_response.status_code == 200
    base_payload = base_response.json()
    filtered_payload = filtered_response.json()
    base_total_rwa = next(
        metric for metric in base_payload["metrics"] if metric["label"] == "TOTAL RWA"
    )
    filtered_total_rwa = next(
        metric for metric in filtered_payload["metrics"] if metric["label"] == "TOTAL RWA"
    )

    assert filtered_payload["filters"] == {
        "period": "YTD",
        "scenario": "Stress",
        "businessUnit": "Corporate Banking",
        "currency": "EUR",
    }
    assert filtered_payload["currency"] == "EUR"
    assert filtered_payload["capitalSummary"]["currency"] == "EUR"
    assert filtered_total_rwa["unit"] == "EUR"
    assert filtered_total_rwa["value"] != base_total_rwa["value"]
    assert filtered_payload["exposureClass"] != base_payload["exposureClass"]
    assert filtered_payload["alerts"] != base_payload["alerts"]


def _app_route_paths(client: TestClient) -> set[str]:
    return {route.path for route in client.app.routes if hasattr(route, "path")}
