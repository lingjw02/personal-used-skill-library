# Reference Analysis

Inspect the reference before writing anything. This file covers four extraction passes: **observation, silhouette, color language, material behavior**. Identity motifs and hierarchy are in `character-identity.md`; costume layering is in `costume-analysis.md`.

## Contents
1. Observation pass
2. Silhouette analysis
3. Color language
4. Material analysis
5. Handling uncertainty

---

## 1. Observation pass

Extract only what you can actually see.

**Character basics**
- Apparent age category (child / teen / young adult / adult / elder)
- Gender presentation
- Body proportions (head-to-body ratio, stylization level: chibi, 6-head, 8-head, realistic)

**Face**
- Face shape (round, oval, angular, soft-jaw)
- Eye shape (large round, sharp/narrow, downturned, upturned), eye color, iris detail (gradient, highlights, pupil style)
- Eyebrow shape and color
- Facial expression
- Distinctive features (beauty mark, scar, blush marks, fang, freckles)

**Hair**
- Color (and gradient/highlight color if present), length, overall style
- Bangs type (blunt, side-swept, parted, hime cut)
- Hair ornaments (position matters as much as type)
- Special strands (ahoge, sidelocks, twin tails, braids)

Do not invent unnecessary identity traits. A plain feature stays plain.

---

## 2. Silhouette analysis

Squint at the image, or imagine it as a flat black shape. Record the outline of:

- Overall body silhouette (narrow, A-line, top-heavy, wide)
- Hair silhouette (volume, where it extends, twin-tail spread)
- Sleeves (fitted, bell, detached, oversized)
- Skirt (A-line, layered, tiered, asymmetrical hem)
- Cape/cloak (length, spread, attachment point)
- Ribbons and trailing elements
- Weapon or held accessory
- Major asymmetrical elements (one long sleeve, single pauldron, off-center ornament)

Then decide which of these are **essential to recognition**. Silhouette-defining elements outrank tiny decorative ones. Asymmetry is especially valuable: it's often the character's signature and the thing a generator most easily "corrects" into symmetry, so it needs explicit protection in the prompt.

---

## 3. Color language

Classify the palette:

| Role | Meaning |
|---|---|
| PRIMARY | The dominant character color |
| SECONDARY | Supporting costume colors |
| ACCENT | Small high-contrast colors that pull the eye |
| METALLIC | Gold / silver / bronze elements |
| LIGHT | Colors produced by illumination (glow, magic), not by materials |

Rules:
- Note the overall **color temperature** (warm, cool, neutral) and preserve it. Warm-to-cool drift is one of the most common ways a redraw stops feeling like the same character.
- Do not over-saturate. Generators tend to push saturation upward; describe colors with restraint ("muted lavender," "desaturated teal") when the reference is soft.
- Use specific color words over generic ones (crimson vs. red, ivory vs. white) when the reference supports it.
- Keep LIGHT colors separate from material colors so an emissive glow isn't mistaken for a fabric dye.

---

## 4. Material analysis

Identify the material of every major surface, then its behavior:

- **Roughness**: matte ↔ glossy
- **Reflectivity**: how sharp are the highlights
- **Translucency**: does light pass through (chiffon, glass, crystal)
- **Fold behavior**: stiff creases vs. soft drape vs. flowing
- **Highlight behavior**: broad soft sheen (satin) vs. small hard specular (metal, jewels)
- **Edge softness**: crisp (leather, metal) vs. feathered (tulle, fur)

Common materials: satin, silk, translucent fabric, lace, leather, metal, crystal, glass, embroidered fabric, matte cloth, glossy ornament.

Avoid rendering every surface with the same glossy finish. A single "shiny" instruction applied globally is the usual cause of plastic-looking costumes.

---

## 5. Handling uncertainty

Keep a running **Uncertain** list. For each item, write what is unclear and why (cropped, hidden by hair, low resolution, conflicting views). Then choose one of:

- **Leave neutral**: omit from the prompt so the generator doesn't hallucinate a specific answer.
- **Choose conservatively**: pick the simplest plausible option and flag it as an assumption to the user.
- **Ask**: if the uncertain feature is Tier 1 (e.g., you cannot tell the eye color and it's a defining feature), ask the user.

Never resolve uncertainty by picking the more interesting option.
