# Decisions
## DEC-001 — SQLite as the store
**Status:** ASSUMED
- Decision: SQLite via stdlib sqlite3.
- Reason: REQ-TC-001 names SQLite.
- Alternatives: Postgres. Rejected: no multi-writer requirement given.
- Impact: CMP-02.
## DEC-002 — Click analytics retention
**Status:** REQUIRES USER DECISION
- Decision: how long to keep per-click records vs. only a counter.
- Reason: privacy/cost trade-off not specified.
- Alternatives: counter only (recommended); per-click log.
- Impact: TASK-2.4.
## User Decisions Required
| ID | Decision | Options | Recommendation | Blocks | Needed by |
|---|---|---|---|---|---|
| UDR-001 | Click retention | counter / log | counter | TASK-2.4 | PHASE-02 |
