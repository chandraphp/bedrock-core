# Evidence Log

A living record of design decisions and the evidence behind them.

Add a row before changing behavior. Move a row to **Accepted** or
**Rejected** only when real evidence exists — internal conviction doesn't
count, and neither does this document's own confidence.

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
| `e6a90cd` | 2026-06-23 | Chandu | Resolve GAP-001, GAP-002, GAP-005: Connector, LifecycleApp, Config | docs/decisions/evidence-log.md, src/bedrock_core/__init__.py, src/bedrock_core/config.py, src/bedrock_core/connector.py, src/bedrock_core/lifecycle.py, tests/test_architecture.py |
| `dad4bbc` | 2026-06-23 | Chandu | Add ADR-005 CI gate: cross-repo compatibility check against nb-ops-brain | .github/workflows/adr005-gate.yml, docs/decisions/evidence-log.md |
| `8aa08e4` | 2026-06-23 | Chandu | ADR-005: framework/application separation; update roadmap + CodeQL | .github/workflows/codeql.yml, ROADMAP.md, docs/adr/ADR-005-framework-application-separation.md, docs/decisions/evidence-log.md |
| `9e79300` | 2026-06-23 | Chandu | Update README to professional OSS standard; add CodeQL | .github/workflows/codeql.yml, .gitignore, README.md, docs/decisions/evidence-log.md |
| `26cceef` | 2026-06-22 | Chandu | Add community health files and repo credibility layer | .github/ISSUE_TEMPLATE/bug_report.md, .github/ISSUE_TEMPLATE/documentation.md, .github/ISSUE_TEMPLATE/feature_request.md, .github/PULL_REQUEST_TEMPLATE/pull_request_template.md, .github/dependabot.yml, CHANGELOG.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md, README.md, ROADMAP.md, SECURITY.md, docs/decisions/evidence-log.md |
| `6297657` | 2026-06-22 | Chandu | Add OllamaProvider: local/on-prem LLM support, zero API key | docs/decisions/evidence-log.md, examples/local_models.py, src/bedrock_core/app.py, src/bedrock_core/providers/ollama.py, tests/test_ollama.py |
| `9045dd1` | 2026-06-22 | Chandu | Add auto-update Evidence Log workflow + script | .github/workflows/update-evidence-log.yml, docs/decisions/evidence-log.md, scripts/update_evidence_log.py |
| `28ad084` | 2026-06-22 | Chandu | Add feedback tracker — connects observations to decisions | docs/validation/feedback-tracker.md |
