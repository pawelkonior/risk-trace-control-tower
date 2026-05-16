import { readFileSync, readdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { z } from "zod";
import { RegulationSchema, type Regulation } from "../schemas/regulation.js";
import { ControlSchema, type Control } from "../schemas/control.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const DEFAULT_DATA_DIR = join(__dirname, "../../data");

/**
 * Mapping data structures
 */
const MappingFileSchema = z.object({
  description: z.string(),
  mappings: z.record(z.array(z.string())),
});

type MappingFile = z.infer<typeof MappingFileSchema>;

export type KeywordMapping = MappingFile;

export type ArtifactMapping = MappingFile;

export type DomainMapping = MappingFile;

/**
 * Complete corpus data
 */
export interface RegulatoryCorpus {
  regulations: Regulation[];
  controls: Control[];
  keywordMappings: KeywordMapping;
  artifactMappings: ArtifactMapping;
  domainMappings: DomainMapping;
}

/**
 * Validation error
 */
export class CorpusValidationError extends Error {
  public readonly code = "CORPUS_LOAD_ERROR";

  constructor(
    message: string,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = "CorpusValidationError";
  }
}

function readJsonFile(filePath: string, label: string): unknown {
  try {
    return JSON.parse(readFileSync(filePath, "utf-8"));
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new CorpusValidationError(
      `CORPUS_LOAD_ERROR: Failed to read or parse ${label}: ${message}`
    );
  }
}

/**
 * Load and validate all regulations from data/regulations/*.json
 */
function loadRegulations(dataDir: string): Regulation[] {
  const regulationsDir = join(dataDir, "regulations");
  const files = readdirSync(regulationsDir)
    .filter((f) => f.endsWith(".json"))
    .sort(); // Deterministic ordering

  const regulations: Regulation[] = [];
  const seenIds = new Set<string>();

  for (const file of files) {
    const filePath = join(regulationsDir, file);
    const data = readJsonFile(filePath, `regulation ${file}`);

    // Validate with Zod
    const result = RegulationSchema.safeParse(data);
    if (!result.success) {
      throw new CorpusValidationError(
        `Invalid regulation in ${file}: ${result.error.message}`,
        result.error.errors
      );
    }

    // Check for duplicate IDs
    if (seenIds.has(result.data.id)) {
      throw new CorpusValidationError(
        `Duplicate regulation ID: ${result.data.id} in ${file}`
      );
    }
    seenIds.add(result.data.id);

    regulations.push(result.data);
  }

  return regulations;
}

/**
 * Load and validate all controls from data/controls/*.json
 */
function loadControls(dataDir: string): Control[] {
  const controlsDir = join(dataDir, "controls");
  const files = readdirSync(controlsDir)
    .filter((f) => f.endsWith(".json"))
    .sort(); // Deterministic ordering

  const controls: Control[] = [];
  const seenIds = new Set<string>();

  for (const file of files) {
    const filePath = join(controlsDir, file);
    const data = readJsonFile(filePath, `control ${file}`);

    // Validate with Zod
    const result = ControlSchema.safeParse(data);
    if (!result.success) {
      throw new CorpusValidationError(
        `Invalid control in ${file}: ${result.error.message}`,
        result.error.errors
      );
    }

    // Check for duplicate IDs
    if (seenIds.has(result.data.id)) {
      throw new CorpusValidationError(
        `Duplicate control ID: ${result.data.id} in ${file}`
      );
    }
    seenIds.add(result.data.id);

    controls.push(result.data);
  }

  return controls;
}

/**
 * Load mapping file
 */
function loadMapping(dataDir: string, filename: string): MappingFile {
  const filePath = join(dataDir, "mappings", filename);
  const data = readJsonFile(filePath, `mapping ${filename}`);
  const result = MappingFileSchema.safeParse(data);

  if (!result.success) {
    throw new CorpusValidationError(
      `Invalid mapping in ${filename}: ${result.error.message}`,
      result.error.errors
    );
  }

  return result.data;
}

/**
 * Validate that all control IDs in mappings exist in the corpus
 */
function validateControlMappings(
  mappings: Record<string, string[]>,
  validControlIds: Set<string>,
  mappingName: string
): void {
  for (const [key, controlIds] of Object.entries(mappings)) {
    for (const controlId of controlIds) {
      if (!validControlIds.has(controlId)) {
        throw new CorpusValidationError(
          `Invalid control ID '${controlId}' in ${mappingName} mapping for key '${key}'`
        );
      }
    }
  }
}

/**
 * Validate that all regulation IDs in mappings exist in the corpus
 */
function validateRegulationMappings(
  mappings: Record<string, string[]>,
  validRegulationIds: Set<string>,
  mappingName: string
): void {
  for (const [key, regulationIds] of Object.entries(mappings)) {
    for (const regulationId of regulationIds) {
      if (!validRegulationIds.has(regulationId)) {
        throw new CorpusValidationError(
          `Invalid regulation ID '${regulationId}' in ${mappingName} mapping for domain '${key}'`
        );
      }
    }
  }
}

/**
 * Validate that all regulation IDs referenced in controls exist
 */
function validateControlRegulationReferences(
  controls: Control[],
  validRegulationIds: Set<string>
): void {
  for (const control of controls) {
    for (const basis of control.regulatory_basis) {
      if (!validRegulationIds.has(basis.regulation_id)) {
        throw new CorpusValidationError(
          `Control ${control.id} references non-existent regulation: ${basis.regulation_id}`
        );
      }
    }
  }
}

/**
 * Load and validate the complete regulatory corpus
 */
export function loadCorpus(dataDir: string = DEFAULT_DATA_DIR): RegulatoryCorpus {
  // Load all data
  const regulations = loadRegulations(dataDir);
  const controls = loadControls(dataDir);
  const keywordMappings = loadMapping(dataDir, "keywords-to-controls.json");
  const artifactMappings = loadMapping(dataDir, "artifact-type-to-controls.json");
  const domainMappings = loadMapping(dataDir, "domain-to-regulations.json");

  // Build validation sets
  const validRegulationIds = new Set(regulations.map((r) => r.id));
  const validControlIds = new Set(controls.map((c) => c.id));

  // Validate control references in controls
  validateControlRegulationReferences(controls, validRegulationIds);

  // Validate mappings
  validateControlMappings(
    keywordMappings.mappings,
    validControlIds,
    "keywords-to-controls"
  );
  validateControlMappings(
    artifactMappings.mappings,
    validControlIds,
    "artifact-type-to-controls"
  );
  validateRegulationMappings(
    domainMappings.mappings,
    validRegulationIds,
    "domain-to-regulations"
  );

  return {
    regulations,
    controls,
    keywordMappings,
    artifactMappings,
    domainMappings,
  };
}

// Made with Bob
