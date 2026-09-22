# Artifact Control and Verification

Run this before delivering the prompt, and again on any generated image. It covers **anatomy QC, hair QC, clothing physics, prevention of common generation failures, and the final self-check**.

## Contents
1. Anatomy checklist
2. Hair construction and checklist
3. Clothing physics
4. Common artifact risks
5. Final self-check
6. Correction loop

---

## 1. Anatomy checklist

Explicitly check the planned pose against:

- Head-to-body proportion (matches the reference's stylization level)
- Shoulder structure
- Elbow position
- Wrist direction
- Hand anatomy and finger count
- Hip alignment
- Knee orientation
- Ankle structure
- Foot placement and ground contact

Do not sacrifice anatomy for decorative complexity. If a pose forces a risky hand or foot configuration, change the pose (hide the hand in a sleeve, rest it on a prop, turn the foot) before adding more negative-prompt terms.

---

## 2. Hair construction and checklist

Hair is a major identity feature. Describe and check it as a hierarchy:

```
PRIMARY MASS → SECONDARY LOCKS → INDIVIDUAL STRANDS → FLYAWAY STRANDS
```

Maintain:
- Coherent hair direction (flow follows head shape and pose)
- Believable attachment to the scalp and hairline
- Consistent volume from the reference
- Controlled strand density

Avoid: "spaghetti hair," random disconnected strands, excessive strand noise, hair growing from the wrong place, hair color drifting between sections.

Prompt tip: describe hair by its **mass and locks** ("long straight mass with two face-framing sidelocks and blunt bangs"), then add a small, controlled amount of flyaway ("a few loose strands catching the rim light").

---

## 3. Clothing physics

Clothing must respond to gravity, body movement, wind, fabric weight, and material stiffness.

- Long sleeves, ribbons, skirts, and capes should share **one coherent flow direction** (wind or motion), not float independently.
- Heavy fabrics (brocade, leather) fall in fewer, larger folds; light fabrics (chiffon, tulle) billow and layer.
- Folds gather at joints and where fabric is pulled or pinned.
- If there's wind, state its direction once and make hair and cloth agree.
- Trailing elements attach at their real anchor point (a ribbon must start at the bow, not from nowhere).

---

## 4. Common artifact risks

Track which of these apply to this particular character; they feed the negative prompt (`templates/negative-prompt.md`):

- Extra, missing, or fused fingers; malformed hands
- Asymmetrical eyes (unintended)
- Duplicated accessories (two circlets, doubled earrings)
- Floating ornaments not attached to anything
- Broken limbs, impossible joints
- Disconnected or melted clothing
- Tangled hair
- Random symbols or text
- Inconsistent costume colors
- Excessive bloom or sharpening
- Plastic skin
- Noisy or over-detailed background competing with the character
- Accidental text, watermark, logo
- Low-resolution facial details
- Duplicated objects
- Inconsistent perspective

Flag **character-specific risks** too: an asymmetrical costume tends to get "symmetrized," a complex headpiece tends to duplicate, a held weapon tends to merge into the hand.

---

## 5. Final self-check

Answer every question. A "no" on a critical item means revise the prompt before delivering.

| Area | Question |
|---|---|
| IDENTITY | Can the character still be recognized without the background? |
| SILHOUETTE | Are the major silhouette features preserved? |
| COSTUME | Are the major clothing structures preserved? |
| COLOR | Is the original color language (including temperature) maintained? |
| MOTIFS | Are all items on the Critical Identity List present in the prompt? |
| ANATOMY | Is the pose physically plausible, and are hands low-risk? |
| COMPOSITION | Does the character remain the visual focal point? |
| LIGHTING | Does the lighting have one consistent direction, with sourced glow? |
| MATERIAL | Do different materials behave differently? |
| BACKGROUND | Does the environment support rather than overpower the character? |
| ARTIFACTS | Are the common failures for this character explicitly controlled? |

---

## 6. Correction loop

If you have generated an image (or the user shows you one), compare it against the Critical Identity List item by item.

1. Identify what drifted (color, silhouette, accessory, asymmetry, anatomy).
2. Locate which prompt sections govern it (hair → HAIR section; missing emblem → DISTINCTIVE MOTIFS).
3. Strengthen that section: move the item earlier, make it more specific, or add a positive-phrased reinforcement ("left sleeve long, right sleeve short").
4. Only add negative terms for genuinely new artifacts; do not pile on generic ones.
5. Change one or two things per iteration so you can see what worked.
