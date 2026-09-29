"""PreToolUse (Write|Edit|MultiEdit|NotebookEdit|Bash): protect source-of-truth paths.

Rules (see CLAUDE.md invariants 1-2 and docs/adr/):
  .claude/approvals/**  human-only; agents may never write here
  .git/**, .venv/**, .env*  never written by tools
  tests/fixtures/**     raw instrument exports: append-only (new files OK, existing files immutable)
  tests/golden/**       expected outputs: writable only with a valid golden approval marker
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import block, golden_approval, project_dir, read_input, rel_posix

FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
# Shell verbs that modify or destroy files (a heuristic outer wall, not a parser).
MUTATING = re.compile(
    r"(\brm\b|\bmv\b|\bsed\s+-i|\btruncate\b|\btee\b|(?<![\d=-])>(?!&)|\bgit\s+(rm|mv|checkout|restore|clean)\b"
    r"|\bRemove-Item\b|\bSet-Content\b|\bOut-File\b|\bdel\b|\bunlink\b|\bshutil\b|\bos\.remove\b)"
)
COPY_INTO = re.compile(r"\b(cp|Copy-Item|robocopy|xcopy)\b")


def check_file(rel: str, root: Path, tool: str) -> None:
    if rel.startswith(".claude/approvals/"):
        block(
            f"BLOCKED: {rel} is human-only. Approval markers must be created by a human "
            "(see docs/adr/README.md). Ask the user."
        )
    if rel.startswith((".git/", ".venv/")) or rel.split("/")[-1].startswith(".env"):
        block(f"BLOCKED: {rel} is generated/secret and must not be written by tools.")
    if rel.startswith("tests/fixtures/"):
        exists = (root / rel).exists()
        if tool != "Write" or exists:
            block(
                f"BLOCKED: {rel} is a raw instrument export (invariant 1). Existing fixture files "
                "are immutable; add a NEW sample folder instead (skill: add-fixture-sample)."
            )
    if rel.startswith("tests/golden/"):
        ok, why = golden_approval(root)
        if not ok:
            block(
                f"BLOCKED: {rel} is golden reference data (invariant 2): {why}. "
                "Golden data changes only via scripts/regenerate_golden.py + an Accepted ADR + "
                "a human-created approval marker (skill: regenerate-golden). Never edit it to make "
                "a test pass."
            )


def check_bash(cmd: str, root: Path) -> None:
    c = cmd.replace("\\", "/")
    if ".claude/approvals" in c and (MUTATING.search(c) or COPY_INTO.search(c)):
        block("BLOCKED: .claude/approvals/ is human-only. Ask the user to create the marker.")
    if "tests/fixtures" in c and MUTATING.search(c):
        block(
            "BLOCKED: shell command would modify/delete raw fixture data in tests/fixtures/ "
            "(invariant 1). Fixtures are append-only; use 'cp -n' into a new sample folder."
        )
    touches_golden = "tests/golden" in c and (MUTATING.search(c) or COPY_INTO.search(c))
    if touches_golden or "regenerate_golden" in c:
        ok, why = golden_approval(root)
        if not ok:
            block(f"BLOCKED: golden data change without approval (invariant 2): {why}.")


def main() -> None:
    payload = read_input()
    root = project_dir(payload)
    tool = payload.get("tool_name", "")
    tin = payload.get("tool_input") or {}
    if tool in FILE_TOOLS:
        path = tin.get("file_path") or tin.get("notebook_path")
        if path and (rel := rel_posix(path, root)) is not None:
            check_file(rel, root, tool)
    elif tool == "Bash" or tool == "PowerShell":
        check_bash(tin.get("command", ""), root)


if __name__ == "__main__":
    main()
