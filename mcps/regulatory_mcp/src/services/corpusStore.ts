import { loadCorpus, type RegulatoryCorpus } from "./corpusLoader.js";
import type { Regulation } from "../schemas/regulation.js";
import type { Control } from "../schemas/control.js";

/**
 * Singleton store for the regulatory corpus.
 * Loads corpus once on first access and caches it.
 */
class CorpusStore {
  private corpus: RegulatoryCorpus | null = null;

  /**
   * Get the corpus, loading it if necessary
   */
  getCorpus(): RegulatoryCorpus {
    if (!this.corpus) {
      this.corpus = loadCorpus();
    }
    return this.corpus;
  }

  /**
   * Reset the corpus cache (useful for testing)
   */
  reset(): void {
    this.corpus = null;
  }

  /**
   * Get all regulations
   */
  getRegulations(): Regulation[] {
    return this.getCorpus().regulations;
  }

  /**
   * Get regulation by ID
   */
  getRegulation(id: string): Regulation | undefined {
    return this.getRegulations().find((r) => r.id === id);
  }

  /**
   * Get all controls
   */
  getControls(): Control[] {
    return this.getCorpus().controls;
  }

  /**
   * Get control by ID
   */
  getControl(id: string): Control | undefined {
    return this.getControls().find((c) => c.id === id);
  }

  /**
   * Get controls by keyword
   */
  getControlsByKeyword(keyword: string): Control[] {
    const corpus = this.getCorpus();
    const controlIds = corpus.keywordMappings.mappings[keyword.toLowerCase()];
    if (!controlIds) {
      return [];
    }
    return controlIds
      .map((id) => this.getControl(id))
      .filter((c): c is Control => c !== undefined);
  }

  /**
   * Get controls by artifact type
   */
  getControlsByArtifactType(artifactType: string): Control[] {
    const corpus = this.getCorpus();
    const controlIds = corpus.artifactMappings.mappings[artifactType];
    if (!controlIds) {
      return [];
    }
    return controlIds
      .map((id) => this.getControl(id))
      .filter((c): c is Control => c !== undefined);
  }

  /**
   * Get regulations by domain
   */
  getRegulationsByDomain(domain: string): Regulation[] {
    const corpus = this.getCorpus();
    const regulationIds = corpus.domainMappings.mappings[domain];
    if (!regulationIds) {
      return [];
    }
    return regulationIds
      .map((id) => this.getRegulation(id))
      .filter((r): r is Regulation => r !== undefined);
  }

  /**
   * Get controls by severity
   */
  getControlsBySeverity(severity: string): Control[] {
    return this.getControls().filter((c) => c.severity === severity);
  }

  /**
   * Get controls by domain
   */
  getControlsByDomain(domain: string): Control[] {
    return this.getControls().filter((c) =>
      c.domains.some((controlDomain) => controlDomain === domain)
    );
  }

  /**
   * Get regulations by jurisdiction
   */
  getRegulationsByJurisdiction(jurisdiction: string): Regulation[] {
    return this.getRegulations().filter((r) => r.jurisdiction === jurisdiction);
  }

  /**
   * Search controls by text (title or description)
   */
  searchControls(query: string): Control[] {
    const lowerQuery = query.toLowerCase();
    return this.getControls().filter(
      (c) =>
        c.title.toLowerCase().includes(lowerQuery) ||
        c.description.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Search regulations by text (title or summary)
   */
  searchRegulations(query: string): Regulation[] {
    const lowerQuery = query.toLowerCase();
    return this.getRegulations().filter(
      (r) =>
        r.title.toLowerCase().includes(lowerQuery) ||
        r.summary.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Get corpus statistics
   */
  getStats() {
    const corpus = this.getCorpus();
    return {
      regulationCount: corpus.regulations.length,
      controlCount: corpus.controls.length,
      keywordMappingCount: Object.keys(corpus.keywordMappings.mappings).length,
      artifactMappingCount: Object.keys(corpus.artifactMappings.mappings)
        .length,
      domainMappingCount: Object.keys(corpus.domainMappings.mappings).length,
    };
  }
}

// Export singleton instance
export const corpusStore = new CorpusStore();

// Made with Bob
