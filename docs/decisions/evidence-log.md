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
| `28ad084` | 2026-06-22 | Chandu | Add feedback tracker — connects observations to decisions | docs/validation/feedback-tracker.md |
