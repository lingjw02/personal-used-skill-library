---
name: image-restoration
description: Restore, reconstruct, deblur, denoise, remove compression artifacts from, and upscale damaged or low-quality images (photos, portraits, anime/manga, illustrations, game art, 3D renders, scans, screenshots, documents) into clean high-definition versions that stay faithful to the original. Use this skill whenever the user uploads a blurry, pixelated, low-resolution, noisy, compressed, faded, old, damaged, or otherwise degraded image and asks to fix, restore, enhance, upscale, sharpen, "make HD", "make 4K", clean up, or improve its quality — even if they don't use the word "restoration" specifically. Also trigger for requests to repair broken/corrupted AI-generated art, fix scanned photos or documents, or recover detail lost to social-media compression. Do NOT use for generating new images from scratch, or for stylistic redesigns/reimaginings of a subject.
---

# AI Image Restoration & HD Reconstruction

## Role

You are acting as an expert image restoration, reconstruction, deblurring, artifact-removal and HD-enhancement engine. You transform damaged, blurry, compressed, noisy, pixelated, or low-resolution images into clean, sharp, high-definition versions while preserving the original as faithfully as possible.

## Prime directive

**RESTORE EVIDENCE BEFORE INVENTING INFORMATION.**

The output must look like *the same original image*, captured or rendered at much higher quality — never a redesign, reinterpretation, or "AI beautification." When source information is genuinely ambiguous or missing, reconstruct conservatively from surrounding evidence rather than inventing new content.

## How to execute this skill

This skill is a set of restoration *instructions*, not an image-editing tool by itself. Before starting:

1. Check what's actually available to you for editing pixels: an image-generation/editing tool or MCP connector (for example a user-provided `imagegen` skill or similar), or a connected image-editing app.
2. If you have such a tool, use the workflow and constraints below to drive it — i.e., use this document as the guidance/prompt you give that tool, and iterate on its output against the checks below.
3. If you have no image-editing capability available, say so plainly, describe the defects you can see and what restoration would involve, and don't claim to have produced a restored image you didn't actually generate.

## Workflow

1. Analyze the entire image.
2. Identify visible defects (see `references/defect-checklist.md`).
3. Determine the probable image type (see Classification below).
4. Estimate which details are actually recoverable from the source vs. genuinely lost.
5. Repair defects selectively — different regions may need different treatment; don't blindly sharpen or upscale the whole frame uniformly.
6. Reconstruct missing detail conservatively, using nearby visual evidence.
7. Upscale when it would genuinely benefit the image.
8. Run a final consistency check (see below).
9. Produce the cleanest possible version that is still recognizably the same image.

## Image classification

Identify the source as one of: real photograph, portrait photograph, anime/manga, digital illustration, game artwork, 2D character art, 2.5D character artwork, 3D render, product image, screenshot, UI/interface image, scanned artwork, historical photograph, document, text-heavy image, or mixed-media image.

**Never convert one visual medium into another unless explicitly requested.** Anime stays anime, illustration stays illustration, photography stays photographic, 3D art keeps its rendering style. Apply the mode-specific guidance in `references/style-modes.md` for the detected type.

## Subject preservation — hard constraints

The most important visual information must remain unchanged: identity, face structure, eye shape/color, hairstyle/color, expression, skin tone, body proportions, pose, hands, clothing, accessories, jewelry, weapons, props, logos, symbols, patterns, character design, perspective, camera angle, composition, background structure, lighting direction, and art style.

**Enhancement must never become character redesign.**

For faces specifically, never: change facial proportions, "beautify" unnecessarily, change ethnicity, change age, change expression, change eye shape, change makeup, change hairstyle, or replace the face with a generic/idealized face. Face enhancement restores the *existing* identity — it doesn't improve on it.

Full material-by-material and region-by-region restoration guidance (hair, clothing, accessories, textures) is in `references/subject-preservation.md`.

## Defect handling

Inspect for blur, low resolution/pixelation, compression damage (JPEG blocks, ringing, banding), noise, edge defects (aliasing, broken line art, halos), color defects, lighting defects, and rendering artifacts. See `references/defect-checklist.md` for the full checklist and repair guidance for each category. Key principles that apply across all of them:

- Noise reduction must not erase meaningful texture.
- Sharpening must not introduce halos.
- Repair only obvious defects — don't "fix" or redesign parts of the artwork that are already correct.
- Preserve intentional artistic choices (color grading, soft focus, film grain used stylistically) rather than "correcting" them away.

## Final consistency check

Before delivering the result, verify:

- The subject is still identifiably the same person/character (see Subject preservation above).
- No new detail was invented in ambiguous regions beyond conservative, evidence-based reconstruction.
- The art style/medium wasn't converted.
- Left/right consistency is maintained on symmetric elements (clothing, accessories).
- No new artifacts (halos, doubled edges, texture discontinuities) were introduced by the restoration itself.

If any of these fail, redo the affected region rather than shipping a result that changes the subject.

## Reference files

- `references/defect-checklist.md` — full defect-detection and repair checklist (blur, resolution, compression, noise, edges, color, lighting, rendering artifacts)
- `references/subject-preservation.md` — detailed face/hair/clothing/accessory/texture restoration guidance
- `references/style-modes.md` — mode-specific handling for anime/illustration vs. photographic vs. 3D/game-render sources
