---
description: Start a session - restore working state from the memory layer and state the plan
---
Restore the working state before doing anything else:

1. Read `MEMORY.md` and `PROGRESS.md` in full.
2. Read the newest one or two notes in `docs/sessions/` (sort by filename).
3. Run `git status` and `git log --oneline -10`. Flag uncommitted changes or commits that
   PROGRESS.md does not mention. These mean the previous session ended without `/handoff`.
4. If NEXT STEP names vault notes, skills or ADRs, read them now. Read nothing else yet.
5. Reply with at most ~12 lines:
   - **Where we are:** phase and CURRENT TASK, in one or two lines.
   - **Plan for this session:** the concrete steps from NEXT STEP, with the gate that must pass.
   - **Blockers / questions for the human:** anything marked blocked, or any Proposed ADR that
     the plan depends on.
   - **Inconsistencies:** anything from step 3.

Then wait for the go-ahead if there are blockers. Otherwise start on the first step.

$ARGUMENTS
