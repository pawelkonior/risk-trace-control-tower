# RCT-40 Technical Analysis: Finalize Enterprise IBM Watsonx LLM Runtime

**Task**: RCT-40
**Story**: RCT-14 - Implement optimized guarded multi-agent RWA executive commentary workflow
**Epic**: RCT-13 - Deliver guarded, observable, multi-agent RWA executive commentary
**Analysis Date**: 2026-05-17
**Status**: Superseded by implementation - see `docs/RCT-40_WATSONX_FINALIZATION.md`

---

## Executive Summary

> Implementation update: the original gap analysis below was written before the RCT-40
> implementation was completed. The repository now includes the watsonx client, provider
> selection, guarded supervisor synthesis, observability counters, environment placeholders, and
> targeted tests. Use `docs/RCT-40_WATSONX_FINALIZATION.md` as the current finalization record.

RCT-40 describes finalizing an IBM Watsonx LLM integration for RWA executive commentary that was supposedly implemented in commit `f69ad63`. However, **the watsonx integration does not currently exist in the codebase**. This task requires implementing the complete watsonx integration from scratch, not just finalizing existing work.

### Critical Finding

The task description references:
- Commit `f69ad63 Add optional watsonx commentary provider` - **This commit/code does not exist**
- Files like `watsonx.py` - **Not present in codebase**
- Runtime validation evidence - **Cannot be validated without implementation**

### Current State

- ✅ Deterministic workflow fully implemented
- ✅ LLM Guard guardrails operational
- ✅ Langfuse observability integrated
- ✅ Prompt registry with fallback
- ❌ **Watsonx integration: NOT IMPLEMENTED**
- ❌ **LLM provider selection: NOT IMPLEMENTED**
- ❌ **Watsonx configuration in config.py: NOT IMPLEMENTED**

---

## 1. Requirements Analysis

### 1.1 Business Requirements

**Primary Objective**: Enable optional IBM Watsonx LLM-backed executive commentary synthesis while maintaining:
- Deterministic RWA validation as source of truth
- PII-safe, guarded, observable workflow
- Fallback to deterministic commentary on LLM failure
- No LLM-based RWA formula calculations

**Key Constraints**:
- LLM must be opt-in (default: deterministic)
- No secrets in repository
- Summarized context only (no raw portfolio data to LLM)
- Enterprise IBM Cloud watsonx.ai integration
- Guardrail scanning at all LLM boundaries

### 1.2 Technical Requirements

From RCT-40 acceptance criteria:

1. **Configuration**: `RWA_AGENTS_LLM_PROVIDER`, `WATSONX_PROJECT_ID`, `WATSONX_APIKEY`, `WATSONX_URL`, `RWA_AGENTS_WATSONX_MODEL_ID`
2. **Runtime**: IBM IAM token exchange, `/ml/v1/text/chat` API calls, token tracking, guardrail scans
3. **Fallback**: Graceful degradation to deterministic commentary
4. **Observability**: `llm_call_count`, `total_token_count`, `guardrail_block_count`

---

## 2. Gap Analysis

### 2.1 Missing Components

| Component | Status | Priority | Effort |
|-----------|--------|----------|--------|
| `watsonx.py` module | ❌ Not implemented | **CRITICAL** | High |
| `WatsonxConfig` class | ❌ Not implemented | **CRITICAL** | Medium |
| LLM provider selection | ❌ Not implemented | **CRITICAL** | Low |
| Watsonx supervisor synthesis | ❌ Not implemented | **CRITICAL** | High |
| LLM observability counters | ❌ Not implemented | **HIGH** | Low |
| `.env.example` watsonx docs | ❌ Not implemented | **MEDIUM** | Low |
| Watsonx integration tests | ❌ Not implemented | **HIGH** | Medium |

### 2.2 Files to Create

1. `apps/backend/src/rwa_agents/watsonx.py` - IBM watsonx client
2. `apps/backend/tests/agents/test_watsonx.py` - Unit tests

### 2.3 Files to Modify

1. `apps/backend/src/rwa_agents/config.py` - Add watsonx config
2. `apps/backend/src/rwa_agents/workflow.py` - Add LLM synthesis path
3. `apps/backend/src/rwa_agents/schemas.py` - Add LLM counters
4. `apps/backend/src/rwa_agents/observability.py` - Track LLM calls
5. `apps/backend/.env.example` - Document watsonx settings
6. `apps/docker-compose.yml` - Pass watsonx env vars
7. `apps/backend/tests/agents/test_workflow.py` - Add watsonx tests

---

## 3. Technical Impact Analysis

### 3.1 Affected Services

- ✅ `rwa_agents` - Primary implementation target
- ⚠️ `rwa_calculator` - API mounting (already done)
- ✅ `rwa_dashboard` - No changes needed
- ✅ Frontend - No changes needed (API contract unchanged)

### 3.2 API Contract Impact

**Backward Compatibility**: ✅ Fully compatible (additive only)

Enhanced observability metadata:
```typescript
{
  observability: {
    llm_call_count: number;        // NEW
    total_token_count: number;     // NEW
    guardrail_block_count: number; // EXISTING
    // ...
  }
}
```

### 3.3 Performance Impact

- **Deterministic Mode**: ~100-500ms (unchanged)
- **Watsonx Mode**: +2-5 seconds (IBM IAM + watsonx call)
- **Fallback**: Automatic to deterministic on failure

### 3.4 Security Impact

- ✅ No secrets in repository
- ✅ PII rejection before graph execution
- ✅ Summarized context only to LLM
- ✅ Guardrail scanning at all boundaries

---

## 4. Implementation Plan

### Phase 1: Core Watsonx Integration (4-6 hours)

**Create `watsonx.py`**:
- `WatsonxClient` class
- IBM IAM token exchange
- `/ml/v1/text/chat` API calls
- Token usage extraction
- Error handling

**Update `config.py`**:
- Add `WatsonxConfig` class
- Add `RWA_AGENTS_LLM_PROVIDER` setting
- Support unprefixed `WATSONX_*` aliases

### Phase 2: Workflow Integration (3-4 hours)

**Update `workflow.py`**:
- Modify `supervisor_agent()` to check provider
- Build summarized prompt context
- Call watsonx when enabled
- Parse structured JSON response
- Fallback to deterministic on error
- Add guardrail scans (input/output)

### Phase 3: Observability Enhancement (2-3 hours)

**Update `schemas.py`**:
- Add `llm_call_count` and `total_token_count` to `ObservabilityMetadata`

**Update `observability.py`**:
- Add `llm()` method for tracking calls
- Token count accumulation
- Langfuse LLM span creation

### Phase 4: Configuration & Documentation (2 hours)

- Update `.env.example` with watsonx settings
- Update `docker-compose.yml` to pass env vars
- Create operational runbook

### Phase 5: Testing & Validation (4-5 hours)

- Unit tests for watsonx client
- Integration tests for workflow
- Manual smoke testing with IBM Cloud
- Validation against RCT-40 acceptance criteria

**Total Estimated Effort**: 15-20 hours (2-3 days)

---

## 5. Risk Assessment

### 5.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| IBM model availability varies by region | **HIGH** | Medium | Document validated model/region, make configurable |
| IAM token exchange failures | Medium | High | Implement retry logic, clear error messages |
| LLM response parsing failures | Medium | High | Strict JSON schema, fallback to deterministic |
| Secrets accidentally committed | Low | **CRITICAL** | Pre-commit hooks, `.gitignore` enforcement |

### 5.2 Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Increased latency in production | **HIGH** | Medium | Timeout configuration, async architecture (future) |
| IBM Cloud service outages | Medium | Medium | Automatic fallback to deterministic |
| Configuration errors in deployment | Medium | High | Validation on startup, clear error messages |

---

## 6. Proposed Execution Plan

### 6.1 Pre-Implementation

1. **Verify IBM Cloud Access**:
   - Confirm watsonx.ai project access
   - Validate API key permissions
   - Test regional endpoint connectivity
   - Verify model `meta-llama/llama-3-3-70b-instruct` availability in `eu-de`

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/RCT-40-watsonx-integration
   ```

3. **Approve This Analysis**: Stakeholder sign-off required

### 6.2 Implementation Timeline

**Day 1**:
- Phase 1: Core watsonx integration (4-6 hours)
- Phase 2: Workflow integration (3-4 hours)

**Day 2**:
- Phase 3: Observability enhancement (2-3 hours)
- Phase 4: Configuration & docs (2 hours)
- Phase 5: Testing & validation (4-5 hours)

**Day 3**:
- Code review
- Manual smoke testing
- Documentation finalization
- PR creation

### 6.3 Rollout Strategy

**Phased rollout with feature flag**:

1. **Week 1**: Deploy with deterministic default, watsonx opt-in only
2. **Week 2**: Enable watsonx for 10% of requests, monitor
3. **Week 3**: Increase to 50% of requests
4. **Week 4**: Full rollout or keep as opt-in based on performance/cost

**Rollback Plan**: Set `RWA_AGENTS_LLM_PROVIDER=deterministic` (instant rollback)

---

## 7. Success Criteria

### 7.1 Functional Requirements

- ✅ Deterministic mode works without watsonx credentials
- ✅ Watsonx mode generates LLM-backed commentary when enabled
- ✅ Guardrails scan all LLM boundaries
- ✅ Fallback to deterministic on LLM failure
- ✅ No secrets committed to repository
- ✅ API contract backward compatible

### 7.2 Acceptance Criteria (from RCT-40)

All 9 scenarios from RCT-40 must pass:

1. ✅ Deterministic mode remains default
2. ✅ Watsonx config loaded from `.env`
3. ✅ Direct watsonx client call succeeds
4. ✅ Guarded LLM synthesis through API
5. ✅ LLM cannot perform RWA calculations
6. ✅ Unsafe LLM boundary blocked
7. ✅ Watsonx failure falls back safely
8. ✅ Main FastAPI app exposes agents endpoint
9. ✅ All validation plan tests pass

---

## 8. Affected Files Summary

### New Files (2)
- `apps/backend/src/rwa_agents/watsonx.py`
- `apps/backend/tests/agents/test_watsonx.py`

### Modified Files (7)
- `apps/backend/src/rwa_agents/config.py`
- `apps/backend/src/rwa_agents/workflow.py`
- `apps/backend/src/rwa_agents/schemas.py`
- `apps/backend/src/rwa_agents/observability.py`
- `apps/backend/.env.example`
- `apps/docker-compose.yml`
- `apps/backend/tests/agents/test_workflow.py`

### No Changes Required
- Frontend (API contract unchanged)
- Database (stateless LLM calls)
- Other backend services

---

## 9. Open Questions

1. **IBM Cloud Configuration**:
   - Q: Is the watsonx project already associated with a WML runtime instance?
   - A: **Needs verification** - Required for model calls to succeed

2. **Model Selection**:
   - Q: Is `meta-llama/llama-3-3-70b-instruct` available in `eu-de` region?
   - A: **Needs verification** - Model availability is region-specific

3. **Cost Management**:
   - Q: What is the expected token usage budget?
   - A: **Needs clarification** - For monitoring and alerting

---

## 10. Conclusion

### Summary

RCT-40 requires **implementing a complete IBM Watsonx LLM integration from scratch**, not finalizing existing work. The task description incorrectly references commit `f69ad63` which does not exist.

**Current State**: Deterministic workflow fully operational, ready for LLM enhancement
**Required Work**: ~15-20 hours of focused implementation
**Risk Level**: **Medium** (well-defined requirements, existing guardrails operational)
**Recommendation**: **Proceed with implementation** after stakeholder approval

### Next Steps

1. ✅ **Approve this technical analysis**
2. ✅ **Verify IBM Cloud access and model availability**
3. ✅ **Create feature branch `feature/RCT-40-watsonx-integration`**
4. ⏸️ **Implement Phases 1-5** (awaiting approval)
5. ⏸️ **Submit PR for review** (awaiting implementation)
6. ⏸️ **Deploy to staging** (awaiting PR merge)
7. ⏸️ **Phased production rollout** (awaiting staging validation)

### Approval Required

**Stakeholders**:
- Product Owner: Approve business requirements
- Technical Lead: Approve architecture and implementation plan
- Security Team: Approve secrets management approach
- DevOps: Approve deployment strategy

**Sign-off**: ⏸️ Awaiting approval to proceed

---

**Document Version**: 1.0
**Last Updated**: 2026-05-17T12:00:00+02:00
**Author**: Bob (AI Assistant)
**Reviewers**: Pending
