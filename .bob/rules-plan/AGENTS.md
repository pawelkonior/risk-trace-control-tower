# Plan Mode Rules (Non-Obvious Only)

## Architecture Constraints

### Backend Microservices Architecture
- **Single package, multiple services**: All 6 microservices (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs) share one `pyproject.toml` and dependency set
- **Service ports**: Calculator (8000), Projection (8010), Steering (8020), RATS (8030), Forecast (8040) - must not conflict
- **Batch error handling**: `calculate_batch()` intentionally continues on row errors for bank data-quality workflows - don't change this to fail-fast
- **Generated inputs coupling**: Steering service depends on deterministically generated CSVs with manifest validation - CI enforces reproducibility

### Database Architecture
- **Dynamic URL resolution**: Uses `RWA_DATABASE_URL` env var, falls back to temp SQLite file (not in-memory)
- **Pool strategy varies**: SQLite `:memory:` uses StaticPool, file URLs use NullPool, Postgres uses default pool with pre_ping
- **Docker Compose dependency**: Backend waits for Postgres health check, frontend waits for backend health check

### Frontend-Backend Integration
- **Dev proxy requirement**: Vite must proxy `/api` to `http://127.0.0.1:8000` - hardcoded backend URLs will break
- **Host binding constraint**: Both apps bind to `127.0.0.1` (not `localhost` or `0.0.0.0`) for consistency
- **E2E test coupling**: Playwright starts both backend and frontend in single command - backend must be on port 8000

### Testing Architecture
- **Coverage gates**: 70% minimum with branch coverage - affects CI pipeline
- **Pandera warnings**: Intentionally ignored in pytest config - don't try to fix them
- **Test isolation**: Backend tests run from `apps/backend/`, frontend from `apps/frontend/` - no shared test runner

### Package Data Constraints
- **Reference data inclusion**: Basel III JSONs in `src/rwa_calculator/reference_data/` included via setuptools.package-data
- **Generated inputs versioning**: CSVs in `src/rwa_steering/generated_inputs/` must match manifest hashes - manual edits break CI