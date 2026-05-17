# RCT-40 Watsonx Runtime Finalization

The RWA executive commentary API supports an opt-in IBM watsonx.ai synthesis path while
preserving deterministic RWA validation as the source of truth.

## Runtime Contract

- Default mode is deterministic: `RWA_AGENTS_LLM_PROVIDER=deterministic`.
- External LLM calls occur only when `RWA_AGENTS_LLM_PROVIDER=watsonx` and watsonx credentials
  are configured.
- Deterministic Python tools run before any LLM interpretation.
- The LLM receives summarized counts, totals, findings, flags, actions, and deterministic
  baseline commentary, not raw full portfolio rows.
- The watsonx prompt instructs the model not to calculate RWA formulas and to return only JSON
  fields `executive_summary`, `cro_view`, and `cfo_view`.
- Malformed watsonx responses and provider failures fall back to deterministic commentary.
- Unsafe LLM prompt, LLM output, or final commentary is blocked before frontend display.

## Configuration

Required for watsonx runtime:

```text
RWA_AGENTS_LLM_PROVIDER=watsonx
WATSONX_PROJECT_ID=<IBM watsonx.ai project id>
WATSONX_APIKEY=<IBM Cloud IAM API key>
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
RWA_AGENTS_WATSONX_MODEL_ID=meta-llama/llama-3-3-70b-instruct
```

`apps/backend/.env.example` contains placeholders only. Secrets must remain in ignored local
`.env` files, container secret management, or CI/CD secret stores.

## Observability

The API response keeps stable fields and includes:

- `observability.llm_call_count`
- `observability.total_token_count`
- `observability.guardrail_results`
- `observability.guardrail_block_count`

No API response exposes `llm_guard_enabled`, watsonx credentials, or raw provider error details.

## Validation

Targeted gates for this task:

```powershell
cd apps/backend
uv run pytest tests/agents --no-cov -q
uv run ruff check src/rwa_agents tests/agents
uv run ruff format --check src/rwa_agents tests/agents
uv run mypy
```

Direct IBM Cloud smoke testing should be run only with valid local credentials and must not print
or commit secrets.
