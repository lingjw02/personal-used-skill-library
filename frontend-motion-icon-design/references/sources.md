# Verification & Evidence Sources

Every design claim or guideline in this skill's output should be traceable to a source, prioritizing primary sources:

- **WCAG (W3C)** — for accessibility requirements: animation pause/stop, reduced motion, contrast, target sizes, flashing content limits.
- **Platform HIGs** — Apple Human Interface Guidelines (animation), Android Material Design (motion style, icon usage), Microsoft Fluent (light, depth, motion principles).
- **Design system docs** — Material Design motion/icon guidelines, Google's Material Icons reference, Apple's SF Symbols documentation.
- **Browser specs/MDN** — technical behavior, e.g. `prefers-reduced-motion` usage and support.
- **Component library docs** — if using Bootstrap, MUI, etc., their own animation/icon documentation.

When uncertain, say so. If recommending a specific animation library, verify it's actively maintained where possible; if unsure, label it explicitly, e.g. "(e.g. GreenSock or Anime.js — check current maintenance status)."

Any new "fact" introduced (an icon size standard, an animation duration convention) should either cite a source or be labeled "common practice" if it's drawn from general UX convention rather than a specific document. Never invent data or cite a study/spec that wasn't actually checked. If a detail can't be verified, say "(source needed)" or "(unverified)" rather than stating it as settled.
