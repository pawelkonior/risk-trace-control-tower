# SonarQube BLOCKER Issues - Fix Plan

**Date:** 2026-05-17  
**Total BLOCKER Issues:** 30  
**Estimated Effort:** 2-3 hours  
**Priority:** CRITICAL

---

## Overview

This document provides a detailed plan to fix all 30 BLOCKER issues identified in the SonarQube analysis. The issues fall into three categories:

1. **S8409 - Redundant response_model (24 issues)** - Remove redundant `response_model` parameters
2. **S8410 - Missing Annotated types (16 issues)** - Add `Annotated` type hints for FastAPI dependencies
3. **S5644 - Type error (1 issue)** - Fix `sessionmaker` type annotation

Note: Some endpoints have both S8409 and S8410 issues, so the total unique locations is less than 30.

---

## Issue Category 1: S8409 - Redundant response_model (24 issues)

### Problem
FastAPI endpoints have redundant `response_model` parameters that duplicate the return type annotation. Modern FastAPI (0.100+) automatically infers the response model from the return type annotation.

### Solution Pattern
**Before:**
```python
@app.get("/endpoint", response_model=ResponseType)
def endpoint() -> ResponseType:
    return ResponseType(...)
```

**After:**
```python
@app.get("/endpoint")
def endpoint() -> ResponseType:
    return ResponseType(...)
```

### Files to Fix

#### 1. [`apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py) (18 issues)

**Lines to fix:**
- Line 140-141: `/v1/health` and `/health` endpoints
- Line 196: `/v1/calculator/rules` endpoint
- Line 208: `/v1/calculator/rules/{rule_id}` endpoint
- Line 233: `/v1/calculator/rules/{rule_id}/overlays` endpoint
- Line 248: `/v1/calculator/rules/{rule_id}/overlays/{overlay_id}` endpoint
- Line 262: `/v1/calculator/jurisdictions` endpoint
- Line 278: `/v1/calculator/jurisdictions/{jurisdiction_id}` endpoint
- Line 294: `/v1/calculator/jurisdictions/{jurisdiction_id}/overlays` endpoint
- Line 309: `/v1/calculator/jurisdictions/{jurisdiction_id}/overlays/{overlay_id}` endpoint
- Line 321: `/v1/calculator/asset-classes` endpoint
- Line 332-333: `/v1/calculator/calculate` and `/calculator/calculate` endpoints
- Line 366-367: `/v1/dashboard/summary` and `/dashboard/summary` endpoints
- Line 406: `/v1/dashboard/notifications` endpoint
- Line 415: `/v1/dashboard/ui-actions` endpoint
- Line 422: `/v1/dashboard/briefing` endpoint
- Line 432: `/v1/dashboard/lineage` endpoint
- Line 441: `/v1/dashboard/lineage/transformations` endpoint

**Fix approach:**
- Remove `response_model=HealthResponse` from lines 140-141
- Remove `response_model=RuleListResponse` from line 196
- Remove `response_model=RuleDetailResponse` from line 208
- Remove `response_model=OverlayListResponse` from line 233
- Remove `response_model=OverlayDetailResponse` from line 248
- Remove `response_model=JurisdictionListResponse` from line 262
- Remove `response_model=JurisdictionDetailResponse` from line 278
- Remove `response_model=OverlayListResponse` from line 294
- Remove `response_model=OverlayDetailResponse` from line 309
- Remove `response_model=AssetClassListResponse` from line 321
- Remove `response_model=CalculationResponse` from lines 332-333
- Remove `response_model=DashboardSummaryResponse` from lines 366-367
- Remove `response_model=NotificationsResponse` from line 406
- Remove `response_model=UiActionsResponse` from line 415
- Remove `response_model=BriefingResponse` from line 422
- Remove `response_model=LineageResponse` from line 432
- Remove `response_model=TransformationsResponse` from line 441

#### 2. [`apps/backend/src/rwa_forecast_service/fastapi_app.py`](apps/backend/src/rwa_forecast_service/fastapi_app.py) (2 issues)

**Lines to fix:**
- Line 54-55: `/v1/forecasts/run` and `/forecasts/run` endpoints

**Fix approach:**
- Remove `response_model=ForecastResponse` from lines 54-55

#### 3. [`apps/backend/src/rwa_projection_service/fastapi_app.py`](apps/backend/src/rwa_projection_service/fastapi_app.py) (2 issues)

**Lines to fix:**
- Line 49-50: `/v1/projections/calculate` and `/projections/calculate` endpoints

**Fix approach:**
- Remove `response_model=ProjectionResponse` from lines 49-50

#### 4. [`apps/backend/src/rwa_rats_service/fastapi_app.py`](apps/backend/src/rwa_rats_service/fastapi_app.py) (2 issues)

**Lines to fix:**
- Line 54-55: `/v1/rats/optimize` and `/rats/optimize` endpoints

**Fix approach:**
- Remove `response_model=RATSResponse` from lines 54-55

#### 5. [`apps/backend/src/rwa_steering/fastapi_app.py`](apps/backend/src/rwa_steering/fastapi_app.py) (2 issues)

**Lines to fix:**
- Line 60-61: `/v1/steering/run` and `/steering/run` endpoints

**Fix approach:**
- Remove `response_model=SteeringResponse` from lines 60-61

---

## Issue Category 2: S8410 - Missing Annotated Types (16 issues)

### Problem
FastAPI dependency injection should use `Annotated` type hints for better type safety and IDE support. The current code uses `Depends()` as a default parameter value, which is deprecated in modern FastAPI.

### Solution Pattern
**Before:**
```python
from fastapi import Depends

def endpoint(session: Session = Depends(get_db_session)):
    ...
```

**After:**
```python
from typing import Annotated
from fastapi import Depends

def endpoint(session: Annotated[Session, Depends(get_db_session)]):
    ...
```

### Files to Fix

#### 1. [`apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py) (16 issues)

**Import changes needed:**
```python
from typing import Annotated  # Add this import at the top
```

**Lines to fix:**
- Line 169: `get_rules()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 192: `get_rule()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 198: `get_rule()` - `rule_id: str` parameter
- Line 214: `get_rule_overlays()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 216: `get_rule_overlays()` - `rule_id: str` parameter
- Line 238: `get_rule_overlay()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 252: `get_jurisdictions()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 268: `get_jurisdiction()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 284: `get_jurisdiction_overlays()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 299: `get_jurisdiction_overlay()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 313: `get_asset_classes()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 324: `calculate()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 336: `calculate_batch()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 369: `get_dashboard_summary()` - `service: RisktraceUiService = Depends(get_risktrace_service)`
- Line 370-372: `get_dashboard_summary()` - Multiple path parameters
- Line 376: `get_notifications()` - `service: RisktraceUiService = Depends(get_risktrace_service)`

**Fix approach:**
Replace all occurrences of:
```python
service: RisktraceUiService = Depends(get_risktrace_service)
```
with:
```python
service: Annotated[RisktraceUiService, Depends(get_risktrace_service)]
```

And for path parameters like `rule_id: str`, if they're used with `Path()`, convert to:
```python
rule_id: Annotated[str, Path(...)]
```

---

## Issue Category 3: S5644 - Type Error (1 issue)

### Problem
Line 21 in [`apps/backend/src/rwa_common/db.py`](apps/backend/src/rwa_common/db.py:21) uses incorrect type annotation syntax for `sessionmaker`.

**Current code:**
```python
SessionFactory = sessionmaker[Session]
```

### Solution
The issue is that `sessionmaker` doesn't support subscript notation (`[Session]`). The correct approach is to use type alias or proper typing.

**Option 1 - Type Alias (Recommended):**
```python
from typing import TypeAlias

SessionFactory: TypeAlias = sessionmaker
```

**Option 2 - Callable Type:**
```python
from collections.abc import Callable

SessionFactory: Callable[..., Session] = sessionmaker
```

**Option 3 - Remove type annotation:**
```python
SessionFactory = sessionmaker
```

**Recommended fix:** Use Option 1 (Type Alias) as it provides the best type safety while being correct.

---

## Implementation Plan

### Phase 1: Fix S8409 Issues (Redundant response_model) - 1 hour

**Order of execution:**
1. Fix [`rwa_calculator/fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py) (18 issues) - 30 min
2. Fix [`rwa_forecast_service/fastapi_app.py`](apps/backend/src/rwa_forecast_service/fastapi_app.py) (2 issues) - 5 min
3. Fix [`rwa_projection_service/fastapi_app.py`](apps/backend/src/rwa_projection_service/fastapi_app.py) (2 issues) - 5 min
4. Fix [`rwa_rats_service/fastapi_app.py`](apps/backend/src/rwa_rats_service/fastapi_app.py) (2 issues) - 5 min
5. Fix [`rwa_steering/fastapi_app.py`](apps/backend/src/rwa_steering/fastapi_app.py) (2 issues) - 5 min
6. Run tests to verify no regressions - 10 min

### Phase 2: Fix S8410 Issues (Missing Annotated types) - 1 hour

**Order of execution:**
1. Add `from typing import Annotated` import to [`rwa_calculator/fastapi_app.py`](apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py)
2. Convert all 16 dependency injection parameters to use `Annotated` - 40 min
3. Run tests to verify no regressions - 10 min
4. Verify type checking with mypy - 10 min

### Phase 3: Fix S5644 Issue (Type error) - 15 minutes

**Order of execution:**
1. Fix [`db.py:21`](apps/backend/src/rwa_common/db.py:21) using Type Alias approach - 5 min
2. Run tests to verify no regressions - 5 min
3. Verify type checking with mypy - 5 min

### Phase 4: Validation - 30 minutes

**Validation steps:**
1. Run full test suite: `uv run pytest` - 10 min
2. Run type checking: `uv run mypy` - 5 min
3. Run linting: `uv run ruff check .` - 5 min
4. Re-run SonarQube scan to verify all BLOCKER issues are resolved - 10 min

---

## Testing Strategy

### Unit Tests
All existing unit tests should pass without modification since we're only changing type annotations and removing redundant parameters, not changing behavior.

### Integration Tests
Run the full test suite to ensure:
- FastAPI endpoints still return correct response models
- Dependency injection still works correctly
- Database session management still functions

### Manual Testing
1. Start the backend services
2. Test key endpoints:
   - Health check: `GET /health`
   - Calculator: `POST /v1/calculator/calculate`
   - Dashboard: `GET /v1/dashboard/summary`
3. Verify OpenAPI docs still generate correctly: `http://localhost:8000/docs`

---

## Risk Assessment

### Low Risk Changes
- **S8409 fixes (response_model removal):** Very low risk. FastAPI automatically infers response models from return type annotations since version 0.100+. All endpoints already have proper return type annotations.
- **S5644 fix (type alias):** Very low risk. This is a type annotation fix that doesn't affect runtime behavior.

### Medium Risk Changes
- **S8410 fixes (Annotated types):** Low-medium risk. This changes the dependency injection syntax but maintains the same runtime behavior. The main risk is typos during refactoring.

### Mitigation Strategies
1. Make changes incrementally, one file at a time
2. Run tests after each file is modified
3. Use search/replace with careful review for repetitive changes
4. Verify OpenAPI documentation generation after changes

---

## Rollback Plan

If issues are discovered after deployment:

1. **Immediate rollback:** Revert the commit(s) containing the fixes
2. **Partial rollback:** If only specific files cause issues, revert those files individually
3. **Git commands:**
   ```bash
   # Revert specific commit
   git revert <commit-hash>
   
   # Revert specific file
   git checkout HEAD~1 -- path/to/file.py
   ```

---

## Success Criteria

1. ✅ All 30 BLOCKER issues resolved in SonarQube
2. ✅ All existing tests pass (70% coverage maintained)
3. ✅ Type checking passes with mypy
4. ✅ Linting passes with ruff
5. ✅ OpenAPI documentation generates correctly
6. ✅ Manual testing of key endpoints successful
7. ✅ No new issues introduced

---

## Post-Implementation

### Documentation Updates
- Update [`AGENTS.md`](AGENTS.md) if any non-obvious patterns were changed
- Add entry to CHANGELOG if maintained

### Monitoring
- Monitor application logs for any unexpected errors after deployment
- Check SonarQube dashboard to confirm BLOCKER count is 0

### Follow-up Tasks
After BLOCKER issues are fixed, consider addressing:
1. CRITICAL issues (30 issues) - Code duplication and cognitive complexity
2. MAJOR issues (47 issues) - HTTPException documentation and other improvements

---

## Appendix: Detailed Line-by-Line Changes

### File: apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py

**Change 1 - Add import:**
```python
# Add after line 1
from typing import Annotated
```

**Change 2 - Lines 140-141 (S8409):**
```python
# Before:
@app.get("/v1/health", response_model=HealthResponse, tags=["service"])
@app.get("/health", response_model=HealthResponse, tags=["service"])

# After:
@app.get("/v1/health", tags=["service"])
@app.get("/health", tags=["service"])
```

**Change 3 - Line 169 (S8410):**
```python
# Before:
def get_rules(
    service: RisktraceUiService = Depends(get_risktrace_service),
) -> RuleListResponse:

# After:
def get_rules(
    service: Annotated[RisktraceUiService, Depends(get_risktrace_service)],
) -> RuleListResponse:
```

**Change 4 - Lines 192, 196, 198 (S8410 + S8409):**
```python
# Before:
def get_rule(
    service: RisktraceUiService = Depends(get_risktrace_service),
    rule_id: str,
) -> RuleDetailResponse:

@app.get("/v1/calculator/rules/{rule_id}", response_model=RuleDetailResponse, tags=["calculator"])

# After:
def get_rule(
    service: Annotated[RisktraceUiService, Depends(get_risktrace_service)],
    rule_id: str,
) -> RuleDetailResponse:

@app.get("/v1/calculator/rules/{rule_id}", tags=["calculator"])
```

*[Continue this pattern for all remaining endpoints...]*

### File: apps/backend/src/rwa_common/db.py

**Change - Line 21 (S5644):**
```python
# Before:
SessionFactory = sessionmaker[Session]

# After:
from typing import TypeAlias  # Add to imports

SessionFactory: TypeAlias = sessionmaker
```

---

## Estimated Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: S8409 fixes | 1 hour | None |
| Phase 2: S8410 fixes | 1 hour | Phase 1 complete |
| Phase 3: S5644 fix | 15 min | None (can be parallel) |
| Phase 4: Validation | 30 min | All phases complete |
| **Total** | **2h 45min** | |

**Recommended approach:** Execute phases sequentially with validation after each phase to catch issues early.