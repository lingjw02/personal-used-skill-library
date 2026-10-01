# Requirements
| ID | Requirement | Priority | Source | Verification |
|---|---|---|---|---|
| REQ-F-001 | A client can create a short link for a valid http(s) URL. | MUST | user | API test |
| REQ-F-002 | Visiting a short code redirects (302) to the original URL; unknown code returns 404. | MUST | user | API test |
| REQ-F-003 | Each redirect increments a click counter. | SHOULD | user | integration test |
| REQ-F-004 | Custom domains per user. | OUT_OF_SCOPE | user ("later") | — |
| REQ-SEC-001 | Reject non-http(s) schemes (e.g. javascript:) and malformed URLs. | MUST | derived: open-redirect/XSS risk | unit test |
| REQ-NFR-001 | Redirect p95 < 50 ms at 10k links. ASSUMPTION | SHOULD | assumed | perf test |
| REQ-TC-001 | Python 3.12 with SQLite storage. | MUST | user | static + app start |
