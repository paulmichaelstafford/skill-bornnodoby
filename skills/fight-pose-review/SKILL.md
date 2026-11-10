---
name: Fight Pose Review
description: Review the fighting part of a Born Nobody training or sparring scene: guard readability, wind-up, travel, recovery, parry and block by geometry, feint, riposte, the blade path, the contact point and two-man framing. Use whenever a duel or training fight looks like a guard drill, a blow is unreadable, a parry or block does not read, a blade or contact mark is in the wrong place, a combination does not flow, or the user asks to make a fight look like two people fighting. It never changes the contact rule; for grounding and general body mechanics, use animation-review first.
---

# Fight pose review

## Purpose

This is a manual review skill, not a PR certificate. The bornnobody gate does not load it; the gate names its skills and pins a commit in `.github/workflows/pr-dev.yml`.

Make the fighting read as intent, commitment and contact: a guard that says what can come, a wind-up that can be read, a blade that
travels to the line the body aimed at, a parry or block that meets it, and a recovery that is a choice. Body grounding, joint
chains, silhouettes and camera belong to `animation-review`; run that first. If the body is not grounded, this review cannot save
the fight.

The contact rule is already built. This skill reviews what the fight **looks like**; it never changes `Sweep`, damage, a test
outcome or a decision rule.

## Inputs

- A video and contact sheet of `--training=1` or `--sparring=1`.
- `TrainingPose.kt`, `TrainingShape.kt`, `TrainingBrain.kt`, `Guard.kt`, `TrainingFight.kt`/`SparringFight.kt`.
- The HUD: guard, phase, blows, hits, gap, health, training level.
- The contact points from `SweepHit` and the scene's marks.

## Review order

### 1. The guard

- The guard is readable before the blow: high, low, centre, forward, one.
- A guard change is a committed action; it takes time and the pose shows the change.
- A guard is a trade, not a decoration: the blows it leads to are quicker; a low guard's cut has to rise.
- The HUD and the pose agree.

### 2. The blow

- The wind-up is readable before the blade travels; the travel is readable before the contact; the recovery is visible.
- A cut traces an arc; a thrust stays on its line.
- The hilt is at the sword hand at every sampled phase. A floating blade or a hilt inside the body is a Critical finding.
- **The blade is one rigid length.** The tip is at hilt + direction × length at every phase; a wind-up that pulls the hilt
  back while the tip stays on a circle of "reach" stretches the sword. A length that changes through the swing is a
  Critical finding; `the blade keeps one length through the swing` is the gate.
- **A landed blade stops at what it met.** The drawn tip is the action's recorded stop (body, parry blade or shield), not
  the full point; a sword that comes out of a man's back is a Critical finding. `FightPose.drawnTip()` is the reader.
- The blade line is the line the body aimed at; a blow that visibly goes wide or short is a miss, not a hit.
- The training man's first blow comes from the guard he came to the post in; later blows may change guard first.

### 3. Contact

- The hit is at the point `Sweep` found, on the part it found; the mark is at that point.
- A parry is a blade meeting a blade: the parry blade is across the incoming line, from the near side of the body, and is up in time.
- A block is a shield meeting a blade on the line it covers; the shield arm stays behind the shield.
- **A shield at guard is still a shield.** It covers the line it stands on, and a sword does not pass through it. Only a
  committed parry makes the sword (not the shield) the answer to that line; the two are not the same defence.
- **A defence sets; it does not teleport.** The parry blade and the shield ease from the guard pose to the parry line or
  block height over the action's set time. A shield that jumps from the hip to the line in one frame is a snap, not a
  block.
- **A low line is not a sword parry.** The hand cannot reach knee height from the shoulder; the parry is high or middle,
  a low line is a shield block with a crouch (or a step). A low parry is a stretched forearm.
- A late parry visibly misses; a parry on the wrong line does not stop the blow.
- A miss is visibly short or wide, and the recovery follows the miss.
- Damage is seen after the contact, not before it.

### 4. Timing and intent

- Approach, measure, circle, strike: the man only strikes in measure.
- A trained combination changes the act and the line; the next link starts before the previous recovery ends.
- A recruit throws one blow and resets; a trained man flows.
- A blown man withdraws and breathes before he strikes again.
- A faster defender's reaction gets the parry up; a slower one is hit.
- A feint's wind-up looks like a blow until the pull; the real blow takes the line the parry left open.
- A riposte starts while the attacker is still recovering.
- A parry or block abandons the attacker's plan; the combination does not continue stale.

### 5. Two men

- The gap is a fighting measure, not a hug or a corridor.
- The feet step; the bodies do not slide through each other. Run `animation-review` and the `auditBodies` gate for intersection.
- Both blades are visible at the contact frame; the near man does not hide the far man's weapon.
- The shield does not hide the line the blow is taking.
- The camera shows the line of the exchange and keeps both men at the closest and farthest measure.

## Known fight failure modes

- The guard and the wind-up are the same pose, so the blow is unreadable.
- The blade stretches and shrinks because the tip is placed on a reach circle while the hilt moves; the sword is rubber.
- The parry hilt is on the far side of the body, so the sword arm crosses the chest.
- The shield is a large slab that hides the arm and the line, or a slab the blade passes through.
- Blades stay crossed at head height; the scene reads as a guard drill.
- The contact mark is at the body's middle, not at the sweep point.
- A miss and a hit have the same recovery, so the miss does not read.
- A combination continues after a parry or block.
- A feint's real blow repeats the feint's line.
- A hit leaves no answer: no flinch, no recoil, no guard reset.
- A man at the knockout line keeps fencing.
- A one-handed sword is held with both hands near the hilt in the guard and only one hand on the strike; the grip changes
  between phases. A free hand stays at the hip, or both hands stay on a two-handed hilt.
- A bout that ends (down, dead, broken) leaves the same crouched pose on screen for the rest of the video; the scene needs
  a beat and a next bout or a cut.
- The camera is too far, too side-on, or behind the man, so the blade's line is hidden or the back is the view. A camera
  that follows the line's rotation hides the circling.

## Output

```markdown
Issue: <one sentence>
Evidence: <timestamp or frame>; <what is visibly wrong>
Cause: <file/constant or math>
Change: <the pose/action/drawing change>
Expected: <what the next capture should show>
Gate: <which test or capture proves it>
```

Sort by impact. A blade or contact error comes before a camera nudge.

## Rules

- Never change the contact rule, the sweep, the damage or a test expectation to make a picture look better.
- Run `animation-review` first for grounding, joints, self-intersection and camera; this skill owns the fighting part.
- The training/sparring BDD scenes enable `auditBodies`; if `PoseAudit` throws, fix the pose, not the audit.
- Pose data is in `TrainingShape.Geo`, `BladeKeys` and the `TrainingBody`/`TrainingBlade`/`TrainingLimbs` split; prefer a
  named constant or a small pose function.
- Keep the pose's full `bladeTip` for the sweep and the length test; clip only the drawn tip at `bladeStop`.
- No physics or ragdoll. The design deliberately has none; fix the pose, not the engine.
- Re-capture after every change and compare the same timestamps.
- Run `TrainingScenesTest`, `SparringScenesTest` and the client renderer test after a change. The new gates include
  the blade length, the step-in, the contact stop, the elbow, the legs, the flinch, the guard shield and the down state.

## Capture recipe

From the bornnobody root:

```bash
Xvfb :99 -screen 0 1600x1000x24 &
sleep 1
DISPLAY=:99 timeout 30s ./gradlew :client:run --args='--sparring=1' &
CLIENT=$!
sleep 7
DISPLAY=:99 gst-launch-1.0 -q ximagesrc use-damage=0 num-buffers=360 \
  ! video/x-raw,framerate=30/1 ! videoscale ! video/x-raw,width=1280,height=800 \
  ! videoconvert ! vp8enc deadline=1 cpu-used=8 target-bitrate=2500000 \
  ! webmmux ! filesink location=/tmp/opencode/sparring.webm
wait $CLIENT || true
```

Use `--training=1` for the post. Frames and contact sheet:

```bash
gst-launch-1.0 -q filesrc location=/tmp/opencode/sparring.webm \
  ! matroskademux ! vp8dec ! videoconvert ! videorate \
  ! video/x-raw,framerate=2/1 ! pngenc \
  ! multifilesink location=/tmp/opencode/frame-%02d.png
python3 "$SKILL_DIR/contact_sheet.py" \
  '/tmp/opencode/frame-*.png' /tmp/opencode/contact.png
```
