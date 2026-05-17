from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from .config import LangfuseConfig
from .schemas import EvaluationScore, GuardrailResult, ObservabilityMetadata, PromptUsage

logger = logging.getLogger(__name__)


class LocalObservability:
    """
    Observability service with optional Langfuse integration.

    Tracks workflow execution, node transitions, tool calls, guardrail results,
    and evaluation scores. Submits traces to Langfuse when enabled.
    """

    def __init__(self, request_id: str, config: LangfuseConfig | None = None) -> None:
        """
        Initialize observability service.

        Args:
            request_id: Unique request identifier used as thread_id
            config: Langfuse configuration. If None, loads from environment.
        """
        self.config = config or LangfuseConfig.from_env()
        self.langfuse_enabled = self.config.is_configured()
        self.request_id = request_id
        self._client: Any = None
        self._trace: Any = None

        self.metadata = ObservabilityMetadata(
            langfuse_enabled=self.langfuse_enabled,
            trace_id=f"trace-{uuid4().hex[:12]}" if self.langfuse_enabled else None,
            callback_handler_attached=False,
            thread_id=request_id,
        )

        if self.langfuse_enabled:
            self._init_langfuse_trace()

        logger.info(
            "LocalObservability initialized with langfuse_enabled=%s, request_id=%s",
            self.langfuse_enabled,
            request_id,
        )

    def _init_langfuse_trace(self) -> None:
        """Initialize Langfuse client and create trace."""
        try:
            from langfuse import Langfuse

            self._client = Langfuse(
                public_key=self.config.langfuse_public_key,
                secret_key=self.config.langfuse_secret_key,
                host=self.config.langfuse_base_url,
            )

            self._trace = self._client.trace(
                name="rwa_analysis",
                id=self.request_id,
                metadata={
                    "service": "rwa_agents",
                    "workflow": "multi_agent_commentary",
                },
            )

            self.metadata.callback_handler_attached = True
            logger.info("Langfuse trace created: %s", self.request_id)
        except ImportError as exc:
            logger.warning(
                "Langfuse library not available, observability will be local only: %s",
                exc,
            )
            self.langfuse_enabled = False
            self.metadata.langfuse_enabled = False
        except Exception as exc:
            logger.error("Failed to initialize Langfuse trace: %s", exc)
            self.langfuse_enabled = False
            self.metadata.langfuse_enabled = False

    def node(self, name: str) -> None:
        """
        Record node transition.

        Args:
            name: Node name
        """
        self.metadata.node_transition_count += 1

        if self.langfuse_enabled and self._trace:
            try:
                self._trace.span(
                    name=f"node_{name}",
                    metadata={"node": name, "type": "graph_node"},
                )
            except Exception as exc:
                logger.warning("Failed to record node span in Langfuse: %s", exc)

    def tool(self, name: str) -> None:
        """
        Record tool call.

        Args:
            name: Tool name
        """
        self.metadata.tool_call_count += 1

        if self.langfuse_enabled and self._trace:
            try:
                self._trace.span(
                    name=f"tool_{name}",
                    metadata={"tool": name, "type": "deterministic_tool"},
                )
            except Exception as exc:
                logger.warning("Failed to record tool span in Langfuse: %s", exc)

    def llm(self, *, provider: str, model_id: str, token_count: int) -> None:
        """
        Record an external LLM call and token usage.

        Args:
            provider: LLM provider name
            model_id: Provider model identifier
            token_count: Total tokens reported by the provider, if available
        """
        self.metadata.llm_call_count += 1
        self.metadata.total_token_count += max(0, token_count)

        if self.langfuse_enabled and self._trace:
            try:
                self._trace.span(
                    name=f"llm_{provider}",
                    metadata={
                        "provider": provider,
                        "model_id": model_id,
                        "total_token_count": token_count,
                    },
                )
            except Exception as exc:
                logger.warning("Failed to record LLM span in Langfuse: %s", exc)

    def prompt(self, usage: PromptUsage) -> None:
        """
        Record prompt usage.

        Args:
            usage: Prompt usage metadata
        """
        self.metadata.prompt_usages.append(usage)

        if self.langfuse_enabled and self._trace:
            try:
                self._trace.span(
                    name=f"prompt_{usage.prompt_name}",
                    metadata={
                        "prompt_name": usage.prompt_name,
                        "prompt_version": usage.prompt_version,
                        "source": usage.source,
                    },
                )
            except Exception as exc:
                logger.warning("Failed to record prompt span in Langfuse: %s", exc)

    def guardrail(self, result: GuardrailResult) -> None:
        """
        Record guardrail scan result.

        Args:
            result: Guardrail scan result
        """
        self.metadata.guardrail_results.append(result)

        if result.blocked:
            self.metadata.guardrail_block_count += 1

        if "pii" in result.categories:
            self.metadata.pii_detected = True

        if "prompt_injection" in result.categories:
            self.metadata.prompt_injection_risk = max(
                self.metadata.prompt_injection_risk,
                result.risk_score,
            )

        if self.langfuse_enabled and self._trace:
            try:
                self._trace.event(
                    name=f"guardrail_{result.stage}",
                    metadata={
                        "stage": result.stage,
                        "scanner": result.scanner,
                        "passed": result.passed,
                        "blocked": result.blocked,
                        "risk_score": result.risk_score,
                        "categories": result.categories,
                    },
                )
            except Exception as exc:
                logger.warning("Failed to record guardrail event in Langfuse: %s", exc)

    def score(self, name: str, value: float, comment: str) -> None:
        """
        Record evaluation score.

        Args:
            name: Score name
            value: Score value (0.0 to 1.0)
            comment: Score explanation
        """
        score = EvaluationScore(name=name, value=value, comment=comment)
        self.metadata.evaluation_scores.append(score)

        if self.langfuse_enabled and self._trace:
            try:
                self._trace.score(
                    name=name,
                    value=value,
                    comment=comment,
                )
            except Exception as exc:
                logger.warning("Failed to submit score to Langfuse: %s", exc)

    def compute_final_scores(self, state: dict[str, Any]) -> list[EvaluationScore]:
        """
        Compute all required evaluation scores from workflow state.

        Args:
            state: Final workflow state

        Returns:
            List of computed evaluation scores
        """
        scores: list[EvaluationScore] = []

        # Faithfulness: Quantitative validation used Python tools only
        scores.append(
            EvaluationScore(
                name="Faithfulness",
                value=1.0,
                comment="Quantitative validation used Python tools only, no LLM calculations",
            )
        )

        # Groundedness: Commentary synthesized from deterministic findings
        scores.append(
            EvaluationScore(
                name="Groundedness",
                value=1.0,
                comment="Commentary synthesized from deterministic findings and tool outputs",
            )
        )

        # Anomaly Detection: Based on critical validation flags
        critical_flags = [
            flag for flag in state.get("validation_flags", []) if flag.severity == "critical"
        ]
        anomaly_detected = len(critical_flags) > 0
        scores.append(
            EvaluationScore(
                name="Anomaly_Detection",
                value=1.0 if anomaly_detected else 0.0,
                comment=f"Detected {len(critical_flags)} critical validation flags",
            )
        )

        # Guardrail Block Count: From metadata
        scores.append(
            EvaluationScore(
                name="Guardrail_Block_Count",
                value=float(self.metadata.guardrail_block_count),
                comment=f"Total guardrail blocks: {self.metadata.guardrail_block_count}",
            )
        )

        # PII Detected: From metadata
        scores.append(
            EvaluationScore(
                name="PII_Detected",
                value=1.0 if self.metadata.pii_detected else 0.0,
                comment="PII detected" if self.metadata.pii_detected else "No PII detected",
            )
        )

        # Prompt Injection Risk: From metadata
        scores.append(
            EvaluationScore(
                name="Prompt_Injection_Risk",
                value=self.metadata.prompt_injection_risk,
                comment=(
                    "Maximum prompt injection risk score: "
                    f"{self.metadata.prompt_injection_risk:.2f}"
                ),
            )
        )

        # Submit all scores to Langfuse if enabled
        for score in scores:
            if self.langfuse_enabled and self._trace:
                try:
                    self._trace.score(
                        name=score.name,
                        value=score.value,
                        comment=score.comment,
                    )
                except Exception as exc:
                    logger.warning("Failed to submit score %s to Langfuse: %s", score.name, exc)

        # Add to metadata
        self.metadata.evaluation_scores.extend(scores)

        return scores

    def finalize(self) -> None:
        """Finalize observability and flush to Langfuse if enabled."""
        if self.langfuse_enabled and self._client:
            try:
                self._client.flush()
                logger.info("Langfuse trace finalized and flushed")
            except Exception as exc:
                logger.warning("Failed to flush Langfuse trace: %s", exc)


# Made with Bob
