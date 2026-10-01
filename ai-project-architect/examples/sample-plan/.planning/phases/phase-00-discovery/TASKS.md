# Tasks

### TASK-0.1 — Confirm toolchain
- **Purpose:** Confirm toolchain.
- **Files / Components:** none (inspection)
- **Requirements:** REQ-TC-001
- **Dependencies:** none
- **Implementation details:** Run `python3 --version`; confirm 3.12 available; record in PROJECT.md.
- **Expected output:** Toolchain recorded as VERIFIED.
- **Acceptance criteria:** Python 3.12 confirmed or UDR raised.
- **Validation command:** `python3 --version`
- **Failure conditions:** Python < 3.12 -> stop and raise a decision.
- **Verification:** TEST-0.1-A
- **Parallel group:** none
- **Decisions:** none
- **Status:** READY
