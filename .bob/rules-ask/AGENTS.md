# Ask Mode Rules (Non-Obvious Only)

## Project Documentation Context

### Monorepo Structure
- `apps/backend/` contains Python backend with `src/` layout - NOT a typical backend folder structure
- Single `pyproject.toml` defines 6 different microservices as CLI entry points (not separate packages)
- Docker Compose file is at `apps/docker-compose.yml` (not at repository root)

### Backend Architecture
- **Multiple services, one package**: rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs all share dependencies
- **Generated inputs are versioned**: `src/rwa_steering/generated_inputs/` contains CSVs that must match manifest hashes - CI fails on drift
- **Reference data in package**: Basel III rules in `src/rwa_calculator/reference_data/` are included via setuptools, not external files
- **Database defaults**: If `RWA_DATABASE_URL` unset, creates temp SQLite file (not in-memory) in system temp directory

### Frontend Architecture
- **Dev proxy setup**: Vite proxies `/api` to `http://127.0.0.1:8000` - backend must be running on that exact address
- **Playwright web server**: E2E config starts BOTH backend and frontend in single shell command (not separate processes)
- **API base URL**: Uses `apiBaseUrl()` helper that respects `VITE_RWA_API_BASE_URL` env var

### Testing Context
- **Backend tests**: Run from `apps/backend/` directory with `uv run pytest`
- **Single test file**: `uv run pytest tests/calculator/test_rwa_backend.py` for focused testing
- **Frontend E2E**: Requires `npm run playwright:install` once before first run
- **Coverage gates**: 70% minimum with branch coverage enabled