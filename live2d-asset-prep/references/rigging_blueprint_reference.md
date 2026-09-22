# Rigging Blueprint Reference

Read this when you're writing the LIVE2D_RIG_BLUEPRINT document (the text specification that hands off to whoever does the actual rigging). None of this is rigging itself — it's a recommendation set for a human rigger or a rigging tool to start from.

## Standard parameters to recommend

```
Core:      ParamAngleX, ParamAngleY, ParamAngleZ,
           ParamBodyAngleX, ParamBodyAngleY, ParamBodyAngleZ
Eyes:      ParamEyeLOpen, ParamEyeROpen, ParamEyeBallX, ParamEyeBallY
Brows:     ParamBrowLY, ParamBrowRY, ParamBrowLAngle, ParamBrowRAngle
Mouth:     ParamMouthOpenY, ParamMouthForm
Breathing: ParamBreath
```
Suggest additional custom parameters only when the character has something the standard set doesn't cover (e.g. a tail, extra ears, a floating object).

## Physics blueprint format

For each component that should get physics (typically: front/side hair, hair specials, ribbons, skirts, capes, dangling earrings/necklaces), record:

```
PHYSICS_GROUP: <name>
SOURCE_PARAMETER: <what drives it, e.g. ParamAngleX>
TARGET_LAYER: <layer name>
INTENSITY: <rough 0-1 suggestion>
RESPONSE_SPEED: <rough qualitative: slow/medium/fast>
DAMPING_RECOMMENDATION: <rough qualitative: light/medium/heavy>
```
Label these clearly as **initial recommendations**, not calibrated values — actual physics tuning happens inside Cubism with the live model.

## Expression system

Minimum useful set: `NORMAL, HAPPY, SAD, ANGRY, SURPRISED`. Add more only where the character's personality/design supports it — don't force a fixed list onto every character. Common additions: `CONFUSED, EMBARRASSED, EXCITED, TIRED, SERIOUS, SMUG, WORRIED, SHOCKED, SLEEPY, FOCUSED`. Every expression must keep face structure, eye design, hairstyle, and accessories identical to the base — only the emotional read changes.

## Phoneme map

Map mouth shapes to the five standard vowel states plus neutral/closed: `A, I, U, E, O, Neutral/Closed`. Only include mouth sub-parts (teeth, tongue) that are visible on the character's actual design.

## AI interaction state map (optional, include only if the character is meant for interactive/VTuber use)

```
IDLE      → normal expression, random blink, breathing, minor hair physics
LISTENING → eyes toward user, slight head-attention movement
THINKING  → eye direction shift, thinking expression, reduced mouth movement
SPEAKING  → phoneme lip sync, subtle head movement, natural blinking
WORKING   → focused expression
SUCCESS   → happy expression
CONFUSED  → confused expression
ERROR     → concerned/surprised expression
```
Keep the animation intensity proportional to the character's personality — a reserved character shouldn't get exaggerated motion just because a state exists.

## Motion stress test (do this as a thought experiment, not a literal simulation)

For each of these, ask "would moving this reveal missing artwork or a bad seam?" and note it as a QA warning if the answer might be yes, given what you can actually see in the source art:

`HEAD LEFT/RIGHT/UP/DOWN/TILT, EYES LEFT/RIGHT/CLOSED, MOUTH OPEN, BODY LEAN LEFT/RIGHT, HAIR SWING, ARM MOVE`

## Blueprint document structure

When you write the final LIVE2D_RIG_BLUEPRINT, include these sections: `CHARACTER` (identity summary), `LAYER_TREE`, `MOVABLE_PARTS`, `PARAMETER_MAP`, `PHYSICS_GROUPS`, `EXPRESSION_MAP`, `PHONEME_MAP`, `AI_STATE_MAP` (if applicable), `KNOWN_LIMITATIONS`, `QA_WARNINGS`.
