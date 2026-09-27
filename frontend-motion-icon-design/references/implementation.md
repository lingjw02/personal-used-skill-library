# Implementation Guidance

The skill is framework-agnostic, but each ecosystem has natural tooling:

**React**: Framer Motion or React Spring for physics-based animation; `lottie-react`/`react-lottie` for Lottie JSON; styled-components/CSS Modules for scoped animation CSS. Always clean up animation refs on unmount.

**Vue**: Vue-Motion or VueUse Motion for reactive animation; `vue-lottie` for Lottie; built-in `v-enter-active`/`v-leave-active` transition classes for most cases.

**Angular**: built-in `@angular/animations` for declarative triggers (`[@fadeIn]`); `ngx-lottie` for Lottie; RxJS/observables to sync animation state with data.

**CSS/JS libraries**: `@keyframes` + `:hover`/`:active` + `prefers-reduced-motion` covers most cases. GreenSock (GSAP) for complex timelines/sequences the CSS approach can't handle. Anime.js for lightweight SVG-morphing/path animation. Web Animations API for direct JS control (`element.animate(...)`).

**Lottie**: embeds rich vector animation exported from After Effects (via Bodymovin) through a framework's Lottie component. Keep JSON under roughly 50–100KB where possible; `lottie-web` renders via Canvas or SVG, so test actual runtime performance, not just file size.

```jsx
import Lottie from 'react-lottie';
import animationData from './search.json';

<Lottie
  options={{ animationData, loop: false, autoplay: false }}
  height={48}
  width={48}
  isClickToPauseDisabled={true}
/>
```

## Sample component spec: Animated Loading Button

**Component**: `LoadingButton`
**Props**: `label: string`, `loading: boolean`, `onClick: function`

**Behavior**: when `loading=false`, shows a regular button with the label. On `loading=true` (e.g. after click), the label fades out and a spinner fades in. Once `loading=false` again, the label fades back in.

**Motion**: label↔spinner cross-fade over ~200ms; press gives a quick scale-down to 90% over ~100ms, then eases back out.

**States**: normal (label visible, icon hidden) · hover/focus (slight box-shadow increase) · pressed (scale down, background shifts) · loading (label opacity → 0, spinner opacity → 1).

**Accessibility**: `aria-busy="true"` on the button while loading; visually-hidden "Loading…" text for screen readers; spinner `<svg>` has `aria-label="Loading"` and `role="img"`. Under `prefers-reduced-motion: reduce`, skip the fade — swap instantly and drop transition durations to 0.

```jsx
<button className={loading ? 'btn loading' : 'btn'}
        onClick={onClick} disabled={loading}>
  {!loading && label}
  {loading && <SpinnerIcon aria-label="Loading" />}
</button>
```

```css
.btn {
  transition: transform var(--duration-fast) var(--curve-ease);
}
.btn:active {
  transform: scale(0.9);
}
.btn.loading > span {
  animation: fadeOut var(--duration-medium) var(--curve-ease) forwards;
}
.btn.loading > svg {
  animation: fadeIn var(--duration-medium) var(--curve-ease) forwards;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .btn.loading > span,
  .btn.loading > svg {
    animation: none;
  }
}
```

## Additional framework snippets

**React + Framer Motion, animated icon button:**
```jsx
import { motion } from 'framer-motion';
const AnimatedIcon = ({ icon: IconComp, label }) => (
  <motion.div
    role="button"
    whileHover={{ scale: 1.1 }}
    whileTap={{ scale: 0.9 }}
    tabIndex={0}
    aria-label={label}
  >
    <IconComp width={24} height={24} />
  </motion.div>
);
```

**Vue, CSS-transition spinner swap:**
```vue
<template>
  <button @click="increment" class="counter-btn">
    <span v-if="!loading">{{ count }} Votes</span>
    <svg v-else class="spinner"><!-- spinner SVG --></svg>
  </button>
</template>
<script>
export default {
  data() { return { count: 0, loading: false } },
  methods: {
    increment() {
      this.loading = true;
      setTimeout(() => { this.count++; this.loading = false; }, 1000);
    }
  }
}
</script>
<style>
.counter-btn span { transition: opacity 0.3s ease; }
.counter-btn .spinner { opacity: 0; transition: opacity 0.3s ease; }
.counter-btn.loading span { opacity: 0; }
.counter-btn.loading .spinner { opacity: 1; }
</style>
```

**Angular, template-driven enter/leave + toggle animations:**
```html
<button [@fadeInOut]="inView ? 'in' : 'out'" (click)="showDetail()">
  Show Details
</button>
<ng-template #details>
  <div @slideDownUp>Here are the details!</div>
</ng-template>
```
```ts
import { trigger, state, style, transition, animate } from '@angular/animations';
@Component({
  animations: [
    trigger('slideDownUp', [
      transition(':enter', [
        style({ height: '0px', opacity: 0 }),
        animate('300ms ease-out', style({ height: '*', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('300ms ease-in', style({ height: '0px', opacity: 0 }))
      ])
    ]),
    trigger('fadeInOut', [
      state('in', style({ opacity: 1 })),
      state('out', style({ opacity: 0 })),
      transition('out => in', [ animate('200ms') ]),
      transition('in => out', [ animate('200ms') ])
    ])
  ]
})
export class ExampleComponent { inView = false; showDetail(){ this.inView = true; } }
```

## Full token reference

```css
/* Motion */
--duration-quick: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
--easing-standard: cubic-bezier(0.4, 0, 0.2, 1);
--delay-stagger: 50ms;   /* sequential reveals */
--spring-stiff: 300 20;  /* spring config for physics-based libs */

/* Icons */
--icon-size-xs: 16px; --icon-size-sm: 20px; --icon-size-md: 24px; --icon-size-lg: 32px;
--icon-color-primary: #333; --icon-color-secondary: #888; --icon-color-disabled: #CCC;
--icon-stroke-width: 2px;
```
