# Accessibility & Performance Constraints

## Accessibility (WCAG)

- **Reduce motion**: honor `prefers-reduced-motion`. Provide an equivalent effect (instant reveal, or a simple cross-fade) rather than just deleting the transition entirely.
- **Animation control**: any non-essential animation that auto-plays for more than 5 seconds must be pausable or stoppable — this includes carousels, auto-scrolling tickers, and animated infographics. Provide a pause button or skip option.
- **Flashing content**: never flash more than 3 times per second (WCAG 2.3.1) — no blinking notices or rapid flashing highlights.
- **Icon accessibility**: use `role="img"` with a `<title>`/`aria-label`, or `aria-hidden="true"` for decorative icons.
- **Contrast & size**: icons and text meet contrast minimums; touch targets at least 44×44px; keyboard operability preserved (animations must not auto-advance without user control when triggered by a key).

## Performance

- **Animation efficiency**: use GPU-friendly properties (`transform`, `opacity`); avoid animating `top`/`left`/`width`/`height`, which force layout thrash.
- **Asset optimization**: minify Lottie JSON; use vector icon sprites or inlined SVG; keep frame rates smooth (60fps target) while minimizing redraw work.
- **Lazy loading**: defer offscreen animations — e.g. only animate an icon once it scrolls into view.
- **Memory/CPU**: limit the number of simultaneously active animations. In React/Vue/Angular, always clean up JS animation instances on component unmount to avoid leaks.
- **Testing**: profile on low-end devices, not just a dev machine. Disable any animation library instance that would otherwise loop continuously.

Following WCAG and platform guidelines, plus checking performance explicitly, reduces the risk of user discomfort (motion sickness, seizure triggers) and a sluggish UI.
