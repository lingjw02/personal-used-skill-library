# Detailed UI/UX Checklists

Use as probes, not a rigid script. Skip items that don't apply, and record what you skipped.

## Contents
1. Visual hierarchy
2. Layout and spacing
3. Typography and color
4. Components (buttons, inputs, dropdowns, modals, tables, cards, tabs, tooltips, nav)
5. State design matrix
6. Content and microcopy
7. Accessibility probes
8. Responsive probes
9. Friction patterns

## 1. Visual hierarchy
- Page title/heading present and distinguishable? Does it match the nav label the user clicked?
- Is there exactly one clearly primary action per view/section? Do secondary actions look secondary?
- Does the most prominent element (size, color, contrast, position) match the most important task or information?
- Heading levels visually distinct and sequential? Body vs label vs helper text distinguishable?
- Is it obvious what is clickable (links, cards, rows, icons) and what is static? Look for clickable things that look static and static things that look clickable.
- Warning signs: three equally loud buttons, destructive action styled as primary, decorative element outshining key data, status colors used decoratively.

## 2. Layout and spacing
- Consistent outer margins and container max-width across pages.
- Elements on a shared left/right edge actually align (labels, inputs, cards, table columns).
- Spacing follows a recognizable scale (e.g. 4/8/16/24); note random values.
- Cards in a row: equal height/width where they should be? Equal internal padding?
- Buttons in the same group: equal height, consistent order (e.g. Cancel left of Save everywhere).
- Content touching screen or container edges; text hugging borders.
- Clipping/truncation without tooltip or expansion; overflow scrollbars inside containers; overlapping layers (sticky header over content, dropdown under a card, toast over a button).
- Excess empty space vs crowded regions; unbalanced pages.
- Long content: long names, long strings without spaces, many items, large numbers, many table columns.

## 3. Typography and color
- Limited, consistent set of sizes/weights; line-height comfortable; line length readable (about 45-90 chars for prose).
- Text contrast: body, secondary/muted text, placeholder, disabled, text on images/colored backgrounds, text on buttons, links.
- Non-text contrast: input borders, icons, focus rings, chart elements against background.
- Color is not the sole carrier of meaning (status, errors, chart series, required fields).
- Semantic colors consistent (same red/green/amber meaning everywhere). Brand color not reused for error/success.
- If dark mode exists: test it; check contrast, shadows, images, borders.

## 4. Components

### Buttons
Hover feedback, pointer cursor, pressed/active feedback, visible focus, disabled looks disabled AND explains why if non-obvious, loading state on async actions (and blocks double submit), label describes outcome, icon-only buttons have tooltip/accessible name, size consistent and target at least about 24px (ideally 44px on touch).

### Inputs and forms
Visible label (not placeholder-only); required/optional indicated; helper text; focus style; typing and clearing work; clear affordance where appropriate; inline validation timing (not shouting on first keystroke, not only on submit); error text adjacent to the field, specific, and says how to fix; error persists until fixed; input preserved after error; sensible input types/masks (email, number, date); Enter submits where expected; Tab order follows visual order; autofocus appropriate; long forms chunked; destructive/irreversible submission confirmed.

### Dropdowns and menus
Open on click (and Enter/Space/ArrowDown); arrow-key navigation; Enter selects; Escape closes and returns focus to trigger; outside click closes; selected value clearly shown; long lists scroll/search; menu not clipped by container or viewport edge; only one open at a time.

### Modals and dialogs
Clear title and purpose; focus moves in, is trapped, returns on close; Escape closes (unless data-loss risk, then confirms); outside click behavior sensible; visible close control; primary/secondary button hierarchy; destructive confirm names the object ("Delete 'Q3 report'?"); background scroll locked; long content scrolls inside the modal with action buttons reachable; small-screen fit; stacked modals avoided.

### Tables and lists
Header clarity and stickiness; sort/filter indicators and state; alignment (numbers right-aligned, text left); row hover/selected states; row actions discoverable; pagination or infinite scroll with position feedback; empty/loading/error states; overflow behavior on narrow screens; column truncation with access to full value; bulk actions feedback.

### Cards
Consistent structure, padding, radius, shadow; clear whether whole card is clickable; action placement consistent; handles missing image/long title/missing data.

### Tabs, filters, search
Active tab obvious and keyboard operable; filter state visible and clearable; active filters summarized; search has clear affordance, empty-result message, loading feedback, preserves query on back-navigation.

### Tooltips and popovers
Reachable by keyboard focus, not only hover; don't cover the trigger; dismissible; contain non-essential info only; not the sole location of critical information.

### Navigation (sidebar, header, breadcrumbs)
Current page indicated clearly and consistently; labels match page titles; grouping logical; icons have labels or tooltips; sidebar expand/collapse state remembered and not janky; breadcrumbs accurate and clickable; browser Back/Forward behave; deep links and refresh preserve location and state; URL reflects tabs/filters where users would expect to share/bookmark; logo returns home; user/account menu discoverable; logout findable.

### Notifications and toasts
Appear near the action; readable duration; dismissible; don't stack unmanageably; announce success/failure; error toasts persist or are recoverable; not the only place an important error appears.

## 5. State design matrix

For each key interactive component, record presence and quality:

| State | What to check |
|---|---|
| Default | clear affordance |
| Hover | change visible, cursor correct |
| Focus | visible indicator, sufficient contrast |
| Active/pressed | immediate feedback |
| Disabled | looks inactive, reason available, not just low contrast |
| Loading | spinner/skeleton/progress; blocks repeat action; no layout jump |
| Success | confirmation of what happened and where to see it |
| Error | what/why/next step; field-level and form-level |
| Empty | explains why empty and offers the next action |
| Partial | incomplete data, optional fields, partially loaded lists |
| Offline/slow | graceful message, retry, no silent failure |

## 6. Content and microcopy
For each message ask: What happened? Why? What can I do next? Flag: generic "Something went wrong", raw error codes/stack text, jargon, internal terminology, inconsistent terms for one concept (Delete/Remove/Discard), ambiguous buttons ("OK", "Submit" in a multi-action dialog), placeholder text that disappears and was needed, tooltips repeating the label, confirmation messages that don't name the object, tone shifts between pages. Do not rewrite for taste.

## 7. Accessibility probes
- Tab through whole page: order logical? skip link? any element unreachable or trapped? any invisible focus?
- Can every mouse action be done by keyboard (menus, modals, tabs, date pickers, drag-and-drop alternatives)?
- Icon-only buttons: accessible name or tooltip? (inspect `aria-label`/text)
- Form fields programmatically labelled? Errors tied to fields (`aria-describedby`) where inspectable?
- Heading structure and landmarks (`header/nav/main/footer`) where inspectable.
- Zoom to 200% and text-only enlargement: content still usable?
- Motion: auto-playing or large animations; does `prefers-reduced-motion` get respected (if testable)?
- Target size, spacing between adjacent targets.
- Note explicitly: no screen reader testing performed unless you did so.

## 8. Responsive probes
At each tested width: horizontal page scroll? clipped/overlapping items? nav collapsed into working menu? primary action still visible? tables usable? forms usable with on-screen keyboard assumptions? images/charts scale? text wraps cleanly? touch targets adequate? modals fit and scroll? sticky elements eating too much viewport? Also check intermediate "awkward" widths (e.g. 900-1100px) where breakpoints often fail, and landscape mobile if cheap.

## 9. Friction patterns
Hidden or buried primary actions · unlabeled icons · action located far from the data it affects · missing confirmation on destructive actions · unnecessary confirmation on trivial ones · no success feedback · no loading feedback · lost input after error · forced re-entry of known data · forced memory across pages · unexpected navigation/redirects · modal chains · dead ends with no next step · unclear terminology · settings that don't say whether they auto-save · pagination/filters resetting unexpectedly · inconsistent location of the same action.
