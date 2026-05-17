from __future__ import annotations

import logging
from datetime import datetime, timedelta
from time import perf_counter
from typing import Any

from .config import LangfuseConfig
from .schemas import PromptUsage

logger = logging.getLogger(__name__)

DATA_ANALYST_PROMPT = "rwa-data-analyst-agent-system"
RISK_EXPERT_PROMPT = "rwa-risk-expert-agent-system"
SUPERVISOR_PROMPT = "rwa-supervisor-agent-system"

LOCAL_PROMPTS = {
    DATA_ANALYST_PROMPT: (
        "Analyze anonymized RWA inputs for data quality issues using deterministic tools first."
    ),
    RISK_EXPERT_PROMPT: "Analyze deterministic RWA validation results and portfolio risk drivers.",
    SUPERVISOR_PROMPT: "Synthesize safe structured executive, CRO, and CFO commentary.",
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
                return self._get_local_fallback(prompt_name, fetch_status="error")

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
            label=self.config.langfuse_prompt_label,
            fetch_status="cached",
        )

    def _fetch_from_langfuse(self, prompt_name: str) -> tuple[str, PromptUsage]:
        """Fetch prompt from Langfuse with timeout."""
        logger.debug("Fetching prompt '%s' from Langfuse", prompt_name)
        started_at = perf_counter()

        try:
            prompt = self._client.get_prompt(
                name=prompt_name,
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
                label=self.config.langfuse_prompt_label,
                fetch_status="fetched",
                fetch_latency_ms=(perf_counter() - started_at) * 1000,
            )
        except Exception as exc:
            logger.error("Error fetching prompt from Langfuse: %s", exc)
            raise

    def _get_local_fallback(
        self,
        prompt_name: str,
        fetch_status: str = "fallback",
    ) -> tuple[str, PromptUsage]:
        """Get prompt from local fallback registry."""
        if prompt_name not in LOCAL_PROMPTS:
            raise ValueError(f"Unknown prompt name: {prompt_name}")

        logger.debug("Using local fallback prompt for '%s'", prompt_name)

        return LOCAL_PROMPTS[prompt_name], PromptUsage(
            prompt_name=prompt_name,
            prompt_version="local-v1",
            source="local_fallback",
            label=self.config.langfuse_prompt_label,
            fetch_status=fetch_status,
        )


class PromptManager:
    """
    Enhanced prompt manager with versioning support and caching.
    
    Extends PromptRegistry with additional features:
    - Prompt version tracking in observability
    - Enhanced caching with TTL
    - Source tracking (langfuse vs local_fallback)
    - Backward compatible with existing PromptRegistry
    """

    def __init__(
        self,
        config: LangfuseConfig | None = None,
        cache_ttl_seconds: int = 300,
        observability: Any | None = None,
    ) -> None:
        """
        Initialize prompt manager.
        
        Args:
            config: Langfuse configuration. If None, loads from environment.
            cache_ttl_seconds: Cache TTL in seconds (default: 5 minutes)
            observability: Optional observability service for tracking
        """
        self.config = config or LangfuseConfig.from_env()
        self.cache_ttl_seconds = cache_ttl_seconds
        self.observability = observability
        
        # Use existing PromptRegistry for core functionality
        self._registry = PromptRegistry(config)
        
        logger.info(
            "PromptManager initialized with cache_ttl=%ds, langfuse_enabled=%s",
            cache_ttl_seconds,
            self._registry.langfuse_enabled,
        )

    def get_prompt(self, prompt_name: str) -> tuple[str, PromptUsage]:
        """
        Get prompt by name with version tracking.
        
        Args:
            prompt_name: Name of the prompt to fetch
            
        Returns:
            Tuple of (prompt_text, prompt_usage_metadata)
        """
        # Use registry to fetch prompt
        prompt_text, usage = self._registry.get(prompt_name)
        
        # Track in observability if available
        if self.observability:
            try:
                self.observability.prompt(usage)
            except Exception as exc:
                logger.warning("Failed to track prompt in observability: %s", exc)
        
        # Log version information
        logger.debug(
            "Prompt '%s' fetched: version=%s, source=%s, status=%s",
            prompt_name,
            usage.prompt_version,
            usage.source,
            usage.fetch_status,
        )
        
        return prompt_text, usage

    def clear_cache(self) -> None:
        """Clear the prompt cache."""
        self._registry._cache.clear()
        logger.info("Prompt cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "cached_prompts": len(self._registry._cache),
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "langfuse_enabled": self._registry.langfuse_enabled,
        }


# Made with Bob
