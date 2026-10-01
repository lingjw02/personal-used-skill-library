# Final QA Report

`$T report` generates `qa-run/report.md` from tracker state, redacts secrets, and applies the structure below. Your job before running it: make the tracker complete and write the narrative.

## Before generating

1. `$T status` — resolve warnings (PASSED without evidence, FAILED without a live bug, unknown related IDs, fixes pending retest).
2. Every feature has a state; anything not tested is `BLOCKED`/`SKIPPED` **with a reason**, or still `DISCOVERED` (shown as untested).
3. Write `qa-run/summary.md` — the Executive Summary narrative (3–8 sentences, plain prose): what was tested and how (tier, environment), overall coverage, the major functional problems, critical blockers, and the most important untested areas. Numbers must match `$T status`.
4. `$T scan`, review screenshots by eye for secrets/personal data.
5. `$T report`.

## Structure produced

1. **Executive Summary** — narrative + computed coverage, open defects by severity, critical blockers, untested/blocked areas, unverified fix claims.
2. **Feature Coverage** — `| Feature | Tested | Result | Issues |`
3. **Bug Report** — `| ID | Severity | Feature | Status | Reproduction |`
4. **Detailed Findings** — per issue: problem, preconditions, steps, expected, actual, reproduction rate, evidence, severity, confidence, suspected area (labeled hypothesis, with basis), recommended modification, implementation area, risk, verification method, retest history.
5. **Observations (not defects)** — feature requests, UX suggestions, expected-behavior notes.
6. **Coverage Gaps** — everything not PASSED/FAILED with its reason.
7. **Recommended Development Order** — engineering work ordered by risk (data loss → blocking → core workflow → integration → error handling → secondary → cosmetic), then severity. This orders the *work*, not the product.

## Tone and content rules

- Read like a professional QA report: specific, neutral, evidence-backed. No hype, no apologies, no speculation presented as fact.
- Distinguish **Observed** from **Suspected** everywhere.
- Say what you did *not* do (tiers, roles, browsers, environments, data volumes).
- Never include credentials, tokens, session data, or personal data. Describe roles, not secrets.
- Do not rank the product ("quality score"); rank engineering work.
- Final chat response: short summary + path to `report.md` and `evidence/`; list the blocking decisions you need from the user (e.g., credentials for missing roles, permission for destructive tests).
