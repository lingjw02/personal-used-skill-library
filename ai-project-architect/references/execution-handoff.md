# Execution Handoff, State, Phase Handoff Contract

The plan's value is realized only if a *different* agent, in a *different* session, can continue correctly. Design for cold starts: assume the executor knows nothing but the repository and `.planning/`.

## Contents
1. EXECUTION.md content
2. STATE.md
3. Phase handoff contract (HANDOFF.md)
4. Deviation handling
5. Agent pointers
6. Kickoff prompt

## 1. EXECUTION.md content

Instruct the executor to (the template contains this verbatim):

1. Read `ROADMAP.md`, `STATE.md`, then the current phase `SPEC.md` and `TASKS.md`.
2. Inspect the repository before modifying files; never assume a file exists.
3. Never overwrite unrelated functionality; keep diffs focused on the task's listed files.
4. Complete tasks in dependency order; start only `READY` tasks.
5. Run the task's validation command after each meaningful change.
6. Stop and report when a blocking problem appears (failed validation you cannot fix within the task, missing prerequisite, contradicted assumption).
7. Never silently skip a failed acceptance criterion; never weaken a test to make it pass.
8. Update `STATE.md` (and task status) after each task.
9. Record deviations (file touched outside plan, different approach, added dependency) in the phase `HANDOFF.md` and `DECISIONS.md`.
10. Never expand scope; ideas go to `STATE.md → Pending Decisions`.
11. At phase end, run the checkpoint, write `HANDOFF.md`, update ROADMAP status.
12. Treat `ASSUMPTION` and `UNKNOWN` as unconfirmed. Ask or stop when a task depends on one.

## 2. STATE.md

Short, current, and the first file any session reads. Sections (validator checks for them): `Current Phase`, `Current Task`, `Completed Tasks`, `Blocked Tasks`, `Recent Changes`, `Known Issues`, `Active Decisions`, `Pending Decisions`, `Test Status`, `Next Action`. `Next Action` must be a single unambiguous instruction naming a task ID. Keep history terse (last ~10 changes); detail lives in HANDOFF files.

Initial state when the plan is created: Current Phase = first phase, all tasks NOT_STARTED/READY, Next Action = "Begin TASK-x.y (first READY task) or resolve UDR-… if blocked".

## 3. Phase handoff contract (`phases/phase-NN-*/HANDOFF.md`)

Written by the executor at phase end (the planner leaves the template empty). Fixed fields so the next agent can machine-read it:

```text
PHASE STATUS:            COMPLETE | FAILED | BLOCKED
Completed tasks:         TASK-…
Modified files:          path (reason)
Created files:           path
Tests executed:          command → result
Tests passed / failed:   N / M (names of failures)
Known issues:            …
Architecture changes:    (and whether DECISIONS.md was updated)
Deviations from plan:    …
Remaining blockers:      …
Next phase prerequisites: …
```

## 4. Deviation handling

Small, behavior-preserving deviations (rename a helper, different internal function split) → note in HANDOFF. Anything that changes an interface, adds a dependency, touches an unplanned module, or alters requirements → stop, record a `DEC` with `REQUIRES USER DECISION` (or update the plan if the user approves), then continue. The plan is a contract; changes are explicit.

## 5. Agent pointers

If the repo has `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, or `.cursor/rules`, propose (don't force) adding one line: "Active plan: read `.planning/EXECUTION.md` and `.planning/STATE.md` before making changes." For tools without a rules file, the kickoff prompt covers it. Do not edit those files unless the user asked; list the suggested line in the final response.

## 6. Kickoff prompt (goes at the bottom of EXECUTION.md)

```text
You are the execution agent for this project. Read .planning/EXECUTION.md, then .planning/STATE.md.
Continue from "Next Action". Follow the execution rules exactly. Do not expand scope.
After every task: run its validation command and update STATE.md. Stop at any blocker.
```
