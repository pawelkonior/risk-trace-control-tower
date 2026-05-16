# RiskTrace Control Tower

RiskTrace Control Tower is a monorepo with a Python backend, React/Vite frontend, and local
Docker Compose runtime under `apps/`.

## Local MCP Tooling

Repository-local MCP-assisted quality and security tooling lives in `.mcp/`. IBM Bob reads the
committed `.bob/mcp.json` directly; there is no generated MCP client configuration.

Create local MCP secrets once:

```bash
cp .mcp/.env.example .mcp/.env
```

Edit `.mcp/.env` with local SonarQube, ZAP, and optional Sonatype values. The file is ignored by
git.

Start and initialize local SonarQube:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml up -d sonarqube
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml --profile setup run --rm -T sonarqube-init
```

Start OWASP ZAP:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml up -d zap
```

Run SonarQube analysis when needed:

```bash
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
docker compose --env-file .mcp/.env -f .mcp/docker-compose.yml --profile scan run --rm -T sonar-scan-frontend
```

See `.mcp/README.md` for the full workflow.
