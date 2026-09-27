---
name: character-reference-sheet
description: Turn a character image into a clean reference sheet for fan art / 二创 (redraws, outfit swaps, pose practice) that preserves the character's face, hair, palette, and silhouette exactly as drawn. Use this whenever the user uploads a character image and wants a "reference sheet", "model sheet", "turnaround", "base template", something "easy to redraw", "easy to change the outfit on", or wants to prep a character for fan art / derivative works. This skill deliberately does NOT infer or expose body shape hidden under clothing and does NOT generate a body-conforming/skin-tight placeholder garment — it keeps the original outfit (or a loose, non-form-fitting placeholder shape) so proportions stay exactly as depicted in the source art, never reconstructed.
---

# Character Reference Sheet Generator

## Purpose

Produce a clean, reusable reference sheet from a source character image so someone can redraw the character in new outfits, poses, or scenes (fan art / 二创) while staying consistent with the original design.

This is an **identity-extraction and layout tool**, not a body-reconstruction tool. It never tries to figure out what's "underneath" the character's clothes, and it never renders the character in a skin-tight or form-fitting garment. Proportions are taken only from what is actually visible in the source art.

## Core rule (read this first)

- Preserve: face, hair, color palette, accessories that are part of the character's identity, art style, and the **silhouette exactly as drawn** (including the outfit's silhouette).
- Never: infer anatomy hidden by clothing, render the character in a body-conforming/skin-tight suit, "reveal" body shape, sexualize, or make the character more revealing than the source.
- If a request asks for a form-fitting bodysuit, anatomy-revealing template, or to show the body "under" the clothes, decline that specific part and offer the loose-placeholder approach instead — do not reinterpret the request to quietly do it anyway.

## Step 1 — Analyze the source image

Note, without inventing anything not visible:
- Face: shape, eyes, distinguishing features
- Hair: style, color, silhouette
- Palette: key colors used across the design
- Identity-defining features: things like horns, tails, wings, unique ears, permanent markings — features that are part of the character, not the outfit
- Outfit: describe it, but treat it as replaceable content, not identity
- Pose/angle available in the source (note if only front view exists — don't fabricate side/back)

## Step 2 — Choose the body placeholder

Default (per user preference): a **loose, flat-colored/grey silhouette shape** over the body — NOT skin-tight, NOT anatomy-revealing. It should read as "a simple placeholder shape," roughly following the original outfit's silhouette (e.g., if the source wears a loose jacket and pants, the placeholder keeps that loose block shape) rather than the body underneath it.

Alternative the user can request instead: keep the character in their original outfit and just clean up the background/pose. Never default to a form-fitting suit; if the user explicitly asks for one, explain that this skill is built to avoid anatomy-inference/skin-tight templates and suggest the loose-silhouette or original-outfit approach instead.

## Step 3 — Layout

Build a reference sheet with:
- Front view (always, since it's always available from a single source image)
- Side and back views **only if** the source image or additional references make them reasonably inferable; otherwise, label them "not available from source" rather than guessing
- Small color palette swatch strip (pulled from the actual design)
- Optional close-up callouts of identity-defining features (face, hair, unique markings)

Neutral, plain background (flat color or transparent) — no scene, no props unless prop is identity-defining (e.g., a signature staff).

## Step 4 — Consistency check before finalizing

- Is the face still clearly the same character?
- Is the hair silhouette preserved?
- Are proportions taken from the source art, not invented?
- Is the body placeholder loose/non-revealing, matching what was agreed in Step 2?
- No new anatomy, no added skin exposure, no sexualization relative to the source?

If any of these fail, revise before presenting the result.

## What this skill will not do

- Infer or render body shape/anatomy hidden by clothing
- Generate a skin-tight, form-fitting, or "second skin" bodysuit template
- Increase skin exposure or make the design more revealing than the source
- Apply this process to real photos of real people (this is for illustrated/fictional characters only)
- Fabricate unseen details (e.g., inventing a back view with no reference)
