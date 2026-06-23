"""Architecture fitness tests.

These don't test behavior — they test that the structural decisions made in
ADRs actually hold in the code, so architecture can't silently drift.
"""

from __future__ import annotations

import ast
import pathlib

SRC = pathlib.Path(__file__).resolve().parents[1] / "src" / "bedrock_core"
CORE_MODULES = ["adapter.py", "capability.py", "runtime.py"]


def _imported_modules(path: pathlib.Path) -> set[str]:
    tree = ast.parse(path.read_text())
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name)
    return modules


def test_core_does_not_import_providers():
    """Layering invariant: Adapter/Capability/Runtime must not know about any
    concrete provider. Only app.py (the public sugar layer) is allowed to —
    that's what lets a provider be added without touching the core."""
    for filename in CORE_MODULES:
        modules = _imported_modules(SRC / filename)
        provider_imports = {m for m in modules if m and "providers" in m}
        assert not provider_imports, (
            f"{filename} imports {provider_imports} — core layers must not "
            "depend on concrete providers."
        )


def test_public_api_surface_is_frozen():
    """Catches accidental additions to or removals from the public API.
    Update `expected` deliberately, with an ADR — not by accident."""
    import bedrock_core

    expected = {
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
    }
    assert set(bedrock_core.__all__) == expected


def test_adding_a_provider_requires_no_core_changes():
    """Evidence test for the interface-freeze decision: both real providers
    (anthropic, openai) must subclass Adapter and implement only its public
    methods — proving the interface generalized across two structurally
    different SDKs without modification."""
    from bedrock_core.adapter import Adapter
    from bedrock_core.providers.anthropic import AnthropicProvider
    from bedrock_core.providers.openai import OpenAIProvider

    for provider_cls in (AnthropicProvider, OpenAIProvider):
        assert issubclass(provider_cls, Adapter)
        # No provider should define methods outside Adapter's contract plus __init__.
        adapter_methods = {"complete", "estimate_cost"}
        own_methods = {
            name
            for name, value in vars(provider_cls).items()
            if callable(value) and not name.startswith("_")
        }
        assert own_methods <= adapter_methods, (
            f"{provider_cls.__name__} defines extra public methods {own_methods - adapter_methods} "
            "— the Adapter interface may not actually be sufficient yet."
        )
