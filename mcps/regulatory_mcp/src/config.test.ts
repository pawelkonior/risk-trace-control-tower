import { describe, it, expect } from 'vitest';
import { getConfig } from './config.js';

describe('config', () => {
  it('should return valid server configuration', () => {
    const config = getConfig();

    expect(config).toBeDefined();
    expect(config.serverName).toBe('regulatory-mcp');
    expect(config.serverVersion).toBe('0.1.0');
    expect(config.projectRoot).toBeDefined();
    expect(config.dataDir).toBeDefined();
    expect(typeof config.projectRoot).toBe('string');
    expect(typeof config.dataDir).toBe('string');
  });

  it('should have consistent paths', () => {
    const config = getConfig();

    expect(config.dataDir).toContain(config.projectRoot);
  });
});

// Made with Bob
