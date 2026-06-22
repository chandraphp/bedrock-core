# Roadmap

This roadmap is evidence-gated. A phase doesn't start until the previous
phase has been externally validated. We do not add scope to satisfy a roadmap;
we update the roadmap to reflect what evidence tells us to build next.

---

## ✅ Sprint 0 — Foundation (complete)

**Goal:** can a minimal AI runtime provide a clean public API while hiding a
composable internal architecture?

**Exit criteria met:**
- Public API (`App → agent() → ask()`) works offline in under 5 minutes
- `Runtime → Capability → Adapter` layering enforced by fitness tests
- Three providers validated (Mock, Anthropic, OpenAI, Ollama) with zero
  core changes — provider interface considered stable
- CI green on Python 3.10–3.12

---

## 🔄 Validation — Study 1 (in progress)

**Goal:** does an engineer who didn't build this understand and use it
without help?

**Exit criteria:**
- ≥ 3 independent engineers complete the Quick Start
- ≥ 2 complete it without any assistance
- Average TTFS < 10 minutes
- No critical installation failures
- Public API unchanged after review, or changes backed by documented evidence

See `docs/validation/first-user-study.md` for the session script.

---

## ⏳ Sprint 1 — From "Hello World" to "Useful" (pending Study 1)

Scope will be set by Study 1 findings. Current candidates (subject to change):

- Structured logging on every execution (request ID, duration, provider, tokens, cost)
- Unified exception hierarchy (no provider-specific exceptions leaking)
- Configuration loading (`BEDROCK_PROVIDER`, `BEDROCK_MODEL` env vars)
- Plugin interface — design only after ≥ 1 real plugin is implemented
- Study 2: provider-swap UX validation (mock → real provider)

---

## 🔮 Future (unscheduled — requires evidence)

These are candidates, not commitments. Each requires a user study or
issue evidence before entering a sprint.

| Feature | Waiting for |
|---|---|
| Plugin interface freeze | ≥ 3 plugin types implemented |
| Memory / RAG | Sprint 1 complete + Study 2 |
| MCP integration | Plugin interface stable |
| Workflow orchestration | Memory + MCP stable |
| Final package name + PyPI publish | PyPI/GitHub/domain/trademark check |
| Studio / Hub UI | Core framework mature |

---

## What we will not build (deliberately)

- A "batteries included" framework that hides operational behaviour
- Provider lock-in of any kind
- Features without a documented observation justifying them
