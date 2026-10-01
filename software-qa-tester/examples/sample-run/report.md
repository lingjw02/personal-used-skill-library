# QA Report - Acme Admin (EXAMPLE - fictional)

- **Environment:** staging   **Capability tier:** B   **Run started:** 2026-10-01T04:33:15   **Report generated:** 2026-10-01T04:33:30
- **Context:** Illustrative run; evidence files are placeholders, not real screenshots.

## Executive Summary

EXAMPLE (fictional) run. Tested Acme Admin in a staging environment using browser automation, as a regular user. 5 of 7 discovered features were executed (71%). Two defects are open: 1 Medium (BUG-002, fix claimed but not verified) and 1 High (BUG-001). Search fails for names with accents, which blocks a core workflow; double-submitting the Create form creates duplicates. Bulk delete (data-loss risk) was not tested pending permission, and the admin role was not available.

**Coverage (from tracker):** 5/7 features executed (71%). PASSED 3, FAILED 2, BLOCKED 1, SKIPPED 1.

**Open defects:** 1 High, 1 Medium.
**Critical blockers:** none recorded.
**Untested/blocked areas:** 2 feature(s) - see Coverage Gaps.
**Fix claimed, not verified:** BUG-002.

## Feature Coverage

| Feature | Tested | Result | Issues |
|---|---:|---|---|
| F-001 Auth / Login / Login | Yes | PASSED | - |
| F-002 Auth / Login / Logout ends session | Yes | PASSED | - |
| F-003 Users / List / Search users | Yes | FAILED | BUG-001 |
| F-004 Users / Detail / Edit user email | Yes | PASSED | - |
| F-005 Users / Create / Create user | Yes | FAILED | BUG-002 |
| F-006 Users / List / Bulk delete users | No | BLOCKED | - |
| F-007 Settings / Profile / Change theme | No | SKIPPED | - |

## Bug Report

| ID | Severity | Feature | Status | Reproduction |
|---|---|---|---|---|
| BUG-001 | High | F-003 | OPEN | 3/3 (Confirmed) |
| BUG-002 | Medium | F-005 | FIXED_PENDING_RETEST | 4/5 (Confirmed) |

## Detailed Findings

### BUG-001 - Search returns no rows for names with accents

- **Severity:** High   **Confidence:** Confirmed   **Kind:** functional   **Status:** OPEN
- **Affected features:** F-003
- **Problem:** Search returns no rows for names with accents
- **Preconditions:** Regular user; user 'José' exists
- **Steps:**
  1. Open Users > List
  2. Type 'José' in search, press Enter
- **Expected:** Row for José is listed
- **Actual:** 'No results' shown; 'Jose' (no accent) finds the row
- **Reproduction rate:** 3/3
- **Observed context (console/network/log):** GET /api/users?q=Jos%3F -> 200, body []
- **Evidence:** `evidence/F-003-accent-empty.txt`; `evidence/F-003-network.log`
- **Suspected area (HYPOTHESIS, not fact):** Search request encoding - basis: network log shows the accent sent as '?'
- **Recommended modification:** Encode the query as UTF-8 before building the request URL
- **Implementation area:** Users list search request builder (frontend)
- **Risk of the change:** Other callers of the same helper may rely on current encoding
- **Verification test:** Search 'José' returns the row; 'Jose' and 'jos' unchanged; add a regression test with an accented name

### BUG-002 - Double-click on Create user submits twice (duplicate user)

- **Severity:** Medium   **Confidence:** Confirmed   **Kind:** functional   **Status:** FIXED_PENDING_RETEST
- **Affected features:** F-005
- **Problem:** Double-click on Create user submits twice (duplicate user)
- **Steps:**
  1. Open Users > Create
  2. Fill valid data
  3. Double-click Save
- **Expected:** One user created
- **Actual:** Two identical users appear in the list
- **Reproduction rate:** 4/5
- **Evidence:** `evidence/F-005-save-twice.txt`; `evidence/F-005-list-dupes.txt`
- **Recommended modification:** Disable the Save button while the request is in flight and make creation idempotent server-side
- **Implementation area:** Create user form submit handler; POST /api/users
- **Risk of the change:** Other forms may share the handler; confirm they still submit once
- **Verification test:** Double-click Save creates exactly one user; Enter-key double press likewise
- _History 2026-10-01T04:33:16:_ claimed fixed (UNVERIFIED) dev: commit 4f2a9c (example)

## Observations (not defects)

- **NOTE-001** (feature-request, F-003): Would like CSV export from the Users list

## Coverage Gaps

| Feature | State | Reason / note |
|---|---|---|
| F-006 Bulk delete users | BLOCKED | destructive; staging shared with other teams - waiting for permission to delete only QA-created users |
| F-007 Change theme | SKIPPED | cosmetic; deprioritized behind untested data-loss feature |

## Recommended Development Order

_Engineering work ordered by risk (not a ranking of the product)._

1. **[core-workflow]** BUG-001 (High) - Search returns no rows for names with accents
2. **[core-workflow]** BUG-002 (Medium) - Double-click on Create user submits twice (duplicate user)
