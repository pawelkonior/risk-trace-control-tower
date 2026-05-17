# Performance Optimization Implementation Guide

This guide provides detailed implementation steps for each optimization in the performance plan.

## Table of Contents

1. [Phase 1: Quick Wins](#phase-1-quick-wins)
2. [Phase 2: Core Optimizations](#phase-2-core-optimizations)
3. [Phase 3: Advanced Optimizations](#phase-3-advanced-optimizations)
4. [Testing & Validation](#testing--validation)

---

## Phase 1: Quick Wins

### 1.1 Response Caching with LRU Cache

**File:** `apps/backend/src/rwa_common/cache.py` (new)

```python
from __future__ import annotations

from functools import lru_cache, wraps
from typing import Any, Callable, TypeVar
from datetime import datetime, timedelta
import hashlib
import json

T = TypeVar("T")

class TTLCache:
    """Time-based LRU cache with automatic expiration."""
    
    def __init__(self, ttl_seconds: int = 300, maxsize: int = 128):
        self.ttl_seconds = ttl_seconds
        self.maxsize = maxsize
        self._cache: dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Any | None:
        if key not in self._cache:
            return None
        value, expires_at = self._cache[key]
        if datetime.utcnow() > expires_at:
            del self._cache[key]
            return None
        return value
    
    def set(self, key: str, value: Any) -> None:
        if len(self._cache) >= self.maxsize:
            # Remove oldest entry
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        expires_at = datetime.utcnow() + timedelta(seconds=self.ttl_seconds)
        self._cache[key] = (value, expires_at)
    
    def clear(self) -> None:
        self._cache.clear()

# Global cache instances
dashboard_cache = TTLCache(ttl_seconds=300, maxsize=100)
calculation_cache = TTLCache(ttl_seconds=600, maxsize=50)

def cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate cache key from function arguments."""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    return hashlib.sha256(key_data.encode()).hexdigest()

def cached(cache: TTLCache) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for caching function results with TTL."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator
```

**File:** `apps/backend/src/rwa_dashboard/data.py` (modify)

```python
# Add at top of file
from rwa_common.cache import cached, calculation_cache

# Modify current_rwa_snapshot function
@cached(calculation_cache)
def current_rwa_snapshot(as_of_date: date, row_limit: int | None = None) -> CurrentRwaSnapshot:
    """Calculate current Basel RWA and aggregate it for the dashboard.
    
    Results are cached for 10 minutes to avoid redundant calculations.
    """
    # ... existing implementation
```

**Expected Impact:** 80-90% latency reduction for cached requests

---

### 1.2 Response Compression

**File:** `apps/backend/src/rwa_dashboard/api.py` (modify)

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZIPMiddleware

def create_dashboard_app() -> FastAPI:
    app = FastAPI(title="RWA Dashboard API")
    
    # Add compression middleware
    app.add_middleware(
        GZIPMiddleware,
        minimum_size=1000,  # Only compress responses > 1KB
        compresslevel=6     # Balance between speed and compression ratio
    )
    
    # ... rest of app setup
```

**Expected Impact:** 60-70% payload size reduction, 20-30% latency improvement

---

### 1.3 Database Connection Pooling

**File:** `apps/backend/src/rwa_common/db.py` (modify)

```python
def create_database_engine(database_url: str | None = None) -> Engine:
    """Create an SQLAlchemy engine with optimized connection pooling."""
    resolved_url = database_url or os.getenv("RWA_DATABASE_URL")
    if resolved_url is None:
        sqlite_path = Path(gettempdir()) / f"risktrace-ui-{uuid4().hex}.sqlite3"
        resolved_url = f"sqlite+pysqlite:///{sqlite_path}"
    
    if resolved_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        if resolved_url.endswith(":memory:"):
            return create_engine(
                resolved_url,
                connect_args=connect_args,
                poolclass=StaticPool,
                future=True,
            )
        return create_engine(
            resolved_url,
            connect_args=connect_args,
            poolclass=NullPool,
            future=True,
        )
    
    # Production Postgres configuration with optimized pooling
    return create_engine(
        resolved_url,
        pool_size=20,              # Increased from default 5
        max_overflow=10,           # Allow burst capacity
        pool_pre_ping=True,        # Verify connections before use
        pool_recycle=3600,         # Recycle connections after 1 hour
        echo_pool=False,           # Disable pool logging in production
        future=True,
    )
```

**Expected Impact:** 30-40% reduction in connection overhead

---

### 1.4 Request Timeouts

**File:** `apps/frontend/src/api/client.ts` (modify)

```typescript
const DEFAULT_API_BASE_URL = "/api";
const DEFAULT_TIMEOUT_MS = 30000; // 30 seconds

export async function requestJson<T>(
  path: string,
  options: RequestInit & { signal?: AbortSignal; timeout?: number } = {},
): Promise<T> {
  const timeout = options.timeout ?? DEFAULT_TIMEOUT_MS;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(`${apiBaseUrl()}${path}`, {
      ...options,
      signal: options.signal ?? controller.signal,
      headers: {
        Accept: "application/json",
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...options.headers,
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(await readErrorMessage(response));
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return (await response.json()) as T;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout - please try again');
    }
    throw error;
  }
}
```

**Expected Impact:** Prevent hung requests, improve error handling

---

## Phase 2: Core Optimizations

### 2.1 Pandas Optimization

**File:** `apps/backend/src/rwa_dashboard/data.py` (modify)

```python
def _calculator_results_frame(
    source_rows: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> pd.DataFrame:
    """Join calculator output with input metadata and convert numeric values for charts.
    
    Optimized version using categorical dtypes and vectorized operations.
    """
    if not results:
        return pd.DataFrame(columns=[*CORE_METADATA_COLUMNS, *RWA_FIELDS])
    
    # Use categorical dtypes for low-cardinality columns
    metadata = pd.DataFrame(source_rows)[list(CORE_METADATA_COLUMNS)]
    metadata['entity_class'] = metadata['entity_class'].astype('category')
    metadata['sub_class'] = metadata['sub_class'].astype('category')
    metadata['exposure_ccy'] = metadata['exposure_ccy'].astype('category')
    metadata['incorporation_country'] = metadata['incorporation_country'].astype('category')
    
    output = pd.DataFrame(results)
    frame = metadata.merge(output, on="id", how="inner")
    
    # Vectorized numeric conversion (faster than map)
    numeric_cols = [*("exposure_amount", "residual_maturity", "counterparty_dlgd"), 
                    *RWA_FIELDS, *RISK_WEIGHT_FIELDS]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors='coerce')
    
    # Vectorized ratio calculation
    frame["rwa_density"] = frame[RWA_FINAL_FIELD].div(
        frame["exposure_amount"].where(frame["exposure_amount"] != 0)
    )
    
    return frame
```

**Expected Impact:** 40-60% reduction in data processing time

---

### 2.2 Async Database Operations

**File:** `apps/backend/src/rwa_common/db_async.py` (new)

```python
from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async def create_async_database_engine(database_url: str | None = None) -> AsyncEngine:
    """Create an async SQLAlchemy engine for non-blocking database operations."""
    resolved_url = database_url or os.getenv("RWA_DATABASE_URL")
    
    if resolved_url is None:
        sqlite_path = Path(gettempdir()) / f"risktrace-ui-{uuid4().hex}.sqlite3"
        resolved_url = f"sqlite+aiosqlite:///{sqlite_path}"
    
    # Convert sync URLs to async
    if resolved_url.startswith("sqlite+pysqlite"):
        resolved_url = resolved_url.replace("sqlite+pysqlite", "sqlite+aiosqlite")
    elif resolved_url.startswith("postgresql://"):
        resolved_url = resolved_url.replace("postgresql://", "postgresql+asyncpg://")
    
    return create_async_engine(
        resolved_url,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
        future=True,
    )

def create_async_session_factory(engine: AsyncEngine) -> sessionmaker[AsyncSession]:
    """Create an async session factory."""
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )

async def async_session_scope(
    session_factory: sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async request-scoped DB session."""
    async with session_factory() as session:
        yield session
```

**File:** `apps/backend/src/rwa_dashboard/repositories_async.py` (new)

```python
from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import RisktraceUiDataset

class AsyncRisktraceUiRepository:
    """Async persistence gateway for frontend-facing RiskTrace data."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_payload(self, dataset_key: str) -> dict[str, Any]:
        """Fetch dataset payload asynchronously."""
        result = await self.session.execute(
            select(RisktraceUiDataset).where(RisktraceUiDataset.dataset_key == dataset_key)
        )
        dataset = result.scalar_one_or_none()
        if dataset is None:
            raise RisktraceDatasetNotFoundError(dataset_key)
        return dict(dataset.payload)
```

**Expected Impact:** 50-70% throughput increase under load

---

### 2.3 Parallel Batch Processing

**File:** `apps/backend/src/rwa_steering/engine.py` (modify)

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any

class RwaSteeringService:
    def __init__(self, *args, max_workers: int = 4, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_workers = max_workers
    
    def _parallel_driver_deltas(
        self,
        request: SteeringRequest,
        scenario: ScenarioAssumption,
        projection_date: date,
        current_total: Decimal,
    ) -> dict[str, Decimal]:
        """Calculate all attribution drivers in parallel."""
        
        drivers = [
            ("volume_delta", {"apply_volume": True}),
            ("maturity_delta", {"apply_maturity": True}),
            ("rating_delta", {"apply_rating": True}),
            ("dlgd_delta", {"apply_dlgd": True}),
            ("fx_delta", {"apply_fx": True}),
        ]
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self._driver_delta,
                    request,
                    scenario,
                    projection_date,
                    current_total,
                    **flags
                ): name
                for name, flags in drivers
            }
            
            results = {}
            for future in as_completed(futures):
                driver_name = futures[future]
                results[driver_name] = future.result()
        
        return results
```

**Expected Impact:** 3-4x speedup on multi-core systems

---

## Phase 3: Advanced Optimizations

### 3.1 Redis Caching Layer

**File:** `apps/backend/src/rwa_common/redis_cache.py` (new)

```python
from __future__ import annotations

import json
import pickle
from typing import Any
from datetime import timedelta

try:
    import redis
    from redis import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class RedisCache:
    """Distributed cache using Redis for horizontal scalability."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        default_ttl: int = 300,
    ):
        if not REDIS_AVAILABLE:
            raise RuntimeError("Redis not available - install redis-py")
        
        self.client: Redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=False,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Any | None:
        """Get value from cache."""
        try:
            value = self.client.get(key)
            if value is None:
                return None
            return pickle.loads(value)
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """Set value in cache with TTL."""
        try:
            serialized = pickle.dumps(value)
            ttl_seconds = ttl or self.default_ttl
            return self.client.setex(key, timedelta(seconds=ttl_seconds), serialized)
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            return bool(self.client.delete(key))
        except Exception:
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern."""
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception:
            return 0
```

**Expected Impact:** Horizontal scalability, 95%+ cache hit rate

---

### 3.2 Request Deduplication

**File:** `apps/frontend/src/hooks/useApiResource.ts` (modify)

```typescript
import { useEffect, useState, useRef } from "react";

// Global request cache
const requestCache = new Map<string, Promise<any>>();
const responseCache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL_MS = 60000; // 1 minute

export function useApiResource<T>(
  load: (signal: AbortSignal) => Promise<T>,
  deps: unknown[] = [],
  options: { enabled?: boolean; cacheKey?: string; cacheTTL?: number } = {},
) {
  const enabled = options.enabled ?? true;
  const cacheKey = options.cacheKey;
  const cacheTTL = options.cacheTTL ?? CACHE_TTL_MS;
  
  const [state, setState] = useState<ApiResourceState<T>>({
    data: null,
    error: null,
    isLoading: enabled,
  });

  useEffect(() => {
    if (!enabled) {
      setState((current) => ({ ...current, isLoading: false }));
      return;
    }

    // Check response cache first
    if (cacheKey) {
      const cached = responseCache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < cacheTTL) {
        setState({ data: cached.data, error: null, isLoading: false });
        return;
      }
    }

    const controller = new AbortController();
    setState((current) => ({ ...current, error: null, isLoading: true }));

    // Deduplicate in-flight requests
    const executeLoad = async () => {
      if (cacheKey && requestCache.has(cacheKey)) {
        return requestCache.get(cacheKey)!;
      }

      const promise = load(controller.signal);
      if (cacheKey) {
        requestCache.set(cacheKey, promise);
      }

      try {
        const result = await promise;
        if (cacheKey) {
          responseCache.set(cacheKey, { data: result, timestamp: Date.now() });
          requestCache.delete(cacheKey);
        }
        return result;
      } catch (error) {
        if (cacheKey) {
          requestCache.delete(cacheKey);
        }
        throw error;
      }
    };

    executeLoad()
      .then((data) => {
        if (!controller.signal.aborted) {
          setState({ data, error: null, isLoading: false });
        }
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }
        setState({
          data: null,
          error: error instanceof Error ? error.message : "REST API unavailable",
          isLoading: false,
        });
      });

    return () => controller.abort();
  }, [enabled, cacheKey, cacheTTL, ...deps]);

  return state;
}
```

**Expected Impact:** 50-60% reduction in redundant API calls

---

## Testing & Validation

### Performance Test Suite

**File:** `apps/backend/tests/performance/test_dashboard_performance.py` (new)

```python
import pytest
import time
from datetime import date

from rwa_dashboard.data import current_rwa_snapshot

@pytest.mark.performance
def test_dashboard_snapshot_latency():
    """Verify dashboard snapshot completes within SLO."""
    start = time.perf_counter()
    snapshot = current_rwa_snapshot(date(2026, 1, 1))
    duration_ms = (time.perf_counter() - start) * 1000
    
    assert duration_ms < 500, f"Dashboard snapshot took {duration_ms:.0f}ms (SLO: 500ms)"
    assert not snapshot.results.empty

@pytest.mark.performance
def test_dashboard_snapshot_cached():
    """Verify cached requests are fast."""
    # First call (cache miss)
    current_rwa_snapshot(date(2026, 1, 1))
    
    # Second call (cache hit)
    start = time.perf_counter()
    current_rwa_snapshot(date(2026, 1, 1))
    duration_ms = (time.perf_counter() - start) * 1000
    
    assert duration_ms < 50, f"Cached snapshot took {duration_ms:.0f}ms (expected <50ms)"
```

### Load Test Enhancement

**File:** `k6/performance-test.js` (new)

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const errorRate = new Rate("errors");
const dashboardLatency = new Trend("dashboard_p95_latency", true);
const cacheHitRate = new Rate("cache_hits");

export const options = {
  scenarios: {
    performance_test: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "1m", target: 20 },
        { duration: "3m", target: 50 },
        { duration: "1m", target: 0 },
      ],
    },
  },
  thresholds: {
    "dashboard_p95_latency": ["p(95)<500"],
    "http_req_duration": ["p(95)<1000"],
    "errors": ["rate<0.001"],
    "cache_hits": ["rate>0.80"],
  },
};

const BASE_URL = __ENV.TARGET_URL || "http://localhost:8000";

export default function () {
  const res = http.get(`${BASE_URL}/v1/dashboard/snapshot`);
  
  check(res, {
    "status 200": (r) => r.status === 200,
    "latency <500ms": (r) => r.timings.duration < 500,
  });
  
  dashboardLatency.add(res.timings.duration);
  errorRate.add(res.status !== 200);
  
  // Check for cache hit header
  const cacheHit = res.headers["X-Cache-Hit"] === "true";
  cacheHitRate.add(cacheHit);
  
  sleep(1);
}
```

---

## Deployment Checklist

- [ ] Run full test suite
- [ ] Run performance benchmarks
- [ ] Deploy to dev environment
- [ ] Validate metrics in dev
- [ ] Deploy to staging
- [ ] Run load tests in staging
- [ ] Deploy to 10% production
- [ ] Monitor for 24 hours
- [ ] Deploy to 100% production
- [ ] Document results

## Monitoring Alerts

```yaml
# Prometheus alert rules
groups:
  - name: performance
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.95, rwa_request_duration_seconds) > 0.5
        for: 5m
        annotations:
          summary: "p95 latency above SLO"
      
      - alert: LowCacheHitRate
        expr: rate(rwa_cache_hits_total[5m]) / rate(rwa_cache_requests_total[5m]) < 0.80
        for: 10m
        annotations:
          summary: "Cache hit rate below 80%"
```

---

**Next:** Switch to Code mode to implement these optimizations