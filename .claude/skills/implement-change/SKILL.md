---
name: implement-change
description: Standard unit of work for adding or changing behavior in src/sheetres (parser, stats, cli) - test-first, invariant-checked, reviewed, committed green.
---
# Implement one unit of work

1. **Scope.** Restate the unit in one sentence. Read exactly the component note in
   `docs/components/` and any ADR it links. If the change needs a decision that no Accepted ADR
   covers (an estimator, the input contract, the output format, a dependency), stop: draft a
   Proposed ADR and ask the human.
2. **Test first.** Write or extend tests in `tests/` that fail for the right reason:
   - Build parser inputs from `tests/fixtures/<sample>/`, or from small CSVs created in `tmp_path`
     for the error cases.
   - Numeric expectations must be computed **by hand in the test** (with the formula written
     out), never copied from running the implementation.
   - Every error path gets a test that asserts the exception type and that the message names the file.
3. **Implement** the smallest change that passes. Keep `stats` pure. Put units in names.
   Name every constant. The lint/type hook reports findings after each write; fix them immediately.
4. **Verify.** Follow skill `verify` (fast tier).
5. **Review.** Invoke the `reviewer` agent on `git diff`. Address every BLOCKING item. Record
   any NOTE you choose not to address in the journal.
6. **Docs.** Update the component note (its status, interface, quirks). Add pitfalls to MEMORY.md.
7. **Commit** atomically: `feat(parser): … because …`. The commit hook re-runs the gate.

**Done when:** tests are green, the reviewer has no BLOCKING items, the note is updated, and the commit is made.
