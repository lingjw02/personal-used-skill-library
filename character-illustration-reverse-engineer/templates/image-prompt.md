# Image Prompt Template

Build the final prompt from the completed Reference Profile in this **fixed order**. The order gives the prompt a visual hierarchy: identity first (the generator weights early content most), atmosphere and finish last. Do not collapse it into one unstructured paragraph.

## Contents
1. The sixteen sections
2. Skeleton
3. Adapting to the target model
4. Length and budget
5. Common mistakes

---

## 1. The sixteen sections

| # | Section | What goes in it |
|---|---|---|
| 1 | CHARACTER IDENTITY | Age category, gender presentation, build, one-line character summary, and the Critical Identity List items stated up front |
| 2 | HAIR | Color, length, style, bangs, ornaments and their positions, mass/locks/flyaway description |
| 3 | FACE | Face shape, eye shape and color, brows, distinctive features |
| 4 | BODY | Proportions, stylization level, posture baseline |
| 5 | COSTUME | Layer-by-layer construction (see `workflows/costume-analysis.md`) |
| 6 | DISTINCTIVE MOTIFS | Signature accessories, emblems, asymmetry: restate the critical ones here in concrete terms |
| 7 | POSE | Anatomical description of the new pose |
| 8 | EXPRESSION | Specific expression and gaze direction |
| 9 | CAMERA | Shot type, angle, lens feel |
| 10 | COMPOSITION | Framing, headroom/footroom, negative space, focal hierarchy |
| 11 | ENVIRONMENT | Setting that supports the character, kept subordinate |
| 12 | LIGHTING | Key / fill / rim / ambient / accent (see `workflows/lighting.md`) |
| 13 | MATERIALS | Per-surface material behavior |
| 14 | ATMOSPHERE | Particles, haze, weather: each with a visible source |
| 15 | RENDERING STYLE | Linework, shading approach, finish: each term tied to a visible property |
| 16 | QUALITY CONTROL | Positive anatomy/consistency statements (and the negative prompt as a separate block) |

---

## 2. Skeleton

```
[1 CHARACTER IDENTITY]
<age/gender presentation/build>, <one-line summary>.
Critical identity: <feature 1>; <feature 2>; <feature 3>; ...

[2 HAIR]
<color, length, style>, <bangs>, <ornaments + position>, <locks/flyaways>.

[3 FACE]
<face shape>, <eye shape + color + iris detail>, <brows>, <distinctive features>.

[4 BODY]
<proportions, stylization level>.

[5 COSTUME]
<layer 1: shape/material/color/trim>; <layer 2>; ...

[6 DISTINCTIVE MOTIFS]
<signature items, asymmetry, exact placement>.

[7 POSE]
<weight distribution, torso/head orientation, arms, hands, legs>.

[8 EXPRESSION]
<expression + gaze>.

[9 CAMERA]
<shot type, angle>.

[10 COMPOSITION]
<framing, headroom/footroom, focal hierarchy, depth layers>.

[11 ENVIRONMENT]
<setting details supporting theme/palette; lower contrast than character>.

[12 LIGHTING]
Key: ...; Fill: ...; Rim: ...; Ambient: ...; Accent: ...

[13 MATERIALS]
<satin: broad soft sheen; metal: small sharp highlights; ...>

[14 ATMOSPHERE]
<particles/haze with source>.

[15 RENDERING STYLE]
<linework quality, shading method, skin rendering, finish>.

[16 QUALITY CONTROL]
Anatomically correct hands with five fingers each; symmetrical eyes; all costume elements attached and coherent; consistent palette; clean background hierarchy.
```

---

## 3. Adapting to the target model

Ask or infer which generator the user is using; if unknown, deliver the structured natural-language version and offer a condensed one.

- **Natural-language models (DALL·E-style, Flux, Imagen-style, GPT image models):** use the skeleton as written, in full sentences or short clauses. These models follow structure and detail well. Prefer **positive phrasing** ("exactly five fingers on each hand") over negation, since many ignore or invert negatives.
- **Stable Diffusion / NovelAI / tag-based anime models:** convert each section into weighted, comma-separated tags in the same order. Put the Critical Identity tags first. Use the platform's weighting syntax sparingly, only on Critical Identity items. Keep the negative prompt in the dedicated field.
- **Midjourney:** condense to a dense but readable paragraph of roughly 60–120 words, identity first; move exclusions to `--no`; add style/aspect parameters (`--ar`, `--style`, `--s`) as the user's setup requires. Avoid stacking many long clauses; the model drops trailing detail.
- **Unknown or multi-model:** provide the structured version plus a condensed one-paragraph version.

Deliver in a code block so the user can copy it cleanly.

---

## 4. Length and budget

- Aim for the shortest prompt that carries every Tier 1 and Tier 2 item. Long prompts dilute attention; identity items in the last third often get ignored.
- Spend words in proportion to recognition value: hair, silhouette, signature accessory, color blocking first; ornament last.
- If you must cut, cut Tier 4 embellishments and Tier 3 details before touching Tier 1/2.

---

## 5. Common mistakes

- Opening with style/quality words ("masterpiece, ultra detailed") before identity.
- Describing the character by name or franchise instead of by visible features.
- Repeating the same quality word many times.
- Describing a pose abstractly ("dynamic") with no anatomy.
- Putting all glow/atmosphere without a source.
- Omitting asymmetry, so it gets "corrected" to symmetry.
- Letting the environment section outweigh the costume section in length.
