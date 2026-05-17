from __future__ import annotations

from typing import Any

from rwa_agents.config import RwaAgentsConfig
from rwa_agents.guardrails import GuardrailService
from rwa_agents.schemas import GuardrailResult, RwaAnalysisRequest
from rwa_agents.watsonx import (
    WatsonxAPIError,
    WatsonxClient,
    WatsonxResponse,
    WatsonxResponseError,
    WatsonxTokenUsage,
)
from rwa_agents.workflow import run_rwa_analysis

from .test_validation import valid_payload


def test_deterministic_mode_is_default_and_does_not_call_watsonx(monkeypatch) -> None:
    class FailIfInstantiated:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise AssertionError("WatsonxClient must not be used in deterministic mode")

    monkeypatch.setattr("rwa_agents.workflow.WatsonxClient", FailIfInstantiated)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert response.observability.llm_call_count == 0
    assert response.observability.total_token_count == 0


def test_watsonx_configuration_uses_unprefixed_env_aliases(monkeypatch) -> None:
    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("WATSONX_PROJECT_ID", "project-id")
    monkeypatch.setenv("WATSONX_APIKEY", "api-key")
    monkeypatch.setenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")

    config = RwaAgentsConfig.from_env()

    assert config.uses_watsonx is True
    assert config.watsonx_configured is True
    assert config.watsonx.watsonx_project_id == "project-id"
    assert config.watsonx.watsonx_apikey == "api-key"
    assert config.watsonx.watsonx_url == "https://eu-de.ml.cloud.ibm.com"


def test_watsonx_token_usage_normalizes_ibm_shapes() -> None:
    client = WatsonxClient(project_id="project-id", api_key="api-key", url="https://example.com")

    usage = client._extract_token_usage(
        {
            "usage": {"input_token_count": "10"},
            "results": [{"generated_token_count": 7}],
        }
    )

    assert usage.input_tokens == 10
    assert usage.output_tokens == 7
    assert usage.total_tokens == 17


def test_supervisor_uses_watsonx_when_enabled(monkeypatch) -> None:
    prompts: list[str] = []

    class FakeWatsonxClient:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.kwargs = kwargs

        def chat(self, prompt: str) -> WatsonxResponse:
            prompts.append(prompt)
            return WatsonxResponse(
                executive_summary="watsonx executive summary",
                cro_view="watsonx cro view",
                cfo_view="watsonx cfo view",
                token_usage=WatsonxTokenUsage(
                    input_tokens=430,
                    output_tokens=108,
                    total_tokens=538,
                ),
            )

    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("WATSONX_PROJECT_ID", "project-id")
    monkeypatch.setenv("WATSONX_APIKEY", "api-key")
    monkeypatch.setattr("rwa_agents.workflow.WatsonxClient", FakeWatsonxClient)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert response.final_commentary.executive_summary == "watsonx executive summary"
    assert response.final_commentary.cro_view == "watsonx cro view"
    assert response.final_commentary.cfo_view == "watsonx cfo view"
    assert response.observability.llm_call_count == 3
    assert response.observability.total_token_count == 1614
    assert response.observability.guardrail_block_count == 0
    assert len(prompts) == 3
    assert any("You are DataAnalystAgent" in prompt for prompt in prompts)
    assert any("You are RiskExpertAgent" in prompt for prompt in prompts)
    supervisor_prompt = next(
        prompt for prompt in prompts if "Synthesize executive-ready RWA commentary" in prompt
    )
    assert "Do not calculate RWA formulas" in supervisor_prompt
    assert "Do not copy deterministic baseline sentences verbatim" in supervisor_prompt
    assert "Use PLN as the monetary unit" in supervisor_prompt
    assert "Raw portfolio rows and direct identifiers are intentionally not provided" in (
        supervisor_prompt
    )
    assert all("ASSET-001" not in prompt for prompt in prompts)
    assert "DataAnalystAgent Watsonx synthesis completed." in response.messages
    assert "RiskExpertAgent Watsonx synthesis completed." in response.messages


def test_watsonx_malformed_output_falls_back_to_deterministic_commentary(monkeypatch) -> None:
    class MalformedWatsonxClient:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def chat(self, prompt: str) -> WatsonxResponse:
            _ = prompt
            raise WatsonxResponseError(
                "Invalid JSON",
                raw_text="not-json commentary",
                token_usage=WatsonxTokenUsage(input_tokens=5, output_tokens=3, total_tokens=8),
            )

    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("WATSONX_PROJECT_ID", "project-id")
    monkeypatch.setenv("WATSONX_APIKEY", "api-key")
    monkeypatch.setattr("rwa_agents.workflow.WatsonxClient", MalformedWatsonxClient)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert "Submitted portfolio RWA" in response.final_commentary.executive_summary
    assert "not-json commentary" not in response.final_commentary.executive_summary
    assert response.observability.llm_call_count == 3
    assert response.observability.total_token_count == 24


def test_watsonx_provider_failure_falls_back_without_llm_metrics(monkeypatch) -> None:
    class FailingWatsonxClient:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def chat(self, prompt: str) -> WatsonxResponse:
            _ = prompt
            raise WatsonxAPIError("unauthorized provider failure")

    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("WATSONX_PROJECT_ID", "project-id")
    monkeypatch.setenv("WATSONX_APIKEY", "api-key")
    monkeypatch.setattr("rwa_agents.workflow.WatsonxClient", FailingWatsonxClient)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert "Submitted portfolio RWA" in response.final_commentary.executive_summary
    assert "unauthorized provider failure" not in response.final_commentary.executive_summary
    assert response.observability.llm_call_count == 0
    assert response.observability.total_token_count == 0


def test_unsafe_watsonx_output_is_blocked_before_state_update(monkeypatch) -> None:
    class UnsafeWatsonxClient:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def chat(self, prompt: str) -> WatsonxResponse:
            _ = prompt
            return WatsonxResponse(
                executive_summary="unsafe jane.client@example.com",
                cro_view="unsafe jane.client@example.com",
                cfo_view="unsafe jane.client@example.com",
                token_usage=WatsonxTokenUsage(input_tokens=5, output_tokens=5, total_tokens=10),
            )

    original_scan = GuardrailService.scan

    def block_llm_output(self: GuardrailService, stage: str, payload: object) -> GuardrailResult:
        if stage == "llm_output":
            return GuardrailResult(
                stage=stage,
                scanner="test",
                passed=False,
                blocked=True,
                risk_score=1.0,
                categories=["pii"],
                message="blocked test output",
            )
        return original_scan(self, stage, payload)

    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("WATSONX_PROJECT_ID", "project-id")
    monkeypatch.setenv("WATSONX_APIKEY", "api-key")
    monkeypatch.setattr("rwa_agents.workflow.WatsonxClient", UnsafeWatsonxClient)
    monkeypatch.setattr(GuardrailService, "scan", block_llm_output)
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    assert response.status == "BLOCKED"
    assert "jane.client@example.com" not in response.final_commentary.executive_summary
    assert response.observability.llm_call_count == 2
    assert response.observability.guardrail_block_count >= 1
