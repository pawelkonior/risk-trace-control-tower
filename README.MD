<p align="center">
  <img src="apps/frontend/public/risktrace-logo.png" alt="RiskTrace Control Tower" width="168" />
</p>

<h1 align="center">RiskTrace Control Tower</h1>

<p align="center">
  Enterprise-grade Basel III RWA analytics, steering, lineage and AI-assisted executive
  commentary in one full-stack control tower.
</p>

<p align="center">
  <img alt="Python 3.12+" src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="React 19" src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black" />
  <img alt="Vite" src="https://img.shields.io/badge/Vite-7-646CFF?style=flat-square&logo=vite&logoColor=white" />
  <img alt="Docker Compose" src="https://img.shields.io/badge/Docker%20Compose-ready-2496ED?style=flat-square&logo=docker&logoColor=white" />
  <img alt="License" src="https://img.shields.io/badge/License-Proprietary-lightgrey?style=flat-square" />
</p>

---

## Overview

RiskTrace Control Tower is a monorepo for capital, credit-risk and RWA decision support. It
combines a Python/FastAPI backend, a React/Vite frontend, deterministic generated inputs,
AI-assisted RWA commentary, and production-oriented platform assets for observability,
deployment and security analysis.

The platform is built for teams that need to inspect Basel III capital metrics, understand
movement drivers, trace data lineage, run scenario projections, and turn portfolio signals into
clear management-ready briefings.

## What It Delivers

| Capability | Description |
| --- | --- |
| RWA dashboard | Portfolio capital summary, exposure mix, rating distribution, trends, alerts and map views. |
| Basel III calculator | Versioned REST API and CLI for credit RWA, output floor, operational risk, CVA, leverage ratio and portfolio capital calculations. |
| Projection and forecast services | Monthly run-off projections, VAR-style and recurrent factor forecast paths, Monte Carlo trajectories and capital-ratio breach analysis. |
| Steering and optimization | Scenario-aware steering recommendations plus deterministic Risk-Aware Trading Swarm optimization. |
| Data lineage | Traceable calculation flow and transformation steps for audit-style review. |
| AI executive commentary | Parallel RWA analysis agents with guardrails, retries, cache, cost tracking and optional LangFuse tracing. |
| Enterprise runtime assets | Docker Compose, Helm charts, Terraform modules, Kubernetes policy, Prometheus/Grafana/Loki/Tempo/Alertmanager configuration and local MCP security tooling. |

## Product Screens

<table>
  <tr>
    <td width="50%">
      <img src="docs/assets/readme/screens/home.png" alt="RiskTrace Control Tower home workspace" />
      <br />
      <strong>Management workspace</strong>
      <br />
      Quarter-end cockpit, system health and review queue.
    </td>
    <td width="50%">
      <img src="docs/assets/readme/screens/rwa-dashboard.png" alt="RiskTrace RWA Dashboard" />
      <br />
      <strong>RWA Dashboard</strong>
      <br />
      Exposure, RWA, capital ratio, country and rating views.
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="docs/assets/readme/screens/data-lineage.png" alt="RiskTrace Data Lineage" />
      <br />
      <strong>Data Lineage</strong>
      <br />
      End-to-end traceability from source records to calculated results.
    </td>
    <td width="50%">
      <img src="docs/assets/readme/screens/rwa-intelligence-briefing.png" alt="RiskTrace RWA Intelligence Briefing" />
      <br />
      <strong>RWA Intelligence Briefing</strong>
      <br />
      AI-assisted movement attribution and management action review.
    </td>
  </tr>
</table>

## Team

<table>
  <tr>
    <td align="center" width="20%">
      <img src="docs/assets/readme/team/cezary-szukiel.png" alt="Cezary Szukiel" width="140" />
      <br />
      <strong>Cezary Szukiel</strong>
    </td>
    <td align="center" width="20%">
      <img src="docs/assets/readme/team/karol-marszalek.png" alt="Karol Marszałek" width="140" />
      <br />
      <strong>Karol Marszałek</strong>
    </td>
    <td align="center" width="20%">
      <img src="docs/assets/readme/team/mateusz-natkaniec.png" alt="Mateusz Natkaniec" width="140" />
      <br />
      <strong>Mateusz Natkaniec</strong>
    </td>
    <td align="center" width="20%">
      <img src="docs/assets/readme/team/pawel-konior.png" alt="Paweł Konior" width="140" />
      <br />
      <strong>Paweł Konior</strong>
    </td>
    <td align="center" width="20%">
      <img src="docs/assets/readme/team/przemyslaw-stanisz.jpg" alt="Przemysław Stanisz" width="140" />
      <br />
      <strong>Przemysław Stanisz</strong>
    </td>
  </tr>
</table>

## Architecture

```mermaid
flowchart LR
    user[Risk, Finance and Treasury users] --> ui[React Control Tower]
    ui --> api[FastAPI Calculator API]

    api --> dashboard[RWA dashboard data]
    api --> calc[Basel III calculator]
    api --> capital[Capital modules]
    api --> agents[AI executive commentary agents]
    api --> lineage[Lineage and exports]

    calc --> reference[Reference data and jurisdiction overlays]
    calc --> generated[Generated steering inputs]
    agents --> watsonx[WatsonX or deterministic runtime]
    agents --> langfuse[Optional LangFuse traces]

    projection[Projection service] --> calc
    forecast[Forecast service] --> rats[RATS optimization]
    steering[Steering service] --> calc

    api --> db[(Postgres or local SQLite fallback)]
```

## Repository Map

```text
apps/
  backend/          Python 3.12 FastAPI services, CLI entry points, tests and generated inputs
  frontend/         React 19 + Vite control tower UI and Playwright tests
  docker-compose.yml

docker/             Host-oriented development and production Compose files
docs/               Technical analyses, validation reports and AI agent documentation
infra/
  helm/             Backend, frontend and platform Helm charts
  terraform/        AWS-oriented modules and environment definitions
  kubernetes/       Namespaces, RBAC and network policies
k8s/                Ingress, cert-manager, External Secrets and OPA policy examples
observability/      Prometheus, Grafana, Loki, Tempo, Alertmanager and agent alert rules
mcps/               Local SonarQube, OWASP ZAP and MCP-assisted quality/security tooling
scripts/            Bootstrap and operational helper scripts
```

## Quick Start

The fastest path is Docker Compose from the repository root:

```bash
cd apps
docker compose up --build frontend
```

Compose starts Postgres, the backend API and the frontend. When the health checks pass:

| Service | URL |
| --- | --- |
| Frontend | `http://127.0.0.1:8080` |
| Backend health | `http://127.0.0.1:8000/v1/health` |
| Dashboard API | `http://127.0.0.1:8000/v1/dashboard/snapshot` |

Stop the stack with:

```bash
docker compose down
```

## Local Development

### Prerequisites

- Python `>=3.12,<3.15`
- `uv`
- Node.js and npm
- Docker Desktop or Docker Engine with Compose

### Backend

```bash
cd apps/backend
cp .env.example .env
uv sync --all-groups
uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000
```

Useful backend commands:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run bandit -q -c pyproject.toml -r src
uv run rwa-generate-missing-inputs
```

The backend uses `RWA_DATABASE_URL` when it is set. If it is unset, it creates a temporary
SQLite database file for local execution. The Compose runtime uses Postgres:

```text
postgresql+psycopg://rwa:rwa_local_password@postgres:5432/rwa_steering
```

### Frontend

```bash
cd apps/frontend
cp .env.example .env
npm ci
npm run dev
```

The Vite development server binds to `127.0.0.1:5173` and proxies `/api` to the backend at
`http://127.0.0.1:8000` by default. Override the API target with `VITE_RWA_API_BASE_URL`.

Useful frontend commands:

```bash
npm run typecheck
npm run build
npm run playwright:install -- chromium
npm run test:e2e
```

## Service Catalog

All services are packaged in `apps/backend` and exposed through CLI entry points:

| Service | Command | Default port | Primary endpoint |
| --- | --- | ---: | --- |
| Calculator API | `uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000` | 8000 | `POST /v1/rwa/calculate` |
| Projection | `uv run rwa-projection --host 127.0.0.1 --port 8010` | 8010 | `POST /v1/projections/calculate` |
| Steering | `uv run rwa-steering --host 127.0.0.1 --port 8020` | 8020 | `POST /v1/steering/run` |
| RATS | `uv run rwa-rats --host 127.0.0.1 --port 8030` | 8030 | `POST /v1/rats/optimize` |
| Forecast | `uv run rwa-forecast --host 127.0.0.1 --port 8040` | 8040 | `POST /v1/forecasts/run` |
| Generated inputs | `uv run rwa-generate-missing-inputs` | n/a | Deterministic CSV and manifest regeneration |

## API Surface

Core calculator and capital endpoints:

```text
GET  /v1/health
GET  /v1/readiness
POST /v1/rwa/calculate
POST /v1/rwa/calculate/csv
POST /v1/output-floor/calculate
POST /v1/operational-risk/calculate
POST /v1/cva/calculate
POST /v1/leverage-ratio/calculate
POST /v1/capital/portfolio
```

RiskTrace UI endpoints:

```text
GET  /v1/app/context
GET  /v1/dashboard/snapshot
GET  /v1/lineage/traces/{trace_id}
GET  /v1/briefing/snapshot
POST /v1/agents/rwa-analysis/run
POST /v1/ui/actions/{action_id}
POST /v1/exports/{export_type}
GET  /v1/exports/{export_type}
GET  /v1/notifications
GET  /v1/search
```

Reference endpoints are available under `/reference/*` and compatibility routes without `/v1`
remain in place for selected calculator, projection, forecast, steering and RATS operations.

## Generated Inputs

`apps/backend/src/rwa_steering/generated_inputs/` contains deterministic CSV inputs plus a
manifest and validation metadata. The runtime loader verifies hashes, scenario references,
projection dates, overlay choices and rating-migration probability totals before the steering
service starts.

Regenerate the package after changing input-generation logic:

```bash
cd apps/backend
uv run rwa-generate-missing-inputs
```

CI is expected to fail if committed generated files drift from regeneration output.

## AI Agents

The AI-assisted RWA commentary workflow lives in `apps/backend/src/rwa_agents` and is exposed at
`POST /v1/agents/rwa-analysis/run`.

It includes:

- parallel Data Analyst and Risk Expert worker phases
- supervisor consensus and loop-limit handling
- request and output guardrails with PII sanitization
- exponential backoff retry for transient failures
- LRU response cache with TTL
- per-node timing, token usage, cost calculation and error/recovery metrics
- optional LangFuse prompt and trace integration
- WatsonX or deterministic local runtime

Default local and Compose execution uses deterministic mode. Configure WatsonX and LangFuse
through the backend `.env` when external AI services are required.

## Quality Gates

Backend:

```bash
cd apps/backend
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv run bandit -q -c pyproject.toml -r src
```

Frontend:

```bash
cd apps/frontend
npm run typecheck
npm run build
npm run test:e2e
```

Agent-specific tests are organized under `apps/backend/tests/agents/` with `chaos`,
`performance` and `integration` markers.

## Observability And Operations

The repository includes production-oriented observability assets:

- Prometheus rules under `observability/prometheus/rules/`
- Grafana dashboards under `observability/grafana/dashboards/`
- Loki and Tempo configuration under `observability/`
- Alertmanager configuration under `observability/alertmanager.yaml`
- AI agent alert rules under `observability/agents-alerts.yaml`

Agent SLO targets documented in `docs/agents/monitoring.md` include p95 latency below 10 seconds,
p99 latency below 15 seconds, success rate above 99.5 percent, token usage below 5000 tokens per
request, and cost below 0.50 USD per request.

## Deployment Assets

The repo contains several deployment paths:

| Path | Purpose |
| --- | --- |
| `apps/docker-compose.yml` | Local developer runtime for Postgres, backend and frontend. |
| `docker/docker-compose.yml` | Host-oriented development Compose setup. |
| `docker/docker-compose.prod.yml` | Production Compose template with external image tags and host nginx assumption. |
| `infra/helm/` | Backend, frontend and platform Helm charts. |
| `infra/terraform/` | AWS modules and dev/prod environment definitions. |
| `k8s/` and `infra/kubernetes/` | Ingress, certificates, External Secrets, OPA policy examples, namespaces, RBAC and network policies. |

## Local Security And MCP Tooling

Repository-local MCP-assisted quality and security tooling lives in `mcps/`. Copy local secrets
from templates:

```bash
cp mcps/.env.example mcps/.env
cp .bob/mcp.example.json .bob/mcp.json
```

Start and initialize local SonarQube:

```bash
docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d sonarqube
docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile setup run --rm -T sonarqube-init
```

Start OWASP ZAP:

```bash
docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d zap
```

Run local SonarQube scans:

```bash
docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-frontend
```

See `mcps/README.md` for the full workflow.

## Documentation

| Document | Description |
| --- | --- |
| `apps/backend/README.md` | Backend architecture, CLI, endpoints, generated inputs and quality gates. |
| `apps/frontend/README.md` | Frontend setup, API proxying and e2e test workflow. |
| `docs/agents/architecture.md` | RWA executive commentary workflow and resilience layers. |
| `docs/agents/contracts.md` | AI agent request and response contracts. |
| `docs/agents/monitoring.md` | Metrics, SLOs, dashboards and alerting guidance. |
| `docs/agents/validation.md` | Validation and guardrail guidance. |
| `docs/RCT-*_TECHNICAL_ANALYSIS.md` | Feature-level technical analyses. |
| `docs/RCT-*_IMPLEMENTATION_SUMMARY.md` | Implementation summaries and validation reports. |
