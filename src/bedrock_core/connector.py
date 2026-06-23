from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Connector(ABC):
    """Base class for all external system connectors.

    bedrock-core defines the contract (start, stop, health, capabilities,
    execute). Domain-specific connectors (SplunkConnector, JiraConnector,
    RunbookConnector, etc.) live in application repositories and subclass this.

    The framework never imports a concrete connector — only this base class.
    """

    name: str

    @abstractmethod
    async def start(self) -> None:
        """Initialize the connector (open connections, authenticate, etc.)."""
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        """Clean up resources (close connections, flush buffers, etc.)."""
        raise NotImplementedError

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Return current health status.

        Must always return a dict with at least:
            {"status": "ok" | "degraded" | "unavailable", "connector": self.name}
        """
        raise NotImplementedError

    def capabilities(self) -> List[str]:
        """Return a list of named operations this connector supports.

        Used for introspection and documentation — not enforced at runtime.
        Override to advertise what execute() accepts.
        """
        return []

    @abstractmethod
    def execute(self, operation: str, **kwargs: Any) -> Any:
        """Run a named operation against the external system.

        Implementations should raise ValueError for unknown operations.
        All provider-specific exceptions should be caught and re-raised
        as ConnectorError so callers don't need to handle SDK-specific types.
        """
        raise NotImplementedError


class ConnectorError(Exception):
    """Raised when a connector operation fails.

    Wraps provider-specific exceptions so callers never need to import
    Splunk SDK, Jira SDK, or any other provider library directly.
    """

    def __init__(self, connector: str, operation: str, message: str):
        self.connector = connector
        self.operation = operation
        super().__init__(f"[{connector}:{operation}] {message}")
