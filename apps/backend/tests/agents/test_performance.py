from __future__ import annotations

import time
from decimal import Decimal

import pytest

from rwa_agents.cache import TokenOptimizer
from rwa_agents.schemas import RwaAnalysisRequest
from rwa_agents.tools import DataAnalystTool, RiskExpertTool, execute_tools_parallel_sync
from rwa_agents.workflow import run_rwa_analysis

from .test_validation import valid_payload


@pytest.mark.performance
def test_workflow_latency() -> None:
    """Test workflow completes within SLA (10 seconds)."""
    request = RwaAnalysisRequest.model_validate(valid_payload())

    start_time = time.perf_counter()
    response = run_rwa_analysis(request)
    end_time = time.perf_counter()

    duration_seconds = end_time - start_time

    # Should complete successfully
    assert response.status == "COMPLETED"

    # Should complete within 10 second SLA
    assert duration_seconds < 10.0, f"Workflow took {duration_seconds:.2f}s, exceeds 10s SLA"

    # Log performance metrics
    print(f"\nWorkflow latency: {duration_seconds:.3f}s")
    print(f"Node transitions: {response.observability.node_transition_count}")
    print(f"Tool calls: {response.observability.tool_call_count}")


@pytest.mark.performance
def test_token_efficiency() -> None:
    """Test token usage stays within budget (5000 tokens, $0.50)."""
    request = RwaAnalysisRequest.model_validate(valid_payload())

    response = run_rwa_analysis(request)

    # Should complete successfully
    assert response.status == "COMPLETED"

    # Check token usage
    total_tokens = response.observability.total_token_count
    total_cost = float(response.observability.total_cost_usd)

    # Should stay within token budget (5000 tokens)
    assert total_tokens <= 5000, f"Used {total_tokens} tokens, exceeds 5000 token budget"

    # Should stay within cost budget ($0.50)
    assert total_cost <= 0.50, f"Cost ${total_cost:.4f}, exceeds $0.50 budget"

    # Log efficiency metrics
    print(f"\nToken usage: {total_tokens} tokens")
    print(f"Total cost: ${total_cost:.6f}")
    print(f"Cost per token: ${total_cost / total_tokens:.6f}" if total_tokens > 0 else "N/A")


@pytest.mark.performance
def test_cache_effectiveness() -> None:
    """Test cache hit rate for duplicate requests."""
    cache = TokenOptimizer(max_size=100, ttl_seconds=300)

    # Simulate LLM call
    def mock_llm_call(prompt: str) -> str:
        time.sleep(0.1)  # Simulate LLM latency
        return f"Response to: {prompt[:50]}"

    prompt = "Analyze the following RWA data for compliance issues..."
    model_id = "test-model-v1"

    # First call - cache miss
    start_time = time.perf_counter()
    result1 = cache.cached_llm_call(
        prompt=prompt,
        model_id=model_id,
        llm_callable=lambda: mock_llm_call(prompt),
    )
    first_call_duration = time.perf_counter() - start_time

    # Second call - cache hit
    start_time = time.perf_counter()
    result2 = cache.cached_llm_call(
        prompt=prompt,
        model_id=model_id,
        llm_callable=lambda: mock_llm_call(prompt),
    )
    second_call_duration = time.perf_counter() - start_time

    # Results should be identical
    assert result1 == result2

    # Cache hit should be much faster
    assert second_call_duration < first_call_duration / 10, "Cache hit not significantly faster"

    # Check cache statistics
    stats = cache.get_stats()
    assert stats["hits"] == 1, "Expected 1 cache hit"
    assert stats["misses"] == 1, "Expected 1 cache miss"
    assert stats["hit_rate"] == 0.5, "Expected 50% hit rate"

    # Make 8 more calls to same prompt
    for _ in range(8):
        cache.cached_llm_call(
            prompt=prompt,
            model_id=model_id,
            llm_callable=lambda: mock_llm_call(prompt),
        )

    # Check final statistics
    final_stats = cache.get_stats()
    assert final_stats["hits"] == 9, "Expected 9 cache hits"
    assert final_stats["misses"] == 1, "Expected 1 cache miss"
    assert final_stats["hit_rate"] == 0.9, "Expected 90% hit rate"

    # Log cache metrics
    print("\nCache statistics:")
    print(f"  Hits: {final_stats['hits']}")
    print(f"  Misses: {final_stats['misses']}")
    print(f"  Hit rate: {final_stats['hit_rate']:.1%}")
    print(f"  First call: {first_call_duration * 1000:.2f}ms")
    print(f"  Cached call: {second_call_duration * 1000:.2f}ms")
    print(f"  Speedup: {first_call_duration / second_call_duration:.1f}x")


@pytest.mark.performance
def test_parallel_tool_execution_speedup() -> None:
    """Test parallel execution provides speedup over sequential."""
    request = RwaAnalysisRequest.model_validate(valid_payload())

    data_tool = DataAnalystTool()
    risk_tool = RiskExpertTool()

    # Sequential execution
    start_time = time.perf_counter()
    result1 = data_tool.execute(request)
    result2 = risk_tool.execute(request)
    sequential_duration = time.perf_counter() - start_time

    # Parallel execution
    start_time = time.perf_counter()
    results = execute_tools_parallel_sync([
        (data_tool, (request,), {}),
        (risk_tool, (request,), {}),
    ])
    parallel_duration = time.perf_counter() - start_time

    # Results should be equivalent
    assert len(results) == 2
    assert not isinstance(results[0], Exception)
    assert not isinstance(results[1], Exception)

    # Parallel should be faster (at least 1.2x speedup)
    speedup = sequential_duration / parallel_duration
    assert speedup >= 1.2, f"Parallel execution speedup {speedup:.2f}x is less than 1.2x"

    # Log performance metrics
    print("\nParallel execution performance:")
    print(f"  Sequential: {sequential_duration * 1000:.2f}ms")
    print(f"  Parallel: {parallel_duration * 1000:.2f}ms")
    print(f"  Speedup: {speedup:.2f}x")


@pytest.mark.performance
def test_memory_usage_stability() -> None:
    """Test memory usage remains stable across multiple requests."""
    import gc
    import sys

    # Force garbage collection
    gc.collect()

    # Get baseline memory
    if hasattr(sys, "getsizeof"):
        baseline_objects = len(gc.get_objects())

    # Run multiple requests
    for i in range(10):
        payload = valid_payload()
        payload["request_id"] = f"memory-test-{i}"
        request = RwaAnalysisRequest.model_validate(payload)
        response = run_rwa_analysis(request)
        assert response.status == "COMPLETED"

    # Force garbage collection
    gc.collect()

    # Check memory growth
    if hasattr(sys, "getsizeof"):
        final_objects = len(gc.get_objects())
        object_growth = final_objects - baseline_objects

        # Object growth should be reasonable (less than 10000 objects)
        assert object_growth < 10000, f"Memory leak suspected: {object_growth} new objects"

        print("\nMemory stability:")
        print(f"  Baseline objects: {baseline_objects}")
        print(f"  Final objects: {final_objects}")
        print(f"  Growth: {object_growth} objects")


@pytest.mark.performance
def test_large_dataset_performance() -> None:
    """Test performance with large dataset (1000 records)."""
    # Create large payload
    payload = valid_payload()

    base_input = payload["rwa_input_data"][0].copy()
    base_output = payload["rwa_output_results"][0].copy()

    large_inputs = []
    large_outputs = []

    for i in range(1000):
        input_record = base_input.copy()
        input_record["asset_id"] = f"ASSET-PERF-{i:05d}"
        input_record["exposure_amount"] = str(Decimal("1000000") + Decimal(i * 1000))
        large_inputs.append(input_record)

        output_record = base_output.copy()
        output_record["asset_id"] = f"ASSET-PERF-{i:05d}"
        output_record["rwa_amount"] = str(Decimal("750000") + Decimal(i * 750))
        large_outputs.append(output_record)

    payload["rwa_input_data"] = large_inputs
    payload["rwa_output_results"] = large_outputs

    request = RwaAnalysisRequest.model_validate(payload)

    # Measure performance
    start_time = time.perf_counter()
    response = run_rwa_analysis(request)
    duration = time.perf_counter() - start_time

    # Should complete successfully
    assert response.status == "COMPLETED"

    # Should complete within reasonable time (30 seconds for 1000 records)
    assert duration < 30.0, f"Large dataset took {duration:.2f}s, exceeds 30s threshold"

    # Should have findings
    assert len(response.agent_findings) > 0

    # Log performance metrics
    print("\nLarge dataset performance:")
    print("  Records: 1000")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Records/second: {1000 / duration:.1f}")
    print(f"  Findings: {len(response.agent_findings)}")


@pytest.mark.performance
def test_cache_memory_efficiency() -> None:
    """Test cache memory usage with many entries."""
    cache = TokenOptimizer(max_size=1000, ttl_seconds=3600)

    # Add many entries
    for i in range(1500):  # More than max_size
        prompt = f"Test prompt number {i} with some content"
        model_id = "test-model"
        result = cache.cached_llm_call(
            prompt=prompt,
            model_id=model_id,
            llm_callable=lambda: f"Response {i}",
        )
        assert result == f"Response {i}"

    # Cache should not exceed max_size
    stats = cache.get_stats()
    assert stats["size"] <= 1000, f"Cache size {stats['size']} exceeds max_size 1000"

    # Should have evicted oldest entries
    assert stats["misses"] == 1500, "All entries should be cache misses"

    print("\nCache memory efficiency:")
    print("  Entries added: 1500")
    print(f"  Cache size: {stats['size']}")
    print(f"  Max size: {stats['max_size']}")


# Made with Bob
