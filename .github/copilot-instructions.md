# Copilot Instructions

For RWA, regulatory reporting, rule governance, audit, data lineage, or release evidence work, use `bankRegulatoryControls` before producing Jira, GitHub, Confluence, architecture, or release output.

Required checks:

- Run `match_controls` for feature, architecture, code diff, and release artifacts.
- Run `review_feature_description`, `review_architecture_text`, or `review_code_diff` before regulated implementation or review output.
- Run `assess_release_readiness` before release approval or release-note output.
- Require explicit confirmation before Jira, GitHub, or Confluence writes.
- Block RWA work that lacks rule versioning, data lineage, audit logging, regulatory tests, or release evidence.
- Do not claim legal compliance, legal advice, or regulatory certification. Require qualified human review.

RWA implementation must include:

- `rule_version`
- `regulation_reference`
- `calculation_trace_id`
- `input_hash`
- `source_system`
- `reporting_date`
- audit events for upload, validate, calculate, and export
- no PII in logs
- reproducible tests and retained release evidence
