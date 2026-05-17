from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field

_LOCAL_ENV_LOADED = False


class GuardrailConfig(BaseModel):
    """Configuration for LLM Guard guardrails."""

    llm_guard_enabled: bool = Field(
        default=True,
        description="Enable LLM Guard scanning at all LLM boundaries",
    )
    llm_guard_fail_fast: bool = Field(
        default=True,
        description="Stop workflow immediately on guardrail block",
    )
    llm_guard_block_on_prompt_injection: bool = Field(
        default=True,
        description="Block requests/responses with prompt injection patterns",
    )
    llm_guard_block_on_pii: bool = Field(
        default=True,
        description="Block requests/responses containing PII",
    )
    llm_guard_block_on_secrets: bool = Field(
        default=True,
        description="Block requests/responses containing secrets",
    )
    llm_guard_input_timeout_seconds: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Timeout for input scanning operations",
    )
    llm_guard_output_timeout_seconds: int = Field(
        default=30,
        ge=1,
        le=120,
        description="Timeout for output scanning operations",
    )

    @classmethod
    def from_env(cls) -> GuardrailConfig:
        """Load guardrail configuration from environment variables."""
        _load_local_env_files()
        return cls(
            llm_guard_enabled=_parse_bool(os.getenv("RWA_LLM_GUARD_ENABLED", "true")),
            llm_guard_fail_fast=_parse_bool(os.getenv("RWA_LLM_GUARD_FAIL_FAST", "true")),
            llm_guard_block_on_prompt_injection=_parse_bool(
                os.getenv("RWA_LLM_GUARD_BLOCK_ON_PROMPT_INJECTION", "true")
            ),
            llm_guard_block_on_pii=_parse_bool(os.getenv("RWA_LLM_GUARD_BLOCK_ON_PII", "true")),
            llm_guard_block_on_secrets=_parse_bool(
                os.getenv("RWA_LLM_GUARD_BLOCK_ON_SECRETS", "true")
            ),
            llm_guard_input_timeout_seconds=int(
                os.getenv("RWA_LLM_GUARD_INPUT_TIMEOUT_SECONDS", "10")
            ),
            llm_guard_output_timeout_seconds=int(
                os.getenv("RWA_LLM_GUARD_OUTPUT_TIMEOUT_SECONDS", "30")
            ),
        )


class LangfuseConfig(BaseModel):
    """Configuration for Langfuse observability."""

    langfuse_enabled: bool = Field(
        default=False,
        description="Enable Langfuse tracing and observability",
    )
    langfuse_public_key: str | None = Field(
        default=None,
        description="Langfuse public API key",
    )
    langfuse_secret_key: str | None = Field(
        default=None,
        description="Langfuse secret API key",
    )
    langfuse_base_url: str = Field(
        default="https://cloud.langfuse.com",
        description="Langfuse API base URL",
    )
    langfuse_prompt_label: str = Field(
        default="production",
        description="Label for fetching prompts from Langfuse",
    )
    langfuse_prompt_cache_ttl_seconds: int = Field(
        default=300,
        ge=0,
        le=3600,
        description="TTL for cached prompts in seconds",
    )
    langfuse_prompt_fetch_timeout_seconds: int = Field(
        default=5,
        ge=1,
        le=30,
        description="Timeout for prompt fetch operations",
    )

    @classmethod
    def from_env(cls) -> LangfuseConfig:
        """Load Langfuse configuration from environment variables."""
        _load_local_env_files()
        return cls(
            langfuse_enabled=_parse_bool(os.getenv("RWA_LANGFUSE_ENABLED", "false")),
            langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            langfuse_base_url=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
            langfuse_prompt_label=os.getenv("RWA_LANGFUSE_PROMPT_LABEL", "production"),
            langfuse_prompt_cache_ttl_seconds=int(
                os.getenv("RWA_LANGFUSE_PROMPT_CACHE_TTL_SECONDS", "300")
            ),
            langfuse_prompt_fetch_timeout_seconds=int(
                os.getenv("RWA_LANGFUSE_PROMPT_FETCH_TIMEOUT_SECONDS", "5")
            ),
        )

    def is_configured(self) -> bool:
        """Check if Langfuse is properly configured with credentials."""
        return (
            self.langfuse_enabled
            and self.langfuse_public_key is not None
            and self.langfuse_secret_key is not None
        )


class WatsonxConfig(BaseModel):
    """Configuration for IBM watsonx.ai LLM integration."""

    watsonx_project_id: str | None = Field(
        default=None,
        description="IBM watsonx.ai project ID",
    )
    watsonx_apikey: str | None = Field(
        default=None,
        description="IBM Cloud IAM API key",
    )
    watsonx_url: str = Field(
        default="https://eu-de.ml.cloud.ibm.com",
        description="Regional watsonx.ai endpoint URL",
    )
    watsonx_model_id: str = Field(
        default="meta-llama/llama-3-3-70b-instruct",
        description="Foundation model ID",
    )
    watsonx_api_version: str = Field(
        default="2024-03-14",
        description="Watsonx API version",
    )
    watsonx_max_new_tokens: int = Field(
        default=2048,
        ge=1,
        le=4096,
        description="Maximum tokens to generate",
    )
    watsonx_time_limit: int = Field(
        default=60000,
        ge=1000,
        le=300000,
        description="Generation time limit in milliseconds",
    )
    watsonx_http_timeout: int = Field(
        default=120,
        ge=10,
        le=300,
        description="HTTP request timeout in seconds",
    )

    @classmethod
    def from_env(cls) -> WatsonxConfig:
        """Load watsonx configuration from environment variables."""
        _load_local_env_files()
        # Support both prefixed and unprefixed env var names for .env compatibility
        return cls(
            watsonx_project_id=os.getenv("RWA_AGENTS_WATSONX_PROJECT_ID")
            or os.getenv("WATSONX_PROJECT_ID"),
            watsonx_apikey=os.getenv("RWA_AGENTS_WATSONX_APIKEY") or os.getenv("WATSONX_APIKEY"),
            watsonx_url=os.getenv("RWA_AGENTS_WATSONX_URL")
            or os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com"),
            watsonx_model_id=os.getenv("RWA_AGENTS_WATSONX_MODEL_ID")
            or os.getenv("WATSONX_MODEL_ID", "meta-llama/llama-3-3-70b-instruct"),
            watsonx_api_version=os.getenv("RWA_AGENTS_WATSONX_API_VERSION", "2024-03-14"),
            watsonx_max_new_tokens=int(os.getenv("RWA_AGENTS_WATSONX_MAX_NEW_TOKENS", "2048")),
            watsonx_time_limit=int(os.getenv("RWA_AGENTS_WATSONX_TIME_LIMIT", "60000")),
            watsonx_http_timeout=int(os.getenv("RWA_AGENTS_WATSONX_HTTP_TIMEOUT", "120")),
        )

    def is_configured(self) -> bool:
        """Check if watsonx is properly configured with credentials."""
        return (
            self.watsonx_project_id is not None
            and self.watsonx_apikey is not None
            and len(self.watsonx_project_id.strip()) > 0
            and len(self.watsonx_apikey.strip()) > 0
        )


class RwaAgentsConfig(BaseModel):
    """Combined configuration for RWA agents workflow."""

    llm_provider: str = Field(
        default="deterministic",
        description="LLM provider selection: 'deterministic' or 'watsonx'",
    )
    guardrails: GuardrailConfig = Field(default_factory=GuardrailConfig)
    langfuse: LangfuseConfig = Field(default_factory=LangfuseConfig)
    watsonx: WatsonxConfig = Field(default_factory=WatsonxConfig)

    @classmethod
    def from_env(cls) -> RwaAgentsConfig:
        """Load complete configuration from environment variables."""
        _load_local_env_files()
        return cls(
            llm_provider=os.getenv("RWA_AGENTS_LLM_PROVIDER", "deterministic").strip().lower(),
            guardrails=GuardrailConfig.from_env(),
            langfuse=LangfuseConfig.from_env(),
            watsonx=WatsonxConfig.from_env(),
        )

    @property
    def uses_watsonx(self) -> bool:
        """Return whether the external watsonx runtime was explicitly selected."""
        return self.llm_provider == "watsonx"

    @property
    def watsonx_configured(self) -> bool:
        """Expose watsonx credential readiness for tests and diagnostics."""
        return self.watsonx.is_configured()


def _parse_bool(value: str) -> bool:
    """Parse boolean from environment variable string."""
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_local_env_files() -> None:
    """
    Load ignored local .env files for developer/runtime convenience.

    Explicit process environment variables keep precedence over file values.
    """
    global _LOCAL_ENV_LOADED
    if _LOCAL_ENV_LOADED:
        return

    for env_file in _local_env_file_candidates():
        if not env_file.exists():
            continue
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            parsed = _parse_env_line(raw_line)
            if parsed is None:
                continue
            key, value = parsed
            os.environ.setdefault(key, value)

    _LOCAL_ENV_LOADED = True


def _local_env_file_candidates() -> tuple[Path, Path]:
    backend_root = Path(__file__).resolve().parents[2]
    apps_root = backend_root.parent
    return (apps_root / ".env", backend_root / ".env")


def _parse_env_line(raw_line: str) -> tuple[str, str] | None:
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None

    key, value = line.split("=", 1)
    key = key.strip()
    if key.startswith("export "):
        key = key.removeprefix("export ").strip()
    if not key:
        return None

    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key, value


# Made with Bob
