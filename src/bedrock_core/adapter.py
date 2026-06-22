from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class Adapter(ABC):
    """Connects a Capability to an external provider (LLM API, DB, queue, etc.).

    This is the only place provider-specific code is allowed to live. Capabilities
    and Runtime never import a concrete provider directly.
    """

    name: str

    @abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        """Run a single completion. Returns (text, usage_dict).

        usage_dict should contain at least 'prompt_tokens' and 'completion_tokens'
        when the provider can report them, so capabilities can compute metrics/cost.
        """
        raise NotImplementedError

    def estimate_cost(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        """Default cost estimate. Providers should override with real pricing."""
        return {"usd": 0.0, "note": "cost estimation not implemented for this adapter"}
