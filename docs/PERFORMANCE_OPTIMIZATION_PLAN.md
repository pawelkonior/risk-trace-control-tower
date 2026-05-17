# RiskTrace Control Tower - Performance Optimization Plan

**Date:** 2026-05-17  
**Version:** 1.0  
**Status:** Planning Phase

## Executive Summary

This document outlines a comprehensive performance optimization strategy for the RiskTrace Control Tower application, focusing on reducing latency, increasing throughput, and lowering error rates while maintaining all regulatory compliance, audit logging, and security controls.

## Identified Performance Bottlenecks

### 1. **Database Operations (HIGH PRIORITY)**

**Location:** `apps/backend/src/rwa_dashboard/repositories.py`, `apps/backend/src/rwa_common/db.py`

**Issues:**
- No connection pooling for production Postgres (uses default pool)
- SQLite NullPool for file-based databases prevents connection reuse
- No query result caching for frequently accessed datasets
- Synchronous database operations block request threads
- Deep copy operations on large payloads (`deepcopy(self.repository.get_payload())`)

**Impact:**
- High p95 latency on dashboard endpoints
- Database connection overhead on every request
- Memory pressure from payload duplication

### 2. **Heavy Data Processing (HIGH PRIORITY)**

**Location:** `apps/backend/src/rwa_dashboard/data.py`, `apps/backend/src/rwa_dashboard/api.py`

**Issues:**
- `current_rwa_snapshot()` loads entire portfolio and calculates RWA on every request (line 127-145)
- No caching of calculation results
- Pandas operations on large DataFrames without optimization
- Multiple groupby/aggregation operations per request
- CSV file loading on every calculation (`load_core_csv()`)

**Impact:**
- Dashboard endpoints likely >2s p95 latency
- High CPU usage during peak load
- Memory allocation spikes

### 3. **Synchronous Service Calls (MEDIUM PRIORITY)**

**Location:** `apps/backend/src/rwa_steering/engine.py`, `apps/backend/src/rwa_forecast_service/engine.py`

**Issues:**
- Sequential calculator batch calls in loops (lines 85, 105, 325)
- No parallelization of independent calculations
- Attribution driver calculations run sequentially (lines 263-277)
- Recommendation generation processes rows one-by-one (lines 347-373)

**Impact:**
- Linear scaling with portfolio size
- Underutilized CPU cores
- Long request times for large portfolios

### 4. **Frontend API Calls (MEDIUM PRIORITY)**

**Location:** `apps/frontend/src/api/client.ts`, `apps/frontend/src/hooks/useApiResource.ts`

**Issues:**
- No request deduplication
- No response caching
- Sequential API calls in hooks
- No request timeout configuration
- No retry logic for transient failures

**Impact:**
- Redundant backend calls
- Poor user experience on slow networks
- Cascading failures

### 5. **Data Serialization (LOW-MEDIUM PRIORITY)**

**Location:** Multiple FastAPI endpoints

**Issues:**
- No response compression (gzip/brotli)
- Large JSON payloads without pagination
- Decimal/date serialization overhead
- No streaming for large responses

**Impact:**
- High network bandwidth usage
- Slow response times on limited bandwidth
- Memory pressure on serialization

## Optimization Strategy

### Phase 1: Quick Wins (Week 1)

#### 1.1 Add Response Caching
- **File:** `apps/backend/src/rwa_dashboard/service.py`
- **Change:** Implement in-memory LRU cache for dashboard snapshots
- **Expected Impact:** 80-90% latency reduction for cached requests
- **Risk:** Low - cache invalidation on data updates

#### 1.2 Enable Response Compression
- **File:** `apps/backend/src/rwa_dashboard/api.py` (FastAPI middleware)
- **Change:** Add GZipMiddleware with compression level 6
- **Expected Impact:** 60-70% payload size reduction, 20-30% latency improvement
- **Risk:** Very Low - standard middleware

#### 1.3 Optimize Database Connection Pooling
- **File:** `apps/backend/src/rwa_common/db.py`
- **Change:** Configure proper pool size (10-20), max_overflow (5-10), pool_pre_ping
- **Expected Impact:** 30-40% reduction in connection overhead
- **Risk:** Low - standard SQLAlchemy configuration

#### 1.4 Add Request Timeouts
- **File:** `apps/frontend/src/api/client.ts`
- **Change:** Add 30s timeout with AbortController
- **Expected Impact:** Prevent hung requests, improve error handling
- **Risk:** Very Low - defensive programming

### Phase 2: Core Optimizations (Week 2-3)

#### 2.1 Implement Calculation Result Caching
- **File:** `apps/backend/src/rwa_dashboard/data.py`
- **Change:** Cache `current_rwa_snapshot()` results with TTL (5-15 minutes)
- **Expected Impact:** 90%+ latency reduction for repeated calculations
- **Risk:** Medium - requires cache invalidation strategy

#### 2.2 Optimize Pandas Operations
- **File:** `apps/backend/src/rwa_dashboard/data.py`
- **Changes:**
  - Use categorical dtypes for entity_class, sub_class, country codes
  - Vectorize operations instead of iterrows()
  - Pre-allocate DataFrames where possible
  - Use query() instead of boolean indexing
- **Expected Impact:** 40-60% reduction in data processing time
- **Risk:** Low - performance optimization only

#### 2.3 Add Async Database Operations
- **File:** `apps/backend/src/rwa_dashboard/repositories.py`
- **Change:** Use SQLAlchemy async engine with asyncpg
- **Expected Impact:** 50-70% throughput increase under load
- **Risk:** Medium - requires async/await refactoring

#### 2.4 Implement Batch Processing
- **File:** `apps/backend/src/rwa_steering/engine.py`
- **Change:** Parallelize independent calculator calls using ProcessPoolExecutor
- **Expected Impact:** 3-4x speedup on multi-core systems
- **Risk:** Medium - requires careful state management

### Phase 3: Advanced Optimizations (Week 4)

#### 3.1 Add Redis Caching Layer
- **Files:** New `apps/backend/src/rwa_common/cache.py`
- **Change:** Distributed cache for calculation results, dashboard snapshots
- **Expected Impact:** Horizontal scalability, 95%+ cache hit rate
- **Risk:** Medium - requires Redis infrastructure

#### 3.2 Implement Query Result Pagination
- **File:** `apps/backend/src/rwa_dashboard/api.py`
- **Change:** Add limit/offset pagination for large result sets
- **Expected Impact:** 70-80% reduction in response size
- **Risk:** Low - standard REST pattern

#### 3.3 Add Frontend Request Deduplication
- **File:** `apps/frontend/src/hooks/useApiResource.ts`
- **Change:** Implement request deduplication and response caching
- **Expected Impact:** 50-60% reduction in redundant API calls
- **Risk:** Low - client-side optimization

#### 3.4 Optimize CSV Loading
- **File:** `apps/backend/src/rwa_dashboard/data.py`
- **Change:** Load and cache CSV files at startup, not per-request
- **Expected Impact:** 100-200ms reduction per request
- **Risk:** Low - one-time load with refresh mechanism

## Performance Monitoring & Instrumentation

### Metrics to Track

1. **Latency Metrics:**
   - p50, p95, p99 response times per endpoint
   - Database query duration
   - Calculation engine duration
   - External service call duration

2. **Throughput Metrics:**
   - Requests per second (RPS)
   - Concurrent request handling
   - Queue depth

3. **Resource Metrics:**
   - CPU utilization
   - Memory usage
   - Database connection pool stats
   - Cache hit/miss rates

4. **Error Metrics:**
   - Error rate by endpoint
   - Timeout rate
   - Database connection errors
   - Cache failures

### Implementation

**File:** New `apps/backend/src/rwa_common/monitoring.py`

```python
# Prometheus metrics integration
from prometheus_client import Counter, Histogram, Gauge

request_duration = Histogram(
    'rwa_request_duration_seconds',
    'Request duration in seconds',
    ['endpoint', 'method', 'status']
)

calculation_duration = Histogram(
    'rwa_calculation_duration_seconds',
    'RWA calculation duration',
    ['calculation_type']
)

cache_hits = Counter(
    'rwa_cache_hits_total',
    'Cache hit count',
    ['cache_type']
)

db_pool_size = Gauge(
    'rwa_db_pool_size',
    'Database connection pool size'
)
```

## Testing Strategy

### 1. Performance Baseline
- Run k6 load tests before optimizations
- Capture baseline metrics for all endpoints
- Document current p95/p99 latencies

### 2. Regression Testing
- Ensure all existing tests pass
- Add performance regression tests
- Validate calculation results unchanged

### 3. Load Testing
- Gradually increase load to 2x, 5x, 10x baseline
- Monitor resource utilization
- Identify new bottlenecks

### 4. Chaos Testing
- Test cache failures
- Test database connection loss
- Validate graceful degradation

## Risk Assessment & Rollback Plan

### Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Cache invalidation bugs | Medium | High | Comprehensive testing, TTL safety net |
| Async/await refactoring errors | Medium | High | Gradual rollout, feature flags |
| Memory leaks from caching | Low | Medium | Memory monitoring, cache size limits |
| Database pool exhaustion | Low | High | Pool monitoring, circuit breakers |
| Breaking changes to API contracts | Low | Critical | Contract testing, versioning |

### Rollback Strategy

1. **Feature Flags:** All optimizations behind feature flags
2. **Gradual Rollout:** Deploy to dev → staging → 10% prod → 100% prod
3. **Monitoring:** Real-time alerts on latency/error rate increases
4. **Quick Rollback:** One-command rollback via feature flag toggle
5. **Database Migrations:** Reversible migrations only

### Rollback Triggers

- p95 latency increases >20% from baseline
- Error rate increases >1%
- Memory usage increases >50%
- Any calculation result discrepancies

## Expected Performance Impact

### Conservative Estimates

| Metric | Current (Estimated) | Target | Improvement |
|--------|-------------------|--------|-------------|
| Dashboard p95 latency | 2000-3000ms | <500ms | 75-85% |
| Calculation p95 latency | 1500-2500ms | <300ms | 80-88% |
| Throughput (RPS) | 10-20 | 50-100 | 250-500% |
| Error rate | 1-2% | <0.1% | 90-95% |
| Memory usage | Baseline | +20% | Acceptable |
| CPU efficiency | 30-40% | 60-80% | 50-100% |

### Aggressive Estimates (with all optimizations)

| Metric | Target | Improvement |
|--------|--------|-------------|
| Dashboard p95 latency | <200ms | 90-93% |
| Calculation p95 latency | <150ms | 93-95% |
| Throughput (RPS) | 100-200 | 500-1000% |
| Cache hit rate | >95% | N/A |

## Implementation Timeline

### Week 1: Quick Wins
- Day 1-2: Response caching + compression
- Day 3-4: Database pooling + timeouts
- Day 5: Testing and monitoring

### Week 2-3: Core Optimizations
- Day 6-8: Calculation caching
- Day 9-11: Pandas optimizations
- Day 12-14: Async database operations
- Day 15: Batch processing

### Week 4: Advanced & Polish
- Day 16-18: Redis integration
- Day 19-20: Pagination + deduplication
- Day 21-22: CSV loading optimization
- Day 23-24: Performance testing
- Day 25: Documentation and handoff

## Compliance & Security Notes

### Maintained Controls

✅ All validation logic preserved  
✅ Audit logging unchanged  
✅ Regulatory checks intact  
✅ Security controls maintained  
✅ Data integrity guarantees preserved  

### New Security Considerations

- Cache encryption for sensitive data
- Redis authentication and TLS
- Rate limiting to prevent abuse
- Cache poisoning prevention

## Success Criteria

1. ✅ p95 latency <500ms for all dashboard endpoints
2. ✅ p99 latency <1000ms for all endpoints
3. ✅ Error rate <0.1%
4. ✅ Throughput >50 RPS sustained
5. ✅ All existing tests pass
6. ✅ No calculation result changes
7. ✅ Memory usage increase <30%
8. ✅ Zero security regressions

## Next Steps

1. **Approve Plan:** Review and approve optimization strategy
2. **Create Performance Dataset:** Generate baseline metrics
3. **Set Up Monitoring:** Deploy Prometheus/Grafana dashboards
4. **Begin Phase 1:** Implement quick wins
5. **Measure & Iterate:** Continuous measurement and refinement

---

**Document Owner:** Performance Engineering Team  
**Last Updated:** 2026-05-17  
**Next Review:** After Phase 1 completion