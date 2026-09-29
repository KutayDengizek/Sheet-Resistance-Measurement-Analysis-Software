"""PostToolUse (Write|Edit|MultiEdit): lint + type-check the Python file just written and feed
findings straight back to the agent (exit 2 -> stderr is shown to Claude)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import BLOCK, project_dir, read_input, rel_posix

CHECKED_ROOTS = ("src/", "tests/", "scripts/")


def run(root: Path, *cmd: str) -> tuple[int, str]:
    p = subprocess.run(
        ["uv", "run", "--quiet", *cmd],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> None:
    payload = read_input()
    root = project_dir(payload)
    path = (payload.get("tool_input") or {}).get("file_path", "")
    rel = rel_posix(path, root) if path else None
    if not rel or not rel.endswith(".py") or not rel.startswith(CHECKED_ROOTS):
        return
    problems = []
    code, out = run(root, "ruff", "check", "--output-format", "concise", rel)
    if code:
        problems.append(f"ruff check:\n{out}")
    code, out = run(root, "ruff", "format", "--check", "--diff", rel)
    if code:
        problems.append(f"ruff format (run `uv run ruff format {rel}`):\n{out[:2000]}")
    code, out = run(root, "mypy", rel)
    if code:
        problems.append(f"mypy --strict:\n{out}")
    if problems:
        print(
            f"Lint/type findings in {rel} - fix now while the file is in context:\n",
            file=sys.stderr,
        )
        print("\n\n".join(problems), file=sys.stderr)
        sys.exit(BLOCK)


if __name__ == "__main__":
    main()
