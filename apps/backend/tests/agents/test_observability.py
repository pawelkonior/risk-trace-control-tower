from __future__ import annotations

import sys
from types import SimpleNamespace
from typing import ClassVar

from rwa_agents.config import LangfuseConfig
from rwa_agents.observability import LocalObservability
from rwa_agents.prompts import DATA_ANALYST_PROMPT, PromptRegistry
from rwa_agents.schemas import GuardrailResult, PromptUsage


class FakeTrace:
    def __init__(self) -> None:
        self.spans: list[tuple[str, dict]] = []
        self.events: list[tuple[str, dict]] = []
        self.scores: list[tuple[str, float, str]] = []

    def span(self, *, name: str, metadata: dict) -> None:
        self.spans.append((name, metadata))

    def event(self, *, name: str, metadata: dict) -> None:
        self.events.append((name, metadata))

    def score(self, *, name: str, value: float, comment: str) -> None:
        self.scores.append((name, value, comment))


class FakeLangfuse:
    instances: ClassVar[list[FakeLangfuse]] = []

    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs
        self.trace_obj = FakeTrace()
        self.flushed = False
        self.prompts: list[tuple[str, str | None]] = []
        FakeLangfuse.instances.append(self)

    def trace(self, **kwargs: object) -> FakeTrace:
        self.trace_name = kwargs["name"]
        self.trace_id = kwargs["id"]
        self.trace_metadata = kwargs["metadata"]
        return self.trace_obj

    def get_prompt(self, *, name: str, label: str | None = None):
        self.prompts.append((name, label))
        return SimpleNamespace(prompt="prompt from langfuse", version=42)

    def flush(self) -> None:
        self.flushed = True


def test_langfuse_observability_attaches_callback_and_records_events(monkeypatch) -> None:
    FakeLangfuse.instances = []
    monkeypatch.setitem(sys.modules, "langfuse", SimpleNamespace(Langfuse=FakeLangfuse))
    config = LangfuseConfig(
        langfuse_enabled=True,
        langfuse_public_key="public",
        langfuse_secret_key="secret",  # noqa: S106 - fake test credential
    )

    observability = LocalObservability("thread-1", config)
    usage = PromptUsage(
        prompt_name=DATA_ANALYST_PROMPT,
        prompt_version="v1",
        source="langfuse",
        label="production",
        fetch_status="fetched",
    )
    guardrail = GuardrailResult(
        stage="llm_input",
        scanner="llm_guard",
        passed=True,
        affected_node="SupervisorAgent",
    )

    observability.node("AnalysisPhase")
    observability.tool("DataTools")
    observability.llm(provider="watsonx", model_id="model", token_count=12)
    observability.prompt(usage)
    observability.guardrail(guardrail)
    observability.score("Faithfulness", 1.0, "grounded")
    observability.finalize()

    fake = FakeLangfuse.instances[0]
    assert observability.metadata.langfuse_enabled is True
    assert observability.metadata.callback_handler_attached is True
    assert observability.metadata.llm_call_count == 1
    assert observability.metadata.total_token_count == 12
    assert fake.trace_id == "thread-1"
    assert fake.trace_obj.spans
    assert fake.trace_obj.events
    assert fake.trace_obj.scores
    assert fake.flushed is True


def test_prompt_registry_fetches_from_langfuse_when_enabled(monkeypatch) -> None:
    FakeLangfuse.instances = []
    monkeypatch.setitem(sys.modules, "langfuse", SimpleNamespace(Langfuse=FakeLangfuse))
    config = LangfuseConfig(
        langfuse_enabled=True,
        langfuse_public_key="public",
        langfuse_secret_key="secret",  # noqa: S106 - fake test credential
    )

    prompt, usage = PromptRegistry(config).get(DATA_ANALYST_PROMPT)

    assert prompt == "prompt from langfuse"
    assert usage.source == "langfuse"
    assert usage.prompt_version == "42"
    assert usage.fetch_status == "fetched"
    assert FakeLangfuse.instances[0].prompts == [(DATA_ANALYST_PROMPT, "production")]


def test_langfuse_disabled_uses_local_metadata_without_client(monkeypatch) -> None:
    class FailLangfuse:
        def __init__(self, **kwargs) -> None:
            _ = kwargs
            raise AssertionError("Langfuse client should not be constructed when disabled")

    monkeypatch.setitem(sys.modules, "langfuse", SimpleNamespace(Langfuse=FailLangfuse))
    config = LangfuseConfig(
        langfuse_enabled=False,
        langfuse_public_key="public",
        langfuse_secret_key="secret",  # noqa: S106 - fake test credential
    )

    observability = LocalObservability("thread-2", config)
    prompt, usage = PromptRegistry(config).get(DATA_ANALYST_PROMPT)

    assert observability.metadata.langfuse_enabled is False
    assert observability.metadata.callback_handler_attached is False
    assert prompt
    assert usage.source == "local_fallback"
