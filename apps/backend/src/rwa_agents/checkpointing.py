from __future__ import annotations

from copy import deepcopy
from typing import Any

try:
    from langgraph.checkpoint.memory import MemorySaver as LangGraphMemorySaver
except ImportError:  # pragma: no cover - newer langgraph names the saver InMemorySaver.
    from langgraph.checkpoint.memory import InMemorySaver as LangGraphMemorySaver


class MemorySaverCheckpoint:
    """MemorySaver-compatible checkpointer keyed by stable thread_id."""

    name = "MemorySaver"

    def __init__(self) -> None:
        self._langgraph_saver = LangGraphMemorySaver()
        self._states: dict[str, dict[str, Any]] = {}

    @property
    def langgraph_saver(self) -> Any:
        return self._langgraph_saver

    def put(self, thread_id: str, state: dict[str, Any]) -> None:
        self._states[thread_id] = deepcopy(state)

    def get(self, thread_id: str) -> dict[str, Any] | None:
        state = self._states.get(thread_id)
        return deepcopy(state) if state is not None else None
