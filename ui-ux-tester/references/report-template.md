# UI/UX Test Report Template

Fill every section. If a section has nothing to report, say what was checked and found fine. Never leave a section silently empty, and never include evidence you did not capture.

---

# UI/UX Test Report: <App name>

**Date / Tester:** · **Target:** <URL/build> · **Environment:** <browser, OS, viewports tested, auth role, test data> · **Scope:** <pages/workflows covered>

## 1. Overall Interface Assessment
2-4 short paragraphs describing observed characteristics, strengths, and dominant problem themes, in measured language. Include counts by severity:

| Critical | High | Medium | Low | Cosmetic |
|---|---|---|---|---|

State the primary user audience and tasks assumed.

## 2. Page-by-Page Review

| Page | Visual | Usability | Interaction | Responsive | Issues |
|---|---|---|---|---|---|
| /dashboard | Good: clear hierarchy | Fair: filters hidden | Good | Fail at 375px | UI-003, UI-007 |

Use short ratings (Good / Fair / Poor / Not tested) with a few words of reason.

## 3. UI Findings

| ID | Type | Severity | Confidence | Page | Problem |
|---|---|---|---|---|---|

Sort by severity, then by page.

## 4. Detailed Findings

### UI-001: <title>
- **Type / Severity / Confidence:**
- **Page / Component:**
- **Observation:** (include steps to reproduce when interaction-dependent)
- **User impact:**
- **Evidence:** (screenshot path or exact interaction sequence)
- **Recommendation:** (specific; name property/token/component and target value where possible)
- **Expected result / benefit:**
- **Potential side effects:**
- **Verification:** (how to confirm the fix)

## 5. Consistency Review

### Design Consistency Matrix
| Component | Page A | Page B | Page C | Consistent |
|---|---|---|---|---|

Follow with notes on each "No": which variant should be the standard and why (usually the most common or the one that best meets usability needs).

## 6. Accessibility Review
- **Tested:** keyboard navigation (pages), focus visibility, contrast measurements (method), target sizes, labels, etc.
- **Observed concerns:** list with finding IDs. Use "Potential accessibility issue" when evidence is limited.
- **Not tested / limitations:** e.g. no screen reader, no full WCAG audit, no zoom testing.
- No claim of WCAG compliance unless a full audit was performed.

## 7. Responsive Review

| Viewport | Pages checked | Result | Findings |
|---|---|---|---|
| 1920 | | | |
| 1366 | | | |
| 768 | | | |
| 375 | | | |

## 8. Interaction Review
Problematic patterns: missing/incorrect states, feedback gaps, keyboard gaps, modal/dropdown behavior, navigation/URL sync. Also list interaction patterns that work well and should be preserved.

## 9. Design System Recommendations
Observed system (approximate values marked `approx.`):

| Token | Observed |
|---|---|
| Primary color | |
| Semantic colors | |
| Type scale | |
| Radius / shadow | |
| Spacing scale | |
| Button / input / card / modal variants | |

Recommend changes only where evidence shows they are necessary, referencing finding IDs.

## 10. Coverage and Limitations
- Pages/components reached vs not reached (and why)
- States forced vs not forced (error/empty/offline/loading)
- Tools used, what could not be tested
- Items marked Unconfirmed/Probable and what would confirm them

## 11. Implementation Checklist
Ordered, directly actionable, one line each, referencing IDs:

- [ ] UI-004 (High): <exact change>
- [ ] UI-001 (High): <exact change>
- ...

Group optional improvements last under "Design Improvements (subjective)".

## 12. Fix Verification (only when re-testing)

| ID | Previous status | Result (Fixed / Partially / Not fixed / Regressed) | Evidence |
|---|---|---|---|
