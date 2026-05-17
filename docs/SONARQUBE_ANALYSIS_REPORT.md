# SonarQube Analysis Report - RiskTrace Control Tower

**Analysis Date:** 2026-05-17  
**Analyzed Projects:** Backend & Frontend

---

## Executive Summary

The SonarQube scan of the RiskTrace Control Tower repository reveals **108 issues in the backend** and **0 issues in the frontend**. The backend has passed its quality gate (status: OK), while the frontend shows no quality gate status (NONE), indicating it may not have been analyzed yet or lacks configured quality gates.

### Overall Status
- **Backend Quality Gate:** ✅ PASSED (OK)
- **Frontend Quality Gate:** ⚠️ NONE (No analysis or unconfigured)
- **Total Issues:** 108 (all in backend)

---

## Backend Analysis (risktrace-control-tower-backend)

### Quality Gate Status
**Status:** ✅ **PASSED (OK)**

### Issue Summary by Severity

| Severity | Count | Percentage |
|----------|-------|------------|
| **BLOCKER** | 30 | 27.8% |
| **CRITICAL** | 30 | 27.8% |
| **MAJOR** | 47 | 43.5% |
| **MINOR** | 1 | 0.9% |
| **Total** | **108** | **100%** |

### Issue Breakdown by Category

#### 1. **FastAPI Best Practices (60 issues - 55.6%)**

**BLOCKER Issues (30):**
- **S8409 - Redundant response_model (24 issues):** Multiple FastAPI endpoints have redundant `response_model` parameters that duplicate return type annotations
  - Files affected: [`fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py), [`rwa_forecast_service/fastapi_app.py`](apps/backend/src/rwa_forecast_service/fastapi_app.py), [`rwa_projection_service/fastapi_app.py`](apps/backend/src/rwa_projection_service/fastapi_app.py), [`rwa_rats_service/fastapi_app.py`](apps/backend/src/rwa_rats_service/fastapi_app.py), [`rwa_steering/fastapi_app.py`](apps/backend/src/rwa_steering/fastapi_app.py)
  
- **S8410 - Missing Annotated type hints (16 issues):** FastAPI dependency injection should use `Annotated` type hints
  - Files affected: [`fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py) (multiple endpoints)

**MAJOR Issues (14):**
- **S8415 - Undocumented HTTPException (14 issues):** HTTPExceptions with status codes 404, 422, and 503 are not documented in the `responses` parameter
  - Files affected: [`fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py)

#### 2. **Code Duplication - Magic Strings (30 issues - 27.8%)**

**CRITICAL Issues (30):**
- **S1192 - Duplicated string literals:** Multiple string literals are duplicated throughout the codebase and should be extracted to constants
  - Key files:
    - [`seed.py`](apps/backend/src/rwa_dashboard/seed.py): 12 violations (e.g., "briefing.evidence.open" 7x, "vs 2025-12-31" 6x, "12,312" 9x)
    - [`missing_inputs.py`](apps/backend/src/rwa_steering/missing_inputs.py): 14 violations (CSV filenames duplicated 3-4x each)
    - [`input_package.py`](apps/backend/src/rwa_steering/input_package.py): 5 violations
    - [`capital.py`](apps/backend/src/rwa_calculator/rwa_calculator/capital.py): 1 violation ("Basel III final reforms" 8x)
    - [`api.py`](apps/backend/src/rwa_dashboard/api.py): 1 violation ("0.00 pp" 3x)
    - [`service.py`](apps/backend/src/rwa_dashboard/service.py): 3 violations

#### 3. **Cognitive Complexity (6 issues - 5.6%)**

**CRITICAL Issues (6):**
- **S3776 - High cognitive complexity:** Functions exceed the allowed complexity threshold of 15
  - [`fastapi_app.py:95`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py:95) - Complexity: 36 (allowed: 15)
  - [`calculator.py:241`](apps/backend/src/rwa_calculator/rwa_calculator/calculator.py:241) - Complexity: 19 (allowed: 15)
  - [`generate_preprod_rwa_dataset.py:205`](apps/backend/src/rwa_calculator/generate_preprod_rwa_dataset.py:205) - Complexity: 19 (allowed: 15)
  - [`service.py:292`](apps/backend/src/rwa_dashboard/service.py:292) - Complexity: 22 (allowed: 15)
  - [`engine.py:244`](apps/backend/src/rwa_rats_service/engine.py:244) - Complexity: 23 (allowed: 15)
  - [`input_package.py:334`](apps/backend/src/rwa_steering/input_package.py:334) - Complexity: 16 (allowed: 15)
  - [`missing_inputs.py:1155`](apps/backend/src/rwa_steering/missing_inputs.py:1155) - Complexity: 38 (allowed: 15) ⚠️ **Highest**

#### 4. **Other Issues (12 issues - 11.1%)**

**BLOCKER (1):**
- **S5644 - Type error:** [`db.py:21`](apps/backend/src/rwa_common/db.py:21) - `sessionmaker` does not have a `__getitem__` method

**MAJOR (3):**
- **S6735 - Missing validate parameter:** [`data.py:464`](apps/backend/src/rwa_dashboard/data.py:464) - Pandas merge should specify `validate` parameter
- **S1244 - Float equality check:** [`pandera_validation.py:65`](apps/backend/src/rwa_calculator/rwa_calculator/pandera_validation.py:65) - Avoid equality checks with floating point values
- **S1172 - Unused parameter:** [`missing_inputs.py:1382`](apps/backend/src/rwa_steering/missing_inputs.py:1382) - Unused function parameter `entity_class`

**MINOR (1):**
- **S3626 - Redundant return:** [`server.py:74`](apps/backend/src/rwa_calculator/rwa_calculator/server.py:74) - Remove redundant return statement

---

## Frontend Analysis (risktrace-control-tower-frontend)

### Quality Gate Status
**Status:** ⚠️ **NONE** (No analysis or unconfigured quality gate)

### Issue Summary
- **Total Issues:** 0
- **Status:** No issues detected, but quality gate status is NONE, suggesting the project may not have been analyzed or lacks quality gate configuration

---

## Priority Recommendations

### 🔴 Critical Priority (Address Immediately)

1. **Fix FastAPI Blocker Issues (30 issues)**
   - Remove redundant `response_model` parameters (24 issues)
   - Add `Annotated` type hints for dependency injection (16 issues)
   - **Impact:** Code clarity, maintainability, FastAPI best practices
   - **Effort:** Low - Mechanical refactoring

2. **Reduce Cognitive Complexity (6 issues)**
   - Refactor [`missing_inputs.py:1155`](apps/backend/src/rwa_steering/missing_inputs.py:1155) (complexity: 38)
   - Refactor [`fastapi_app.py:95`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py:95) (complexity: 36)
   - **Impact:** Code maintainability, testability, bug risk
   - **Effort:** Medium - Requires careful refactoring

3. **Fix Type Error in db.py (1 BLOCKER)**
   - [`db.py:21`](apps/backend/src/rwa_common/db.py:21) - Fix `sessionmaker` usage
   - **Impact:** Potential runtime errors
   - **Effort:** Low

### 🟡 High Priority (Address Soon)

4. **Extract Magic Strings to Constants (30 issues)**
   - Focus on high-duplication files: [`seed.py`](apps/backend/src/rwa_dashboard/seed.py) (12), [`missing_inputs.py`](apps/backend/src/rwa_steering/missing_inputs.py) (14)
   - **Impact:** Maintainability, refactoring safety
   - **Effort:** Medium - Requires careful constant naming

5. **Document HTTPExceptions (14 issues)**
   - Add `responses` parameter to FastAPI endpoints
   - **Impact:** API documentation completeness
   - **Effort:** Low - Add OpenAPI response documentation

### 🟢 Medium Priority (Plan for Future Sprint)

6. **Fix Pandas Merge Validation (1 issue)**
   - [`data.py:464`](apps/backend/src/rwa_dashboard/data.py:464) - Add `validate` parameter
   - **Impact:** Data quality validation
   - **Effort:** Low

7. **Fix Float Equality Check (1 issue)**
   - [`pandera_validation.py:65`](apps/backend/src/rwa_calculator/rwa_calculator/pandera_validation.py:65)
   - **Impact:** Numerical stability
   - **Effort:** Low

8. **Remove Unused Code (2 issues)**
   - Remove redundant return in [`server.py:74`](apps/backend/src/rwa_calculator/rwa_calculator/server.py:74)
   - Remove unused parameter in [`missing_inputs.py:1382`](apps/backend/src/rwa_steering/missing_inputs.py:1382)
   - **Impact:** Code cleanliness
   - **Effort:** Trivial

### 🔵 Low Priority (Technical Debt)

9. **Configure Frontend Quality Gate**
   - Investigate why frontend has NONE status
   - Configure quality gate thresholds
   - **Impact:** Continuous quality monitoring
   - **Effort:** Low - Configuration task

---

## Files Requiring Most Attention

### Top 10 Files by Issue Count

1. [`fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py) - **45 issues** (BLOCKER: 24, MAJOR: 14, CRITICAL: 7)
2. [`missing_inputs.py`](apps/backend/src/rwa_steering/missing_inputs.py) - **16 issues** (CRITICAL: 15, MAJOR: 1)
3. [`seed.py`](apps/backend/src/rwa_dashboard/seed.py) - **12 issues** (CRITICAL: 12)
4. [`input_package.py`](apps/backend/src/rwa_steering/input_package.py) - **6 issues** (CRITICAL: 6)
5. [`service.py`](apps/backend/src/rwa_dashboard/service.py) - **4 issues** (CRITICAL: 4)
6. [`rwa_forecast_service/fastapi_app.py`](apps/backend/src/rwa_forecast_service/fastapi_app.py) - **2 issues** (BLOCKER: 2)
7. [`rwa_projection_service/fastapi_app.py`](apps/backend/src/rwa_projection_service/fastapi_app.py) - **2 issues** (BLOCKER: 2)
8. [`rwa_rats_service/fastapi_app.py`](apps/backend/src/rwa_rats_service/fastapi_app.py) - **3 issues** (BLOCKER: 2, CRITICAL: 1)
9. [`rwa_steering/fastapi_app.py`](apps/backend/src/rwa_steering/fastapi_app.py) - **2 issues** (BLOCKER: 2)
10. [`calculator.py`](apps/backend/src/rwa_calculator/rwa_calculator/calculator.py) - **1 issue** (CRITICAL: 1)

---

## Estimated Remediation Effort

| Priority | Issues | Estimated Effort | Timeline |
|----------|--------|------------------|----------|
| Critical | 37 | 3-5 days | Sprint 1 |
| High | 44 | 2-3 days | Sprint 1-2 |
| Medium | 4 | 1 day | Sprint 2 |
| Low | 23 | 0.5 days | Sprint 3 |
| **Total** | **108** | **6.5-9.5 days** | **3 sprints** |

---

## Clean Code Attributes Affected

The issues impact the following clean code attributes:

- **INTENTIONAL (Clear):** 54 issues (50%)
- **ADAPTABLE (Focused):** 6 issues (5.6%)
- **ADAPTABLE (Distinct):** 30 issues (27.8%)
- **INTENTIONAL (Complete):** 14 issues (13%)
- **INTENTIONAL (Logical):** 2 issues (1.9%)
- **INTENTIONAL (Clear):** 2 issues (1.9%)

---

## Conclusion

The backend codebase has **passed the quality gate** despite having 108 issues, indicating that the quality gate thresholds may be configured to allow these types of issues. The majority of issues are related to:

1. **FastAPI best practices** (55.6%) - Mostly mechanical fixes
2. **Code duplication** (27.8%) - Requires refactoring to constants
3. **Cognitive complexity** (5.6%) - Requires careful refactoring

The frontend shows **no issues** but has an unconfigured quality gate, which should be addressed to ensure continuous quality monitoring.

**Recommended Action:** Start with critical priority items (FastAPI blockers and cognitive complexity) in the next sprint, as these have the highest impact on code quality and maintainability.