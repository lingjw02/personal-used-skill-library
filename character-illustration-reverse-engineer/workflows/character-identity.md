# Character Identity

This is the step that determines whether the final image reads as *the same character*. It covers **motif extraction, the Critical Identity List, and the design hierarchy**.

## Contents
1. Motif extraction
2. The Critical Identity List
3. Tiering everything
4. Worked check: the "background swap" test

---

## 1. Motif extraction

Find the visual elements a fan would use to recognize the character from across the room. Scan for:

- Unique hair accessory (and where it sits)
- Emblem, crest, or symbol
- Cape or cloak pattern
- Gold/metal ornament with a distinctive shape
- Ribbon arrangement (count, placement, length)
- Unusual sleeve design
- A specific color *combination* (often more identifying than any single color)
- Unique footwear
- Magical symbol or effect
- Companion animal or floating object
- Asymmetry (one glove, one earring, uneven hem)

Ask of each candidate: *if this were removed or changed, would the character still be recognizable?* If yes, it is decoration, not a motif.

---

## 2. The Critical Identity List

Compile **3–8 features** (fewer is better; if everything is critical, nothing is). These MUST survive reconstruction and must be stated explicitly in the prompt, in the most prominent position that section allows.

Write each as a concrete, checkable statement:

- Good: "Silver crescent circlet resting at the center of the forehead, with a single teardrop moonstone."
- Weak: "Fancy headpiece."

- Good: "Left sleeve is long and bell-shaped, reaching below the knee; right sleeve is short and fitted."
- Weak: "Asymmetrical sleeves."

Include at least one silhouette feature, one color feature, and (if present) one signature accessory. Balance is what makes the list actually protective.

---

## 3. Tiering everything

Assign every extracted item to a tier (definitions live in `SKILL.md`):

| Tier | Typical contents |
|---|---|
| 1 — MUST preserve | Face type, eye color, hair color/length/style, signature accessory, overall silhouette |
| 2 — SHOULD preserve | Costume structure, palette, secondary accessories, material character |
| 3 — CAN reinterpret | Small trims, minor folds, tertiary ornaments, fine embroidery |
| 4 — CAN change | Background, environment, camera, lighting, atmosphere |

Use the tiers to allocate prompt space and to resolve conflicts. If the new pose would hide a Tier 1 feature (e.g., a back view hides the front-facing emblem), change the pose, not the feature. If a Tier 3 detail fights with clean rendering, simplify it.

---

## 4. The "background swap" test

Before moving on, imagine the character on a plain white background, then on a completely different environment. Ask:

- Can the character still be identified without the scenery?
- Are the Tier 1 and Tier 2 elements all present in the plan?
- Did any Tier 4 choice (lighting color, camera angle, environment palette) accidentally alter a Tier 1/2 element such as shifting the hair color or washing out an accent?

If any answer is no, fix the plan before writing the prompt.
