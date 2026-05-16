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