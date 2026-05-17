from __future__ import annotations

import hashlib
import logging
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry with value and expiration time."""

    value: Any
    expires_at: float


class TokenOptimizer:
    """
    LLM response cache with TTL and LRU eviction.

    Caches LLM responses by prompt+model hash to reduce token usage and costs.
    Thread-safe implementation with configurable cache size and TTL.
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600) -> None:
        """
        Initialize token optimizer cache.

        Args:
            max_size: Maximum number of cached entries (default: 1000)
            ttl_seconds: Time-to-live for cache entries in seconds (default: 3600)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

        logger.info(
            "TokenOptimizer initialized with max_size=%d, ttl_seconds=%d",
            max_size,
            ttl_seconds,
        )

    def cached_llm_call(
        self,
        prompt: str,
        model_id: str,
        llm_callable: Callable[..., Any],
        **kwargs: Any,
    ) -> Any:
        """
        Execute LLM call with caching.

        Args:
            prompt: Input prompt text
            model_id: Model identifier
            llm_callable: Function to call if cache miss
            **kwargs: Additional arguments passed to llm_callable

        Returns:
            Cached or fresh LLM response
        """
        cache_key = self._compute_cache_key(prompt, model_id)

        # Try to get from cache
        with self._lock:
            if cache_key in self._cache:
                entry = self._cache[cache_key]
                current_time = time.time()

                # Check if entry is still valid
                if current_time < entry.expires_at:
                    # Move to end (LRU)
                    self._cache.move_to_end(cache_key)
                    self._hits += 1
                    logger.debug("Cache hit for key=%s (hits=%d)", cache_key[:12], self._hits)
                    return entry.value
                # Entry expired, remove it
                del self._cache[cache_key]
                logger.debug("Cache entry expired for key=%s", cache_key[:12])

        # Cache miss - call LLM
        self._misses += 1
        logger.debug("Cache miss for key=%s (misses=%d)", cache_key[:12], self._misses)

        response = llm_callable(**kwargs)

        # Store in cache
        with self._lock:
            expires_at = time.time() + self.ttl_seconds
            self._cache[cache_key] = CacheEntry(value=response, expires_at=expires_at)
            self._cache.move_to_end(cache_key)

            # Evict oldest entry if cache is full
            if len(self._cache) > self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                logger.debug("Cache full, evicted oldest entry: %s", oldest_key[:12])

        return response

    def _compute_cache_key(self, prompt: str, model_id: str) -> str:
        """
        Compute cache key from prompt and model ID.

        Args:
            prompt: Input prompt text
            model_id: Model identifier

        Returns:
            SHA256 hash of prompt+model
        """
        content = f"{prompt}|{model_id}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def get_stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache hits, misses, size, and hit rate
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

            return {
                "hits": self._hits,
                "misses": self._misses,
                "size": len(self._cache),
                "max_size": self.max_size,
                "hit_rate": hit_rate,
                "total_requests": total_requests,
            }

    def clear(self) -> None:
        """Clear all cache entries and reset statistics."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            logger.info("Cache cleared")

    def invalidate(self, prompt: str, model_id: str) -> bool:
        """
        Invalidate a specific cache entry.

        Args:
            prompt: Input prompt text
            model_id: Model identifier

        Returns:
            True if entry was found and removed, False otherwise
        """
        cache_key = self._compute_cache_key(prompt, model_id)

        with self._lock:
            if cache_key in self._cache:
                del self._cache[cache_key]
                logger.debug("Cache entry invalidated: %s", cache_key[:12])
                return True

        return False


# Made with Bob
