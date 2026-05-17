# RiskTrace Control Tower Frontend

Frontend service for the RiskTrace Control Tower application.

## Quickstart

```powershell
npm ci
npm run dev
npm run build
npm run test:e2e
```

The development server binds to `127.0.0.1` and uses Vite's default port unless another port is
provided by the environment.

## Backend API

By default the app calls `/api/v1/dashboard/snapshot`. In local development Vite proxies `/api`
to `http://127.0.0.1:8000`, so start the backend with:

```powershell
cd ../backend
uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000
```

Set `VITE_RWA_API_BASE_URL` in `.env` to call a different REST API base URL.

## End-to-end tests

Playwright starts the backend and Vite through `scripts/playwright-web-server.mjs`. Install
browsers once, then run the suite:

```powershell
npm run playwright:install -- chromium
npm run test:e2e
```

## Docker

From the repository root:

```powershell
docker compose up --build frontend
```

The container serves the app on `http://127.0.0.1:8080` and proxies `/api/*` to the backend
service inside the Compose network.
