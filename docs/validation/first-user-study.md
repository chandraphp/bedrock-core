# First User Study

Purpose: find out whether someone who didn't build this can understand and
use it without help. Every finding here is worth more than another feature.

No feature gets merged until at least one study below shows a successful run.

**Scope of this round (Study 1):** onboarding, installation, API clarity,
and TTFS using the default mock provider — no API key required. Provider-swap
UX (mock → real) is a separate, later study (Study 2); don't conflate the two.

---

## Session script (hand this section to the reviewer, nothing else)

You have ~30 minutes. Work through the tasks below out loud — narrate what
you're thinking, especially anything that confuses you or doesn't match
what you expected. Nobody will explain anything during the session.

1. **Install it.** Clone the repo, install the package. No assistance.
2. **Run Hello World.** Get `examples/hello_world.py` running. No assistance.
3. **Swap in a real provider.** Replace the mock provider with a real one
   (Anthropic or OpenAI). Note where you hesitate or have to guess.
4. **Explain the architecture back.** Read the Architecture section of the
   README, then describe Runtime / Capability / Adapter / Agent in your own
   words, as if explaining it to a teammate.
5. **What would you build first?** What's the first real thing you'd try to
   build with this?

---

## Time to First Success (TTFS)

| Milestone | Target | Actual |
|---|---|---|
| Clone | < 1 min | |
| Install | < 2 min | |
| First successful `agent.ask()` | < 5 min | |
| First modification (e.g. swap provider) | < 10 min | |

## Scorecard (reviewer fills in, 1–5)

| Category | Score | Notes |
|---|---|---|
| Installation | | |
| Documentation | | |
| API clarity | | |
| Error messages | | |
| Code organization | | |
| Test readability | | |
| Confidence to contribute | | |

**"What would stop you from using this in a side project?"**

>

---

## Per-session record

Copy the block below for each session.

### Session N — [date]

- **Reviewer role:** (e.g. "Senior Python Engineer", "SRE", "ML Engineer")
- **TTFS:** clone __ / install __ / first success __ / first modification __
- **Where they got stuck:**
- **Scenario observed** (A: smooth / B: confused by `App()` / C: install
  failed / D: questioned the Agent/Runtime split / E: couldn't find
  `ExecutionResult` / other):
- **Their explanation of the architecture, in their words:**
- **What they'd build first:**
- **Scorecard:** (paste table above, filled in)
- **What changed afterward** (doc fix / API change / nothing — and why):
