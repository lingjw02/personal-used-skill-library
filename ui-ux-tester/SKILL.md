---
name: ui-ux-tester
description: Autonomous UI/UX testing of a running application by actually driving it with mouse, keyboard and viewport resizing, then producing an evidence-based report with severity-rated findings, a design consistency matrix, and concrete fix recommendations. Use this skill whenever the user asks to review, audit, critique, test, or evaluate the look, feel, usability, responsiveness, accessibility, consistency, or interaction quality of a web app, dashboard, site, or UI, even if they only say "check the UI", "does this feel right", "find design problems", "review the frontend", or "UX review". Also use it after UI changes to verify fixes. This is complementary to functional QA - it asks "can users understand and comfortably use it?" rather than "does it work?". Do not use for pure functional/API testing or for generating new designs from scratch.
---

# UI/UX Tester

Evaluate the **rendered, running interface** like a professional UI/UX tester. The question this skill answers is: *can users understand, operate, and comfortably use the system?* A functional QA tester asks whether it works; you ask whether it is clear, consistent, accessible, and low-friction.

Source code can explain a finding, but it never replaces observing the rendered UI. A single screenshot is not a review. Interact.

## Method

**Observe → Navigate → Interact → Compare → Identify friction → Verify → Document → Recommend**

## Step 0: Establish tooling and scope

Before testing, find out what you can actually do, because every claim in the report must be traceable to something you did.

1. **Identify the driver.** Look for any of: a browser automation tool (Playwright, Puppeteer, Selenium, a browser MCP), a computer-use tool (screenshot + mouse + keyboard), Claude in Chrome, or a local dev server you can launch and drive from bash. Use real input events (click, hover, type, Tab, Escape, viewport resize), not DOM-only shortcuts, whenever possible.
2. **Get the target.** A URL, a local dev command, or a running window. If none is provided and none is discoverable (check the repo for a start script, README, `package.json`), ask once.
3. **Record the environment** (browser, viewport sizes, OS, auth state, test data). It goes in the report's Limitations section.
4. **If you cannot interact at all** (no browser, no display, app won't start): say so plainly. You may offer a clearly labelled *static code review* of markup/CSS, but every finding from it is `Unconfirmed` and the report must state that nothing was observed live. Never fabricate screenshots, states, or interactions.
5. **Ask about scope only if it changes the work materially**: target users, critical workflows, pages out of bounds, destructive actions. Otherwise state your assumptions and proceed. Do not trigger destructive actions (delete, pay, send) on real data without permission; use test data or stop at the confirmation step and note it.

Consider the application's **purpose and audience**. A dense trading dashboard and a consumer onboarding flow have different right answers. Preserve intentional design decisions that do not hurt usability.

## Step 1: Build the UI map (inventory)

Before detailed testing, walk the app and write an internal map. Capture:

- Global navigation, sidebar, top bar, main content, footer
- Every reachable page/route and how it is reached
- Reusable components: buttons, inputs, selects, cards, tables, tabs, filters, search, menus, modals/dialogs, toasts/notifications, tooltips
- Primary user workflows (3-6 of them, ranked by importance)

This map drives coverage. At the end, list pages/components you did not reach.

## Step 2: Evaluate each page

For every page, work through the checklists in `references/checklists.md` (read it now; it has the detailed probes). Summary of the dimensions:

1. **Visual hierarchy**: can a new user tell within seconds (a) where they are, (b) what the page is about, (c) the primary action, (d) what is important, (e) what is secondary, (f) what is interactive? Flag cases where visual emphasis contradicts functional importance.
2. **Layout and spacing**: margins, padding, grid alignment, vertical rhythm, whitespace, edge contact, overflow, clipping, overlap, inconsistent card/button sizes.
3. **Interaction**: hover, click, active, disabled, loading for buttons; focus, typing, clearing, invalid input, validation for inputs; open/select/close/outside-click/keyboard for dropdowns; open/close/Escape/outside-click/confirm/cancel/long content/small screen for modals; active state, breadcrumbs, back button, URL/state sync for navigation.
4. **Responsive**: actually resize (see below).
5. **Accessibility**: practical checks (see below).
6. **State design**: default, hover, focus, active, disabled, loading, success, error, empty, partial, offline. Note which are **missing**, e.g. a network-triggering button with no loading state invites double submission.
7. **Content and microcopy**: does wording say what happened, why, and what to do next? Only flag copy that creates ambiguity or friction, not personal taste.

Force states you will not see by default: submit empty forms, enter invalid data, clear lists/filters to reach empty states, throttle or go offline if the driver allows, trigger error paths with harmless bad input.

## Responsive testing

If the app is responsive, **resize the actual viewport** and inspect the result. Do not infer from media queries. At minimum:

| Class | Typical width |
|---|---|
| Large desktop | 1920 |
| Laptop | 1366 (or 1440) |
| Tablet | 768 |
| Mobile | 375 (also try 320 if cheap) |

At each size, check: horizontal scrolling, overlap, hidden or unreachable controls, text wrapping/truncation, navigation collapse (does the menu exist and work?), modal overflow, table overflow, stretched images, spacing. Re-test one modal and one form at mobile size, since that is where they usually break. Record exactly which sizes you tested.

## Accessibility testing (practical, not a certification)

Test with the keyboard for real: Tab / Shift+Tab through each page, Enter/Space on controls, Escape on overlays, arrow keys in menus/tabs/selects.

Check: logical tab order, **visible focus indicator** on every focusable element, no keyboard traps, focus moves into a modal and returns on close, accessible names for icon-only controls, labels on form fields (not placeholder-only), errors communicated in text near the field (not color alone), contrast of text and UI components, touch/click target size, disabled-state clarity, tooltip availability by keyboard, and semantic structure where inspectable (headings, landmarks, button vs div).

Use `scripts/contrast.py` and the snippets in `references/measurement-snippets.md` to measure rather than eyeball contrast and target size.

**Language rule:** never claim WCAG conformance unless a proper audit was performed. When evidence is limited, write "Potential accessibility issue" and state what you did and did not check (e.g. "no screen reader was used"). Measured contrast below 4.5:1 for body text is a *confirmed measurement*; calling it a "WCAG failure" is acceptable only with the measured ratio and text size cited.

## Step 3: Cross-page consistency

Compare the same component across all pages and build a **Design Consistency Matrix**:

| Component | Page A | Page B | Page C | Consistent |
|---|---|---|---|---|
| Primary button | Style A | Style A | Style B | No |

Cover buttons, icons (same icon = same meaning; same action = same icon), border radius, shadows, typography, spacing pattern, semantic colors, error/success behaviour, modal structure, table behaviour, navigation behaviour. Describe each style by observed values (e.g. "blue #2563EB, 8px radius, 14px/600"), not vague labels.

## Step 4: Workflow friction testing

For each important workflow: state the user's goal, attempt it naturally as a first-time user would, then record interaction count, confusing steps, unclear terminology, unnecessary navigation, missing feedback, hidden actions, ambiguous icons, missing confirmation, poor error recovery, and information the user must remember from another page.

Fewer clicks is not automatically better. For each step ask whether it delivers needed information or protects against a costly mistake (e.g. confirmation before delete). Only flag steps that add effort without adding value, and say so when a step is justified.

## Step 5: Verify before you report

- Reproduce each suspected issue at least once more, ideally via a different path or viewport. Mark `Confirmed` only if you saw it directly and can state the steps. Use `Probable` if consistent evidence points to it but you could not isolate it. Use `Unconfirmed` for code-only or one-off observations.
- Distinguish **objective defects** (overlap, clipped text, unreachable control, invisible focus, broken hover/click) from **subjective preferences** (taste, trend). Subjective items go in "Design Improvement" and are labelled as such. Never call a design bad merely because it differs from current trends.
- Capture evidence at the moment you observe it: screenshot path, or an exact interaction sequence ("At 375px, open Settings > Billing, tap Edit; the modal's Save button is below the fold and the modal does not scroll"). Never invent evidence.

## Findings: classification and format

**Types:** Visual Defect · Interaction Defect · Usability Issue · Accessibility Concern · Consistency Issue · Design Improvement

**Severity:** Critical (blocks a core task or excludes users) · High (major friction or likely errors on a key flow) · Medium (noticeable, workaround exists) · Low (minor annoyance) · Cosmetic

**Confidence:** Confirmed · Probable · Unconfirmed

Every important finding uses this record:

```
### UI-001: <short title>
- Type / Severity / Confidence:
- Page / Component:
- Observation: what was actually seen (steps to reproduce if interaction-dependent)
- User impact: who is affected and how
- Evidence: screenshot path or interaction sequence
- Recommendation: specific change (what to change)
- Rationale and expected benefit: why, and what improves for users
- Potential side effects: what else the change could affect
- Verification: how to check the fix (steps, viewport, measurement)
```

**Recommendations must be concrete.** Bad: "Improve the sidebar." Good: "Reduce visual competition between the active nav item and its siblings: give the active item one distinct treatment (e.g. filled background plus bolder label) and apply the identical state on every page." Where useful, name the CSS property/token/component to change and a target value, so a developer or coding agent can implement it directly.

## Design system extraction (when useful)

Infer the existing system from observation, not imagination: primary and semantic colors, type hierarchy, radius, shadows, spacing scale, button/input/card/modal variants, icon style. Use measurement snippets for real computed values. Mark anything estimated as `approx.` and do not propose a new system before documenting the existing one. Recommend system changes only where evidence shows inconsistency or a defect.

## Final report

Produce the report using `references/report-template.md` (read it before writing). Sections: 1 Overall assessment, 2 Page-by-page review, 3 Findings table, 4 Detailed findings, 5 Consistency review, 6 Accessibility review, 7 Responsive review, 8 Interaction review, 9 Design system recommendations, plus **Coverage and Limitations** and a prioritized **Implementation checklist** that a developer or coding agent can work through top to bottom.

Delivery: if the report is long, save it as a Markdown file (and present it via the file-presenting tool if available); otherwise give it inline. Keep the chat summary to the headline findings and counts by severity.

If you are asked to verify fixes, re-run the original reproduction steps at the same viewport and mark each prior issue as Fixed, Partially fixed, Not fixed, or Regressed, and note any new issues the change introduced.

## Rules (and why)

- **Interact for real.** Static impressions miss hover, focus, loading, overflow, and responsive failures, which is where most UX problems live.
- **Never claim untested things.** If you did not test it, list it under Limitations. An honest gap is more useful than a confident guess.
- **Never claim WCAG compliance** without a proper audit; use "potential accessibility issue" wording.
- **Never invent screenshots or evidence.**
- **Separate defects from preferences**, and consider purpose and audience.
- **Compare repeated components across pages.** Inconsistency is only visible by comparison.
- **Test keyboard, responsive, states** (including loading, error, empty) on every reviewed area you can reach.
- **Give concrete modifications**, and verify proposed fixes by interacting when you can.
- **Stay non-destructive** unless the user has authorized otherwise.
