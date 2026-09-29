"""The only sanctioned writer of tests/golden/ (skill: regenerate-golden).

Guarded by .claude/hooks/protect_paths.py: agents may run it only while
.claude/approvals/golden.approved names an Accepted ADR.
"""

import sys


def main() -> int:
    print(
        "regenerate_golden: stats not implemented yet (Phase 3 in PROGRESS.md). Nothing written.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
