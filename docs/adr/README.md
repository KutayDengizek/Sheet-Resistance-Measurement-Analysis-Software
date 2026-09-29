# Architecture Decision Records

One file per significant decision: `ADR-NNNN-kebab-title.md`, numbered sequentially. An ADR is
**immutable once Accepted**. To change a decision, write a new ADR that supersedes the old one and
set the old one's status to `Superseded by ADR-NNNN`. Only the status line of an Accepted ADR may be edited.

**Required for:** a new runtime dependency; any change to the CSV input contract, the output format,
or the statistical estimators; any change to `tests/golden/`; any deliberate deviation from a
CLAUDE.md invariant; anything that is "on purpose" but looks odd.

Statuses: `Proposed` → `Accepted` (the human decides) · `Superseded by ADR-NNNN` · `Rejected`.
Agents may draft ADRs as `Proposed`. Only the human changes a status to `Accepted`.

## Golden-data approval procedure (human)
1. Accept an ADR that explains why the expected outputs change.
2. Create `.claude/approvals/golden.approved` containing `ADR-NNNN`. Agents cannot write this
   directory; the hooks block it.
3. The agent runs `uv run python scripts/regenerate_golden.py` (skill `regenerate-golden`) and
   commits the diff together with the ADR.
4. Delete the marker afterwards, so the approval covers one change only.

## Template
```markdown
# ADR-NNNN: <title>
Status: Proposed
Date: YYYY-MM-DD

## Context
<the forces at play; what problem prompted this>

## Decision
<what we do, stated precisely enough to test>

## Alternatives considered
- <option> — <why not>

## Consequences
<what becomes easier or harder; what must now be kept true; which tests or notes change>
```
