# Why bedrock-core?

When evaluating an AI framework, the first question is usually:
*"Why not LangChain / LlamaIndex / LlamaIndex / CrewAI?"*

This document answers that directly.

---

## The one-sentence answer

bedrock-core is an **AI Application Runtime** — the execution environment
your AI application runs on top of. The others are frameworks that solve
specific AI problems. That's a different abstraction level.

---

## The landscape

| Project | Category | Core abstraction |
|---|---|---|
| LangChain | Agent framework | Chains and agents |
| LlamaIndex | RAG framework | Indexes and query engines |
| Haystack | Search + RAG | Pipelines and components |
| CrewAI | Multi-agent | Crews and tasks |
| Semantic Kernel | Enterprise SDK | Skills and planners |
| Pydantic AI | Typed agents | Type-safe agent contracts |
| **bedrock-core** | **AI Runtime** | **Workflow · Event Bus · Provider · Connector** |

bedrock-core doesn't try to win on breadth of features. It competes on:
- architectural clarity
- observability as a first-class concern (not bolted on)
- API stability with CI-enforced compatibility
- production defaults (mock-first, lifecycle management, typed config)
- evidence-driven evolution (public API changes require ADRs and cross-repo validation)

---

## Why not LangChain?

LangChain has a vast ecosystem and moves fast. That's also its problem for
production use: the public API changes frequently, abstractions like "Chain"
and "Agent" mix orchestration with execution, and observability requires
third-party integrations.

bedrock-core's position: LangChain is an excellent prototyping tool.
bedrock-core is what you build on when you need to run something in production
for three years without rewriting the integration layer every quarter.

In bedrock-core's architecture, LangChain could be an `Adapter` —
a provider you optionally drop in, not a dependency that shapes everything.

---

## Why not LlamaIndex?

LlamaIndex is excellent at RAG. bedrock-core's `Retriever` abstraction is
deliberately similar in spirit — it learned from LlamaIndex's design.

The difference: LlamaIndex is a RAG framework. bedrock-core is the runtime
that RAG (and agents, and tools, and connectors) runs inside. `Retriever`
in bedrock-core is one extension point among many, not the core abstraction.

---

## Why not CrewAI?

CrewAI makes multi-agent workflows approachable. bedrock-core makes
single-agent, production-grade applications with proper lifecycle management,
observability, and API stability first — then multi-agent later, as an
application-layer concern.

The principle: solve one problem well before composing it.

---

## What bedrock-core does differently

### 1. Observable by design

In most frameworks, observability is an afterthought — you add logging,
then tracing, then metrics, each as a separate integration.

In bedrock-core, every runtime component (Workflow, Stage, Provider,
Retriever) publishes typed events to the Event Bus. Subscribers — OTel
exporters, loggers, cost trackers, alerting — register without touching
execution code.

### 2. Composable pipelines, not hardcoded chains

```python
# Other frameworks: hardcoded pipeline
result = chain.run(prompt)

# bedrock-core: composable Workflow
workflow = Workflow(
    RetrieveStage(retriever),
    RankStage(),
    SummarizeStage(agent),
    EvaluateStage(evaluator),
)
result = workflow.run(query)
```

Each Stage is independently testable, replaceable, and reusable across
different Workflows. The pipeline is data, not code.

### 3. Provider interface, not provider lock-in

```python
# Swap providers without touching application code
agent = app.agent(provider="mock")         # offline dev
agent = app.agent(provider="ollama",       # local inference
                  model="qwen2.5:9b")
agent = app.agent(provider="anthropic",    # production
                  model="claude-sonnet-4-6")
```

The `Adapter` interface extends to Chat, Embedding, Reranker, and Vision
without changing the `Capability` or `Runtime` layers.

### 4. Cross-repo compatibility as a CI gate

When ops-brain (a downstream application) is updated to depend on a new
bedrock-core version, a CI workflow in bedrock-core builds a fresh wheel
and runs ops-brain's full test suite against it before any PR merges.

Breaking the downstream application blocks the framework PR. This is
enforced automatically, not by convention.

---

## When to use bedrock-core

✅ You're building a production AI application that needs to run reliably
for months or years.

✅ You want observability, lifecycle management, and typed configuration
without wiring them together yourself.

✅ You want to swap LLM providers without changing application code.

✅ You need a stable public API you can version and commit to.

---

## When not to use bedrock-core

❌ You're prototyping and need 50 integrations immediately — LangChain
has a larger ecosystem today.

❌ You're building a RAG search application primarily — LlamaIndex has
more mature indexing primitives.

❌ You need multi-agent orchestration out of the box — CrewAI is further
along on that specific problem.

---

## The framework/application boundary

bedrock-core never contains domain-specific logic. The clearest illustration:

```
bedrock-core knows:          ops-brain knows:
─────────────────            ────────────────
Workflow                     IncidentReport
Stage                        SplunkConnector
EventBus                     RCAAgent
Retriever                    TimelineBuilder
Adapter                      Jira ticket mapping
Connector                    SRE-specific prompts
```

This boundary is enforced in CI. Any PR that adds SRE, security, or
domain-specific concepts to bedrock-core is rejected by the ADR-005 gate.

That separation is what makes bedrock-core reusable across domains.
```

ops-brain                   sec-brain (future)
    ↑                           ↑
    └───────── bedrock-core ────┘
```
