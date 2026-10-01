---
name: ai-project-architect
description: Turn a software/system idea, product requirement, rough spec, or existing repository into a complete, dependency-aware, phase-by-phase implementation plan (a `.planning/` blueprint) that another AI coding agent (Claude Code, Codex, Cursor, Antigravity, Gemini agents) can execute autonomously. This is a PLANNING skill - it never writes application code. Produces requirements with stable IDs, architecture, dependency graph, phased roadmap, atomic tasks with validation commands, risk register, decision log, unknowns, traceability matrix, STATE.md and handoff contracts. Use this skill whenever the user asks to plan, architect, scope, roadmap, break down, phase, decompose, or "spec out" a project or feature, wants an implementation plan or handoff for an AI agent, says "how should I build X", "plan this out before we code", "create a roadmap / PRD / task breakdown / .planning folder", or wants to resume or audit an existing plan - even if they never say "skill", "architect" or "phase".
---

# AI Project Architect & Phase Planner

Turn an idea, spec, or repository into a blueprint another AI agent can execute without rediscovering the project.

The pipeline is fixed:

**RESEARCH → UNDERSTAND → DEFINE → ARCHITECT → DECOMPOSE → SEQUENCE → VERIFY → HAND OFF**

Never jump from a vague idea to a task checklist. A checklist written before the system is understood is the main reason AI-built projects stall: the executor hits a missing prerequisite on task 14 and has no context to recover.

## Non-negotiables

1. **Planning only.** Do not implement the project, scaffold app code, or install dependencies. Contract sketches (type signatures, JSON/DB schemas, endpoint tables, config keys) are allowed because they are *specifications*; function bodies, components, and working logic are not.
2. **Never invent project facts.** If the repository or documentation can answer a question, inspect it instead of asking the user. If nothing can answer it, label it (see Evidence labels). Silent guessing is the failure this skill exists to prevent.
3. **Never fake verification.** Say "VERIFIED" only for things you actually opened, ran, or read (cite the path, command, or URL). Otherwise say what you did not check.
4. **No orphan work.** Every task traces to a requirement; every MUST requirement traces to a task and a verification.
5. **Smaller and executable beats large and impressive.** Every task, phase, and document must earn its place. Do not pad.
6. **Never silently change requirements or scope.** Scope changes go through the decision log.

## Evidence labels

Use these exact tokens anywhere a fact is not directly confirmed, so the executing agent cannot mistake a guess for a fact:

| Label | Meaning |
|---|---|
| `VERIFIED` | Confirmed by inspection/execution/official source. Always cite `(path)`, `(cmd)` or `(url)`. |
| `UNKNOWN` | Needed but cannot be determined from available evidence. |
| `ASSUMPTION` | Temporarily assumed so planning can proceed. State what breaks if false. |
| `REQUIRES USER DECISION` | A choice that materially changes architecture/scope/cost. Do not pick silently. |
| `REQUIRES RESEARCH` | Answerable from external docs; research before the dependent task starts (or now, if cheap). |

Executors must never treat `ASSUMPTION` as `VERIFIED`. Tasks that depend on an unresolved item must be `BLOCKED`, not `READY`.

## Step 0 — Orient (do this before anything else)

Decide three things; they set the depth and the output location.

**A. Environment**
- *Repo-aware agent* (can read files/run commands): inspect the repository, write files into `.planning/`.
- *Chat-only / no repo*: ask for what you need only if essential; produce the plan as files in `/mnt/user-data/outputs/.planning/` (or one consolidated Markdown if the user prefers) and present them.

**B. Project type**
- *Greenfield* (no code): Phase 0 is mostly requirements + research.
- *Existing codebase*: follow the **Existing Codebase Rule** below. Do not design a greenfield architecture.
- *Spec-only* (documents but no code): treat documents as the source of truth; flag contradictions.

**C. Scale** (drives phase count and document depth — see `references/phases-and-tasks.md` §Adaptive profiles)
- *Small* (≈ <2 weeks human work, one subsystem): 3–4 phases, merged documents allowed.
- *Medium*: 5–7 phases, full `.planning/` set.
- *Large* (multi-service, AI/ML, infra, compliance): 8+ phases, per-phase SPEC + TASKS, explicit parallel tracks.

If a planning convention already exists (`.planning/`, `docs/plans/`, `PLAN.md`, `TODO.md`, `CLAUDE.md`, `AGENTS.md`, `.cursor/rules`, `GEMINI.md`, issue templates), **read it and follow it** instead of imposing this layout. Map this skill's artifacts onto the existing convention and note the mapping in `PROJECT.md`.

## Workflow

Work through the steps in order. Read the referenced file when you reach the step — not before — to keep context lean.

### Step 1 — Discovery (Phase 0) → `references/discovery.md`
Inspect the repo (structure, framework, package manager, config, APIs, DB, auth, state, UI, tests, build, deploy, docs, agent instructions, TODOs). **Search for reusable code before proposing anything new.** Answer six questions: what exists, what is reusable, what must change, what must be created, what constraints already exist, what technical debt/risk exists. Research external dependencies from official sources and record references.

### Step 2 — Requirements → `references/requirements.md`
Extract Functional, Non-Functional, UX, and Technical-Constraint requirements; classify MUST / SHOULD / COULD / OUT OF SCOPE; assign stable IDs (`REQ-F-001`, `REQ-UI-001`, `REQ-DATA-001`, `REQ-SEC-001`, `REQ-NFR-001`, `REQ-TC-001`). Each requirement is testable and states how it will be verified.

### Step 3 — Architecture → `references/architecture.md`
Design the system before any task exists: components (ID, responsibility, inputs, outputs, dependencies, interfaces, data ownership, failure behavior, security), a diagram (Mermaid or ASCII), data models, API/event contracts, and a producer/consumer map. Design interfaces from their consumers' needs, not in isolation. Decide extend / refactor / replace / new for each affected existing component and justify every major change.

### Step 4 — Dependency graph & phase design → `references/phases-and-tasks.md`
Build the task dependency graph (prerequisites, blockers, optional deps, parallel work, critical path). Cut phases along *coherent, testable increments* — not by task count. Remove artificial serialization: if two tasks need only a shared contract, give them the contract and let them run in parallel.

### Step 5 — Atomic tasks
Every task is small enough for an agent to finish and verify in one focused session, names concrete files/components, references requirement IDs, lists dependencies, and has a runnable validation command. Use the exact task block in `assets/templates/phase-TASKS.md`; the validator parses it.

Bad: "Implement backend."
Good: "Create `src/api/auth/login.ts` implementing POST `/api/auth/login`; validate credentials with the existing auth service; return the schema in ARCHITECTURE §API-3; add integration tests for valid, invalid, and expired credentials."

### Step 6 — Verification & checkpoints
Pick verification appropriate to the technology (static analysis, unit, integration, API, DB, UI, E2E, performance, security, manual with an explicit script). Every phase ends in a checkpoint of *objective* evidence (build passes, migration applies, endpoint returns X). "Code is finished" is not a checkpoint. Build the traceability chain `REQ → TASK → TEST → PHASE CHECKPOINT`.

### Step 7 — Risks, decisions, unknowns → `references/risk-decisions-unknowns.md`
Register risks *before* implementation (do not exaggerate). Log decisions with alternatives and rejection reasons. Keep three explicit lists: Unknowns, Assumptions, User Decisions Required.

### Step 8 — Handoff & state → `references/execution-handoff.md`
Write the execution contract (`EXECUTION.md`), the persistent `STATE.md`, and the per-phase handoff format so work survives across sessions and across different agents.

### Step 9 — Quality gates → `references/quality-gates.md`
Run three audits (Factual, Logical, Execution-risk) and then the validator. **If any audit fails, revise the plan, then re-run all three.** Do not output a plan that fails.

```bash
python <skill-dir>/scripts/validate_plan.py .planning          # errors + warnings
python <skill-dir>/scripts/validate_plan.py .planning --report # + critical path & parallel levels
python <skill-dir>/scripts/validate_plan.py .planning --emit-matrix > matrix.md
```

The validator checks structure and logic (ID integrity, coverage, dependency cycles, forward dependencies, phase/status consistency, parallel-group safety, unresolved placeholders). It cannot check factual claims — Audit 1 is still your job. For small plans that merge documents, pass `--allow-missing RISKS,DECISIONS` — but keep the task, requirement, and phase formats intact, because those are what it parses.

`examples/sample-plan/.planning/` is a small, validator-clean plan (fictional project) showing the exact formats, including a `BLOCKED` task tied to a `REQUIRES USER DECISION`. Look at it when unsure how a file should read.

## Output layout

Scaffold with the helper (optional; you may also write files directly from `assets/templates/`):

```bash
python <skill-dir>/scripts/init_plan.py --root <project-root> --project "Name" \
  --phases "discovery,foundation,core,features,integration,hardening,release"
```

```text
.planning/
├── PROJECT.md        summary, scope, existing-codebase findings, references, plan conventions
├── REQUIREMENTS.md   requirement table with IDs, priority, verification + traceability matrix
├── ARCHITECTURE.md   components, diagram, data/API design, dependency graph
├── ROADMAP.md        phase roadmap with status, deps, deliverables, critical tasks, checkpoint
├── STATE.md          live project state (the resume point for any new session)
├── DECISIONS.md      decision log + unknowns + assumptions + user decisions required
├── RISKS.md          risk register
├── EXECUTION.md      instructions the executing agent must follow + kickoff prompt
└── phases/
    ├── phase-00-discovery/SPEC.md
    └── phase-NN-<name>/{SPEC.md, TASKS.md, HANDOFF.md (written by executor)}
```

Mapping to the 20 required plan sections: 1–2 → PROJECT; 3, 17 → REQUIREMENTS; 4–6 → ARCHITECTURE; 7–8 → ROADMAP + phase SPECs; 9–11 → TASKS + SPECs; 12 → RISKS; 13–16 → DECISIONS; 18–20 → EXECUTION + STATE + HANDOFF.

If the user wants a single document or is in chat only, still use these section boundaries as headings so the content maps 1:1 onto files later.

## Existing Codebase Rule

When the project already has code: do not create a greenfield architecture. First establish architecture, conventions, abstractions, reusable code, and technical debt (cite file paths). Then for each affected area choose **extend / refactor / replace / introduce new** and write the justification into `DECISIONS.md`. Match existing naming, test framework, directory conventions, and commands — the plan's validation commands must be the repo's real ones (read `package.json`, `Makefile`, `pyproject.toml`, CI config; do not guess `npm test`).

## Asking the user questions

Ask only when (a) the repo/docs cannot answer it and (b) the answer materially changes architecture, scope, cost, or security. Batch questions in one message, give your recommended default for each, and keep planning with the default labeled `ASSUMPTION` rather than stalling. If the user is unavailable or said "just go", proceed fully with labeled assumptions and a `User Decisions Required` list. Never ask for facts you could read from the repo.

## Final response to the user

Keep it short. Include: where the plan lives; phase list with one-line objectives; the critical path; the top risks; **the User Decisions Required that block execution**; audit/validator results (state honestly what was and was not verified); and the one-line kickoff for the executor (the prompt in `EXECUTION.md`). Do not paste the entire plan into chat when files exist.

## Anti-patterns (reject these in your own output)

- Phases defined by "10 tasks each" or by technology layer alone when the increments are not independently testable.
- Tasks like "set up the database" with no files, schema, or validation command.
- Validation commands that are placeholders ("run tests") or that the repo does not support.
- Rebuilding something the repo already has; proposing a framework migration "for cleanliness".
- Requirements that no task satisfies; tasks that satisfy no requirement.
- Hidden scope: features appearing in tasks that are not in REQUIREMENTS.
- Assumptions written as facts; versions or APIs stated from memory without checking.
- A plan so long the executor cannot hold one phase (SPEC + TASKS + referenced architecture sections) in context. Keep each phase self-contained and cross-reference by ID.
- Writing implementation code "as an example". Specify; do not build.
