# Regression & Retesting

A bug is fixed only when the *running application* behaves correctly. A changed source file, a developer's note, or a merged PR is a claim, not a result.

## Flow

1. Developer says it is fixed → `$T mark-fixed BUG-001 --note "dev: commit abc123"`. Status becomes `FIXED_PENDING_RETEST`; the report lists it as "fix claimed, not verified".
2. Make sure you are testing the new build: confirm the app version/commit, restart or redeploy if needed, clear stale cache/session, and say how you confirmed it.
3. `$T regression BUG-001` prints the checklist (below). Add `--save` to keep it in the run dir.
4. Re-run the **original failing case** exactly as recorded (steps from the bug). Capture evidence.
   - Pass → `$T retest BUG-001 --result pass --note "re-ran steps 1-3 on build abc123" --evidence evidence/...`
   - Fail → `$T retest BUG-001 --result fail ...` (bug becomes `REOPENED`; say what differs now).
5. Work through the rest of the checklist, recording results per feature with `set` (PASSED needs evidence, FAILED needs a bug).
6. Regenerate the report; the history of the bug shows claim → retest.

## Regression checklist (what `regression` prints)

1. The original failing case.
2. Features directly affected (linked to the bug).
3. Neighboring features on the same page/module.
4. Dependent workflows (features declared `--related`).
5. Previously passing **Critical** functionality.

Add checks the tool cannot know: other callers of the same component/API, same bug pattern elsewhere (e.g., accent search broken in Users → check Orders search), data created before the fix (migrations), and refresh/restart persistence of the repaired behavior.

## Rules

- Never mark a feature PASSED while a linked bug is open; after `VERIFIED_FIXED`, re-set the feature with fresh evidence.
- If the fix introduces a new problem, record a **new** bug (link the cause in the note) rather than rewriting the old one.
- If you cannot retest (environment unavailable), leave `FIXED_PENDING_RETEST` and list it in Coverage Gaps. Do not upgrade it.
- Keep evidence from before and after the fix; both go in the report history.
