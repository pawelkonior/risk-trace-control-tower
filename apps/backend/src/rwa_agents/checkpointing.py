from __future__ import annotations

from copy import deepcopy
from typing import Any

try:  # pragma: no cover - exercised only when langgraph is installed locally.
    from langgraph.checkpoint.memory import MemorySaver as LangGraphMemorySaver
except Exception:  # pragma: no cover
    LangGraphMemorySaver = None  # type: ignore[assignment]


class MemorySaverCheckpoint:
    """MemorySaver-compatible checkpointer keyed by stable thread_id."""

    name = "MemorySaver"

    def __init__(self) -> None:
        self._langgraph_saver = LangGraphMemorySaver() if LangGraphMemorySaver else None
        self._states: dict[str, dict[str, Any]] = {}

    def put(self, thread_id: str, state: dict[str, Any]) -> None:
        self._states[thread_id] = deepcopy(state)

    def get(self, thread_id: str) -> dict[str, Any] | None:
        state = self._states.get(thread_id)
        return deepcopy(state) if state is not None else None
