# Requirements & Scope

Goal: convert the idea into explicit, testable, ID'd requirements with a controlled scope. The roadmap is built from this file; anything missing here will not be built, anything extra here will be built — so be deliberate.

## Contents
1. Extraction categories
2. Writing a good requirement
3. ID scheme
4. Scope classes (MoSCoW)
5. Table format (parsed by the validator)
6. Scope-creep control
7. Traceability matrix

## 1. Extraction categories

- **Functional (F)** — what the system does. Observable behavior, per actor/flow.
- **Non-functional (NFR)** — performance (with numbers), security, reliability, scalability, accessibility, maintainability, compatibility, privacy, offline support, resource limits.
- **UX (UI)** — navigation, user flows, feedback, loading / error / empty states, responsive behavior, interaction behavior.
- **Data (DATA)** — entities, retention, migration, integrity rules.
- **Security (SEC)** — authn/authz, secrets, input validation, auditability.
- **Technical constraints (TC)** — mandated framework/DB/library, GPU/RAM limits, API quotas, hosting, OS, budget, licensing.
- **Integration (INT)** — external systems and their contracts.

Mine the user's text, attached docs, and the repository. Quote the source in the `Source` column (`user`, `README §x`, `src/…`) so the origin is auditable. Where the user's statement is vague ("fast", "secure", "nice UI"), do not invent a number silently: propose a measurable target labeled `ASSUMPTION` and add it to the user-decision list if it affects cost/architecture.

## 2. Writing a good requirement

- One behavior per requirement; "shall"-style statement.
- Testable: a stranger could write a pass/fail check from it.
- States the *what*, not the *how* (the how belongs in architecture).
- Has a stated verification method (unit / integration / API / DB / UI / E2E / manual / perf / security / static).

Weak: "The app should be fast."
Strong: "REQ-NFR-001: The search endpoint returns p95 < 300 ms for 10k-record datasets on the target hosting tier. (perf test)" — if 300 ms was not given by the user, mark it `ASSUMPTION`.

## 3. ID scheme

`REQ-<TYPE>-<NNN>`, `NNN` zero-padded, never reused or renumbered after the plan is published. Types: `F`, `NFR`, `UI`, `DATA`, `SEC`, `TC`, `INT`. If a requirement is dropped, keep the row and mark it `OUT_OF_SCOPE` or `DROPPED` with the reason — stable IDs keep old handoffs valid.

## 4. Scope classes

- **MUST** — system doesn't function / isn't acceptable without it. Needs tasks in the plan.
- **SHOULD** — important, not needed for the first usable version. Scheduled in later phases or flagged as deferred.
- **COULD** — optional improvements. Listed, not scheduled unless trivial.
- **OUT_OF_SCOPE** — explicitly excluded. Executor must not build it. Record why (user said so / cost / later release).

Define "first usable version" (MVP) in one sentence in PROJECT.md; MUST = what that sentence needs.

## 5. Table format

The validator reads rows beginning with `| REQ-`. Keep exactly these columns:

```markdown
| ID | Requirement | Priority | Source | Verification |
|---|---|---|---|---|
| REQ-F-001 | Users can sign in with email + password. | MUST | user | API test + E2E |
| REQ-NFR-001 | Search p95 < 300 ms at 10k records. ASSUMPTION | SHOULD | assumed | perf test |
| REQ-F-014 | Social login. | OUT_OF_SCOPE | user ("later") | — |
```

`Priority` ∈ `MUST | SHOULD | COULD | OUT_OF_SCOPE | DROPPED`.

## 6. Scope-creep control

- A task may only reference requirements that are not OUT_OF_SCOPE/DROPPED (the validator enforces it).
- If, while decomposing, you discover necessary work with no requirement (e.g. CI, logging, migrations), either add a derived requirement (`REQ-TC-…`/`REQ-NFR-…`, Source = `derived: <why>`) or fold it into the task that needs it with the reason stated. Never leave it implicit.
- New ideas from you (not the user) go in as COULD or in DECISIONS as proposals, not as MUST.

## 7. Traceability matrix

`REQ → TASK → TEST → PHASE CHECKPOINT`. Generate with `validate_plan.py --emit-matrix` and paste into REQUIREMENTS.md under `## Traceability Matrix` (regenerate after any plan change). A MUST requirement with an empty cell in any column is a plan defect.
