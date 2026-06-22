from __future__ import annotations

from typing import Any, Dict, List, Optional

from .capability import Capability


class ExecutionResult:
    """Result of one Runtime.execute() call.

    Operational data (metrics, trace, cost) lives here — on what just happened —
    rather than as mutable state on the agent. This keeps the agent object simple
    even as the operational surface grows.
    """

    def __init__(
        self,
        output: str,
        *,
        metrics: Dict[str, Any],
        trace: List[Dict[str, Any]],
        cost: Dict[str, Any],
    ):
        self.output = output
        self._metrics = metrics
        self._trace = trace
        self._cost = cost

    def metrics(self) -> Dict[str, Any]:
        return self._metrics

    def trace(self) -> List[Dict[str, Any]]:
        return self._trace

    def cost(self) -> Dict[str, Any]:
        return self._cost

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"ExecutionResult(output={self.output!r})"


class Runtime:
    """Composes Capabilities. Everything else in the public API is sugar over this."""

    def __init__(self, capabilities: Optional[List[Capability]] = None):
        self.capabilities: List[Capability] = list(capabilities or [])

    def add_capability(self, capability: Capability) -> "Runtime":
        self.capabilities.append(capability)
        return self

    def execute(self, capability_name: str, **kwargs: Any) -> ExecutionResult:
        for cap in self.capabilities:
            if cap.name == capability_name:
                return cap.run(**kwargs)
        known = [c.name for c in self.capabilities]
        raise ValueError(
            f"No capability named '{capability_name}' on this runtime. Known: {known}"
        )
