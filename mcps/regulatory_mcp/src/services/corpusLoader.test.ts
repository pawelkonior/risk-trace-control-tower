import { describe, it, expect, beforeEach } from "vitest";
import {
  cpSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from "fs";
import { join } from "path";
import { tmpdir } from "os";
import { loadCorpus, CorpusValidationError } from "./corpusLoader.js";
import { corpusStore } from "./corpusStore.js";

function withTemporaryCorpus(
  mutate: (dataDir: string) => void,
  assert: (dataDir: string) => void
): void {
  const tempDir = mkdtempSync(join(tmpdir(), "regulatory-mcp-corpus-"));
  const dataDir = join(tempDir, "data");
  cpSync(join(process.cwd(), "data"), dataDir, { recursive: true });

  try {
    mutate(dataDir);
    assert(dataDir);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf-8")) as T;
}

function writeJson(path: string, value: unknown): void {
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);
}

describe("Corpus Loader", () => {
  beforeEach(() => {
    corpusStore.reset();
  });

  describe("loadCorpus", () => {
    it("should load corpus successfully", () => {
      const corpus = loadCorpus();
      expect(corpus).toBeDefined();
      expect(corpus.regulations).toBeDefined();
      expect(corpus.controls).toBeDefined();
      expect(corpus.keywordMappings).toBeDefined();
      expect(corpus.artifactMappings).toBeDefined();
      expect(corpus.domainMappings).toBeDefined();
    });

    it("should load at least 9 regulations", () => {
      const corpus = loadCorpus();
      expect(corpus.regulations.length).toBeGreaterThanOrEqual(9);
    });

    it("should load at least 15 controls", () => {
      const corpus = loadCorpus();
      expect(corpus.controls.length).toBeGreaterThanOrEqual(15);
    });

    it("should have no duplicate regulation IDs", () => {
      const corpus = loadCorpus();
      const ids = corpus.regulations.map((r) => r.id);
      const uniqueIds = new Set(ids);
      expect(ids.length).toBe(uniqueIds.size);
    });

    it("should have no duplicate control IDs", () => {
      const corpus = loadCorpus();
      const ids = corpus.controls.map((c) => c.id);
      const uniqueIds = new Set(ids);
      expect(ids.length).toBe(uniqueIds.size);
    });

    it("should validate all regulations pass schema", () => {
      const corpus = loadCorpus();
      for (const regulation of corpus.regulations) {
        expect(regulation.id).toBeDefined();
        expect(regulation.title).toBeDefined();
        expect(regulation.type).toBeDefined();
        expect(regulation.jurisdiction).toBeDefined();
        expect(regulation.status).toBeDefined();
        expect(regulation.key_requirements.length).toBeGreaterThan(0);
        expect(regulation.engineering_implications.length).toBeGreaterThan(0);
        expect(regulation.source_references.length).toBeGreaterThan(0);
      }
    });

    it("should validate all controls pass schema", () => {
      const corpus = loadCorpus();
      for (const control of corpus.controls) {
        expect(control.id).toBeDefined();
        expect(control.id).toMatch(/^[A-Z]+-[A-Z]+-\d{3}$/);
        expect(control.title).toBeDefined();
        expect(control.severity).toBeDefined();
        expect(control.regulatory_basis.length).toBeGreaterThan(0);
        expect(control.required_evidence.length).toBeGreaterThan(0);
        expect(control.acceptance_criteria.length).toBeGreaterThan(0);
        expect(control.test_obligations.length).toBeGreaterThan(0);
      }
    });

    it("should have valid control references in keyword mappings", () => {
      const corpus = loadCorpus();
      const validControlIds = new Set(corpus.controls.map((c) => c.id));

      for (const [keyword, controlIds] of Object.entries(
        corpus.keywordMappings.mappings
      )) {
        for (const controlId of controlIds) {
          expect(
            validControlIds.has(controlId),
            `Invalid control ID '${controlId}' in keyword mapping for '${keyword}'`
          ).toBe(true);
        }
      }
    });

    it("should have valid control references in artifact mappings", () => {
      const corpus = loadCorpus();
      const validControlIds = new Set(corpus.controls.map((c) => c.id));

      for (const [artifactType, controlIds] of Object.entries(
        corpus.artifactMappings.mappings
      )) {
        for (const controlId of controlIds) {
          expect(
            validControlIds.has(controlId),
            `Invalid control ID '${controlId}' in artifact mapping for '${artifactType}'`
          ).toBe(true);
        }
      }
    });

    it("should have valid regulation references in domain mappings", () => {
      const corpus = loadCorpus();
      const validRegulationIds = new Set(corpus.regulations.map((r) => r.id));

      for (const [domain, regulationIds] of Object.entries(
        corpus.domainMappings.mappings
      )) {
        for (const regulationId of regulationIds) {
          expect(
            validRegulationIds.has(regulationId),
            `Invalid regulation ID '${regulationId}' in domain mapping for '${domain}'`
          ).toBe(true);
        }
      }
    });

    it("should have valid regulation references in controls", () => {
      const corpus = loadCorpus();
      const validRegulationIds = new Set(corpus.regulations.map((r) => r.id));

      for (const control of corpus.controls) {
        for (const basis of control.regulatory_basis) {
          expect(
            validRegulationIds.has(basis.regulation_id),
            `Control ${control.id} references non-existent regulation: ${basis.regulation_id}`
          ).toBe(true);
        }
      }
    });

    it("should load regulations in deterministic order", () => {
      const corpus1 = loadCorpus();
      corpusStore.reset();
      const corpus2 = loadCorpus();

      const ids1 = corpus1.regulations.map((r) => r.id);
      const ids2 = corpus2.regulations.map((r) => r.id);

      expect(ids1).toEqual(ids2);
    });

    it("should load controls in deterministic order", () => {
      const corpus1 = loadCorpus();
      corpusStore.reset();
      const corpus2 = loadCorpus();

      const ids1 = corpus1.controls.map((c) => c.id);
      const ids2 = corpus2.controls.map((c) => c.id);

      expect(ids1).toEqual(ids2);
    });

    it("should include expected regulations", () => {
      const corpus = loadCorpus();
      const regulationIds = corpus.regulations.map((r) => r.id);

      const expectedRegulations = [
        "CRR3",
        "EBA_REPORTING_4",
        "BCBS239",
        "DORA",
        "EBA_ICT_SECURITY",
        "GDPR",
        "INTERNAL_SDLC",
        "INTERNAL_RULE_GOVERNANCE",
        "INTERNAL_AUDIT_EVIDENCE",
      ];

      for (const expectedId of expectedRegulations) {
        expect(
          regulationIds.includes(expectedId),
          `Expected regulation ${expectedId} not found`
        ).toBe(true);
      }
    });

    it("should include expected controls", () => {
      const corpus = loadCorpus();
      const controlIds = corpus.controls.map((c) => c.id);

      const expectedControls = [
        "RWA-CALC-001",
        "RWA-RULE-001",
        "RWA-DATA-001",
        "RWA-DQ-001",
        "RWA-AUDIT-001",
        "RWA-REPORT-001",
        "RWA-RECON-001",
        "SEC-INPUT-001",
        "SEC-LOG-001",
        "SEC-ACCESS-001",
        "DORA-ICT-001",
        "TEST-REG-001",
        "REL-EVID-001",
        "ARCH-ADR-001",
        "PERF-RWA-001",
      ];

      for (const expectedId of expectedControls) {
        expect(
          controlIds.includes(expectedId),
          `Expected control ${expectedId} not found`
        ).toBe(true);
      }
    });

    it("should have critical RWA controls", () => {
      const corpus = loadCorpus();
      const criticalRwaControls = corpus.controls.filter(
        (c) => c.severity === "critical" && c.id.startsWith("RWA-")
      );

      expect(criticalRwaControls.length).toBeGreaterThan(0);
    });

    it("should have controls with required evidence", () => {
      const corpus = loadCorpus();
      const controlsWithRequiredEvidence = corpus.controls.filter((c) =>
        c.required_evidence.some((e) => e.required_for_release)
      );

      expect(controlsWithRequiredEvidence.length).toBeGreaterThan(0);
    });

    it("should fail when a duplicate regulation ID exists", () => {
      withTemporaryCorpus(
        (dataDir) => {
          const source = join(dataDir, "regulations", "CRR3.json");
          const duplicate = join(dataDir, "regulations", "ZZZ_DUPLICATE_CRR3.json");
          writeJson(duplicate, readJson(source));
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/Duplicate regulation ID: CRR3/);
        }
      );
    });

    it("should fail when a duplicate control ID exists", () => {
      withTemporaryCorpus(
        (dataDir) => {
          const source = join(dataDir, "controls", "RWA-CALC-001.json");
          const duplicate = join(dataDir, "controls", "ZZZ_DUPLICATE_RWA_CALC_001.json");
          writeJson(duplicate, readJson(source));
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(
            /Duplicate control ID: RWA-CALC-001/
          );
        }
      );
    });

    it("should fail when a keyword mapping references an unknown control ID", () => {
      withTemporaryCorpus(
        (dataDir) => {
          const mappingPath = join(dataDir, "mappings", "keywords-to-controls.json");
          const mapping = readJson<{
            description: string;
            mappings: Record<string, string[]>;
          }>(mappingPath);
          mapping.mappings.pii = ["SEC-PRIVACY-001"];
          writeJson(mappingPath, mapping);
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/SEC-PRIVACY-001/);
        }
      );
    });

    it("should fail when an artifact mapping references an unknown control ID", () => {
      withTemporaryCorpus(
        (dataDir) => {
          const mappingPath = join(
            dataDir,
            "mappings",
            "artifact-type-to-controls.json"
          );
          const mapping = readJson<{
            description: string;
            mappings: Record<string, string[]>;
          }>(mappingPath);
          mapping.mappings.code_diff = ["UNKNOWN-CONTROL-001"];
          writeJson(mappingPath, mapping);
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/UNKNOWN-CONTROL-001/);
        }
      );
    });

    it("should fail when a domain mapping references an unknown regulation ID", () => {
      withTemporaryCorpus(
        (dataDir) => {
          const mappingPath = join(dataDir, "mappings", "domain-to-regulations.json");
          const mapping = readJson<{
            description: string;
            mappings: Record<string, string[]>;
          }>(mappingPath);
          mapping.mappings.data_quality = ["UNKNOWN_REGULATION"];
          writeJson(mappingPath, mapping);
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/UNKNOWN_REGULATION/);
        }
      );
    });

    it("should fail when a control references an unknown regulation ID", () => {
      withTemporaryCorpus(
        (dataDir) => {
          const controlPath = join(dataDir, "controls", "RWA-RULE-001.json");
          const control = readJson<{
            regulatory_basis: Array<{ regulation_id: string }>;
          }>(controlPath);
          control.regulatory_basis[0].regulation_id = "UNKNOWN_REGULATION";
          writeJson(controlPath, control);
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/UNKNOWN_REGULATION/);
        }
      );
    });

    it("should fail with CORPUS_LOAD_ERROR context when JSON cannot be parsed", () => {
      withTemporaryCorpus(
        (dataDir) => {
          writeFileSync(join(dataDir, "regulations", "BROKEN.json"), "{");
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/CORPUS_LOAD_ERROR/);
          expect(() => loadCorpus(dataDir)).toThrow(/BROKEN\.json/);
        }
      );
    });

    it("should fail when a mapping file has an invalid shape", () => {
      withTemporaryCorpus(
        (dataDir) => {
          writeJson(join(dataDir, "mappings", "keywords-to-controls.json"), {
            description: "Broken mapping",
            mappings: {
              rwa: "RWA-CALC-001",
            },
          });
        },
        (dataDir) => {
          expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
          expect(() => loadCorpus(dataDir)).toThrow(/Invalid mapping/);
        }
      );
    });
  });
});

// Made with Bob
