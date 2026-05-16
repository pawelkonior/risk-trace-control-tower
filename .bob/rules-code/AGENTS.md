# Code Mode Rules (Non-Obvious Only)

## Backend Python Patterns
- **Import style**: Always use `from __future__ import annotations` at top of files (Python 3.12+ requirement)
- **Decimal precision**: Use `RATE_Q = Decimal("0.000001")` and `MONEY_Q = Decimal("0.01")` constants from calculator.py for rounding
- **Error tolerance in batch**: `calculate_batch()` collects errors per row instead of failing entire batch - this is intentional for bank workflows
- **Package data access**: Reference data JSONs in `src/rwa_calculator/reference_data/` are included via setuptools.package-data, not as regular files
- **CLI entry points**: Six different microservices share one package - use correct entry point (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs)
- **Database pooling**: SQLite `:memory:` uses StaticPool, file URLs use NullPool, Postgres uses default with pre_ping
- **Generated inputs**: Never manually edit CSVs in `src/rwa_steering/generated_inputs/` - always regenerate with `uv run rwa-generate-missing-inputs`

## Frontend React/TypeScript Patterns
- **API base URL**: Use `apiBaseUrl()` from `src/api/client.ts` which respects `VITE_RWA_API_BASE_URL` env var
- **Dev proxy**: Vite dev server proxies `/api` to backend at `http://127.0.0.1:8000` - don't hardcode backend URLs
- **Host binding**: Always use `127.0.0.1` not `localhost` or `0.0.0.0` for consistency with backend
- **Playwright setup**: E2E tests start both backend AND frontend in single command - backend must be on port 8000

## Testing
- **Single test file**: `uv run pytest tests/calculator/test_rwa_backend.py` (from backend directory)
- **Coverage requirement**: 70% minimum with branch coverage enabled
- **Test warnings**: Pandera deprecation warnings are intentionally ignored in pytest config
- **E2E browser install**: Run `npm run playwright:install` once before first e2e test run