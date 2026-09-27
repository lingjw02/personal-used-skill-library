# Mode-Specific Restoration Guidance

Apply the section that matches the image's classification (see main SKILL.md). Never cross modes — the output must stay in the same visual medium as the input.

## Anime / manga / illustration / game art mode

Prioritize:
- Clean line art with consistent line weight
- Smooth curves rather than jagged or stair-stepped lines
- Sharp, well-defined eye detail (the eyes are usually the focal point in this style)
- Flat or cel-shaded color regions kept flat/cel-shaded, not converted to painterly gradients
- Preserving the original line-art "language" — thin uniform lines stay thin and uniform, painterly brush lines stay painterly

Avoid: adding photographic texture (skin pores, fabric weave detail) to a flat-shaded style; softening crisp line art into a painted look; smoothing out intentional stylization.

## Photographic / portrait mode

Prioritize:
- Natural skin texture (pores, fine lines) rather than plastic-smooth skin
- Realistic edge definition on hair strands and fabric
- Accurate, natural-looking color and exposure recovery
- Sensor/film grain reduced but not eliminated if it reads as intentional or period-appropriate (e.g. historical photographs)

Avoid: over-smoothing skin, introducing a "beauty filter" look, oversharpening into a crunchy HDR appearance.

## Historical photograph / scanned artwork mode

Prioritize:
- Dust, scratch, and tear repair
- Fading and color-cast correction while respecting the period's natural tonal range (don't force modern vivid color grading onto a black-and-white or sepia photo unless asked to colorize)
- Scanner noise and moiré reduction
- Careful reconstruction of physically damaged/missing regions using surrounding evidence only

Avoid: colorizing unless explicitly requested; inventing content in torn-away or missing regions beyond very conservative, evidence-based fill.

## 3D render / product image mode

Prioritize:
- Preserving the render's lighting model and material shaders as-is
- Cleaning up rendering artifacts (aliasing, noise from ray-traced renders, texture seams) without changing materials
- Sharpening geometry edges without introducing halos

Avoid: changing the render style (e.g. stylized-to-photoreal or vice versa), altering material properties.

## Screenshot / UI / document / text-heavy image mode

Prioritize:
- Text legibility above all — clean, sharp, correctly-shaped glyphs
- Preserving exact layout, colors, icons, and UI elements as they are
- Removing compression blocking around text edges

Avoid: any content invention — text must not be "guessed" or altered; if characters are truly illegible, leave them as restored-but-illegible rather than fabricating text.
