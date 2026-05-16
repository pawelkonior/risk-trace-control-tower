# RiskTrace Control Tower

RiskTrace Control Tower is a monorepo with a Python backend, React/Vite frontend, and local
Docker Compose runtime under `apps/`.

## Local MCP Tooling

Repository-local MCP-assisted quality and security tooling lives in `mcps/`. IBM Bob reads the
local `.bob/mcp.json`; copy it from the committed `.bob/mcp.example.json` template.

Create local MCP secrets once:

```bash
cp mcps/.env.example mcps/.env
cp .bob/mcp.example.json .bob/mcp.json
```

Edit `mcps/.env` with local SonarQube, ZAP, and optional Sonatype values. The file is ignored by
git.

Start and initialize local SonarQube:

```bash
docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d sonarqube
docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile setup run --rm -T sonarqube-init
```

Start OWASP ZAP:

```bash
docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d zap
```

Run SonarQube analysis when needed:

```bash
docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-frontend
```

See `mcps/README.md` for the full workflow.
