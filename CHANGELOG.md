# Changelog

All notable changes to bedrock-core are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [0.0.1-alpha] — 2026-06-22

First tagged release. Sprint 0 deliverables only.

### Added

- `App` / `Agent` public sugar API: `app = App(); agent = app.agent(); result = agent.ask(...)`
- Internal `Runtime → Capability → Adapter` layered architecture
- `ExecutionResult` with `.metrics()`, `.trace()`, `.cost()` — operability
  lives on the execution, not the agent
- `MockProvider` — default, offline, no API key required
- `AnthropicProvider` — Claude models via `pip install "bedrock-core[anthropic]"`
- `OpenAIProvider` — GPT models via `pip install "bedrock-core[openai]"`
- `OllamaProvider` — any local/on-prem model via Ollama, including remote
  hosts (`OllamaProvider(host="http://gpu-server-01:11434")`)
- Architecture fitness tests: layering invariant, frozen public API surface,
  provider-interface-sufficiency check
- CI: ruff, mypy, pytest, Quick Start smoke test on Python 3.10–3.12
- Evidence Log (`docs/decisions/evidence-log.md`) — auto-updated on push
- Feedback Tracker (`docs/validation/feedback-tracker.md`)
- First-user-study validation instrument (`docs/validation/first-user-study.md`)

### Fixed

- `python` → `python3` in README, example, and CI — macOS does not alias
  `python` by default. *First evidence-driven fix (F-001).*

### Deferred

- Plugin interface — requires ≥1 real implementation before freeze
- Memory, RAG, MCP, Workflows, Studio, Hub — Sprint 1+ concerns
- Final package/project name — pending PyPI, GitHub org, domain, and
  trademark review

---

[Unreleased]: https://github.com/chandraphp/bedrock-core/compare/v0.0.1-alpha...HEAD
[0.0.1-alpha]: https://github.com/chandraphp/bedrock-core/releases/tag/v0.0.1-alpha
