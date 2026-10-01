# Tasks

### TASK-2.1 — URL validator
- **Purpose:** URL validator.
- **Files / Components:** CREATE src/validate.py, CREATE tests/test_validate.py
- **Requirements:** REQ-SEC-001
- **Dependencies:** TASK-1.1
- **Implementation details:** Pure function; accept http/https only; reject others.
- **Expected output:** validate_url(url)->bool.
- **Acceptance criteria:** javascript:, data:, empty, malformed rejected; https accepted.
- **Validation command:** `pytest -q tests/test_validate.py`
- **Failure conditions:** Any non-http scheme accepted.
- **Verification:** TEST-2.1-A
- **Parallel group:** A
- **Decisions:** none
- **Status:** NOT_STARTED

### TASK-2.2 — POST /links endpoint
- **Purpose:** POST /links endpoint.
- **Files / Components:** CREATE src/api/create.py, CREATE tests/test_create.py
- **Requirements:** REQ-F-001, REQ-SEC-001
- **Dependencies:** TASK-1.2, TASK-2.1
- **Implementation details:** Implements API-1; uses validator; returns 201 {code}, 422 on invalid.
- **Expected output:** Endpoint works.
- **Acceptance criteria:** valid -> 201; invalid -> 422.
- **Validation command:** `pytest -q tests/test_create.py`
- **Failure conditions:** Invalid URL stored.
- **Verification:** TEST-2.2-A
- **Parallel group:** none
- **Decisions:** none
- **Status:** NOT_STARTED

### TASK-2.3 — GET /{code} redirect
- **Purpose:** GET /{code} redirect.
- **Files / Components:** CREATE src/api/redirect.py, CREATE tests/test_redirect.py
- **Requirements:** REQ-F-002
- **Dependencies:** TASK-1.2
- **Implementation details:** Implements API-2; 302 or 404.
- **Expected output:** Redirect works.
- **Acceptance criteria:** known -> 302 Location; unknown -> 404.
- **Validation command:** `pytest -q tests/test_redirect.py`
- **Failure conditions:** Wrong status code.
- **Verification:** TEST-2.3-A
- **Parallel group:** A
- **Decisions:** none
- **Status:** NOT_STARTED

### TASK-2.4 — Count clicks on redirect
- **Purpose:** Count clicks on redirect.
- **Files / Components:** MODIFY src/api/redirect.py (after TASK-2.3)
- **Requirements:** REQ-F-003
- **Dependencies:** TASK-2.3
- **Implementation details:** Counter only unless DEC-002 resolves otherwise.
- **Expected output:** clicks increments.
- **Acceptance criteria:** Two visits -> clicks == 2.
- **Validation command:** `pytest -q tests/test_clicks.py`
- **Failure conditions:** Counter not persisted.
- **Verification:** TEST-2.4-A
- **Parallel group:** none
- **Decisions:** DEC-002
- **Status:** BLOCKED

### TASK-2.5 — Redirect latency check
- **Purpose:** Redirect latency check.
- **Files / Components:** CREATE tests/perf/test_redirect_latency.py
- **Requirements:** REQ-NFR-001
- **Dependencies:** TASK-2.3
- **Implementation details:** Seed 10k links; measure p95.
- **Expected output:** Perf test exists.
- **Acceptance criteria:** p95 < 50 ms on dev machine (ASSUMPTION threshold).
- **Validation command:** `pytest -q tests/perf`
- **Failure conditions:** p95 above threshold -> report, do not tune silently.
- **Verification:** TEST-2.5-A
- **Parallel group:** none
- **Decisions:** none
- **Status:** NOT_STARTED
