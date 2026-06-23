from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Dict, List

from .app import App
from .connector import Connector

logger = logging.getLogger(__name__)


class LifecycleApp(App):
    """App subclass that adds startup/shutdown lifecycle and a connector registry.

    Resolves GAP-002: connectors previously had to be initialised manually in
    application __init__ with no async support and no guaranteed cleanup.

    Usage:

        app = LifecycleApp()
        app.register_connector(SplunkConnector(config))

        async with app:
            agent = app.agent(provider="ollama", model="qwen2.5:9b")
            result = agent.ask("What errors occurred in the last hour?")
            # on exit, all connectors are stopped cleanly

    Or explicitly:

        await app.startup()
        ...
        await app.shutdown()
    """

    def __init__(self) -> None:
        super().__init__()
        self._connectors: Dict[str, Connector] = {}
        self._startup_hooks: List[Callable[[], Any]] = []
        self._shutdown_hooks: List[Callable[[], Any]] = []
        self._started = False

    # ── Connector registry ───────────────────────────────────────────────

    def register_connector(self, connector: Connector) -> "LifecycleApp":
        """Register a connector. It will be started during startup()."""
        self._connectors[connector.name] = connector
        return self

    def get_connector(self, name: str) -> Connector:
        if name not in self._connectors:
            registered = list(self._connectors)
            raise KeyError(
                f"No connector named '{name}' registered. "
                f"Registered connectors: {registered}"
            )
        return self._connectors[name]

    def connector_health(self) -> Dict[str, Any]:
        """Return health status for all registered connectors."""
        return {name: conn.health() for name, conn in self._connectors.items()}

    # ── Lifecycle hooks ──────────────────────────────────────────────────

    def on_startup(self, fn: Callable[[], Any]) -> Callable[[], Any]:
        """Decorator: register a function to run during startup."""
        self._startup_hooks.append(fn)
        return fn

    def on_shutdown(self, fn: Callable[[], Any]) -> Callable[[], Any]:
        """Decorator: register a function to run during shutdown."""
        self._shutdown_hooks.append(fn)
        return fn

    async def startup(self) -> None:
        """Start all connectors, then run registered startup hooks."""
        if self._started:
            return
        logger.info("LifecycleApp: starting %d connector(s)", len(self._connectors))
        for name, connector in self._connectors.items():
            try:
                await connector.start()
                logger.info("Connector started: %s", name)
            except Exception as exc:
                logger.error("Connector failed to start: %s — %s", name, exc)
                raise
        for hook in self._startup_hooks:
            result = hook()
            if asyncio.iscoroutine(result):
                await result
        self._started = True

    async def shutdown(self) -> None:
        """Run shutdown hooks, then stop all connectors in reverse order."""
        for hook in reversed(self._shutdown_hooks):
            result = hook()
            if asyncio.iscoroutine(result):
                await result
        for name, connector in reversed(list(self._connectors.items())):
            try:
                await connector.stop()
                logger.info("Connector stopped: %s", name)
            except Exception as exc:
                logger.warning("Connector failed to stop cleanly: %s — %s", name, exc)
        self._started = False

    # ── Async context manager ────────────────────────────────────────────

    async def __aenter__(self) -> "LifecycleApp":
        await self.startup()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.shutdown()
