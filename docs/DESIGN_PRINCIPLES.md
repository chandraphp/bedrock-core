# Design Principles

These principles govern every decision in the bedrock-core ecosystem —
framework evolution, API changes, experiments, and documentation. They are
not aspirations. They are the distilled lessons from building ops-brain
on top of bedrock-core across six sprints, seven ADRs, and multiple
architectural review cycles.

Read these before reading any code. They explain why the code looks the
way it does.

---

## 1. Runtime before applications

bedrock-core is a runtime — the execution environment that AI applications
run on top of. It does not know what a Splunk event, an incident report,
or a Jira ticket is. It knows what a Stage, an Event, a Connector, and a
Retriever are.

Applications (ops-brain, doc-qa, future consumers) own domain logic.
The runtime owns execution primitives. That boundary is enforced by CI.

*See: ADR-005, cross-repo compatibility gate.*

---

## 2. Evidence before abstraction

A public API is a long-term commitment. New symbols are added to
`bedrock_core.__all__` only after at least two independent consumers
independently converge on the same primitive.

"This looks architecturally clean" is not evidence.
"Two applications independently needed this" is.

The question before every API addition: *Could this remain internal for
one more release cycle without blocking anything?* If yes, it should.

*See: ADR-007, Promotion Candidates table, Promotion Ratio metric.*

---

## 3. Providers are replaceable

An application that works with one LLM provider should work with any
other by changing a single configuration value. The same applies to
embedding models, vector stores, and connectors.

No application-level code should import a provider SDK directly.
All provider-specific logic lives behind an Adapter or Connector.
This is verified by `test_bedrock_core_is_the_only_ai_dependency`.

*See: Adapter interface, ADR-005.*

---

## 4. Every conclusion cites evidence

An IncidentReport without cited sources is an opinion. An ADR without
observed evidence is a guess. An experiment without raw data is anecdote.

Every answer — from the LLM, from the framework, from the team — should
be traceable to the observation that supports it. When evidence is
insufficient, say so explicitly. Silence is not a citation.

*See: CitationEngine, Evidence Log, experiment PLAN/RESULTS separation.*

---

## 5. Unknowns are explicit

An `IncidentReport.unknowns` field that is empty is different from one
that is absent. A baseline measurement marked "N/A" is different from
one that was never measured. Gaps in understanding are real information.

Explicit unknowns build more trust than false completeness.
"We don't know yet" is a valid answer; omitting the question is not.

*See: IncidentReport.unknowns, baseline/v1.0.0-mock.md.*

---

## 6. Public APIs are earned

The framework's public API (`bedrock_core.__all__`) is smaller than its
internal implementation. That gap is intentional. Internal code can
change freely; public symbols carry a compatibility promise measured in
years, not sprints.

Every PR that adds a public symbol must include an Evidence section.
Reviewers check for it the same way they check for tests.

*See: ADR-007, CONTRIBUTING.md reviewer checklist.*

---

## 7. Applications validate the runtime

ops-brain does not exist to showcase bedrock-core features. It exists to
discover missing runtime primitives. Every GAP entry in the Framework Gap
Log is the result of ops-brain encountering a missing abstraction and
waiting for it to be added to the framework rather than working around it.

The promotion path flows upward:
```
application (ops-brain)
    ↓ discovers need
bedrock-core internal
    ↓ survives second consumer
bedrock-core public API
```

*See: Framework Gap Log, ADR-005 validation criteria.*

---

## 8. Experiments are immutable

A PLAN.md committed before running cannot be revised to match results
seen afterward. A RESULTS.md written after running cannot retroactively
change the hypothesis. Raw data in `raw/` is never edited.

This ordering — hypothesis before results — protects against the most
common form of engineering bias: shaping methodology to fit outcomes
already observed. The PLAN/RESULTS/raw separation exists for this reason.

*See: benchmarks/experiments/TEMPLATE/, ADR-006 validation criteria.*

---

## 9. Observability is built in

A pipeline that produces output but emits no events is a black box.
Every Stage in the runtime publishes `STAGE_STARTED`, `STAGE_COMPLETED`,
and `STAGE_FAILED` events. Every investigation records latency, tokens,
cost, and confidence through the PipelineTracer.

Subscribers — OpenTelemetry exporters, cost trackers, loggers, alerting —
register without touching execution code. Execution and observation are
orthogonal.

*See: EventBus, PipelineTracer, CostAccounting.*

---

## 10. Simplicity beats completeness

A framework that does ten things reliably is more valuable than one that
does a hundred things inconsistently. The goal is not to have the most
integrations, the most adapters, or the most features. The goal is to
have the right primitives — the ones that every AI application needs,
done well enough that they require no workarounds.

When in doubt about whether to add something: wait. If multiple
applications independently ask for it, add it then. If they don't, the
omission was correct.

*See: bedrock-core stabilization notice, Promotion Ratio.*

---

## The one question

When any decision is unclear, ask:

> *Does this belong in every AI application, regardless of domain?*

If yes — it may belong in bedrock-core, pending evidence.
If no — it belongs in the application.

That question is the runtime boundary, made operational.

---

## Non-Goals

bedrock-core deliberately does not aim to:

- **Become a model server.** Use Ollama, vLLM, or cloud providers instead.
  bedrock-core provides the Adapter interface that connects to them.

- **Replace vector databases.** The Retriever interface is an abstraction
  over retrieval — not a database. Persistent storage belongs in the
  application layer.

- **Be an all-in-one AI framework.** The goal is the smallest set of
  primitives that every AI application needs, not the largest set that
  any AI application could want.

- **Contain domain-specific logic.** SRE, security, finance, healthcare —
  none of these concepts belong in bedrock-core. They belong in applications
  that depend on it.

- **Predict future abstractions.** Abstractions are promoted after multiple
  applications independently discover them, not before any application has
  needed them.

- **Hide uncertainty from downstream systems.** An answer without evidence,
  a report without unknowns, a confidence score without calibration — these
  are forms of hidden uncertainty. Explicit gaps are preferable to false
  completeness.

- **Optimize benchmarks at the expense of reproducibility.** A number that
  cannot be reproduced by another engineer is not a measurement. Every
  experiment result includes the methodology and raw data needed to
  recalculate it independently.

- **Grow the public API without evidence.** Every symbol in
  `bedrock_core.__all__` carries a compatibility promise measured in years.
  Adding to it without evidence from multiple consumers is taking on
  long-term maintenance debt without demonstrated value.

---

## The unofficial motto

> *What evidence would change this decision?*

This question applies to code reviews, ADRs, experiments, roadmap items,
and framework evolution. It guards against the most common form of
engineering failure: continuing to build something whose value has never
been tested against reality.

If contributors internalize this question, they will not just contribute
code — they will contribute evidence.
