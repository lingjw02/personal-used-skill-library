# Safety, Test Data, Credentials

Read before the first interaction that writes, deletes, sends, or pays.

## Environment rules

| Env | Rule |
|---|---|
| `local` / `test` | Full testing allowed, including destructive actions on test data. Still record what you created so you can clean up. |
| `staging` | Testing allowed. Destructive actions on shared staging data only on records you created. Avoid real outbound side effects (real emails/SMS/payments) unless sandboxed. |
| `production` | Read-only exploration by default. No create/edit/delete/send/pay without explicit user confirmation *per action class*. Never modify production data. Prefer asking for a test environment. |
| `unknown` | Treated as production. Ask the user to classify it. |

The tracker enforces part of this: destructive features cannot move to TESTING in `production`/`unknown` without `--confirm-destructive "<who/when>"`. Only pass it after the user explicitly said yes in the conversation.

## Destructive & side-effect actions

Examples: delete/purge, overwrite, bulk edit, reset/migrate, logout-all, close account, send email/SMS/notification, submit payment/order, publish, webhook triggers, third-party calls. Mark these `--destructive`. Before running one, check: env permits it? Is it on data I created? Can it be undone? Is there a sandbox mode?

## Test data

- Create your own clearly-labeled records (`qa-test-<date>-<n>`), so cleanup and attribution are easy.
- Use obviously fake data; never real people's data. Do not paste real personal data into reports.
- Track what you created in `qa-run/created-data.md` (type, id/name, where) and offer cleanup or perform it if allowed.
- For uploads, use small harmless files; for oversize/invalid-type tests use generated files, never real documents.
- Avoid load/stress/fuzz volume beyond what the environment owner allows; no denial-of-service-style testing, no scanning third parties, no attempts to bypass authentication of systems you do not own. Security checks are limited to observable behavior in normal use (e.g., can a regular user open an admin URL? is a protected page reachable after logout?).

## Credentials & sensitive information

- Use only provided credentials; do not store them in files inside the run dir. Refer to them by role ("admin test account").
- Never include passwords, tokens, API keys, session cookies, or personal data in the report, tracker notes, or chat. The tracker redacts common patterns but is not a guarantee.
- Screenshots: avoid capturing password fields, tokens, or other users' personal data; crop or re-capture. Review images before sharing (the scanner cannot read them).
- Before delivering: `$T scan` (checks text files in the run dir). Fix findings, regenerate the report.

## When to stop and ask

Ask the user (batched, with your recommended default) when: the environment is unclear; a needed action is destructive or has external side effects; credentials for an important role are missing; the application behaves in a way that suggests real customer data is present; you suspect you caused unintended changes.
