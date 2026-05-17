from __future__ import annotations

import logging
from typing import Any

from .config import GuardrailConfig
from .privacy import find_pii, has_prompt_injection_risk
from .schemas import GuardrailResult

logger = logging.getLogger(__name__)


class GuardrailService:
    """
    Guardrail service with LLM Guard integration.

    Provides input/output scanning at all LLM boundaries with configurable
    scanners for PII, prompt injection, secrets, and toxicity detection.
    Falls back to local privacy checks when LLM Guard is disabled.
    """

    def __init__(self, config: GuardrailConfig | None = None) -> None:
        """
        Initialize guardrail service with configuration.

        Args:
            config: Guardrail configuration. If None, loads from environment.
        """
        self.config = config or GuardrailConfig.from_env()
        self.scanner_name = "llm_guard" if self.config.llm_guard_enabled else "local"
        self._input_scanners: list[Any] = []
        self._output_scanners: list[Any] = []

        if self.config.llm_guard_enabled:
            self._init_llm_guard_scanners()

        logger.info(
            "GuardrailService initialized with scanner=%s, enabled=%s",
            self.scanner_name,
            self.config.llm_guard_enabled,
        )

    def _init_llm_guard_scanners(self) -> None:
        """Initialize LLM Guard scanners based on configuration."""
        try:
            # Import LLM Guard scanners only when enabled
            from llm_guard.input_scanners import (
                PromptInjection,
                Secrets,
                TokenLimit,
            )
            from llm_guard.output_scanners import (
                NoRefusal,
                Relevance,
                Sensitive,
            )

            # Initialize input scanners
            if self.config.llm_guard_block_on_prompt_injection:
                self._input_scanners.append(PromptInjection(threshold=0.75))

            if self.config.llm_guard_block_on_secrets:
                self._input_scanners.append(Secrets())

            # Token limit to prevent excessive input
            self._input_scanners.append(TokenLimit(limit=4096, encoding_name="cl100k_base"))

            # Initialize output scanners
            if self.config.llm_guard_block_on_pii:
                self._output_scanners.append(
                    Sensitive(
                        entity_types=[
                            "EMAIL_ADDRESS",
                            "PHONE_NUMBER",
                            "PERSON",
                            "IBAN_CODE",
                            "CREDIT_CARD",
                        ],
                        redact=False,
                    )
                )

            # Check for refusals and relevance
            self._output_scanners.append(NoRefusal(threshold=0.75))
            self._output_scanners.append(Relevance(threshold=0.5))

            logger.info(
                "LLM Guard scanners initialized: input=%d, output=%d",
                len(self._input_scanners),
                len(self._output_scanners),
            )
        except ImportError as exc:
            logger.warning(
                "LLM Guard library not available, falling back to local checks: %s",
                exc,
            )
            self.config.llm_guard_enabled = False
            self.scanner_name = "local"

    def scan(self, stage: str, payload: Any) -> GuardrailResult:
        """
        Scan payload for safety and compliance issues.

        Args:
            stage: Scanning stage identifier (e.g., "input", "output", "final_output")
            payload: Content to scan (string, dict, or Pydantic model)

        Returns:
            GuardrailResult with scan outcome and metadata
        """
        if self.config.llm_guard_enabled and self._input_scanners:
            return self._scan_with_llm_guard(stage, payload)
        return self._scan_with_local_checks(stage, payload)

    def _scan_with_llm_guard(self, stage: str, payload: Any) -> GuardrailResult:
        """Scan using LLM Guard scanners."""
        try:
            from llm_guard import scan_output, scan_prompt

            # Convert payload to string for scanning
            text = self._payload_to_text(payload)

            # Determine scanner set based on stage
            is_output_stage = stage in {"output", "final_output", "worker_outputs"}
            scanners = self._output_scanners if is_output_stage else self._input_scanners

            # Run appropriate scan
            if is_output_stage:
                _sanitized_output, results_valid, results_score = scan_output(scanners, "", text)
            else:
                _sanitized_prompt, results_valid, results_score = scan_prompt(scanners, text)

            # Extract categories from results
            categories: list[str] = []
            max_risk = 0.0

            for scanner_name, is_valid in results_valid.items():
                if not is_valid:
                    scanner_lower = scanner_name.lower()
                    if "injection" in scanner_lower:
                        categories.append("prompt_injection")
                    elif "secret" in scanner_lower:
                        categories.append("secrets")
                    elif "sensitive" in scanner_lower or "pii" in scanner_lower:
                        categories.append("pii")
                    elif "toxic" in scanner_lower:
                        categories.append("toxicity")

                    # Get risk score for this scanner
                    score = results_score.get(scanner_name, 1.0)
                    max_risk = max(max_risk, score)

            blocked = max_risk >= 0.75 or not all(results_valid.values())

            if blocked and self.config.llm_guard_fail_fast:
                message = f"LLM Guard blocked content: {', '.join(categories)}"
            elif categories:
                message = f"LLM Guard flagged: {', '.join(categories)}"
            else:
                message = "LLM Guard scan passed"

            return GuardrailResult(
                stage=stage,
                scanner=self.scanner_name,
                passed=not blocked,
                blocked=blocked,
                risk_score=max_risk,
                categories=categories,
                message=message,
            )

        except Exception as exc:
            logger.error("LLM Guard scan failed, falling back to local checks: %s", exc)
            return self._scan_with_local_checks(stage, payload)

    def _scan_with_local_checks(self, stage: str, payload: Any) -> GuardrailResult:
        """Scan using local privacy checks (fallback mode)."""
        pii_findings = find_pii(payload)
        injection_risk = has_prompt_injection_risk(payload)

        categories: list[str] = []
        if pii_findings:
            categories.append("pii")
        if injection_risk > 0:
            categories.append("prompt_injection")

        risk_score = max(1.0 if pii_findings else 0.0, injection_risk)
        blocked = risk_score >= 0.75

        message = "passed"
        if blocked:
            message = "blocked unsafe or non-compliant content"
        elif categories:
            message = "reviewable guardrail signal detected"

        return GuardrailResult(
            stage=stage,
            scanner=self.scanner_name,
            passed=not blocked,
            blocked=blocked,
            risk_score=risk_score,
            categories=categories,
            message=message,
        )

    def _payload_to_text(self, payload: Any) -> str:
        """Convert payload to text for scanning."""
        if isinstance(payload, str):
            return payload

        if hasattr(payload, "model_dump_json"):
            # Pydantic model
            return payload.model_dump_json()

        if isinstance(payload, dict):
            # Extract text from dict recursively
            texts: list[str] = []
            self._extract_text_from_dict(payload, texts)
            return " ".join(texts)

        return str(payload)

    def _extract_text_from_dict(self, data: dict[str, Any], texts: list[str]) -> None:
        """Recursively extract text from dictionary."""
        for value in data.values():
            if isinstance(value, str):
                texts.append(value)
            elif isinstance(value, dict):
                self._extract_text_from_dict(value, texts)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        texts.append(item)
                    elif isinstance(item, dict):
                        self._extract_text_from_dict(item, texts)


# Made with Bob
