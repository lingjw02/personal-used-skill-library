# Tasks — PHASE-{{PHASE_NUM_PADDED}} {{PHASE_NAME}}

<!-- Format is parsed by scripts/validate_plan.py. Keep the heading and bold field names exactly.
     Dependencies: comma-separated TASK IDs or `none`. Requirements: REQ IDs. Status: see vocabulary. -->

### TASK-{{PHASE_NUM}}.1 — {{Imperative title}}
- **Purpose:** {{why this task exists}}
- **Files / Components:** {{CREATE path | MODIFY path (VERIFIED) | CMP-…}}
- **Requirements:** {{REQ-F-001, REQ-SEC-001}}
- **Dependencies:** {{none | TASK-…}}
- **Implementation details:** {{Read first: paths. Decisions to follow: interfaces, edge cases, conventions to mirror. Cite API-/ENT-/CMP- IDs. No code.}}
- **Expected output:** {{files/behavior that exist after the task}}
- **Acceptance criteria:** {{observable pass/fail statements}}
- **Validation command:** `{{real command}}`   (or `MANUAL:` exact steps + expected observation)
- **Failure conditions:** {{when to stop and not proceed}}
- **Verification:** {{TEST-{{PHASE_NUM}}.1-A}}
- **Parallel group:** {{A | none}}
- **Decisions:** {{none | DEC-…}}
- **Status:** {{READY | NOT_STARTED | BLOCKED}}
