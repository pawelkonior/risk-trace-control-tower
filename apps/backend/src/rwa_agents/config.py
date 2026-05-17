from __future__ import annotations

import os

from pydantic import BaseModel, Field


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


class RwaAgentsConfig(BaseModel):
    """Combined configuration for RWA agents workflow."""

    guardrails: GuardrailConfig = Field(default_factory=GuardrailConfig)
    langfuse: LangfuseConfig = Field(default_factory=LangfuseConfig)

    @classmethod
    def from_env(cls) -> RwaAgentsConfig:
        """Load complete configuration from environment variables."""
        return cls(
            guardrails=GuardrailConfig.from_env(),
            langfuse=LangfuseConfig.from_env(),
        )


def _parse_bool(value: str) -> bool:
    """Parse boolean from environment variable string."""
    return value.strip().lower() in {"1", "true", "yes", "on"}


# Made with Bob
