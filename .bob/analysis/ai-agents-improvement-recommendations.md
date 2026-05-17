# AI Agents System - Improvement Recommendations

**Analysis Date:** 2026-05-17  
**Source:** LangFuse Events Export (1779019867878-lf-events-export-cmp9mqwv205e6ad07fnqsh1ua.json)  
**Traces Analyzed:** 4 distinct workflows (watsonx-all-agents-smoke, agent-test-run, briefing-1779018409164)

---

## Executive Summary

The multi-agent RWA analysis system demonstrates a well-structured workflow with comprehensive guardrails. However, analysis reveals opportunities for optimization in observability, error handling, and performance.

---

## 1. Observability & Instrumentation Issues

### 1.1 Missing Latency Data
**Severity:** HIGH  
**Finding:** All events have `latencyMs: null`, `timeToFirstTokenMs: null`, and `endTime: null`

**Impact:**
- Cannot measure node execution time
- Unable to identify performance bottlenecks
- No SLA monitoring capability
- Difficult to optimize slow paths

**Recommendation:**
```python
# Add timing instrumentation to each node
class TimedNode:
    def __init__(self, node_name: str):
        self.node_name = node_name
        self.start_time = None
        self.end_time = None
    
    async def __aenter__(self):
        self.start_time = time.perf_counter()
        return self
    
    async def __aexit__(self, *args):
        self.end_time = time.perf_counter()
        latency_ms = (self.end_time - self.start_time) * 1000
        # Log to LangFuse with actual latency
        langfuse.span(
            name=self.node_name,
            start_time=self.start_time,
            end_time=self.end_time,
            metadata={"latency_ms": latency_ms}
        )
```

### 1.2 Empty Token Usage Tracking
**Severity:** MEDIUM  
**Finding:** `usageDetails: {}` and `costDetails: {}` are empty despite LLM calls

**Impact:**
- No cost tracking per request
- Cannot optimize for token efficiency
- Budget overruns risk

**Recommendation:**
- Capture token counts from WatsonX responses
- Calculate costs based on model pricing
- Add to `ObservabilityMetadata.total_token_count`
- Track per-agent token usage for cost attribution

---

## 2. Guardrail System Analysis

### 2.1 Guardrail Coverage
**Finding:** 8 distinct guardrail stages identified:
1. `request_validation` - Input validation
2. `data_analyst_prompt` - Prompt safety
3. `risk_expert_prompt` - Prompt safety
4. `supervisor_prompt` - Prompt safety
5. `llm_input` - Pre-LLM guardrails
6. `llm_output` - Post-LLM guardrails
7. `worker_outputs` - Agent output validation
8. `final_output` - Final response validation

**Strengths:**
- Comprehensive coverage across workflow
- Multiple scanner types (local, llm_guard, test)
- PII detection active

### 2.2 Guardrail Blocking Behavior
**Finding:** One trace shows PII detection blocking:
```json
{
  "categories": "[\"pii\"]",
  "risk_score": "1",
  "blocked": "true",
  "passed": "false",
  "scanner": "test"
}
```

**Issue:** System correctly blocks but lacks recovery mechanism

**Recommendation:**
```python
class GuardrailRecovery:
    """Handle guardrail failures gracefully"""
    
    async def handle_pii_detection(self, content: str) -> str:
        """Sanitize PII and retry"""
        sanitized = self.redact_pii(content)
        return sanitized
    
    async def handle_prompt_injection(self, prompt: str) -> str:
        """Escape injection attempts"""
        escaped = self.escape_injection_patterns(prompt)
        return escaped
    
    def should_retry(self, guardrail_result: GuardrailResult) -> bool:
        """Determine if retry is possible"""
        return guardrail_result.risk_score < 0.8 and \
               guardrail_result.sanitized_text_used
```

---

## 3. Agent Workflow Optimization

### 3.1 Parallel Agent Execution
**Finding:** DataAnalystAgent and RiskExpertAgent run in parallel (same timestamps)

**Current Flow:**
```
RequestValidation → AgentStateBuilt → AnalysisPhase → 
  ├─ DataAnalystAgent (parallel)
  └─ RiskExpertAgent (parallel)
→ AnalysisFanIn → SupervisorAgent → FinalOutputGuard → FinalStructuredResponse
```

**Strengths:**
- Efficient parallel execution
- Proper fan-in synchronization

**Recommendation:**
- Add timeout handling for parallel agents
- Implement partial result handling if one agent fails
- Add circuit breaker for repeated failures

### 3.2 Loop Limit Handling
**Finding:** `loop_limit: 2` enforced, status can be `LOOP_LIMIT_REACHED`

**Issue:** No graceful degradation when limit reached

**Recommendation:**
```python
class SupervisorAgent:
    async def handle_loop_limit(self, state: AgentState) -> FinalCommentary:
        """Provide best-effort results when loop limit reached"""
        return FinalCommentary(
            status="LOOP_LIMIT_REACHED",
            consensus_reached=False,
            executive_summary=self.synthesize_partial_results(state),
            messages=[
                "Analysis incomplete: loop limit reached",
                "Results based on partial consensus"
            ],
            validation_flags=[
                ValidationFlag(
                    code="INCOMPLETE_ANALYSIS",
                    severity="warning",
                    message="Loop limit reached before full consensus",
                    source_agent="SupervisorAgent"
                )
            ]
        )
```

---

## 4. Prompt Management

### 4.1 Prompt Versioning
**Finding:** All prompts use `source: "local_fallback"` with `prompt_version: "local-v1"`

**Issue:** No remote prompt management or A/B testing capability

**Recommendation:**
```python
class PromptManager:
    def __init__(self, langfuse_client):
        self.langfuse = langfuse_client
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def get_prompt(self, name: str, version: str = "latest") -> str:
        """Fetch prompt with fallback to local"""
        try:
            # Try remote first
            prompt = await self.langfuse.get_prompt(name, version)
            return PromptUsage(
                prompt_name=name,
                prompt_version=prompt.version,
                source="langfuse",
                fetch_status="success"
            )
        except Exception as e:
            # Fallback to local
            return self.load_local_prompt(name)
```

### 4.2 Prompt Templates
**Finding:** Three system prompts identified:
- `rwa-data-analyst-agent-system`
- `rwa-risk-expert-agent-system`
- `rwa-supervisor-agent-system`

**Recommendation:**
- Version prompts in LangFuse
- Enable A/B testing for prompt improvements
- Track prompt performance metrics

---

## 5. Error Handling & Resilience

### 5.1 Missing Error Context
**Finding:** No error traces in export despite test scenarios

**Recommendation:**
```python
class ErrorEnrichment:
    """Add context to errors for better debugging"""
    
    def enrich_error(self, error: Exception, context: dict) -> dict:
        return {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "node": context.get("node"),
            "agent": context.get("agent"),
            "trace_id": context.get("trace_id"),
            "state_snapshot": self.sanitize_state(context.get("state")),
            "retry_count": context.get("retry_count", 0),
            "timestamp": datetime.now(UTC).isoformat()
        }
```

### 5.2 Retry Strategy
**Recommendation:**
```python
class RetryStrategy:
    """Implement exponential backoff for transient failures"""
    
    async def retry_with_backoff(
        self,
        func: Callable,
        max_retries: int = 3,
        base_delay: float = 1.0
    ):
        for attempt in range(max_retries):
            try:
                return await func()
            except TransientError as e:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
```

---

## 6. Performance Optimization

### 6.1 Token Efficiency
**Finding:** Multiple LLM calls per workflow (3-4 calls typical)

**Recommendation:**
- Implement response caching for identical inputs
- Use streaming for long responses
- Optimize prompt length

```python
class TokenOptimizer:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=3600)
    
    async def cached_llm_call(self, prompt: str, model: str) -> str:
        cache_key = hashlib.sha256(f"{prompt}:{model}".encode()).hexdigest()
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = await self.llm.generate(prompt, model)
        self.cache[cache_key] = response
        return response
```

### 6.2 Parallel Tool Execution
**Finding:** DataTools and RiskTools execute sequentially within agents

**Recommendation:**
```python
async def execute_tools_parallel(self, tools: list[Tool]) -> dict:
    """Execute independent tools in parallel"""
    tasks = [tool.execute() for tool in tools if tool.can_run_parallel()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return self.merge_results(results)
```

---

## 7. Monitoring & Alerting

### 7.1 Key Metrics to Track
**Recommendation:** Implement monitoring for:

```python
class AgentMetrics:
    """Key metrics for monitoring"""
    
    # Latency metrics
    node_execution_time_p50: float
    node_execution_time_p95: float
    node_execution_time_p99: float
    
    # Success metrics
    workflow_success_rate: float
    guardrail_block_rate: float
    consensus_reached_rate: float
    
    # Resource metrics
    tokens_per_request: int
    cost_per_request: Decimal
    llm_calls_per_request: int
    
    # Quality metrics
    validation_flag_rate: float
    critical_finding_rate: float
    loop_limit_reached_rate: float
```

### 7.2 Alerting Rules
```yaml
alerts:
  - name: high_guardrail_block_rate
    condition: guardrail_block_rate > 0.1
    severity: warning
    
  - name: low_consensus_rate
    condition: consensus_reached_rate < 0.8
    severity: warning
    
  - name: high_latency
    condition: node_execution_time_p95 > 5000
    severity: critical
    
  - name: cost_spike
    condition: cost_per_request > 0.50
    severity: warning
```

---

## 8. Schema Improvements

### 8.1 Add Timing Fields
**File:** `apps/backend/src/rwa_agents/schemas.py`

```python
class ObservabilityMetadata(AgentSchema):
    # Existing fields...
    
    # Add timing metrics
    workflow_start_time: datetime | None = None
    workflow_end_time: datetime | None = None
    workflow_duration_ms: float | None = None
    
    # Add per-node timing
    node_timings: dict[str, float] = Field(default_factory=dict)
    
    # Add cost tracking
    total_cost_usd: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))
    cost_breakdown: dict[str, Decimal] = Field(default_factory=dict)
```

### 8.2 Add Error Tracking
```python
class ErrorRecord(AgentSchema):
    error_type: str
    error_message: str
    node: str
    agent: str | None = None
    timestamp: datetime
    retry_count: int = 0
    recovered: bool = False
    recovery_strategy: str | None = None

class ObservabilityMetadata(AgentSchema):
    # Add error tracking
    errors: list[ErrorRecord] = Field(default_factory=list)
    error_count: int = 0
    recovery_count: int = 0
```

---

## 9. Testing Recommendations

### 9.1 Add Performance Tests
```python
@pytest.mark.performance
async def test_workflow_latency():
    """Ensure workflow completes within SLA"""
    start = time.perf_counter()
    result = await run_rwa_analysis(test_request)
    duration = time.perf_counter() - start
    
    assert duration < 10.0, f"Workflow took {duration}s, exceeds 10s SLA"
    assert result.observability.workflow_duration_ms < 10000

@pytest.mark.performance
async def test_token_efficiency():
    """Ensure token usage is within budget"""
    result = await run_rwa_analysis(test_request)
    
    assert result.observability.total_token_count < 5000
    assert result.observability.total_cost_usd < Decimal("0.50")
```

### 9.2 Add Chaos Testing
```python
@pytest.mark.chaos
async def test_llm_timeout_handling():
    """Test graceful degradation on LLM timeout"""
    with mock_llm_timeout():
        result = await run_rwa_analysis(test_request)
        
        assert result.status in ["COMPLETED", "LOOP_LIMIT_REACHED"]
        assert any("timeout" in msg.lower() for msg in result.messages)

@pytest.mark.chaos
async def test_partial_agent_failure():
    """Test workflow continues with one agent failure"""
    with mock_agent_failure("DataAnalystAgent"):
        result = await run_rwa_analysis(test_request)
        
        assert result.status == "COMPLETED"
        assert "partial results" in result.final_commentary.executive_summary.lower()
```

---

## 10. Priority Implementation Roadmap

### Phase 1: Critical (Week 1-2)
1. ✅ Add latency tracking to all nodes
2. ✅ Implement token usage and cost tracking
3. ✅ Add error context enrichment
4. ✅ Set up basic monitoring dashboard

### Phase 2: High Priority (Week 3-4)
5. ✅ Implement guardrail recovery mechanisms
6. ✅ Add retry strategy with exponential backoff
7. ✅ Implement prompt versioning via LangFuse
8. ✅ Add performance tests

### Phase 3: Medium Priority (Week 5-6)
9. ✅ Optimize parallel tool execution
10. ✅ Implement response caching
11. ✅ Add chaos testing
12. ✅ Set up alerting rules

### Phase 4: Nice-to-Have (Week 7-8)
13. ✅ A/B testing framework for prompts
14. ✅ Advanced cost optimization
15. ✅ ML-based anomaly detection
16. ✅ Auto-scaling based on load

---

## Conclusion

The AI agents system demonstrates solid architecture with comprehensive guardrails. Key improvements focus on:

1. **Observability:** Add timing, cost, and error tracking
2. **Resilience:** Implement retry strategies and graceful degradation
3. **Performance:** Optimize token usage and parallel execution
4. **Monitoring:** Track key metrics and set up alerts

Implementing these recommendations will improve system reliability, reduce costs, and enable data-driven optimization.