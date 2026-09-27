# 🎨 Personal AI Agent Skills Library & Visual Production Suite

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Skills-4285F4?logo=google&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![Claude Compatible](https://img.shields.io/badge/Claude-Code%20%26%20Desktop-D97757?logo=anthropic&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![GitHub Repository](https://img.shields.io/badge/GitHub-lingjw02%2Fpersonal--used--skill--library-181717?logo=github&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A curated suite of specialized **AI Agent Skills** and structured prompt engineering systems designed for anime character illustration, concept art decompilation, Live2D Cubism rigging preparation, collectible trading cards, precision 3D orthographic technical sheets, UI/UX motion design, brand identity, and automated QA verification.

Compatible with **Google Antigravity**, **Claude Code**, **Claude Desktop**, **Cursor**, and leading image generation platforms (**Midjourney**, **Flux**, **Stable Diffusion**, **DALL-E 3**).

---

## 🧭 Skills Catalog

| Skill Folder | Description | Primary Deliverables | Target Tools & Workflows |
|---|---|---|---|
| [**`anime-wallpaper-prompt-design`**](./anime-wallpaper-prompt-design/) | Anime character wallpaper & illustration prompt engineering (NovelAI, SDXL, FLUX, Midjourney Niji) with safe zones. | Tuned prompt + Danbooru tags + parameters + safe-zone composition plan | NovelAI, SDXL/ComfyUI, Flux, Midjourney Niji, Mobile/Desktop Wallpaper |
| [**`character-breakdown-sheet-generator`**](./character-breakdown-sheet-generator/) | Generates character model sheets, turnaround views (front/side/back), and decomposed layer callouts. | Structured prompt + layout plan + consistency controls | Midjourney, SDXL, Flux, 3D Modeler handoff |
| [**`character-illustration-reverse-engineer`**](./character-illustration-reverse-engineer/) | Deconstructs character artwork into design specs and high-fidelity generation prompts preserving character DNA. | 16-section generation prompt + Critical Identity List | Midjourney v6, SD/Pony, Flux, Concept Art |
| [**`character-reference-sheet`**](./character-reference-sheet/) | Generates clean, reusable character reference sheets from source art to maintain visual consistency for fan art & outfits. | Identity-extracted prompt + silhouette & turnaround guide | Midjourney, SD/Pony, Flux, Concept Art, Model Sheets |
| [**`frontend-motion-icon-design`**](./frontend-motion-icon-design/) | Senior UI/UX motion design, micro-interactions, loading states, and accessible icon systems (WCAG). | Motion guidelines + SVG/icon systems + framework code | Web, React, Vue, CSS, Lottie, UI/UX Design |
| [**`holosticker-2-5d-character-card`**](./holosticker-2-5d-character-card/) | Transforms character art into luxury 2.5D collectible cards (HoloSticker) with theme-aware frames & foil effects. | 2.5D layered design + theme frame + rarity tier (N/R/SR/SSR) | Photoshop, Stable Diffusion, Game UI, Collectibles |
| [**`image-restoration-skill`**](./image-restoration-skill/) | Restores, denoises, deblurs, removes artifacts, and upscales damaged/low-resolution images into HD. | Restoration prompt + defect analysis + HD reconstruction | SD/Flux, Upscalers, Photo & Anime Restoration |
| [**`independent-verification-review`**](./independent-verification-review/) | Three-level independent verification & factual audit protocol (evidence, logic, risk assessment). | Multi-tier review checklist + fact verification report | Quality Assurance, Research, Content Review |
| [**`live2d-asset-prep`**](./live2d-asset-prep/) | Prepares character art for Live2D Cubism rigging: generates layer hierarchies, parameter maps, and assembles PSDs. | Layer blueprint + rigging spec + assembled PSD & QA report | Live2D Cubism, VTubers, Photoshop, Spine |
| [**`logo-identity-designer`**](./logo-identity-designer/) | Complete brand identity design workflow (intake, creative strategy, 3+ concepts, scoring, vector production delivery). | Logo strategy + evaluation scoring + lockups & brand vector delivery spec | Illustrator, SVG, Vector Design, Brand Systems, UI/UX |
| [**`orthographic-view-prompt-generator`**](./orthographic-view-prompt-generator/) | Generates mathematically consistent prompts for CAD-style 3D three-view drawings (front/side/top/isometric). | True orthographic multi-view prompt with dimensions | Midjourney, CAD, 3D Modeling, Product Design |
| [**`readme-writer`**](./readme-writer/) | Generates structured, high-accuracy README and documentation pages tailored to actual project manifests and codebases. | Clean Markdown/MDX documentation + installation guides + usage examples | GitHub, Markdown, Documentation, Open Source Projects |

---

## 🔄 End-to-End Character Production Pipeline

These skills can be used independently or chained together into an end-to-end creative workflow:

```mermaid
flowchart TD
    A[Initial Character Concept / Reference Image] --> B[character-illustration-reverse-engineer]
    B -->|High-Fidelity Prompt & Identity Lock| C[Polished Master Illustration]
    
    C --> D[character-breakdown-sheet-generator]
    C --> E[holosticker-2-5d-character-card]
    
    D -->|Turnaround Views & Layer Breakdowns| F[Production Assets]
    
    F -->|Character & Garment Decomposition| G[live2d-asset-prep]
    F -->|Weapons, Equipment & Hardware Specs| H[orthographic-view-prompt-generator]
    
    G -->|Assembled & Grouped PSD + Rigging Blueprint| I[Live2D Cubism Rigging / VTuber Model]
    H -->|3-View Technical Drawing with Proportions| J[3D Modeling / Blender / CAD]
    E -->|Theme Frame, Holographic Foil & Info Panel| K[Collectible Trading Card / Game UI]
```

---

## 📂 Repository Structure

```
Skills/
├── character-breakdown-sheet-generator/
│   ├── SKILL.md                          # Agent skill specification
│   ├── README.md                         # Detailed documentation & prompt template
│   └── evals_evals.json                  # Test cases and evaluation criteria
│
├── character-illustration-reverse-engineer/
│   ├── SKILL.md                          # Agent skill specification
│   ├── README.md                         # 7-stage pipeline & 4-tier system
│   ├── workflows/                        # Specialized workflow step guides
│   ├── templates/                        # Profile, 16-section prompt & negative prompt
│   └── examples/                         # Worked examples (anime, fantasy, full-body)
│
├── holosticker-2-5d-character-card/
│   ├── SKILL.md                          # Agent skill specification (v2.1)
│   ├── README.md                         # 2.5D layer stack, frame themes & foil effects
│   └── assets/
│       └── sample-character.jpg          # Sample input character
│
├── live2d-asset-prep/
│   ├── SKILL.md                          # Agent skill specification
│   ├── README.md                         # Rigging blueprint & QA guide
│   ├── requirements.txt                  # Python dependencies
│   ├── scripts/                          # Automated PSD assembly & QA testing
│   └── references/                       # Layer hierarchies, parameters & checklists
│
├── orthographic-view-prompt-generator/
│   ├── SKILL.md                          # Agent skill specification
│   ├── README.md                         # CAD projection rules & template
│   └── evals_evals.json                  # Test cases and evaluation scenarios
│
├── packages/                             # Pre-packaged .skill zip archives & consolidated bundle
│   ├── all-skills.zip
│   ├── anime-wallpaper-prompt-design.skill
│   ├── character-breakdown-sheet-generator.skill
│   ├── character-illustration-reverse-engineer.skill
│   ├── character-reference-sheet.skill
│   ├── frontend-motion-icon-design.skill
│   ├── holosticker-2-5d-character-card.skill
│   ├── image-restoration-skill.skill
│   ├── independent-verification-review.skill
│   ├── live2d-asset-prep.skill
│   ├── logo-identity-designer.skill
│   ├── orthographic-view-prompt-generator.skill
│   └── readme-writer.skill
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Installation & Usage

### Option 1: Using with Google Antigravity (AGY)
To use any skill in your Antigravity workflows:
1. Copy the desired skill folder (e.g. `character-breakdown-sheet-generator/`) to your project's skills directory:
   ```bash
   # Workspace-level skills
   mkdir -p .agent/skills
   cp -r character-breakdown-sheet-generator .agent/skills/
   ```
   Or into the global skills directory:
   ```bash
   # Global skills
   cp -r character-breakdown-sheet-generator ~/.gemini/antigravity-cli/builtin/skills/
   ```
2. The skill is automatically discovered and indexed by the agent.

### Option 2: Using with Claude Code / Claude Desktop
1. Clone this repository or copy individual skill folders to your `.claude/skills` directory:
   ```bash
   mkdir -p ~/.claude/skills
   cp -r character-illustration-reverse-engineer ~/.claude/skills/
   ```
2. In chat, activate by uploading an image or asking relevant queries (e.g. *"Break down this character's outfit"* or *"Turn this illustration into a 3-view CAD drawing"*).

### Option 3: Prepackaged `.skill` Archives
If your platform accepts `.skill` package uploads directly, download the ready-to-use zip packages from the [`packages/`](./packages/) directory:
- [`anime-wallpaper-prompt-design.skill`](./packages/anime-wallpaper-prompt-design.skill)
- [`character-breakdown-sheet-generator.skill`](./packages/character-breakdown-sheet-generator.skill)
- [`character-illustration-reverse-engineer.skill`](./packages/character-illustration-reverse-engineer.skill)
- [`character-reference-sheet.skill`](./packages/character-reference-sheet.skill)
- [`frontend-motion-icon-design.skill`](./packages/frontend-motion-icon-design.skill)
- [`holosticker-2-5d-character-card.skill`](./packages/holosticker-2-5d-character-card.skill)
- [`image-restoration-skill.skill`](./packages/image-restoration-skill.skill)
- [`independent-verification-review.skill`](./packages/independent-verification-review.skill)
- [`live2d-asset-prep.skill`](./packages/live2d-asset-prep.skill)
- [`logo-identity-designer.skill`](./packages/logo-identity-designer.skill)
- [`orthographic-view-prompt-generator.skill`](./packages/orthographic-view-prompt-generator.skill)
- [`readme-writer.skill`](./packages/readme-writer.skill)

### Option 4: Standalone / Manual Prompting
All skills contain ready-to-copy prompt structures in their respective `README.md` files that can be pasted directly into:
- **Midjourney** (v6+ recommended)
- **Flux.1** (Dev / Schnell)
- **Stable Diffusion WebUI / ComfyUI**
- **DALL-E 3**

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
