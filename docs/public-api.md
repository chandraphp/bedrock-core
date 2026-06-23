# Public API

Every symbol listed here is exported via `bedrock_core.__all__` and covered
by the compatibility promise in [ADR-005](adr/ADR-005-framework-application-separation.md).

**Anything not on this list is internal and may change without notice.**

Changes to this list require:
- a PR that updates `bedrock_core.__all__`
- the `test_public_api_surface_is_frozen` architecture test updated to match
- this file updated in the same commit
- a CHANGELOG entry
- a major version bump if symbols are *removed* or *renamed*

---

## Stable public symbols — v0.1.0-alpha

### Application entry points

| Symbol | Description |
|---|---|
| `App` | Root entry point. `app = App(); agent = app.agent()` |
| `LifecycleApp` | `App` subclass with connector registry and async startup/shutdown |
| `Agent` | Sugar API: `agent.ask(prompt)` → `ExecutionResult` |

### Core runtime

| Symbol | Description |
|---|---|
| `Runtime` | Composes `Capability` instances and executes them by name |
| `ExecutionResult` | Return type of `agent.ask()`. Carries `.output`, `.metrics()`, `.trace()`, `.cost()` |

### Extension points

| Symbol | Description |
|---|---|
| `Adapter` | Abstract base for LLM/provider adapters. Implement `complete()` and `estimate_cost()` |
| `Capability` | Abstract base for runtime capabilities (chat, retrieve, evaluate, ...) |
| `ChatCapability` | Built-in capability: single-turn chat completion |
| `Connector` | Abstract base for external system connectors. Implement `start()`, `stop()`, `health()`, `execute()` |
| `ConnectorError` | Exception raised when a connector operation fails. Wraps provider-specific exceptions. |

### Configuration

| Symbol | Description |
|---|---|
| `BaseConfig` | Base for all config dataclasses. Provides secret redaction and `to_dict()` |
| `ConnectorConfig` | Base connector config: `mock`, `timeout` from env vars |
| `LLMConfig` | Standard LLM config: `provider`, `model`, `api_key`, `timeout` from env vars |
| `ConfigurationError` | Raised when required config is missing or invalid |

---

## Not public (internal — do not import directly)

- `bedrock_core.app._resolve_provider`
- `bedrock_core.lifecycle` (module) — use `from bedrock_core import LifecycleApp`
- `bedrock_core.providers.*` — use `app.agent(provider="anthropic")` or pass an `Adapter` instance
- Any symbol not listed above
