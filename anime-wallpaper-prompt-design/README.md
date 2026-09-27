# 📱 Anime Wallpaper & Illustration Prompt Design

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Skill-4285F4?logo=google&logoColor=white)](https://github.com/)
[![Claude Compatible](https://img.shields.io/badge/Claude-Code%20%26%20Desktop-D97757?logo=anthropic&logoColor=white)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Category: Prompt Engineering](https://img.shields.io/badge/Category-Visual%20Prompt%20Engineering-FF69B4)](SKILL.md)

An engineering-grade prompt design and compilation skill for anime character desktop wallpapers, mobile home screens, lock screens, and standalone character illustrations across **NovelAI**, **SDXL / ComfyUI**, **FLUX.1**, **GPT Image**, and **Midjourney Niji**.

Instead of stacking arbitrary adjectives, this skill decomposes wallpaper generation into independent, controllable variables (safe-zone margins, aspect ratio, camera framing, subject DNA, lighting palette, and model-specific parameters).

---

## ⚖️ Before & After Comparison

| Factor | ❌ Before (Ad-hoc / Naive Prompting) | ✅ After (With `anime-wallpaper-prompt-design`) |
|---|---|---|
| **Prompt Structure** | Adjective soup (`masterpiece, 8k, beautiful anime girl, cute, best quality, wallpaper`) | Modular, orthogonal variable compilation (Subject + Framing + Lighting + Palette + Negative space) |
| **Wallpaper Usability** | Character centered; faces and heads obstructed by mobile clocks; desktop icons obscure main character body | Strict safe-zone enforcement (rule of thirds offset for desktop icons; generous head clearance for mobile lockscreen widgets) |
| **Framing & Cropping** | Full body requests frequently crop feet, ankles, or cut off hair at the top border | Explicit bounding constraint (`full body visible from head to toe, both feet fully inside frame`, zero conflicting zoom keywords) |
| **Model Compatibility** | Same prompt pasted into NovelAI, SDXL, and Midjourney, ignoring syntax and parameter differences | Target-compiled: Danbooru tags for NovelAI, natural language syntax for FLUX/GPT, `--ar --s --c` flags for Midjourney |
| **Multi-Character Scene** | Hair colors, eye colors, and clothing textures bleed together into composite hybrid characters | Decoupled Base Scene + Independent Character Prompt scopes avoiding attribute color leakage |
| **Parameter Tuning** | Blindly cranking CFG/steps to extreme values (`CFG 15`, `steps 100`) causing burned, oversaturated images | Empirically grounded baselines (e.g. NovelAI Guidance 5–6, FLUX 28 steps Guidance 4, SDXL CFG 6–7) |
| **Color Control** | Clashing neon hues caused by stacking `vibrant`, `neon`, `glowing`, `HDR` simultaneously | Defined 3-tier color hierarchy (Dominant primary + Subordinate secondary + Accent pop) |

### Concrete Output Example

#### ❌ Before (Naive Approach)
```text
Prompt: 1girl, anime girl, beautiful face, highly detailed, 8k resolution, best quality, aesthetic, neon cyberpunk city, glowing eyes, wallpaper, 4k desktop wallpaper
Negative: bad anatomy, bad hands, text, error, missing fingers
Result: Character is centered right where desktop shortcut columns sit; legs are cut off below the knees; colors are overblown; prompt ignores model-specific CFG/scheduler settings.
```

#### ✅ After (Skill Engineered - Desktop 16:9 Midjourney Niji)
```text
Prompt: A cybernetic anime archivist standing gracefully, soft bob-cut lavender hair, luminous violet eyes, high-collar tactical techwear coat with matte carbon accents. Positioned in the right third of the frame, three-quarter angle looking towards the left. Left two-thirds features a clean minimalist server monolith interior with soft volumetric cyan haze, creating generous empty negative space for desktop icons. Cinematic rim lighting, muted desaturated palette with neon magenta status LEDs. Clean linework, cel-shaded rendering. --ar 16:9 --niji 6 --style expressive --s 250 --no text, watermarks, desktop icons, cluttered foreground
Result: Perfect icon clearance on the left side; sharp character silhouette on the right; intentional cinematic lighting; zero foot/head cropping.
```

---

## ✨ Features

- **Multi-Model Compilation:** Translates one unified visual concept into the ideal format for NovelAI (Danbooru tags), SDXL/ComfyUI (Pos/Neg tokens), FLUX.1 (natural prose), or Midjourney Niji (parameters & flags).
- **Safe-Zone Engineering:** Calculates exact screen aspect ratios (`16:9`, `21:9`, `9:16`, `19.5:9`) and reserves clean negative space for OS clocks, widgets, and app grids.
- **Color & Light Matrix:** Prevents oversaturation by structuring palettes into Primary, Secondary, and Accent colors.
- **Failure Mode Defense:** Built-in safeguards against attribute color bleeding, limb amputations, distorted perspective, and waxy over-denoising.
- **Curated Example Library:** Includes 14 production-ready, multi-style templates (Anime Cel, Cyberpunk, Watercolor, Chibi, Gothic, Mecha, and Multi-character groups).

---

## 📂 Repository Structure

```
anime-wallpaper-prompt-design/
├── SKILL.md                                  # Core skill instructions & compilation engine
├── README.md                                 # Documentation & Before/After comparison
└── references/
    ├── example-library.md                    # 14 complete, reusable prompt cases (A through N)
    ├── failure-modes.md                      # Diagnosis & fixes for common generation artifacts
    ├── legal-and-qa.md                       # IP guidelines, artist attribution policies & QA checklist
    ├── model-comparison-and-params.md        # CFG, steps, samplers, and schedulers across models
    ├── output-specs-and-composition.md       # Aspect ratios, safe zones & visual variable matrix
    └── prompt-templates.md                   # YAML specification schema & negative prompt blueprints
```

---

## 🚀 Installation & Setup

### For Google Antigravity (AGY)
Drop the skill folder into your workspace or global Antigravity skills directory:
```bash
# Workspace level
mkdir -p .agent/skills
cp -r anime-wallpaper-prompt-design .agent/skills/

# Global level
cp -r anime-wallpaper-prompt-design ~/.gemini/skills/
```

### For Claude Code / Claude Desktop
Copy the skill folder into your Claude skills directory:
```bash
mkdir -p ~/.claude/skills
cp -r anime-wallpaper-prompt-design ~/.claude/skills/
```

---

## 💡 Example Trigger Prompts

Ask your AI assistant:
- *"I need a 4K desktop wallpaper of an anime swordsman using NovelAI, but keep the left side clean for my desktop shortcuts."*
- *"Design a 9:16 lockscreen wallpaper for iPhone 16 Pro featuring an anime sorceress with enough headroom for the lock clock."*
- *"Compile a prompt for FLUX.1 to generate two characters in a library without their hair and outfit colors bleeding into each other."*
- *"My SDXL prompt keeps cutting off the character's feet. How do I fix the framing?"*

---

## 📄 License

This skill is distributed under the [MIT License](../LICENSE).
