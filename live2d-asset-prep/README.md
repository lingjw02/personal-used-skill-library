# Live2D Character Production Asset Prep

> **AI Skill**: Prepare anime character artwork into production-ready materials for Live2D Cubism rigging, VTuber models, and animation—producing layer blueprints, rigging specifications, and assembling transparent parts into structured PSD files with automated QA.

---

## 📌 Overview

**Live2D Asset Prep** bridges the gap between static 2D character artwork and Live2D Cubism rigging. 

Rigging an anime character requires strict organization: every eye layer, mouth part, hair strand, and clothing layer must follow standardized naming conventions, appropriate hierarchy, transparent padding, and sufficient overlap margins.

### What This Skill Does
- **Blueprint Generation**: Full layer tree hierarchy, naming conventions, Live2D standard parameter mapping (`ParamAngleX/Y/Z`, `ParamEyeLOpen`, etc.), physics setup, and expression/phoneme blueprints.
- **Automated PSD Assembly**: Compiles pre-separated, canvas-aligned transparent PNG pieces into a properly structured Photoshop PSD with nested layer groups.
- **Mechanical QA Validation**: Verifies layer names, canvas sizes, alpha transparency, bounding box overlaps, and group hierarchy.

### Scope & Boundaries
- **Flat Illustration (Merged)**: When only a single merged character image is provided, this skill produces the comprehensive **text blueprint and layer plan** (ready for an artist or inpainting tool to cut parts).
- **Separated Transparent PNGs**: When cut parts are provided, this skill executes automated assembly and QA scripts.
- *Note*: This skill prepares the production PSD and blueprint; final mesh deformation and physics calibration occur inside Live2D Cubism Editor.

---

## 🏗️ Layer Structure & Hierarchy

Standardized naming follows the `Category_Subcategory_Side` format (e.g., `Hair_Front_Center`, `Eye_L_Iris`, `Clothing_Coat_Sleeve_R`).

```
CHARACTER_ROOT/
├── FOREGROUND_EFFECTS/      (Floating particles, foreground props)
├── HEAD/
│   ├── HAIR_FRONT/          (Bangs, side locks, front hair accessories)
│   ├── FACE/
│   │   ├── BROW/            (Brow_L, Brow_R)
│   │   ├── EYE_L/           (Highlight, UpperLid, LowerLid, Lash, Iris, Pupil, White)
│   │   ├── EYE_R/           (Highlight, UpperLid, LowerLid, Lash, Iris, Pupil, White)
│   │   ├── NOSE/            (Nose, Nose_Shadow)
│   │   ├── MOUTH/           (Upper, Lower, Inner, Teeth_Upper, Teeth_Lower, Tongue)
│   │   ├── BLUSH/           (Cheek glow, blush stickers)
│   │   └── Face_Base        (Clean facial skin without hair shadows baked in)
│   ├── HAIR_SIDE/           (Left/Right flowing locks)
│   └── EAR/                 (Ear_L, Ear_R)
├── BODY/
│   ├── NECK/                (Neck base, throat shadow)
│   ├── CLOTHING_UPPER/      (Jacket, shirt, collar, tie, buttons)
│   ├── ARMS_L / ARMS_R/     (Upper arm, forearm, hand, fingers)
│   ├── CLOTHING_LOWER/      (Belt, skirt/pants, pleats)
│   └── LEGS/                (Thighs, calves, boots/shoes)
└── HAIR_BACK/               (Back hair mass, ponytail base, back ribbons)
```

For complete tier structures (Basic, Standard, Advanced, Professional), see [`references/layer_structure_reference.md`](references/layer_structure_reference.md).

---

## ⚙️ Automated Python Tools

### Installation
Install dependencies via Python 3.9+:
```bash
pip install -r requirements.txt
```

### 1. PSD Assembly (`scripts/assemble_psd.py`)
Assembles transparent RGBA PNG files into a nested, grouped Photoshop `.psd` and renders a composite `preview.png`.

```bash
python scripts/assemble_psd.py <spec.json> <images_dir> <output_dir>
```

#### `spec.json` Format
```json
{
  "canvas": {"width": 2000, "height": 2600},
  "tree": [
    {
      "type": "group",
      "name": "HEAD",
      "children": [
        {"type": "layer", "name": "Hair_Front", "file": "hair_front.png"},
        {
          "type": "group",
          "name": "FACE",
          "children": [
            {"type": "layer", "name": "Face_Base", "file": "face_base.png"}
          ]
        }
      ]
    },
    {"type": "layer", "name": "Body_Torso", "file": "body_torso.png"}
  ]
}
```
*Note*: All input PNGs must match the full canvas size padded with transparency.

### 2. QA Validation (`scripts/qa_check.py`)
Validates assembled PSD integrity against specification:
```bash
python scripts/qa_check.py <spec.json> <images_dir> <output_dir>/character.psd <output_dir> [--overlap-pairs overlap_pairs.json]
```

Checks performed:
- [x] Clean naming regex compliance (`Bad patterns: "Layer 1", "Copy", "Untitled"`)
- [x] Zero missing or extraneous layers
- [x] Exact hierarchy and parent-child group structure
- [x] Canvas dimensions match specification
- [x] Transparent backgrounds (flags accidentally opaque corners)
- [x] Overlap margin bounding box verification at key seams

---

## 📂 File Structure

```
live2d-asset-prep/
├── SKILL.md                          # Skill definition and agent guidelines
├── README.md                         # Detailed documentation
├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── assemble_psd.py               # Deterministic PSD assembler
│   └── qa_check.py                   # Automated QA test suite
└── references/
    ├── layer_structure_reference.md  # Standard Live2D layer hierarchy & tiers
    ├── rigging_blueprint_reference.md# Parameters, physics & phoneme mapping
    └── qa_checklist_reference.md     # Mechanical vs human inspection checklist
```

---

## 📦 Deliverable Package Layout

When fully assembled, outputs are organized cleanly:

```
<CharacterName>_Live2D/
├── 02_PSD/
│   └── character.psd                 # Fully grouped & named PSD
├── 03_PREVIEW/
│   └── preview.png                   # Alpha-composited preview
├── 05_BLUEPRINT/
│   └── rig_blueprint.md              # Parameters, physics & phoneme map
└── 06_QA/
    ├── qa_report.json                # Machine-readable test log
    └── qa_report.md                  # Human-readable QA checklist
```
