# Release Notes — v0.1.0-alpha

**bedrock-core** · **nb-ops-brain** · 2026-06-23

---

## What this release is

bedrock-core v0.1.0-alpha establishes the framework foundations for AI
applications: lifecycle management, configuration, extensibility, and a
versioned public API governed by a documented compatibility promise.

nb-ops-brain v0.1.0-alpha demonstrates those foundations through an
SRE-focused reference application built exclusively on bedrock-core's
public interfaces — no internal imports, no forks, no monkey-patches.

This is an **alpha release**. The public API is documented and tested,
but the project name, PyPI package name, and some capabilities are
intentionally incomplete pending validation.

---

## bedrock-core — What's included

### Public API (stable from this release)

| Symbol | Description |
|---|---|
| `App` | Root entry point |
| `LifecycleApp` | App + connector registry + async startup/shutdown |
| `Agent` | `agent.ask(prompt)` → `ExecutionResult` |
| `Runtime` | Composes capabilities |
| `ExecutionResult` | `.output`, `.metrics()`, `.trace()`, `.cost()` |
| `Adapter` | Base for LLM provider adapters |
| `Capability` / `ChatCapability` | Base + built-in chat capability |
| `Connector` / `ConnectorError` | Base for external system connectors |
| `BaseConfig` / `ConnectorConfig` / `LLMConfig` / `ConfigurationError` | Typed, validated, secret-redacting config |

### Providers

| Provider | Notes |
|---|---|
| `MockProvider` | Default. Offline, no API key. |
| `AnthropicProvider` | Claude models. `pip install "bedrock-core[anthropic]"` |
| `OpenAIProvider` | GPT models. `pip install "bedrock-core[openai]"` |
| `OllamaProvider` | Any local/on-prem model. No API key. Remote hosts supported. |

### Process

- Architecture fitness tests enforce layering invariants in CI
- Cross-repo CI gate: every bedrock-core PR runs nb-ops-brain's test suite
- Semantic versioning with documented compatibility promise (ADR-005)
- Evidence Log auto-updated on every push

---

## nb-ops-brain — What's included

- `NbOpsApp`: wraps `LifecycleApp`, registers connectors
- `SplunkConnector`: mock-first (synthetic events), real Splunk SDK optional
- CLI: `nb-ops "What errors occurred in the last hour?"`
- Mock mode runs offline with no Splunk, no API key, no network

---

## Known limitations (planned — not forgotten)

| Gap | Description | Target |
|---|---|---|
| GAP-003 | No `PromptRegistry` — prompts are inline strings, no versioning or templating | bedrock-core v0.3 |
| GAP-004 | No `Retriever` — naive full-context injection, will hit token limits at scale | bedrock-core v0.4 |
| Naming | `bedrock-core` is a working title. Final name pending PyPI/domain/trademark check | Before v1.0.0 |
| PyPI | Not yet published to PyPI | Before v1.0.0 stable |
| Plugin system | Interface not yet defined — requires ≥3 real implementations first | bedrock-core v0.2 |

Being explicit about what isn't implemented builds more trust than hiding it.

---

## How to try it

```bash
# bedrock-core — no API key needed
git clone https://github.com/chandraphp/bedrock-core.git
cd bedrock-core
pip install -e ".[dev]"
python3 examples/hello_world.py

# nb-ops-brain — no Splunk needed
git clone https://github.com/chandraphp/nb-ops-brain.git
cd nb-ops-brain
pip install -e ".[dev]"
nb-ops "What errors occurred in the last hour?"
```

---

## What comes next

Sprint 2 priorities are driven by the open gaps above and by Study 1
(external developer validation of bedrock-core). No features merge before
Study 1 exit criteria are met or gap evidence justifies an exception.
