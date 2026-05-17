from __future__ import annotations

import logging
from typing import Any

from .config import GuardrailConfig
from .privacy import find_pii, has_prompt_injection_risk
from .schemas import GuardrailResult

logger = logging.getLogger(__name__)

_SENSITIVE_ENTITY_TYPES = ["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD"]


def _sensitive_regex_patterns() -> list[dict[str, Any]]:
    """Limit LLM Guard custom sensitive regexes to PII, not dates or financial amounts."""
    return [
        {
            "expressions": [
                r"\b[A-Za-z0-9._%+-]+(\[AT\]|@)[A-Za-z0-9.-]+(\[DOT\]|\.)[A-Za-z]{2,}\b"
            ],
            "name": "EMAIL_ADDRESS_RE",
            "examples": ["john.doe@example.com", "john.doe[AT]example[DOT]com"],
            "context": [],
            "score": 0.75,
            "languages": ["en"],
        },
        {
            "expressions": [
                r"(?:(4\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4})|(3[47]\d{2}[-\s]?\d{6}[-\s]?\d{5})|(3(?:0[0-5]|[68]\d)\d{11}))"
            ],
            "name": "CREDIT_CARD_RE",
            "examples": ["4111111111111111", "378282246310005"],
            "context": [],
            "score": 0.75,
            "languages": ["en"],
        },
        {
            "expressions": [r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"],
            "name": "IBAN_RE",
            "examples": ["PL61109010140000071219812874"],
            "context": ["iban", "account"],
            "score": 0.75,
            "languages": ["en"],
        },
        {
            "expressions": [r"\b(?:\+?\d{1,3}[-.\s])?(?:\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}\b"],
            "name": "PHONE_NUMBER_FORMATTED_RE",
            "examples": ["+1 212 555 0100", "(212) 555-0100"],
            "context": ["phone", "telephone", "mobile", "call"],
            "score": 0.75,
            "languages": ["en"],
        },
        {
            "expressions": [r"\b\d{3}-\d{2}-\d{4}\b"],
            "name": "US_SSN_RE",
            "examples": ["111-22-3333"],
            "context": ["ssn", "social security"],
            "score": 0.75,
            "languages": ["en"],
        },
    ]


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
                        entity_types=_SENSITIVE_ENTITY_TYPES.copy(),
                        regex_patterns=_sensitive_regex_patterns(),
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
        except Exception as exc:
            logger.warning(
                "LLM Guard scanners unavailable, falling back to local checks: %s",
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
            is_output_stage = self._is_output_stage(stage)
            scanners = self._output_scanners if is_output_stage else self._input_scanners

            # Run appropriate scan
            if is_output_stage:
                output_prompt = self._output_scan_prompt(stage)
                sanitized_text, results_valid, results_score = scan_output(
                    scanners,
                    output_prompt,
                    text,
                )
            else:
                sanitized_text, results_valid, results_score = scan_prompt(scanners, text)

            # Extract categories from results
            categories: list[str] = []
            max_risk = 0.0

            normalized_valid = {
                scanner_name: self._coerce_valid(is_valid)
                for scanner_name, is_valid in results_valid.items()
            }
            normalized_scores = {
                scanner_name: self._coerce_score(score)
                for scanner_name, score in results_score.items()
            }

            for scanner_name, is_valid in normalized_valid.items():
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
                    score = normalized_scores.get(scanner_name, 1.0)
                    max_risk = max(max_risk, score)

            blocked = max_risk >= 0.75 or not all(normalized_valid.values())

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
                affected_node=self._affected_node(stage),
                sanitized_text_used=sanitized_text != text,
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
            affected_node=self._affected_node(stage),
            sanitized_text_used=False,
        )

    def _affected_node(self, stage: str) -> str | None:
        """Map guardrail scan stages to graph nodes for audit metadata."""
        return {
            "request_validation": "RequestValidation",
            "data_analyst_prompt": "DataAnalystAgent",
            "data_analyst_llm_input": "DataAnalystAgent",
            "data_analyst_llm_output": "DataAnalystAgent",
            "risk_expert_prompt": "RiskExpertAgent",
            "risk_expert_llm_input": "RiskExpertAgent",
            "risk_expert_llm_output": "RiskExpertAgent",
            "worker_outputs": "AnalysisFanIn",
            "supervisor_prompt": "SupervisorAgent",
            "llm_input": "SupervisorAgent",
            "llm_output": "SupervisorAgent",
            "watsonx_output": "SupervisorAgent",
            "supervisor_output": "SupervisorAgent",
            "final_output": "FinalOutputGuard",
        }.get(stage)

    def _is_output_stage(self, stage: str) -> bool:
        """Return whether a stage should be scanned as model/workflow output."""
        return stage in {
            "output",
            "llm_output",
            "watsonx_output",
            "supervisor_output",
            "final_output",
            "worker_outputs",
            "data_analyst_llm_output",
            "risk_expert_llm_output",
        }

    def _output_scan_prompt(self, stage: str) -> str:
        """Provide factual context for output relevance scanners."""
        if stage in {"data_analyst_llm_output", "risk_expert_llm_output"}:
            return (
                "Worker agent output must be concise structured RWA commentary grounded "
                "in deterministic tool observations, validation flags, and recommended actions."
            )
        if stage == "final_output":
            return (
                "RWA executive commentary must be a structured JSON payload with "
                "executive_summary, cro_view, cfo_view, observations, quantitative "
                "validation, validation flags, and recommended actions grounded in "
                "deterministic RWA calculator outputs."
            )
        if stage in {"llm_output", "watsonx_output", "supervisor_output"}:
            return (
                "The model output must be concise stakeholder RWA commentary in JSON "
                "fields executive_summary, cro_view, and cfo_view, grounded only in "
                "provided deterministic findings and validation results."
            )
        return "Structured RWA analysis output must remain relevant, safe, and PII-free."

    def _coerce_valid(self, value: Any) -> bool:
        """Normalize llm-guard validity values across released result shapes."""
        if isinstance(value, bool):
            return value
        if isinstance(value, dict):
            for key in ("valid", "is_valid", "passed"):
                nested = value.get(key)
                if isinstance(nested, bool):
                    return nested
            return bool(value)
        if isinstance(value, list | tuple):
            if not value:
                return True
            return self._coerce_valid(value[0])
        if hasattr(value, "valid"):
            nested = value.valid
            if isinstance(nested, bool):
                return nested
        if hasattr(value, "passed"):
            nested = value.passed
            if isinstance(nested, bool):
                return nested
        return bool(value)

    def _coerce_score(self, value: Any) -> float:
        """Normalize llm-guard score values to the backend 0..1 risk range."""
        if isinstance(value, bool) or value is None:
            return 0.0
        if isinstance(value, int | float):
            return min(1.0, max(0.0, float(value)))
        if isinstance(value, str):
            try:
                return min(1.0, max(0.0, float(value)))
            except ValueError:
                return 0.0
        if isinstance(value, dict):
            for key in ("score", "risk_score", "probability"):
                if key in value:
                    return self._coerce_score(value[key])
            return 0.0
        if isinstance(value, list | tuple):
            for item in reversed(value):
                score = self._coerce_score(item)
                if score > 0:
                    return score
            return 0.0
        if hasattr(value, "score"):
            return self._coerce_score(value.score)
        if hasattr(value, "risk_score"):
            return self._coerce_score(value.risk_score)
        return 0.0

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
