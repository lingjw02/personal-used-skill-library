# Composition

This file covers **pose reconstruction, camera and framing, environment, and depth**. These are mostly Tier 4 decisions: this is where the new illustration is allowed to differ most from the reference, as long as it stays compatible with the character design.

## Contents
1. Pose reconstruction
2. Camera
3. Framing
4. Environment
5. Depth layers
6. Choosing based on the request

---

## 1. Pose reconstruction

Do not blindly copy the reference pose. Reference poses are often static, cropped, or awkward. Decompose it, then design a better one.

**Decompose:**
- Gesture (the one-line feeling of the pose: "reaching," "waiting," "mid-step")
- Center of gravity and weight distribution
- Head direction
- Shoulder angle
- Hip direction
- Arm and hand position and gesture
- Leg positioning
- Fabric movement, hair movement

**Then create a new pose that:**
- Keeps every Tier 1 feature visible (see `character-identity.md`)
- Shows the silhouette-defining elements clearly (don't hide the asymmetrical sleeve behind the body)
- Is anatomically plausible with a believable weight distribution
- Has a clear, readable line of action

**Avoid:** twisted joints, broken wrists, disconnected limbs, unnatural fingers, impossible weight distribution, excessive body bending. Hands are the highest-risk area: prefer poses where hands are relaxed, holding a simple prop, or partly covered by sleeves over complex finger gestures.

Describe the pose in plain anatomical terms ("weight on the right leg, left knee slightly bent, torso turned three-quarters to the viewer, right hand holding the staff at chest height") rather than abstract ones ("dynamic pose").

---

## 2. Camera

Pick one and state it:

- Full-body
- Three-quarter body (head to mid-thigh)
- Medium shot (head to waist)
- Bust / portrait
- Angle: eye level, slight low angle (heroic, taller), slight high angle (softer, smaller)
- Optional slight elevation for showing costume layers and skirts

A low angle exaggerates capes and skirts and reads as powerful; an eye-level three-quarter is the safest default for costume readability.

---

## 3. Framing

Prefer:
- A clear, uncluttered silhouette against the background
- Sufficient headroom
- Sufficient footroom for full-body shots (cropped feet are a common failure; say "feet and footwear fully visible with ground contact" if it matters)
- Controlled negative space
- Readable costume layers

For a character illustration, **character readability beats background complexity**. If the two conflict, simplify the background.

---

## 4. Environment

Do not add scenery at random. The environment should reinforce:

- Character theme
- Color palette (support it, or contrast it in a controlled way so the character pops)
- Narrative atmosphere
- Costume symbolism
- Lighting direction

Examples of theme-to-environment mapping:

| Character type | Good environment directions |
|---|---|
| Fantasy princess | Palace hall, cathedral-like architecture, magical garden, moonlit terrace, enchanted courtyard |
| Mystical character | Ruins, floating particles, magical symbols, ethereal fog, celestial sky |
| Warrior / knight | Battlement at dawn, ruined bridge, snowy pass, banner-lined hall |
| Everyday/school setting | Rooftop at sunset, classroom window light, cherry-blossom street |

The environment must never compete with the character: lower its contrast, saturation, and detail near the character's edges.

---

## 5. Depth layers

Build the image in layers:

```
FOREGROUND → MIDGROUND → CHARACTER → BACKGROUND → DISTANT BACKGROUND
```

Tools:
- Atmospheric perspective (distant elements lighter, cooler, lower contrast)
- Depth of field (soft foreground and far background, sharp character)
- Overlapping objects (a foreground branch or railing partly overlapping the frame edge)
- Scale variation
- Controlled blur (never on the character's face or key motifs)

The character must remain the primary focal point. Foreground elements are for framing and depth, not for covering the character.

---

## 6. Choosing based on the request

- **User named a scene** → use it, and adapt pose/camera/lighting to fit while preserving identity (see Adaptation rule in `SKILL.md`).
- **User said "polish/improve this"** → keep the general intent of the reference pose and camera but fix anatomy, strengthen the silhouette, and enrich the environment modestly.
- **User gave no direction** → default to a three-quarter or full-body shot, eye level or slight low angle, a theme-supporting environment with a soft-focus background, and a natural relaxed pose.
