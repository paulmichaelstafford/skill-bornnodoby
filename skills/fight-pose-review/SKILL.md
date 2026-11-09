---
name: Fight Pose Review
description: Review a Born Nobody training or sparring scene for realistic human movement and strikes, using video frames, contact sheets and the pose source. Use whenever a fight looks stiff, floaty or reads wrong, a limb passes through a body, a weapon floats free, a foot skates, a guard or strike is unreadable, or the user asks to make the training dummy or a duel look like two real people fighting. This skill proposes pose and drawing changes; it never changes the contact rule.
---

# Fight pose review

## Purpose

Make one man against a post, and then two men sparring, read like bodies with weight, joints and intent. The contact rule is already built; this skill reviews the **body**, the **weapon** and the **camera**. It does not judge game design, damage, or whether a blow should land.

The model can look at images. Take frames at the moments that matter, not only the nicest frame.

## Requirements

- Born Nobody's client (`./gradlew :client:run --args='--training=1'` or `--sparring=1`).
- `Xvfb`, GStreamer with `ximagesrc`, `vp8enc` and `webmmux`, Python with Pillow.
- The pose source: `sim-verbs/.../training/internal/TrainingPose.kt` and `TrainingShape.kt`, and the client renderer.
- The HUD names each man's guard and phase; use it to label the frames.

Run commands from the bornnobody repository root. `contact_sheet.py` sits beside this file.

## The review order

Work in this order; a later pass cannot save a body that is not grounded.

### 1. Grounding and weight

- One foot is planted while the body moves; the other steps.
- The hips are over the support foot, not floating between both.
- A step changes the feet before the torso arrives; the torso does not slide over still feet.
- The legs bend a little at the knee; a straight column reads as a mannequin.
- A planted foot's box bottom is at the floor, not through it.

### 2. The arm chain

- Shoulder → elbow → wrist → hilt. The elbow is not optional; a single straight box from shoulder to hand reads as a stick and can pass through the torso.
- The shoulder sits outside the torso silhouette.
- The sword hand is on the hilt; the blade must not float free.
- The shield hand is on the shield's back; the shield must not float away from the arm.
- No arm box intersects the torso, head or legs. This is a pose problem: the fight rule has no body self-collision.
- The off arm counterbalances; it does not hang dead unless the man is exhausted.

### 3. The blade

- The hilt is at the sword hand at every sampled phase.
- The wind-up puts the blade behind the line; the travel puts it through the target; the recovery returns it to guard.
- A cut traces an arc, not a straight line; a thrust stays on its line.
- The contact point is the point the sweep found, and the mark is at that point.
- A parry brings the blade across the incoming line from the **near** side of the body; a parry held across the chest is an arm-through-body bug.
- A shield block moves the shield to the line and keeps the shield arm behind it.

### 4. The body

- Head, neck and torso are connected; no floating head.
- The torso twists into a cut and follows through; it does not stay square.
- The legs and feet are separate enough to read as legs.
- No part intersects another; no part passes through the ground.
- The silhouettes at guard, wind-up and strike are distinguishable.

### 5. Timing and intent

- The guard is readable before the wind-up.
- The wind-up is readable before the blade travels.
- The recovery is visible; a trained combination flows, a recruit resets.
- A parry is a committed action with its own set time; a late parry visibly misses.
- A feint's wind-up looks like a blow until the pull, then the real blow takes the open line.
- A riposte starts while the attacker is still recovering.

### 6. Camera and framing

- Both men fit in the frame at the closest and farthest measure.
- The camera is not inside a body or a shield.
- The near man does not hide the far man's weapon at the contact.
- The angle shows the blade's line; a blade pointing straight at the camera reads as a dot.
- The HUD names the state without covering the figures.

## Known failure modes

Check these first; each has already happened in this project.

- The sword arm was one straight box from shoulder to hilt, and the shoulder sat inside the torso.
- A parry hilt was placed on the far side of the body, so the arm crossed the chest.
- The shield was a large slab that hid the shield arm and read as part of the torso.
- The feet swung too little to read as a step; the walk looked like sliding.
- The torso stayed square while the blade travelled.
- The camera sat far enough that the action did not read at contact-sheet size.

## Output

For each issue:

```
Issue: <one sentence>
Evidence: <timestamp or frame>; <what is visibly wrong>
Cause: <file/constant or math>
Change: <the pose/IK/drawing change>
Expected: <what the next capture should show>
Gate: <which test or capture proves it>
```

Sort by visual impact. Do not put a cosmetic issue above a limb through a body.

## Rules

- Never change the contact rule, the sweep, the damage or a test expectation to make a picture look better.
- Pose data is in `TrainingShape.Geo` and `TrainingPose`; prefer a named constant or a small pose function.
- No physics or ragdoll. The design deliberately has none; fix the pose, not the engine.
- Re-capture after every change and compare the same timestamps.
- Run the training and sparring tests after a pose change; a visual fix must not break the contact scenes.

## Capture recipe

Video, from the bornnobody root:

```bash
Xvfb :99 -screen 0 1600x1000x24 &
sleep 1
DISPLAY=:99 timeout 30s ./gradlew :client:run --args='--training=1' &
CLIENT=$!
sleep 7
DISPLAY=:99 gst-launch-1.0 -q ximagesrc use-damage=0 num-buffers=360 \
  ! video/x-raw,framerate=30/1 ! videoscale ! video/x-raw,width=1280,height=800 \
  ! videoconvert ! vp8enc deadline=1 cpu-used=8 target-bitrate=2500000 \
  ! webmmux ! filesink location=/tmp/opencode/training.webm
wait $CLIENT || true
```

Use `--sparring=1` and a `sparring.webm` path for the duel.

Frames and contact sheet, where `SKILL_DIR` is this skill's directory:

```bash
gst-launch-1.0 -q filesrc location=/tmp/opencode/training.webm \
  ! matroskademux ! vp8dec ! videoconvert ! videorate \
  ! video/x-raw,framerate=2/1 ! pngenc \
  ! multifilesink location=/tmp/opencode/frame-%02d.png
python3 "$SKILL_DIR/contact_sheet.py" \
  '/tmp/opencode/frame-*.png' /tmp/opencode/contact.png
```

Read the contact sheet, pick the 3–6 frames that show the issue, and read those full-size.
