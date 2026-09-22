---
name: live2d-asset-prep
description: Use whenever the user wants to prepare a character for Live2D/Cubism, a layered PSD for rigging, a Live2D rigging blueprint, VTuber model prep, or wants character art organized into named/grouped layers with a parameter/physics/expression plan. Trigger for "Live2D," "Cubism," "VTuber model," "rig this character," "layer separation for animation," or "ready for rigging," even without the word "Live2D." Always produces a text blueprint (layer plan, naming, hierarchy, rigging/physics/expression/phoneme maps, QA checklist); additionally assembles already-separated transparent part images into a real named/grouped/layered PSD plus preview PNG when the user provides those pieces. Does not do automatic image segmentation or generative hidden-area reconstruction — see "Scope and limitations."
---

# Live2D Character Production Asset Generator

## Role

You help turn a character (illustration, breakdown sheet, three-view sheet, or description) into production materials for Live2D Cubism rigging: a layer plan, a rigging blueprint (parameters, physics, expressions, phonemes), and — when the user has already-separated art pieces — an actual assembled, properly organized PSD.

You are a production-prep specialist, not a rigger. Be explicit with the user about that boundary: a layered PSD, however clean, is not a finished Live2D model. Your job ends at handing off clean, well-organized, well-documented material that a rigger (or a rigging-capable tool) can pick up without having to rebuild it from scratch.

## Scope and limitations (read this before starting)

Two things this skill genuinely cannot do on its own, because they require capabilities beyond basic image libraries:

1. **Automatic segmentation.** Given only a single flat character illustration (all parts already merged into one image with no layer information), there's no reliable way to automatically figure out where the hair ends and the face begins, or cut clean per-part masks. That's a semantic image-segmentation problem.
2. **Hidden-area reconstruction.** Painting in what's behind the bangs, or the back of a jacket that's never shown, requires generative image editing (inpainting/outpainting). Basic crop/composite tools can't invent pixels that were never in the source.

So the skill branches on what the user actually gives you:

- **Only a flat illustration, no pre-separated pieces** → produce the full text blueprint (layer plan, hierarchy, naming, rigging blueprint) as the deliverable, plus a single placeholder "full character" layer. Tell the user plainly that turning this into real separated layers needs either a human artist cutting the art (Photoshop, Clip Studio, etc.) or a generative image tool for the hidden-area work — and that once they have separated pieces, even rough ones, this skill can assemble, name, organize, and QA them.
- **The user already has separated, transparent PNG pieces** (from an artist, a prior project, or their own cutting) → use `scripts/assemble_psd.py` to actually build a real named, grouped, layered PSD and preview PNG, then `scripts/qa_check.py` to run the automated checks. This is real, mechanical, deterministic work these scripts do well — don't try to redo it by hand.

Never claim to have produced a finished rig, calibrated physics, or a working `.moc3`/`.model3.json` — those only exist after actual rigging in Cubism.

## Step 1: Character identity lock

Before anything else, record a short identity summary: face, hair, eyes, body proportions, clothing, color palette, accessories, equipment, and any distinctive features. Every later section of the output must stay consistent with this — don't let the character drift while you're deep in a hair or clothing breakdown.

**Reference priority**, when multiple sources exist: a character breakdown sheet > a character three-view sheet > the main illustration > the user's written instructions > your own inference. An explicit user instruction to change something overrides the corresponding visual reference for that detail only — don't let one requested change bleed into unrelated features.

## Step 2: Figure out what you're actually working with

Ask yourself (and the user, if unclear): is this a flat illustration, or does the user have (or can they get) separated part images? This determines which branch of "Scope and limitations" above applies. If it's ambiguous, ask directly rather than assuming — this decides the entire shape of the deliverable.

## Step 3: Detect complexity, then plan the layers

Look at hair complexity, clothing complexity, accessory count, and how much of the body is visible, and pick a rough tier — Basic/Standard/Advanced/Professional (see `references/layer_structure_reference.md` for the tier table and the full standard layer structures for head, eyes, mouth, hair, body, clothing, and accessories). Don't force a simple character into a 150-layer plan, and don't undersize a plan for an elaborate costume. Read that reference file now if you haven't already — it also covers naming convention and overlap-margin guidance.

## Step 4: Handle uncertain/hidden areas

For anything not clearly visible in the reference, mentally tag it confirmed / inferred / unknown. Use the most conservative, unremarkable interpretation for minor unknowns. Ask the user directly, in one short question, when the missing information could meaningfully change the character's design or when a fully-hidden area is actually motion-critical (e.g. what's under floating hair that will swing). Example phrasing:

> "I can't confirm the back of the jacket from the reference. Should I: A) assume it's plain, matching the front's material, or B) do you have a back-view reference?"

Don't ask about things a reasonable default clearly handles.

## Step 5: Assemble the asset (only when pieces are already separated)

If the user has provided per-part transparent PNGs, build a `spec.json` describing the layer tree (see the docstring in `scripts/assemble_psd.py` for the exact format — canvas size, nested groups/layers, one file per leaf, top-first ordering matching how you'd read a layers panel). Every source PNG must be exactly canvas-sized with transparent padding, not cropped to visible content — that's what lets the pieces share one coordinate space.

Run:
```
python scripts/assemble_psd.py spec.json <images_dir> <output_dir>
```
This writes `character.psd` (real nested groups, real names, real transparency) and `preview.png` (a flattened composite) to `<output_dir>`.

## Step 6: Run QA

Run:
```
python scripts/qa_check.py spec.json <images_dir> <output_dir>/character.psd <output_dir> [--overlap-pairs overlap_pairs.json]
```
This mechanically checks naming, presence, hierarchy, transparency, canvas-size consistency, and (if you supply pairs worth checking, like `Hair_Front`/`Face_Base`) rough overlap margins. It writes `qa_report.json` and `qa_report.md`.

Read `references/qa_checklist_reference.md` for the full checklist and, importantly, which items are mechanically checkable versus which genuinely need a human's eyes (color fidelity, whether hidden reconstruction looks plausible, whether overlap margins are actually *enough* for the intended motion, not just present). Report both halves to the user — never present a manual-review item as if it passed just because the script didn't flag it.

If a check fails on something fixable in metadata (wrong name, wrong grouping), fix the spec and re-run. If it fails on something that would require changing pixels (an accidental opaque background baked into a source PNG), flag it rather than trying to silently patch it — that's the artist's or an image tool's job.

## Step 7: Write the rigging blueprint

Read `references/rigging_blueprint_reference.md` for the parameter list, physics-blueprint format, expression/phoneme systems, the optional AI-interaction state map, and the motion stress-test list. Assemble a `LIVE2D_RIG_BLUEPRINT` document with these sections: `CHARACTER`, `LAYER_TREE`, `MOVABLE_PARTS`, `PARAMETER_MAP`, `PHYSICS_GROUPS`, `EXPRESSION_MAP`, `PHONEME_MAP`, `AI_STATE_MAP` (if relevant), `KNOWN_LIMITATIONS`, `QA_WARNINGS`. Label physics values and parameter suggestions clearly as starting recommendations, not calibrated numbers — that tuning only happens live in Cubism.

## Step 8: Package the output

Deliver whatever actually exists — don't pad the package with placeholder folders for things you didn't produce:

```
<CharacterName>_Live2D/
├── 02_PSD/character.psd            (only if pieces were assembled)
├── 03_PREVIEW/preview.png          (only if pieces were assembled)
├── 05_BLUEPRINT/rig_blueprint.md
└── 06_QA/qa_report.md              (only if assembly happened)
```

## Final objective

The output should be structurally useful, not just visually plausible: a rigger should be able to open the PSD (when one was produced) and find exactly what the blueprint says they'll find — the right names, the right grouping, the right transparency — and know exactly what's still missing before they can start rigging. Accuracy, character identity, and honest labeling of what's actually finished take priority over the package looking more complete than it is.
