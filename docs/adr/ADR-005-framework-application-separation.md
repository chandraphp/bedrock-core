# ADR-005 — Framework / Application Separation

**Date:** 2026-06-23
**Status:** Accepted
**Supersedes:** none
**Superseded by:** none

---

## Context

During Sprint 0, a question arose about whether domain-specific SRE
capabilities (Splunk ingestion, RCA, anomaly detection, Jira/Teams/Slack
integration) should be built inside bedrock-core or in a separate repository.

The original "NB Ops Brain" and "SRE Ops Brain" projects already exist as
standalone applications. The question is whether to merge them into the
framework or keep them separate.

## Decision

**bedrock-core is a domain-agnostic AI application runtime.**

It will never contain knowledge of Splunk indexes, Jira tickets, Kubernetes
pods, incident schemas, or any other domain-specific concept.

A second repository — **nb-ops-brain** — will be the flagship application
built on top of bedrock-core. It depends on bedrock-core as a library
(`pip install bedrock-core`) and implements SRE-specific logic on top.

```
bedrock-core  (this repo)
    LLM abstraction
    RAG pipeline
    Vector store interfaces
    Agent framework
    Prompt management
    Evaluation
    Observability
    Plugin system
    Memory
    Workflow orchestration
    Connectors SDK
         ↓
         pip install bedrock-core
         ↓
nb-ops-brain  (separate repo)
    Splunk ingestion
    Dynatrace integration
    Jira / JSM connector
    Microsoft Teams / Slack ChatOps
    Kubernetes context
    RCA pipeline
    Anomaly detection
    SRE-specific prompts and agents
```

## Consequences

**Positive:**
- bedrock-core stays domain-agnostic and reusable beyond SRE
- nb-ops-brain can evolve at its own pace without framework API churn
- Portfolio demonstrates both framework engineering and applied AI
- Other teams can build non-SRE applications on bedrock-core
- Architecture mirrors successful open-source splits (FastAPI / full-stack
  apps, LangGraph / domain agents, Haystack / search applications)

**Negative:**
- Two repositories to maintain
- bedrock-core features must be general enough to serve nb-ops-brain without
  special-casing; this is a forcing function for good API design

## Validation

This decision is correct if:
1. nb-ops-brain can be built entirely using bedrock-core's public API, with
   no patches or forks to the framework itself
2. A third application (non-SRE domain) could be built on bedrock-core using
   the same APIs nb-ops-brain uses

**Sprint 1 evidence for (1):** GAP-001 (Connector), GAP-002 (LifecycleApp),
and GAP-005 (Config) were identified by nb-ops-brain, resolved in bedrock-core,
and consumed by nb-ops-brain using only the public API. No forks, no internal
imports, no monkey-patches required. ADR-005 validated in practice.

---

## Addendum: Cross-Repository Versioning Policy

*Added 2026-06-23 — effective from bedrock-core v0.1.0-alpha.*

### Public API contract

Only symbols exported through `bedrock_core.__all__` are considered stable
and covered by the compatibility promise.

**Supported imports:**
```python
from bedrock_core import Connector
from bedrock_core import LifecycleApp
from bedrock_core import LLMConfig
```

**Unsupported imports** (internal, may change without notice):
```python
from bedrock_core.lifecycle import ...   # internal module
from bedrock_core.app import _resolve_provider  # private symbol
```

The canonical list of stable public symbols is maintained in
[`docs/public-api.md`](../public-api.md).

### Semantic versioning

bedrock-core follows [Semantic Versioning 2.0.0](https://semver.org).

| Release type | When used | Migration guide required |
|---|---|---|
| Patch (0.1.x) | Bug fixes, no public API changes | No |
| Minor (0.x.0) | New public capabilities, backwards compatible | No |
| Major (x.0.0) | Removed or changed public APIs | Yes — before release |

### Compatibility requirement for downstream applications

nb-ops-brain (and any other downstream application) **must**:
- depend on an officially released version of bedrock-core (not a git ref or local path in production)
- build and pass its full test suite against that release
- never require source patches, monkey-patches, private imports, or repository forks

If nb-ops-brain cannot meet these requirements, the missing capability is a
bedrock-core sprint item — not an application workaround.

### Continuous validation (CI gate)

Every pull request to bedrock-core:
1. Builds a distributable wheel from the PR branch
2. Clones nb-ops-brain
3. Installs the fresh wheel into a clean environment
4. Runs nb-ops-brain's full test suite

A failing downstream test **blocks the merge** until either:
- compatibility is restored, or
- the breaking change is documented with a migration guide and the major version is incremented

