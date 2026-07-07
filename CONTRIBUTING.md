# Contributing to bedrock-core

Thank you for considering a contribution. This document explains how we work.

## Our standard

Every change should leave the project more understandable, more reliable, or
more usable than it was before. We prefer small, focused contributions over
large ones. We value clarity over cleverness.

## Before you open a pull request

1. **Check for an existing issue.** If none exists, open one first so we can
   discuss the problem before you spend time on a solution.
2. **Read the Evidence Log** (`docs/decisions/evidence-log.md`). It explains
   why the project looks the way it does. Understanding it prevents PRs that
   conflict with established decisions.
3. **No feature is complete until someone outside the core team has used it.**
   If your contribution introduces a new public API, be prepared to include
   a runnable example and at least one external validation.

## Development setup

```bash
git clone https://github.com/chandraphp/bedrock-core.git
cd bedrock-core
pip install -e ".[dev]"
python3 examples/hello_world.py   # should work immediately
```

## Before every commit

All four must pass:

```bash
ruff check src tests examples   # lint
mypy src                        # type check
pytest -v                       # tests
python3 examples/hello_world.py # smoke test
```

CI enforces the same checks. A PR isn't ready until CI is green.

## What we accept

| Type | Notes |
|---|---|
| Bug fixes | Always welcome. Include a test that reproduces the bug. |
| Documentation improvements | Always welcome. |
| New providers | Must implement `Adapter` with zero changes to core. Include tests that run offline (mock the HTTP/SDK call). |
| New capabilities | Open an issue first. Must fit the `Capability` interface. |
| New public API | Requires an ADR and external validation before merge. |
| Features without evidence | Will be deferred until user studies justify them. |

## What we defer

- Memory, RAG, MCP, Workflows, Studio, Hub — these are planned but not
  yet in scope. Opening issues to track interest is welcome; PRs implementing
  them will be deferred until the core is stable.
- Anything that changes the public API surface without an ADR and evidence.

## Commit message format

```
<type>: short description (under 72 chars)

Optional longer explanation. Include the observation that motivated
the change if it came from user feedback.
```

Types: `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Adding a new public API symbol

Every PR that adds a new symbol to `bedrock_core.__all__` must include an
**Evidence** section in the PR description answering:

- How many independent consumers currently use this abstraction?
- Were those consumers written independently, or did one follow from the other?
- What would break if this symbol were removed in six months?

A PR without this section will be returned with a review request, the same
way a PR without tests would be. See [ADR-007](docs/adr/ADR-007-public-apis-are-promoted-not-invented.md).

**Example — insufficient evidence (keep internal):**

```
## Evidence
Consumers: RCAAgent (ops-brain)
Independent implementations: None
Recommendation: Keep in bedrock_core.workflow, not in __all__
```

**Example — sufficient evidence (promote):**

```
## Evidence
Consumers: RCAAgent, EvaluationPipeline, ScanPipeline (all in ops-brain)
Shared semantics: All three iterate stages, emit events, return typed result
Recommendation: Promote Workflow to public API
```

## Promotion vs. Implementation

New capabilities should normally begin as internal implementations within
an application (such as ops-brain). Only after demonstrating reuse across
at least two independent consumers should they be proposed for promotion
into bedrock-core. Contributors are encouraged to optimize for evidence
rather than early abstraction.

The question to ask before opening a PR that touches `__all__`:

> "Could this remain internal for one more release cycle?"

If the answer is "yes," it should.

## Reviewer checklist for public API changes

These are architectural questions, not implementation questions. Reviewers
should work through them for any PR that adds or changes a public symbol:

- [ ] Is there at least one real consumer already using this?
- [ ] Is the abstraction domain-independent (no SRE, security, or finance concepts)?
- [ ] Could this remain internal for one more release without blocking anything?
- [ ] Could this live in an external package rather than the core?
- [ ] Is the promotion justified by evidence from multiple consumers?

If the answer to any of the last three is "yes," request changes.
