# Quality Gates — three audits + validator

Run all three audits on the finished plan. If any item fails, fix the plan, then re-run **all** audits (a fix in one place often breaks another). Record the result in `PROJECT.md §Plan Audit` — state what was and was not verified; never claim a check you did not perform.

## Audit 1 — FACTUAL
- Every repository fact cites a path/command and was actually inspected (VERIFIED) — or is labeled UNKNOWN/ASSUMPTION.
- Technology names/versions match manifests or official docs, not memory.
- Files named in `MODIFY` actually exist; files named in `CREATE` do not collide with existing ones.
- Validation commands exist in the repo (script names, targets) or are created by an earlier task.
- External references are official/primary and recorded with URLs and dates.
- Requirements match what the user said (re-read the request; nothing silently added/dropped).

## Audit 2 — LOGICAL
- Run `validate_plan.py`: no errors (IDs unique, refs resolve, no cycles, no forward-phase deps, statuses consistent).
- Every MUST requirement → ≥1 task → ≥1 verification → a phase checkpoint.
- Architecture serves every MUST; every interface has producer + consumer; data has one owner.
- Order is correct: contracts before consumers, schema before queries, auth before protected routes, migrations before code that needs them.
- No contradictions between ARCHITECTURE, REQUIREMENTS, task details, decisions.
- Phase boundaries each deliver something observable.

## Audit 3 — EXECUTION RISK
- Missing prerequisites (env vars, accounts, API keys, installed tools, test data, hardware) listed in entry criteria.
- Tasks realistic for one session; none vague ("implement X"), none touching unbounded numbers of files.
- Hidden assumptions surfaced; `BLOCKED` tasks tied to a pending decision.
- Every task and checkpoint has validation; checkpoints are objective.
- Scope creep: nothing in tasks that is not traceable to a non-OUT_OF_SCOPE requirement.
- Security: authn/authz, secrets, input validation, dependency risk addressed where relevant; no secrets in plan files.
- Rollback exists for destructive/irreversible steps (migrations, data changes, deploys).
- Agent limits: each phase fits in context (SPEC + TASKS + referenced IDs); cross-references by ID; read-first lists present.
- Parallel groups touch disjoint files.

## Validator

```bash
python scripts/validate_plan.py .planning [--report] [--emit-matrix] [--json] [--strict]
```
Exit code 0 = no errors (warnings allowed unless `--strict`), 1 = errors. Treat warnings as items to either fix or consciously justify in the plan.
