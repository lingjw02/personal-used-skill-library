# QA Checklist Reference

The full Live2D asset QA checklist, split by what `scripts/qa_check.py` can actually verify from pixels/metadata versus what needs a human (or a generative image tool) to judge. Report both in the QA output — don't silently drop the manual-only items, just label them clearly as "manual review needed" rather than claiming they passed.

## Checks `qa_check.py` can run automatically

- Layer naming matches convention (no `Layer 1`, `Copy 3`, `Untitled`, etc.)
- Every layer/group named in the layer plan actually exists in the assembled PSD (and vice versa — nothing unexpected)
- Layer hierarchy matches the plan (correct nesting/grouping)
- Canvas has transparency (not an accidental opaque white/solid background)
- Canvas size is consistent across all layers
- Rough overlap check between named adjacent-layer pairs (e.g. hair→face): flags a warning if their bounding boxes don't overlap by a minimum margin, since a tight or non-overlapping seam is likely to show a gap in motion

## Checks that need a human (or a generative image/inpainting tool) to actually judge

These come from the original checklist but genuinely require visual/artistic judgment or generative capability this skill doesn't have on its own — always list them as open items, never mark them "passed":

- Character identity, face, hairstyle, and clothing genuinely preserved (vs. just structurally present)
- Colors visually consistent across layers
- Hidden areas (what's behind hair, under overlapping clothing) actually reconstructed with plausible art
- No visible seams or transparent holes when a component would move
- Overlap margins are actually *sufficient* for the intended range of motion, not just present
- Iris/eye-white artwork extends far enough for believable eye movement
- Mouth pieces are usable for A/I/U/E/O phoneme animation
- Hair/clothing/accessory physics pieces are cut with motion in mind, not just visually separated

## Failure handling

- **Automated-check failure** that's fixable in metadata/organization (e.g. a misnamed layer, wrong group nesting) → fix it directly and note the fix.
- **Automated-check failure** that would require changing pixels (e.g. accidental opaque background baked into a source image) → flag it, don't attempt to silently paint over it.
- **Manual-review item** → always surface it in the report; never claim it passed just because nothing crashed.
