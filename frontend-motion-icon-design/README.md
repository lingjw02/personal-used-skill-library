# ⚡ Frontend Motion & Icon Design

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Skill-4285F4?logo=google&logoColor=white)](https://github.com/)
[![Claude Compatible](https://img.shields.io/badge/Claude-Code%20%26%20Desktop-D97757?logo=anthropic&logoColor=white)](https://github.com/)
[![WCAG: 2.2 AA](https://img.shields.io/badge/WCAG-2.2%20AA%20Compliant-green.svg)](https://www.w3.org/WAI/standards-guidelines/wcag/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Category: Frontend Engineering](https://img.shields.io/badge/Category-UI%2FUX%20%26%20Motion-00BCD4)](SKILL.md)

A senior UI/UX engineering skill for web and mobile interfaces that elevates user experience through deliberate, accessible **motion design** (transitions, micro-interactions, loading states, entry choreography) and **scalable iconography systems** (clean SVG geometry and accessible icon tokens).

Grounded in an **independent judgment and 3-level review protocol** (Technical Evidence → UX Logic → Visual & Risk), ensuring animations and icons earn their place through usability, performance, and accessibility rather than superficial decoration.

---

## ⚖️ Before & After Comparison

| Factor | ❌ Before (Standard / Decorative Animation) | ✅ After (With `frontend-motion-icon-design`) |
|---|---|---|
| **Animation Purpose** | Decorative "bling" added arbitrarily (`transition: all 0.5s ease-in-out`) | Intentional state communication (spatial awareness, progress feedback, hierarchy cues) |
| **Rendering Performance** | Animating layout properties (`top`, `left`, `width`, `height`, `margin`) causing continuous layout thrashing and dropped frames (<30fps) | 60fps GPU acceleration strictly animating composite properties (`transform`, `opacity`) with optimal `will-change` hints |
| **Motion Accessibility** | Zero consideration for vestibular sensitivity; triggers nausea on sensitive users | Enforces `@media (prefers-reduced-motion: reduce)` fallbacks for all non-essential movement (instant switch or soft cross-fade) |
| **Touch Targets** | Tiny interactive icons (<24–32px) causing frequent misclicks on touchscreens | Enforces minimum 44×44 CSS px touch target hitboxes per WCAG 2.5.5 |
| **Screen Reader Accessibility** | Unlabeled icon-only buttons (`<button><svg>...</svg></button>`) announced as blank by assistive technology | Strict accessibility tagging: semantic `aria-label`, inline `<title id="...">`, and `aria-hidden="true"` on decorative icons |
| **Looping & Flashing** | Infinite auto-playing carousels or splash animations that cannot be paused | Auto-playing motion >5s is required to be pausable or skippable; strict zero-tolerance for flashing >3×/sec (WCAG 2.3.1) |
| **Choreography Timing** | Sluggish transitions (>500ms) making the application feel unresponsive | Micro-interactions tuned to human perception thresholds (100–300ms, natural decelerate/spring curves) |

### Code Implementation Comparison

#### ❌ Before (Sluggish, Inaccessible CSS)
```css
/* Bad: Triggers layout recalculation, no reduced-motion fallback, arbitrary timing */
.modal {
  transition: all 0.6s ease;
  top: -100px;
  width: 300px;
}
.modal.open {
  top: 100px;
  width: 500px;
}
.icon-btn {
  width: 24px;
  height: 24px; /* Too small for fingers! */
}
```

#### ✅ After (High-Performance, Accessible CSS)
```css
/* Good: Composited transform, instant fallback for reduced motion, 44px hit area */
.modal {
  opacity: 0;
  transform: translateY(-16px) scale(0.98);
  transition: opacity 200ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform, opacity;
}
.modal.open {
  opacity: 1;
  transform: translateY(0) scale(1);
}

@media (prefers-reduced-motion: reduce) {
  .modal {
    transition: opacity 100ms ease-out;
    transform: none !important;
  }
}

.icon-btn {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

---

## ✨ Features

- **Three-Level Review Protocol:**
  - **Level 1 (Evidence & Technical):** Verifies WCAG criteria, browser API compatibility, and frame-rate math.
  - **Level 2 (UX & Logic):** Audits cognitive load, trigger-result coherence, and state coverage (loading, error, empty, active).
  - **Level 3 (Visual & Risk):** Audits contrast, grid alignment, loop risks, and cross-device performance budgets.
- **Micro-Interaction System:** Timing scales, spring mechanics, and state transitions for buttons, toggles, dropdowns, bottom sheets, and modals.
- **Accessible Icon Architecture:** Scalable vector guidelines, stroke consistency, optical sizing, and SVG semantic markup.
- **Multi-Framework Ready:** Ready-to-copy code tokens and implementations for **React**, **Vue**, **Angular**, **Tailwind CSS**, and **Framer Motion**.

---

## 📂 Repository Structure

```
frontend-motion-icon-design/
├── SKILL.md                                  # Core design instructions & 3-level review protocol
├── README.md                                 # Documentation & Before/After comparison
└── references/
    ├── accessibility-performance.md          # Full WCAG constraints & frame performance budgets
    ├── checklists-and-templates.md           # Motion, Iconography & General UI audit checklists
    ├── iconography.md                        # SVG style, sizing, grid optical weights & tokens
    ├── implementation.md                     # React, Vue, Framer Motion, and CSS code samples
    ├── interaction-patterns.md               # Micro-interactions, button states, toggles & timing
    ├── motion-guidelines.md                  # Animation physics, duration tables & easing curves
    └── sources.md                            # Standards citations (WCAG 2.2, Apple HIG, Material Design 3)
```

---

## 🚀 Installation & Setup

### For Google Antigravity (AGY)
Add to your project's workspace or global skills directory:
```bash
# Workspace level
mkdir -p .agent/skills
cp -r frontend-motion-icon-design .agent/skills/

# Global level
cp -r frontend-motion-icon-design ~/.gemini/skills/
```

### For Claude Code / Claude Desktop
Copy into your Claude skills directory:
```bash
mkdir -p ~/.claude/skills
cp -r frontend-motion-icon-design ~/.claude/skills/
```

---

## 💡 Example Trigger Prompts

- *"Design a fluid micro-interaction and loading animation for this submit button in React with Tailwind, ensuring it meets WCAG AA standards."*
- *"Audit the animations in our checkout flow and create a prefers-reduced-motion fallback plan."*
- *"Create an accessible SVG icon system for our navigation bar with proper aria attributes and 44px touch targets."*
- *"Polish this mobile modal transition with spring physics and zero layout thrashing."*

---

## 📄 License

This skill is distributed under the [MIT License](../LICENSE).
