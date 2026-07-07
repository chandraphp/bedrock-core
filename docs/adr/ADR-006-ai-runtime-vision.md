# ADR-006 — AI Runtime Vision

**Date:** 2026-06-23  
**Status:** Accepted  
**Authors:** Chandu (Guntamukkala N Rama Chandra Shekar)

---

## Context

After v1.0.0 of ops-brain was shipped, an architectural review raised a
question that bedrock-core had not formally answered:

*What kind of thing is bedrock-core, precisely?*

The framework had accumulated the right primitives (Adapter, Capability,
Connector, Retriever, LifecycleApp, PromptRegistry) but had not yet defined
a long-term structural vision. Without that, future feature decisions would
be made case by case rather than against a consistent architectural principle.

---

## Decision

**bedrock-core is an AI Application Runtime.**

Not a framework. Not a toolkit. A runtime — the execution environment that
AI applications run on top of, the same way Python applications run on the
Python runtime and web applications run on a web server.

The analogy:

```
Python runtime     →  bedrock-core
Python application →  ops-brain / sec-brain / finops-brain
```

### The filter for every future feature

Before adding anything to bedrock-core, one question must be answered:

> *"Does this belong in every AI application, regardless of domain?"*

If **yes** → belongs in bedrock-core.  
If **no** → belongs in the application (ops-brain, etc.).

Examples:

| Feature | Belongs in |
|---|---|
| Event emission from every pipeline stage | bedrock-core |
| Composable workflow DAG | bedrock-core |
| Tool registry | bedrock-core |
| LLM/embedding/reranker provider interface | bedrock-core |
| Splunk log format | ops-brain |
| IncidentReport schema | ops-brain |
| SRE-specific prompts | ops-brain |
| Jira ticket mapping | ops-brain |

---

## The target runtime architecture

```
bedrock-core
    │
    ├── Runtime Graph        ← composable, observable execution engine
    │   ├── Workflow         ← ordered DAG of Stages
    │   ├── Stage            ← single unit of work (retrieve, rank, summarize, ...)
    │   └── Event Bus        ← every stage emits events; subscribers are pluggable
    │
    ├── Provider Interface   ← Chat | Embedding | Reranker | Vision
    │   └── (Anthropic, OpenAI, Ollama, Mock)
    │
    ├── Tool Registry        ← @tool decorator, auto-discovery
    │
    ├── Connector API        ← start/stop/health/execute (existing)
    │
    ├── Retriever Interface  ← (existing)
    │
    ├── PromptRegistry       ← versioned, compiled, A/B-testable (existing, extend)
    │
    ├── Memory               ← operational (incident→resolution→embedding), not chat history
    │
    ├── Policy Engine        ← can_execute(tool, context) → bool | ApprovalRequired
    │
    └── Configuration        ← hierarchical, SecretProvider-aware (existing, extend)
```

---

## Implementation order

Priority is set by cross-application evidence, not ambition.

### P0 — Implement now (proven need from ops-brain v1.0)

| Component | Evidence |
|---|---|
| Event Bus | PipelineTracer is bolted-on; events should be native |
| Runtime Graph / Workflow | RCAAgent is a hardcoded 6-stage pipeline; composability unproven |

### P1 — Implement when ops-brain Sprint 2 proves the need

| Component | Evidence required |
|---|---|
| Tool Registry | ops-brain needs ≥2 auto-discovered tools |
| Prompt Compiler | PromptRegistry A/B testing required by evaluation |
| Memory | Historical incident retrieval requested by ≥3 users |

### P2 — Implement when a second application (non-SRE) proves generality

| Component | Evidence required |
|---|---|
| Policy Engine | Enterprise user requires approval workflow |
| Secret Manager | SecretProvider needed by ≥2 different applications |
| Scheduler | Scheduled workflow needed by ≥2 different applications |

### Explicitly deferred (applications, not runtime)

- Multi-agent orchestration
- Autonomous remediation
- Browser agents
- AutoGPT-style planning
- Domain-specific connectors

---

## Competitive position

| Project | Category |
|---|---|
| LangChain | Agent framework |
| LlamaIndex | RAG framework |
| Haystack | Search + RAG |
| CrewAI | Multi-agent workflows |
| **bedrock-core** | **AI Application Runtime** |

bedrock-core does not compete feature-for-feature. It competes on:
- architecture clarity
- observability by design (not by instrumentation)
- API stability and governance
- production readiness defaults
- evidence-driven evolution

---

## Consequences

**Positive:**
- Every new feature has a clear acceptance test: "does this belong in every AI application?"
- The Event Bus makes bedrock-core observable without requiring applications to instrument themselves
- The Workflow Engine makes pipelines composable and testable in isolation
- A second non-SRE application can be built to validate generality before v2.0

**Negative:**
- P1 and P2 features require real cross-application evidence before implementation, which means deliberately slower expansion
- The runtime framing raises expectations — "runtime" implies stability guarantees that "framework" does not

## Validation

This ADR is correct if:
1. A second application (non-SRE domain) can be built on bedrock-core using only the public API, with the Event Bus and Workflow Engine as natural extension points
2. ops-brain's RCAAgent can be rewritten as a Workflow without changing the IncidentReport contract
3. The Event Bus enables OpenTelemetry export without changes to application code
