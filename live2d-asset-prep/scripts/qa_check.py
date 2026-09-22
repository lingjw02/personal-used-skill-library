#!/usr/bin/env python3
"""
Run automated QA checks on a PSD assembled by assemble_psd.py, against the
same spec.json and source images_dir used to build it.

This only checks what can be verified mechanically (naming, presence,
hierarchy, transparency, canvas size, rough overlap between named pairs).
It does NOT judge visual/artistic quality, hidden-area reconstruction, or
whether overlap margins are actually *sufficient* for motion - those are
listed in the report as manual-review items, never marked as passed.
See references/qa_checklist_reference.md for the full breakdown.

Usage:
    python qa_check.py <spec.json> <images_dir> <psd_path> <output_dir>
        [--overlap-pairs overlap_pairs.json]

overlap_pairs.json (optional) format:
[
  {"a": "Hair_Front", "b": "Face_Base", "min_margin_px": 15},
  ...
]
"""
import sys
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

BAD_NAME_PATTERNS = [
    re.compile(r"^layer\s*\d*$", re.I),
    re.compile(r"^copy\s*\d*$", re.I),
    re.compile(r"^untitled\s*\d*$", re.I),
]
NAME_RE = re.compile(r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$")


def flatten_spec(tree, parent=None):
    """Return list of (name, type, parent_name) for every node in the spec."""
    out = []
    for node in tree:
        out.append((node["name"], node["type"], parent))
        if node["type"] == "group":
            out.extend(flatten_spec(node["children"], parent=node["name"]))
    return out


def leaf_files(tree):
    out = {}
    for node in tree:
        if node["type"] == "layer":
            out[node["name"]] = node["file"]
        elif node["type"] == "group":
            out.update(leaf_files(node["children"]))
    return out


def alpha_bbox(img):
    arr = np.array(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def boxes_overlap_with_margin(box_a, box_b, margin):
    """True if box_a and box_b overlap, or come within `margin` px of
    each other (a loose proxy for 'is there enough shared art at the
    seam')."""
    ax0, ay0, ax1, ay1 = box_a
    bx0, by0, bx1, by1 = box_b
    ax0, ay0, ax1, ay1 = ax0 - margin, ay0 - margin, ax1 + margin, ay1 + margin
    return not (ax1 < bx0 or bx1 < ax0 or ay1 < by0 or by1 < ay0)


def main():
    args = sys.argv[1:]
    overlap_pairs_path = None
    if "--overlap-pairs" in args:
        idx = args.index("--overlap-pairs")
        overlap_pairs_path = args[idx + 1]
        del args[idx:idx + 2]

    if len(args) != 4:
        print(__doc__)
        sys.exit(1)

    spec_path, images_dir, psd_path, output_dir = args
    with open(spec_path) as f:
        spec = json.load(f)
    width = spec["canvas"]["width"]
    height = spec["canvas"]["height"]
    tree = spec["tree"]

    expected = flatten_spec(tree)
    expected_names = {n for n, _, _ in expected}
    files_by_name = leaf_files(tree)

    report = {"passed": [], "failed": [], "warnings": [], "manual_review_required": []}

    # --- Check 1: naming convention ---
    bad_names = []
    for name, _, _ in expected:
        if not NAME_RE.match(name) or any(p.match(name) for p in BAD_NAME_PATTERNS):
            bad_names.append(name)
    if bad_names:
        report["failed"].append(f"Naming convention violated for: {bad_names}")
    else:
        report["passed"].append("All layer/group names follow the naming convention.")

    # --- Check 2 & 3: presence + hierarchy, by reading the PSD back ---
    from psd_tools import PSDImage

    psd = PSDImage.open(psd_path)

    def walk(layer, parent=None):
        out = [(layer.name.rstrip("\x00"), "group" if layer.is_group() else "layer", parent)]
        if layer.is_group():
            for child in layer:
                out.extend(walk(child, parent=layer.name.rstrip("\x00")))
        return out

    actual = []
    for layer in psd:
        actual.extend(walk(layer))
    actual_names = {n for n, _, _ in actual}

    missing = expected_names - actual_names
    extra = actual_names - expected_names
    if missing:
        report["failed"].append(f"Layers/groups missing from PSD: {sorted(missing)}")
    if extra:
        report["warnings"].append(f"Unexpected layers/groups in PSD not in spec: {sorted(extra)}")
    if not missing and not extra:
        report["passed"].append("Every planned layer/group is present in the PSD (and nothing unplanned).")

    expected_parent = {n: p for n, _, p in expected}
    actual_parent = {n: p for n, _, p in actual}
    hierarchy_mismatches = [
        n for n in expected_names & actual_names
        if expected_parent.get(n) != actual_parent.get(n)
    ]
    if hierarchy_mismatches:
        report["failed"].append(f"Hierarchy mismatch (wrong parent group) for: {hierarchy_mismatches}")
    else:
        report["passed"].append("Layer hierarchy matches the plan.")

    # --- Check 4 & 5: transparency + canvas size, from source images ---
    size_issues = []
    opaque_background_issues = []
    bboxes = {}
    for name, filename in files_by_name.items():
        img = Image.open(Path(images_dir) / filename).convert("RGBA")
        if img.size != (width, height):
            size_issues.append(f"{name}: {img.size} != canvas ({width},{height})")
        arr = np.array(img)
        corner_alphas = [
            arr[0, 0, 3], arr[0, -1, 3], arr[-1, 0, 3], arr[-1, -1, 3],
        ]
        if any(a > 10 for a in corner_alphas):
            opaque_background_issues.append(name)
        bboxes[name] = alpha_bbox(img)

    if size_issues:
        report["failed"].append(f"Canvas size mismatches: {size_issues}")
    else:
        report["passed"].append("All source images match the canvas size exactly.")

    if opaque_background_issues:
        report["failed"].append(
            f"Non-transparent canvas corners (possible accidental opaque "
            f"background) in: {opaque_background_issues}"
        )
    else:
        report["passed"].append("No accidental opaque background detected at canvas corners.")

    # --- Check 6: overlap heuristic between named pairs ---
    if overlap_pairs_path:
        with open(overlap_pairs_path) as f:
            pairs = json.load(f)
        for pair in pairs:
            a, b, margin = pair["a"], pair["b"], pair.get("min_margin_px", 10)
            box_a, box_b = bboxes.get(a), bboxes.get(b)
            if box_a is None or box_b is None:
                report["warnings"].append(f"Overlap check skipped for {a}/{b}: one layer has no visible pixels.")
                continue
            if boxes_overlap_with_margin(box_a, box_b, margin):
                report["passed"].append(f"{a} and {b} have adequate overlap/proximity for the seam.")
            else:
                report["warnings"].append(
                    f"{a} and {b} do not overlap within {margin}px - likely to show a gap when either moves."
                )

    # --- Manual review items (never auto-passed) ---
    report["manual_review_required"] = [
        "Character identity, face, hairstyle, and clothing genuinely match the reference (structural presence was checked, not visual fidelity).",
        "Colors are visually consistent across layers.",
        "Hidden areas (behind hair, under clothing) are plausibly reconstructed, if applicable.",
        "Overlap margins are actually sufficient for the intended range of motion, not just present.",
        "Eye-white/iris artwork extends far enough for believable eye movement.",
        "Mouth pieces are usable for A/I/U/E/O phoneme animation.",
        "Physics-candidate pieces (hair, ribbons, skirts, accessories) are cut with motion in mind.",
    ]

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "qa_report.json", "w") as f:
        json.dump(report, f, indent=2)

    lines = ["# QA Report", ""]
    lines.append(f"**Passed ({len(report['passed'])})**")
    lines += [f"- {x}" for x in report["passed"]]
    lines.append("")
    lines.append(f"**Failed ({len(report['failed'])})**")
    lines += [f"- {x}" for x in report["failed"]] or ["- none"]
    lines.append("")
    lines.append(f"**Warnings ({len(report['warnings'])})**")
    lines += [f"- {x}" for x in report["warnings"]] or ["- none"]
    lines.append("")
    lines.append("**Manual review required (not auto-verifiable)**")
    lines += [f"- {x}" for x in report["manual_review_required"]]
    with open(out_dir / "qa_report.md", "w") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
