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

### get_server_info

Get information about the regulatory MCP server.

**Input:** None

**Output:** JSON object with server metadata including name, version, project root, and data directory.

## Configuration

The server configuration is managed in `src/config.ts` and includes:

- `projectRoot`: Root directory of the project
- `dataDir`: Directory for local data storage
- `serverName`: Server identifier
- `serverVersion`: Current version

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
- Configuration (2 tests)

## License

UNLICENSED - Internal use only

## Notes

- This server does NOT make external API calls to Jira, GitHub, SonarQube, or LLMs
- All operations are deterministic and local
- The server uses STDIO transport for MCP communication
- Startup logs are written to stderr (stdout is reserved for MCP protocol)
