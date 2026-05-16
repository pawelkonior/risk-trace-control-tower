# Local MCP Tooling

This directory owns the repository-local MCP tooling setup for RiskTrace Control Tower. It is
intentionally separate from `apps/docker-compose.yml` so quality and security assistant tooling
does not change backend or frontend application runtime behavior.

## What Is Included

- `.mcp/docker-compose.yml` starts local SonarQube, its Postgres database, and an OWASP ZAP
  daemon with the official ZAP MCP Integration add-on installed inside the same ZAP container.
- `.mcp/scripts/setup-sonarqube.sh` starts SonarQube and creates separate backend and frontend
  SonarQube projects.
- `.mcp/scripts/scan-sonarqube.sh` publishes backend and frontend analysis to local SonarQube.
- `.mcp/scripts/start-zap.sh` starts ZAP in daemon mode only. It does not run spider or active
  scans.
- `.mcp/scripts/generate-mcp-config.sh` creates or updates IBM Bob and VS Code MCP client
  configuration in the client paths those tools read.
- `.mcp/local/` is created by scripts for local-only env files and secrets. It is ignored by git.

## Secret Handling

Do not put real tokens or passwords in committed files. The committed `.mcp/.env.example` file
contains placeholders only.

Generated local files are ignored by git:

- `.mcp/local/sonarqube-compose.env`
- `.mcp/local/sonarqube-mcp.env`
- `.mcp/local/zap-mcp.env`
- `.mcp/local/mcp-env.sh`
- `.vscode/mcp.json`

`.bob/mcp.json` is committed on purpose. It must contain only non-secret values and environment
variable references such as `${env:ZAP_MCP_SECURITY_KEY}`.

## Start Local SonarQube

From the repository root:

```bash
.mcp/scripts/setup-sonarqube.sh
```

The script:

1. Creates `.mcp/local/sonarqube-compose.env` with local-only Docker credentials.
2. Starts `.mcp/docker-compose.yml` services `sonarqube-db` and `sonarqube`.
3. Waits for `http://127.0.0.1:9000`.
4. Creates these SonarQube projects when missing:
   - `risktrace-control-tower-backend`
   - `risktrace-control-tower-frontend`
5. Generates a local SonarQube user token and stores it in
   `.mcp/local/sonarqube-mcp.env`.

If you changed the local SonarQube admin password in the UI, update
`.mcp/local/sonarqube-compose.env` with:

```bash
SONARQUBE_ADMIN_USER=admin
SONARQUBE_ADMIN_PASSWORD=<your-local-password>
```

## Analyze Backend And Frontend

The local project settings are committed under `.mcp/sonarqube/` and contain no secrets.

Run both backend and frontend scans:

```bash
.mcp/scripts/scan-sonarqube.sh
```

Or run one project:

```bash
.mcp/scripts/scan-sonarqube.sh backend
.mcp/scripts/scan-sonarqube.sh frontend
```

The script reads `.mcp/local/sonarqube-mcp.env`, passes the token to
`sonarsource/sonar-scanner-cli` through environment variables, and does not write secrets to the
repository.

## Start OWASP ZAP

From the repository root:

```bash
.mcp/scripts/start-zap.sh
```

This starts the ZAP daemon at `http://127.0.0.1:8090`, installs the official ZAP MCP Integration
add-on inside that same container, and exposes the add-on at `http://127.0.0.1:8282` by default.
The API key and MCP security key are written to `.mcp/local/zap-mcp.env`. It does not start a
spider, AJAX spider, passive wait, or active scan. Any active scan must be requested explicitly by
a developer against an authorized local target.

The default target hint is:

```bash
ZAP_MCP_TARGET_URL=http://127.0.0.1:5173
```

Change it in `.mcp/local/zap-mcp.env` or export it before generating MCP config if you want the
MCP workflow to target a different local URL.

## Generate MCP Client Config

From the repository root:

```bash
.mcp/scripts/generate-mcp-config.sh
```

Generated client files:

- `.bob/mcp.json` for IBM Bob. This file is safe to commit.
- `.vscode/mcp.json` for VS Code

The generator merges these files instead of replacing them wholesale. Existing non-RiskTrace MCP
servers stay in place; RiskTrace entries are refreshed.

SonarQube, OWASP ZAP, and Sonatype Guide use launcher scripts for IBM Bob. The OWASP ZAP launcher
bridges Bob's stdio MCP process to the official ZAP MCP add-on HTTP endpoint running inside the ZAP
daemon, and reads `ZAP_MCP_SECURITY_KEY` from `.mcp/local/zap-mcp.env`. The secret value is not
written to `.bob/mcp.json`.

If you want to use direct HTTP clients, load the local ZAP MCP key:

```bash
set -a
source .mcp/local/zap-mcp.env
set +a
```

If you start IBM Bob from a desktop launcher, configure the same environment variable there.

For the least friction from a shell, source the generator instead of executing it:

```bash
source .mcp/scripts/generate-mcp-config.sh
```

That regenerates `.bob/mcp.json`, writes `.mcp/local/mcp-env.sh`, and exports the MCP environment
variables into the current shell immediately. IBM Bob's ZAP bridge can also read the key directly
from `.mcp/local/zap-mcp.env`, so desktop-launched Bob does not need `ZAP_MCP_SECURITY_KEY` in its
global environment. A normal executed script cannot mutate its parent shell, so sourced mode is the
automatic export path for clients that do need environment variables.

You can also run any command with the generated MCP environment loaded:

```bash
.mcp/scripts/with-mcp-env.sh <command>
```

SonarQube is included when `.mcp/local/sonarqube-mcp.env` exists or when `SONARQUBE_TOKEN` is
available in the shell. OWASP ZAP is always included because the generator can create the local
ZAP env file safely.

## Sonatype Guide MCP

Sonatype Guide uses `SONATYPE_GUIDE_MCP_TOKEN` from the current shell:

```bash
export SONATYPE_GUIDE_MCP_TOKEN=<your-token>
.mcp/scripts/generate-mcp-config.sh
```

The token value is not written to generated config. Keep the variable exported when launching the
MCP client so `.mcp/scripts/run-sonatype-guide-mcp.sh` can pass it to `mcp-remote`.

If `SONATYPE_GUIDE_MCP_TOKEN` is missing, generation still succeeds and preserves an existing
`sonatype-guide` entry instead of deleting it. SonarQube and OWASP ZAP configuration are still
generated when their prerequisites are met.

## Client Prerequisites

- SonarQube MCP uses Docker to run the `mcp/sonarqube` image.
- OWASP ZAP MCP is provided by the official ZAP MCP Integration add-on installed inside the ZAP
  container. IBM Bob reaches it through a local stdio bridge, but no separate ZAP MCP server
  process is required.
- OWASP ZAP and Sonatype Guide MCP use `npx -y mcp-remote` from launcher scripts.

## Stop Local Tooling

```bash
docker compose \
  --env-file .mcp/local/sonarqube-compose.env \
  --env-file .mcp/local/zap-mcp.env \
  -f .mcp/docker-compose.yml \
  down
```
