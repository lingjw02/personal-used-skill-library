# Motion & Animation Guidelines

## Principles

Motion should clarify, not distract. Use it to indicate state changes, focus shifts, or feedback. Prefer natural, physics-based easing (acceleration then deceleration). Apple's Human Interface Guidelines advise using animation judiciously and striving for realism — movement should make sense or it feels disorienting. Always support reduced motion: use the `prefers-reduced-motion` media query (or the equivalent platform setting) to disable or simplify animations for users who opt out.

## Common animations & patterns

- **Loading indicators**: spinner or progress bar for indeterminate waits; skeleton screens for data loading improve perceived performance. If a loading animation runs beyond 5s, provide a cancel or fallback.
- **Hover/active feedback**: subtle animation on hover/press (color fade, slight scale or shadow change) — e.g. a CSS ripple on click, or a scale-down on tap.
- **Transitions between views**: fade or slide, typically 150–300ms with ease-in-out, kept short (≤300ms) so they don't delay content. Modals/dialogs commonly fade or scale up from the trigger's position.
- **Interactive controls**: toggles, accordions, dropdowns animate open/close smoothly (height expansion, or `clip-path`); keep it snappy, not slow.
- **Micro-interactions**: small animations on state change (toggle knob + background, a "like" button pop, a brief shake/color change on form validation error). Fast (<300ms), and never required to understand the UI.
- **Entry/splash animations**: brief animation on launch or screen entry (logo fade/scale, content slide-in). Per WCAG, treat these as "essential" only if they communicate real progress; otherwise let the user skip. Keep them short (roughly 0.5–1.5s) and always bypassable (e.g. tap to skip).
- **Outro/exit animations**: fade-out or slide-away on delete/close, similarly quick.

## Timing & easing

Keep durations and easings consistent across the UI. Common conventions: 150ms (fast), 300ms (normal), 500ms (slow). Ease-out for objects leaving, ease-in for objects arriving; spring/bounce curves for playful UIs. Avoid linear motion unless intentional — rapid, jittery, or blinking motion can trigger vestibular discomfort.

## Accessibility

Honor `prefers-reduced-motion`: replace complex animations with a simple cross-fade or no animation. Never rely on motion alone to convey information — pair it with a state change the user can also perceive statically (a color/text/icon change).

## Performance

Prefer CSS `transform`/`opacity` (GPU-accelerated) over layout-triggering properties (`top`/`left`/`width`/`height`), which cause jank. Limit simultaneous animations. Optimize Lottie/GIF assets (see comparison table below). Use the Web Animations API or `requestAnimationFrame` for coordinated sequences when necessary; most simple UI transitions only need CSS3.

### Example CSS animation with reduced-motion fallback

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.animated {
  animation: fadeIn 0.25s ease-in-out both;
}

@media (prefers-reduced-motion: reduce) {
  .animated {
    animation: none;
  }
}
```

## Animation technique comparison

| Technique | Pros | Cons | Performance impact |
|---|---|---|---|
| CSS animations/transitions | Easy; GPU-accelerated; works everywhere | Limited to a few properties; less control for complex sequences | Low (compositor) |
| Web Animations API (JS) | Full JS control of the timeline; pause/resume; keyframes in JS | More code; learning curve; may need a polyfill on old browsers | Moderate (still CSS transforms) |
| JS (`requestAnimationFrame`) | Max control for complex/numeric or physics-based animation | More CPU work; can jank if unoptimized | High (CPU-driven) |
| SVG `<animate>`/SMIL | Declarative, built into SVG | Deprecated/poor support in some browsers; limited easing | Moderate (SVG rendering cost) |
| Lottie (JSON, After Effects) | Rich multi-part animations from designers; scalable, loopable | Large JSON files; runtime parsing overhead; needs a Lottie library | Variable — can be heavy (100–200KB+, real load cost) |
| GIF/APNG/video | Trivial to embed | Large file size; no interactivity; hard to match UI style; no control | High (frame decoding, blocking) |

Choose CSS for simple UI transitions; reach for Lottie or video only for genuinely complex animation (animated illustrations), and only when it's worth the weight. Always test on target devices, not just desktop dev tools.

## Entry (opening) animations

An entry animation (splash screen or content reveal) sets initial context. It should orient the user quickly, not delay interaction or distract.

- **Splash screen with progress**: brief logo fade-in/scale-up while loading. Treat as "essential" (non-skippable) only if it communicates real load progress; otherwise let the user skip.
- **Content reveal**: staggered fade/slide of page sections (nav, header, content blocks) instead of a blank page. Keep individual stagger delays short (50–100ms) so content appears promptly.
- **Interaction prompt**: for onboarding, animate the next action into view (e.g. a "Get Started" button).

Guidelines: limit full-screen splash animations to under 5s total, or provide a skip action if longer. Use a real progress indicator for lengthy loads. Entry animations must never block keyboard focus/interaction (WCAG 3.2.1). For single-page apps, animate transitions between major sections (old section out, new section in) rather than hard-cutting.
