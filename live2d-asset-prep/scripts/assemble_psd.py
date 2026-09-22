#!/usr/bin/env python3
"""
Assemble pre-cut, already-transparent character part images into a single
properly named, grouped, layered PSD - plus a composited preview PNG.

This script does NOT segment a flat illustration into parts and does NOT
reconstruct hidden art. It only organizes pieces that already exist as
separate transparent PNGs (each exactly canvas-sized, padded with
transparency) into a clean production PSD. See SKILL.md for when this
script applies versus when only the text blueprint can be produced.

Usage:
    python assemble_psd.py <spec.json> <images_dir> <output_dir>

spec.json format:
{
  "canvas": {"width": 2000, "height": 2600},
  "tree": [
    {"type": "group", "name": "HEAD", "children": [
        {"type": "layer", "name": "Hair_Front", "file": "hair_front.png"},
        {"type": "group", "name": "FACE", "children": [
            {"type": "layer", "name": "Face_Base", "file": "face_base.png"}
        ]}
    ]},
    {"type": "layer", "name": "Body_Torso", "file": "body_torso.png"}
  ]
}

Node order within a list is "top first", i.e. the same order you'd read
top-to-bottom in a Photoshop layers panel (front-most / topmost item
listed first). The script handles reversing this internally for the
underlying library.

Every leaf "file" must be an RGBA PNG exactly the size of "canvas" -
pad with transparency rather than cropping to the visible content, so
all layers share one coordinate space.
"""
import sys
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image


def load_rgba_exact(path, width, height):
    img = Image.open(path).convert("RGBA")
    if img.size != (width, height):
        raise ValueError(
            f"{path} is {img.size}, expected exactly ({width}, {height}). "
            f"Pad the source image to the full canvas size with "
            f"transparency instead of cropping to visible content."
        )
    return img


def collect_leaves_bottom_to_top(tree):
    """Flatten the tree into a bottom-to-top ordered list of leaf layers,
    for building the preview composite. 'tree' is top-first per node, so
    reverse at each level."""
    leaves = []
    for node in reversed(tree):
        if node["type"] == "layer":
            leaves.append(node)
        elif node["type"] == "group":
            leaves.extend(collect_leaves_bottom_to_top(node["children"]))
        else:
            raise ValueError(f"Unknown node type: {node['type']}")
    return leaves


def build_pytoshop_nodes(tree, images_dir, width, height, loaded_cache):
    """Build pytoshop nested_layers nodes. pytoshop/psd-tools store layers
    bottom-to-top (last in the python list = topmost), so we reverse the
    top-first spec order at every level."""
    from pytoshop.user import nested_layers

    nodes = []
    for node in reversed(tree):
        if node["type"] == "layer":
            img_path = Path(images_dir) / node["file"]
            img = load_rgba_exact(img_path, width, height)
            loaded_cache[node["name"]] = img
            arr = np.array(img)
            r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
            nodes.append(
                nested_layers.Image(
                    name=node["name"],
                    channels={0: r, 1: g, 2: b, -1: a},
                    top=0, left=0, bottom=height, right=width,
                )
            )
        elif node["type"] == "group":
            children = build_pytoshop_nodes(
                node["children"], images_dir, width, height, loaded_cache
            )
            nodes.append(
                nested_layers.Group(name=node["name"], layers=children, closed=False)
            )
        else:
            raise ValueError(f"Unknown node type: {node['type']}")
    return nodes


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    spec_path, images_dir, output_dir = sys.argv[1:4]
    with open(spec_path) as f:
        spec = json.load(f)

    width = spec["canvas"]["width"]
    height = spec["canvas"]["height"]
    tree = spec["tree"]

    os.makedirs(output_dir, exist_ok=True)

    # --- Build and write the PSD ---
    from pytoshop.user import nested_layers
    from pytoshop.enums import ColorMode, Compression

    loaded_cache = {}
    top_level_nodes = build_pytoshop_nodes(tree, images_dir, width, height, loaded_cache)

    # NOTE: this pytoshop version's RLE compressor has a bug (undefined
    # 'packbits' name) - use raw compression, which is larger but reliable.
    psdfile = nested_layers.nested_layers_to_psd(
        top_level_nodes,
        color_mode=ColorMode.rgb,
        size=(height, width),
        compression=Compression.raw,
        depth=8,
    )
    psd_out_path = Path(output_dir) / "character.psd"
    with open(psd_out_path, "wb") as fd:
        psdfile.write(fd)

    # --- Build the preview PNG ourselves (don't rely on psd-tools'
    #     composite(), which mis-renders overlapping alpha in this setup) ---
    leaves_bottom_to_top = collect_leaves_bottom_to_top(tree)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for leaf in leaves_bottom_to_top:
        img = loaded_cache[leaf["name"]]
        canvas = Image.alpha_composite(canvas, img)
    preview_out_path = Path(output_dir) / "preview.png"
    canvas.save(preview_out_path)

    print(f"Wrote {psd_out_path}")
    print(f"Wrote {preview_out_path}")
    print(f"Total leaf layers: {len(leaves_bottom_to_top)}")


if __name__ == "__main__":
    main()
