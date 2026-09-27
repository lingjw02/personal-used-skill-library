# 🖋️ Logo & Brand Identity Designer

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Skill-4285F4?logo=google&logoColor=white)](https://github.com/)
[![Claude Compatible](https://img.shields.io/badge/Claude-Code%20%26%20Desktop-D97757?logo=anthropic&logoColor=white)](https://github.com/)
[![Output: Vector SVG Ready](https://img.shields.io/badge/Format-SVG%20%2B%20Vector%20Master-00E676)](references/production-delivery.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Category: Brand Identity](https://img.shields.io/badge/Category-Brand%20Design-FF9800)](SKILL.md)

An end-to-end brand identity and vector logo design engineering workflow. Guides teams from initial brief intake and strategic differentiation through 3+ distinct concept territories, AI image-generation prompts, multi-factor evaluation scoring, vector production specs, and complete asset package delivery.

Enforces real-world production discipline: **Treats AI raster output as concept material until rebuilt as genuine, scalable vector artwork**.

---

## ⚖️ Before & After Comparison

| Factor | ❌ Before (Ad-Hoc Prompting / Generic Logo Generator) | ✅ After (With `logo-identity-designer`) |
|---|---|---|
| **Strategy & Context** | Immediate prompt jumping: "make a cool modern tech logo in blue", ignoring audience and market | Brief validation & strategic differentiation: core brand thesis, audience profiling, and category cliché avoidance |
| **Concept Variety** | Generates 4 minor variations of the exact same cliché (e.g. 4 glowing blue brain icons) | Develops 3–5 distinct visual concept territories (e.g. geometric monogram vs typographic wordmark vs metaphorical symbol) |
| **Vector Production** | Raster PNG with glossy 3D gradients and drop shadows; unusable for print or web scaling | Production-ready SVG vector master with defined bezier curves, clean geometry, and scalable viewBox coordinates |
| **Monochrome Versatility** | Degrades into an unrecognizable dark blob when printed in single-color black and white | Tested and verified in 1-bit monochrome (black on white, white on black) for stamps, embroidery, and laser engraving |
| **Responsive Lockups** | Single fixed composition that breaks when used as a square app icon or wide website header | Complete lockup system: Primary horizontal lockup, stacked vertical lockup, icon-only mark, and 16px micro favicon |
| **Color & Font Systems** | Arbitrary hex colors with no print support; hallucinated unlicenseable fonts | Precise color specs (HEX, RGB, CMYK) + accessible contrast scores + commercially licensed open typography pairings |
| **Legal & Trademark** | Completely blind to trademark infringement; risks expensive Cease & Desist letters | Integrated preliminary trademark conflict screening protocol (identifying visual and phonetic conflicts early) |

### Concept Evolution Comparison

```mermaid
flowchart TD
    subgraph AdHoc["❌ Ad-Hoc Generative Approach"]
        A1[Idea: 'Fintech Logo'] --> B1[Single Midjourney Prompt]
        B1 --> C1[3D Glossy Raster Graphic: Unusable for Vector / Unscalable]
    end

    subgraph Disciplined["✅ Logo Identity Designer Workflow"]
        A2[Idea: 'Fintech Logo'] --> B2[Brief Intake & Cliché Filter (No Generic Shields/Coins)]
        B2 --> C2[3 Differentiated Concept Territories]
        C2 --> D2[Evaluation Matrix (Scalability, Legibility, Monochrome)]
        D2 --> E2[Vector Construction & Responsive Lockup Hierarchy]
        E2 --> F2[Production Delivery: SVG Master + Spec Sheet + Palette + Fonts]
    end
```

---

## ✨ Features

- **Six Adaptive Creative Modes:** Automatically adapts workflow depth to project scope:
  - `minimal`: Fast ideation for early prototypes and side projects.
  - `detailed` *(default)*: Standard commercial brand identity package.
  - `creative-exploratory`: High-differentiation exploratory work for fashion, music, and cultural brands.
  - `corporate`: Institutional, regulated, and B2B brand design systems.
  - `vintage`: Heritage, craft, artisanal, and nostalgic emblem aesthetics.
  - `tech-startup`: App-first, developer tool, SaaS, and AI product branding.
- **Objective Evaluation Matrix:** Scores concepts (1–10) on strategic fit, distinctiveness, legibility, scalability, monochrome reproduction, and app-icon adaptability.
- **Production Delivery Spec:** Defines viewBox specifications, grid systems, clear-space buffers, minimum legible sizes, and color palettes.
- **Trademark Screening Gate:** Preliminary visual and phonetical risk identification before committing to final branding assets.

---

## 📂 Repository Structure

```
logo-identity-designer/
├── SKILL.md                                  # Core identity design workflow, mode selection & QA gates
├── README.md                                 # Documentation & Before/After comparison
└── references/
    ├── mode-presets.md                       # Complete guidelines & worked examples for all 6 creative modes
    ├── production-delivery.md                # Delivery file checklist, SVG specifications & export rules
    └── trademark-screening.md                # Preliminary conflict checks, Nice classification & counsel handoff
```

---

## 🚀 Installation & Setup

### For Google Antigravity (AGY)
Install into your project or global Antigravity skills repository:
```bash
# Workspace level
mkdir -p .agent/skills
cp -r logo-identity-designer .agent/skills/

# Global level
cp -r logo-identity-designer ~/.gemini/skills/
```

### For Claude Code / Claude Desktop
Copy into your Claude skills repository:
```bash
mkdir -p ~/.claude/skills
cp -r logo-identity-designer ~/.claude/skills/
```

---

## 💡 Example Trigger Prompts

- *"I need to design a logo for a developer-focused cybersecurity SaaS called 'CipherShield'. Use the tech-startup mode."*
- *"Develop 3 distinct brand identity concepts for an artisanal sourdough bakery, complete with evaluation scores and vector specs."*
- *"Critique our current app icon design and develop a responsive lockup set for our navigation bar and favicon."*
- *"Create an AI prompt to explore minimalist monograms for an architecture firm, ensuring it works in pure black and white."*

---

## 📄 License

This skill is distributed under the [MIT License](../LICENSE).
