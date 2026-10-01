# Architecture, Data & Interfaces

Goal: define the system before defining tasks, so tasks have something concrete to build against.

## Contents
1. Component identification
2. Component spec template
3. Diagram
4. Data & interface analysis
5. Producer/consumer rule
6. Change strategy for existing code
7. Technology choices
8. Architecture section checklist

## 1. Component identification

Walk this list and include only what the project truly has/needs: frontend, backend, APIs, services, database, object/file storage, authentication/authorization, external integrations, AI/ML components (model, inference serving, prompts, evals, GPU/CPU budget, fallbacks), background workers, queues/schedulers, configuration/secrets, deployment/infra, monitoring/logging, testing layers. For small projects this may be 3–5 components; do not manufacture microservices.

## 2. Component spec template

```markdown
### CMP-03 — Auth Service            Status: EXISTS(extend) | NEW | MODIFY
- Responsibility: one sentence.
- Inputs: …            - Outputs: …
- Depends on: CMP-01, CMP-02
- Interfaces: API-3 (POST /api/auth/login), EVT-1
- Data ownership: owns `users`, `sessions`; others access via interface only.
- Failure behavior: what happens on dependency failure / bad input (fail closed? retry? degrade?).
- Security: trust boundary, secrets, authz checks, input validation.
- Existing code: src/auth/* (VERIFIED) — reuse/extend notes.
```

Every component has exactly one owner of each piece of data. Two components writing the same table is a design smell — record it as a risk or fix it.

## 3. Diagram

Include at least one diagram: Mermaid (`flowchart TD`/`sequenceDiagram`) when the output may be rendered, ASCII otherwise. Show component boundaries, data flow direction, external systems, and trust boundaries. Add a second diagram (sequence) for the most critical flow if it clarifies ordering.

## 4. Data & interface analysis

Capture, for everything significant:

- **Data models/entities** with fields, types, constraints, relationships, indexes if performance-relevant, and migration notes (existing DB: additive vs breaking).
- **API endpoints**: method + path, auth, request schema, response schema, error cases/codes, idempotency, pagination/rate limits.
- **Events / WebSockets / queues**: name, payload, producer, consumers, delivery guarantees, ordering.
- **File formats** and storage layout.
- **Auth flows**: login, refresh, logout, permissions model.
- **External services**: contract, limits, auth, failure modes, sandbox availability.

Give each an ID (`API-1`, `ENT-2`, `EVT-1`, `EXT-1`) so tasks cite them. Specs may include schema/signature sketches; they must not become implementation.

## 5. Producer/consumer rule

For each important data structure or interface fill:

| Interface | Producer | Consumer(s) | What consumers need | Contract owner |
|---|---|---|---|---|

Design from the consumer's needs (UI needs pagination + totals → the API returns them; worker needs idempotency key → the event carries it). Contract-first: a task that defines the contract (OpenAPI/types/schema doc) precedes producer and consumer tasks, which then run in parallel.

## 6. Change strategy for existing code

For every affected existing area choose one and justify (DEC entry for anything beyond *extend*):

- **Extend** — default. Add within existing abstractions.
- **Refactor** — only when the existing structure blocks the requirement; define the refactor boundary, keep behavior, add characterization tests first.
- **Replace** — only with documented failure of the existing component and a migration/rollback path.
- **Introduce new** — only when nothing reusable exists (cite the reuse search).

Never plan a framework/library migration as a side effect of a feature.

## 7. Technology choices

Choose from evidence: existing stack first; then official docs for capabilities/limits; then constraints (cost, hosting, hardware). Each non-obvious choice → DEC entry with alternatives. If two options are equally viable and the user's preference matters (cost, vendor, hosting), mark `REQUIRES USER DECISION`, recommend one, and plan so the decision only blocks the tasks that really depend on it.

## 8. Architecture checklist (before moving on)

- Every MUST requirement is served by ≥1 component.
- Every component has a responsibility, owner of data, failure behavior.
- Every interface has a producer and ≥1 consumer.
- Security boundaries and secret handling are explicit.
- Observability (logs/metrics/health) and config are placed somewhere.
- Test layers per component are identified.
- Existing code reuse is recorded with paths.
