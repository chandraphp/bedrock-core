from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from .adapter import Adapter

if TYPE_CHECKING:
    from .runtime import ExecutionResult


class Capability(ABC):
    """A single thing a Runtime can do (chat, retrieve, evaluate, ...).

    Every capability is backed by exactly one Adapter, so swapping providers
    never touches capability or runtime code.
    """

    name: str

    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    @abstractmethod
    def run(self, **kwargs: Any) -> "ExecutionResult":
        raise NotImplementedError


class ChatCapability(Capability):
    """The first capability: a single-turn chat completion."""

    name = "chat"

    def run(self, **kwargs: Any) -> "ExecutionResult":
        from .runtime import ExecutionResult  # local import avoids a circular import

        try:
            prompt: str = kwargs.pop("prompt")
        except KeyError as exc:
            raise TypeError("ChatCapability.run() requires a 'prompt' keyword argument") from exc

        trace: list[dict[str, Any]] = [{"step": "chat.request", "prompt": prompt}]

        start = time.perf_counter()
        text, usage = self.adapter.complete(prompt, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000

        trace.append({"step": "chat.response", "elapsed_ms": round(elapsed_ms, 2)})
        cost = self.adapter.estimate_cost(usage)

        return ExecutionResult(
            output=text,
            metrics={"elapsed_ms": round(elapsed_ms, 2), "tokens": usage},
            trace=trace,
            cost=cost,
        )
