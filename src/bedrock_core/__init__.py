from .adapter import Adapter
from .app import App, Agent
from .capability import Capability, ChatCapability
from .config import BaseConfig, ConnectorConfig, ConfigurationError, LLMConfig
from .connector import Connector, ConnectorError
from .lifecycle import LifecycleApp
from .runtime import ExecutionResult, Runtime

__all__ = [
    # Public sugar API
    "App",
    "Agent",
    "LifecycleApp",
    # Core primitives
    "Runtime",
    "ExecutionResult",
    "Adapter",
    "Capability",
    "ChatCapability",
    # Extension points
    "Connector",
    "ConnectorError",
    # Configuration
    "BaseConfig",
    "ConnectorConfig",
    "ConfigurationError",
    "LLMConfig",
]

__version__ = "0.1.0"
