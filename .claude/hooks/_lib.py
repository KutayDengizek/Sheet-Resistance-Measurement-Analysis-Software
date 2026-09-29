"""Shared helpers for the Claude Code hook scripts in this directory (stdlib only)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# UTF-8 in and out regardless of the Windows console code page.
sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

BLOCK = 2  # exit code that makes Claude Code block the tool call and show stderr to the agent


def read_input() -> dict[str, Any]:
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw.strip() else {}


def project_dir(payload: dict[str, Any]) -> Path:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    return Path(root).resolve()


def rel_posix(path: str, root: Path) -> str | None:
    """Project-relative POSIX path, or None if the path lies outside the project."""
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    try:
        rel = os.path.relpath(p.resolve(), root)
    except ValueError:  # different drive on Windows
        return None
    rel = rel.replace("\\", "/")
    return None if rel.startswith("../") or rel == ".." else rel


def git(root: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8", check=False
    )
    return out.stdout


def golden_approval(root: Path) -> tuple[bool, str]:
    """A golden-data change is approved iff .claude/approvals/golden.approved names an
    Accepted ADR. The approvals directory is human-only (writes are blocked by protect_paths)."""
    marker = root / ".claude" / "approvals" / "golden.approved"
    if not marker.is_file():
        return False, "no approval marker at .claude/approvals/golden.approved"
    m = re.search(r"ADR-(\d{4})", marker.read_text(encoding="utf-8"))
    if not m:
        return False, "approval marker does not name an ADR (expected 'ADR-NNNN')"
    adrs = list((root / "docs" / "adr").glob(f"ADR-{m.group(1)}-*.md"))
    if not adrs:
        return False, f"approval marker names ADR-{m.group(1)}, but no such file in docs/adr/"
    if not re.search(r"^Status:\s*Accepted", adrs[0].read_text(encoding="utf-8"), re.M):
        return False, f"{adrs[0].name} is not 'Status: Accepted'"
    return True, f"approved by {adrs[0].name}"


def block(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(BLOCK)
