from .adapter import Adapter
from .app import App, Agent
from .capability import Capability, ChatCapability
from .config import BaseConfig, ConnectorConfig, ConfigurationError, LLMConfig
from .connector import Connector, ConnectorError
from .events import (
    EventBus, EventType, RuntimeEvent, StageEvent,
    PromptEvent, RetrievalEvent,
    get_event_bus, set_event_bus,
)
from .lifecycle import LifecycleApp
from .retriever import Document, MockRetriever, Retriever
from .runtime import ExecutionResult, Runtime
from .workflow import Stage, StageResult

__all__ = [
    # Public sugar API
    "App", "Agent", "LifecycleApp",
    # Core runtime
    "Runtime", "ExecutionResult",
    "Adapter", "Capability", "ChatCapability",
    # Stage protocol (runtime primitive — orchestration is NOT public yet)
    "Stage", "StageResult",
    # Event bus
    "EventBus", "EventType", "RuntimeEvent",
    "StageEvent", "PromptEvent", "RetrievalEvent",
    "get_event_bus", "set_event_bus",
    # Extension points
    "Connector", "ConnectorError",
    "Retriever", "MockRetriever", "Document",
    # Configuration
    "BaseConfig", "ConnectorConfig", "ConfigurationError", "LLMConfig",
]

__version__ = "0.3.0"
