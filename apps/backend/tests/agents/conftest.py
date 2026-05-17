from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def deterministic_agent_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep agent tests deterministic unless an individual test opts into watsonx."""
    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "deterministic")
    monkeypatch.setenv("RWA_LANGFUSE_ENABLED", "false")
    for name in (
        "WATSONX_PROJECT_ID",
        "WATSONX_APIKEY",
        "WATSONX_URL",
        "WATSONX_MODEL_ID",
        "RWA_AGENTS_WATSONX_PROJECT_ID",
        "RWA_AGENTS_WATSONX_APIKEY",
        "RWA_AGENTS_WATSONX_URL",
        "RWA_AGENTS_WATSONX_MODEL_ID",
    ):
        monkeypatch.delenv(name, raising=False)
