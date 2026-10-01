# Dependency Graph, Phase Design, Atomic Tasks, Verification

## Contents
1. Dependency graph
2. Phase design
3. Adaptive profiles
4. Phase spec required sections
5. Atomic task rules & format
6. Sizing for agent context
7. Parallelism
8. Checkpoints
9. Verification menu
10. Task status vocabulary

## 1. Dependency graph

For every major task record: prerequisites (must finish first), blocking dependencies (hard), optional dependencies (nice to have first), parallelizable siblings, and whether it is on the critical path. Express it in TASKS.md via `Dependencies:` (parsed) and draw the overall graph in ARCHITECTURE.md/ROADMAP.md.

```text
Architecture contract ─┬─> Database schema ──> Backend API ──┐
                       ├─> Frontend shell ───────────────────┼─> UI integration ─> E2E
                       └─> API client types ─────────────────┘
```

Rules: no cycles; no task depends on a later phase; depend on the *specific* task that produces what you need, not on "the whole previous phase"; if a dependency is only on an interface, depend on the contract task, not the implementation.

## 2. Phase design

A phase is a **coherent, testable increment** with a checkpoint that proves it. Cut by what can be demonstrated, not by layer or task count. Test each boundary: "After this phase, what can I run/observe that I could not before?" If the answer is "nothing", merge it with its neighbor.

Prefer **vertical slices** after the foundation (one feature end-to-end) over completing all backend then all frontend, unless the contract-first parallel pattern makes layering safe. A walking skeleton (thin end-to-end path) early surfaces integration risk cheaply.

Typical order (use only what applies): Discovery & Architecture → Foundation → Core Infrastructure → Core Functionality → Feature Modules → UI/UX Integration → Integration → Testing & Hardening → Deployment.

## 3. Adaptive profiles

| Scale | Shape | Docs |
|---|---|---|
| Small | Foundation → Core → Testing → Release (3–4 phases, ≤ ~20 tasks) | Merge RISKS/DECISIONS into short sections; still keep requirement IDs and checkpoints |
| Medium | Discovery → Foundation → Core → Features → Integration → Hardening → Release (5–7) | Full `.planning/` set |
| Large | Discovery → Architecture → Infrastructure → Backend → Frontend → Integrations → AI/ML → Testing → Security → Deployment (8+), parallel tracks | Full set + per-track notes; consider splitting phase TASKS into waves |

Pick from dependencies and complexity, not from the table. If the plan exceeds what one executor session can hold per phase, split the phase.

## 4. Phase spec required sections

Each `SPEC.md` contains (headings are checked by the validator): **Objective**, **Why this phase exists**, **Entry criteria**, **Dependencies**, **Deliverables**, **Acceptance criteria**, **Verification**, **Checkpoint**, **Exit criteria**, **Risks**, **Rollback / Recovery**. Plus a `**Status:**` line. See `assets/templates/phase-SPEC.md`.

- *Entry criteria* are checkable (previous checkpoint passed; env var present; decision DEC-004 resolved).
- *Checkpoint* lists exact commands and expected results.
- *Rollback* says how to get back to a known good state (git tag/branch, migration down, feature flag, backup) — particularly for DB migrations and deploys.

## 5. Atomic task rules & format

Every task has: ID, title, purpose, files/components, requirements, dependencies, implementation details, expected output, acceptance criteria, validation command, failure conditions (and verification ID). Use the block from `assets/templates/phase-TASKS.md` verbatim — the validator parses these field names.

Rules:
- IDs are `TASK-<phase>.<n>` (e.g. `TASK-2.3`); the phase number matches the directory.
- **Files / Components** name real paths. For existing files say `MODIFY src/x.ts` (VERIFIED); for new ones `CREATE src/y.ts`. Never reference a file you did not see unless marked CREATE.
- **Implementation details** state decisions the executor must follow (interfaces, algorithm choice, edge cases, conventions to mirror) without writing the code.
- **Validation command** is a real command from the repo (or one the plan's earlier task creates). If none is possible (pure visual check), write `MANUAL:` followed by exact steps and expected observation.
- **Failure conditions** say what means "stop, do not proceed" (test fails, schema mismatch, unexpected file diff).
- Each task is independently verifiable. If it can only be verified together with another task, merge them or add an intermediate check.

Good vs. bad: see SKILL.md Step 5.

## 6. Sizing for agent context

A task should be completable in one focused session: roughly **1–5 files touched, one concern, ≤ ~1–2 hours human equivalent**, with all needed context pointable by ID (REQ, CMP, API, ENT, DEC). If the executor would need to read half the repo to do it, add the needed facts to the task. If it touches 10+ files, split. Include "read first" file paths in implementation details.

## 7. Parallelism

Mark independent work with a shared `Parallel group:` label (e.g. `A`). Safe parallelism requires: disjoint files, a settled shared contract, and no shared mutable state (migrations, lockfiles, generated code are classic collision points — serialize them). State merge/ordering instructions where outputs touch the same module. Do not parallelize just to look fast; a serial plan that executes safely beats a parallel plan that conflicts.

## 8. Checkpoints

A checkpoint = objective evidence, e.g. "app starts (`<cmd>` exits 0 / health endpoint 200)", "build succeeds", "all unit tests pass (N ≥ baseline)", "migration applies and reverts on a clean DB", "E2E flow X passes", "no regression: baseline suite unchanged". The checkpoint also verifies the phase's acceptance criteria one by one. A phase is `COMPLETE` only if the checkpoint passed and its results are recorded in `HANDOFF.md`.

## 9. Verification menu

Choose what fits the tech; do not demand tests the stack cannot run.

| Layer | Examples |
|---|---|
| Static | typecheck, lint, formatter check, dependency audit, schema validation |
| Unit | pure logic, validators, reducers |
| Integration | service + DB, API handlers with real test DB/containers |
| API | contract tests against OpenAPI/schema, status codes, error bodies |
| DB | migration up/down on a clean DB, constraint checks, seed scripts |
| UI/component | component tests, accessibility checks, state coverage (loading/error/empty) |
| E2E | critical user flows (Playwright/Cypress equivalents already in the repo) |
| Perf | benchmark with explicit threshold from a REQ-NFR |
| Security | authz tests, input fuzz/negative tests, secret scan, dependency audit |
| AI/ML | eval set with metric threshold, determinism/seed policy, fallback behavior, latency/GPU budget |
| Manual | scripted steps + expected observation (only when automation is impractical) |

Name tests `TEST-<phase>.<task>-<letter>` (e.g. `TEST-2.3-A`) and list them in the task's `Verification:` field.

## 10. Status vocabulary

`NOT_STARTED`, `READY`, `IN_PROGRESS`, `BLOCKED`, `COMPLETE`, `FAILED`. `READY` = all dependencies complete and no unresolved decision. A task depending on an unresolved decision or incomplete task is `BLOCKED` or `NOT_STARTED`, never `READY`.
