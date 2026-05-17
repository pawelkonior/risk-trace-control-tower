from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any

from pydantic import BaseModel

REJECTED_PII_FIELDS = {
    "account_number",
    "address",
    "borrower_name",
    "client_name",
    "counterparty_name",
    "customer_name",
    "email",
    "first_name",
    "iban",
    "last_name",
    "passport",
    "pesel",
    "phone",
    "ssn",
    "tax_id",
}

PII_VALUE_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", re.IGNORECASE),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "pesel": re.compile(r"\b\d{11}\b"),
    "phone": re.compile(r"\+\d{1,3}[\s-]?(?:\d[\s-]?){7,}\b"),
}

PROMPT_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"reveal\s+(the\s+)?system\s+prompt", re.IGNORECASE),
    re.compile(r"\bjailbreak\b", re.IGNORECASE),
]


class PiiDetectionError(ValueError):
    """Raised when PII-like data is found before graph state construction."""

    def __init__(self, findings: list[str]) -> None:
        self.findings = findings
        super().__init__("PII-like data is not allowed: " + ", ".join(findings))


def find_pii(payload: Any) -> list[str]:
    findings: list[str] = []
    _scan_payload(payload, "$", findings)
    return sorted(set(findings))


def ensure_no_pii(payload: Any) -> None:
    findings = find_pii(payload)
    if findings:
        raise PiiDetectionError(findings)


def has_prompt_injection_risk(payload: Any) -> float:
    text = " ".join(_iter_text(payload))
    if not text:
        return 0.0
    hits = sum(1 for pattern in PROMPT_INJECTION_PATTERNS if pattern.search(text))
    return min(1.0, hits / len(PROMPT_INJECTION_PATTERNS))


def _scan_payload(payload: Any, path: str, findings: list[str]) -> None:
    if isinstance(payload, BaseModel):
        _scan_payload(payload.model_dump(mode="json"), path, findings)
        return
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            normalized_key = str(key).strip().lower()
            child_path = f"{path}.{normalized_key}"
            if normalized_key in REJECTED_PII_FIELDS:
                findings.append(child_path)
            _scan_payload(value, child_path, findings)
        return
    if isinstance(payload, Iterable) and not isinstance(payload, str | bytes):
        for index, item in enumerate(payload):
            _scan_payload(item, f"{path}[{index}]", findings)
        return
    if isinstance(payload, str):
        for label, pattern in PII_VALUE_PATTERNS.items():
            if pattern.search(payload):
                findings.append(f"{path}:{label}")


def _iter_text(payload: Any) -> Iterable[str]:
    if isinstance(payload, BaseModel):
        yield from _iter_text(payload.model_dump(mode="json"))
    elif isinstance(payload, Mapping):
        for key, value in payload.items():
            yield str(key)
            yield from _iter_text(value)
    elif isinstance(payload, Iterable) and not isinstance(payload, str | bytes):
        for item in payload:
            yield from _iter_text(item)
    elif isinstance(payload, str):
        yield payload
