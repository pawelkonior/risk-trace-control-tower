import {
  STANDARD_DISCLAIMER,
  type CommonMetadata,
  type Confidence,
  type RegulatoryDomain,
  type Severity,
} from "../schemas/common.js";
import type { Control } from "../schemas/control.js";
import type { EvidenceArtifact } from "../schemas/evidence.js";
import type { Regulation, SourceReference } from "../schemas/regulation.js";
import { corpusStore } from "./corpusStore.js";

export interface SourceReferenceSummary {
  regulation_id: string;
  citation: string;
  url?: string;
}

export interface ServiceEnvelope {
  metadata: CommonMetadata;
  disclaimer: string;
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

export const DEFAULT_RECOMMENDED_ACTIONS = [
  "Validate regulatory interpretation with qualified compliance or legal reviewers.",
  "Link controls, test results, and evidence artifacts before production release.",
  "Record human approval for material RWA calculation, reporting, or rule changes.",
];

const STOP_WORDS = new Set([
  "a",
  "an",
  "and",
  "are",
  "as",
  "by",
  "for",
  "from",
  "in",
  "into",
  "of",
  "on",
  "or",
  "the",
  "to",
  "with",
]);

export function createMetadata(
  confidence: Confidence = "medium",
  jurisdiction = "GLOBAL",
  requiresHumanReview = true
): CommonMetadata {
  return {
    disclaimer: STANDARD_DISCLAIMER,
    as_of: new Date().toISOString(),
    jurisdiction,
    confidence,
    requires_human_review: requiresHumanReview,
  };
}

export function normalizeText(value: string): string {
  return value
    .toLowerCase()
    .replace(/[_/]+/g, " ")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function tokenize(value: string): string[] {
  return unique(
    normalizeText(value)
      .split(" ")
      .filter((term) => term.length > 2 && !STOP_WORDS.has(term))
  );
}

export function unique<T>(items: T[]): T[] {
  return [...new Set(items)];
}

export function uniqueById<T extends { id: string }>(items: T[]): T[] {
  const seen = new Set<string>();
  return items.filter((item) => {
    if (seen.has(item.id)) {
      return false;
    }
    seen.add(item.id);
    return true;
  });
}

export function severityRank(severity: Severity): number {
  const ranks: Record<Severity, number> = {
    critical: 5,
    high: 4,
    medium: 3,
    low: 2,
    info: 1,
  };
  return ranks[severity];
}

export function confidenceFromScore(score: number): Confidence {
  if (score >= 60) {
    return "high";
  }
  if (score >= 25) {
    return "medium";
  }
  return "low";
}

export function sourceReferencesFromRegulations(
  regulations: Regulation[]
): SourceReferenceSummary[] {
  return regulations.flatMap((regulation) =>
    regulation.source_references.map((reference) => ({
      regulation_id: regulation.id,
      citation: reference.citation,
      url: reference.url,
    }))
  );
}

export function sourceReferencesForControls(
  controls: Control[]
): SourceReferenceSummary[] {
  const regulations = uniqueById(
    controls.flatMap((control) =>
      control.regulatory_basis
        .map((basis) => corpusStore.getRegulation(basis.regulation_id))
        .filter((regulation): regulation is Regulation => regulation !== undefined)
    )
  );
  return sourceReferencesFromRegulations(regulations);
}

export function summarizeEvidence(controls: Control[]): EvidenceArtifact[] {
  const key = (artifact: EvidenceArtifact) =>
    `${artifact.type}:${artifact.description}`;
  const seen = new Set<string>();
  return controls
    .flatMap((control) => control.required_evidence)
    .filter((artifact) => {
      const artifactKey = key(artifact);
      if (seen.has(artifactKey)) {
        return false;
      }
      seen.add(artifactKey);
      return true;
    });
}

export function summarizeControlReferences(controlIds: string[]): Control[] {
  return unique(controlIds)
    .map((id) => corpusStore.getControl(id))
    .filter((control): control is Control => control !== undefined);
}

export function sourceReferenceCitations(
  references: SourceReference[]
): string[] {
  return references.map((reference) => reference.citation);
}

export function safeLimit(limit: number | undefined, fallback = 10): number {
  if (!limit || Number.isNaN(limit)) {
    return fallback;
  }
  return Math.max(1, Math.min(50, Math.floor(limit)));
}

export function textIncludesAny(text: string, phrases: string[]): boolean {
  const normalized = normalizeText(text);
  return phrases.some((phrase) => normalized.includes(normalizeText(phrase)));
}

export function domainAliases(domains: string[] = []): string[] {
  const aliases: Record<string, RegulatoryDomain[]> = {
    calculation: ["capital_adequacy", "credit_risk"],
    lineage: ["data_quality", "audit_trail"],
    rule_versioning: ["governance", "audit_trail", "data_quality"],
    rules: ["governance", "data_quality"],
    resilience: ["ict_security", "operational_risk", "testing"],
    security: ["ict_security", "data_protection"],
  };

  return unique(
    domains.flatMap((domain) => [
      domain,
      ...(aliases[normalizeText(domain).replaceAll(" ", "_")] ?? []),
    ])
  );
}

export function makeServiceEnvelope(
  controls: Control[],
  confidence: Confidence = "medium"
): ServiceEnvelope {
  return {
    metadata: createMetadata(confidence),
    disclaimer: STANDARD_DISCLAIMER,
    source_references: sourceReferencesForControls(controls),
    recommended_actions: DEFAULT_RECOMMENDED_ACTIONS,
  };
}
