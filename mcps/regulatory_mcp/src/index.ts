#!/usr/bin/env node

import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { createServer } from './server.js';

/**
 * Main entry point for the Regulatory MCP Server
 */
async function main(): Promise<void> {
  const server = createServer();
  const transport = new StdioServerTransport();

  // Log startup to stderr (stdout is reserved for MCP protocol)
  console.error('[regulatory-mcp] Starting MCP server...');
  console.error('[regulatory-mcp] Server name: regulatory-mcp');
  console.error('[regulatory-mcp] Server version: 0.1.0');
  console.error('[regulatory-mcp] Transport: STDIO');
  console.error('[regulatory-mcp] Ready for connections');

  await server.connect(transport);
}

main().catch((error) => {
  console.error('[regulatory-mcp] Fatal error:', error);
  process.exit(1);
});

// Made with Bob
