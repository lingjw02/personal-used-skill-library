# Defect Detection & Repair Checklist

Use this as a scan checklist before and during restoration. Not every image will have every defect — identify which apply, and treat only those regions/aspects.

## Blur

Detect: motion blur, defocus blur, Gaussian-like softness, camera shake, directional blur, excessive softness, poor focus, localized blur (e.g. only part of the frame is soft).

Repair goal: recover natural edge definition without producing halos or an oversharpened, "crunchy" look. Directional blur should be corrected along its axis, not uniformly.

## Low resolution

Detect: pixelation, poor sampling, enlarged/blocky pixels, lost micro-detail, jagged diagonal lines (staircasing), weak facial detail, weak texture information.

Repair goal: reconstruct detail conservatively based on nearby visual evidence and the image's own style — don't invent detail that isn't implied by the surrounding pixels.

## Compression damage

Detect and repair where possible: JPEG blocking artifacts, ringing, mosquito noise, edge contamination, color bleeding at edges, quantization artifacts, banding in gradients, social-media re-compression artifacts (heavy blocking + oversharpening halos from platform processing).

## Noise

Detect and reduce: luminance noise, color/chroma noise, sensor noise, film or scanner grain, random pixel noise, AI-generation speckle artifacts.

Repair goal: reduce noise without erasing meaningful texture (skin pores, fabric weave, fine hair) — don't produce a smoothed/plastic look.

## Edge defects

Detect and repair: aliasing, stair-stepping, rough or broken outlines, broken line art (anime/illustration), double edges, edge halos, unnatural sharpening artifacts (over-crisp fringing).

Repair goal: clean, natural contours consistent with the image's own line style.

## Color defects

Detect and correct when it's clearly a defect (not an artistic choice): color cast, faded colors, low saturation, oversaturation, poor white balance, weak contrast, crushed blacks, washed-out look, uneven color reproduction across the frame.

Preserve intentional artistic color grading — don't "correct" a deliberately warm/cool or desaturated look.

## Lighting defects

Detect and recover where possible: underexposure, overexposure, weak shadow detail, weak highlight detail, uneven illumination, haze, low local contrast.

Do not artificially relight the entire scene — recover detail within the existing lighting, don't redesign it, unless the user explicitly asks for relighting.

## AI / rendering defects

For AI-generated or rendered source images, inspect for: broken lines, strange/inconsistent textures, duplicated small details, corrupted accessories, broken geometric objects, localized rendering glitches, texture discontinuities.

Repair only the obvious defects. Do not redesign or "improve" portions of the artwork that are already correct — this is a repair pass, not a re-generation.
