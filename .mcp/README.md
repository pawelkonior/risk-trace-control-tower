# Local MCP Tooling

This directory owns repository-local MCP tooling for RiskTrace Control Tower. It stays separate
from `apps/docker-compose.yml` so quality and security assistant tooling does not change backend
or frontend application runtime behavior.

## What Is Included

- `.mcp/docker-compose.yml` starts local SonarQube, its Postgres database, and OWASP ZAP.
- `sonarqube-init` is a one-shot Compose service with the `setup` profile. It creates the backend
  and frontend SonarQube projects, refreshes a local token, and stores it in the
  `risktrace_mcp_secrets` Docker volume.
- `sonarqube-mcp`, `owasp-zap-mcp`, and `sonatype-guide-mcp` are stdio MCP services intended to
  be started by IBM Bob through `.bob/mcp.json`. They are hidden behind the `mcp` profile so a
  plain Compose `up` does not start them.
- `sonar-scan-backend` and `sonar-scan-frontend` publish analysis to the local SonarQube. They
  are hidden behind the `scan` profile.

## Secret Handling

Do not put real tokens or passwords in committed files. Copy the template and edit local values:

```bash
cp .mcp/.env.example .mcp/.env
```

`.mcp/.env` is ignored by git. The generated SonarQube token is stored in the
`risktrace_mcp_secrets` Docker volume, not in the repository.

## Start SonarQube

From the repository root:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml up -d sonarqube
```

Then initialize the local projects and token:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml --profile setup run --rm -T sonarqube-init
```

The initializer:

1. Waits for `http://sonarqube:9000` inside the Compose network.
2. Creates these projects when missing:
   - `risktrace-control-tower-backend`
   - `risktrace-control-tower-frontend`
3. Revokes and regenerates the token named by `SONARQUBE_TOKEN_NAME`.
4. Writes the MCP/scanner environment to the shared Docker volume.

If you changed the local SonarQube admin password in the UI, update `.mcp/.env` with the matching
`SONARQUBE_ADMIN_USER` and `SONARQUBE_ADMIN_PASSWORD` before running `sonarqube-init`.

## Analyze Backend And Frontend

The local project settings are committed under `.mcp/sonarqube/` and contain no secrets.

Run scans from the repository root:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml --profile scan run --rm -T sonar-scan-frontend
```

These services read the SonarQube token from the shared Docker volume. Run `sonarqube-init` again
if the token is missing or should be rotated.

## Start OWASP ZAP

From the repository root:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml up -d zap
```

This starts the ZAP daemon at `http://127.0.0.1:8090`, installs the official ZAP MCP Integration
add-on inside that same container, and exposes the add-on at `http://127.0.0.1:8282` by default.
It does not start a spider, AJAX spider, passive wait, or active scan. Any active scan must be
requested explicitly by a developer against an authorized local target.

The default target hint is:

```bash
ZAP_MCP_TARGET_URL=http://127.0.0.1:5173
```

Change it in `.mcp/.env` if the MCP workflow should target a different local URL.

## IBM Bob MCP

`.bob/mcp.json` is committed and is the source of truth for IBM Bob. Local RiskTrace MCP entries
start Compose services directly with the `mcp` profile:

- `risktrace-sonarqube` -> `sonarqube-mcp`
- `owaspZap` -> `owasp-zap-mcp`
- `sonatype-guide` -> `sonatype-guide-mcp`

Atlassian MCP stays as a direct remote MCP entry because it is not part of the local RiskTrace
tooling runtime.

## Stop Local Tooling

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml down
```
