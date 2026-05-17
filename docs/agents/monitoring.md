# RWA AI Agents - Monitoring Guide

**Document Version:** 1.0  
**Last Updated:** May 17, 2026  
**Audience:** DevOps, SRE, Platform Engineers

---

## Overview

This guide provides comprehensive monitoring and observability guidance for the RWA AI Agents system. It covers key metrics, SLA definitions, dashboard requirements, alerting rules, and troubleshooting procedures.

**Monitoring Stack:**
- **Metrics:** Prometheus
- **Dashboards:** Grafana
- **Alerting:** Alertmanager
- **Tracing:** LangFuse (optional)
- **Logs:** Structured JSON logging

---

## Key Metrics

### 1. Latency Metrics

**Metric Names:**
```
rwa_agents_workflow_duration_ms
rwa_agents_node_duration_ms{node="<node_name>"}
rwa_agents_llm_call_duration_ms{agent="<agent_name>"}
```

**Labels:**
- `node`: Node name (e.g., "DataAnalystAgent", "SupervisorAgent")
- `agent`: Agent name
- `status`: Workflow status ("COMPLETED", "LOOP_LIMIT_REACHED", "BLOCKED")

**Percentiles to Track:**
- p50 (median)
- p95 (95th percentile)
- p99 (99th percentile)
- p99.9 (99.9th percentile)

**PromQL Queries:**
```promql
# Workflow latency p95
histogram_quantile(0.95, 
  rate(rwa_agents_workflow_duration_ms_bucket[5m])
)

# Per-node latency p95
histogram_quantile(0.95, 
  rate(rwa_agents_node_duration_ms_bucket[5m])
) by (node)

# LLM call latency by agent
histogram_quantile(0.95, 
  rate(rwa_agents_llm_call_duration_ms_bucket[5m])
) by (agent)
```

### 2. Success Metrics

**Metric Names:**
```
rwa_agents_workflow_total{status="<status>"}
rwa_agents_workflow_success_rate
rwa_agents_guardrail_block_rate
rwa_agents_consensus_reached_rate
```

**PromQL Queries:**
```promql
# Success rate (last 5 minutes)
sum(rate(rwa_agents_workflow_total{status="COMPLETED"}[5m])) /
sum(rate(rwa_agents_workflow_total[5m]))

# Guardrail block rate
sum(rate(rwa_agents_guardrail_blocked_total[5m])) /
sum(rate(rwa_agents_guardrail_scans_total[5m]))

# Consensus reached rate
sum(rate(rwa_agents_consensus_reached_total[5m])) /
sum(rate(rwa_agents_workflow_total{status="COMPLETED"}[5m]))
```

### 3. Resource Metrics

**Metric Names:**
```
rwa_agents_tokens_total{type="<input|output>"}
rwa_agents_cost_usd_total
rwa_agents_llm_calls_total{agent="<agent_name>"}
rwa_agents_cache_hits_total
rwa_agents_cache_misses_total
```

**PromQL Queries:**
```promql
# Tokens per request (average over 5 minutes)
rate(rwa_agents_tokens_total[5m]) /
rate(rwa_agents_workflow_total[5m])

# Cost per request
rate(rwa_agents_cost_usd_total[5m]) /
rate(rwa_agents_workflow_total[5m])

# LLM calls per request
rate(rwa_agents_llm_calls_total[5m]) /
rate(rwa_agents_workflow_total[5m])

# Cache hit rate
rate(rwa_agents_cache_hits_total[5m]) /
(rate(rwa_agents_cache_hits_total[5m]) + rate(rwa_agents_cache_misses_total[5m]))
```

### 4. Quality Metrics

**Metric Names:**
```
rwa_agents_validation_flags_total{severity="<severity>"}
rwa_agents_critical_findings_total
rwa_agents_loop_limit_reached_total
rwa_agents_error_total{error_type="<type>"}
rwa_agents_recovery_total{strategy="<strategy>"}
```

**PromQL Queries:**
```promql
# Validation flag rate by severity
rate(rwa_agents_validation_flags_total[5m]) by (severity)

# Critical finding rate
rate(rwa_agents_critical_findings_total[5m]) /
rate(rwa_agents_workflow_total[5m])

# Loop limit reached rate
rate(rwa_agents_loop_limit_reached_total[5m]) /
rate(rwa_agents_workflow_total[5m])

# Error recovery rate
rate(rwa_agents_recovery_total[5m]) /
rate(rwa_agents_error_total[5m])
```

---

## SLA Definitions

### Service Level Objectives (SLOs)

| Metric | Target | Measurement Window | Severity |
|--------|--------|-------------------|----------|
| **Availability** | 99.9% | 30 days | Critical |
| **Latency (p95)** | < 10s | 5 minutes | Critical |
| **Latency (p99)** | < 15s | 5 minutes | Warning |
| **Success Rate** | > 99.5% | 5 minutes | Critical |
| **Token Budget** | < 5000 per request | 5 minutes | Warning |
| **Cost Budget** | < $0.50 per request | 5 minutes | Warning |
| **Cache Hit Rate** | > 30% | 1 hour | Info |
| **Error Recovery Rate** | > 80% | 5 minutes | Warning |

### Service Level Indicators (SLIs)

**Availability SLI:**
```promql
# Percentage of successful requests
sum(rate(rwa_agents_workflow_total{status="COMPLETED"}[30d])) /
sum(rate(rwa_agents_workflow_total[30d])) * 100
```

**Latency SLI:**
```promql
# Percentage of requests under 10s
sum(rate(rwa_agents_workflow_duration_ms_bucket{le="10000"}[5m])) /
sum(rate(rwa_agents_workflow_duration_ms_count[5m])) * 100
```

**Error Budget:**
```
# For 99.9% availability over 30 days
Total requests: 1,000,000
Allowed failures: 1,000 (0.1%)
Error budget: 1,000 failed requests
```

---

## Dashboard Requirements

### 1. Executive Dashboard

**Purpose:** High-level overview for management

**Panels:**
1. **Current Status** (Single Stat)
   - Requests/minute
   - Success rate (last 5m)
   - Average latency (last 5m)
   - Current cost/request

2. **SLA Compliance** (Gauge)
   - Availability vs. 99.9% target
   - Latency p95 vs. 10s target
   - Success rate vs. 99.5% target

3. **Cost Trends** (Time Series)
   - Cost per request over time
   - Total daily cost
   - Token usage trends

4. **Quality Indicators** (Bar Chart)
   - Validation flags by severity
   - Critical findings rate
   - Consensus reached rate

### 2. Operations Dashboard

**Purpose:** Detailed metrics for SRE/DevOps

**Panels:**
1. **Latency Breakdown** (Time Series)
   - Workflow latency (p50, p95, p99)
   - Per-node latency
   - LLM call latency by agent

2. **Throughput** (Time Series)
   - Requests per second
   - Successful requests/s
   - Failed requests/s

3. **Error Analysis** (Time Series + Table)
   - Error rate by type
   - Recovery rate by strategy
   - Top 10 error messages

4. **Resource Utilization** (Time Series)
   - Token usage (input/output)
   - LLM calls per request
   - Cache hit/miss rate

5. **Guardrail Activity** (Time Series)
   - Scans per stage
   - Block rate by category
   - Sanitization rate

### 3. Performance Dashboard

**Purpose:** Performance optimization and capacity planning

**Panels:**
1. **Latency Heatmap** (Heatmap)
   - Request latency distribution over time
   - Identify patterns and anomalies

2. **Node Performance** (Bar Chart)
   - Average duration by node
   - p95 duration by node
   - Slowest nodes

3. **Cache Effectiveness** (Time Series + Pie Chart)
   - Hit rate over time
   - Hit/miss distribution
   - Cache size and evictions

4. **Parallel Execution** (Time Series)
   - Parallel vs. sequential time
   - Speedup factor
   - Concurrency level

5. **Token Efficiency** (Time Series)
   - Tokens per request trend
   - Input vs. output token ratio
   - Cost per token

### 4. Quality Dashboard

**Purpose:** Data quality and compliance monitoring

**Panels:**
1. **Validation Flags** (Time Series + Table)
   - Flags by severity over time
   - Top validation issues
   - Flags requiring intervention

2. **Guardrail Effectiveness** (Time Series)
   - PII detection rate
   - Prompt injection blocks
   - Toxicity detections

3. **Consensus Metrics** (Time Series)
   - Consensus reached rate
   - Loop iterations distribution
   - Loop limit reached rate

4. **Agent Quality** (Bar Chart)
   - Findings per agent
   - Critical findings by agent
   - Agent execution success rate

---

## Alerting Rules

### Critical Alerts

**1. High Latency**
```yaml
- alert: RwaAgentsHighLatency
  expr: |
    histogram_quantile(0.95, 
      rate(rwa_agents_workflow_duration_ms_bucket[5m])
    ) > 10000
  for: 5m
  labels:
    severity: critical
    team: rwa-platform
    page: "true"
  annotations:
    summary: "RWA Agents p95 latency exceeds 10s"
    description: "p95 latency is {{ $value }}ms (threshold: 10000ms)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-high-latency"
```

**2. Low Success Rate**
```yaml
- alert: RwaAgentsLowSuccessRate
  expr: |
    sum(rate(rwa_agents_workflow_total{status="COMPLETED"}[5m])) /
    sum(rate(rwa_agents_workflow_total[5m])) < 0.995
  for: 5m
  labels:
    severity: critical
    team: rwa-platform
    page: "true"
  annotations:
    summary: "RWA Agents success rate below 99.5%"
    description: "Success rate is {{ $value | humanizePercentage }} (threshold: 99.5%)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-low-success-rate"
```

**3. Service Down**
```yaml
- alert: RwaAgentsServiceDown
  expr: up{job="rwa-agents"} == 0
  for: 1m
  labels:
    severity: critical
    team: rwa-platform
    page: "true"
  annotations:
    summary: "RWA Agents service is down"
    description: "Service has been down for more than 1 minute"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-service-down"
```

### Warning Alerts

**4. High Guardrail Block Rate**
```yaml
- alert: RwaAgentsHighGuardrailBlockRate
  expr: |
    sum(rate(rwa_agents_guardrail_blocked_total[5m])) /
    sum(rate(rwa_agents_guardrail_scans_total[5m])) > 0.1
  for: 10m
  labels:
    severity: warning
    team: rwa-platform
  annotations:
    summary: "High guardrail block rate detected"
    description: "Block rate is {{ $value | humanizePercentage }} (threshold: 10%)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-high-block-rate"
```

**5. Low Consensus Rate**
```yaml
- alert: RwaAgentsLowConsensusRate
  expr: |
    sum(rate(rwa_agents_consensus_reached_total[5m])) /
    sum(rate(rwa_agents_workflow_total{status="COMPLETED"}[5m])) < 0.8
  for: 10m
  labels:
    severity: warning
    team: rwa-platform
  annotations:
    summary: "Low consensus rate in agent workflows"
    description: "Consensus rate is {{ $value | humanizePercentage }} (threshold: 80%)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-low-consensus"
```

**6. Cost Spike**
```yaml
- alert: RwaAgentsCostSpike
  expr: |
    rate(rwa_agents_cost_usd_total[5m]) /
    rate(rwa_agents_workflow_total[5m]) > 0.50
  for: 10m
  labels:
    severity: warning
    team: rwa-platform
  annotations:
    summary: "Cost per request exceeds budget"
    description: "Cost is ${{ $value }} per request (threshold: $0.50)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-cost-spike"
```

**7. High Error Rate**
```yaml
- alert: RwaAgentsHighErrorRate
  expr: |
    rate(rwa_agents_error_total[5m]) /
    rate(rwa_agents_workflow_total[5m]) > 0.05
  for: 10m
  labels:
    severity: warning
    team: rwa-platform
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-high-error-rate"
```

### Info Alerts

**8. Low Cache Hit Rate**
```yaml
- alert: RwaAgentsLowCacheHitRate
  expr: |
    rate(rwa_agents_cache_hits_total[1h]) /
    (rate(rwa_agents_cache_hits_total[1h]) + rate(rwa_agents_cache_misses_total[1h])) < 0.3
  for: 1h
  labels:
    severity: info
    team: rwa-platform
  annotations:
    summary: "Cache hit rate below target"
    description: "Hit rate is {{ $value | humanizePercentage }} (target: 30%)"
    runbook_url: "https://docs.example.com/runbooks/rwa-agents-low-cache-hit-rate"
```

---

## Troubleshooting Guide

### High Latency Issues

**Symptoms:**
- p95 latency > 10s
- Slow response times
- User complaints about performance

**Diagnosis Steps:**

1. **Check Node Timings:**
```bash
# Query Prometheus for per-node latency
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=histogram_quantile(0.95, rate(rwa_agents_node_duration_ms_bucket[5m])) by (node)'
```

2. **Identify Slow Nodes:**
```python
# From observability metadata
for node, duration_ms in response.observability.node_timings.items():
    if duration_ms > 3000:
        print(f"Slow node: {node} took {duration_ms:.2f}ms")
```

3. **Check LLM Performance:**
```bash
# Query for LLM call latency
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=histogram_quantile(0.95, rate(rwa_agents_llm_call_duration_ms_bucket[5m])) by (agent)'
```

**Common Causes:**
- WatsonX service degradation
- Network latency to external services
- Large prompt sizes
- Cache misses
- Parallel execution not working

**Solutions:**

1. **Enable/Optimize Caching:**
```python
cache = TokenOptimizer(
    max_size=2000,      # Increase cache size
    ttl_seconds=7200    # Increase TTL
)
```

2. **Reduce Prompt Size:**
```python
# Optimize prompts for brevity
# Remove unnecessary context
# Use prompt compression techniques
```

3. **Check WatsonX Health:**
```bash
# Monitor WatsonX service status
curl https://status.watsonx.ai/api/v2/status.json
```

4. **Increase Timeout:**
```python
retry = RetryStrategy(
    max_retries=3,
    base_delay=2.0,     # Increase base delay
    max_delay=60.0      # Increase max delay
)
```

### High Token Usage

**Symptoms:**
- Token count > 5000 per request
- Cost > $0.50 per request
- Budget alerts firing

**Diagnosis Steps:**

1. **Check Token Breakdown:**
```python
print(f"Input tokens: {response.observability.input_token_count}")
print(f"Output tokens: {response.observability.output_token_count}")
print(f"Cost breakdown: {response.observability.cost_breakdown}")
```

2. **Identify Expensive Agents:**
```bash
# Query for tokens by agent
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=rate(rwa_agents_tokens_total[5m]) by (agent)'
```

**Common Causes:**
- Verbose prompts
- Large input data
- Multiple LLM calls
- Low cache hit rate
- Unnecessary context

**Solutions:**

1. **Enable Caching:**
```python
# Ensure caching is enabled
cache = TokenOptimizer(max_size=1000, ttl_seconds=3600)
```

2. **Optimize Prompts:**
```python
# Use concise system prompts
# Remove redundant instructions
# Use structured output formats
```

3. **Reduce Input Size:**
```python
# Limit number of records
# Summarize large datasets
# Use sampling for analysis
```

4. **Monitor Cache Hit Rate:**
```python
stats = cache.get_stats()
if stats['hit_rate'] < 0.3:
    # Investigate cache configuration
    # Check for cache key collisions
    # Increase cache size or TTL
```

### Guardrail Blocks

**Symptoms:**
- High block rate (> 10%)
- Requests returning BLOCKED status
- PII detection alerts

**Diagnosis Steps:**

1. **Check Guardrail Results:**
```python
for result in response.observability.guardrail_results:
    if result.blocked:
        print(f"Stage: {result.stage}")
        print(f"Categories: {result.categories}")
        print(f"Risk score: {result.risk_score}")
        print(f"Message: {result.message}")
```

2. **Analyze Block Patterns:**
```bash
# Query for blocks by category
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=rate(rwa_agents_guardrail_blocked_total[5m]) by (category)'
```

**Common Causes:**
- PII in input data
- Prompt injection attempts
- Sensitive information leakage
- Misconfigured thresholds

**Solutions:**

1. **Enable Sanitization:**
```python
# Guardrail service automatically sanitizes when possible
guardrail = GuardrailService()
safe_text, result = guardrail.scan_with_recovery(text, stage)
```

2. **Adjust Thresholds:**
```python
config = GuardrailConfig(
    pii_detection_threshold=0.85,      # Increase threshold
    prompt_injection_threshold=0.90    # Increase threshold
)
```

3. **Pre-process Input:**
```python
# Anonymize data before submission
# Use ASSET-### identifiers
# Remove email addresses, phone numbers
```

4. **Review Input Validation:**
```python
# Ensure proper validation
request = RwaAnalysisRequest.model_validate(payload)
# Validation automatically checks for PII-like patterns
```

### Low Cache Hit Rate

**Symptoms:**
- Cache hit rate < 30%
- High token usage
- Increased costs

**Diagnosis Steps:**

1. **Check Cache Statistics:**
```python
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']:.1%}")
print(f"Hits: {stats['hits']}")
print(f"Misses: {stats['misses']}")
print(f"Size: {stats['size']}/{stats['max_size']}")
```

2. **Analyze Cache Keys:**
```python
# Check for key diversity
# High diversity = low hit rate
```

**Common Causes:**
- Unique queries (no repetition)
- Short TTL
- Small cache size
- Cache key collisions
- Prompt variations

**Solutions:**

1. **Increase Cache Size:**
```python
cache = TokenOptimizer(
    max_size=2000,      # Increase from 1000
    ttl_seconds=3600
)
```

2. **Increase TTL:**
```python
cache = TokenOptimizer(
    max_size=1000,
    ttl_seconds=7200     # Increase from 3600
)
```

3. **Normalize Prompts:**
```python
# Ensure consistent prompt formatting
# Remove timestamps or unique identifiers
# Use canonical representations
```

4. **Pre-warm Cache:**
```python
# Cache common queries at startup
common_queries = load_common_queries()
for query in common_queries:
    cache.cached_llm_call(query, model_id, llm_callable)
```

### Error Recovery Failures

**Symptoms:**
- Low recovery rate (< 80%)
- Repeated errors
- Workflow failures

**Diagnosis Steps:**

1. **Check Error Records:**
```python
for error in response.observability.errors:
    print(f"Type: {error.error_type}")
    print(f"Node: {error.node}")
    print(f"Retry count: {error.retry_count}")
    print(f"Recovered: {error.recovered}")
    print(f"Strategy: {error.recovery_strategy}")
```

2. **Analyze Error Types:**
```bash
# Query for errors by type
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=rate(rwa_agents_error_total[5m]) by (error_type)'
```

**Common Causes:**
- Non-transient errors
- Insufficient retry attempts
- Short retry delays
- External service failures

**Solutions:**

1. **Increase Retry Attempts:**
```python
retry = RetryStrategy(
    max_retries=5,      # Increase from 3
    base_delay=1.0,
    max_delay=30.0
)
```

2. **Adjust Backoff Strategy:**
```python
retry = RetryStrategy(
    max_retries=3,
    base_delay=2.0,     # Increase base delay
    max_delay=60.0,     # Increase max delay
    exponential_base=2.5  # More aggressive backoff
)
```

3. **Implement Circuit Breaker:**
```python
# Add circuit breaker for repeated failures
# Fail fast after threshold
# Prevent cascading failures
```

4. **Add Fallback Logic:**
```python
# Implement graceful degradation
# Return partial results
# Use cached responses
```

---

## Log Analysis

### Structured Logging Format

All logs are emitted in JSON format:

```json
{
  "timestamp": "2026-05-17T13:00:00.000Z",
  "level": "INFO",
  "logger": "rwa_agents.workflow",
  "message": "Workflow completed successfully",
  "request_id": "req-abc123",
  "duration_ms": 5123.45,
  "status": "COMPLETED",
  "token_count": 2800,
  "cost_usd": 0.28
}
```

### Common Log Queries

**1. Find High Latency Requests:**
```bash
# Using jq
cat logs.json | jq 'select(.duration_ms > 10000)'
```

**2. Find Failed Requests:**
```bash
cat logs.json | jq 'select(.status != "COMPLETED")'
```

**3. Find Expensive Requests:**
```bash
cat logs.json | jq 'select(.cost_usd > 0.50)'
```

**4. Analyze Error Patterns:**
```bash
cat logs.json | jq 'select(.level == "ERROR") | .message' | sort | uniq -c
```

---

## Performance Tuning

### Optimization Checklist

- [ ] Enable response caching
- [ ] Configure appropriate cache size and TTL
- [ ] Enable parallel tool execution
- [ ] Optimize prompt lengths
- [ ] Use appropriate retry configuration
- [ ] Monitor and adjust guardrail thresholds
- [ ] Pre-warm cache with common queries
- [ ] Implement request batching where possible
- [ ] Use streaming for long responses
- [ ] Monitor external service health

### Capacity Planning

**Current Capacity:**
- Throughput: ~100 requests/minute
- Average latency: 5.1s
- Average cost: $0.28/request

**Scaling Considerations:**
- Horizontal scaling: Add more instances
- Vertical scaling: Increase resources per instance
- Cache scaling: Increase cache size for higher hit rates
- Database scaling: Optimize checkpoint storage

**Cost Projections:**
```
Daily requests: 100,000
Cost per request: $0.28
Daily cost: $28,000
Monthly cost: $840,000
```

---

## Related Documentation

- [Implementation Summary](./RCT-AGENTS-IMPROVEMENTS.md) - Detailed improvements
- [Architecture Documentation](./architecture.md) - System architecture
- [Alerting Configuration](../../observability/agents-alerts.yaml) - Alert rules
- [API Contracts](./contracts.md) - Request/response schemas

---

**Document Maintained By:** RWA Platform Team  
**Last Updated:** May 17, 2026  
**Next Review:** August 2026