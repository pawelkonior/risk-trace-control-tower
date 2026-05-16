# RWA Regulatory Workflow Skill

Use this workflow for regulated RWA Control Tower work.

1. Context: call `bankRegulatoryControls.search_regulations` and `bankRegulatoryControls.match_controls`.
2. Planning: generate acceptance criteria, lineage requirements, audit log requirements, and test obligations.
3. Build: include rule versioning, source references, lineage fields, audit events, validation, and no-PII logging.
4. Review gate: call the relevant review tool and resolve blocking findings.
5. Ship evidence: call `assess_release_readiness` and generate the regulatory mapping report.

Never present MCP output as legal advice or certification. Always require qualified human review for regulatory interpretation and production release.
