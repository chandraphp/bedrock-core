# examples/doc-qa

A minimal document Q&A application that validates bedrock-core's runtime
primitives are genuinely domain-independent.

## Why this exists

This example is a **framework validation experiment**, not a feature demo.

After building ops-brain (an SRE application), a question arose: are `Stage`,
`StageResult`, and `EventBus` truly general runtime primitives, or are they
SRE abstractions that happen to look generic?

The only way to answer that is to build something with no SRE concepts and
see if the primitives feel natural. This example is that experiment.

**What it intentionally does not use:**
- No Splunk, no IncidentReport, no RCA pipeline
- No ops-brain imports of any kind
- No SRE-specific terminology

**What it does use:**
- `Stage` — each processing step (load, chunk, retrieve, answer)
- `StageResult` — typed output from each stage
- `EventBus` — timing collected via subscription, zero changes to stages
- `MockRetriever` / `Document` — retrieval over Markdown content
- `App` / `Agent` — LLM call for the answer step

## Run it

```bash
# Against bedrock-core's own docs (no setup required)
python3 examples/doc-qa/app.py docs/ "What is the public API?"

# Against any directory of Markdown files
python3 examples/doc-qa/app.py /path/to/your/docs/ "your question"
```

## What it proved (ADR-007 evidence)

Result from running against 8 bedrock-core documentation files:

| Primitive | Transferred naturally? | Notes |
|---|---|---|
| `Stage` | ✅ | 4 stages, zero SRE imports |
| `StageResult` | ✅ | Implicit via stage loop |
| `EventBus` | ✅ | Timing collected without touching stages |
| `Document` | ✅ | Used with Markdown, not Splunk events |
| `Workflow` | N/A — not needed | Plain loop sufficed; supports ADR-007 deferral |

This result was recorded in the Evidence Log and influenced the promotion
decision for v0.3.0: Stage and EventBus were promoted; Workflow was deferred.

## CI role

This example runs in CI on every push. If it breaks, either:
- a bedrock-core change broke the public API contract, or
- a previously-stable primitive acquired a domain-specific dependency

Either outcome is worth catching before merge.
