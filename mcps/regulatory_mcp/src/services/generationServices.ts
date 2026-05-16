import type { AcceptanceCriterion, Control, TestObligation } from "../schemas/control.js";
import type { EvidenceArtifact } from "../schemas/evidence.js";
import { corpusStore } from "./corpusStore.js";
import { matchControls } from "./controlMatcher.js";
import {
  DEFAULT_RECOMMENDED_ACTIONS,
  createMetadata,
  sourceReferencesForControls,
  summarizeControlReferences,
  summarizeEvidence,
  unique,
  type SourceReferenceSummary,
} from "./serviceUtils.js";

export interface ControlGenerationInput {
  text?: string;
  artifact_type?: string;
  domains?: string[];
  control_ids?: string[];
}

export interface GenerationEnvelope {
  metadata: ReturnType<typeof createMetadata>;
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

export interface AcceptanceCriteriaGenerationResult extends GenerationEnvelope {
  criteria: Array<AcceptanceCriterion & { control_id: string }>;
}

export interface DataLineageRequirementsResult extends GenerationEnvelope {
  required_fields: string[];
  lineage_flow: string[];
  acceptance_criteria: string[];
}

export interface AuditLogRequirementsResult extends GenerationEnvelope {
  required_events: Array<{
    event: string;
    fields: string[];
    no_pii: boolean;
  }>;
  security_notes: string[];
}

export interface TestObligationsResult extends GenerationEnvelope {
  obligations: Array<
    TestObligation & {
      control_id: string;
      given: string;
      when: string;
      then: string;
    }
  >;
}

export interface RwaRunEvidenceRequirementsResult extends GenerationEnvelope {
  evidence_package: Array<{
    id: string;
    description: string;
    evidence_type: EvidenceArtifact["type"];
    required_for_release: boolean;
  }>;
}

export interface ExplainControlResult extends GenerationEnvelope {
  control: Control;
  developer_tasks: string[];
  common_mistakes: string[];
  required_evidence: EvidenceArtifact[];
}

const LINEAGE_FIELDS = [
  "source_system",
  "source_record_id",
  "input_snapshot_id",
  "input_hash",
  "rule_version",
  "calculation_trace_id",
  "reporting_date",
];

const AUDIT_FIELDS = [
  "event_id",
  "timestamp",
  "actor_id",
  "correlation_id",
  "operation",
  "outcome",
  "calculation_trace_id",
];

function controlsForGeneration(input: ControlGenerationInput): Control[] {
  if (input.control_ids?.length) {
    return summarizeControlReferences(input.control_ids);
  }
  return matchControls({
    text: input.text ?? "",
    artifact_type: input.artifact_type,
    domains: input.domains,
  }).applicable_controls.map((match) => match.control);
}

function envelope(controls: Control[]): GenerationEnvelope {
  return {
    metadata: createMetadata("medium"),
    source_references: sourceReferencesForControls(controls),
    recommended_actions: DEFAULT_RECOMMENDED_ACTIONS,
  };
}

export function generateAcceptanceCriteria(
  input: ControlGenerationInput
): AcceptanceCriteriaGenerationResult {
  const controls = controlsForGeneration(input);
  const criteriaByDescription = new Map<string, AcceptanceCriterion & { control_id: string }>();

  for (const control of controls) {
    for (const criterion of control.acceptance_criteria) {
      const key = criterion.description.toLowerCase();
      if (!criteriaByDescription.has(key)) {
        criteriaByDescription.set(key, { ...criterion, control_id: control.id });
      }
    }
  }

  return {
    ...envelope(controls),
    criteria: [...criteriaByDescription.values()].sort((a, b) =>
      `${a.control_id}:${a.id}`.localeCompare(`${b.control_id}:${b.id}`)
    ),
  };
}

export function generateDataLineageRequirements(
  input: ControlGenerationInput = {}
): DataLineageRequirementsResult {
  const controls = controlsForGeneration({
    ...input,
    control_ids: input.control_ids ?? ["RWA-DATA-001", "RWA-AUDIT-001"],
  });
  return {
    ...envelope(controls),
    required_fields: LINEAGE_FIELDS,
    lineage_flow: [
      "Capture source system and source record id at ingestion.",
      "Create immutable input snapshot and input hash before validation.",
      "Link approved rule version and regulation reference before calculation.",
      "Propagate calculation trace id through results, report exports, and audit logs.",
      "Store reporting date with all generated RWA outputs.",
    ],
    acceptance_criteria: [
      "Every RWA result can be traced back to source system, input snapshot, rule version, and reporting date.",
      "Input hashes are reproducible for the same input snapshot.",
      "Lineage report is retained with release evidence.",
    ],
  };
}

export function generateAuditLogRequirements(
  input: ControlGenerationInput = {}
): AuditLogRequirementsResult {
  const controls = controlsForGeneration({
    ...input,
    control_ids: input.control_ids ?? ["RWA-AUDIT-001", "SEC-LOG-001"],
  });
  return {
    ...envelope(controls),
    required_events: ["upload", "validate", "calculate", "export"].map((event) => ({
      event,
      fields: AUDIT_FIELDS,
      no_pii: true,
    })),
    security_notes: [
      "Do not log PII, raw customer identifiers, uploaded file contents, or exposure-level personal data.",
      "Use correlation ids, actor ids, and redacted business identifiers for troubleshooting.",
      "Protect audit logs from unauthorized modification and retain them according to policy.",
    ],
  };
}

export function generateTestObligations(
  input: ControlGenerationInput
): TestObligationsResult {
  const controls = controlsForGeneration(input);
  const obligations = controls.flatMap((control) =>
    control.test_obligations.map((obligation) => ({
      ...obligation,
      control_id: control.id,
      given: `Given ${control.title} is required for the change`,
      when: `When ${obligation.description.toLowerCase()}`,
      then: `Then the test must pass before ${obligation.blocking ? "release" : "approval"}.`,
    }))
  );

  return {
    ...envelope(controls),
    obligations,
  };
}

export function generateRwaRunEvidenceRequirements(
  input: ControlGenerationInput = {}
): RwaRunEvidenceRequirementsResult {
  const controls = controlsForGeneration({
    ...input,
    control_ids: input.control_ids ?? [
      "RWA-CALC-001",
      "RWA-DATA-001",
      "RWA-AUDIT-001",
      "RWA-RECON-001",
      "REL-EVID-001",
    ],
  });

  return {
    ...envelope(controls),
    evidence_package: [
      {
        id: "input_snapshot",
        description: "Immutable source input snapshot used for the RWA run.",
        evidence_type: "documentation",
        required_for_release: true,
      },
      {
        id: "validation_report",
        description: "Validation and data-quality result for the input snapshot.",
        evidence_type: "data_quality_report",
        required_for_release: true,
      },
      {
        id: "applied_rules",
        description: "Applied regulatory rules and jurisdiction overlays.",
        evidence_type: "change_log",
        required_for_release: true,
      },
      {
        id: "rule_version",
        description: "Approved rule version and effective date used for calculation.",
        evidence_type: "approval_record",
        required_for_release: true,
      },
      {
        id: "results",
        description: "RWA calculation outputs and calculation trace references.",
        evidence_type: "calculation_trace",
        required_for_release: true,
      },
      {
        id: "lineage_report",
        description: "Lineage report linking results back to source system and input hash.",
        evidence_type: "documentation",
        required_for_release: true,
      },
      {
        id: "audit_extract",
        description: "Audit extract for upload, validate, calculate, and export events.",
        evidence_type: "audit_log",
        required_for_release: true,
      },
      {
        id: "reconciliation_summary",
        description: "Reconciliation between expected, prior, and generated outputs.",
        evidence_type: "reconciliation_report",
        required_for_release: true,
      },
    ],
  };
}

export function explainControl(controlId: string): ExplainControlResult {
  const control = corpusStore.getControl(controlId);
  if (!control) {
    throw new Error(`Unknown control: ${controlId}`);
  }

  return {
    ...envelope([control]),
    control,
    developer_tasks: unique([
      ...control.implementation_hints.map((hint) => hint.description),
      ...control.acceptance_criteria.map((criterion) => criterion.description),
      ...control.test_obligations.map((obligation) => obligation.description),
    ]),
    common_mistakes: control.anti_patterns.map(
      (antiPattern) =>
        `${antiPattern.description}. Risk: ${antiPattern.risk}. Use instead: ${antiPattern.alternative}.`
    ),
    required_evidence: summarizeEvidence([control]),
  };
}
