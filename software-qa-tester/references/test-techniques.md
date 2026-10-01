# Test Techniques

How to exercise a feature. Apply what is relevant to each feature; not every technique fits every control. Always use the application's real interface, as a user would.

## Contents
1. Human-like interaction
2. Sequences, not single clicks
3. Coverage categories (the six passes)
4. Control-type checklists
5. Per-environment notes (web, desktop, CLI, API)
6. Observing results
7. Avoiding false results

## 1. Human-like interaction

Use what a person uses: mouse move/click (left, right, double), drag and drop, scroll, typing, Tab/Shift+Tab, Enter, Escape, arrow keys, Ctrl/Cmd shortcuts, browser back/forward/refresh, window resize, app restart. Wait for the UI to settle before judging (spinners, transitions). Type like a user (real key events), not by injecting values into the DOM, unless the control forces it — and note when you had to.

## 2. Sequences, not single clicks

Weak: click Submit. Strong: open page → enter valid data → submit → observe loading → observe response/message → verify resulting state in the UI → refresh → verify persistence → check where else the data should appear.

Screenshot (or capture output) at each significant step: before submit, during loading, after result, after refresh.

## 3. The six passes

**Happy path** — valid input, expected workflow, each role that should have access.

**Invalid input** — empty required fields; wrong format (email, phone, date); invalid characters (quotes, `<>`, emoji, RTL, leading/trailing spaces, `%`, `\`); extremely long input; duplicates of unique values; missing required fields; invalid file types; oversized files. Check: is it rejected or accepted *correctly*, is the message clear and next to the field, is entered data preserved, can the user recover.

**Boundaries** — minimum/maximum, zero, negative where relevant, exactly-at-limit and one-over, empty dataset, single item, very large dataset, long text in lists/tables (wrapping/overflow), many items at once, date edges (leap day, timezone, month end), pagination edges (last page, page beyond range).

**Interaction errors** — double-click submit; repeated submission; rapid navigation; clicking while loading; closing a dialog mid-operation; back/forward during a flow; refresh during an operation; open the same record in two tabs/windows and edit both; session expiry mid-form (only where safe).

**State management** — after refresh; logout/login; navigating away and back; browser back/forward; app restart; close and reopen; deep-link to a page directly; multiple tabs; different role; returning after idle. What is preserved, what should be, what leaked from a previous user/session.

**Cross-feature** — chains such as create → edit → search → filter → sort → export → delete → verify it disappears *everywhere* (lists, counts, dashboards, search, related records, exports). Use the tracker's `--related` links to pick chains. Check that changing A did not break B.

## 4. Control-type checklists

- **Buttons/links:** enabled/disabled logic, hover/focus state, keyboard activation (Enter/Space), double-click protection, goes where its label says.
- **Forms:** tab order, required markers, inline vs. submit-time validation, submit with Enter, reset/cancel behavior, unsaved-changes warning, autofill, paste, character counters, preserved values after error.
- **Dialogs/modals:** open/close via X, Escape, outside-click, focus trapped and returned, scroll behavior, stacked dialogs, confirm vs. cancel actually does what it says.
- **Menus/tabs/navigation:** current-location indicator, deep links, back-button behavior, breadcrumbs, role-based items, keyboard/arrow navigation.
- **Tables/lists:** sort (asc/desc/stable), pagination, page size, select-all/bulk, empty state, loading state, long content, column resize/hide, row actions.
- **Search/filter:** exact, partial, case, accents, special characters, empty query, no results message, combine filters, clear filters, persistence after navigation, result counts matching rows.
- **CRUD:** create (valid/invalid/duplicate), read (list vs. detail consistent), update (partial, concurrent), delete (confirmation, cascade, undo, disappears everywhere).
- **Uploads/downloads:** valid/invalid type, size limits, zero-byte, name with spaces/unicode, duplicate names, progress/cancel, downloaded file opens and content is correct.
- **Authentication:** valid/invalid login, lockout messaging, logout truly ends access (back button, direct URL), session persistence/expiry, password reset flow, role boundaries (user cannot reach admin pages/actions), protected pages when logged out.
- **Settings/preferences:** change → save → reload → still applied → affects the behavior it claims to.
- **Loading/empty/error states:** each exists, is understandable, and offers recovery (retry, back, contact).
- **Responsive/visual (tier A/B):** resize to narrow/wide, zoom, scroll, overflow, overlapping, truncated text, focus visibility. Judge usability, report only what you can show in a screenshot.
- **Accessibility basics:** keyboard-only completion of the main flow, visible focus, labels on inputs, contrast obviously failing, images with meaning lacking text alternatives (report as Low/Medium unless it blocks use).

## 5. Per-environment notes

**Web (tier A/B):** open DevTools console and network when available; record console errors/warnings and failing/slow requests (status, endpoint) alongside the UI symptom. Test in at least the primary browser; mention browser/version. Check refresh and deep-link behavior of SPA routes. Test at one narrow and one wide viewport if the app claims to be responsive.

**Desktop apps (tier A):** window controls (minimize/maximize/resize), multi-window, system dialogs (open/save), clipboard, drag-drop from the OS, shortcuts, tray/menu bar, close-and-relaunch persistence, behavior when files/permissions are missing.

**CLI (tier C):** `--help` accuracy, exit codes (0 on success, non-zero on error), stdout vs. stderr, invalid flags/args, missing files, empty input, huge input, piping, idempotency on re-run, interrupted run (Ctrl+C) leaving clean state.

**API/service (tier C):** each documented endpoint with valid/invalid/missing auth; status codes and error bodies; schema conformity; pagination; idempotency; concurrent requests where safe; consistency between API and UI. Use curl/httpie with test credentials; keep secrets out of saved commands.

## 6. Observing results

Judge against an explicit expectation written *before* you act: from the UI text/labels, docs, spec, industry convention, or the app's own consistent behavior elsewhere. State the source of the expectation when you report. Then verify through more than one channel: UI → refresh → other screen → API/log/DB read (if available).

## 7. Avoiding false results

- Re-run before concluding: a one-off may be timing, stale session, or dirty data. Retry from a clean state (fresh login, fresh record) to separate causes.
- Check preconditions: right role? right data? right feature flag? same behavior in a clean session/incognito?
- Note flaky behavior as such (e.g. `2/5`) rather than rounding up to "broken" or down to "fine".
- Do not count your own mistakes (wrong field, typo) as defects; redo the step carefully.
- A feature that works only in the happy path is `PASSED` only for what you tested; say which passes you covered in the note.
