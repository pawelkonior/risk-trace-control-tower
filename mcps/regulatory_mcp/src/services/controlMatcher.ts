import type { Control } from "../schemas/control.js";
import type { EvidenceArtifact } from "../schemas/evidence.js";
import { corpusStore } from "./corpusStore.js";
import {
  DEFAULT_RECOMMENDED_ACTIONS,
  confidenceFromScore,
  createMetadata,
  domainAliases,
  normalizeText,
  safeLimit,
  severityRank,
  sourceReferencesForControls,
  summarizeEvidence,
  tokenize,
  unique,
  type SourceReferenceSummary,
} from "./serviceUtils.js";

export interface ControlMatchInput {
  text?: string;
  artifact_type?: string;
  domains?: string[];
  explicit_control_ids?: string[];
  excluded_control_ids?: string[];
  limit?: number;
}

export interface ApplicableControl {
  control: Control;
  score: number;
  severity: Control["severity"];
  confidence: "high" | "medium" | "low";
  matched_keywords: string[];
  matched_domains: string[];
  match_reasons: string[];
  required_evidence: EvidenceArtifact[];
  source_references: SourceReferenceSummary[];
}

export interface ControlMatchResult {
  status: "ok" | "no_match";
  metadata: ReturnType<typeof createMetadata>;
  applicable_controls: ApplicableControl[];
  required_evidence: EvidenceArtifact[];
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

const TEXT_HINTS: Array<{
  phrases: string[];
  controlIds: string[];
  reason: string;
}> = [
  {
    phrases: ["risk weight", "risk-weight", "risk weighted", "rwa calculation"],
    controlIds: ["RWA-RULE-001", "RWA-CALC-001"],
    reason: "Risk weight calculation requires controlled rules and traceable RWA math.",
  },
  {
    phrases: ["csv upload", "file upload", "uploaded csv"],
    controlIds: ["RWA-DATA-001", "RWA-DQ-001", "RWA-AUDIT-001", "SEC-INPUT-001"],
    reason: "CSV upload introduces lineage, data quality, audit, and secure input obligations.",
  },
  {
    phrases: ["lineage", "calculation trace", "trace id"],
    controlIds: ["RWA-DATA-001", "RWA-AUDIT-001"],
    reason: "Lineage text maps to data completeness and audit traceability controls.",
  },
  {
    phrases: ["pii", "personal data", "email", "ssn"],
    controlIds: ["SEC-LOG-001"],
    reason: "PII-sensitive processing requires secure logging controls.",
  },
];

function addScore(
  scores: Map<string, ApplicableControl>,
  controlId: string,
  points: number,
  keyword: string,
  reason: string
): void {
  const control = corpusStore.getControl(controlId);
  if (!control) {
    return;
  }
  const existing =
    scores.get(controlId) ??
    ({
      control,
      score: 0,
      severity: control.severity,
      confidence: "low",
      matched_keywords: [],
      matched_domains: [],
      match_reasons: [],
      required_evidence: control.required_evidence,
      source_references: sourceReferencesForControls([control]),
    } satisfies ApplicableControl);

  existing.score += points;
  existing.matched_keywords = unique([...existing.matched_keywords, keyword]);
  existing.match_reasons = unique([...existing.match_reasons, reason]);
  scores.set(controlId, existing);
}

function addMappedControls(
  scores: Map<string, ApplicableControl>,
  controlIds: string[],
  points: number,
  keyword: string,
  reason: string
): void {
  for (const controlId of controlIds) {
    addScore(scores, controlId, points, keyword, reason);
  }
}

function inferDomains(text: string): string[] {
  const normalized = normalizeText(text);
  const domains: string[] = [];
  const hints: Record<string, string[]> = {
    capital_adequacy: ["rwa", "capital", "risk weight", "exposure"],
    data_quality: ["validation", "csv", "upload", "data quality", "input"],
    audit_trail: ["audit", "trace", "lineage", "evidence"],
    governance: ["rule", "version", "approval", "change"],
    ict_security: ["security", "auth", "pii", "logging", "sanitize"],
    testing: ["test", "coverage", "regression"],
    reporting: ["report", "xbrl", "export"],
    performance: ["performance", "benchmark", "latency"],
  };

  for (const [domain, phrases] of Object.entries(hints)) {
    if (phrases.some((phrase) => normalized.includes(normalizeText(phrase)))) {
      domains.push(domain);
    }
  }
  return domains;
}

export function getControlById(controlId: string): Control | undefined {
  return corpusStore.getControl(controlId);
}

export function matchControls(
  input: ControlMatchInput = {}
): ControlMatchResult {
  const text = input.text ?? "";
  const normalized = normalizeText(text);
  const tokens = tokenize(text);
  const scores = new Map<string, ApplicableControl>();
  const excluded = new Set(input.excluded_control_ids ?? []);

  for (const controlId of input.explicit_control_ids ?? []) {
    addScore(scores, controlId, 100, controlId, "Control was explicitly requested.");
  }

  for (const [keyword, controlIds] of Object.entries(
    corpusStore.getCorpus().keywordMappings.mappings
  )) {
    const normalizedKeyword = normalizeText(keyword);
    if (normalized.includes(normalizedKeyword) || tokens.includes(normalizedKeyword)) {
      addMappedControls(
        scores,
        controlIds,
        35,
        keyword,
        `Keyword '${keyword}' matched the artifact text.`
      );
    }
  }

  for (const hint of TEXT_HINTS) {
    const matchedPhrase = hint.phrases.find((phrase) =>
      normalized.includes(normalizeText(phrase))
    );
    if (matchedPhrase) {
      addMappedControls(scores, hint.controlIds, 45, matchedPhrase, hint.reason);
    }
  }

  if (input.artifact_type) {
    addMappedControls(
      scores,
      corpusStore.getControlsByArtifactType(input.artifact_type).map((control) => control.id),
      25,
      input.artifact_type,
      `Artifact type '${input.artifact_type}' maps to these controls.`
    );
  }

  const requestedDomains = domainAliases([
    ...(input.domains ?? []),
    ...inferDomains(text),
  ]);
  for (const domain of requestedDomains) {
    for (const control of corpusStore.getControlsByDomain(domain)) {
      addScore(scores, control.id, 20, domain, `Domain '${domain}' matched this control.`);
      const existing = scores.get(control.id);
      if (existing) {
        existing.matched_domains = unique([...existing.matched_domains, domain]);
      }
    }
  }

  const applicableControls = [...scores.values()]
    .filter((match) => !excluded.has(match.control.id))
    .map((match) => ({
      ...match,
      confidence: confidenceFromScore(match.score),
    }))
    .sort(
      (a, b) =>
        b.score - a.score ||
        severityRank(b.severity) - severityRank(a.severity) ||
        a.control.id.localeCompare(b.control.id)
    )
    .slice(0, safeLimit(input.limit, 15));

  const controls = applicableControls.map((match) => match.control);
  return {
    status: applicableControls.length > 0 ? "ok" : "no_match",
    metadata: createMetadata(applicableControls[0]?.confidence ?? "low"),
    applicable_controls: applicableControls,
    required_evidence: summarizeEvidence(controls),
    source_references: sourceReferencesForControls(controls),
    recommended_actions: [
      ...DEFAULT_RECOMMENDED_ACTIONS,
      "Use the matched controls to update Jira acceptance criteria and release evidence.",
    ],
  };
}
