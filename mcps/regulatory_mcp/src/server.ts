import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { getConfig } from './config.js';
import { registerPrompts } from './resources/registerPrompts.js';
import { registerResources } from './resources/registerResources.js';
import { registerTools } from './tools/registerTools.js';

/**
 * Create and configure the MCP server
 */
export function createServer(): Server {
  const config = getConfig();
  
  const server = new Server(
    {
      name: config.serverName,
      version: config.serverVersion,
    },
    {
      capabilities: {
        tools: {},
        resources: {},
        prompts: {},
      },
    }
  );

  registerTools(server, config);
  registerResources(server);
  registerPrompts(server);

  return server;
}

// Made with Bob
