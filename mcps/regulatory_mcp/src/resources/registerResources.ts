import { readFileSync } from "fs";
import { join } from "path";
import type { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { getConfig } from "../config.js";
import { corpusStore } from "../services/corpusStore.js";

interface ResourceDefinition {
  uri: string;
  name: string;
  title: string;
  description: string;
  mimeType: string;
  read: () => string;
}

const EXAMPLE_RESOURCES = [
  {
    uri: "examples://feature",
    name: "feature-example",
    title: "Feature Review Example",
    file: "feature-rwa-csv-upload.md",
  },
  {
    uri: "examples://architecture",
    name: "architecture-example",
    title: "Architecture Review Example",
    file: "architecture-rwa-service.md",
  },
  {
    uri: "examples://code_diff",
    name: "code-diff-example",
    title: "Code Diff Review Example",
    file: "code-diff-risk-weight.patch",
  },
  {
    uri: "examples://release_evidence",
    name: "release-evidence-example",
    title: "Release Evidence Example",
    file: "release-evidence.json",
  },
];

function json(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

export function listResourceDefinitions(): ResourceDefinition[] {
  const config = getConfig();
  const exampleDir = join(config.dataDir, "examples");
  return [
    {
      uri: "regulations://index",
      name: "regulations-index",
      title: "Regulations Index",
      description: "List of curated regulatory records.",
      mimeType: "application/json",
      read: () =>
        json(
          corpusStore.getRegulations().map((regulation) => ({
            id: regulation.id,
            title: regulation.title,
            jurisdiction: regulation.jurisdiction,
            domains: regulation.domains,
          }))
        ),
    },
    ...corpusStore.getRegulations().map((regulation) => ({
      uri: `regulations://${regulation.id}`,
      name: `regulation-${regulation.id.toLowerCase()}`,
      title: regulation.title,
      description: `Regulation detail for ${regulation.id}.`,
      mimeType: "application/json",
      read: () => json(regulation),
    })),
    {
      uri: "controls://index",
      name: "controls-index",
      title: "Controls Index",
      description: "List of engineering controls.",
      mimeType: "application/json",
      read: () =>
        json(
          corpusStore.getControls().map((control) => ({
            id: control.id,
            title: control.title,
            severity: control.severity,
            domains: control.domains,
          }))
        ),
    },
    ...Object.keys(corpusStore.getCorpus().domainMappings.mappings).map((domain) => ({
      uri: `controls://domain/${domain}`,
      name: `controls-${domain}`,
      title: `Controls for ${domain}`,
      description: `Controls mapped to regulatory domain ${domain}.`,
      mimeType: "application/json",
      read: () => json(corpusStore.getControlsByDomain(domain)),
    })),
    ...EXAMPLE_RESOURCES.map((example) => ({
      uri: example.uri,
      name: example.name,
      title: example.title,
      description: `Example input artifact for ${example.title}.`,
      mimeType: example.file.endsWith(".json") ? "application/json" : "text/plain",
      read: () => readFileSync(join(exampleDir, example.file), "utf-8"),
    })),
  ];
}

export function registerResources(server: Server): void {
  server.setRequestHandler(ListResourcesRequestSchema, async () => ({
    resources: listResourceDefinitions().map((resource) => ({
      uri: resource.uri,
      name: resource.name,
      title: resource.title,
      description: resource.description,
      mimeType: resource.mimeType,
    })),
  }));

  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const resource = listResourceDefinitions().find(
      (item) => item.uri === request.params.uri
    );
    if (!resource) {
      throw new Error(`Unknown resource: ${request.params.uri}`);
    }
    return {
      contents: [
        {
          uri: resource.uri,
          mimeType: resource.mimeType,
          text: resource.read(),
        },
      ],
    };
  });
}
