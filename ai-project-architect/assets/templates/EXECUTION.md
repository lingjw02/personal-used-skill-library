# Execution Instructions — {{PROJECT_NAME}}

You are the execution agent. This plan is a contract. Follow it exactly.

1. Read `ROADMAP.md`, then `STATE.md`, then the current phase `SPEC.md` and `TASKS.md`.
2. Inspect the repository before modifying anything. Never assume a file exists; `MODIFY` targets must exist, `CREATE` targets must not collide.
3. Never overwrite unrelated functionality. Keep diffs limited to the task's listed files/components.
4. Work in dependency order. Start only tasks whose dependencies are COMPLETE and whose status is READY.
5. After each meaningful change run the task's validation command.
6. Stop and report when you hit a blocking problem (unfixable failed validation, missing prerequisite, contradicted assumption, pending decision).
7. Never silently skip a failed acceptance criterion. Never weaken, delete, or skip a test to make it pass.
8. After each task update the task `Status` and `STATE.md`.
9. Record deviations (unplanned files, different approach, new dependency) in the phase `HANDOFF.md` and `DECISIONS.md`. Interface changes, new dependencies, or requirement changes require approval first.
10. Never expand scope. Park ideas under `STATE.md → Pending Decisions`.
11. Treat ASSUMPTION / UNKNOWN / REQUIRES USER DECISION as unconfirmed. Do not build on them; mark dependent tasks BLOCKED and ask.
12. At phase end: run every checkpoint command, write `HANDOFF.md` (template in the phase folder), set the phase status in SPEC.md and ROADMAP.md. A phase is COMPLETE only if its checkpoint passed.
13. Never write secrets into plan files or commits.

## Kickoff prompt
```text
You are the execution agent for this project. Read .planning/EXECUTION.md, then .planning/STATE.md.
Continue from "Next Action". Follow the execution rules exactly. Do not expand scope.
After every task: run its validation command and update STATE.md. Stop at any blocker.
```
