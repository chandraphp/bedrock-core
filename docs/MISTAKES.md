# Mistakes

Abstractions introduced too early. Assumptions invalidated by experiments.
APIs that never became public. Features removed because evidence didn't
support them.

Projects rarely publish their mistakes. These lessons are often more
valuable for future maintainers than any success story.

---

## Format

Each entry has:
- **What we did**
- **Why it seemed right at the time**
- **What we learned**
- **What changed**

---

## M-001 — Workflow promoted before evidence (2026-06-23)

**What we did:** During the v0.3.0 development cycle, a `Workflow` class
was proposed for the public `bedrock_core.__all__`. It was implemented,
tested, and documented before the PR was reviewed.

**Why it seemed right at the time:** The orchestration pattern was clean.
The stages existed. The event bus was ready. The abstraction felt like the
natural next layer.

**What we learned:** "Architecturally clean" is not the same as "earned
by evidence." At the time of the PR, only one workflow existed (RCAAgent).
The doc-qa experiment later showed that a plain loop was sufficient for a
second domain — meaning the orchestration abstraction was not required by
a second independent consumer.

**What changed:** `Workflow` was removed from `__all__` and kept as an
internal class in `bedrock_core.workflow`. ADR-007 was written to encode
the lesson. The PR evidence requirement was added to CONTRIBUTING.md.

*This was the first time the project's own discipline was applied to the
project's own code by an external reviewer. That review improved the
framework more than the feature itself would have.*

---

## M-002 — Planning documents that planned future planning (2026-06-xx)

**What we did:** In the early sessions, multiple architecture documents
were produced that described what architecture documents would be produced
next. Several "sprints" concluded with a deliverable of "begin planning."

**Why it seemed right at the time:** The architectural questions were
genuinely important. Getting them right before writing code seemed prudent.

**What we learned:** Documents that plan future planning are a failure
mode, not progress. The corrective was the 1:3 rule: for every one
architecture document, three engineering deliverables. And the clearest
signal that planning had gone too far was noticing that three consecutive
meetings had ended with "we should start building."

**What changed:** The 1:3 rule became an explicit project discipline.
The first working code (`App → agent() → ask()`) was built specifically
to interrupt a planning loop that had run too long.

---

*Entries are added when a mistake is identified — whether during active
development, in a retrospective, or when an experiment invalidates an
assumption. Future mistakes are expected and welcome: they are evidence
that the project is testing its assumptions against reality.*
