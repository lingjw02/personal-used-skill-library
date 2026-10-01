---
name: software-qa-tester
description: Operate and test a running software application like a human QA engineer - launching it, clicking through it, typing into it, and judging what it actually does - then report reproducible bugs with evidence, severity, confidence, developer fix recommendations, and regression retests. Uses whatever control is available (computer-use mouse/keyboard/screenshots, browser automation, terminal/CLI/HTTP) and states honestly what it could not test. Tracks feature coverage with a state tracker so nothing is claimed tested that was not. Use this skill whenever the user asks to test, QA, smoke-test, regression-test, exploratory-test, UAT, "click through", "try out", "find bugs in", or "verify the fix for" an app, website, web app, desktop app, CLI tool, or API - or asks "does X actually work" about something that can be run. Also use it to retest after a fix. Do NOT use it for writing unit tests, static code review, or fixing the code; those do not involve operating the running system.
---

# Software System QA Tester

Test the application the way a human QA engineer would: by using it, observing what it really does, and reporting what you can prove.

The method is fixed:

**OBSERVE → UNDERSTAND → TEST → VERIFY → REPRODUCE → DIAGNOSE → RECOMMEND → RETEST**

Reading source code can tell you where to look; it can never tell you whether something works. A feature is only "passed" when you saw it work in the running system.

## Non-negotiables

1. **Actual behavior over source assumptions.** Source may be read to find routes, launch commands, or (after a failure) to form a hypothesis. It is never evidence that something passes.
2. **Never fabricate.** No invented results, no "tested" claims for pages you did not exercise, no bugs without evidence, no "fixed" without a retest in the running app.
3. **Evidence for every claim.** A PASS needs an observation you can point to; a bug needs evidence files (screenshot/log/output) and a reproduction record.
4. **Observation ≠ hypothesis.** Write what you saw as fact and what you suspect as hypothesis, labeled. When unsure, mark the finding `Unconfirmed` rather than presenting speculation as fact.
5. **Report first, never rewrite.** Do not modify source code unless the user explicitly asks. Your product is findings and the smallest recommended change.
6. **Safe by default.** Prefer isolated/test environments and test data. No destructive action against production or an unknown environment without explicit user confirmation. Never modify production data.
7. **Secrets stay out of reports.** Use only credentials the user gave you, never paste them into reports, evidence notes, or chat; redact tokens and passwords in logs and screenshots you keep.
8. **Track coverage honestly.** Everything discovered gets a state; what was not tested is listed with the reason.

## Step 0 — Establish capability tier and environment

Find out what control you actually have before promising anything. State the tier in the report.

| Tier | You can | Typical coverage |
|---|---|---|
| **A — Full computer use** | Screenshots + mouse + keyboard + windows + terminal | Everything: visual state, drag/drop, dialogs, desktop apps, window resize |
| **B — Browser automation** | Drive a real browser (Chrome tool, Playwright/Puppeteer, MCP browser) + terminal | Web apps via real clicks/typing, console + network inspection; limited native dialogs/visual judgment |
| **C — Terminal only** | Shell: launch, CLI input, HTTP via curl, logs, headless scripts | CLI apps and APIs; web UIs only via scripted headless browser if one can be installed |
| **D — Cannot execute** | Nothing runs | **You cannot QA.** Offer a test plan and feature inventory only, and say clearly that no results exist |

If the application is not reachable from where you run (no network route, not installed, needs hardware you lack), say so and stop. Do not simulate results from the code.

Classify the environment: `production | staging | test | local | unknown`. **Treat `unknown` as production.** Ask the user (one batched question, with your default) if you cannot tell and it affects safety. Safety rules per environment are in `references/safety-and-data.md` — read it before the first interaction with anything that writes data.

## Run workspace and tracker

All state lives in a run directory (default `qa-run/`) managed by `scripts/qa_tracker.py`. Use it for every state change: it keeps an audit log and enforces the honesty rules (a PASS needs evidence, a FAILED feature needs a bug, a Confirmed bug needs evidence and repeat reproduction, a fix is not verified without a retest). Evidence (screenshots, logs, outputs) goes in `qa-run/evidence/`.

```bash
T="python <skill-dir>/scripts/qa_tracker.py --dir qa-run"
$T init --app "Acme Admin" --env staging --tier B
$T add-feature --id F-001 --module Auth --page Login --function "Login" --priority Critical --risk auth-security
$T next --n 5                       # what to test next (risk-ordered)
$T set F-001 TESTING
$T set F-001 PASSED --note "valid login lands on dashboard; session survives refresh" --evidence evidence/F-001-login-ok.png
$T add-bug --title "..." --features F-001 --severity High --confidence Confirmed ...   # see references/evidence-and-bugs.md
$T status | $T report | $T scan
```

Run `$T --help` and `$T <command> --help` for all options. `examples/sample-run/` shows a finished (fictional) run and report; `assets/summary-template.md` and `assets/created-data-template.md` are starting points for the narrative and the test-data log.

## Workflow

Read each referenced file when you reach its step, not before.

1. **Discover** → `references/discovery.md`. Find how to launch the app, entry points, accounts, navigation, modules, dependencies. Build the **Feature Inventory** in the tracker (ID, module, page, function, priority, risk class). Do not stop at the home page; follow navigation systematically and keep a visited-set.
2. **Plan by risk.** Auth/security → data loss → core business → CRUD → payments/transactions → navigation → forms → search/filter → error handling → secondary → cosmetic. `$T next` orders by this. Do not spend the session on cosmetics while core features are untested.
3. **Test each feature** with real interaction → `references/test-techniques.md`. For every feature: happy path, invalid input, boundaries, interaction errors, state persistence, cross-feature effects — as relevant to that feature. Prefer realistic *sequences* (open → enter → submit → observe loading → verify result → refresh → verify persistence), not single clicks.
4. **When something looks wrong** → `references/evidence-and-bugs.md`. Do not assume the cause. Capture the exact action, message, screenshot, page, state, console/network/log output; repeat the action; rule out environment, test-data, and timing causes; classify (defect vs. feature request vs. UX vs. expected behavior); then record the bug.
5. **Report** → `$T report` generates the structured report from tracker state (coverage numbers come from the tracker, not from memory). Write the executive-summary narrative into `qa-run/summary.md` first so it appears in the report. Template and rules: `references/report.md`.
6. **Retest after fixes** → `references/retest.md`. A bug is fixed only after the original failing case *and* related/dependent/critical functionality are re-tested in the running app.

## Per-feature loop (the core habit)

```
pick next feature → set TESTING → perform sequence → observe (screenshot/log after each significant step)
→ verify result independently (does it persist? appear elsewhere? survive refresh/restart?)
→ PASSED (with evidence) | FAILED (with bug) | UNCONFIRMED | BLOCKED (reason) | SKIPPED (reason)
```

Verify results through a second channel whenever possible (list view after create, reload after save, API/DB read after UI action). A success toast alone is not proof that data was saved.

## Exploration without loops

- Keep a visited-set keyed by normalized URL/route or screen signature; ids and query noise in URLs do not make a new page.
- For repeated templates (detail pages, list rows) test 2–3 representative instances plus edge instances (empty, longest, special characters), not all of them.
- Avoid dangerous links during exploration: logout, delete/purge, payment confirm, send email/SMS, external sites. Test them deliberately, last, under the safety rules.
- Stop a branch when it repeats; record the cap and why. Never claim "every page tested" unless the tracker says so.
- If you hit a wall (blocked by login, missing data, crash), mark `BLOCKED` with the reason and move on.

## Final response to the user

Keep it short and honest: capability tier and environment; coverage numbers from the tracker; bug count by severity; the critical blockers; what was **not** tested and why; where the report and evidence are; the engineering order (by risk). Never paste secrets. Do not claim anything the tracker does not support.

## Anti-patterns (reject in your own work)

- Marking a feature passed because the code looks right, or because the page loaded.
- Testing only the happy path, only the home page, or only what is easy.
- Reporting a "bug" from a single unrepeated observation as Confirmed.
- Naming a source-code cause without evidence.
- Blaming the app for environment problems (stale session, dirty test data, network flake) without ruling them out.
- Recommending large rewrites; recommend the smallest change that fixes the confirmed problem.
- Deleting/overwriting real data "to see what happens".
- Declaring a bug fixed because the diff looks right.
