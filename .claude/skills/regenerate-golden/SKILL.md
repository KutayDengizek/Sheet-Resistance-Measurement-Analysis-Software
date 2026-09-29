---
name: regenerate-golden
description: Create or update expected outputs in tests/golden/ - only with an Accepted ADR and a human-created approval marker. Also covers building the initial baseline and validating the validator.
---
# Regenerate golden data

The golden files are the oracle. Their silent corruption invalidates every later "green". The hooks
block all writes to `tests/golden/`, and any run of `regenerate_golden`, unless
`.claude/approvals/golden.approved` names an Accepted ADR.

1. **Preconditions.** An Accepted ADR explains why the outputs are created or changed. The human
   has created the approval marker. Agents cannot create it; if it is missing, ask.
2. **Before regenerating**, run the fast tier and save the current failing diff (if any) for the
   journal. A regeneration must be explainable line by line by the ADR.
3. **Regenerate:** `uv run python scripts/regenerate_golden.py`. It writes one
   `tests/golden/<sample>.json` per fixture sample. Never hand-edit the JSON.
4. **Inspect the diff** (`git diff tests/golden`). Every changed number must follow from the ADR.
   Anything unexplained means stop and report.
5. **Validate the validator** (first baseline, and after any comparator change): plant a deliberate
   bug, for example ddof 1 → 0 in `stats`. Confirm the golden test fails **and** that its message
   shows the differing quantity. Revert the bug. Record "mutation caught" in the journal.
6. **Commit** the golden diff together with a reference to the ADR:
   `test(golden): regenerate per ADR-NNNN`.
7. Ask the human to delete the approval marker, so each approval covers exactly one change.

**Done when:** the golden files are committed, the ADR is referenced, the mutation check passed, and the marker is removed.
