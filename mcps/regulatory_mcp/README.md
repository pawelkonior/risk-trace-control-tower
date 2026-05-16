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
│   └── *.test.ts      # Test files
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

## Testing

The project uses Vitest for testing. Tests are located alongside source files with the `.test.ts` extension.

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch
```

## License

UNLICENSED - Internal use only

## Notes

- This server does NOT make external API calls to Jira, GitHub, SonarQube, or LLMs
- All operations are deterministic and local
- The server uses STDIO transport for MCP communication
- Startup logs are written to stderr (stdout is reserved for MCP protocol)