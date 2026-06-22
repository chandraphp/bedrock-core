from __future__ import annotations

from typing import Any, Dict, Tuple

from ..adapter import Adapter


class MockProvider(Adapter):
    """Deterministic offline provider. Default for App.agent() and the test suite.

    Mirrors the mock-first adapter pattern used in production SRE tooling: every
    real provider should be developable and testable with zero network access and
    zero API keys before it's ever called for real.
    """

    name = "mock"

    def complete(self, prompt: str, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        text = f"[mock response to: {prompt[:60]!r}]"
        usage = {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(text.split()),
        }
        return text, usage

    def estimate_cost(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        return {"usd": 0.0, "note": "mock provider — no real cost incurred"}
