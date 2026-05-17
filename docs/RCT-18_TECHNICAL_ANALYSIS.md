# RCT-18 Technical Analysis: Build React AI Executive Commentary UI

**Epic:** RCT-13 - Deliver guarded, observable, multi-agent RWA executive commentary  
**Story:** RCT-14 - Implement optimized guarded multi-agent RWA executive commentary workflow  
**Task:** RCT-18 - Build React AI Executive Commentary UI connected to guarded RWA commentary backend  
**Status:** In Progress  
**Analysis Date:** 2026-05-17

---

## Executive Summary

RCT-18 requires building a React/TypeScript AI Executive Commentary component that connects to the existing guarded backend workflow. The analysis reveals that **the component already exists and is functional**, but requires enhancements to fully meet the acceptance criteria specified in the task.

### Current State Assessment

✅ **Already Implemented:**
- React component exists at `apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.tsx`
- Backend workflow is complete with LangGraph, guardrails, and observability
- API integration exists via `postRwaExecutiveCommentary()`
- Three-tab interface (Executive Summary, CRO View, CFO View)
- Regenerate functionality
- Loading, error, blocked, and empty states
- Recommended actions checklist
- Observability metadata display

⚠️ **Gaps Identified:**
1. Request builder uses **synthetic/mocked data** from movement drivers instead of real calculated RWA rows
2. Missing PII exclusion validation in request builder
3. No explicit anonymization of asset IDs from dashboard data
4. Backend schema may need extensions for UI-required fields
5. Test coverage needs verification

---

## 1. Requirements Analysis

### 1.1 Core Requirements

| Requirement | Status | Notes |
|------------|--------|-------|
| React/TypeScript component | ✅ Complete | `AiExecutiveCommentaryCard.tsx` exists |
| Three-tab interface | ✅ Complete | Executive Summary, CRO View, CFO View |
| Backend integration | ✅ Complete | Uses `POST /v1/agents/rwa-analysis/run` |
| Regenerate action | ✅ Complete | Implemented with new request_id |
| Loading state | ✅ Complete | Shows "Generating commentary" |
| Empty state | ✅ Complete | Shows "No commentary has been generated yet" |
| Blocked state | ✅ Complete | Shows guardrail block message |
| Error state | ✅ Complete | Shows error message |
| Recommended actions | ✅ Complete | Rendered as checklist |
| Timestamp/source label | ✅ Complete | Displayed in meta section |

### 1.2 Critical Gaps

#### Gap 1: Request Builder Uses Synthetic Data
**Current Implementation:**
```typescript
function buildCommentaryRequest(data: RwaBriefingData): RwaAnalysisRequest {
  const rows = data.movementAttribution.movementDrivers.map((driver, index) => {
    const rwaAmount = Math.max(Math.abs(parseMoney(driver.impact)), 1);
    const exposureAmount = rwaAmount * 2;  // ❌ Synthetic calculation
    const assetId = `ASSET-${String(index + 1).padStart(3, "0")}`;  // ❌ Generated ID
    return {
      input: {
        asset_id: assetId,
        asset_class: driver.driver,
        sector: sectorForDriver(driver.driver),  // ❌ Derived from driver name
        exposure_amount: exposureAmount.toFixed(2),
        risk_weight: "0.50",  // ❌ Hardcoded
        rating: index < 2 ? "BBB" : "BB",  // ❌ Hardcoded
        pd: "0.0200",  // ❌ Hardcoded
        lgd: "0.4500",  // ❌ Hardcoded
        maturity_years: "2.50",  // ❌ Hardcoded
        approach: "dashboard-calculated",
      },
      // ...
    };
  });
}
```

**Required:** Use real calculated RWA rows from dashboard data with actual Basel 3.1 parameters.

#### Gap 2: No PII Exclusion
The request builder does not explicitly exclude PII-like fields. While the current synthetic data doesn't contain PII, real dashboard data might include:
- customer_name
- counterparty_name
- email, phone, address
- account_number, IBAN
- PESEL, SSN, tax_id

#### Gap 3: Missing Real Dashboard Data Source
The `BriefingSnapshot` type doesn't expose calculated RWA rows. Need to identify where real calculated data exists in the backend.

---

## 2. Technical Impact Analysis

### 2.1 Affected Components

#### Frontend Components
```
apps/frontend/src/
├── components/rwa-briefing/
│   └── AiExecutiveCommentaryCard.tsx  ⚠️ Needs request builder fix
├── api/
│   ├── rwaApi.ts                      ✅ Already correct
│   └── types.ts                       ✅ Types match backend
├── hooks/
│   └── useRwaBriefingData.ts          ⚠️ May need real RWA data exposure
└── pages/
    └── RwaIntelligenceBriefingPage.tsx ✅ Already integrated
```

#### Backend Components
```
apps/backend/src/
├── rwa_agents/
│   ├── workflow.py                    ✅ Complete
│   ├── schemas.py                     ✅ Complete
│   ├── guardrails.py                  ✅ Complete
│   ├── observability.py               ✅ Complete
│   └── validation.py                  ⚠️ May need PII validation enhancement
├── rwa_dashboard/
│   └── api.py                         ⚠️ May need calculated rows endpoint
└── rwa_calculator/
    └── (calculator modules)           ℹ️ Source of real RWA data
```

### 2.2 Data Flow Analysis

**Current Flow (Synthetic):**
```
BriefingSnapshot.movementDrivers
  → buildCommentaryRequest() [generates synthetic data]
  → POST /v1/agents/rwa-analysis/run
  → Backend workflow
  → RwaAnalysisResponse
  → AiExecutiveCommentaryCard display
```

**Required Flow (Real Data):**
```
RWA Calculator Output
  → Dashboard API (calculated rows)
  → BriefingSnapshot (with real RWA rows)
  → buildCommentaryRequest() [maps real data, excludes PII]
  → POST /v1/agents/rwa-analysis/run
  → Backend workflow
  → RwaAnalysisResponse
  → AiExecutiveCommentaryCard display
```

### 2.3 Backend Schema Verification

**Backend Response Fields (from workflow.py):**
```python
FinalCommentary(
    status=status,                          # ✅ Used
    consensus_reached=state["consensus_reached"],  # ✅ Used
    loop_count=state["loop_count"],         # ✅ Used
    executive_summary=views.executive_summary,  # ✅ Used
    cro_view=views.cro_view,                # ✅ Used
    cfo_view=views.cfo_view,                # ✅ Used
    data_quality_observations=[...],        # ✅ Used
    risk_observations=[...],                # ✅ Used
    quantitative_validation=state["quantitative_validation"],  # ✅ Used
    recommended_actions=state["recommended_actions"],  # ✅ Used
    validation_flags=state["validation_flags"],  # ✅ Used
    source_agents=sorted({...}),            # ✅ Used
    messages=state["messages"],             # ✅ Used
)
```

**Frontend Expected Fields (from types.ts):**
All fields match! ✅

### 2.4 Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| PII leakage from real dashboard data | 🔴 Critical | Implement explicit PII exclusion in request builder |
| Mocked data in production | 🟡 High | Replace synthetic data with real calculated rows |
| Missing calculated RWA data source | 🟡 High | Expose calculated rows via dashboard API |
| Test coverage gaps | 🟡 Medium | Add tests for request mapping and PII exclusion |
| Performance with large datasets | 🟢 Low | Backend already handles batch processing |

---

## 3. Implementation Plan

### Phase 1: Data Source Integration (Priority: Critical)

**Step 1.1: Expose Real Calculated RWA Rows**
- **File:** `apps/backend/src/rwa_dashboard/api.py`
- **Action:** Add endpoint or extend existing briefing endpoint to include calculated RWA rows
- **Schema:**
```python
class CalculatedRwaRow(BaseModel):
    asset_id: str  # Anonymized
    entity_class: str
    sector: str
    exposure_amount: Decimal
    risk_weight: Decimal
    rating: str | None
    pd: Decimal | None
    lgd: Decimal | None
    maturity_years: Decimal | None
    rwa_amount: Decimal
    approach: str
```

**Step 1.2: Update Frontend Types**
- **File:** `apps/frontend/src/api/types.ts`
- **Action:** Add `calculatedRwaRows` to `BriefingSnapshot`
```typescript
export type BriefingSnapshot = {
  // ... existing fields
  calculatedRwaRows?: CalculatedRwaRow[];
};

export type CalculatedRwaRow = {
  asset_id: string;
  entity_class: string;
  sector: string;
  exposure_amount: string;
  risk_weight: string;
  rating?: string;
  pd?: string;
  lgd?: string;
  maturity_years?: string;
  rwa_amount: string;
  approach: string;
};
```

### Phase 2: Request Builder Refactoring (Priority: Critical)

**Step 2.1: Implement Real Data Mapping**
- **File:** `apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.tsx`
- **Action:** Replace `buildCommentaryRequest()` with real data mapping

```typescript
function buildCommentaryRequest(data: RwaBriefingData): RwaAnalysisRequest {
  // Use real calculated rows if available, fallback to synthetic for backward compatibility
  const calculatedRows = data.calculatedRwaRows ?? [];
  
  if (calculatedRows.length === 0) {
    // Fallback to current synthetic approach for backward compatibility
    return buildSyntheticRequest(data);
  }

  // Map real calculated rows, excluding PII-like fields
  const rows = calculatedRows.map((row) => ({
    input: {
      asset_id: anonymizeAssetId(row.asset_id),  // Ensure anonymization
      asset_class: row.entity_class,
      sector: row.sector,
      exposure_amount: row.exposure_amount,
      risk_weight: row.risk_weight,
      rating: row.rating ?? undefined,
      pd: row.pd ?? undefined,
      lgd: row.lgd ?? undefined,
      maturity_years: row.maturity_years ?? undefined,
      approach: row.approach,
    },
    output: {
      asset_id: anonymizeAssetId(row.asset_id),
      rwa_amount: row.rwa_amount,
      exposure_amount: row.exposure_amount,
      risk_weight: row.risk_weight,
      approach: row.approach,
    },
  }));

  return {
    request_id: `briefing-${new Date(data.generatedAt).getTime() || Date.now()}`,
    loop_limit: 2,
    materiality_threshold: "0.05",
    rwa_input_data: rows.map((row) => row.input),
    rwa_output_results: rows.map((row) => row.output),
  };
}

function anonymizeAssetId(assetId: string): string {
  // Ensure asset ID follows anonymized format
  const normalized = assetId.trim().toUpperCase();
  const allowedPrefixes = ["ASSET-", "EXPOSURE-", "PORTFOLIO-", "RWA-"];
  
  if (allowedPrefixes.some(prefix => normalized.startsWith(prefix))) {
    return normalized;
  }
  
  // Generate anonymized ID if not already anonymized
  return `ASSET-${hashString(assetId).substring(0, 12)}`;
}

function hashString(str: string): string {
  // Simple hash for anonymization (use crypto in production)
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36).toUpperCase();
}
```

**Step 2.2: Add PII Exclusion Validation**
```typescript
const PII_FIELD_PATTERNS = [
  /customer.*name/i,
  /counterparty.*name/i,
  /client.*name/i,
  /email/i,
  /phone/i,
  /address/i,
  /account.*number/i,
  /iban/i,
  /pesel/i,
  /ssn/i,
  /tax.*id/i,
];

function validateNoPii(data: Record<string, unknown>): void {
  const keys = Object.keys(data);
  const piiFields = keys.filter(key => 
    PII_FIELD_PATTERNS.some(pattern => pattern.test(key))
  );
  
  if (piiFields.length > 0) {
    throw new Error(`PII-like fields detected: ${piiFields.join(", ")}`);
  }
}
```

### Phase 3: Testing (Priority: High)

**Step 3.1: Backend Tests**
- **File:** `apps/backend/tests/agents/test_request_validation.py`
- **Tests:**
  - ✅ Backend response contains UI-required fields
  - ✅ PII-like fields are rejected before graph execution
  - ✅ Anonymized asset IDs are accepted
  - ✅ Guardrails block unsafe content

**Step 3.2: Frontend Tests**
- **File:** `apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.test.tsx`
- **Tests:**
  - React frontend renders AI Executive Commentary title
  - React frontend exposes tabs: Executive Summary, CRO View, CFO View
  - Selected tab renders only its matching structured field
  - Recommended actions render as checklist items
  - Generated timestamp and source label render
  - Regenerate button triggers backend workflow
  - Loading state displays correctly
  - Empty/unavailable state displays correctly
  - Blocked state displays correctly
  - Error state displays correctly
  - No mocked commentary rendered in production
  - React request builder uses calculated RWA rows when available
  - React request builder anonymizes IDs
  - React request builder excludes PII-like fields

**Step 3.3: E2E Tests**
- **File:** `apps/frontend/tests/e2e/ai-commentary.spec.ts`
- **Tests:**
  - Full workflow from dashboard to commentary generation
  - Regenerate functionality
  - Tab switching
  - State transitions

### Phase 4: Documentation (Priority: Medium)

**Step 4.1: Update API Documentation**
- Document calculated RWA rows endpoint
- Document request/response contracts
- Document PII exclusion rules

**Step 4.2: Update Component Documentation**
- Add JSDoc comments to `AiExecutiveCommentaryCard`
- Document request builder logic
- Document anonymization strategy

---

## 4. Proposed Actions

### Immediate Actions (Sprint 1)

1. **Verify Real Data Source**
   - [ ] Identify where calculated RWA rows exist in backend
   - [ ] Confirm data includes all required fields
   - [ ] Verify anonymization is already applied

2. **Extend Dashboard API**
   - [ ] Add `calculatedRwaRows` to briefing endpoint response
   - [ ] Ensure proper anonymization at source
   - [ ] Add validation for PII exclusion

3. **Refactor Request Builder**
   - [ ] Implement real data mapping
   - [ ] Add PII exclusion validation
   - [ ] Add anonymization helper
   - [ ] Keep synthetic fallback for backward compatibility

4. **Add Tests**
   - [ ] Backend: PII exclusion validation
   - [ ] Frontend: Request builder with real data
   - [ ] Frontend: PII field detection
   - [ ] E2E: Full commentary generation flow

### Follow-up Actions (Sprint 2)

5. **Performance Optimization**
   - [ ] Implement request caching
   - [ ] Add pagination for large datasets
   - [ ] Optimize re-render behavior

6. **Enhanced Error Handling**
   - [ ] Add retry logic for transient failures
   - [ ] Improve error messages
   - [ ] Add error recovery suggestions

7. **Observability Enhancement**
   - [ ] Add frontend telemetry
   - [ ] Track commentary generation metrics
   - [ ] Monitor PII detection events

---

## 5. Affected Files and Services

### Frontend Files (Modification Required)

```
apps/frontend/src/
├── components/rwa-briefing/
│   └── AiExecutiveCommentaryCard.tsx          ⚠️ MODIFY: Request builder
├── api/
│   └── types.ts                               ⚠️ MODIFY: Add CalculatedRwaRow type
└── hooks/
    └── useRwaBriefingData.ts                  ℹ️ REVIEW: May need update
```

### Backend Files (Modification Required)

```
apps/backend/src/
├── rwa_dashboard/
│   └── api.py                                 ⚠️ MODIFY: Add calculated rows to response
└── rwa_agents/
    └── validation.py                          ℹ️ REVIEW: PII validation already exists
```

### Test Files (Creation Required)

```
apps/frontend/src/components/rwa-briefing/
└── AiExecutiveCommentaryCard.test.tsx         ➕ CREATE

apps/frontend/tests/e2e/
└── ai-commentary.spec.ts                      ➕ CREATE

apps/backend/tests/agents/
└── test_request_validation.py                 ℹ️ REVIEW: May already exist
```

---

## 6. Execution Plan

### Week 1: Data Integration
- **Day 1-2:** Identify and expose calculated RWA rows in backend
- **Day 3:** Update frontend types and API client
- **Day 4-5:** Implement real data mapping in request builder

### Week 2: Validation and Testing
- **Day 1-2:** Implement PII exclusion validation
- **Day 3:** Add anonymization helpers
- **Day 4-5:** Write and execute tests

### Week 3: Integration and Verification
- **Day 1-2:** End-to-end testing
- **Day 3:** Performance testing
- **Day 4:** Documentation
- **Day 5:** Code review and refinement

---

## 7. Acceptance Criteria Verification

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Display generated executive commentary | ✅ Complete | Component renders `final_commentary.executive_summary` |
| Switch commentary views | ✅ Complete | Three tabs implemented with state management |
| Regenerate commentary | ✅ Complete | Button triggers new request with unique ID |
| Use real calculated data | ⚠️ Partial | Needs real data source integration |
| Prevent PII from frontend request | ⚠️ Partial | Needs explicit validation |
| Handle unavailable commentary | ✅ Complete | Empty state implemented |
| Handle blocked commentary | ✅ Complete | Blocked state with guardrail message |
| Handle generation error | ✅ Complete | Error state with message |
| No mocked commentary | ⚠️ Partial | Currently uses synthetic data |
| Tests pass | ⚠️ Pending | Tests need to be added |

---

## 8. Risks and Mitigations

### Risk 1: Real Data Source Not Available
**Impact:** High  
**Probability:** Medium  
**Mitigation:** Keep synthetic fallback, implement progressive enhancement

### Risk 2: PII in Production Data
**Impact:** Critical  
**Probability:** Low  
**Mitigation:** Implement strict validation, add monitoring, fail-safe to block

### Risk 3: Performance Degradation
**Impact:** Medium  
**Probability:** Low  
**Mitigation:** Implement caching, pagination, lazy loading

### Risk 4: Breaking Changes
**Impact:** Medium  
**Probability:** Low  
**Mitigation:** Maintain backward compatibility, feature flags, gradual rollout

---

## 9. Dependencies

### Internal Dependencies
- ✅ Backend workflow (RCT-15, RCT-16, RCT-17) - **Complete**
- ⚠️ Dashboard calculated rows API - **Needs verification**
- ✅ Frontend briefing page - **Complete**

### External Dependencies
- ✅ LangGraph - **Available**
- ✅ React/TypeScript - **Available**
- ✅ Vite build system - **Available**

---

## 10. Success Metrics

### Functional Metrics
- [ ] 100% of acceptance criteria met
- [ ] All tests passing (unit, integration, E2E)
- [ ] Zero PII leakage incidents
- [ ] Real data used in 100% of requests (when available)

### Performance Metrics
- [ ] Commentary generation < 10 seconds (p95)
- [ ] UI response time < 100ms
- [ ] Zero blocking UI operations

### Quality Metrics
- [ ] Code coverage > 80%
- [ ] Zero critical security findings
- [ ] Zero accessibility violations

---

## 11. Conclusion

RCT-18 is **80% complete** with the React component fully functional but requiring critical enhancements:

### ✅ Strengths
- Complete UI implementation with all required states
- Backend integration working
- Guardrails and observability in place
- Good user experience

### ⚠️ Critical Gaps
- Request builder uses synthetic data instead of real calculated RWA rows
- Missing explicit PII exclusion validation
- Test coverage needs to be added

### 🎯 Recommended Approach
1. **Verify** real data source availability in backend
2. **Extend** dashboard API to expose calculated rows
3. **Refactor** request builder to use real data
4. **Add** PII exclusion validation
5. **Test** thoroughly with real data scenarios
6. **Deploy** with feature flag for gradual rollout

**Estimated Effort:** 2-3 weeks (1 developer)  
**Risk Level:** Medium (manageable with proper testing)  
**Business Value:** High (enables production-ready AI commentary)

---

## Appendix A: Related Documentation

- [RCT-15 Technical Analysis](./RCT-15_TECHNICAL_ANALYSIS.md) - Architecture and contracts
- [RCT-16 Technical Analysis](./RCT-16_TECHNICAL_ANALYSIS.md) - LangGraph runtime
- [RCT-17 Implementation Summary](./RCT-17_IMPLEMENTATION_SUMMARY.md) - Guardrails and observability
- [Agent Architecture](./agents/architecture.md)
- [Agent Contracts](./agents/contracts.md)
- [Agent Validation](./agents/validation.md)

---

**Analysis Completed:** 2026-05-17  
**Next Review:** After Phase 1 completion  
**Approval Required:** Product Owner, Tech Lead