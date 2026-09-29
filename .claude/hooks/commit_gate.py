"""PreToolUse (Bash): every commit is green. Before any `git commit`, run the fast tier
(ruff, mypy, pytest -m "not slow"); block the commit if anything is red."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import block, project_dir, read_input

GIT_COMMIT = re.compile(r"\bgit\b(\s+-\S+(\s+\S+)?)*\s+commit\b")
TAIL_LINES = 40

GATE = [
    ("ruff check", ["uv", "run", "--quiet", "ruff", "check", "."]),
    ("mypy", ["uv", "run", "--quiet", "mypy"]),
    ("pytest (fast tier)", ["uv", "run", "--quiet", "pytest", "-q", "-m", "not slow"]),
]


def main() -> None:
    payload = read_input()
    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not GIT_COMMIT.search(cmd):
        return
    if "--no-verify" in cmd:
        block("BLOCKED: --no-verify is not allowed (invariant 6). Fix the failure instead.")
    root = project_dir(payload)
    for name, argv in GATE:
        p = subprocess.run(
            argv, cwd=root, capture_output=True, text=True, encoding="utf-8", check=False
        )
        if p.returncode:
            tail = "\n".join((p.stdout + p.stderr).strip().splitlines()[-TAIL_LINES:])
            block(f"COMMIT BLOCKED - {name} is red (invariant 6: every commit is green):\n{tail}")


if __name__ == "__main__":
    main()
