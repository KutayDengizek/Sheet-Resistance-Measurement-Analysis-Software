"""SessionStart + Stop hooks protecting the memory layer.

session_state.py start  -> record the session's baseline commit; remind to /resume
session_state.py stop   -> if files changed this session but PROGRESS.md did not, remind to
                           /handoff (shown to the user; non-blocking, once per change-set)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import git, project_dir, read_input

IGNORED_PREFIXES = (".claude/state/",)


def state_file(root: Path, session_id: str) -> Path:
    d = root / ".claude" / "state"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"session-{session_id or 'unknown'}.json"


def start(root: Path, session_id: str) -> None:
    sf = state_file(root, session_id)
    if not sf.exists():  # keep the original baseline across resume/compact
        head = git(root, "rev-parse", "HEAD").strip()
        sf.write_text(json.dumps({"baseline": head, "reminded": ""}), encoding="utf-8")
    print("Session protocol: run /resume first (MEMORY.md, PROGRESS.md, last journal note).")


def stop(root: Path, session_id: str) -> None:
    sf = state_file(root, session_id)
    state = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {}
    baseline = state.get("baseline") or "HEAD"
    changed = set(git(root, "diff", "--name-only", baseline).split())
    changed |= set(git(root, "ls-files", "--others", "--exclude-standard").split())
    changed = {f for f in changed if not f.startswith(IGNORED_PREFIXES)}
    if not changed or "PROGRESS.md" in changed:
        return
    digest = hashlib.sha1("\n".join(sorted(changed)).encode()).hexdigest()
    if state.get("reminded") == digest:
        return
    state["reminded"] = digest
    sf.write_text(json.dumps(state), encoding="utf-8")
    msg = (
        f"{len(changed)} file(s) changed this session but PROGRESS.md was not updated. "
        "Run /handoff before ending the session."
    )
    print(json.dumps({"systemMessage": msg}))


def main() -> None:
    payload = read_input()
    root = project_dir(payload)
    sid = str(payload.get("session_id", ""))
    {"start": start, "stop": stop}[sys.argv[1]](root, sid)


if __name__ == "__main__":
    main()
