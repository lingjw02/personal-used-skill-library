# Costume Analysis

Break the costume into layers so the prompt describes *construction*, not just "a fantasy dress." Generic clothing words let the generator substitute its default idea of that garment, which is where most costume drift comes from.

## Contents
1. Layer decomposition
2. Per-component attributes
3. Relationships between components
4. Writing costume prompt text
5. Simplification rules

---

## 1. Layer decomposition

Work from the body outward. Skip layers that don't exist; add layers when the design has them.

1. Base garment (bodysuit, undershirt, slip)
2. Corset / bodice / vest
3. Skirt (or trousers)
4. Sleeves
5. Cape / cloak / overcoat
6. Legwear (stockings, thigh-highs, leggings, boots' upper)
7. Shoes
8. Jewelry (necklace, earrings, bracelets, circlet)
9. Decorative symbols (emblems, crests, embroidery motifs)

Layering order matters: which garment sits over which, what is visible at the overlap, and where a layer ends is part of the design.

---

## 2. Per-component attributes

For every **major** component record:

- **Shape**: cut, length, volume, hem style
- **Material**: see `reference-analysis.md` §4
- **Color**: specific color, with role (primary/secondary/accent)
- **Trim**: edging, piping, lace border, contrasting hem
- **Pattern**: stripes, floral, geometric, gradient
- **Ornament**: buttons, buckles, gems, bows, chains
- **Symmetry / asymmetry**: mirrored or deliberately uneven
- **Relationship**: how it connects to neighbors (laced to the bodice, clipped to the cape, tucked under the belt)

Minor components get a line, not a full record.

---

## 3. Relationships between components

Distinctive costumes are usually defined by how parts interact, not by any single part:

- A cape fastened by a brooch at one shoulder only
- Detached sleeves connected by ribbon to the bodice
- A skirt whose front layer is shorter than the back
- A corset lacing that matches the ribbon color on the boots

Record these connections explicitly. They tend to be lost first when the pose changes.

---

## 4. Writing costume prompt text

Prefer construction language:

- Weak: "elegant white and gold dress"
- Strong: "fitted ivory satin bodice with gold-piped sweetheart neckline, laced at the front with a thin gold cord; layered chiffon skirt in three tiers with a scalloped hem, shorter at the front"

Order the description top-down or inside-out consistently so the generator reads it as one coherent outfit. Keep each garment's material, color, and trim together in one clause rather than scattering "gold" and "satin" across the prompt.

---

## 5. Simplification rules

Prompts have finite capacity, and over-specifying hurts more than it helps.

- Full detail: Tier 1 and Tier 2 components (silhouette-defining garments, signature accessories).
- Compressed: Tier 3 (write "fine gold embroidery along the hem," not each motif).
- Omit: anything so small it won't be visible at the target framing (a bust shot doesn't need boot buckles).
- If the reference's costume is too complex to render cleanly, keep the **silhouette and color blocking** and simplify the internal ornament. A clean, recognizable simplification beats a noisy attempt at everything.
