# Risks, Decisions, Unknowns

## Contents
1. Risk register
2. Decision log
3. Unknowns / Assumptions / User decisions

## 1. Risk register (`RISKS.md`)

Register risks before implementation. Classes: Technical, Architecture, Dependency, Security, Performance, Data, UX, Integration, AI/ML, Deployment, Scope. Include only risks that could realistically change the outcome — padding hides the important ones.

```markdown
### RISK-003 — <short name>                         Class: Integration
- Probability: Low | Medium | High     - Impact: Low | Medium | High
- Detection: how/when we would notice (a test, a checkpoint, a metric)
- Mitigation: what the plan does to reduce it (task IDs)
- Fallback: what we do if it happens anyway
- Affects: PHASE-02, TASK-2.4
```

Good risks are specific and checkable ("Provider X rate limit is 60 req/min — bulk import in TASK-3.2 may exceed it") not generic ("API might be slow"). Put a *de-risking task early* when a High-impact risk blocks a lot of downstream work (spike, prototype, contract test against the sandbox).

## 2. Decision log (`DECISIONS.md`)

One entry per important architectural/scope decision. The heading and `Status` line are parsed by the validator.

```markdown
## DEC-001 — Use existing Postgres via Prisma for new tables
**Status:** DECIDED            <!-- DECIDED | ASSUMED | REQUIRES USER DECISION | SUPERSEDED -->
- Decision:
- Reason: (evidence with paths/URLs)
- Alternatives: A, B
- Why alternatives were rejected:
- Impact: components/phases/tasks affected
```

Rules: if evidence cannot settle it, do not choose silently — `Status: REQUIRES USER DECISION`, include your recommendation and the cost of each option, and make dependent tasks `BLOCKED` (reference the DEC in the task's `Decisions:` field so the validator can catch mistakes). `ASSUMED` decisions are provisional: list what to re-check and when.

## 3. Unknowns / Assumptions / User decisions (in `DECISIONS.md`)

Keep three tables so the executor can see at a glance what is not yet solid:

```markdown
## Unknowns
| ID | Question | Why it matters | How to resolve | Blocks |
| UNK-001 | Max file size users upload? | Storage + timeout design | Ask user / check product docs | TASK-3.2 |

## Assumptions
| ID | Assumption | Basis | If false | Re-check at |
| ASM-001 | Single-region deploy is acceptable | No HA requirement given | Re-architect DB replication | PHASE-05 entry |

## User Decisions Required
| ID | Decision | Options | Recommendation | Blocks | Needed by |
| UDR-001 | Hosting provider | A, B, C | B (cost) | PHASE-06 | before PHASE-05 |
```

The final response to the user must surface every `UDR` that blocks early phases.
