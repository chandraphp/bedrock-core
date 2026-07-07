"""Stage protocol and internal orchestration primitives.

PUBLIC API (in __all__):
  Stage       — abstract unit of work; emits events; returns StageResult
  StageResult — typed output with latency and optional error

NOT public yet (pending evidence from a second workflow consumer):
  Workflow      — ordered stage orchestrator. Lives here so ops-brain can
                  import it directly as an internal implementation detail,
                  but it is NOT exported via bedrock_core.__all__ until a
                  second independent workflow proves orchestration belongs
                  in the runtime. See ADR-006 review decision 2026-06-23.
"""
from __future__ import annotations

import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .events import EventBus, EventType, RuntimeEvent, StageEvent, get_event_bus


@dataclass
class StageResult:
    """Output of one Stage execution."""
    stage_name: str
    output:     Any
    latency_ms: float
    metadata:   Dict[str, Any] = field(default_factory=dict)
    error:      Optional[str]  = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass
class WorkflowResult:
    """Output of a Workflow execution — internal, not public API."""
    workflow_id:   str
    stage_results: List[StageResult]
    total_latency: float
    final_output:  Any = None
    error:         Optional[str] = None

    @property
    def succeeded(self) -> bool:
        return self.error is None and all(r.succeeded for r in self.stage_results)

    def get(self, stage_name: str) -> Optional[StageResult]:
        return next((r for r in self.stage_results if r.stage_name == stage_name), None)


class Stage(ABC):
    """A single unit of work — a runtime primitive.

    Each Stage:
    - receives the previous stage's output (or None for the first)
    - returns its output
    - emits STAGE_STARTED and STAGE_COMPLETED/STAGE_FAILED to the Event Bus

    Stage is public because it is the extension point applications
    use to define reusable, observable units of work. How those units
    are orchestrated (sequentially, in parallel, as a DAG) is a policy
    decision that belongs in the application layer until proven otherwise.
    """

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def run(self, input: Any, context: Dict[str, Any]) -> Any:
        raise NotImplementedError


class Workflow:
    """INTERNAL — not part of the public bedrock-core API.

    An ordered sequence of Stages. This class exists so ops-brain can
    experiment with workflow orchestration internally. It will be promoted
    to the public API only when a second, independent workflow (not RCAAgent)
    proves that orchestration semantics belong in the runtime.

    Import directly from bedrock_core.workflow if you need it:
        from bedrock_core.workflow import Workflow

    Do NOT add to __all__ until ADR-006 evidence criteria are met.
    """

    def __init__(self, *stages: Stage, bus: Optional[EventBus] = None):
        self.stages = list(stages)
        self._bus   = bus or get_event_bus()

    def add(self, stage: Stage) -> "Workflow":
        self.stages.append(stage)
        return self

    def run(self, input: Any = None, context: Optional[Dict[str, Any]] = None) -> WorkflowResult:
        workflow_id   = str(uuid.uuid4())[:8]
        context       = {**(context or {}), "workflow_id": workflow_id}
        results: List[StageResult] = []
        current       = input
        t0            = time.perf_counter()

        self._bus.publish(RuntimeEvent(
            event_type=EventType.WORKFLOW_STARTED, source="Workflow",
            correlation_id=workflow_id,
            metadata={"stages": [s.name for s in self.stages]},
        ))

        try:
            for stage in self.stages:
                t_stage = time.perf_counter()
                self._bus.publish(StageEvent(
                    event_type=EventType.STAGE_STARTED, source=stage.name,
                    stage_name=stage.name, correlation_id=workflow_id,
                ))
                try:
                    output  = stage.run(current, context)
                    latency = (time.perf_counter() - t_stage) * 1000
                    result  = StageResult(stage.name, output, latency)
                    self._bus.publish(StageEvent(
                        event_type=EventType.STAGE_COMPLETED, source=stage.name,
                        stage_name=stage.name, latency_ms=latency,
                        correlation_id=workflow_id,
                    ))
                    results.append(result)
                    current = output
                except Exception as exc:
                    latency = (time.perf_counter() - t_stage) * 1000
                    result  = StageResult(stage.name, None, latency, error=str(exc))
                    self._bus.publish(StageEvent(
                        event_type=EventType.STAGE_FAILED, source=stage.name,
                        stage_name=stage.name, latency_ms=latency,
                        error=str(exc), correlation_id=workflow_id,
                    ))
                    results.append(result)
                    raise
        except Exception as exc:
            total = (time.perf_counter() - t0) * 1000
            self._bus.publish(RuntimeEvent(
                event_type=EventType.WORKFLOW_FAILED, source="Workflow",
                correlation_id=workflow_id,
                metadata={"error": str(exc), "total_latency_ms": total},
            ))
            return WorkflowResult(workflow_id, results, total, error=str(exc))

        total = (time.perf_counter() - t0) * 1000
        self._bus.publish(RuntimeEvent(
            event_type=EventType.WORKFLOW_COMPLETED, source="Workflow",
            correlation_id=workflow_id,
            metadata={"total_latency_ms": total, "stages": len(results)},
        ))
        return WorkflowResult(workflow_id, results, total, final_output=current)
