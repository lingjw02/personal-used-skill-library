# Architecture
```text
Client -> API (CMP-01) -> Link Store (CMP-02, SQLite)
```
### CMP-01 — API   Status: NEW
- Responsibility: HTTP endpoints for create + redirect. Depends on CMP-02, CMP-03.
### CMP-02 — Link Store   Status: NEW
- Responsibility: owns table `links` (ENT-1: code PK, url, created_at, clicks).
### CMP-03 — URL Validator   Status: NEW
- Responsibility: pure function validating URLs (REQ-SEC-001).
### API-1 — POST /links   (body {url}, 201 {code}, 422 invalid)
### API-2 — GET /{code}   (302 Location, 404 unknown)
