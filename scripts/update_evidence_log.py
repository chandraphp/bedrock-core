#!/usr/bin/env python3
"""Update docs/decisions/evidence-log.md with the latest git commit.

Usage (local):
    python3 scripts/update_evidence_log.py

Usage (CI — environment variables injected by GitHub Actions):
    COMMIT_SHA, COMMIT_DATE, COMMIT_AUTHOR, COMMIT_MSG, CHANGED_FILES
    are all set by the workflow before calling this script.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

EVIDENCE_LOG = pathlib.Path("docs/decisions/evidence-log.md")
SECTION_HEADER = "## Commit History"
TABLE_HEADER = "| Commit | Date | Author | Message | Files Changed |"
TABLE_DIVIDER = "| --- | --- | --- | --- | --- |"


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def get_commit_info() -> dict[str, str]:
    """Get info from env (CI) or from git directly (local)."""
    return {
        "sha":     os.environ.get("COMMIT_SHA")     or git("rev-parse", "--short", "HEAD"),
        "date":    os.environ.get("COMMIT_DATE")     or git("log", "-1", "--pretty=format:%ci").split()[0],
        "author":  os.environ.get("COMMIT_AUTHOR")   or git("log", "-1", "--pretty=format:%an"),
        "message": os.environ.get("COMMIT_MSG")      or git("log", "-1", "--pretty=format:%s"),
        "files":   os.environ.get("CHANGED_FILES")   or git("diff-tree", "--no-commit-id", "-r", "--name-only", "HEAD").replace("\n", ", "),
    }


def build_row(info: dict[str, str]) -> str:
    msg = info["message"].replace("|", "\\|")  # escape pipes so the table doesn't break
    files = info["files"] or "-"
    return f"| `{info['sha']}` | {info['date']} | {info['author']} | {msg} | {files} |"


def update_log(new_row: str) -> None:
    if not EVIDENCE_LOG.exists():
        print(f"ERROR: {EVIDENCE_LOG} not found. Run from the repo root.", file=sys.stderr)
        sys.exit(1)

    content = EVIDENCE_LOG.read_text()

    if SECTION_HEADER not in content:
        # First run — append the whole Commit History section
        section = (
            f"\n\n{SECTION_HEADER}\n\n"
            "Auto-updated on every push to main. Newest commits at the top.\n\n"
            f"{TABLE_HEADER}\n{TABLE_DIVIDER}\n{new_row}\n"
        )
        EVIDENCE_LOG.write_text(content.rstrip() + section)
        print(f"Created Commit History section and logged: {new_row}")
        return

    # Insert new row immediately after the divider line inside the Commit History table
    lines = content.splitlines()
    in_section = False
    insert_after = -1

    for i, line in enumerate(lines):
        if line.strip() == SECTION_HEADER:
            in_section = True
        if in_section and line.strip() == TABLE_DIVIDER:
            insert_after = i
            break

    if insert_after < 0:
        print("ERROR: Could not find table divider in Commit History section.", file=sys.stderr)
        sys.exit(1)

    lines.insert(insert_after + 1, new_row)
    EVIDENCE_LOG.write_text("\n".join(lines) + "\n")
    print(f"Logged: {new_row}")


if __name__ == "__main__":
    info = get_commit_info()
    row = build_row(info)
    update_log(row)
