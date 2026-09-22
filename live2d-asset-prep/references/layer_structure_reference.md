# Layer Structure Reference

Read this when you're building the layer plan (the tree of groups and layers) for a character. It's a menu of standard Live2D layer structures, not a mandatory checklist — use the parts that fit the character's actual complexity (see "Complexity detection" in SKILL.md).

## Naming convention

Use standardized English names that describe purpose. Pattern: `Category_Subcategory_Side` (side only when relevant).

Good: `Face_Base`, `Eye_L_Iris`, `Hair_Front_Center`, `Clothing_Jacket_Sleeve_L`, `Accessory_Ribbon`

Avoid: `Layer 1`, `Copy 3`, `Untitled`, anything auto-generated without meaning.

## Head

```
HEAD
├── Face_Base
├── Ear_L
├── Ear_R
├── Nose
├── Blush
├── Shadow
├── Eye_L (see Eyes below)
├── Eye_R (see Eyes below)
├── Brow_L
├── Brow_R
└── Mouth (see Mouth below)
```
Only split out pieces (nose, blush, shadow) when the character's art actually has them as distinct elements worth animating separately.

## Eyes

Each eye supports independent animation, so both eyes get the full set:

```
Eye_L
├── Eye_L_White
├── Eye_L_Iris
├── Eye_L_Pupil
├── Eye_L_Highlight
├── Eye_L_UpperLid
├── Eye_L_LowerLid
└── Eye_L_Lash
```
(mirror for Eye_R). Don't crop the iris exactly to its visible boundary — leave extra iris artwork so the eye can look in different directions without revealing an edge.

## Mouth (phoneme-ready)

```
Mouth
├── Mouth_Upper
├── Mouth_Lower
├── Mouth_Inner
├── Teeth_Upper
├── Teeth_Lower
└── Tongue
```
Only include the pieces that are visually appropriate for the character (e.g. skip teeth/tongue for a design where the mouth is a simple line). This structure is meant to support `ParamMouthOpenY` / `ParamMouthForm` and A/I/U/E/O phoneme states later.

## Eyebrows

`Brow_L`, `Brow_R`, each with enough surrounding space in its own layer to be raised, lowered, or angled without clipping.

## Hair

Medium-detail default:

```
Hair
├── Hair_Back
├── Hair_Side_L
├── Hair_Side_R
├── Hair_Front_Center
├── Hair_Front_L
├── Hair_Front_R
└── Hair_Special   (ahoge, ponytail, ribbon-in-hair, any character-specific piece)
```
Separate based on what will actually move differently — don't split into dozens of individual strands unless the character's hairstyle genuinely calls for it.

## Body

```
BODY
├── Neck
├── Torso
├── Arm_L_Upper
├── Arm_L_Lower
├── Hand_L
├── Arm_R_Upper
├── Arm_R_Lower
├── Hand_R
├── Waist
├── Leg_L_Upper
├── Leg_L_Lower
├── Foot_L
├── Leg_R_Upper
├── Leg_R_Lower
└── Foot_R
```
Skip anatomical splits that clothing already makes invisible/immovable — a character in a long stiff robe doesn't need separate upper/lower leg layers if the robe itself doesn't reveal leg movement.

## Clothing

```
CLOTHING
├── Shirt
├── Collar
├── Jacket_Body
├── Jacket_Sleeve_L
├── Jacket_Sleeve_R
├── Skirt_Front
├── Skirt_Back
├── Belt
└── Shoes
```
Give loose, physics-candidate pieces (ribbons, ties, coat tails, scarves, capes, skirts, hanging straps) higher separation priority than snug-fitting pieces — they're the ones that will actually benefit from independent movement.

## Accessories

Keep movable accessories as their own layers rather than merging them into hair or clothing: `Accessory_Glasses`, `Accessory_Earring_L`, `Accessory_Earring_R`, `Accessory_Ribbon`, `Accessory_Necklace`, `Accessory_Bag`, `Accessory_Hat`, etc.

## Full hierarchy example

```
CHARACTER
├── HEAD
│   ├── HAIR_BACK
│   ├── FACE
│   │   ├── EYE_L
│   │   ├── EYE_R
│   │   ├── BROW_L
│   │   ├── BROW_R
│   │   └── MOUTH
│   ├── HAIR_SIDE
│   └── HAIR_FRONT
├── BODY
│   ├── TORSO
│   ├── ARM_L
│   ├── ARM_R
│   ├── LEG_L
│   └── LEG_R
├── CLOTHING
└── ACCESSORIES
```
Adapt depth and grouping to the character — this is a starting skeleton, not a fixed template.

## Layer count tiers (for reference, not a rule to force)

| Tier | Layer count | Typical character |
|---|---|---|
| Basic | 20–40 | Simple design, minimal accessories, plain outfit |
| Standard | 40–80 | Typical anime character, moderate hair/clothing detail |
| Advanced | 80–150 | Detailed hairstyle, layered outfit, several accessories |
| Professional | 150+ | Elaborate costume, complex hair physics, heavy accessorizing |

## Overlap margins

Wherever one piece moves relative to another, the piece underneath needs extra artwork beyond the visible seam so no transparent gap appears during motion. This matters most at: hair→face, head→neck, neck→torso, sleeve→arm, arm→torso, skirt→legs, accessories→hair, and between clothing layers. When you're only assembling already-cut pieces (see SKILL.md), you can't add margin that isn't already in the source art — flag any layer pair that looks tight as a QA warning instead of silently accepting it.
