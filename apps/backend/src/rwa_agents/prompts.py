from __future__ import annotations

import os

from .schemas import PromptUsage

LOCAL_PROMPTS = {
    "data_analyst": (
        "Analyze anonymized RWA inputs for data quality issues using deterministic tools first."
    ),
    "risk_expert": ("Analyze deterministic RWA validation results and portfolio risk drivers."),
    "supervisor": "Synthesize safe structured executive, CRO, and CFO commentary.",
}


class PromptRegistry:
    """Prompt registry with local fallback and optional Langfuse metadata."""

    def __init__(self) -> None:
        self.langfuse_enabled = _langfuse_enabled()

    def get(self, prompt_name: str) -> tuple[str, PromptUsage]:
        source = "langfuse" if self.langfuse_enabled else "local"
        # Hosted prompt fetching is intentionally disabled-safe for local/test runs.
        return LOCAL_PROMPTS[prompt_name], PromptUsage(
            prompt_name=prompt_name,
            prompt_version="local-v1",
            source=source,
        )


def _langfuse_enabled() -> bool:
    return os.getenv("RWA_LANGFUSE_ENABLED", "").strip().lower() in {"1", "true", "yes"}
