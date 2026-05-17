# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Monorepo Structure
- `apps/backend/` - Python backend with `src/` layout, multiple microservices in single package
- `apps/frontend/` - React/Vite frontend
- Docker Compose orchestrates both apps with Postgres at repository root level (`apps/docker-compose.yml`)

## Backend (Python)

### Commands (from `apps/backend/`)
```bash
uv sync --all-groups              # Install all dependencies including dev
uv run pytest                     # Run all tests with coverage
uv run pytest tests/calculator/test_rwa_backend.py  # Single test file
uv run ruff check .               # Lint
uv run ruff format --check .      # Format check
uv run mypy                       # Type check
uv run bandit -q -c pyproject.toml -r src  # Security scan
uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000  # Start main API
uv run rwa-generate-missing-inputs  # Regenerate generated_inputs package
```

### Non-Obvious Patterns
- **Generated inputs package**: `src/rwa_steering/generated_inputs/` contains deterministically generated CSVs with manifest/validation. CI fails if committed files drift from regeneration. Use `uv run rwa-generate-missing-inputs` to regenerate.
- **Multiple microservices in one package**: Single `pyproject.toml` defines 6 CLI entry points (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs) for different services on different ports.
- **Batch calculation tolerance**: `RwaCalculator.calculate_batch()` intentionally continues on row errors, collecting them in `errors` array rather than failing entire batch (mirrors bank data-quality workflows).
- **Database URL resolution**: Uses `RWA_DATABASE_URL` env var. If unset, creates temp SQLite file in system temp dir (not in-memory). SQLite uses `StaticPool` for `:memory:` URLs, `NullPool` for file URLs.
- **Reference data in package**: `src/rwa_calculator/reference_data/` contains JSON files for Basel III rules and jurisdiction overlays, included via `setuptools.package-data`.

### Code Style (from pyproject.toml)
- Line length: 100 characters
- Python 3.12+ required (uses `from __future__ import annotations`)
- Ruff ignores: B008, B904, BLE001, S101, UP042
- Tests ignore S101 (assert usage), PT009
- Mypy: `strict = false` but enables `check_untyped_defs`, disables many error codes
- Coverage: 70% minimum, branch coverage enabled

### AI Agents Observability Features

**Implementation:** `src/rwa_agents/` package

The RWA AI Agents system includes comprehensive observability, resilience, and performance features:

**Observability (`observability.py`):**
- Per-node execution timing with millisecond precision
- Token usage tracking with cost calculation (WatsonX pricing)
- Error recording with retry and recovery tracking
- Optional LangFuse integration for trace analysis

**Resilience (`retry.py`, `guardrails.py`):**
- Exponential backoff retry (3 attempts, 1s base delay, 30s max)
- Guardrail recovery with PII sanitization
- Structured error records with recovery strategies
- Graceful degradation on failures

**Performance (`cache.py`, `tools.py`):**
- LRU cache with TTL for LLM responses (1000 entries, 1h TTL)
- Parallel tool execution for independent operations
- Response caching reduces costs by up to 60%
- Thread-safe cache implementation

**Prompt Management (`prompts.py`):**
- Remote prompt versioning via LangFuse
- Local fallback for reliability
- 5-minute cache TTL for prompts
- A/B testing support

**Configuration:**
```bash
# Enable LangFuse observability
export RWA_LANGFUSE_ENABLED=true
export RWA_LANGFUSE_PUBLIC_KEY=pk-lf-xxx
export RWA_LANGFUSE_SECRET_KEY=sk-lf-xxx
export RWA_LANGFUSE_BASE_URL=https://cloud.langfuse.com

# Enable LLM Guard guardrails
export RWA_AGENTS_LLM_GUARD_ENABLED=true

# WatsonX configuration
export RWA_AGENTS_LLM_PROVIDER=watsonx
export RWA_AGENTS_WATSONX_PROJECT_ID=your-project-id
export RWA_AGENTS_WATSONX_APIKEY=your-api-key
export RWA_AGENTS_WATSONX_URL=https://us-south.ml.cloud.ibm.com
export RWA_AGENTS_WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
```

**Key Metrics:**
- `workflow_duration_ms`: Total end-to-end latency
- `node_timings`: Per-node execution time
- `total_token_count`: Cumulative tokens across LLM calls
- `total_cost_usd`: Calculated cost based on pricing
- `error_count` / `recovery_count`: Error handling metrics

**SLA Targets:**
- Latency: p95 < 10s, p99 < 15s
- Token usage: < 5000 tokens per request
- Cost: < $0.50 per request
- Success rate: > 99.5%

### Testing Guidelines

**Test Organization:**
```bash
tests/agents/
├── test_validation.py      # Input validation tests
├── test_chaos.py           # Chaos engineering tests
├── test_performance.py     # Performance and SLA tests
└── test_integration.py     # Integration tests
```

**Running Tests:**
```bash
# All agent tests
uv run pytest tests/agents/ -v

# Chaos tests (failure scenarios)
uv run pytest -m chaos tests/agents/test_chaos.py -v

# Performance tests (SLA validation)
uv run pytest -m performance tests/agents/test_performance.py -v

# With coverage
uv run pytest tests/agents/ --cov=rwa_agents --cov-report=html
```

**Test Markers:**
- `@pytest.mark.chaos` - Chaos engineering tests (timeouts, failures, recovery)
- `@pytest.mark.performance` - Performance tests (latency, tokens, cost)
- `@pytest.mark.integration` - Integration tests with external services

**Chaos Test Scenarios:**
1. LLM timeout handling with retry
2. Partial agent failure with degraded results
3. Guardrail recovery with PII sanitization
4. Network errors with exponential backoff

**Performance Test Scenarios:**
1. Workflow latency within 10s SLA
2. Token usage within 5000 token budget
3. Cost within $0.50 budget
4. Cache effectiveness (hit rate > 30%)

**Example Test:**
```python
@pytest.mark.performance
def test_workflow_latency() -> None:
    """Test workflow completes within SLA (10 seconds)."""
    request = RwaAnalysisRequest.model_validate(valid_payload())
    
    start_time = time.perf_counter()
    response = run_rwa_analysis(request)
    duration = time.perf_counter() - start_time
    
    assert response.status == "COMPLETED"
    assert duration < 10.0, f"Workflow took {duration:.2f}s, exceeds 10s SLA"
    assert response.observability.workflow_duration_ms < 10000
```

**Documentation:**
- [Implementation Summary](docs/agents/RCT-AGENTS-IMPROVEMENTS.md) - Detailed improvements
- [Architecture](docs/agents/architecture.md) - System architecture with new components
- [Monitoring Guide](docs/agents/monitoring.md) - Metrics, dashboards, alerting
- [API Contracts](docs/agents/contracts.md) - Request/response schemas

## Frontend (React/TypeScript)

### Commands (from `apps/frontend/`)
```bash
npm ci                            # Install dependencies
npm run dev                       # Dev server on 127.0.0.1:5173
npm run typecheck                 # TypeScript check (must pass before build)
npm run build                     # Typecheck then build
npm run test:e2e                  # Playwright tests
npm run playwright:install        # Install browsers once
```

### Non-Obvious Patterns
- **API proxy in dev**: Vite proxies `/api` to `http://127.0.0.1:8000` (backend). Set `VITE_RWA_API_BASE_URL` to override.
- **Playwright web server**: `playwright.config.ts` starts BOTH backend and frontend in single shell command for e2e tests. Backend must be available on port 8000.
- **Dev server binding**: Always binds to `127.0.0.1` (not `localhost` or `0.0.0.0`) for consistency with backend.

## Docker Compose (from repository root)
```bash
cd apps && docker compose up --build backend   # Backend only
cd apps && docker compose up --build frontend  # Frontend only (depends on backend)
```
- Compose file is at `apps/docker-compose.yml` (not root)
- Backend waits for Postgres health check before starting
- Frontend waits for backend health check before starting
- Postgres uses volume `postgres_data` for persistence