from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from .config import LangfuseConfig
from .schemas import PromptUsage

logger = logging.getLogger(__name__)

LOCAL_PROMPTS = {
    "data_analyst": (
        "Analyze anonymized RWA inputs for data quality issues using deterministic tools first."
    ),
    "risk_expert": ("Analyze deterministic RWA validation results and portfolio risk drivers."),
    "supervisor": "Synthesize safe structured executive, CRO, and CFO commentary.",
}


class PromptRegistry:
    """
    Prompt registry with Langfuse integration and local fallback.
    
    Fetches prompts from Langfuse when enabled and configured, with caching
    and automatic fallback to local prompts on error or when disabled.
    """

    def __init__(self, config: LangfuseConfig | None = None) -> None:
        """
        Initialize prompt registry with configuration.
        
        Args:
            config: Langfuse configuration. If None, loads from environment.
        """
        self.config = config or LangfuseConfig.from_env()
        self.langfuse_enabled = self.config.is_configured()
        self._cache: dict[str, tuple[str, datetime]] = {}
        self._client: Any = None
        
        if self.langfuse_enabled:
            self._init_langfuse_client()
        
        logger.info(
            "PromptRegistry initialized with langfuse_enabled=%s",
            self.langfuse_enabled,
        )

    def _init_langfuse_client(self) -> None:
        """Initialize Langfuse client if enabled and configured."""
        try:
            from langfuse import Langfuse
            
            self._client = Langfuse(
                public_key=self.config.langfuse_public_key,
                secret_key=self.config.langfuse_secret_key,
                host=self.config.langfuse_base_url,
            )
            logger.info("Langfuse client initialized successfully")
        except ImportError as exc:
            logger.warning(
                "Langfuse library not available, using local prompts only: %s",
                exc,
            )
            self.langfuse_enabled = False
        except Exception as exc:
            logger.error("Failed to initialize Langfuse client: %s", exc)
            self.langfuse_enabled = False

    def get(self, prompt_name: str) -> tuple[str, PromptUsage]:
        """
        Get prompt by name from Langfuse or local fallback.
        
        Args:
            prompt_name: Name of the prompt to fetch
            
        Returns:
            Tuple of (prompt_text, prompt_usage_metadata)
        """
        if self.langfuse_enabled and self._client:
            # Try cache first
            cached = self._get_from_cache(prompt_name)
            if cached:
                return cached
            
            # Try fetching from Langfuse
            try:
                return self._fetch_from_langfuse(prompt_name)
            except Exception as exc:
                logger.warning(
                    "Failed to fetch prompt '%s' from Langfuse, using local fallback: %s",
                    prompt_name,
                    exc,
                )
        
        # Fallback to local prompts
        return self._get_local_fallback(prompt_name)

    def _get_from_cache(self, prompt_name: str) -> tuple[str, PromptUsage] | None:
        """Get prompt from cache if not expired."""
        if prompt_name not in self._cache:
            return None
        
        prompt_text, cached_at = self._cache[prompt_name]
        ttl = timedelta(seconds=self.config.langfuse_prompt_cache_ttl_seconds)
        
        if datetime.now() - cached_at > ttl:
            # Cache expired
            del self._cache[prompt_name]
            return None
        
        logger.debug("Prompt '%s' retrieved from cache", prompt_name)
        return prompt_text, PromptUsage(
            prompt_name=prompt_name,
            prompt_version="cached",
            source="langfuse",
        )

    def _fetch_from_langfuse(self, prompt_name: str) -> tuple[str, PromptUsage]:
        """Fetch prompt from Langfuse with timeout."""
        logger.debug("Fetching prompt '%s' from Langfuse", prompt_name)
        
        # Map internal names to Langfuse prompt names
        langfuse_prompt_name = f"rwa-{prompt_name.replace('_', '-')}-agent-system"
        
        try:
            prompt = self._client.get_prompt(
                name=langfuse_prompt_name,
                label=self.config.langfuse_prompt_label,
            )
            
            prompt_text = prompt.prompt if hasattr(prompt, "prompt") else str(prompt)
            prompt_version = prompt.version if hasattr(prompt, "version") else "unknown"
            
            # Cache the fetched prompt
            self._cache[prompt_name] = (prompt_text, datetime.now())
            
            logger.info(
                "Fetched prompt '%s' (version %s) from Langfuse",
                prompt_name,
                prompt_version,
            )
            
            return prompt_text, PromptUsage(
                prompt_name=prompt_name,
                prompt_version=str(prompt_version),
                source="langfuse",
            )
        except Exception as exc:
            logger.error("Error fetching prompt from Langfuse: %s", exc)
            raise

    def _get_local_fallback(self, prompt_name: str) -> tuple[str, PromptUsage]:
        """Get prompt from local fallback registry."""
        if prompt_name not in LOCAL_PROMPTS:
            raise ValueError(f"Unknown prompt name: {prompt_name}")
        
        logger.debug("Using local fallback prompt for '%s'", prompt_name)
        
        return LOCAL_PROMPTS[prompt_name], PromptUsage(
            prompt_name=prompt_name,
            prompt_version="local-v1",
            source="local",
        )

# Made with Bob
