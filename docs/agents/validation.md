# RWA Commentary Validation

Pre-graph validation rejects PII-like keys and values before AgentState construction.

Rejected field names include:

- `customer_name`
- `client_name`
- `borrower_name`
- `counterparty_name`
- `first_name`
- `last_name`
- `email`
- `phone`
- `address`
- `account_number`
- `iban`
- `ssn`
- `pesel`
- `passport`
- `tax_id`

Allowed anonymized identifiers use stable prefixes such as:

- `ASSET-001`
- `EXPOSURE-123`
- `PORTFOLIO-A`
- `RWA-ROW-001`

Quantitative validation uses deterministic Python tools only. The local validation rule
compares reported `rwa_amount` with `exposure_amount * risk_weight` when those fields are
available in the request. LLMs are not used to calculate formulas.

