import type { AppliesTo, Regulation, SourceReference } from "../schemas/regulation.js";
import { corpusStore } from "./corpusStore.js";
import {
  DEFAULT_RECOMMENDED_ACTIONS,
  confidenceFromScore,
  createMetadata,
  domainAliases,
  normalizeText,
  safeLimit,
  sourceReferenceCitations,
  sourceReferencesFromRegulations,
  tokenize,
  unique,
  type SourceReferenceSummary,
} from "./serviceUtils.js";

export interface RegulationSearchInput {
  query?: string;
  domains?: string[];
  applies_to?: AppliesTo[];
  jurisdiction?: string;
  include_internal_policies?: boolean;
  limit?: number;
}

export interface RegulationMatch {
  regulation: Regulation;
  score: number;
  confidence: "high" | "medium" | "low";
  matched_terms: string[];
  matched_domains: string[];
  source_references: SourceReference[];
  recommended_actions: string[];
}

export interface RegulationSearchResult {
  status: "ok" | "no_match";
  metadata: ReturnType<typeof createMetadata>;
  matches: RegulationMatch[];
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

const QUERY_DOMAIN_HINTS: Record<string, string[]> = {
  lineage: ["data_quality", "audit_trail", "reporting"],
  traceability: ["audit_trail", "data_quality"],
  rwa: ["capital_adequacy", "credit_risk", "reporting"],
  calculation: ["capital_adequacy", "credit_risk"],
  "risk weight": ["capital_adequacy", "credit_risk"],
  "rule version": ["governance", "audit_trail", "data_quality"],
};

const SPECIAL_DOMAIN_MATCHES: Record<string, string[]> = {
  rule_versioning: ["CRR3", "INTERNAL_RULE_GOVERNANCE"],
};

function regulationSearchText(regulation: Regulation): string {
  return normalizeText(
    [
      regulation.id,
      regulation.title,
      regulation.summary,
      regulation.jurisdiction,
      regulation.applies_to.join(" "),
      regulation.domains.join(" "),
      ...regulation.key_requirements.flatMap((requirement) => [
        requirement.id,
        requirement.article ?? "",
        requirement.title,
        requirement.description,
      ]),
      ...regulation.engineering_implications.map(
        (implication) => `${implication.area} ${implication.description}`
      ),
    ].join(" ")
  );
}

function inferDomainsFromQuery(query: string): string[] {
  const normalized = normalizeText(query);
  return unique(
    Object.entries(QUERY_DOMAIN_HINTS).flatMap(([phrase, domains]) =>
      normalized.includes(normalizeText(phrase)) ? domains : []
    )
  );
}

function scoreRegulation(
  regulation: Regulation,
  input: RegulationSearchInput
): Omit<RegulationMatch, "confidence" | "source_references" | "recommended_actions"> {
  const query = input.query ?? "";
  const terms = tokenize(query);
  const searchableText = regulationSearchText(regulation);
  const requestedDomains = domainAliases([
    ...(input.domains ?? []),
    ...inferDomainsFromQuery(query),
  ]);
  const requestedJurisdiction = input.jurisdiction?.toLowerCase();
  const matchedTerms: string[] = [];
  const matchedDomains: string[] = [];
  let score = 0;

  if (query) {
    const normalizedQuery = normalizeText(query);
    if (normalizeText(regulation.id) === normalizedQuery) {
      score += 120;
      matchedTerms.push(regulation.id);
    }
    if (normalizeText(regulation.title).includes(normalizedQuery)) {
      score += 60;
      matchedTerms.push(regulation.title);
    }

    for (const term of terms) {
      if (searchableText.includes(term)) {
        score += 8;
        matchedTerms.push(term);
      }
    }

    if (
      normalizedQuery.includes("data lineage") &&
      ["BCBS239", "INTERNAL_AUDIT_EVIDENCE"].includes(regulation.id)
    ) {
      score += 45;
      matchedTerms.push("data lineage");
    }
  }

  for (const domain of requestedDomains) {
    if (regulation.domains.includes(domain as never)) {
      score += 25;
      matchedDomains.push(domain);
    }
  }

  for (const domain of input.domains ?? []) {
    const normalizedDomain = normalizeText(domain).replaceAll(" ", "_");
    if (SPECIAL_DOMAIN_MATCHES[normalizedDomain]?.includes(regulation.id)) {
      score += 55;
      matchedDomains.push(domain);
    }
  }

  if (input.applies_to?.some((appliesTo) => regulation.applies_to.includes(appliesTo))) {
    score += 20;
  }

  if (requestedJurisdiction) {
    if (regulation.jurisdiction.toLowerCase() === requestedJurisdiction) {
      score += 25;
    } else if (regulation.jurisdiction === "GLOBAL") {
      score += 8;
    }
  }

  return {
    regulation,
    score,
    matched_terms: unique(matchedTerms),
    matched_domains: unique(matchedDomains),
  };
}

export function searchRegulations(
  input: RegulationSearchInput = {}
): RegulationSearchResult {
  const limit = safeLimit(input.limit, 10);
  const includeInternalPolicies = input.include_internal_policies ?? true;
  const matches = corpusStore
    .getRegulations()
    .filter(
      (regulation) =>
        includeInternalPolicies ||
        (regulation.jurisdiction !== "INTERNAL" &&
          !regulation.applies_to.includes("internal_policy"))
    )
    .map((regulation) => scoreRegulation(regulation, input))
    .filter((match) => match.score > 0 || !input.query)
    .sort((a, b) => b.score - a.score || a.regulation.id.localeCompare(b.regulation.id))
    .slice(0, limit)
    .map((match) => ({
      ...match,
      confidence: confidenceFromScore(match.score),
      source_references: match.regulation.source_references,
      recommended_actions: [
        `Review ${match.regulation.id} requirements with compliance owners.`,
        `Map impacted engineering controls for ${match.regulation.domains.join(", ")}.`,
      ],
    }));

  const sourceReferences = sourceReferencesFromRegulations(
    matches.map((match) => match.regulation)
  );
  const topConfidence = matches[0]?.confidence ?? "low";

  return {
    status: matches.length > 0 ? "ok" : "no_match",
    metadata: createMetadata(topConfidence),
    matches,
    source_references: sourceReferences,
    recommended_actions: [
      ...DEFAULT_RECOMMENDED_ACTIONS,
      ...unique(
        matches.flatMap((match) =>
          sourceReferenceCitations(match.regulation.source_references).map(
            (citation) => `Validate source reference: ${citation}.`
          )
        )
      ).slice(0, 5),
    ],
  };
}
