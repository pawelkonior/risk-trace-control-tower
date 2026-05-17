# Regulatory MCP Server

A Model Context Protocol (MCP) server for Bank Regulatory Controls and RWA Control Tower.

## Overview

This is a local, deterministic STDIO MCP server that provides tools and resources for regulatory compliance and risk-weighted asset (RWA) calculations. The server is designed to be:

- **Local-first**: All operations run locally without external API calls
- **Deterministic**: Consistent, reproducible results
- **Privacy-focused**: No data sent to external services

## Requirements

- Node.js 20 or higher
- npm

## Installation

```bash
npm install
```

## Development

```bash
# Build the project
npm run build

# Run in development mode with hot reload
npm run dev

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Start the server
npm start
# or
node build/index.js
```

## Project Structure

```
mcps/regulatory_mcp/
├── src/
│   ├── index.ts       # Main entry point with STDIO transport
│   ├── server.ts      # MCP server factory and tool handlers
│   ├── config.ts      # Server configuration
│   ├── schemas/       # Zod schemas and TypeScript types
│   ├── services/      # Corpus loader and store
│   └── *.test.ts      # Test files
├── data/
│   ├── regulations/   # Curated regulatory corpus
│   ├── controls/      # Engineering control library
│   └── mappings/      # Keyword, artifact, and domain mappings
├── build/             # Compiled JavaScript output
├── package.json       # Project dependencies and scripts
├── tsconfig.json      # TypeScript configuration
└── vitest.config.ts   # Test configuration
```

## Available Tools

The server exposes 15 MVP read-only tools:

- `health_check`
- `get_regulatory_profile`
- `search_regulations`
- `match_controls`
- `review_feature_description`
- `review_architecture_text`
- `review_code_diff`
- `generate_acceptance_criteria`
- `generate_data_lineage_requirements`
- `generate_audit_log_requirements`
- `generate_test_obligations`
- `assess_release_readiness`
- `generate_regulatory_mapping_report`
- `generate_rwa_run_evidence_requirements`
- `explain_control`

All tools return `content` and `structuredContent`, include input/output schemas, and are annotated as read-only/idempotent.

## Resources and Prompts

Resources:

- `regulations://index`
- `regulations://<REGULATION_ID>`
- `controls://index`
- `controls://domain/<DOMAIN>`
- `examples://feature`
- `examples://architecture`
- `examples://code_diff`
- `examples://release_evidence`

Prompts:

- `feature_review`
- `architecture_review`
- `code_review`
- `data_lineage_design`
- `audit_log_design`
- `regulatory_mapping_report`

## Configuration

The server configuration is managed in `src/config.ts` and includes:

- `projectRoot`: Root directory of the project
- `dataDir`: Directory for local data storage
- `serverName`: Server identifier
- `serverVersion`: Current version

## Docker

Build and run the MCP container from this directory:

```bash
docker build -t bank-regulatory-controls-mcp .
docker run --rm -i bank-regulatory-controls-mcp
```

The image uses a Node 20 multi-stage build, copies `build/` and `data/`, and starts the STDIO MCP server with:

```bash
node build/index.js
```

It does not expose an HTTP endpoint.

## Docker Compose

From the parent `mcps/` directory:

```bash
docker compose build bank-regulatory-controls-mcp
docker compose run --rm -T bank-regulatory-controls-mcp
```

For clients that support command plus args, a Compose-based command can be configured as:

```json
{
  "command": "docker",
  "args": [
    "compose",
    "-f",
    "mcps/docker-compose.yml",
    "run",
    "--rm",
    "-T",
    "bank-regulatory-controls-mcp"
  ]
}
```

If an MCP client cannot keep `docker compose run` attached as a long-running STDIO process, use the local fallback:

```bash
cd mcps/regulatory_mcp
npm run build
node build/index.js
```

## Bob Integration

Repository-level assets are provided for regulated RWA workflows:

- `.bob/mcp.example.json` provides a tracked `bankRegulatoryControls` template
- local `.bob/mcp.json` can register `bankRegulatoryControls` for Bob
- `.bob/custom_modes.yaml` defines gated RWA workflows and allowed tools

Bob instructions require confirmation before Jira, GitHub, or Confluence writes and block RWA work missing rule versioning, lineage, audit logs, tests, or evidence.

### Bob Usage Instructions

#### Regulated Jira Story

Before writing or updating Jira content for RWA, call `bankRegulatoryControls.match_controls` and `bankRegulatoryControls.generate_acceptance_criteria`.

Include rule versioning, data lineage, audit events, regulatory test obligations, release evidence, source references, and a human review note. Ask for confirmation before writing to Jira.

#### Architecture Review

Before approving architecture for RWA, call `bankRegulatoryControls.review_architecture_text`.

Block the output when the architecture hardcodes risk weights, lacks a rule registry, misses lineage/audit/data-quality/reporting-date controls, or omits resilience requirements.

#### Code Review Gate

Before GitHub PR output for RWA code, call `bankRegulatoryControls.review_code_diff`.

Block hardcoded risk weights, embedded exposure classification, missing traceability fields, PII-like logging, input validation gaps, and rounding without policy.

#### Release Evidence Gate

Before release notes or approval, call `bankRegulatoryControls.assess_release_readiness` and `bankRegulatoryControls.generate_regulatory_mapping_report`.

Do not claim legal compliance. State that qualified compliance, legal, risk, or audit review is required.

### Bob Demo Prompts

#### Health Check

Call `bankRegulatoryControls.health_check` with `include_corpus: true` and summarize the corpus counts.

#### Feature Review

Review this feature before Jira output:

```text
Build CSV upload for exposure data and RWA calculation. The story should include validation, lineage, rule versioning, audit logs, tests, and release evidence.
```

Use `bankRegulatoryControls.review_feature_description`, then generate acceptance criteria.

#### Code Review

Review this diff before GitHub output:

```diff
+ const riskWeight = 0.35;
+ logger.info(customer.email);
+ export function calculateRwa(exposure) {
+   return exposure.amount * riskWeight;
+ }
```

Use `bankRegulatoryControls.review_code_diff` and report blocking findings.

#### Release Report

Generate a regulatory mapping report for RWA CSV upload and calculation with implemented controls and evidence. Include the human review note and do not claim legal compliance.

## Regulatory Corpus

### ⚠️ Important Disclaimer

The `data/` directory contains a **curated local engineering corpus** for RWA control mapping. This is **NOT**:
- A legal research engine
- A source of legal advice
- A regulatory compliance certification tool
- A substitute for qualified compliance review

**All regulatory mappings, controls, evidence requirements, and release readiness decisions MUST be reviewed by qualified compliance, legal, or risk specialists before production use.**

### Corpus Structure

The corpus consists of three main components:

#### 1. Regulations (`data/regulations/`)
Curated regulatory records covering:
- CRR3 / CRD6 (EU Capital Requirements)
- EBA Reporting Framework 4.0
- BCBS 239 (Data Aggregation and Risk Reporting)
- DORA (Digital Operational Resilience Act)
- EBA ICT and Security Risk Management
- GDPR (General Data Protection Regulation)
- Internal SDLC, Rule Governance, and Audit Evidence Policies

Each regulation includes:
- Key requirements and engineering implications
- Applicable domains and jurisdictions
- Source references and effective dates
- Human review flags

#### 2. Controls (`data/controls/`)
Engineering control library with 15+ controls covering:
- RWA calculation accuracy and rule governance
- Data quality and audit logging
- Reporting and reconciliation
- Security (input validation, logging, access control)
- ICT resilience and testing
- Evidence collection and architecture decisions
- Performance monitoring

Each control specifies:
- Severity level and regulatory basis
- Required evidence artifacts
- Acceptance criteria and test obligations
- Implementation hints and anti-patterns
- Bob actions for automated assistance

#### 3. Mappings (`data/mappings/`)
Referential integrity validated mappings:
- Keywords to controls
- Artifact types to controls
- Regulatory domains to regulations

All mappings are validated at load time to ensure no dangling references.

## Testing

The project uses Vitest for testing. Tests are located alongside source files with the `.test.ts` extension.

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch
```

Test coverage includes:
- Schema validation (13 tests)
- Corpus loading and validation (25 tests)
- Corpus store queries and caching (32 tests)
- Regulation search, control matching, review, generation, release readiness, report, resource, prompt, and in-memory MCP tool coverage
- Configuration (2 tests)

### Docker Smoke Test

A comprehensive Docker smoke test script is provided to verify the containerized MCP server:

```bash
# Run Docker smoke test
./test-docker-smoke.sh
```

The smoke test validates:
- ✓ Docker image builds successfully
- ✓ Container starts and runs
- ✓ Corpus loads (≥9 regulations, ≥15 controls)
- ✓ MCP server starts without errors
- ✓ Container stops cleanly

The script uses `docker compose` and checks container logs for:
- Successful corpus loading with expected counts
- MCP server startup confirmation
- Absence of critical errors

**Requirements:**
- Docker and Docker Compose installed
- Run from `mcps/regulatory_mcp/` directory
- Uses `../docker-compose.yml` configuration

**Exit codes:**
- `0`: All checks passed
- `1`: One or more checks failed (see output for details)

## License

UNLICENSED - Internal use only

## Notes

- This server does NOT make external API calls to Jira, GitHub, SonarQube, or LLMs
- All operations are deterministic and local
- The server uses STDIO transport for MCP communication
- Startup logs are written to stderr (stdout is reserved for MCP protocol)
