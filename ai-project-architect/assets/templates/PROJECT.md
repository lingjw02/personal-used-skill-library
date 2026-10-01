# {{PROJECT_NAME}} — Project Plan

**Created:** {{DATE}}   **Plan version:** 1   **Planner:** AI Project Architect

## 1. Project Summary
{{One paragraph: what is being built, for whom, why. State the MVP ("first usable version") in one sentence.}}

**Project type:** {{greenfield | existing codebase | spec-only}}   **Scale:** {{small | medium | large}}
**Existing planning convention found:** {{none | path — and how this plan maps onto it}}

## 2. Scope
**MUST HAVE:** {{REQ IDs / short list}}
**SHOULD HAVE:** {{…}}
**COULD HAVE:** {{…}}
**OUT OF SCOPE (do not implement):** {{…}}

## 3. Existing State (Discovery)
{{Use the discovery report format from references/discovery.md. Label every fact VERIFIED (path/cmd) / UNKNOWN / ASSUMPTION.}}

## 4. External References
| ID | Topic | URL | Accessed | Established | Version |
|---|---|---|---|---|---|
| REF-01 | {{…}} | {{…}} | {{DATE}} | {{…}} | {{…}} |

## 5. Plan Audit
| Audit | Result | What was checked / not checked |
|---|---|---|
| 1 Factual | {{PASS/FAIL}} | {{…}} |
| 2 Logical | {{PASS/FAIL}} | validate_plan.py: {{result}} |
| 3 Execution risk | {{PASS/FAIL}} | {{…}} |

## 6. Plan Conventions
- IDs: `REQ-<TYPE>-NNN`, `CMP-NN`, `API-N`, `ENT-N`, `PHASE-NN`, `TASK-<phase>.<n>`, `TEST-<phase>.<task>-<letter>`, `DEC-NNN`, `RISK-NNN`, `UNK-/ASM-/UDR-NNN`.
- Status vocabulary: NOT_STARTED, READY, IN_PROGRESS, BLOCKED, COMPLETE, FAILED.
- Reading order for any agent: EXECUTION.md → STATE.md → ROADMAP.md → current phase SPEC.md + TASKS.md.
