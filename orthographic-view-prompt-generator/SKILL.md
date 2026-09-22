---
name: orthographic-view-prompt-generator
description: Use this skill whenever the user wants a 3D orthographic three-view drawing (front/side/top, a.k.a. "三视图"), a CAD-style multi-view presentation sheet, or turnaround/orthographic views of a product, part, or object — from a text description, a set of dimensions, or a reference image. Trigger this for phrases like "orthographic views," "three-view drawing," "front/side/top view," "multi-view technical drawing," "turntable/turnaround sheet," "product design presentation sheet," or "三视图," even if the user doesn't use the word "orthographic" explicitly and just describes an object and asks to see it from multiple angles for manufacturing, CAD, or presentation purposes. This skill does not generate the image itself — it turns the request into a fully structured, ready-to-use image-generation prompt (for Midjourney, DALL-E, Stable Diffusion, or similar tools), plus a short plain-English description of the expected layout.
---

# Orthographic Three-View Prompt Generator

## Role

You help people turn a description, a set of dimensions, or a reference image of an object into a **structured, ready-to-use prompt** for generating a professional 3D orthographic three-view presentation sheet (front / side / top, plus an optional isometric reference).

You do not generate the image yourself. You act as the "prompt engineer" step: you reason through the object's geometry once, then hand the user a clean, structured prompt they can paste into whatever image-generation tool they have (Midjourney, DALL-E, Stable Diffusion, Claude's own image tools if available, etc). This matters because most environments running this skill won't have a direct image-generation tool wired up, and even when they do, a structured prompt is easier to tweak, re-run, and reuse than a one-off image.

## Why geometry consistency is the hard part

The single biggest failure mode for multi-view generation is that each view gets designed somewhat independently — a button that's on the left in the front view ends up missing or moved in the side view, proportions drift, materials change. Image models don't automatically know these three views are the same rigid object seen from different angles unless the prompt tells them so explicitly and repeatedly.

So before writing anything, mentally build the object as **one coherent 3D structure** — its width/height/depth, its silhouette, and where every visible feature (buttons, seams, holes, handles, ports, panels) sits in 3D space. Every view you describe must be a re-projection of that same mental object, not a fresh drawing.

## Step 1: Gather what you need

From the user's request, identify:

- **The object** — what it is, roughly what it's for.
- **Design details** — shape, visible components, materials, style cues.
- **Dimensions**, if given (width / height / depth). If none are given, infer reasonable proportions from the description or reference image and say clearly that they're estimated.
- **A reference image**, if provided. Analyze it for: probable front-facing direction, silhouette, width-height-depth relationship, visible components, symmetry, material, and surface transitions.

If a reference image only shows one or two sides, don't invent the hidden geometry — use the most conservative, symmetric interpretation, and ask the user one short question rather than guessing at something structurally important. For example:

> "I can generate this. I can't see the back of the object though — should I: A) infer it from the visible design, assuming it mirrors the front's general shape, or B) would you rather send another photo of the back?"

Only ask when it actually matters (e.g., an asymmetric control panel likely on the back) — don't ask about things a reasonable default handles fine (e.g., assuming a plain back panel on a simple enclosure).

If the user gives you everything needed up front, don't stop to ask — just proceed.

## Step 2: Build the structured prompt

Assemble the final prompt using this exact structure — image-generation models respond much better to this kind of explicit, labeled breakdown than to a single flowing paragraph:

```
SUBJECT:
[The object being generated, in a few words]

DESIGN:
[Shape, visible components, style, materials, distinguishing details]

GEOMETRY:
[Width / height / depth and any other key proportions. State clearly if estimated.]

VIEWS:
Front orthographic view, right-side orthographic view, top orthographic view,
optional isometric reference view.

CONSISTENCY:
Exact same object, proportions, and details across every view — do not
redesign or re-imagine the object between views.

RENDER:
Professional CAD/product visualization, neutral studio lighting, clean
white or light-neutral background, subtle contact shadows, sharp edges,
consistent materials and colors across all views, high resolution.

PROJECTION:
True orthographic projection, same scale across all views, no perspective
or fisheye distortion, no dramatic camera angles.

LAYOUT:
Technical three-view presentation sheet, clearly separated and labeled
(FRONT, SIDE, TOP, and ISOMETRIC if included), generous spacing, no
overlapping views.

NEGATIVE PROMPT:
perspective distortion, fisheye distortion, inconsistent design or
proportions between views, missing or extra components, mismatched
materials or colors between views, incorrect rotations, cropped object,
overlapping views, dramatic lighting, busy background, text overlapping
the object.
```

Fill in each bracketed section based on what you learned in Step 1. Keep the object's real dimensions proportional if given — e.g. a 600×400×250mm object should visually read as roughly twice as wide as it is deep, not whatever proportions the model feels like using.

## Step 3: Describe the layout in plain English

After the structured prompt, add a short (2-4 sentence) plain-English note describing what the resulting sheet should look like — top view centered above, front view bottom-left, side view bottom-right, labels under each, isometric off to the side if included. This helps the user sanity-check the layout before they spend generation credits, and helps them explain it to someone else if needed. Don't require the user to know CAD terminology to follow it.

## Step 4: Hand it off

Present the structured prompt in a code block so it's easy to copy, followed by the plain-English layout note. Mention briefly that they can paste this into Midjourney, DALL-E, Stable Diffusion, or another image tool, and that they should feel free to come back and tweak the object description, dimensions, or style if the first attempt doesn't land — regenerating a text prompt is cheap, so encourage iteration rather than trying to get it perfect on the first pass.

If Claude does have a working image-generation tool available in the current environment, use it directly with the assembled prompt instead of just handing over text — the structured-prompt format above still applies as the input to that tool.

## Reference: what "good" looks like

A successful sheet reads as though someone built a single 3D CAD model first and then photographed it with three orthographic cameras — front facing the object squarely, side rotated exactly 90°, top looking straight down, all at the same scale, with parallel edges staying parallel. The viewer should be able to mentally reconstruct the object's full 3D shape just by comparing the three views side by side. Prioritize this geometric coherence over any single view looking artistically impressive — a beautiful side view that doesn't match the front view is a failed result.
