from __future__ import annotations

from typing import Any

from .privacy import find_pii, has_prompt_injection_risk
from .schemas import GuardrailResult


class GuardrailService:
    """Small local adapter that mirrors LLM Guard boundaries for offline runs."""

    scanner_name = "llm_guard"

    def scan(self, stage: str, payload: Any) -> GuardrailResult:
        pii_findings = find_pii(payload)
        injection_risk = has_prompt_injection_risk(payload)
        categories: list[str] = []
        if pii_findings:
            categories.append("pii")
        if injection_risk:
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
