# ADR-007 — Public APIs Are Promoted, Not Invented

**Date:** 2026-07-03  
**Status:** Accepted  
**Trigger:** PR review of Runtime Graph / Workflow Engine (bedrock-core v0.3.0)

---

## Context

During development of the Runtime Graph (ADR-006), a `Workflow` abstraction
was proposed for the public bedrock-core API alongside `Stage`, `StageResult`,
and the `EventBus`.

Review identified that:

- Only one workflow implementation existed: `RCAAgent` in ops-brain
- No second independent application had exercised the orchestration layer
- The abstraction was proposed because it *looked* architecturally correct,
  not because multiple consumers had independently converged on it

This produced the first "Approve with changes" review in the project's history.

---

## Decision

**Public APIs in bedrock-core are promoted from proven internal use — not
invented based on anticipated need.**

The promotion path for any abstraction is:

```
1. Implement internally (in ops-brain or bedrock_core.internal)
2. Survive real usage in at least one application
3. Observe whether a second independent application needs the same primitive
4. If yes — and only then — promote to bedrock_core.__all__
```

For orchestration specifically:

`Workflow` remains internal (`bedrock_core.workflow`) until at least **two
independent workflows** demonstrate common orchestration semantics. Candidates:
`ScanWorkflow`, `EvaluationWorkflow`, `AlertEnrichmentWorkflow`.

The following *were* promoted in v0.3.0 because they had clear evidence:

| Symbol | Evidence |
|---|---|
| `Stage`, `StageResult` | RCAAgent's 6-stage structure already existed; Stage formalises an existing pattern |
| `EventBus`, event types | PipelineTracer, CostAccounting, and logging all observed execution independently — duplication is evidence of a missing primitive |

---

## PR evidence requirement

Every PR that adds a new public API symbol must include an **Evidence** section:

```markdown
## Evidence

**Current consumers:** RCAAgent (ops-brain)  
**Independent implementations:** None  
**Recommendation:** Keep internal — insufficient evidence for promotion
```

or, when promotion is warranted:

```markdown
## Evidence

**Consumers:** RCAAgent, EvaluationPipeline, ScanPipeline (all in ops-brain)  
**Shared semantics:** All three iterate stages sequentially, emit events,
  and return a typed result — 94% identical orchestration logic  
**Recommendation:** Promote `Workflow` to public API
```

A PR that adds a public symbol without an Evidence section should be
blocked by reviewers, the same way a PR without tests would be.

---

## The promotion ratio

A healthy framework promotes only a small fraction of its internal ideas.
This is not stagnation — it is restraint.

Tracking internal experiments vs. promoted APIs over time gives a signal
that is more useful than feature count: it shows whether the framework is
growing because reality demanded it, or because authors preferred it.

---

## Consequences

**For contributors:**  
New public APIs require evidence, not just architectural justification.
"This looks clean" is not sufficient. "Two independent consumers converged
on this" is.

**For ops-brain:**  
ops-brain is the primary laboratory for bedrock-core evolution. Every
abstraction in ops-brain that survives real usage is a candidate for
promotion. The application should never feel constrained to avoid internal
experimentation — constraint applies only to the *promotion* decision.

**For the framework:**  
The public API intentionally lags internal experimentation. This is a feature,
not a bug. A small, stable public API is more valuable than a large, speculative one.

---

## Validation

This ADR is working correctly if:

1. `Workflow` is eventually promoted — with evidence from two independent workflows — rather than remaining internal indefinitely
2. Future PRs include Evidence sections before reviewers have to ask
3. The promotion ratio (internal experiments / promoted symbols) can be measured over time from the git history

---

## The feedback loop

```
Applications (ops-brain, future apps)
        ↓
Evidence (multiple independent consumers)
        ↓
ADR (documents the promotion decision)
        ↓
Framework (bedrock_core.__all__ grows by one)
```

Not the reverse. The framework does not decide what applications need.
Applications discover what the framework should provide.
