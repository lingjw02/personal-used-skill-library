# Example: Anime Character (bust / three-quarter)

An original character used to demonstrate the flow. Since no image can be embedded here, the "reference" is summarized in words, the way you would after Step 1 observation.

**User request:** "Here's my OC. Can you make a nicer version of her standing on a school rooftop at sunset, and give me a prompt for Stable Diffusion?"

---

## Reference observation (summary)

- Teen, slim build, ~6-head anime proportions
- Short chin-length bob, deep teal, blunt bangs; one long **ahoge** curling to the left
- Large round amber eyes with a small star-shaped highlight; soft blush
- School uniform: white sailor blouse, **oversized mustard-yellow cardigan with sleeves past the hands**, navy pleated skirt, red neck ribbon tied loose
- **Round yellow clip on the right side of the bangs**
- Reference pose: stiff, front-facing, arms down; hands hidden in sleeves
- Palette: cool teal + warm yellow contrast, red as small accent; overall soft pastel

**Uncertain:** shoe style (cropped out). Decision: leave shoes unspecified; keep framing three-quarter body so it doesn't matter.

## Critical Identity List

1. Chin-length deep teal bob with blunt bangs
2. Single long ahoge curling left
3. Round yellow hair clip on the right side of the bangs
4. Oversized mustard cardigan; sleeves fully cover hands (sweater paws)
5. Round amber eyes with star highlight
6. Cool teal / warm yellow palette with a small red ribbon accent

## Tier notes

- Tier 1: items 1–3, 5
- Tier 2: cardigan silhouette, palette, ribbon
- Tier 3: pleat count, blouse collar trim
- Tier 4: pose, background, lighting, camera

## What changes vs. reference

Front-facing stiff pose → relaxed three-quarter turn looking back over the shoulder; plain background → rooftop at sunset; flat lighting → warm key with cool fill. Sleeve-covered hands are *kept* (identity) and also solve the hand-anatomy risk.

## Delivered prompt (tag-based, Stable Diffusion / anime model)

```
1girl, teenage girl, slim build, anime style, three-quarter view, looking back over shoulder,
chin-length deep teal bob haircut, blunt bangs, single long ahoge curling left, round yellow hair clip on right side of bangs,
large round amber eyes, star-shaped eye highlight, soft blush, gentle smile,
white sailor blouse, red loose neck ribbon, oversized mustard-yellow cardigan, sleeves extending past hands, hands hidden in sleeves, navy pleated skirt,
weight on right leg, relaxed posture, hair and skirt moving gently in one wind direction,
school rooftop, chain-link fence softly blurred in foreground, distant city skyline, sunset sky in peach and lavender, low-contrast background,
warm golden key light from upper right, cool lavender fill, pale rim light on hair edge, soft ambient glow,
matte knit cardigan texture, soft cotton blouse, subtle satin ribbon sheen,
clean lineart, soft cel shading with gentle gradients, natural skin shading, depth of field, high resolution illustration
```

**Negative prompt:**

```
extra fingers, malformed hands, asymmetrical eyes, duplicated hair clip, second ahoge, floating ornaments, tangled hair, inconsistent colors, plastic skin, excessive bloom, noisy background, text, watermark, logo, low-resolution face, warm color cast on hair
```

**Note to user:** Shoe style was cropped in your reference, so I kept the framing at three-quarter and didn't invent shoes. If you want full-body, tell me what she wears on her feet.
