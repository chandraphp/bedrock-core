# Roadmap

This roadmap is evidence-gated. A phase doesn't start until the previous
phase has been externally validated. Scope is set by user study findings,
not internal assumptions.

See [ADR-005](docs/adr/ADR-005-framework-application-separation.md) for
the framework / application separation decision.

---

## Two repositories, one ecosystem

```
bedrock-core          ← you are here
    domain-agnostic AI runtime

nb-ops-brain          ← coming next
    SRE application built on bedrock-core
    Splunk · Dynatrace · Jira · Teams · Slack · Kubernetes · RCA
```

---

## bedrock-core roadmap

### ✅ Sprint 0 — Foundation (complete)

- Public API: `App → agent() → ask()`
- Internal `Runtime → Capability → Adapter` architecture
- Providers: Mock, Anthropic, OpenAI, Ollama (local/on-prem)
- Architecture fitness tests + CI on Python 3.10–3.12
- Evidence Log, Feedback Tracker, User Study instrument

### 🔄 Study 1 — External validation (in progress)

Exit criteria before Sprint 1 starts:
- ≥ 3 independent engineers complete the Quick Start
- ≥ 2 complete without assistance
- Average TTFS < 10 minutes
- No critical install failures
- Public API unchanged, or changes backed by documented evidence

### ⏳ Sprint 1 — From "Hello World" to "Useful"

_Scope set by Study 1 findings. Current candidates:_

- Structured logging (request ID, duration, provider, tokens, cost)
- Unified exception hierarchy — no provider-specific exceptions leak
- Configuration loading (`BEDROCK_PROVIDER`, `BEDROCK_MODEL` env vars)
- Plugin interface — after ≥ 1 real plugin is built and tested
- Study 2: provider-swap UX validation (mock → real provider)

### ⏳ Sprint 2 — Plugin system

- Plugin interface freeze (after ≥ 3 plugin types validated)
- Logging plugin
- Reference enterprise plugin

### ⏳ Sprint 3 — RAG framework

- Vector store adapter interface
- Retrieval capability
- Chunking and embedding pipeline
- Citation support on ExecutionResult

### ⏳ Sprint 4 — Agent orchestration

- Multi-step agent loop
- Tool use capability
- Memory interface

### ⏳ Sprint 5 — Evaluation & observability

- Built-in eval harness
- Benchmark runner
- Structured trace export (OpenTelemetry)

### ⏳ Sprint 6 — Stable v1.0

- Final package name (pending PyPI/GitHub/domain/trademark)
- Public PyPI release
- LTS policy

---

## nb-ops-brain roadmap (separate repo)

| Sprint | Focus |
|---|---|
| 1 | Splunk ingestion → embeddings → vector store |
| 2 | RAG with citations |
| 3 | LLM-powered Root Cause Analysis |
| 4 | Anomaly detection and incident correlation |
| 5 | ChatOps: Jira, Microsoft Teams, Slack |
| 6 | Evaluation, benchmarking, AI observability |

nb-ops-brain depends on bedrock-core as a library. It will not patch or
fork the framework — if it needs something the framework doesn't have,
that becomes a bedrock-core Sprint N candidate backed by real evidence.

---

## What we will not build in bedrock-core

- Domain-specific logic (SRE, finance, legal, etc.)
- A UI / Studio (third-party apps or nb-ops-brain can build this)
- Features without a documented observation justifying them
