# Feedback Tracker

Connects raw developer observations to decisions made.
One row per finding. Updated after every study, issue, or discussion that changes something.

**Rule:** no change to the framework, docs, or API without a row here first.

---

## Open (observed, not yet decided)

| # | Source | Raw observation | Interpretation | Priority |
|---|---|---|---|---|
| | | | | |

---

## Decided

| # | Source | Raw observation | Interpretation | Decision | Commit |
|---|---|---|---|---|---|
| F-001 | Founder — first local run (2026-06-22) | `zsh: command not found: python` | macOS does not alias `python` → `python3` by default | Updated README, example, and CI to use `python3` | `2d4bb9c` |

---

## Closed / Won't Fix

| # | Source | Raw observation | Reason closed |
|---|---|---|---|
| | | | |

---

## Sources key

| Code | Meaning |
|---|---|
| `study-1` | Structured user study, Study 1 (onboarding/TTFS) |
| `study-2` | Structured user study, Study 2 (provider swap) |
| `gh-issue-N` | GitHub Issue #N |
| `gh-discussion-N` | GitHub Discussion #N |
| `linkedin` | LinkedIn comment or DM |
| `founder` | Internal observation by founder |
