from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T", bound="RuntimeEvent")
Handler = Callable[["RuntimeEvent"], None]


class EventType(str, Enum):
    # Workflow lifecycle
    WORKFLOW_STARTED   = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED    = "workflow.failed"

    # Stage lifecycle
    STAGE_STARTED      = "stage.started"
    STAGE_COMPLETED    = "stage.completed"
    STAGE_FAILED       = "stage.failed"

    # LLM provider
    PROMPT_STARTED     = "prompt.started"
    PROMPT_COMPLETED   = "prompt.completed"

    # Retrieval
    RETRIEVAL_STARTED  = "retrieval.started"
    RETRIEVAL_COMPLETED= "retrieval.completed"

    # Tool execution
    TOOL_STARTED       = "tool.started"
    TOOL_COMPLETED     = "tool.completed"
    TOOL_FAILED        = "tool.failed"


@dataclass
class RuntimeEvent:
    """Base event emitted by every bedrock-core runtime component.

    Applications subscribe to events rather than subclassing runtime internals.
    This makes observability, logging, tracing, and alerting composable
    without coupling them to the execution engine.
    """
    event_type:     EventType
    source:         str                   # which component emitted this
    timestamp:      float = field(default_factory=time.time)
    correlation_id: Optional[str] = None  # links events in one execution chain
    metadata:       Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type":     self.event_type.value,
            "source":         self.source,
            "timestamp":      self.timestamp,
            "correlation_id": self.correlation_id,
            "metadata":       self.metadata,
        }


@dataclass
class StageEvent(RuntimeEvent):
    stage_name:  str   = ""
    latency_ms:  float = 0.0
    tokens_in:   int   = 0
    tokens_out:  int   = 0
    error:       Optional[str] = None


@dataclass
class PromptEvent(RuntimeEvent):
    model:       str   = ""
    tokens_in:   int   = 0
    tokens_out:  int   = 0
    latency_ms:  float = 0.0
    cost_usd:    float = 0.0


@dataclass
class RetrievalEvent(RuntimeEvent):
    query:       str   = ""
    hits:        int   = 0
    latency_ms:  float = 0.0
    top_score:   float = 0.0


class EventBus:
    """Publish-subscribe event bus for the bedrock-core runtime.

    Every runtime component (Workflow, Stage, Provider, Retriever) publishes
    events here. Subscribers (OTel exporter, logger, cost tracker, alerter)
    register handlers without touching the execution engine.

    This is the architectural difference between "observable by instrumentation"
    (PipelineTracer bolted on after the fact) and "observable by design"
    (events are native to execution).

    Usage:

        bus = EventBus()

        # Subscribe to all events
        bus.subscribe(lambda e: print(e.to_dict()))

        # Subscribe to a specific event type
        bus.subscribe(otel_handler, EventType.PROMPT_COMPLETED)

        # Publish from a runtime component
        bus.publish(PromptEvent(
            event_type=EventType.PROMPT_COMPLETED,
            source="AnthropicProvider",
            model="claude-sonnet-4-6",
            tokens_in=150, tokens_out=80,
            latency_ms=412.3,
        ))
    """

    def __init__(self) -> None:
        self._subscribers: Dict[Optional[EventType], List[Handler]] = {}
        self._history: List[RuntimeEvent] = []
        self._record_history: bool = True

    def subscribe(
        self,
        handler: Handler,
        event_type: Optional[EventType] = None,
    ) -> "EventBus":
        """Register a handler. If event_type is None, receives all events."""
        self._subscribers.setdefault(event_type, []).append(handler)
        return self

    def unsubscribe(self, handler: Handler, event_type: Optional[EventType] = None) -> None:
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                h for h in self._subscribers[event_type] if h is not handler
            ]

    def publish(self, event: RuntimeEvent) -> None:
        """Publish an event. Handlers are called synchronously in registration order."""
        if self._record_history:
            self._history.append(event)

        # Wildcard subscribers first
        for handler in self._subscribers.get(None, []):
            try:
                handler(event)
            except Exception:
                pass  # never let a subscriber crash the runtime

        # Type-specific subscribers
        for handler in self._subscribers.get(event.event_type, []):
            try:
                handler(event)
            except Exception:
                pass

    def events_of_type(self, event_type: EventType) -> List[RuntimeEvent]:
        return [e for e in self._history if e.event_type == event_type]

    @property
    def history(self) -> List[RuntimeEvent]:
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()


# Global default bus — applications can replace with their own instance
_DEFAULT_BUS = EventBus()


def get_event_bus() -> EventBus:
    return _DEFAULT_BUS


def set_event_bus(bus: EventBus) -> None:
    global _DEFAULT_BUS
    _DEFAULT_BUS = bus
