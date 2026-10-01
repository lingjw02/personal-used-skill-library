# Discovery & Feature Inventory

Goal: know what exists, how to run it, and what to test, *before* testing. Discovery is observation of the running system first, source second.

## Contents
1. What to establish
2. Launch & access
3. Mapping the application
4. Feature inventory rules
5. Risk classes and priority
6. Discovery output

## 1. What to establish

Application type (web app, SPA, desktop, mobile emulator, CLI, API/service), entry point, how to launch it, available accounts/test credentials and roles, main pages, navigation structure, modules, major workflows, backend/API and database/storage dependencies, browser/OS requirements, and responsive/desktop/mobile behavior where applicable.

## 2. Launch & access

- Read README / docs / `package.json` scripts / `Makefile` / `docker-compose` / CI config for the launch command and URL. If given a URL, just open it.
- Start the app yourself only if the user asked or it is clearly local. Record the exact command and version/commit in the report.
- Confirm it is up through observation: the page renders, the health endpoint answers, the window opens. A launch that errors is a finding (or an environment problem — see `evidence-and-bugs.md`).
- Credentials: use only what the user/docs provide. Do not guess passwords, brute-force, or create accounts on production. Record *which role* each credential has, never the secret itself. Ask once (batched) for missing roles that matter (admin vs. regular user).
- Record environment details that explain behavior: browser + version, OS, viewport, locale, app version/commit, backend URL.

## 3. Mapping the application

Walk the UI the way a new user would, then systematically:
1. Capture the top-level navigation (menus, tabs, sidebars, command palette, footers, settings, user menu).
2. For each destination: note forms, tables, filters, search, buttons, dialogs, uploads/downloads, bulk actions, pagination, sort, empty states.
3. Follow links systematically with a visited-set; normalize URLs (strip ids/query noise) so repeated templates collapse into one entry with "N instances".
4. Look for hidden paths: role-dependent menu items, settings pages, import/export, help, error pages (404), keyboard shortcuts, context (right-click) menus.
5. For APIs/CLIs: list endpoints/commands from docs/OpenAPI/`--help`; verify each by calling it.
6. Check dependencies by observation: does it work with the backend down? (only if safe), with a slow network? (only in test envs).

Do not stop after the home page or after the first module.

## 4. Feature inventory rules

Add every distinct function to the tracker (`add-feature`, or `--csv` for bulk). One row = one user-visible function with a clear pass/fail ("Login with valid credentials", "Edit user email", "Filter orders by status"). Not "Users module".

Fields: `id` (F-001…), `module`, `page`, `function`, `priority` (Critical/High/Medium/Low), `risk` class, `--destructive` if it deletes/overwrites data or has real-world side effects (emails, payments, external calls), `--related` for features that depend on/are affected by it (used for cross-feature and regression checks).

Add new features as you discover them mid-test; the inventory is never "finished" until exploration is.

## 5. Risk classes and priority

`--risk` (this order drives `next`):
`auth-security` → `data-loss` → `core-business` → `crud` → `payments` → `navigation` → `forms` → `search-filter` → `error-handling` → `secondary` → `cosmetic`.

Priority = business impact if broken: **Critical** (cannot use product / security / data loss), **High** (core workflow degraded), **Medium** (secondary workflow), **Low** (cosmetic/rare).

Inventory a sensible number of rows: enough that each is separately verifiable, not so many that the run cannot cover them. If the app is huge, say so and inventory by module first, then expand the riskiest modules.

## 6. Discovery output

A populated tracker (`$T list`), a one-paragraph note of how to launch/access, the environment classification, and a list of things you could not discover (e.g. admin area without admin credentials → add features as `BLOCKED` with the reason, so they appear in Coverage Gaps).
