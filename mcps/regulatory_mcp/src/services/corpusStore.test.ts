import { describe, it, expect, beforeEach } from "vitest";
import { corpusStore } from "./corpusStore.js";

describe("Corpus Store", () => {
  beforeEach(() => {
    corpusStore.reset();
  });

  describe("getCorpus", () => {
    it("should load corpus on first access", () => {
      const corpus = corpusStore.getCorpus();
      expect(corpus).toBeDefined();
      expect(corpus.regulations.length).toBeGreaterThan(0);
      expect(corpus.controls.length).toBeGreaterThan(0);
    });

    it("should cache corpus after first load", () => {
      const corpus1 = corpusStore.getCorpus();
      const corpus2 = corpusStore.getCorpus();
      expect(corpus1).toBe(corpus2); // Same object reference
    });

    it("should reload corpus after reset", () => {
      const corpus1 = corpusStore.getCorpus();
      corpusStore.reset();
      const corpus2 = corpusStore.getCorpus();
      expect(corpus1).not.toBe(corpus2); // Different object reference
    });
  });

  describe("getRegulations", () => {
    it("should return all regulations", () => {
      const regulations = corpusStore.getRegulations();
      expect(regulations.length).toBeGreaterThanOrEqual(9);
    });
  });

  describe("getRegulation", () => {
    it("should return regulation by ID", () => {
      const regulation = corpusStore.getRegulation("CRR3");
      expect(regulation).toBeDefined();
      expect(regulation?.id).toBe("CRR3");
      expect(regulation?.title).toContain("Capital Requirements");
    });

    it("should return undefined for non-existent regulation", () => {
      const regulation = corpusStore.getRegulation("NON_EXISTENT");
      expect(regulation).toBeUndefined();
    });
  });

  describe("getControls", () => {
    it("should return all controls", () => {
      const controls = corpusStore.getControls();
      expect(controls.length).toBeGreaterThanOrEqual(15);
    });
  });

  describe("getControl", () => {
    it("should return control by ID", () => {
      const control = corpusStore.getControl("RWA-CALC-001");
      expect(control).toBeDefined();
      expect(control?.id).toBe("RWA-CALC-001");
      expect(control?.title).toContain("RWA Calculation");
    });

    it("should return undefined for non-existent control", () => {
      const control = corpusStore.getControl("NON-EXISTENT-001");
      expect(control).toBeUndefined();
    });
  });

  describe("getControlsByKeyword", () => {
    it("should return controls for valid keyword", () => {
      const controls = corpusStore.getControlsByKeyword("rwa");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.some((c) => c.id.startsWith("RWA-"))).toBe(true);
    });

    it("should return empty array for non-existent keyword", () => {
      const controls = corpusStore.getControlsByKeyword("nonexistent");
      expect(controls).toEqual([]);
    });

    it("should be case-insensitive", () => {
      const controls1 = corpusStore.getControlsByKeyword("RWA");
      const controls2 = corpusStore.getControlsByKeyword("rwa");
      expect(controls1.length).toBe(controls2.length);
    });
  });

  describe("getControlsByArtifactType", () => {
    it("should return controls for feature artifact", () => {
      const controls = corpusStore.getControlsByArtifactType("feature");
      expect(controls.length).toBeGreaterThan(0);
    });

    it("should return controls for release_readiness artifact", () => {
      const controls =
        corpusStore.getControlsByArtifactType("release_readiness");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.some((c) => c.id === "RWA-CALC-001")).toBe(true);
    });

    it("should return empty array for non-existent artifact type", () => {
      const controls = corpusStore.getControlsByArtifactType("nonexistent");
      expect(controls).toEqual([]);
    });
  });

  describe("getRegulationsByDomain", () => {
    it("should return regulations for capital_adequacy domain", () => {
      const regulations = corpusStore.getRegulationsByDomain("capital_adequacy");
      expect(regulations.length).toBeGreaterThan(0);
      expect(regulations.some((r) => r.id === "CRR3")).toBe(true);
    });

    it("should return regulations for ict_security domain", () => {
      const regulations = corpusStore.getRegulationsByDomain("ict_security");
      expect(regulations.length).toBeGreaterThan(0);
      expect(regulations.some((r) => r.id === "DORA")).toBe(true);
    });

    it("should return empty array for non-existent domain", () => {
      const regulations = corpusStore.getRegulationsByDomain("nonexistent");
      expect(regulations).toEqual([]);
    });
  });

  describe("getControlsBySeverity", () => {
    it("should return critical controls", () => {
      const controls = corpusStore.getControlsBySeverity("critical");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.every((c) => c.severity === "critical")).toBe(true);
    });

    it("should return high severity controls", () => {
      const controls = corpusStore.getControlsBySeverity("high");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.every((c) => c.severity === "high")).toBe(true);
    });
  });

  describe("getControlsByDomain", () => {
    it("should return controls for capital_adequacy domain", () => {
      const controls = corpusStore.getControlsByDomain("capital_adequacy");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.some((c) => c.id === "RWA-CALC-001")).toBe(true);
    });

    it("should return controls for ict_security domain", () => {
      const controls = corpusStore.getControlsByDomain("ict_security");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.some((c) => c.id.startsWith("SEC-"))).toBe(true);
    });
  });

  describe("getRegulationsByJurisdiction", () => {
    it("should return EU regulations", () => {
      const regulations = corpusStore.getRegulationsByJurisdiction("EU");
      expect(regulations.length).toBeGreaterThan(0);
      expect(regulations.some((r) => r.id === "CRR3")).toBe(true);
      expect(regulations.some((r) => r.id === "DORA")).toBe(true);
    });

    it("should return GLOBAL regulations", () => {
      const regulations = corpusStore.getRegulationsByJurisdiction("GLOBAL");
      expect(regulations.length).toBeGreaterThan(0);
      expect(regulations.some((r) => r.id === "BCBS239")).toBe(true);
    });

    it("should return INTERNAL regulations", () => {
      const regulations = corpusStore.getRegulationsByJurisdiction("INTERNAL");
      expect(regulations.length).toBeGreaterThan(0);
      expect(regulations.some((r) => r.id === "INTERNAL_SDLC")).toBe(true);
    });
  });

  describe("searchControls", () => {
    it("should find controls by title", () => {
      const controls = corpusStore.searchControls("calculation");
      expect(controls.length).toBeGreaterThan(0);
      expect(controls.some((c) => c.id === "RWA-CALC-001")).toBe(true);
    });

    it("should find controls by description", () => {
      const controls = corpusStore.searchControls("audit trail");
      expect(controls.length).toBeGreaterThan(0);
    });

    it("should be case-insensitive", () => {
      const controls1 = corpusStore.searchControls("CALCULATION");
      const controls2 = corpusStore.searchControls("calculation");
      expect(controls1.length).toBe(controls2.length);
    });
  });

  describe("searchRegulations", () => {
    it("should find regulations by title", () => {
      const regulations = corpusStore.searchRegulations("capital");
      expect(regulations.length).toBeGreaterThan(0);
      expect(regulations.some((r) => r.id === "CRR3")).toBe(true);
    });

    it("should find regulations by summary", () => {
      const regulations = corpusStore.searchRegulations("basel");
      expect(regulations.length).toBeGreaterThan(0);
    });

    it("should be case-insensitive", () => {
      const regulations1 = corpusStore.searchRegulations("CAPITAL");
      const regulations2 = corpusStore.searchRegulations("capital");
      expect(regulations1.length).toBe(regulations2.length);
    });
  });

  describe("getStats", () => {
    it("should return corpus statistics", () => {
      const stats = corpusStore.getStats();
      expect(stats.regulationCount).toBeGreaterThanOrEqual(9);
      expect(stats.controlCount).toBeGreaterThanOrEqual(15);
      expect(stats.keywordMappingCount).toBeGreaterThan(0);
      expect(stats.artifactMappingCount).toBeGreaterThan(0);
      expect(stats.domainMappingCount).toBeGreaterThan(0);
    });
  });
});

// Made with Bob
