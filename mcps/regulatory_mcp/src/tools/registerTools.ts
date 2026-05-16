import type { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import type { ToolAnnotations } from "@modelcontextprotocol/sdk/types.js";
import type { getConfig } from "../config.js";
import { corpusStore } from "../services/corpusStore.js";
import { matchControls } from "../services/controlMatcher.js";
import {
  explainControl,
  generateAcceptanceCriteria,
  generateAuditLogRequirements,
  generateDataLineageRequirements,
  generateRwaRunEvidenceRequirements,
  generateTestObligations,
} from "../services/generationServices.js";
import { generateRegulatoryMappingReport } from "../services/reportGenerator.js";
import { assessReleaseReadiness } from "../services/releaseReadiness.js";
import { searchRegulations } from "../services/regulationSearch.js";
import {
  reviewArchitectureText,
  reviewCodeDiff,
  reviewFeatureDescription,
} from "../services/reviewServices.js";
import { createMetadata } from "../services/serviceUtils.js";

type JsonObject = Record<string, unknown>;
type Config = ReturnType<typeof getConfig>;

interface ToolDefinition {
  name: string;
  title: string;
  description: string;
  inputSchema: JsonObject;
  outputSchema: JsonObject;
  annotations: ToolAnnotations;
  handler: (args: JsonObject, config: Config) => JsonObject;
}

const READ_ONLY_ANNOTATIONS: ToolAnnotations = {
  readOnlyHint: true,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: false,
};

const stringProperty = { type: "string" };
const numberProperty = { type: "number" };
const booleanProperty = { type: "boolean" };
const stringArrayProperty = {
  type: "array",
  items: { type: "string" },
};
const objectArrayProperty = {
  type: "array",
  items: { type: "object" },
};

function objectSchema(
  properties: Record<string, object> = {},
  required: string[] = []
): JsonObject {
  return {
    type: "object",
    properties,
    required,
    additionalProperties: false,
  };
}

const genericOutputSchema = objectSchema({
  metadata: { type: "object" },
  source_references: objectArrayProperty,
  recommended_actions: stringArrayProperty,
});

function asStringArray(value: unknown): string[] | undefined {
  if (!Array.isArray(value)) {
    return undefined;
  }
  return value.filter((item): item is string => typeof item === "string");
}

function asJsonObject(value: unknown): JsonObject {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as JsonObject)
    : {};
}

function asJsonObjectArray(value: unknown): JsonObject[] | undefined {
  if (!Array.isArray(value)) {
    return undefined;
  }
  return value.map(asJsonObject);
}

function asString(value: unknown, fallback = ""): string {
  return typeof value === "string" ? value : fallback;
}

function asNumber(value: unknown): number | undefined {
  return typeof value === "number" ? value : undefined;
}

function asBoolean(value: unknown): boolean | undefined {
  return typeof value === "boolean" ? value : undefined;
}

function toolResult(structuredContent: JsonObject) {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(structuredContent, null, 2),
      },
    ],
    structuredContent,
  };
}

function healthCheck(args: JsonObject, config: Config): JsonObject {
  const includeCorpus = asBoolean(args.include_corpus) ?? false;
  return {
    status: "ok",
    metadata: createMetadata("high"),
    server: {
      name: config.serverName,
      version: config.serverVersion,
      transport: "stdio",
      projectRoot: config.projectRoot,
      dataDir: config.dataDir,
    },
    corpus: includeCorpus ? corpusStore.getStats() : undefined,
    source_references: [],
    recommended_actions: [
      "Use bankRegulatoryControls before regulated Jira, GitHub, or release output.",
    ],
  };
}

function regulatoryProfile(args: JsonObject): JsonObject {
  const domains = asStringArray(args.domains);
  const jurisdiction = asString(args.jurisdiction);
  const regulations = jurisdiction
    ? corpusStore.getRegulationsByJurisdiction(jurisdiction)
    : domains?.length
      ? domains.flatMap((domain) => corpusStore.getRegulationsByDomain(domain))
      : corpusStore.getRegulations();
  const controls = domains?.length
    ? domains.flatMap((domain) => corpusStore.getControlsByDomain(domain))
    : corpusStore.getControls();

  return {
    metadata: createMetadata("medium", jurisdiction || "GLOBAL"),
    stats: corpusStore.getStats(),
    regulations: [...new Map(regulations.map((item) => [item.id, item])).values()],
    controls: [...new Map(controls.map((item) => [item.id, item])).values()],
    source_references: [],
    recommended_actions: [
      "Use search_regulations and match_controls for artifact-specific output.",
    ],
  };
}

const tools: ToolDefinition[] = [
  {
    name: "health_check",
    title: "Health Check",
    description: "Return MCP server health, metadata, and optional corpus stats.",
    inputSchema: objectSchema({ include_corpus: booleanProperty }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Health Check" },
    handler: healthCheck,
  },
  {
    name: "get_regulatory_profile",
    title: "Regulatory Profile",
    description: "Return regulations, controls, and corpus stats filtered by domain or jurisdiction.",
    inputSchema: objectSchema({
      domains: stringArrayProperty,
      jurisdiction: stringProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Regulatory Profile" },
    handler: regulatoryProfile,
  },
  {
    name: "search_regulations",
    title: "Search Regulations",
    description: "Search regulations by query, domain, jurisdiction, and applies-to filters.",
    inputSchema: objectSchema({
      query: stringProperty,
      domains: stringArrayProperty,
      applies_to: stringArrayProperty,
      jurisdiction: stringProperty,
      include_internal_policies: booleanProperty,
      limit: numberProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Search Regulations" },
    handler: (args) =>
      searchRegulations({
        query: asString(args.query),
        domains: asStringArray(args.domains),
        applies_to: asStringArray(args.applies_to) as never,
        jurisdiction: asString(args.jurisdiction) || undefined,
        include_internal_policies: asBoolean(args.include_internal_policies),
        limit: asNumber(args.limit),
      }) as unknown as JsonObject,
  },
  {
    name: "match_controls",
    title: "Match Controls",
    description: "Match engineering controls for feature text, architecture text, code diffs, or release artifacts.",
    inputSchema: objectSchema({
      text: stringProperty,
      artifact_type: stringProperty,
      domains: stringArrayProperty,
      explicit_control_ids: stringArrayProperty,
      excluded_control_ids: stringArrayProperty,
      limit: numberProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Match Controls" },
    handler: (args) =>
      matchControls({
        text: asString(args.text),
        artifact_type: asString(args.artifact_type) || undefined,
        domains: asStringArray(args.domains),
        explicit_control_ids: asStringArray(args.explicit_control_ids),
        excluded_control_ids: asStringArray(args.excluded_control_ids),
        limit: asNumber(args.limit),
      }) as unknown as JsonObject,
  },
  {
    name: "review_feature_description",
    title: "Review Feature Description",
    description: "Review a regulated feature description for missing RWA controls and evidence.",
    inputSchema: objectSchema(
      {
        description: stringProperty,
        domains: stringArrayProperty,
      },
      ["description"]
    ),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Review Feature Description" },
    handler: (args) =>
      reviewFeatureDescription({
        description: asString(args.description),
        domains: asStringArray(args.domains),
      }) as unknown as JsonObject,
  },
  {
    name: "review_architecture_text",
    title: "Review Architecture Text",
    description: "Review architecture text for regulatory architecture gaps.",
    inputSchema: objectSchema(
      {
        architecture_text: stringProperty,
        domains: stringArrayProperty,
      },
      ["architecture_text"]
    ),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Review Architecture Text" },
    handler: (args) =>
      reviewArchitectureText({
        architecture_text: asString(args.architecture_text),
        domains: asStringArray(args.domains),
      }) as unknown as JsonObject,
  },
  {
    name: "review_code_diff",
    title: "Review Code Diff",
    description: "Review code diff text for hardcoded RWA logic, missing traceability, PII logging, and validation gaps.",
    inputSchema: objectSchema(
      {
        diff: stringProperty,
        file_path: stringProperty,
      },
      ["diff"]
    ),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Review Code Diff" },
    handler: (args) =>
      reviewCodeDiff({
        diff: asString(args.diff),
        file_path: asString(args.file_path) || undefined,
      }) as unknown as JsonObject,
  },
  {
    name: "generate_acceptance_criteria",
    title: "Generate Acceptance Criteria",
    description: "Generate deduplicated acceptance criteria mapped to controls.",
    inputSchema: objectSchema({
      text: stringProperty,
      artifact_type: stringProperty,
      domains: stringArrayProperty,
      control_ids: stringArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Generate Acceptance Criteria" },
    handler: (args) =>
      generateAcceptanceCriteria({
        text: asString(args.text),
        artifact_type: asString(args.artifact_type) || undefined,
        domains: asStringArray(args.domains),
        control_ids: asStringArray(args.control_ids),
      }) as unknown as JsonObject,
  },
  {
    name: "generate_data_lineage_requirements",
    title: "Generate Data Lineage Requirements",
    description: "Generate RWA lineage fields, flow, and acceptance criteria.",
    inputSchema: objectSchema({
      text: stringProperty,
      control_ids: stringArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Generate Data Lineage Requirements" },
    handler: (args) =>
      generateDataLineageRequirements({
        text: asString(args.text),
        control_ids: asStringArray(args.control_ids),
      }) as unknown as JsonObject,
  },
  {
    name: "generate_audit_log_requirements",
    title: "Generate Audit Log Requirements",
    description: "Generate audit event requirements and secure logging notes.",
    inputSchema: objectSchema({
      text: stringProperty,
      control_ids: stringArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Generate Audit Log Requirements" },
    handler: (args) =>
      generateAuditLogRequirements({
        text: asString(args.text),
        control_ids: asStringArray(args.control_ids),
      }) as unknown as JsonObject,
  },
  {
    name: "generate_test_obligations",
    title: "Generate Test Obligations",
    description: "Generate Given/When/Then regulatory test obligations.",
    inputSchema: objectSchema({
      text: stringProperty,
      artifact_type: stringProperty,
      domains: stringArrayProperty,
      control_ids: stringArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Generate Test Obligations" },
    handler: (args) =>
      generateTestObligations({
        text: asString(args.text),
        artifact_type: asString(args.artifact_type) || undefined,
        domains: asStringArray(args.domains),
        control_ids: asStringArray(args.control_ids),
      }) as unknown as JsonObject,
  },
  {
    name: "assess_release_readiness",
    title: "Assess Release Readiness",
    description: "Assess RWA release readiness from implemented controls, evidence, and known findings.",
    inputSchema: objectSchema({
      implemented_control_ids: stringArrayProperty,
      evidence: objectArrayProperty,
      known_findings: objectArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Assess Release Readiness" },
    handler: (args) =>
      assessReleaseReadiness({
        implemented_control_ids: asStringArray(args.implemented_control_ids),
        evidence: asJsonObjectArray(args.evidence) as never,
        known_findings: asJsonObjectArray(args.known_findings) as never,
      }) as unknown as JsonObject,
  },
  {
    name: "generate_regulatory_mapping_report",
    title: "Generate Regulatory Mapping Report",
    description: "Generate a Markdown regulatory mapping report with controls, evidence, tests, Bob actions, and human review note.",
    inputSchema: objectSchema({
      title: stringProperty,
      feature_text: stringProperty,
      domains: stringArrayProperty,
      artifact_type: stringProperty,
      implemented_control_ids: stringArrayProperty,
      evidence: objectArrayProperty,
      known_findings: objectArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Generate Regulatory Mapping Report" },
    handler: (args) =>
      generateRegulatoryMappingReport({
        title: asString(args.title) || undefined,
        feature_text: asString(args.feature_text),
        domains: asStringArray(args.domains),
        artifact_type: asString(args.artifact_type) || undefined,
        implemented_control_ids: asStringArray(args.implemented_control_ids),
        evidence: asJsonObjectArray(args.evidence) as never,
        known_findings: asJsonObjectArray(args.known_findings) as never,
      }) as unknown as JsonObject,
  },
  {
    name: "generate_rwa_run_evidence_requirements",
    title: "Generate RWA Run Evidence Requirements",
    description: "Generate the required evidence package for an RWA calculation run.",
    inputSchema: objectSchema({
      text: stringProperty,
      control_ids: stringArrayProperty,
    }),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Generate RWA Run Evidence Requirements" },
    handler: (args) =>
      generateRwaRunEvidenceRequirements({
        text: asString(args.text),
        control_ids: asStringArray(args.control_ids),
      }) as unknown as JsonObject,
  },
  {
    name: "explain_control",
    title: "Explain Control",
    description: "Explain a control with developer tasks, common mistakes, evidence, and source references.",
    inputSchema: objectSchema({ control_id: stringProperty }, ["control_id"]),
    outputSchema: genericOutputSchema,
    annotations: { ...READ_ONLY_ANNOTATIONS, title: "Explain Control" },
    handler: (args) => explainControl(asString(args.control_id)) as unknown as JsonObject,
  },
];

export function getToolDefinitions(): ToolDefinition[] {
  return tools;
}

export function registerTools(server: Server, config: Config): void {
  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: tools.map((tool) => ({
      name: tool.name,
      title: tool.title,
      description: tool.description,
      inputSchema: tool.inputSchema,
      outputSchema: tool.outputSchema,
      annotations: tool.annotations,
    })),
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const tool = tools.find((item) => item.name === request.params.name);
    if (!tool) {
      throw new Error(`Unknown tool: ${request.params.name}`);
    }
    return toolResult(tool.handler(asJsonObject(request.params.arguments), config));
  });
}
