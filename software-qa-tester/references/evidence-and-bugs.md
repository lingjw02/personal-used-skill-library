# Evidence, Classification, Bug Records, Developer Recommendations

## Contents
1. Capturing evidence
2. Is it a defect? (classification)
3. Severity and confidence
4. Reproduction
5. Recording the bug
6. Diagnosis (hypotheses vs facts)
7. Developer recommendations

## 1. Capturing evidence

When something unexpected happens, before touching anything else, capture: the **exact action** that caused it, the **visible error message** (verbatim), a **screenshot**, the **current page/screen/route**, the **application state** (logged-in role, data involved), **console errors** (web), **network/API errors** (status, endpoint, response body summary), and **terminal/log output**. Save files in `qa-run/evidence/` with descriptive names (`F-003-search-accent-empty.png`, `F-003-console.log`). Keep excerpts short; redact secrets.

Capture the *before* and *after* of state changes, not just the failure.

## 2. Is it a defect? (classification)

Do not confuse these; record only real defects as bugs. Use `$T note --type …` for the rest.

| Class | Test | Record as |
|---|---|---|
| **Functional defect** | Behavior contradicts the spec/label/documented or clearly intended behavior | bug `functional` |
| **UI defect** | Rendering is wrong/broken (overlap, cut-off, wrong state shown) | bug `ui` |
| **UX inconvenience** | Works as designed but is confusing/hard to use | `note ux-suggestion` (or bug `ux`, Low, if it materially blocks users) |
| **Performance issue** | Measurably slow vs. a stated target or obviously unreasonable; give numbers | bug `performance` |
| **Configuration issue** | Caused by missing/wrong setup (env var, flag, permission) | bug `configuration` or note, per who must act |
| **Environment issue** | Caused by your setup: network, stale session, dirty data, wrong browser | **not a bug** until reproduced in a clean setup |
| **Feature request** | Something absent that was never promised | `note feature-request` |
| **Expected behavior** | Surprising to you but consistent with design/docs | `note expected-behavior` |

If you cannot tell whether it is intended, record it as `Unconfirmed` (or an `observation` note) and say what would settle it (spec, owner answer).

## 3. Severity and confidence

**Severity** (impact on users):
- **Critical** — data loss/corruption, security hole, crash/blocked core workflow with no workaround, cannot log in.
- **High** — core function broken or wrong results; workaround is hard.
- **Medium** — function degraded or wrong in secondary paths; reasonable workaround.
- **Low** — minor/cosmetic, rare edge case.
- **Informational** — observation worth knowing, no user impact.

**Confidence** (how sure you are it is a real, reproducible defect):
- **Confirmed** — reproduced ≥2 times from a clean state; evidence saved; expectation sourced. (The tracker enforces ≥2 reproductions + a file.)
- **Probable** — seen, partly reproduced or one-off with strong evidence; not yet isolated.
- **Unconfirmed** — one-off, cannot reproduce, or depends on unknown intent/environment.

Severity and confidence are independent: a Critical-but-Unconfirmed finding is reported prominently *and* labeled Unconfirmed.

## 4. Reproduction

Repeat from a clean state (new session, fresh record) at least twice; record `reproduced/attempted` (e.g. `5/5`, `2/5` for intermittent). Write the numbered steps as you perform them so another person can follow them exactly, including preconditions (role, data, setting). Then follow your own steps once from scratch to confirm they are complete. If it only occurs after specific prior actions, record that sequence. If it is not safely repeatable (e.g. destructive), say so and use `Probable`.

## 5. Recording the bug

```bash
$T add-bug --title "Search returns empty list for names with accents" \
  --features F-003 --severity High --confidence Confirmed --kind functional --category core-workflow \
  --precondition "Logged in as regular user; user 'José' exists" \
  --step "Open Users > List" --step "Type 'José' in the search box" --step "Press Enter" \
  --expected "Row for José is listed" --actual "'No results' is shown; Jose (no accent) works" \
  --evidence evidence/F-003-accent-empty.png --evidence evidence/F-003-network.log --repro 3/3 \
  --context "GET /api/users?q=Jos%3F -> 200, body []" \
  --suspected-area "Search request encoding" --suspected-basis "network log shows é sent as '?'" \
  --recommendation "Encode the query as UTF-8 before building the request URL" \
  --impl-area "Users list search request builder (frontend)" \
  --risk "Other callers of the same helper may depend on current encoding" \
  --verification "Search 'José' returns the row; 'Jose' and 'jos' unchanged; add a test with an accented name"
$T set F-003 FAILED --note "accent search broken (BUG-001)" --bug BUG-001
```

`--category` is the engineering-order class used by the report: `data-loss`, `blocking`, `core-workflow`, `integration`, `error-handling`, `secondary`, `cosmetic`.

## 6. Diagnosis (hypotheses vs facts)

Facts: what you observed (screen, message, request/response, log line). Hypotheses: why. Only name a source-level cause when evidence supports it (a stack trace line, a request payload, a log message). Use `--suspected-area` for the *area* (page, component, API, state management, database, configuration), with `--suspected-basis` stating the evidence. If you read source after the failure to localize it, say so and still label it a hypothesis unless you reproduced the cause (e.g., changed nothing but observed the exact failing value in a log).

## 7. Developer recommendations

For every Confirmed issue give: **Problem** (what is wrong), **Evidence** (why you concluded it), **Recommended modification** (the smallest change that fixes the confirmed problem and preserves existing behavior), **Implementation area** (page/component/function/API/state/DB/config, when identifiable), **Risk** (what else the change could affect), and a **Verification test** (exactly how the developer confirms the fix, including the original failing case and one neighboring case). Do not recommend rewrites, framework changes, or refactors unless the evidence shows the small fix is impossible — and then explain why. Do not edit source yourself unless the user asked you to.
