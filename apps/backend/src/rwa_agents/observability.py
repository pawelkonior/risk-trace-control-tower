from __future__ import annotations

from uuid import uuid4

from .schemas import EvaluationScore, GuardrailResult, ObservabilityMetadata, PromptUsage


class LocalObservability:
    def __init__(self, request_id: str, langfuse_enabled: bool = False) -> None:
        self.metadata = ObservabilityMetadata(
            langfuse_enabled=langfuse_enabled,
            trace_id=f"trace-{uuid4().hex[:12]}" if langfuse_enabled else None,
            callback_handler_attached=langfuse_enabled,
            thread_id=request_id,
        )

    def node(self, _name: str) -> None:
        self.metadata.node_transition_count += 1

    def tool(self, _name: str) -> None:
        self.metadata.tool_call_count += 1

    def prompt(self, usage: PromptUsage) -> None:
        self.metadata.prompt_usages.append(usage)

    def guardrail(self, result: GuardrailResult) -> None:
        self.metadata.guardrail_results.append(result)
        if result.blocked:
            self.metadata.guardrail_block_count += 1
        if "pii" in result.categories:
            self.metadata.pii_detected = True
        self.metadata.prompt_injection_risk = max(
            self.metadata.prompt_injection_risk,
            result.risk_score if "prompt_injection" in result.categories else 0.0,
        )

    def score(self, name: str, value: float, comment: str) -> None:
        self.metadata.evaluation_scores.append(
            EvaluationScore(name=name, value=value, comment=comment)
        )
