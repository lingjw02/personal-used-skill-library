# HoloSticker: 2.5D Anime Character Card Generator

> **AI Skill (v2.1)**: Transform any anime character illustration into a premium 2.5D collectible trading card (HoloSticker style) with theme-aware custom framing, holographic foil effects, rarity tiers, and an integrated info panel.

---

## 📌 Overview

**HoloSticker** transforms single-character anime illustrations into luxury collectible cards (角色卡 / 立绘卡 / 全息卡). Rather than simply pasting an illustration into a static generic template, this skill designs a bespoke, theme-integrated trading card where:

$$\text{Character} + \text{Theme} + \text{Frame} + \text{Rarity} + \text{Depth} + \text{Holographic Effects} + \text{Typography} = \mathbf{One\ Unified\ Collectible}$$

---

## ✨ Key Features

### 1. 🌟 2.5D Layered Depth Illusion
Simulates dimensional depth and card parallax using a 10-tier optical stack:
- `DEPTH_01` Background atmosphere & gradient
- `DEPTH_02` Graphic backdrop symbols & runes
- `DEPTH_03` Rear ambient particles
- `DEPTH_04` Rear hair strands & back accessories
- `DEPTH_05` Character torso & body
- `DEPTH_06` Character face & expressions
- `DEPTH_07` Front hair & bangs
- `DEPTH_08` Foreground props, weapons, and hands (*can break the frame*)
- `DEPTH_09` Front sparkles & light bursts
- `DEPTH_10` Card glass surface & holographic foil overlay

### 2. 🎴 Dynamic Theme-Aware Frame Generator
Frames are automatically custom-engineered to match the character's aesthetic:
- **Fantasy**: Ornamental metal, arcane glyphs, luminous crystal facets.
- **Cyberpunk**: Holographic HUD glass, neon lines, scanlines, digital glitch accents.
- **Royal**: Filigree gold borders, crest medallions, polished gemstone inlays.
- **Dark / Gothic**: Black ironwork, obsidian textures, subtle crimson luminescence.
- **Idol / Pop**: Penlight glow rings, confetti haze, pastel neon borders, star cutouts.
- **Military / Tactical**: Brushed steel plates, hex bolts, stenciled unit emblems.
- **Traditional / Hanfu-Kimono**: Lacquered wood-grain, cloud lattice motifs, ink wash edges.
- **Aquatic / Mermaid**: Water-caustic patterns, pearlescent inlays, bioluminescent sea glow.

### 3. 💎 Rarity Tier System (RARITY_TIER)
Mirrors trading card game tiers to scale visual richness:

| Tier | Name | Frame Design | Holographic & Particle Intensity | Material |
|:---:|:---:|:---|:---|:---|
| **N** | Normal | Clean single-line border | Subtle surface sheen | Matte |
| **R** | Rare | Double-line border with corner studs | Light holographic sheen on frame | Semi-gloss |
| **SR** | Super Rare | Full themed ornamentation | Foil gradients + moderate background aura | Glossy metallic |
| **SSR** | Secret Super Rare | Maximal ornamentation, elements breaking the border | Full prismatic foil across frame & background, chromatic flares | Iridescent crystal |

### 4. 🌈 Holographic Effect Library (EFFECT_STYLE)
- `RAINBOW_FOIL`: Full-spectrum iridescent sheen across diagonal light bands.
- `PRISM_HOLO`: Sharp crystal facets sweeping across the surface.
- `STARDUST`: Fine celestial glitter concentrated around silhouettes and borders.
- `GLITCH_FOIL`: Subtle chromatic aberration scanlines and tech displacement.
- `PEARL_SHEEN`: Soft, elegant pearlescent low-contrast shimmer.
- `AQUA_RIPPLE`: Caustic refractive water-wave reflections.

### 5. 📜 Integrated Lower-Third Information Panel
- Occupies roughly the lower 30% (68%–95% height).
- Styled to theme (frosted glass, HUD overlay, parchment, or metallic plate).
- Features:
  - **Character Name & Title** in theme-matched typography.
  - **Concise Introduction**: 25–60 characters capturing personality, role, and visual theme.
  - **Rarity Badge**: Styled emblem (gem, star cluster, or wax seal).
  - **Signature Edition (Optional)**: Flowing handwritten autograph or themed seal stamp (印章) in the bottom corner.

---

## 📂 File Structure

```
holosticker-2-5d-character-card/
├── SKILL.md                          # Skill definition (v2.1 specification)
├── README.md                         # Skill documentation and design reference
└── assets/
    └── sample-character.jpg          # Sample input character (Knight OC)
```

---

## 🖼️ Sample Input Reference

A sample character image is provided in [`assets/sample-character.jpg`](assets/sample-character.jpg):
- **Character**: Red-haired female knight in steel plate armor and pleated skirt at castle sunset.
- **Inferred Tier**: `SR` or `SSR`.
- **Recommended Theme**: Royal / Fantasy Knight with gold/silver filigree frame, warm sunset rim lighting, and subtle `STARDUST` or `RAINBOW_FOIL` treatment.

---

## 💡 How to Use

### In Agent Environments (Antigravity, Claude Code, Cursor)
Drop this skill into your skills folder. The skill activates automatically on phrases like:
- *"Turn this character into a card"*
- *"Make a collectible trading card for my OC"*
- *"角色卡"* / *"立绘卡"* / *"全息卡"*
- *"Generate an SSR signature-edition card for this character"*

### Standalone Usage
Use the guidelines in [`SKILL.md`](SKILL.md) to structure image prompts, compositing instructions, or UI card components in Photoshop, Figma, or Stable Diffusion/Midjourney.
