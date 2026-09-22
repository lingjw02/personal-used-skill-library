---
name: character-illustration-reverse-engineer
description: Reverse-engineer a reference character image (anime, fantasy, game, OC, fan art, character sheet) into a structured design specification and a high-fidelity image-generation prompt that preserves the character's identity, silhouette, costume, palette, and signature motifs while upgrading anatomy, composition, lighting, and environment. Use this skill whenever the user uploads or describes a character image and wants it redrawn, polished, re-posed, put in a new scene, turned into a prompt (Midjourney, Stable Diffusion, NovelAI, Flux, DALL-E, etc.), or kept "consistent" across new artwork, even if they never say "reverse engineer" or "specification". Also use for requests like "make this character look more professional", "same character, new scene", "write a prompt for this OC", "analyze this character design", or "image to prompt" for illustrated characters. Not for photorealistic portraits, logos, or non-character art.
---

# Character Illustration Reverse Engineering

Turn a reference character image into a structured visual specification, then into a generation prompt for a **new, more polished illustration of the same character**.

The reference is a **design source**, not a prompt. A caption-style description ("girl with long blue hair in a white dress") throws away the information that makes a character recognizable: the exact silhouette, which details are load-bearing, how the costume is layered, what the palette temperature is. This skill exists to keep that information alive through the rewrite.

The goal is *not* to copy the original composition. The goal is that the result feels like **"the same character in a new premium artwork"**, never **"a different character inspired by the reference."**

## Pipeline

```
REFERENCE → OBSERVE → DECOMPOSE → IDENTIFY → PRIORITIZE
          → RECONSTRUCT → COMPOSE → RENDER → VERIFY → CORRECT
```

Never jump straight from image to prompt. Work through the stages below, reading the linked file for each stage when you reach it.

| Stage | What you do | Read |
|---|---|---|
| 1. Observe | Extract identity, silhouette, palette, materials from the reference. Flag anything unclear. | `workflows/reference-analysis.md` |
| 2. Identify | Find the motifs that make the character recognizable; build the Critical Identity List; rank everything by tier. | `workflows/character-identity.md` |
| 3. Decompose | Break the costume into layers with shape/material/color/trim per layer. | `workflows/costume-analysis.md` |
| 4. Reconstruct | Design a new pose, camera, framing, environment, and depth. | `workflows/composition.md` |
| 5. Light | Define key/fill/rim/ambient/accent lighting before rendering. | `workflows/lighting.md` |
| 6. Write | Fill the profile, then build the prompt and negative prompt. | `templates/character-profile.md`, `templates/image-prompt.md`, `templates/negative-prompt.md` |
| 7. Verify | Anatomy, hair, cloth physics, and the final self-check. Revise before delivering. | `workflows/artifact-control.md` |

For a worked example of the whole flow, read the one closest to the request: `examples/anime-character.md` (stylized/cute, upper-body or bust), `examples/fantasy-character.md` (ornate costume, magical atmosphere), `examples/full-body-illustration.md` (full-figure framing, footroom, pose-heavy).

You do not need to read every file for every request. A quick "just give me a prompt for this character" needs the analysis files and the templates; a "fix why my generations keep breaking the hands" request needs mostly `artifact-control.md` and `negative-prompt.md`.

## Getting the reference

- If an image is in the conversation, look at it directly. If only a file path under `/mnt/user-data/uploads/` is listed, open the image first.
- If there are several images (front/back views, expression sheet, costume variants), treat them as one character: use every view to resolve details hidden in any single one, and note conflicts between them instead of silently picking one.
- If there is no image and only a text description, run the same pipeline but say plainly that the profile is built from description, so more features are "assumed" rather than "observed."
- If a feature is unclear (hidden by pose, blurred, cropped), **mark it uncertain** rather than inventing it. Invented details become false "identity" that later generations then faithfully reproduce.

## Design hierarchy

Everything you extract gets a tier. The tiers decide what the generation is allowed to change.

- **Tier 1 — MUST preserve.** Character identity and silhouette-defining elements: face type, eye color, hair color/length/style, signature accessories, overall body and costume silhouette.
- **Tier 2 — SHOULD preserve.** Major costume structure, palette, important accessories, material character.
- **Tier 3 — CAN reinterpret.** Small decorative details, minor folds, secondary ornaments.
- **Tier 4 — CAN change freely.** Background, environment, camera angle, lighting, atmospheric effects, secondary composition.

Test: the result must stay recognizable even if every Tier 4 element changes dramatically. When prompt space is tight, cut from the bottom tier upward, never the reverse.

## Adaptation rule

When the user asks for a specific scene, mood, or pose:

- **Preserve:** identity, hairstyle, costume identity, important accessories, color language, signature motifs.
- **Adapt:** pose, camera, environment, lighting, atmosphere, composition.

## What to deliver

Build the full Reference Profile (`templates/character-profile.md`) internally as your working analysis. Then deliver, by default:

1. **Critical Identity List** (3–8 features) and any **uncertain features**, so the user can correct a misread before spending generations on it.
2. **The generation prompt**, in the sixteen-section structure from `templates/image-prompt.md`, adapted to the target model if the user named one.
3. **The negative prompt** (or positive-phrased equivalents for models that don't support negatives).
4. **A one-line summary of what changed vs. the reference** (pose, camera, environment, lighting) so the user knows the departures were deliberate.

Show the full Reference Profile only if the user asks for it or wants to edit it. Don't dump internal reasoning by default; it's your scaffolding, not the deliverable.

If an image-generation tool is available in the session, pass the final prompt to it and then check the output against the self-check in `workflows/artifact-control.md`, iterating on the prompt if a critical element fails. If none is available, say so and hand the user the prompt to run in their generator of choice. Do not pretend to have generated an image.

## Principles behind the rules

- **Describe, don't name.** Write the visual features of the character rather than relying on the character's or franchise's name. Names invite the generator to substitute its own memory of the character for the reference you actually analyzed, and they make the prompt useless if the model doesn't know the character.
- **Every quality word must map to something visible.** "Refined linework," "soft rim light on the hair edge," "satin sheen on the bodice" are useful. Repeating "ultra detailed, masterpiece, 8k" is noise that also tends to flatten the style.
- **Silhouette before decoration.** Recognition comes from shape first. Spend prompt budget on the sleeve shape and hair mass before the third row of embroidery.
- **Material variety sells realism.** Not everything is glossy. Differentiate matte cloth, satin, lace, metal, crystal, skin.
- **Glow needs a source.** Magical light must come from something in the scene, or it becomes uncontrolled bloom.
- **The character is the focal point.** Environment supports the character's theme and palette; it never competes.
