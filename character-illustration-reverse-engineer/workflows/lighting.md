# Lighting Design

Define lighting **before** rendering. Uncontrolled lighting is the fastest way to lose the character's palette and to introduce glow, bloom, and muddy shading. Lighting is a Tier 4 element: you may change it freely as long as Tier 1 and Tier 2 colors still read correctly.

## Contents
1. The five lights
2. Rules
3. Lighting recipes
4. How lighting interacts with materials and palette

---

## 1. The five lights

Specify each one that matters. Not every image needs all five, but the key and rim almost always do.

| Light | Role | Specify |
|---|---|---|
| **KEY** | Main illumination | Direction, color, softness (e.g., "warm golden sunlight from upper left, soft") |
| **FILL** | Lifts shadows | Color, strength (e.g., "cool ambient sky fill, low intensity") |
| **RIM** | Separates character from background | Side, color (e.g., "pale cyan rim light along the hair and right shoulder") |
| **AMBIENT** | Environmental color cast | Overall tone the scene puts on everything |
| **ACCENT** | Highlights important costume or magical elements | What it hits (e.g., "faint glow on the gemstone and circlet") |

---

## 2. Rules

- **One consistent direction.** All highlights and shadows must agree with the key light. Mixed directions read as pasted-together.
- **Glow needs a source.** Every glow (magic, lanterns, moonlight, crystals) must correspond to a visible or clearly implied source. Otherwise you get free-floating bloom.
- **Avoid uncontrolled glow.** State limits: "subtle glow, no lens bloom, no overexposed halo."
- **Keep the palette intact.** Colored lighting tints materials; check that the primary and accent colors from the reference still read. If a blue moonlight would turn a crimson cape purple, either soften the light or say "cape remains deep crimson."
- **Rim light protects the silhouette.** A thin rim on hair and shoulders keeps the outline readable against darker environments.
- **Face stays readable.** Even with dramatic light, the face needs enough illumination for eyes and expression to remain clear.

---

## 3. Lighting recipes

Use as starting points, then adapt to the reference's color temperature.

- **Golden hour**: warm key from low side angle, cool blue-lavender fill from sky, warm-peach rim on hair, soft long shadows.
- **Moonlit fantasy**: cool pale-blue key from above and behind, faint warm fill from a lantern or candle nearby, silver rim light, a small accent glow on magical elements.
- **Soft studio / character-sheet**: broad soft key from front-left, gentle fill from the right, minimal rim, neutral ambient. Good for clean costume readability.
- **Interior warm**: window key light with visible directionality, warm ambient bounce, dust motes catching accent light.
- **Overcast**: very soft key, low contrast, gentle cool ambient, subtle rim from sky. Good for pastel palettes.

---

## 4. Lighting interacting with materials and palette

- Satin: broad, soft, elongated highlights along folds.
- Metal: small, sharp specular highlights and reflected color from the environment.
- Translucent fabric: backlit, lighter and warmer where light passes through, with visible layering.
- Matte cloth: minimal highlights, soft gradient shading.
- Crystal / glass: crisp highlights, internal glow or refraction hints.
- Skin: soft, natural shading with a subtle warm bounce; avoid plastic sheen (see `artifact-control.md`).
- Hair: highlight band following the hair's curvature, colored by the key, with the rim defining the edge.

Keep the palette temperature consistent with the reference unless the user explicitly asks for a mood change.
