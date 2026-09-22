# Negative Prompt Template

Explicitly prevent common generation failures, but keep the list **targeted**. A huge generic negative list can degrade results, suppress wanted detail, or push the style toward blandness. Start from the base list, then add character-specific risks identified in `workflows/artifact-control.md`.

## Contents
1. Base negative list
2. Character-specific additions
3. Compact copy-paste version
4. For models without negative prompts

---

## 1. Base negative list (grouped)

**Hands and limbs**
extra fingers, missing fingers, fused fingers, malformed hands, broken limbs, impossible joints, disconnected limbs

**Face**
asymmetrical eyes, low-resolution facial details, distorted face

**Costume and objects**
duplicated accessories, duplicated objects, floating ornaments, disconnected clothing, melted fabric, inconsistent costume colors

**Hair**
tangled hair, spaghetti hair, random disconnected strands

**Rendering**
excessive bloom, excessive sharpening, plastic skin, noisy background, over-detailed background competing with character

**Unwanted content**
accidental text, watermark, logo, random symbols

**Composition**
inconsistent perspective, cropped head, cropped feet (only if full-body)

---

## 2. Character-specific additions

Add only what this character actually risks. Examples:

| Character trait | Likely failure | Add |
|---|---|---|
| Deliberately asymmetrical costume | Generator symmetrizes it | Prefer positive reinforcement; optionally `symmetrical sleeves` |
| Single distinctive headpiece | Duplicated or merged into hair | `duplicate headpiece, second circlet` |
| Long trailing ribbons | Ribbons detached or tangled | `detached ribbons, tangled ribbons` |
| Held weapon or staff | Merges with hand | `weapon fused with hand, extra weapon` |
| Translucent layered fabric | Melted, muddy layers | `melted fabric, muddy layers` |
| Cool-toned palette | Warm color drift | `warm color cast` |
| Gold metallic details | Turns yellow plastic | `plastic gold, flat yellow metal` |

---

## 3. Compact copy-paste version

```
extra fingers, missing fingers, fused fingers, malformed hands, broken limbs, impossible joints, asymmetrical eyes, duplicated accessories, floating ornaments, disconnected clothing, melted fabric, tangled hair, inconsistent costume colors, excessive bloom, excessive sharpening, plastic skin, noisy background, cluttered background, text, watermark, logo, low-resolution face, duplicated objects, inconsistent perspective
```

Append character-specific terms to the end.

---

## 4. For models without negative prompts

Many natural-language image models handle negation poorly and may even render the thing you named. Convert the list into **positive constraints** in the QUALITY CONTROL section instead:

| Negative | Positive equivalent |
|---|---|
| extra / missing / fused fingers | "each hand has exactly five distinct fingers" |
| asymmetrical eyes | "both eyes matching in size, shape, and color" |
| duplicated accessories | "a single circlet, one pair of earrings" |
| floating ornaments | "every ornament physically attached to the garment" |
| plastic skin | "natural skin with soft shading and subtle texture" |
| noisy background | "clean, uncluttered background with low contrast behind the character" |
| text / watermark / logo | "no text or markings anywhere in the image" |
| melted fabric | "fabric folds clearly defined with distinct layers" |

For Midjourney, use `--no` with a short list of the highest-risk items (roughly 5–8 terms), not the full base list.
