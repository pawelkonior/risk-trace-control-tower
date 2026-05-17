from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryStrategy:
    """
    Retry strategy with exponential backoff for transient errors.
    
    Handles network errors, timeouts, and rate limits with configurable
    retry attempts and backoff delays. Integrates with observability
    for tracking retry attempts.
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0,
        observability: Any | None = None,
    ) -> None:
        """
        Initialize retry strategy.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds before first retry
            max_delay: Maximum delay in seconds between retries
            exponential_base: Base for exponential backoff calculation
            observability: Optional observability service for tracking retries
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.observability = observability

    def retry_with_backoff(
        self,
        func: Callable[..., T],
        *args: Any,
        node: str = "unknown",
        agent: str | None = None,
        **kwargs: Any,
    ) -> T:
        """
        Execute function with exponential backoff retry on transient errors.
        
        Args:
            func: Function to execute
            *args: Positional arguments for function
            node: Node name for observability tracking
            agent: Agent name for observability tracking
            **kwargs: Keyword arguments for function
            
        Returns:
            Function result
            
        Raises:
            Exception: If all retry attempts fail
        """
        last_exception: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                result = func(*args, **kwargs)

                # Log successful retry if not first attempt
                if attempt > 0:
                    logger.info(
                        "Retry succeeded on attempt %d/%d for %s",
                        attempt + 1,
                        self.max_retries + 1,
                        node,
                    )

                    if self.observability:
                        try:
                            self.observability.record_error(
                                error=last_exception or Exception("Transient error"),
                                node=node,
                                agent=agent,
                                retry_count=attempt,
                                recovered=True,
                                recovery_strategy="exponential_backoff_retry",
                            )
                        except Exception:
                            pass

                return result

            except Exception as exc:
                last_exception = exc

                # Check if error is retryable
                if not self._is_retryable_error(exc):
                    logger.warning(
                        "Non-retryable error in %s: %s",
                        node,
                        type(exc).__name__,
                    )
                    raise

                # Check if we have retries left
                if attempt >= self.max_retries:
                    logger.error(
                        "All retry attempts exhausted for %s after %d attempts",
                        node,
                        attempt + 1,
                    )

                    if self.observability:
                        try:
                            self.observability.record_error(
                                error=exc,
                                node=node,
                                agent=agent,
                                retry_count=attempt,
                                recovered=False,
                                recovery_strategy="exponential_backoff_retry",
                            )
                        except Exception:
                            pass

                    raise

                # Calculate backoff delay
                delay = self._calculate_delay(attempt)

                logger.warning(
                    "Retryable error in %s (attempt %d/%d): %s. Retrying in %.2fs...",
                    node,
                    attempt + 1,
                    self.max_retries + 1,
                    type(exc).__name__,
                    delay,
                )

                # Wait before retry
                time.sleep(delay)

        # Should never reach here, but satisfy type checker
        if last_exception:
            raise last_exception
        raise RuntimeError("Retry logic error: no exception to raise")

    def _calculate_delay(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay for retry attempt.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        delay = self.base_delay * (self.exponential_base ** attempt)
        return min(delay, self.max_delay)

    def _is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if an error is retryable.
        
        Args:
            error: Exception to check
            
        Returns:
            True if error is retryable, False otherwise
        """
        error_type = type(error).__name__
        error_message = str(error).lower()

        # Network and connection errors
        retryable_types = {
            "ConnectionError",
            "TimeoutError",
            "Timeout",
            "ConnectTimeout",
            "ReadTimeout",
            "HTTPError",
            "RequestException",
            "URLError",
        }

        if error_type in retryable_types:
            return True

        # Rate limit errors
        rate_limit_indicators = [
            "rate limit",
            "too many requests",
            "429",
            "quota exceeded",
            "throttle",
        ]

        if any(indicator in error_message for indicator in rate_limit_indicators):
            return True

        # Temporary service errors
        temp_error_indicators = [
            "503",
            "service unavailable",
            "temporarily unavailable",
            "try again",
        ]

        if any(indicator in error_message for indicator in temp_error_indicators):
            return True

        # WatsonX specific transient errors
        watsonx_transient = [
            "watsonx",
            "watson",
            "ibm cloud",
        ]

        if any(indicator in error_message for indicator in watsonx_transient):
            # Only retry if it looks like a transient error
            if any(temp in error_message for temp in ["timeout", "unavailable", "connection"]):
                return True

        return False


# Made with Bob
