# Checklists & Templates

## Motion/animation checklist (run this per animation/transition)

- **Purpose**: does it convey feedback, status, or a context change?
- **Timing**: appropriate duration (roughly 150–300ms for UI transitions)? Ease-in/out curves for smooth motion?
- **Hardware acceleration**: uses `transform`/`opacity`, not `width`/`height`?
- **Accessibility**: can it be disabled/simplified via `prefers-reduced-motion`?
- **Loops and delays**: no infinite loop without a pause control; entry animations don't exceed ~5s unless truly essential.
- **Phases covered**: loading (spinner/skeleton), empty/error states, final state.
- **Performance**: limited simultaneous animations; compressed assets (optimized Lottie JSON, etc.).
- **Tested**: verified on target devices (desktop/mobile/tablet) and with reduced-motion settings on.

## Iconography checklist (run this per icon)

- **Accessibility**: meaningful icon → `<title>`/`aria-label`; purely decorative → `aria-hidden="true"`.
- **Consistency**: shares style (outline/filled), stroke weight, corner radius with the rest of the set; matches the brand/design system.
- **Size & spacing**: base sizes defined (e.g. 24×24 toolbar, 32×32 buttons); ≥44×44 CSS px touch target.
- **States**: size/color defined for normal, hover/focus, active/pressed, disabled.
- **File format**: SVG preferred; icon-font fallbacks handled if used.
- **Color & contrast**: distinguishable in all states; not color-only for meaning.
- **Organization**: sprite/icon-system used to cut down HTTP requests.

## General UI checklist (every design task)

- Clarity of the user's goal and the primary action.
- Readability: font sizes, line-heights, contrast.
- Layout grid and spacing consistency.
- Responsive adaptation for mobile/desktop.
- Keyboard/mouse/focus behavior (tab order, visible focus indicators).
- Localization readiness (icon meaning stays culturally appropriate).
- Technical constraints acknowledged (animation library choice, screen resolution, browser support).
- Risk mitigation: any unverified assumption is noted explicitly (e.g. "data volume unknown — flagged as a risk").

## Templates

**Storyboarding template**: outline an animation as a sequence — `State A → animation → State B` — with the user trigger, the effect, and timing/easing notes.

**Component spec template** (per component — Button, Modal, IconButton, etc.):
- Props/inputs (label, icon, disabled, ...)
- States and their styling (normal/hover/active/disabled)
- Motion: how it animates between states (ripple, fade, expand, ...)
- Accessibility: required ARIA roles/labels
- Code hooks: event handlers

**Design token definitions**:
```css
/* Motion tokens */
--duration-fast: 150ms;
--duration-medium: 300ms;
--ease: cubic-bezier(0.4, 0, 0.2, 1);
--shadow-depth-low: 0 1px 2px rgba(0,0,0,0.1);

/* Icon tokens */
--icon-sm: 16px;
--icon-md: 24px;
--icon-lg: 32px;
```

**Accessibility note template** (attach to every component spec):
```
// Accessibility: This component uses SVG. Provide a <title> inside the SVG
// for screen readers, or set aria-hidden="true" if decorative.
```
