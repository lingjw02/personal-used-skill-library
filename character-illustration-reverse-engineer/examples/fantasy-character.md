# Example: Fantasy Character (ornate costume, magical atmosphere)

An original character. The "reference" is summarized as the result of observation.

**User request:** "Redraw this moon priestess as a premium illustration in a ruined moonlit temple. I'll use a natural-language image model."

---

## Reference observation (summary)

- Adult woman, tall, graceful, ~8-head proportions
- Very long straight silver-white hair to below the hips; blunt bangs; two thin braided sidelocks
- Narrow, calm violet eyes; serene expression
- **Silver crescent circlet at the center of the forehead with a teardrop moonstone**
- Costume: fitted deep-navy bodice with silver piping and front lacing; layered skirt in navy and translucent pale-blue chiffon, longer at the back; **long bell-shaped left sleeve in translucent chiffon reaching the knee; short fitted right sleeve with a silver bracer**; cape in dark indigo fastened at the **left shoulder only** with a crescent brooch
- Palette: navy primary; silver metallic; pale blue secondary; cold violet accent in eyes and moonstone; overall cool
- Reference pose: standing, holding a staff in the right hand, rigid front view

**Uncertain:** whether the staff top is a moon or a star (blurred). Decision: describe as "a small glowing crescent-shaped staff head" and flag it.

## Critical Identity List

1. Silver crescent circlet with a teardrop moonstone at center forehead
2. Very long straight silver-white hair, blunt bangs, two braided sidelocks
3. **Asymmetric sleeves:** long translucent bell sleeve on the left, short fitted sleeve with silver bracer on the right
4. Indigo cape fastened at the left shoulder only, with a crescent brooch
5. Navy / silver / pale-blue cool palette with violet accents
6. Layered skirt, translucent chiffon over navy, longer at the back

## Tier notes

- Tier 1: items 1–3, 5
- Tier 2: item 4, 6, bodice lacing, staff
- Tier 3: piping pattern, braid detail
- Tier 4: pose, environment, lighting, atmosphere

Asymmetry is the risk: a generator will likely give two matching sleeves. Reinforce it in both COSTUME and DISTINCTIVE MOTIFS.

## What changes vs. reference

Rigid front pose → three-quarter body turned slightly left, staff planted, the free left sleeve lifting with a gentle breeze so the asymmetry is clearly visible. Plain background → moonlit ruined temple. Cold, flat light → cool moonlight key with a magical glow sourced from the staff and moonstone.

## Delivered prompt (structured natural language)

```
CHARACTER: An adult woman, tall and graceful, serene and composed, a moon priestess.
Critical identity: silver crescent circlet with a teardrop moonstone at the center of her forehead; very long straight silver-white hair; asymmetric sleeves (long translucent left bell sleeve, short fitted right sleeve with a silver bracer); indigo cape fastened at the left shoulder only with a crescent brooch; cool navy, silver, and pale-blue palette with violet accents.

HAIR: Very long, straight silver-white hair falling below the hips as one smooth mass, blunt bangs, two thin braided sidelocks framing the face, a few loose strands catching moonlight.

FACE: Oval face, narrow calm violet eyes, soft brows, serene expression.

BODY: Elegant 8-head proportions, upright posture.

COSTUME: Fitted deep-navy bodice with silver piping and a front lacing of thin silver cord; layered skirt of deep-navy fabric under translucent pale-blue chiffon, longer at the back; LEFT sleeve long and bell-shaped in translucent pale-blue chiffon reaching the knee; RIGHT sleeve short and fitted with a silver bracer at the forearm; dark indigo cape attached at the left shoulder only by a silver crescent brooch.

DISTINCTIVE MOTIFS: Silver crescent circlet with a teardrop moonstone (one circlet only); the deliberate asymmetry of the sleeves and single-shoulder cape.

POSE: Three-quarter body turned slightly to her left, weight on the right leg, left knee softly bent; right hand holding a slender staff with a small glowing crescent head planted beside her; left arm lifted slightly so the long chiffon sleeve drifts outward.

EXPRESSION: Calm, serene, gaze directed slightly off-camera toward the moon.

CAMERA: Full-body, slight low angle, eye level at her waist, feet visible.

COMPOSITION: Character centered slightly right, generous headroom and footroom, clear silhouette against a darker background, foreground stone arch softly out of focus at the frame edge.

ENVIRONMENT: A ruined moonlit temple courtyard with broken pillars and moss-covered steps, kept low-contrast and slightly hazy so the character reads first.

LIGHTING: Key: cool pale-blue moonlight from upper left behind her; Fill: faint violet ambient; Rim: silver rim light along hair and cape edge; Accent: soft glow from the staff head and the moonstone, illuminating nearby fabric only.

MATERIALS: Satin sheen on bodice, translucent chiffon layering visible with light passing through, small sharp highlights on silver, matte indigo cape with heavy soft folds, natural skin with soft shading.

ATMOSPHERE: A few drifting motes of moonlit dust and a low mist near the ground, all lit by the moon.

RENDERING STYLE: Highly detailed anime illustration, refined linework, controlled cel shading blended with soft gradients, coherent depth of field, professional character-art finish.

QUALITY CONTROL: Exactly five fingers on each hand, matching eyes, a single circlet, every ornament attached, cape flowing in the same wind direction as hair and sleeve, palette stays cool.
```

**Positive constraints replace the negative prompt** (natural-language model): the QUALITY CONTROL section carries them. If the user's model supports negatives, append: `duplicate circlet, two matching sleeves, symmetrical sleeves, warm color cast, floating ornaments, melted fabric, text, watermark`.

**Note to user:** I couldn't tell whether the staff head is a moon or a star in your reference, so I wrote a small glowing crescent; tell me if it should be different.
