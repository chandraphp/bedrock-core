# Evidence Log

A living record of design decisions and the evidence behind them.

Add a row before changing behavior. Move a row to **Accepted** or
**Rejected** only when real evidence exists — internal conviction doesn't
count, and neither does this document's own confidence.

---

## Promotion Ratio

Tracks internal experiments vs. public API promotions per release.
A decreasing ratio indicates increasing maturity — more exploration,
fewer commitments. The goal is not to maximize it; the goal is to
make it *measurable* so restraint is visible. (ADR-007)

| Release | Internal experiments | Public API promotions | Ratio | Notes |
|---|---|---|---|---|
| v0.1.0 | 5 | 7 | 140% | Bootstrap — primitives promoted from design, not experiments |
| v0.2.0 | 3 | 3 | 100% | Retriever, MockRetriever, Document — all had ops-brain evidence |
| v0.3.0 | 2 | 2 | 100% | Stage, StageResult promoted; Workflow kept internal (ADR-007) |

*Ratio > 100% in v0.1 reflects the bootstrap phase where primitives were
defined before a downstream application existed. From v0.2 onward, the
pattern should shift toward fewer promotions per experiment.*

## Promotion Candidates

Historical record of every public API promotion decision.
Future maintainers can understand why the API looks the way it does
without reading every ADR or PR thread.

| Candidate | Decision | Evidence | Release |
|---|---|---|---|
| `App`, `Agent` | Promoted | Designed as the public entry point; validated in Sprint 0 Quick Start | v0.1.0 |
| `Runtime`, `ExecutionResult` | Promoted | Core primitive; `Agent` is sugar over `Runtime` | v0.1.0 |
| `Adapter`, `Capability`, `ChatCapability` | Promoted | Extension points; validated by Mock + Anthropic + OpenAI providers | v0.1.0 |
| `Connector`, `ConnectorError` | Promoted | ops-brain SplunkConnector proved the interface (GAP-001) | v0.1.0 |
| `LifecycleApp` | Promoted | ops-brain needed async startup/shutdown (GAP-002) | v0.1.0 |
| `BaseConfig`, `ConnectorConfig`, `LLMConfig` | Promoted | ops-brain config refactor proved the pattern (GAP-005) | v0.1.0 |
| `Retriever`, `MockRetriever`, `Document` | Promoted | ops-brain SplunkRetriever proved the interface (GAP-004) | v0.2.0 |
| `Stage`, `StageResult` | Promoted | ops-brain RCAAgent has 6-stage structure; doc-qa experiment confirmed domain-independence | v0.3.0 |
| `EventBus`, event types | Promoted | PipelineTracer + CostAccounting + logging were duplicating observation; EventBus eliminates the duplication | v0.3.0 |
| `Workflow`, `WorkflowResult` | **Deferred** | Only one orchestration (RCAAgent); doc-qa experiment used plain loop — orchestration is application policy | Pending |

---

| Decision | Evidence | Status |
|---|---|---|
| `Agent` stays in the public API, not flattened into `Runtime`+`Capability` | Implemented end-to-end (Sprint 0) | Provisional — pending Study 1 |
| Internal architecture: `Runtime` → `Capability` → `Adapter` | `test_core_does_not_import_providers` passes | Accepted |
| Provider interface | `MockProvider` + `AnthropicProvider` + `OpenAIProvider` implemented with zero changes to `Adapter`/`Capability`/`Runtime`; `test_adding_a_provider_requires_no_core_changes` passes | Accepted |
| Operational data (`metrics`/`trace`/`cost`) lives on `ExecutionResult`, not on `Agent` | `test_operational_data_is_on_the_result_not_the_agent` passes | Accepted |
| Public API surface is `App`, `Agent`, `Runtime`, `ExecutionResult`, `Adapter`, `Capability`, `ChatCapability` | `test_public_api_surface_is_frozen` enforces it in CI | Accepted — frozen; changes require updating this row |
| Plugin interface | No plugin implementation exists yet | Deferred — do not design until ≥1 real plugin is built |
| Package/project name | Several `catalyst*` variants found already taken on PyPI | Deferred — `bedrock-core` is a placeholder only |
| `app.agent()` is understandable without explanation | — | Pending — Study 1 |
| TTFS < 5 min for first successful `agent.ask()` | — | Pending — Study 1 |
| Mock → real provider swap is clear | — | Pending — Study 2 (not started) |

## Commit History

Auto-updated on every push to main. Newest commits at the top.

| Commit | Date | Author | Message | Files Changed |
| --- | --- | --- | --- | --- |
| `2397641` | 2026-07-05 | Chandu | Add DESIGN_PRINCIPLES.md — the ten principles every contributor reads first | README.md, docs/DESIGN_PRINCIPLES.md, docs/decisions/evidence-log.md |
| `b16117a` | 2026-07-04 | Chandu | Stabilization notice: no new public APIs without ADR-007 evidence | README.md, docs/decisions/evidence-log.md |
| `83f8d66` | 2026-07-04 | Chandu | v0.3.1: doc-qa in CI, Promotion Candidates table, doc-qa README | .github/workflows/ci.yml, docs/decisions/evidence-log.md, examples/doc-qa/README.md |
| `9299690` | 2026-07-04 | Chandu | ADR-007 governance + generality experiment + promotion ratio tracking | CONTRIBUTING.md, docs/decisions/evidence-log.md, examples/doc-qa/app.py |
| `6096f3f` | 2026-07-04 | Chandu | ADR-007: Public APIs are promoted, not invented | CONTRIBUTING.md, docs/adr/ADR-007-public-apis-are-promoted-not-invented.md, docs/decisions/evidence-log.md |
| `6172a84` | 2026-07-04 | Chandu | PR review: remove Workflow from public API — abstraction not yet earned | docs/decisions/evidence-log.md, src/bedrock_core/__init__.py, src/bedrock_core/workflow.py, tests/test_architecture.py, tests/test_workflow_and_events.py |
| `1a75d0f` | 2026-07-03 | Chandu | Remove Workflow orchestration — not yet proven by a second pipeline | docs/decisions/evidence-log.md, src/bedrock_core/__init__.py, src/bedrock_core/stage.py, src/bedrock_core/workflow.py, tests/test_architecture.py, tests/test_workflow_and_events.py |
| `71ca335` | 2026-07-03 | Chandu | v0.3.0: Event Bus + Workflow Engine + ADR-006 + why-bedrock-core.md | docs/adr/ADR-006-ai-runtime-vision.md, docs/decisions/evidence-log.md, docs/why-bedrock-core.md, src/bedrock_core/__init__.py, src/bedrock_core/events.py, src/bedrock_core/workflow.py, tests/test_architecture.py, tests/test_workflow_and_events.py |
| `743d5a0` | 2026-06-23 | Chandu | v0.2.0: Retriever, MockRetriever, Document (GAP-004 resolved) | docs/decisions/evidence-log.md |
| `fe942fb` | 2026-06-23 | Chandu | v0.2.0: Add Retriever, MockRetriever, Document — resolves GAP-004 | RELEASE-NOTES-v0.1.0-alpha.md, docs/architecture.mermaid, docs/decisions/evidence-log.md, src/bedrock_core/__init__.py, src/bedrock_core/prompt.py, src/bedrock_core/retriever.py, tests/test_architecture.py |
| `41b0fd4` | 2026-06-23 | Chandu | ADR-005 addendum: versioning policy + public API surface doc | docs/adr/ADR-005-framework-application-separation.md, docs/decisions/evidence-log.md, docs/public-api.md |
| `e6a90cd` | 2026-06-23 | Chandu | Resolve GAP-001, GAP-002, GAP-005: Connector, LifecycleApp, Config | docs/decisions/evidence-log.md, src/bedrock_core/__init__.py, src/bedrock_core/config.py, src/bedrock_core/connector.py, src/bedrock_core/lifecycle.py, tests/test_architecture.py |
| `dad4bbc` | 2026-06-23 | Chandu | Add ADR-005 CI gate: cross-repo compatibility check against nb-ops-brain | .github/workflows/adr005-gate.yml, docs/decisions/evidence-log.md |
| `8aa08e4` | 2026-06-23 | Chandu | ADR-005: framework/application separation; update roadmap + CodeQL | .github/workflows/codeql.yml, ROADMAP.md, docs/adr/ADR-005-framework-application-separation.md, docs/decisions/evidence-log.md |
| `9e79300` | 2026-06-23 | Chandu | Update README to professional OSS standard; add CodeQL | .github/workflows/codeql.yml, .gitignore, README.md, docs/decisions/evidence-log.md |
| `26cceef` | 2026-06-22 | Chandu | Add community health files and repo credibility layer | .github/ISSUE_TEMPLATE/bug_report.md, .github/ISSUE_TEMPLATE/documentation.md, .github/ISSUE_TEMPLATE/feature_request.md, .github/PULL_REQUEST_TEMPLATE/pull_request_template.md, .github/dependabot.yml, CHANGELOG.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md, README.md, ROADMAP.md, SECURITY.md, docs/decisions/evidence-log.md |
| `6297657` | 2026-06-22 | Chandu | Add OllamaProvider: local/on-prem LLM support, zero API key | docs/decisions/evidence-log.md, examples/local_models.py, src/bedrock_core/app.py, src/bedrock_core/providers/ollama.py, tests/test_ollama.py |
| `9045dd1` | 2026-06-22 | Chandu | Add auto-update Evidence Log workflow + script | .github/workflows/update-evidence-log.yml, docs/decisions/evidence-log.md, scripts/update_evidence_log.py |
| `28ad084` | 2026-06-22 | Chandu | Add feedback tracker — connects observations to decisions | docs/validation/feedback-tracker.md |
