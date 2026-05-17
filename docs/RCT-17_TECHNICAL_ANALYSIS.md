# RCT-17 Technical Analysis: LLM Guard, Langfuse Observability, Prompt Registry, Scores, and Checkpointing

**Epic:** RCT-13 - Deliver guarded, observable, multi-agent RWA executive commentary
**Story:** RCT-14 - Implement optimized guarded multi-agent RWA executive commentary workflow
**Task:** RCT-17 - Add guarded LLM boundaries, optional Langfuse observability, prompt registry, evaluation scores, and checkpointing
**Status:** In Progress
**Analyzed:** 2026-05-17

---

## Executive Summary

RCT-17 adds production safety and observability layers to the compact LangGraph runtime implemented in RCT-16. The task requires:

1. **LLM Guard Integration** - Input/output scanning at all LLM boundaries plus final output protection
2. **Langfuse Observability** - Optional tracing, prompt registry, and score submission
3. **Prompt Registry** - Abstraction layer with Langfuse and local fallback modes
4. **Evaluation Scores** - Faithfulness, Groundedness, Anomaly Detection, and guardrail metrics
5. **Checkpointing** - MemorySaver with stable thread_id for state persistence

**Current Implementation Status:** ~80% complete based on codebase analysis

---

## Current Implementation Analysis

### ✅ Already Implemented

#### 1. Basic Guardrail Infrastructure (`guardrails.py`)
- `GuardrailService` class with `scan()` method
- PII detection via `find_pii()` and `ensure_no_pii()`
- Prompt injection risk detection via `has_prompt_injection_risk()`
- `GuardrailResult` schema with stage, scanner, passed, blocked, risk_score, categories
- Integration at key workflow boundaries:
  - Request validation (line 34 in `workflow.py`)
  - Analysis phase prompts (lines 84-91)
  - Worker outputs (line 124)
  - Supervisor prompt (line 150)
  - Final output (line 205)

#### 2. Checkpointing (`checkpointing.py`)
- `MemorySaverCheckpoint` wrapper around LangGraph's MemorySaver
- Stable thread_id using `request.request_id`
- State persistence at key points (lines 42, 49 in `workflow.py`)
- Graph compilation with checkpointer (line 281)

#### 3. Observability Infrastructure (`observability.py`)
- `LocalObservability` class tracking:
  - Node transitions
  - Tool calls
  - Prompt usages
  - Guardrail results
  - Evaluation scores
- `ObservabilityMetadata` schema with all required fields
- Integration throughout workflow

#### 4. Prompt Registry (`prompts.py`)
- `PromptRegistry` class with `get()` method
- Local fallback prompts for all three agents
- `PromptUsage` tracking with source (local/langfuse)
- Langfuse-enabled flag from environment variable

#### 5. Comprehensive Schemas (`schemas.py`)
- All required Pydantic v2 models defined
- `GuardrailResult`, `PromptUsage`, `EvaluationScore`, `ObservabilityMetadata`
- Proper field validation and constraints

#### 6. Workflow Integration (`workflow.py`)
- Parallel worker execution (DataAnalyst + RiskExpert)
- Guardrail scanning at all boundaries
- Final output guard before response
- Blocked state handling
- Observability metadata in response

### ⚠️ Gaps Requiring Implementation

#### 1. **LLM Guard Enhancement** (Priority: HIGH)

**Current State:**
- Basic guardrail scanning exists but uses simple local checks
- No actual LLM Guard library integration
- Missing scanner configuration options

**Required Changes:**
```python
# Need to add to guardrails.py:
class LLMGuardService:
    def __init__(self, config: GuardrailConfig):
        self.enabled = config.llm_guard_enabled
        self.fail_fast = config.llm_guard_fail_fast
        self.input_scanners = self._init_input_scanners(config)
        self.output_scanners = self._init_output_scanners(config)

    def _init_input_scanners(self, config):
        # PromptInjection, Secrets, PII scanners
        pass

    def _init_output_scanners(self, config):
        # Toxicity, PII, FactualConsistency scanners
        pass
```

**Configuration Required:**
```python
# Add to schemas.py or new config.py:
class GuardrailConfig(BaseModel):
    llm_guard_enabled: bool = True
    llm_guard_fail_fast: bool = True
    llm_guard_block_on_prompt_injection: bool = True
    llm_guard_block_on_pii: bool = True
    llm_guard_block_on_secrets: bool = True
    llm_guard_input_timeout_seconds: int = 10
    llm_guard_output_timeout_seconds: int = 30
```

**Files to Modify:**
- `apps/backend/src/rwa_agents/guardrails.py` - Add LLM Guard scanners
- `apps/backend/src/rwa_agents/schemas.py` - Add GuardrailConfig
- `apps/backend/pyproject.toml` - Add `llm-guard` dependency

#### 2. **Langfuse Integration** (Priority: HIGH)

**Current State:**
- Langfuse flag exists but no actual integration
- No callback handler attachment
- No trace creation or span tracking

**Required Changes:**
```python
# Add to observability.py:
class LangfuseObservability:
    def __init__(self, request_id: str, config: LangfuseConfig):
        if config.enabled:
            from langfuse import Langfuse
            self.client = Langfuse(
                public_key=config.public_key,
                secret_key=config.secret_key,
                host=config.base_url
            )
            self.trace = self.client.trace(
                name="rwa_analysis",
                id=request_id
            )
        else:
            self.client = None
            self.trace = None
```

**Configuration Required:**
```python
class LangfuseConfig(BaseModel):
    langfuse_enabled: bool = False
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_base_url: str = "https://cloud.langfuse.com"
    langfuse_prompt_label: str = "production"
    langfuse_prompt_cache_ttl_seconds: int = 300
    langfuse_prompt_fetch_timeout_seconds: int = 5
```

**Files to Modify:**
- `apps/backend/src/rwa_agents/observability.py` - Add Langfuse client
- `apps/backend/src/rwa_agents/schemas.py` - Add LangfuseConfig
- `apps/backend/pyproject.toml` - Add `langfuse` dependency

#### 3. **Prompt Registry Enhancement** (Priority: MEDIUM)

**Current State:**
- Basic registry with local fallbacks exists
- No actual Langfuse prompt fetching
- No caching mechanism

**Required Changes:**
```python
# Enhance prompts.py:
class PromptRegistry:
    def __init__(self, config: LangfuseConfig):
        self.config = config
        self.cache: dict[str, tuple[str, datetime]] = {}
        if config.langfuse_enabled:
            from langfuse import Langfuse
            self.client = Langfuse(...)
        else:
            self.client = None

    def get(self, prompt_name: str) -> tuple[str, PromptUsage]:
        if self.config.langfuse_enabled:
            cached = self._get_from_cache(prompt_name)
            if cached:
                return cached
            return self._fetch_from_langfuse(prompt_name)
        return self._get_local_fallback(prompt_name)
```

**Files to Modify:**
- `apps/backend/src/rwa_agents/prompts.py` - Add caching and Langfuse fetching

#### 4. **Evaluation Scores** (Priority: MEDIUM)

**Current State:**
- Basic score recording exists (lines 213-218 in `workflow.py`)
- Only groundedness and faithfulness scores
- No Langfuse submission

**Required Scores:**
- ✅ Faithfulness (already exists)
- ✅ Groundedness (already exists)
- ❌ Anomaly_Detection (missing)
- ❌ Guardrail_Block_Count (partially exists in metadata)
- ❌ PII_Detected (partially exists in metadata)
- ❌ Prompt_Injection_Risk (partially exists in metadata)

**Required Changes:**
```python
# Add to observability.py:
def compute_scores(self, state: AgentState) -> list[EvaluationScore]:
    scores = [
        EvaluationScore(
            name="Faithfulness",
            value=1.0,
            comment="Quantitative validation used Python tools only"
        ),
        EvaluationScore(
            name="Groundedness",
            value=1.0,
            comment="Commentary synthesized from deterministic findings"
        ),
        EvaluationScore(
            name="Anomaly_Detection",
            value=1.0 if self._detect_anomalies(state) else 0.0,
            comment="Anomaly detection based on validation flags"
        ),
    ]
    return scores
```

**Files to Modify:**
- `apps/backend/src/rwa_agents/observability.py` - Add score computation
- `apps/backend/src/rwa_agents/workflow.py` - Call score computation

#### 5. **Final Output Guard Enhancement** (Priority: CRITICAL)

**Current State:**
- Final output guard exists (line 180 in `workflow.py`)
- Scans complete `FinalCommentary` object
- Blocks unsafe output correctly

**Gap:**
- Task description emphasizes scanning "complete structured final_commentary payload"
- Current implementation already does this correctly
- **No changes needed** - requirement is already met

---

## Implementation Plan

### Phase 1: LLM Guard Integration (2-3 hours)

**Files to Create/Modify:**
1. `apps/backend/src/rwa_agents/config.py` (NEW)
   - Add `GuardrailConfig` class
   - Add `LangfuseConfig` class
   - Environment variable loading

2. `apps/backend/src/rwa_agents/guardrails.py` (MODIFY)
   - Add LLM Guard scanner initialization
   - Implement input scanners (PromptInjection, Secrets, PII)
   - Implement output scanners (Toxicity, PII, FactualConsistency)
   - Add timeout handling
   - Add fail-fast logic

3. `apps/backend/pyproject.toml` (MODIFY)
   - Add `llm-guard>=0.3.0,<1.0` dependency

**Testing:**
- Test input scanning blocks prompt injection
- Test output scanning blocks toxic content
- Test PII detection in both input and output
- Test timeout handling
- Test fail-fast behavior

### Phase 2: Langfuse Integration (3-4 hours)

**Files to Modify:**
1. `apps/backend/src/rwa_agents/observability.py` (MODIFY)
   - Add `LangfuseObservability` class
   - Implement trace creation
   - Implement span tracking for nodes
   - Implement score submission
   - Add callback handler for LangChain/LangGraph

2. `apps/backend/src/rwa_agents/workflow.py` (MODIFY)
   - Attach Langfuse callback handler when enabled
   - Pass config through workflow

3. `apps/backend/pyproject.toml` (MODIFY)
   - Add `langfuse>=2.0,<3.0` dependency

**Testing:**
- Test trace creation when enabled
- Test span tracking for each node
- Test score submission
- Test workflow runs without Langfuse (disabled mode)
- Test callback handler attachment

### Phase 3: Prompt Registry Enhancement (2 hours)

**Files to Modify:**
1. `apps/backend/src/rwa_agents/prompts.py` (MODIFY)
   - Add prompt caching with TTL
   - Implement Langfuse prompt fetching
   - Add timeout handling
   - Add fallback on fetch failure

**Testing:**
- Test Langfuse prompt fetching when enabled
- Test cache hit/miss behavior
- Test TTL expiration
- Test fallback to local prompts on error
- Test timeout handling

### Phase 4: Evaluation Scores (1-2 hours)

**Files to Modify:**
1. `apps/backend/src/rwa_agents/observability.py` (MODIFY)
   - Add `compute_scores()` method
   - Implement Anomaly_Detection logic
   - Extract guardrail metrics to scores

2. `apps/backend/src/rwa_agents/workflow.py` (MODIFY)
   - Call score computation in final_output_guard
   - Submit scores to Langfuse when enabled

**Testing:**
- Test all six required scores are computed
- Test Anomaly_Detection logic
- Test score submission to Langfuse
- Test scores in local metadata when Langfuse disabled

### Phase 5: Testing & Documentation (2-3 hours)

**Files to Create/Modify:**
1. `apps/backend/tests/agents/test_guardrails.py` (NEW)
   - Test LLM Guard input scanning
   - Test LLM Guard output scanning
   - Test final output guard
   - Test blocked content handling

2. `apps/backend/tests/agents/test_observability.py` (NEW)
   - Test Langfuse integration
   - Test score computation
   - Test metadata collection

3. `apps/backend/tests/agents/test_prompts.py` (NEW)
   - Test prompt registry
   - Test caching
   - Test Langfuse fetching

4. `apps/backend/README.md` (MODIFY)
   - Document new environment variables
   - Document configuration options

---

## Configuration Requirements

### Environment Variables

```bash
# LLM Guard Configuration
RWA_LLM_GUARD_ENABLED=true
RWA_LLM_GUARD_FAIL_FAST=true
RWA_LLM_GUARD_BLOCK_ON_PROMPT_INJECTION=true
RWA_LLM_GUARD_BLOCK_ON_PII=true
RWA_LLM_GUARD_BLOCK_ON_SECRETS=true
RWA_LLM_GUARD_INPUT_TIMEOUT_SECONDS=10
RWA_LLM_GUARD_OUTPUT_TIMEOUT_SECONDS=30

# Langfuse Configuration
RWA_LANGFUSE_ENABLED=false
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
RWA_LANGFUSE_PROMPT_LABEL=production
RWA_LANGFUSE_PROMPT_CACHE_TTL_SECONDS=300
RWA_LANGFUSE_PROMPT_FETCH_TIMEOUT_SECONDS=5
```

### Dependencies to Add

```toml
[project]
dependencies = [
    # ... existing dependencies ...
    "llm-guard>=0.3.0,<1.0",
    "langfuse>=2.0,<3.0",
]
```

---

## Risk Assessment

### Technical Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| LLM Guard performance overhead | MEDIUM | Add timeout configuration, make optional |
| Langfuse API unavailability | LOW | Feature flag, local fallback always works |
| Prompt cache invalidation | LOW | TTL configuration, manual cache clear option |
| Breaking changes to existing workflow | LOW | Extensive testing, backward compatibility |

### Implementation Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Incomplete test coverage | MEDIUM | Aim for >80% coverage on new code |
| Configuration complexity | LOW | Clear documentation, sensible defaults |
| Integration with existing code | LOW | Minimal changes to workflow.py |

---

## Acceptance Criteria Validation

### ✅ Already Met

1. ✅ LLM Guard input/output scans implemented (basic version)
2. ✅ Final output guard implemented
3. ✅ Unsafe output blocked from state and response
4. ✅ Prompt registry abstraction implemented
5. ✅ Local fallback prompts implemented
6. ✅ MemorySaver/checkpointing configured
7. ✅ Observability metadata returned in API response

### ⚠️ Requires Enhancement

1. ⚠️ LLM Guard integration - needs actual library integration
2. ⚠️ Langfuse integration - needs actual client integration
3. ⚠️ Prompt registry - needs Langfuse fetching and caching
4. ⚠️ Evaluation scores - needs all six scores computed

### 📋 Testing Requirements

1. ❌ Tests for LLM Guard input scan
2. ❌ Tests for LLM Guard output scan
3. ❌ Tests for final output guard scanning complete payload
4. ❌ Tests for unsafe output blocked from AgentState
5. ❌ Tests for guardrail scan metadata in API response
6. ❌ Tests for prompt registry expected prompt names
7. ❌ Tests for local fallback prompt registry
8. ❌ Tests for Langfuse callback attached when enabled
9. ❌ Tests for no Langfuse calls when disabled
10. ❌ Tests for evaluation scores computed
11. ❌ Tests for scores submitted through Langfuse client
12. ❌ Tests for MemorySaver/checkpointer configured
13. ❌ Tests for stable thread_id
14. ❌ Tests for observability metadata response shape

---

## Affected Files Summary

### Files to Create (3)
1. `apps/backend/src/rwa_agents/config.py` - Configuration classes
2. `apps/backend/tests/agents/test_guardrails.py` - Guardrail tests
3. `apps/backend/tests/agents/test_observability.py` - Observability tests
4. `apps/backend/tests/agents/test_prompts.py` - Prompt registry tests

### Files to Modify (6)
1. `apps/backend/src/rwa_agents/guardrails.py` - Add LLM Guard integration
2. `apps/backend/src/rwa_agents/observability.py` - Add Langfuse client and scores
3. `apps/backend/src/rwa_agents/prompts.py` - Add Langfuse fetching and caching
4. `apps/backend/src/rwa_agents/workflow.py` - Minor config passing changes
5. `apps/backend/pyproject.toml` - Add dependencies
6. `apps/backend/README.md` - Documentation updates

### Files Already Correct (5)
1. `apps/backend/src/rwa_agents/schemas.py` - All schemas defined
2. `apps/backend/src/rwa_agents/state.py` - AgentState correct
3. `apps/backend/src/rwa_agents/checkpointing.py` - Checkpointing complete
4. `apps/backend/src/rwa_agents/api.py` - API endpoint correct
5. `apps/backend/src/rwa_agents/validation.py` - PII validation correct

---

## Execution Plan

### Step 1: Configuration Setup (30 min)
- Create `config.py` with all configuration classes
- Add environment variable loading
- Update `.env.example` with new variables

### Step 2: LLM Guard Integration (2-3 hours)
- Install `llm-guard` package
- Implement scanner initialization
- Add input/output scanning logic
- Add timeout and fail-fast handling
- Test with sample payloads

### Step 3: Langfuse Integration (3-4 hours)
- Install `langfuse` package
- Implement trace creation
- Add span tracking
- Implement callback handler
- Test with mock Langfuse server

### Step 4: Prompt Registry Enhancement (2 hours)
- Add caching mechanism
- Implement Langfuse prompt fetching
- Add timeout handling
- Test cache behavior

### Step 5: Evaluation Scores (1-2 hours)
- Implement score computation
- Add Anomaly_Detection logic
- Extract guardrail metrics
- Test score submission

### Step 6: Testing (2-3 hours)
- Write comprehensive unit tests
- Write integration tests
- Achieve >80% coverage
- Test all acceptance criteria

### Step 7: Documentation (1 hour)
- Update README with configuration
- Document new features
- Add usage examples

**Total Estimated Time:** 12-16 hours

---

## Definition of Done Checklist

- [ ] LLM Guard input/output scans implemented with actual library
- [ ] Final output guard scans complete final_commentary payload
- [ ] Unsafe generated output blocked from state and response
- [ ] Langfuse integration optional and tested
- [ ] Prompt registry abstraction enhanced with Langfuse fetching
- [ ] Local fallback prompts work without Langfuse
- [ ] All six evaluation scores implemented
- [ ] MemorySaver/checkpointing configured (already done)
- [ ] Observability metadata returned in API response (already done)
- [ ] All required tests added and passing
- [ ] ruff passes
- [ ] mypy passes for affected areas
- [ ] pytest passes with >70% coverage
- [ ] Documentation updated

---

## Conclusion

RCT-17 is approximately **80% complete** based on existing implementation. The core architecture is solid with:
- ✅ Guardrail infrastructure in place
- ✅ Checkpointing working
- ✅ Observability framework established
- ✅ Prompt registry abstraction exists

**Remaining work focuses on:**
1. Integrating actual LLM Guard library (vs. simple local checks)
2. Integrating actual Langfuse client (vs. feature flag only)
3. Enhancing prompt registry with real Langfuse fetching and caching
4. Computing all six required evaluation scores

The implementation is well-structured and follows the task requirements closely. The remaining work is primarily integration of external libraries rather than architectural changes.

**Recommendation:** Proceed with implementation following the phased approach outlined above.