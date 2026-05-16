import { matchControls } from "./controlMatcher.js";
import {
  generateAcceptanceCriteria,
  generateRwaRunEvidenceRequirements,
  generateTestObligations,
} from "./generationServices.js";
import { assessReleaseReadiness, type ReleaseReadinessInput } from "./releaseReadiness.js";
import { searchRegulations } from "./regulationSearch.js";
import type { createMetadata } from "./serviceUtils.js";
import type { SourceReferenceSummary } from "./serviceUtils.js";

export interface MappingReportInput extends ReleaseReadinessInput {
  title?: string;
  feature_text?: string;
  domains?: string[];
  artifact_type?: string;
}

export interface MappingReportResult {
  metadata: ReturnType<typeof createMetadata>;
  markdown: string;
  readiness: ReturnType<typeof assessReleaseReadiness>;
  source_references: SourceReferenceSummary[];
  recommended_actions: string[];
}

function bullet(items: string[]): string {
  if (items.length === 0) {
    return "- None";
  }
  return items.map((item) => `- ${item}`).join("\n");
}

export function generateRegulatoryMappingReport(
  input: MappingReportInput = {}
): MappingReportResult {
  const title = input.title ?? "Regulatory Mapping Report";
  const featureText = input.feature_text ?? "RWA regulated delivery artifact";
  const regulationResult = searchRegulations({
    query: featureText,
    domains: input.domains,
    limit: 8,
  });
  const controlResult = matchControls({
    text: featureText,
    artifact_type: input.artifact_type ?? "release_readiness",
    domains: input.domains,
    limit: 15,
  });
  const controlIds = controlResult.applicable_controls.map((match) => match.control.id);
  const criteria = generateAcceptanceCriteria({ control_ids: controlIds }).criteria;
  const obligations = generateTestObligations({ control_ids: controlIds }).obligations;
  const evidence = generateRwaRunEvidenceRequirements().evidence_package;
  const readiness = assessReleaseReadiness(input);
  const bobActions = controlResult.applicable_controls.flatMap((match) =>
    match.control.bob_actions.map((action) => `${match.control.id}: ${action.description}`)
  );

  const markdown = [
    `# ${title}`,
    "",
    "## Applicable Regulations",
    bullet(
      regulationResult.matches.map(
        (match) =>
          `${match.regulation.id} - ${match.regulation.title} (${match.confidence}, score ${match.score})`
      )
    ),
    "",
    "## Applicable Controls",
    bullet(
      controlResult.applicable_controls.map(
        (match) =>
          `${match.control.id} - ${match.control.title} (${match.control.severity}, score ${match.score})`
      )
    ),
    "",
    "## Required Evidence",
    bullet(
      evidence.map(
        (artifact) =>
          `${artifact.id}: ${artifact.description} (${artifact.evidence_type})`
      )
    ),
    "",
    "## Acceptance Criteria",
    bullet(
      criteria.map(
        (criterion) => `${criterion.control_id}: ${criterion.description}`
      )
    ),
    "",
    "## Test Obligations",
    bullet(
      obligations.map(
        (obligation) =>
          `${obligation.control_id}: Given ${obligation.given}; when ${obligation.when}; then ${obligation.then}`
      )
    ),
    "",
    "## Bob Actions",
    bullet(bobActions),
    "",
    "## Release Readiness",
    `- Status: ${readiness.status}`,
    `- Score: ${readiness.score}`,
    bullet(readiness.required_before_production),
    "",
    "## Human Review Note",
    "This report is an engineering control mapping artifact only. It is not legal advice, not a regulatory compliance opinion, and not a substitute for qualified compliance, legal, risk, or audit review.",
    "",
  ].join("\n");

  return {
    metadata: readiness.metadata,
    markdown,
    readiness,
    source_references: readiness.source_references,
    recommended_actions: readiness.recommended_actions,
  };
}
