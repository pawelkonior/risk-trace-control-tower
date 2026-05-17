from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

import pytest

from rwa_agents.guardrails import GuardrailService
from rwa_agents.schemas import RwaAnalysisRequest
from rwa_agents.workflow import run_rwa_analysis

from .test_validation import valid_payload


@pytest.mark.chaos
def test_llm_timeout_handling(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test graceful degradation when LLM times out."""
    # Enable watsonx for this test
    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_PROJECT_ID", "test-project")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_APIKEY", "test-key")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_URL", "https://test.watsonx.ai")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_MODEL_ID", "test-model")

    request = RwaAnalysisRequest.model_validate(valid_payload())

    # Mock WatsonX client to simulate timeout
    with patch("rwa_agents.workflow._new_watsonx_client") as mock_client_factory:
        mock_client = MagicMock()
        mock_generate = MagicMock()

        # Simulate timeout on first call, then succeed
        mock_generate.side_effect = [
            TimeoutError("LLM request timed out"),
            Mock(
                results=[
                    Mock(
                        generated_text="Deterministic analysis completed successfully.",
                        generated_token_count=50,
                        input_token_count=100,
                    )
                ]
            ),
        ]

        mock_client.generate.return_value = mock_generate
        mock_client_factory.return_value = mock_client

        # Should complete with fallback to deterministic analysis
        response = run_rwa_analysis(request)

        assert response.status == "COMPLETED"
        assert response.final_commentary.status == "COMPLETED"
        # Verify error was recorded in observability
        assert response.observability.error_count >= 1
        # Verify recovery happened
        assert response.observability.recovery_count >= 1


@pytest.mark.chaos
def test_partial_agent_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test workflow continues when one agent fails."""
    request = RwaAnalysisRequest.model_validate(valid_payload())

    # Mock one agent to fail
    with patch("rwa_agents.tools.analyze_data_quality") as mock_data_analyst:
        mock_data_analyst.side_effect = RuntimeError("Data analyst agent crashed")

        # Workflow should still complete with risk expert results
        response = run_rwa_analysis(request)

        # Should complete despite one agent failure
        assert response.status in ["COMPLETED", "LOOP_LIMIT_REACHED"]
        # Should have findings from at least one agent
        assert len(response.agent_findings) > 0
        # Error should be recorded
        assert response.observability.error_count >= 1


@pytest.mark.chaos
def test_guardrail_recovery(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test PII sanitization and retry when guardrail detects issues."""
    # Create payload with potential PII-like pattern
    payload = valid_payload()
    payload["rwa_input_data"][0]["asset_id"] = "ASSET-SUSPICIOUS-123"

    request = RwaAnalysisRequest.model_validate(payload)

    # Mock guardrail to detect PII on first scan, pass on retry
    scan_count = {"count": 0}

    def mock_scan(text: str, stage: str) -> Mock:
        scan_count["count"] += 1
        if scan_count["count"] == 1:
            # First scan: detect PII
            result = Mock()
            result.passed = False
            result.blocked = True
            result.risk_score = 0.9
            result.categories = ["pii"]
            result.stage = stage
            result.scanner = "test_scanner"
            result.sanitized_text = text.replace("SUSPICIOUS", "SANITIZED")
            return result
        # Subsequent scans: pass
        result = Mock()
        result.passed = True
        result.blocked = False
        result.risk_score = 0.0
        result.categories = []
        result.stage = stage
        result.scanner = "test_scanner"
        result.sanitized_text = None
        return result

    with patch.object(GuardrailService, "scan_text", side_effect=mock_scan):
        response = run_rwa_analysis(request)

        # Should complete after sanitization
        assert response.status == "COMPLETED"
        # PII should be detected
        assert response.observability.pii_detected is True
        # Should have guardrail results
        assert len(response.observability.guardrail_results) > 0


@pytest.mark.chaos
def test_retry_exhaustion(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test behavior when all retries are exhausted."""
    # Enable watsonx for this test
    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_PROJECT_ID", "test-project")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_APIKEY", "test-key")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_URL", "https://test.watsonx.ai")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_MODEL_ID", "test-model")

    request = RwaAnalysisRequest.model_validate(valid_payload())

    # Mock WatsonX client to always fail
    with patch("rwa_agents.workflow._new_watsonx_client") as mock_client_factory:
        mock_client = MagicMock()
        mock_generate = MagicMock()

        # Always fail
        mock_generate.side_effect = RuntimeError("Persistent LLM failure")

        mock_client.generate.return_value = mock_generate
        mock_client_factory.return_value = mock_client

        # Should fall back to deterministic analysis
        response = run_rwa_analysis(request)

        # Should complete with deterministic fallback
        assert response.status == "COMPLETED"
        assert response.final_commentary.status == "COMPLETED"
        # Should have deterministic findings
        assert len(response.agent_findings) > 0
        # Should record multiple errors (retries)
        assert response.observability.error_count >= 1


@pytest.mark.chaos
def test_concurrent_request_handling() -> None:
    """Test system handles concurrent requests without interference."""
    import concurrent.futures

    def run_analysis(request_id: str) -> str:
        payload = valid_payload()
        payload["request_id"] = request_id
        request = RwaAnalysisRequest.model_validate(payload)
        response = run_rwa_analysis(request)
        return response.status

    # Run 5 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(run_analysis, f"concurrent-test-{i}")
            for i in range(5)
        ]

        results = [future.result(timeout=30) for future in futures]

    # All should complete successfully
    assert all(status == "COMPLETED" for status in results)


@pytest.mark.chaos
def test_memory_pressure_handling() -> None:
    """Test system handles large payloads without memory issues."""
    # Create large payload with many records
    payload = valid_payload()

    # Duplicate records to create larger dataset
    base_input = payload["rwa_input_data"][0].copy()
    base_output = payload["rwa_output_results"][0].copy()

    large_inputs = []
    large_outputs = []

    for i in range(100):  # 100 records
        input_record = base_input.copy()
        input_record["asset_id"] = f"ASSET-LARGE-{i:04d}"
        large_inputs.append(input_record)

        output_record = base_output.copy()
        output_record["asset_id"] = f"ASSET-LARGE-{i:04d}"
        large_outputs.append(output_record)

    payload["rwa_input_data"] = large_inputs
    payload["rwa_output_results"] = large_outputs

    request = RwaAnalysisRequest.model_validate(payload)

    # Should complete without memory errors
    response = run_rwa_analysis(request)

    assert response.status == "COMPLETED"
    assert len(response.agent_findings) > 0


@pytest.mark.chaos
def test_network_interruption_recovery(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test recovery from network interruptions during LLM calls."""
    # Enable watsonx for this test
    monkeypatch.setenv("RWA_AGENTS_LLM_PROVIDER", "watsonx")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_PROJECT_ID", "test-project")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_APIKEY", "test-key")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_URL", "https://test.watsonx.ai")
    monkeypatch.setenv("RWA_AGENTS_WATSONX_MODEL_ID", "test-model")

    request = RwaAnalysisRequest.model_validate(valid_payload())

    # Mock WatsonX client to simulate network interruption then recovery
    with patch("rwa_agents.workflow._new_watsonx_client") as mock_client_factory:
        mock_client = MagicMock()
        mock_generate = MagicMock()

        # Simulate network error on first call, then succeed
        mock_generate.side_effect = [
            ConnectionError("Network connection lost"),
            Mock(
                results=[
                    Mock(
                        generated_text="Analysis completed after network recovery.",
                        generated_token_count=50,
                        input_token_count=100,
                    )
                ]
            ),
        ]

        mock_client.generate.return_value = mock_generate
        mock_client_factory.return_value = mock_client

        # Should recover and complete
        response = run_rwa_analysis(request)

        assert response.status == "COMPLETED"
        # Should record error and recovery
        assert response.observability.error_count >= 1
        assert response.observability.recovery_count >= 1


# Made with Bob
