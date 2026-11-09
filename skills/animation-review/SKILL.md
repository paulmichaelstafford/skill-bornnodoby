---
name: Animation Review
description: Review a Born Nobody client scene's animation and movement for weight, grounding, joints, silhouettes, timing, props, draw order and camera. Use whenever a scene looks stiff, floaty, sliding, disconnected, a limb passes through a body, a foot skates, a pose is unreadable, or the user asks to make a walk, work, crowd, training or sparring scene look like real bodies. It reviews poses and drawing, never combat rules or simulation outcomes.
---

# Animation review

## Purpose

This is a manual review skill, not a PR certificate. The bornnobody gate does not load it; the gate names its skills and pins a commit in `.github/workflows/pr-dev.yml`.

Make the drawn bodies read as bodies: weight on the ground, joints that bend, a silhouette that says what the person is doing, and
a camera that shows it. This skill covers any client scene — walking, working, carrying, fighting, a crowd. The fighting-specific
readability (guard, wind-up, parry, riposte) is `fight-pose-review`; combat contact is not this skill's concern.

Report findings and propose changes. Do not edit code, tests or contact logic.

## Inputs

- A video of the scene at 10–15 seconds.
- A contact sheet at 2–4 frames a second.
- The pose source: `FightPose`/`TrainingPose` and `TrainingShape` for the near scenes, `BodyFrame` for the world's bodies.
- The renderer and the scene's camera.
- The HUD names the state; use it to label frames.

Take frames at the moments that matter, not only the nicest frame.

## The review order

### 1. Grounding and weight

- One foot is planted while the body moves; the other steps.
- The hips are over the support foot, not floating between both.
- A step changes the feet before the torso arrives; the torso does not slide over still feet.
- The knees bend; a straight column reads as a mannequin.
- A planted foot's box bottom is at the floor, not through it.
- A carrying or working body leans into the load; it does not stay upright.

### 2. Joints and the arm chain

- Shoulder → elbow → wrist → hand; hip → knee → ankle → foot.
- The elbow and knee are not optional; a single straight box reads as a stick and can pass through the body.
- The shoulder sits outside the torso silhouette; the hip sits inside it but the thigh leaves it.
- The hand is on the hilt, tool or load; the shield is on the forearm.
- No part intersects another. This is a pose problem: Born Nobody's fight rule has no body self-collision.

### 3. The body and the silhouette

- Head, neck and torso are connected; no floating head.
- The torso twists into a turn, a cut or a lift; it does not stay square.
- The legs and feet are separate enough to read as legs.
- No part passes through the ground.
- The silhouette at the start, the middle and the end of an action is distinguishable.

### 4. Timing and interpolation

- Anticipation, action, recovery; no teleporting between poses.
- The simulation ticks; the renderer may interpolate between ticks, but the brain samples only the tick pose.
- A hold is a hold, not a frozen pose with a missing next frame.
- A step's speed matches its stride; a run is not a walk with a larger translation.
- A contact or carry point stays on the same part through the motion.

### 5. Props, layers and drawing

- The hilt, shield, tool or load is attached to the hand/arm that holds it.
- Draw order: body, then the near arm/shield, then the weapon, then marks; the near side does not disappear.
- A shield is a slab with an arm behind it; not a floating wall.
- A mark, flash or trail is at the contact point, not the middle of the body.
- The camera does not sit inside a body or a shield.

### 6. Camera and framing

- The body fits at the closest and farthest point of the motion.
- The angle shows the motion's line; a motion straight at the camera reads as a dot.
- A near body does not hide the far body's hands or weapon at the contact.
- The HUD names the state without covering the figures.

## Known failure modes

- A `PoseBox` half-size in the wrong axis order: the pose axes are forward, up, right, so a torso's halves are (depth, height, width).
- A shoulder root inside the torso, or one straight box from shoulder to hand.
- A shield centred on the body's width, so its slab overlaps the torso.
- A stride swing too small to read; the walk becomes a slide.
- A torso that stays square through a cut, turn or lift.
- A camera far enough that the action does not read at contact-sheet size.

## Body-intersection gate

Born Nobody's training and sparring BDD tests enable the fight's `auditBodies` flag. `PoseAudit` then throws when an arm box
crosses the torso, head or legs, or when two men's boxes cross. If it throws, fix the pose; do not weaken the audit. It is a
test gate, not collision response, and the client leaves it off.

## Output

```markdown
Issue: <one sentence>
Evidence: <timestamp or frame>; <what is visibly wrong>
Cause: <file/constant or math>
Change: <the pose/IK/drawing change>
Expected: <what the next capture should show>
Gate: <which test or capture proves it>
```

Sort by visual impact. A limb through a body comes before a camera nudge.

## Rules

- Never change the contact rule, the sweep, the damage or a test expectation to make a picture look better.
- Pose data is in `TrainingShape.Geo`/`TrainingPose` or `BodyFrame`; prefer a named constant or a small pose function.
- No physics or ragdoll. The design deliberately has none; fix the pose, not the engine.
- Re-capture after every change and compare the same timestamps.
- Run the scene's tests after a pose change; a visual fix must not break the contact scenes.
- Do not judge combat decisions, model realism or code quality; other skills own those.

## Capture recipe

From the bornnobody root:

```bash
Xvfb :99 -screen 0 1600x1000x24 &
sleep 1
DISPLAY=:99 timeout 30s ./gradlew :client:run --args='--training=1' &
CLIENT=$!
sleep 7
DISPLAY=:99 gst-launch-1.0 -q ximagesrc use-damage=0 num-buffers=360 \
  ! video/x-raw,framerate=30/1 ! videoscale ! video/x-raw,width=1280,height=800 \
  ! videoconvert ! vp8enc deadline=1 cpu-used=8 target-bitrate=2500000 \
  ! webmmux ! filesink location=/tmp/opencode/scene.webm
wait $CLIENT || true
```

Frames and contact sheet, where `SKILL_DIR` is this skill's directory:

```bash
gst-launch-1.0 -q filesrc location=/tmp/opencode/scene.webm \
  ! matroskademux ! vp8dec ! videoconvert ! videorate \
  ! video/x-raw,framerate=2/1 ! pngenc \
  ! multifilesink location=/tmp/opencode/frame-%02d.png
python3 "$SKILL_DIR/contact_sheet.py" \
  '/tmp/opencode/frame-*.png' /tmp/opencode/contact.png
```
