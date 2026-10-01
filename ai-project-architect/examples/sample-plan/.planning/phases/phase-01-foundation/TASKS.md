# Tasks

### TASK-1.1 — Scaffold project and test runner
- **Purpose:** Scaffold project and test runner.
- **Files / Components:** CREATE pyproject.toml, CREATE tests/test_smoke.py
- **Requirements:** REQ-TC-001
- **Dependencies:** TASK-0.1
- **Implementation details:** Use a pytest-based layout; no app logic yet.
- **Expected output:** Project installs; smoke test runs.
- **Acceptance criteria:** pytest collects and passes 1 test.
- **Validation command:** `pytest -q`
- **Failure conditions:** pytest fails to collect.
- **Verification:** TEST-1.1-A
- **Parallel group:** none
- **Decisions:** none
- **Status:** NOT_STARTED

### TASK-1.2 — Create links table migration
- **Purpose:** Create links table migration.
- **Files / Components:** CREATE src/store/schema.sql, CREATE src/store/db.py (connection only)
- **Requirements:** REQ-F-001, REQ-F-002, REQ-F-003
- **Dependencies:** TASK-1.1
- **Implementation details:** Implement ENT-1 exactly as in ARCHITECTURE; schema applies idempotently.
- **Expected output:** Schema applies on empty DB.
- **Acceptance criteria:** Applying twice does not error; table has columns per ENT-1.
- **Validation command:** `pytest -q tests/test_schema.py`
- **Failure conditions:** Schema mismatch with ENT-1.
- **Verification:** TEST-1.2-A
- **Parallel group:** none
- **Decisions:** DEC-001
- **Status:** NOT_STARTED
