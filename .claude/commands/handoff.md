---
description: End a session - externalize all state (PROGRESS, MEMORY, journal) and commit
---
Finalize the session so the next one can resume unaided. Do every step, in this order:

1. **PROGRESS.md**
   - Tick the checklist items that were completed. Update the phase statuses.
   - Rewrite **CURRENT TASK** in one or two lines.
   - Rewrite **NEXT STEP** as a handoff contract: the exact files and notes, the skill to follow,
     reference commits to reuse, known risks ("WATCH: …"), and the gate that must pass. Weak:
     "continue the parser". Strong: "Implement MissingVariable handling in
     src/sheetres/parser.py following skill implement-change; fixture tests/fixtures/260918_E4;
     WATCH trailing blank lines (MEMORY pitfall); gate: fast tier + reviewer."
   - Append one journal line: `- YYYY-MM-DD — [sessions/YYYY-MM-DD-NN](docs/sessions/YYYY-MM-DD-NN.md): <summary>`.
2. **MEMORY.md.** Add dated entries for anything learned this session that would be expensive to
   relearn: pitfalls (trap → symptom → workaround), decisions (link the ADR), and new "Do not"
   items. Keep the file under 200 lines; evict old entries into vault notes if needed.
3. **Vault.** Update the component and domain notes whose status or facts changed. If a decision
   was made, draft an ADR (Status: Proposed unless the human accepted it explicitly).
4. **Journal.** Create `docs/sessions/YYYY-MM-DD-NN.md` (NN = next free number for today) with these
   sections: Done, Broke/learned, Deferred, Commits. Keep it short and factual.
5. **Commit.** Stage the session's work and commit as `docs(handoff): <summary>`, or split it into
   atomic commits if the code changes aren't committed yet. The commit hook runs the fast tier.
   If it is red, report the failure in NEXT STEP instead of forcing it through.
6. Reply with the new NEXT STEP verbatim and the commit hash(es).

$ARGUMENTS
