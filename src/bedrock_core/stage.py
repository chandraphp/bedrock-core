from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .events import EventBus, EventType, StageEvent, get_event_bus


@dataclass
class StageResult:
    """Output of one Stage execution.

    Carries the output, latency, and any error. Applications
    compose stages by passing result.output to the next stage.
    """
    stage_name:  str
    output:      Any
    latency_ms:  float
    metadata:    Dict[str, Any] = field(default_factory=dict)
    error:       Optional[str]  = None
    tokens_in:   int            = 0
    tokens_out:  int            = 0

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass
class StageContext:
    """Shared mutable context threaded through a pipeline execution.

    Stages read and write context to share data that isn't the
    primary output — correlation IDs, accumulated costs, run metadata.
    Applications control what goes in context; bedrock-core only
    injects the correlation_id.
    """
    correlation_id:  str
    data:            Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value


class Stage(ABC):
    """A single unit of work in a pipeline.

    Each Stage:
    - receives the previous output and a shared StageContext
    - emits STAGE_STARTED / STAGE_COMPLETED / STAGE_FAILED events
    - returns a StageResult

    Stages are not orchestrated by bedrock-core — applications
    call them directly in whatever order makes sense. This keeps
    orchestration policy in the application (where domain knowledge
    lives) rather than frozen in the framework.

    When a second independent pipeline proves shared orchestration
    semantics, that evidence will justify a Workflow abstraction.
    Until then, stages compose without a container.

    Usage in an application pipeline:

        ctx    = StageContext(correlation_id="abc123")
        result = RetrieveStage(retriever).execute(query, ctx)
        result = SummarizeStage(agent).execute(result.output, ctx)
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def run(self, input: Any, context: StageContext) -> Any:
        """Execute this stage. Return the output for the next stage."""
        raise NotImplementedError

    def execute(
        self,
        input: Any,
        context: StageContext,
        bus: Optional[EventBus] = None,
    ) -> StageResult:
        """Run with automatic event emission and timing."""
        _bus   = bus or get_event_bus()
        start  = time.perf_counter()

        _bus.publish(StageEvent(
            event_type=EventType.STAGE_STARTED,
            source=self.name,
            stage_name=self.name,
            correlation_id=context.correlation_id,
        ))

        try:
            output     = self.run(input, context)
            latency_ms = (time.perf_counter() - start) * 1000
            _bus.publish(StageEvent(
                event_type=EventType.STAGE_COMPLETED,
                source=self.name,
                stage_name=self.name,
                latency_ms=latency_ms,
                correlation_id=context.correlation_id,
            ))
            return StageResult(stage_name=self.name, output=output, latency_ms=latency_ms)

        except Exception as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            _bus.publish(StageEvent(
                event_type=EventType.STAGE_FAILED,
                source=self.name,
                stage_name=self.name,
                latency_ms=latency_ms,
                error=str(exc),
                correlation_id=context.correlation_id,
            ))
            return StageResult(
                stage_name=self.name, output=None,
                latency_ms=latency_ms, error=str(exc),
            )
