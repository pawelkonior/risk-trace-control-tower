import type { Control } from "../schemas/control.js";
import { corpusStore } from "./corpusStore.js";
import {
  DEFAULT_RECOMMENDED_ACTIONS,
  createMetadata,
  severityRank,
  sourceReferencesForControls,
  summarizeControlReferences,
  type SourceReferenceSummary,
} from "./serviceUtils.js";

export interface EvidenceInput {
  id?: string;
  type?: string;
  control_id?: string;
  location?: string;
  description?: string;
}

export interface KnownFindingInput {
  id: string;
  severity: Control["severity"];
  title: string;
  blocking_release?: boolean;
}

export interface ReleaseReadinessInput {
  implemented_control_ids?: string[];
  evidence?: EvidenceInput[];
  known_findings?: KnownFindingInput[];
}

export interface ReleaseGap {
  control_id?: string;
  title: string;
  severity: Control["severity"];
  blocking: boolean;
  required_before_production: string;
}

export interface ReleaseReadinessResult {
  status: "pass" | "conditional_pass" | "fail";
  score: number;
  metadata: ReturnType<typeof createMetadata>;
  baseline_controls: string[];
  implemented_control_ids: string[];
  missing_controls: string[];
  gaps: ReleaseGap[];
  required_before_production: string[];
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

const BASELINE_CONTROLS = [
  "RWA-RULE-001",
  "RWA-CALC-001",
  "RWA-DATA-001",
  "RWA-AUDIT-001",
  "TEST-REG-001",
  "REL-EVID-001",
];

const BLOCKING_CONTROLS = new Set(BASELINE_CONTROLS);

const EVIDENCE_ALIASES: Record<string, string[]> = {
  change_log: ["rule_version", "applied_rules", "change_log"],
  approval_record: ["approval", "rule_version", "release_approval"],
  reconciliation_report: ["reconciliation", "reconciliation_summary"],
  calculation_trace: ["calculation_trace", "results", "trace"],
  data_quality_report: ["validation_report", "data_quality"],
  audit_log: ["audit_extract", "audit_log"],
  test_result: ["test_result", "test_obligations", "regression_test"],
  documentation: ["lineage_report", "input_snapshot", "documentation"],
};

function evidenceMatches(evidence: EvidenceInput[], expectedType: string): boolean {
  const aliases = EVIDENCE_ALIASES[expectedType] ?? [expectedType];
  return evidence.some((artifact) => {
    const text = [
      artifact.id,
      artifact.type,
      artifact.control_id,
      artifact.location,
      artifact.description,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    return aliases.some((alias) => text.includes(alias.toLowerCase()));
  });
}

export function assessReleaseReadiness(
  input: ReleaseReadinessInput = {}
): ReleaseReadinessResult {
  const implemented = new Set(input.implemented_control_ids ?? []);
  const evidence = input.evidence ?? [];
  const baselineControls = summarizeControlReferences(BASELINE_CONTROLS);
  const gaps: ReleaseGap[] = [];

  for (const control of baselineControls) {
    if (!implemented.has(control.id)) {
      gaps.push({
        control_id: control.id,
        title: `Missing implemented control ${control.id}`,
        severity: control.severity,
        blocking: BLOCKING_CONTROLS.has(control.id),
        required_before_production: `Implement and evidence ${control.id}: ${control.title}.`,
      });
      continue;
    }

    for (const artifact of control.required_evidence.filter(
      (item) => item.required_for_release
    )) {
      if (!evidenceMatches(evidence, artifact.type)) {
        gaps.push({
          control_id: control.id,
          title: `Missing release evidence for ${control.id}: ${artifact.type}`,
          severity: control.severity,
          blocking: BLOCKING_CONTROLS.has(control.id),
          required_before_production: `Provide ${artifact.type}: ${artifact.description}.`,
        });
      }
    }
  }

  for (const knownFinding of input.known_findings ?? []) {
    gaps.push({
      title: `Open finding ${knownFinding.id}: ${knownFinding.title}`,
      severity: knownFinding.severity,
      blocking:
        knownFinding.blocking_release ?? ["critical", "high"].includes(knownFinding.severity),
      required_before_production: `Resolve or formally accept finding ${knownFinding.id}.`,
    });
  }

  const score = Math.max(
    0,
    100 -
      gaps.reduce((total, gap) => total + severityRank(gap.severity) * 6, 0)
  );
  const blockingGaps = gaps.filter((gap) => gap.blocking);
  const status =
    blockingGaps.length > 0 ? "fail" : gaps.length > 0 ? "conditional_pass" : "pass";

  return {
    status,
    score,
    metadata: createMetadata(status === "pass" ? "medium" : "high"),
    baseline_controls: BASELINE_CONTROLS,
    implemented_control_ids: [...implemented],
    missing_controls: BASELINE_CONTROLS.filter((controlId) => !implemented.has(controlId)),
    gaps,
    required_before_production: gaps
      .filter((gap) => gap.blocking)
      .map((gap) => gap.required_before_production),
    source_references: sourceReferencesForControls(baselineControls),
    recommended_actions: [
      ...DEFAULT_RECOMMENDED_ACTIONS,
      "Do not approve production release until blocking gaps are closed or formally accepted.",
    ],
  };
}

export function getBaselineReleaseControls(): string[] {
  return BASELINE_CONTROLS;
}

export function getBaselineReleaseControlDetails(): Control[] {
  return BASELINE_CONTROLS.map((controlId) => corpusStore.getControl(controlId)).filter(
    (control): control is Control => control !== undefined
  );
}
