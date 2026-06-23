# Bedrock Core

> ### ⚠️ Project Naming Notice
>
> **"Bedrock Core" is currently a working title.**
> The architecture, APIs, documentation, and roadmap are considered stable
> for early development, but the project name may change before the first
> stable (v1.0.0) release.
>
> If you fork or integrate this project, please avoid hard-coding the
> repository name into production systems.
>
> A permanent name will be announced before the first stable release.

[![CI](https://github.com/chandraphp/bedrock-core/actions/workflows/ci.yml/badge.svg)](https://github.com/chandraphp/bedrock-core/actions/workflows/ci.yml)
[![CodeQL](https://github.com/chandraphp/bedrock-core/actions/workflows/codeql.yml/badge.svg)](https://github.com/chandraphp/bedrock-core/actions/workflows/codeql.yml)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://pypi.org/project/bedrock-core/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-success)](https://github.com/chandraphp/bedrock-core/security/dependabot)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![Status](https://img.shields.io/badge/status-alpha-orange)](CHANGELOG.md)

A production-minded Python runtime for AI agents. Operability — metrics,
traces, cost — is built in by default, not bolted on as a plugin.

---

## Quick Start (under 2 minutes, no API key)

```bash
git clone https://github.com/chandraphp/bedrock-core.git
cd bedrock-core
pip install -e ".[dev]"
python3 examples/hello_world.py
```

```python
from bedrock_core import App

app = App()
agent = app.agent()           # mock provider — no API key, no network
result = agent.ask("Explain Kubernetes in one sentence.")

print(result.output)
print(result.metrics())       # elapsed_ms, token counts
print(result.trace())         # step-by-step execution trace
print(result.cost())          # cost estimate (0.0 for local/mock providers)
```

### Use a cloud provider

```bash
pip install -e ".[anthropic]"
export ANTHROPIC_API_KEY=sk-...
```
```python
agent = app.agent(provider="anthropic", model="claude-sonnet-4-6")
```

### Use a local / on-prem model (Ollama)

```bash
ollama pull qwen2.5:9b   # or llama3.2, deepseek-r1, mistral, ...
```
```python
from bedrock_core.providers.ollama import OllamaProvider

agent = app.agent(provider=OllamaProvider(model="qwen2.5:9b"))
result = agent.ask("What caused the spike in error rate at 14:32?")
print(result.cost())   # {'usd': 0.0, 'note': 'local model — no cost incurred'}
```

---

## Architecture

Three internal primitives, one public API on top:

```
Adapter      ── talks to one external system (LLM API, DB, queue, ...)
Capability   ── one thing the runtime can do (chat, retrieve, evaluate, ...)
Runtime      ── composes Capabilities and executes them

App / Agent  ── public sugar: Agent is Runtime + ChatCapability pre-wired,
                so agent.ask(...) reads naturally without hiding the core
```

Operability lives on the **execution result**, not the agent:

```python
result = agent.ask("Summarise today's incidents")
result.metrics()   # {'elapsed_ms': 412.3, 'tokens': {'prompt': 18, 'completion': 94}}
result.trace()     # [{'step': 'chat.request', ...}, {'step': 'chat.response', ...}]
result.cost()      # {'usd': 0.000142, 'note': 'estimated from placeholder rates'}
```

This keeps `Agent` simple even as the operational surface grows, and isolates
each call's data from every other call — the same mental model used in
distributed tracing.

---

## Providers

| Provider | Install | Key required |
|---|---|---|
| `mock` (default) | none | ❌ |
| `anthropic` | `pip install -e ".[anthropic]"` | ✅ `ANTHROPIC_API_KEY` |
| `openai` | `pip install -e ".[openai]"` | ✅ `OPENAI_API_KEY` |
| `ollama` | Ollama running locally | ❌ |

---

## Repository Health

| | |
|---|---|
| ✅ Apache-2.0 License | ✅ Contributing Guide |
| ✅ CI / CD | ✅ Roadmap |
| ✅ Security Policy | ✅ Changelog |
| ✅ Code of Conduct | ✅ Issue Templates |
| ✅ Dependabot | ✅ Pull Request Template |
| ⏳ CodeQL (enable in Settings) | ⏳ Protected main branch |
| ⏳ Discussions (enable in Settings) | |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version:

```bash
ruff check src tests examples   # lint
mypy src                        # types
pytest -v                       # tests
python3 examples/hello_world.py # smoke
```

All four must pass. A PR isn't done until CI is green.

No feature is accepted without a documented observation justifying it.
See the [Evidence Log](docs/decisions/evidence-log.md) and
[Feedback Tracker](docs/validation/feedback-tracker.md).

---

## Roadmap

See [ROADMAP.md](ROADMAP.md). Current status: **Sprint 0 complete —
external validation (Study 1) in progress.**

Upcoming: structured logging, unified exception hierarchy, configuration
loading, plugin interface (after first real plugin is built).

---

## License

Apache-2.0 — see [LICENSE](LICENSE).
