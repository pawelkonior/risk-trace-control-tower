import type { Control } from "../schemas/control.js";
import type { Finding, ImpactArea } from "../schemas/finding.js";
import { corpusStore } from "./corpusStore.js";
import { matchControls } from "./controlMatcher.js";
import {
  DEFAULT_RECOMMENDED_ACTIONS,
  createMetadata,
  makeServiceEnvelope,
  normalizeText,
  sourceReferencesForControls,
  summarizeControlReferences,
  textIncludesAny,
  unique,
  type SourceReferenceSummary,
} from "./serviceUtils.js";

export interface FeatureReviewInput {
  description: string;
  domains?: string[];
}

export interface ArchitectureReviewInput {
  architecture_text: string;
  domains?: string[];
}

export interface CodeDiffReviewInput {
  diff: string;
  file_path?: string;
}

export interface ReviewResult {
  review_type: "feature" | "architecture" | "code_diff";
  readiness_status: "ready" | "needs_work" | "not_ready";
  metadata: ReturnType<typeof createMetadata>;
  findings: Finding[];
  applicable_controls: Array<{
    id: string;
    title: string;
    severity: Control["severity"];
  }>;
  acceptance_criteria: string[];
  subtasks: string[];
  bob_actions: string[];
  control_summary: string[];
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

const TRACEABILITY_FIELDS = [
  "rule_version",
  "regulation_reference",
  "calculation_trace_id",
  "input_hash",
  "source_system",
];

function finding(
  id: string,
  title: string,
  description: string,
  controlIds: string[],
  severity: Finding["severity"],
  impactAreas: ImpactArea[],
  recommendation: string,
  location?: Finding["location"]
): Finding {
  const controls = summarizeControlReferences(controlIds);
  const fallbackControl = corpusStore.getControl("RWA-CALC-001");
  const matchedControls = controls.length > 0 ? controls : fallbackControl ? [fallbackControl] : [];
  const requiredEvidence = matchedControls.flatMap((control) =>
    control.required_evidence.map((artifact) => ({
      evidence_type: artifact.type,
      description: artifact.description,
      priority: artifact.required_for_release ? ("required" as const) : ("recommended" as const),
    }))
  );

  return {
    id,
    title,
    description,
    severity,
    confidence: "high",
    status: "open",
    impact_areas: impactAreas,
    impact_description:
      "The artifact does not yet demonstrate the engineering control evidence needed for regulated RWA delivery.",
    matched_controls: matchedControls.map((control) => ({
      control_id: control.id,
      relevance: "direct",
      rationale: `Finding maps to ${control.title}.`,
    })),
    required_evidence: requiredEvidence.slice(0, 6),
    recommendations: [
      {
        priority: severity === "critical" ? "immediate" : "high",
        action: recommendation,
        rationale: "The missing control may block regulated release readiness.",
        estimated_effort: "1-2 days",
        blocking_release: ["critical", "high"].includes(severity),
      },
    ],
    location,
    detected_at: new Date().toISOString(),
    detected_by: "bank-regulatory-controls-mcp",
    requires_human_review: true,
  };
}

function reviewEnvelope(
  reviewType: ReviewResult["review_type"],
  findings: Finding[],
  controls: Control[]
): ReviewResult {
  const uniqueControls = unique([
    ...controls.map((control) => control.id),
    ...findings.flatMap((item) =>
      item.matched_controls.map((control) => control.control_id)
    ),
  ])
    .map((controlId) => corpusStore.getControl(controlId))
    .filter((control): control is Control => control !== undefined);

  const blockingFindings = findings.filter((item) =>
    item.recommendations.some((recommendation) => recommendation.blocking_release)
  );
  const readinessStatus =
    blockingFindings.length > 0
      ? "not_ready"
      : findings.length > 0
        ? "needs_work"
        : "ready";

  return {
    review_type: reviewType,
    readiness_status: readinessStatus,
    metadata: createMetadata(findings.length > 0 ? "high" : "medium"),
    findings,
    applicable_controls: uniqueControls.map((control) => ({
      id: control.id,
      title: control.title,
      severity: control.severity,
    })),
    acceptance_criteria: uniqueControls.flatMap((control) =>
      control.acceptance_criteria.map(
        (criterion) => `${control.id}: ${criterion.description}`
      )
    ),
    subtasks: uniqueControls.map(
      (control) => `Implement and evidence ${control.id}: ${control.title}.`
    ),
    bob_actions: uniqueControls.flatMap((control) =>
      control.bob_actions.map((action) => `${control.id}: ${action.description}`)
    ),
    control_summary: uniqueControls.map(
      (control) => `${control.id} (${control.severity}): ${control.title}`
    ),
    source_references: sourceReferencesForControls(uniqueControls),
    recommended_actions: [
      ...DEFAULT_RECOMMENDED_ACTIONS,
      "Resolve blocking findings before Jira, GitHub, or release approval output.",
    ],
  };
}

export function reviewFeatureDescription(
  input: FeatureReviewInput
): ReviewResult {
  const text = input.description;
  const normalized = normalizeText(text);
  const matchResult = matchControls({
    text,
    artifact_type: "feature",
    domains: input.domains,
  });
  const controls = matchResult.applicable_controls.map((match) => match.control);
  const findings: Finding[] = [];

  if (
    textIncludesAny(text, ["csv upload", "rwa calculation", "risk weight"]) &&
    !textIncludesAny(text, ["lineage", "source_system", "input_hash"])
  ) {
    findings.push(
      finding(
        "FEATURE-LINEAGE-001",
        "Feature lacks data lineage requirements",
        "RWA upload and calculation features must capture source system, input hash, trace id, rule version, and reporting date.",
        ["RWA-DATA-001", "RWA-AUDIT-001"],
        "critical",
        ["regulatory_compliance", "audit_trail", "data_quality"],
        "Add explicit data lineage fields and acceptance criteria."
      )
    );
  }

  if (
    textIncludesAny(text, ["rwa", "risk weight", "calculation"]) &&
    !textIncludesAny(text, ["rule version", "rule_version", "versioned rule"])
  ) {
    findings.push(
      finding(
        "FEATURE-RULE-001",
        "Feature lacks rule versioning",
        "RWA calculation work must reference approved and versioned regulatory rules.",
        ["RWA-RULE-001"],
        "critical",
        ["regulatory_compliance", "calculation_accuracy"],
        "Require rule version, regulation reference, approval, and reconciliation evidence."
      )
    );
  }

  if (normalized.includes("upload") && !normalized.includes("audit")) {
    findings.push(
      finding(
        "FEATURE-AUDIT-001",
        "Feature lacks audit logging requirements",
        "Upload, validation, calculation, and export events must be auditable.",
        ["RWA-AUDIT-001"],
        "high",
        ["audit_trail"],
        "Add auditable events with actor, timestamp, correlation id, and outcome."
      )
    );
  }

  if (
    textIncludesAny(text, ["upload", "input", "csv"]) &&
    !textIncludesAny(text, ["validation", "sanitize", "schema"])
  ) {
    findings.push(
      finding(
        "FEATURE-VALIDATION-001",
        "Feature lacks input validation requirements",
        "Uploaded data must be schema-validated and sanitized before regulated processing.",
        ["SEC-INPUT-001", "RWA-DQ-001"],
        "high",
        ["security", "data_quality"],
        "Add validation, data-quality flags, and rejection paths for malformed input."
      )
    );
  }

  if (
    textIncludesAny(text, ["rwa", "calculation", "report"]) &&
    !textIncludesAny(text, ["test", "regression", "given"])
  ) {
    findings.push(
      finding(
        "FEATURE-TEST-001",
        "Feature lacks regulatory test obligations",
        "Regulated RWA changes need reproducible tests and release evidence.",
        ["TEST-REG-001", "REL-EVID-001"],
        "high",
        ["testability", "regulatory_compliance"],
        "Add Given/When/Then test obligations and required evidence artifacts."
      )
    );
  }

  return reviewEnvelope("feature", findings, controls);
}

export function reviewArchitectureText(
  input: ArchitectureReviewInput
): ReviewResult {
  const text = input.architecture_text;
  const controls = matchControls({
    text,
    artifact_type: "architecture",
    domains: input.domains,
  }).applicable_controls.map((match) => match.control);
  const findings: Finding[] = [];

  if (textIncludesAny(text, ["hardcoded risk weight", "hard-coded risk weight"])) {
    findings.push(
      finding(
        "ARCH-HARDCODED-RULE-001",
        "Architecture hardcodes regulatory risk weights",
        "Risk weights and regulatory classifications must come from governed, versioned rule data.",
        ["RWA-RULE-001", "RWA-CALC-001"],
        "critical",
        ["regulatory_compliance", "calculation_accuracy", "maintainability"],
        "Replace hardcoded values with a versioned rule registry and approval workflow."
      )
    );
  }

  if (
    textIncludesAny(text, ["rwa", "risk weight", "calculation"]) &&
    !textIncludesAny(text, ["rule registry", "versioned", "reference data"])
  ) {
    findings.push(
      finding(
        "ARCH-RULE-REGISTRY-001",
        "Architecture lacks a governed rule registry",
        "RWA engines need a governed source of approved rule versions and effective dates.",
        ["RWA-RULE-001"],
        "critical",
        ["regulatory_compliance", "maintainability"],
        "Add rule registry, approval, effective date, and reconciliation components."
      )
    );
  }

  if (
    !textIncludesAny(text, ["lineage", "audit", "data quality", "reporting date"]) &&
    textIncludesAny(text, ["rwa", "calculation", "reporting"])
  ) {
    findings.push(
      finding(
        "ARCH-CONTROL-COVERAGE-001",
        "Architecture misses lineage, audit, and reporting controls",
        "Regulated RWA architecture must show how lineage, audit, data quality, and reporting date are handled.",
        ["RWA-DATA-001", "RWA-AUDIT-001", "RWA-DQ-001", "RWA-REPORT-001"],
        "high",
        ["audit_trail", "data_quality", "regulatory_compliance"],
        "Extend the architecture with control flow for lineage, audit, validation, and reporting evidence."
      )
    );
  }

  if (
    textIncludesAny(text, ["rwa", "reporting", "critical"]) &&
    !textIncludesAny(text, ["resilience", "recovery", "dora", "continuity"])
  ) {
    findings.push(
      finding(
        "ARCH-RESILIENCE-001",
        "Architecture lacks resilience considerations",
        "Critical regulated processing should describe continuity, recovery, and resilience controls.",
        ["DORA-ICT-001"],
        "medium",
        ["performance", "regulatory_compliance"],
        "Document resilience tests and recovery expectations for regulated processing."
      )
    );
  }

  return reviewEnvelope("architecture", findings, controls);
}

export function reviewCodeDiff(input: CodeDiffReviewInput): ReviewResult {
  const diff = input.diff;
  const controls = matchControls({
    text: diff,
    artifact_type: "code_diff",
  }).applicable_controls.map((match) => match.control);
  const findings: Finding[] = [];
  const normalized = normalizeText(diff);

  if (
    /risk[_\s-]?weight[^a-z0-9]{0,12}[=:][^0-9]{0,6}\d+(\.\d+)?/i.test(diff) ||
    /rw[^a-z0-9]{0,12}[=:][^0-9]{0,6}0\.\d+/i.test(diff)
  ) {
    findings.push(
      finding(
        "CODE-HARDCODED-RISK-WEIGHT-001",
        "Code diff contains numeric risk weights",
        "Numeric risk weights in code are hard to govern, reconcile, and audit.",
        ["RWA-RULE-001", "RWA-CALC-001"],
        "critical",
        ["regulatory_compliance", "calculation_accuracy"],
        "Move risk weights into versioned regulatory reference data.",
        { file_path: input.file_path, artifact_type: "code_diff" }
      )
    );
  }

  if (
    textIncludesAny(diff, ["calculate", "rwa", "risk weight", "exposure"]) &&
    TRACEABILITY_FIELDS.some((field) => !normalized.includes(normalizeText(field)))
  ) {
    const missingFields = TRACEABILITY_FIELDS.filter(
      (field) => !normalized.includes(normalizeText(field))
    );
    findings.push(
      finding(
        "CODE-TRACEABILITY-FIELDS-001",
        "Code diff lacks required traceability fields",
        `Missing traceability fields: ${missingFields.join(", ")}.`,
        ["RWA-DATA-001", "RWA-AUDIT-001"],
        "critical",
        ["audit_trail", "data_quality", "regulatory_compliance"],
        "Persist traceability fields before returning or exporting calculation results.",
        { file_path: input.file_path, artifact_type: "code_diff" }
      )
    );
  }

  if (
    /console\.log|logger\.(info|debug|warn|error)/i.test(diff) &&
    /email|ssn|customer|name|address|dob|personal/i.test(diff)
  ) {
    findings.push(
      finding(
        "CODE-PII-LOGGING-001",
        "Code diff appears to log PII-like data",
        "Logs must not include personal data or sensitive customer fields.",
        ["SEC-LOG-001"],
        "critical",
        ["security", "audit_trail"],
        "Replace PII logging with redacted identifiers and correlation ids.",
        { file_path: input.file_path, artifact_type: "code_diff" }
      )
    );
  }

  if (
    textIncludesAny(diff, ["upload", "parse", "csv"]) &&
    !textIncludesAny(diff, ["validate", "schema", "sanitize"])
  ) {
    findings.push(
      finding(
        "CODE-VALIDATION-GAP-001",
        "Code diff lacks input validation",
        "Input parsing needs schema validation and clear rejection paths.",
        ["SEC-INPUT-001", "RWA-DQ-001"],
        "high",
        ["security", "data_quality"],
        "Validate and sanitize external input before calculation or persistence.",
        { file_path: input.file_path, artifact_type: "code_diff" }
      )
    );
  }

  if (/Math\.round|toFixed|round/i.test(diff) && !normalized.includes("rounding policy")) {
    findings.push(
      finding(
        "CODE-ROUNDING-POLICY-001",
        "Code diff rounds values without an explicit policy",
        "RWA rounding behavior must be policy-driven and regression-tested.",
        ["RWA-CALC-001", "TEST-REG-001"],
        "high",
        ["calculation_accuracy", "testability"],
        "Reference approved rounding policy and add regression tests.",
        { file_path: input.file_path, artifact_type: "code_diff" }
      )
    );
  }

  return reviewEnvelope("code_diff", findings, controls);
}

export function summarizeReviewForTool(result: ReviewResult): ReviewResult {
  const controls = result.applicable_controls
    .map((control) => corpusStore.getControl(control.id))
    .filter((control): control is Control => control !== undefined);
  const envelope = makeServiceEnvelope(controls);
  return {
    ...result,
    metadata: envelope.metadata,
    source_references: envelope.source_references,
    recommended_actions: result.recommended_actions,
  };
}
