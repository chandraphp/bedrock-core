# bedrock-core (placeholder name)

> **Naming notice:** `bedrock-core` is a working name only. Per ADR-003, no
> branding is finalized until PyPI, the GitHub organization, the relevant
> domains, and trademark are all checked. Do not build tooling or docs that
> assume this name is permanent.

A small, production-minded runtime for AI agents. This repository is the
**Proof of Engineering** slice for Sprint 0 — the smallest version of the
public API that has to work before any other feature is built.

## Quick Start (under 2 minutes, no API key)

```bash
pip install -e ".[dev]"
python examples/hello_world.py
```

```python
from bedrock_core import App

app = App()
agent = app.agent()          # defaults to the built-in mock provider
result = agent.ask("Hello")

print(result.output)
print(result.metrics())      # elapsed_ms, token counts
print(result.trace())        # step-by-step execution trace
print(result.cost())         # cost estimate (0.0 for the mock provider)
```

To use a real model instead of the mock provider:

```bash
pip install -e ".[anthropic]"
export ANTHROPIC_API_KEY=sk-...
```

```python
agent = app.agent(provider="anthropic", model="claude-sonnet-4-6")
```

## Architecture (read in under 5 minutes)

Three internal primitives, one public sugar API on top:

```
Adapter      -- talks to one external system (an LLM API, a DB, ...)
Capability   -- one thing the runtime can do (chat, retrieve, evaluate, ...),
                backed by exactly one Adapter
Runtime      -- composes Capabilities and executes them

App / Agent  -- public sugar API: Agent is a Runtime pre-wired with a
                ChatCapability, so `agent.ask(...)` reads naturally without
                hiding the composable core from anyone who wants to extend it
```

**Design decision:** metrics, trace, and cost live on the `ExecutionResult`
returned by `agent.ask(...)`, not as mutable state on the agent itself. This
keeps `Agent` simple even as the number of operational signals grows, and
keeps each call's data isolated from every other call.

## Why a mock provider is the default

Every adapter should be developable and testable with zero network access
and zero API keys before it's ever pointed at a real provider. `MockProvider`
is what `App.agent()` uses by default, and what CI runs against — this is
the same mock-first pattern used in production observability tooling, where
swapping a real backend in is a one-line change, not a rewrite.

## Status

This is Sprint 0 only. Explicitly out of scope until a later sprint: memory,
RAG, MCP, workflows, a Studio/Hub UI, and any provider beyond Anthropic's
Claude (used here as the one real reference adapter).

## Contributing

CI runs `ruff` (lint), `mypy` (types), `pytest` (tests), and the Quick Start
example itself, on Python 3.10–3.12. A PR isn't done until all four pass.
