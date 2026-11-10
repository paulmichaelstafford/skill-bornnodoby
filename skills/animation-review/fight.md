# The fight chapter

Part of `animation-review`. Run the body checks in `SKILL.md` first — grounding, joints, silhouette, timing, props, camera —
then these. A training or sparring scene is one review; this chapter only adds what the exchange must read as.

It reviews what the fight **looks like**. It never changes `Sweep`, damage, a decision rule or a test outcome.

## Inputs

- The same video and contact sheet as `SKILL.md`.
- `TrainingPose.kt`, `TrainingShape.kt`, `TrainingBrain.kt`, `Guard.kt`, `TrainingFight.kt`/`SparringFight.kt`.
- The HUD: guard, phase, blows, hits, gap, health, training level.
- The contact points from `SweepHit` and the scene's marks.

## 1. The style and the guard

A weapon fights in styles, and a style is a culture's way of fighting before it is a technique. European sword fighting has the
German Longsword; Japanese sword fighting has Kenjutsu. The same weapon family can hold both, and the two must not stand
alike. A style is a stance, a grip, a footwork and a trade: the line the blade holds, the blow it leads to and the line it
gives up.

- **German Longsword**: tall and bladed, both hands together on the hilt, the high guard above the head; long cuts and
  thrusts, and a step into the blow.
- **Kenjutsu**: lower and side-on, both hands on the hilt, the blade forward at chest height; the first cut is decisive, the
  thrust is rare.

The stance carries the style: the lead foot, the hips and the bladed torso say the line before the sword does. The styles must
not be the same silhouette with the hand moved; the feet, height, grip, blade line and free hand all change. A style change
is a committed action, and the new style is set at the change's end.

The stance carries the style: the lead foot, the hips and the bladed torso say the line before the sword does. The two must
not be the same silhouette with the hand moved; the feet, height and blade line all change. A style change is a committed
action, and the new style is set at the change's end.

- The guard is readable before the blow: high, low, centre, forward, one.
- A guard change is a committed action; it takes time and the pose shows the change.
- A guard is a trade, not a decoration: the blows it leads to are quicker; a low guard's cut has to rise.
- The HUD and the pose agree.

## 2. The blow

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

## 3. Contact

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

## 4. Timing and intent

- Approach, measure, circle, strike: the man only strikes in measure.
- A trained combination changes the act and the line; the next link starts before the previous recovery ends.
- A recruit throws one blow and resets; a trained man flows.
- A blown man withdraws and breathes before he strikes again.
- A faster defender's reaction gets the parry up; a slower one is hit.
- A feint's wind-up looks like a blow until the pull; the real blow takes the line the parry left open.
- A riposte starts while the attacker is still recovering.
- A parry or block abandons the attacker's plan; the combination does not continue stale.

## 5. Two men

- The gap is a fighting measure, not a hug or a corridor.
- The feet step; the bodies do not slide through each other. `PoseAudit` (the `auditBodies` gate) must stay green.
- Both blades are visible at the contact frame; the near man does not hide the far man's weapon.
- The shield does not hide the line the blow is taking.

## Fight failure modes

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

## Rules

- Never change the contact rule, the sweep, the damage or a test expectation to make a picture look better.
- The body checks and their rules in `SKILL.md` apply unchanged; this chapter adds the fight-specific ones.
- Keep the pose's full `bladeTip` for the sweep and the length test; clip only the drawn tip at `bladeStop`.
- Pose data is in `TrainingShape.Geo`, `BladeKeys` and the `TrainingBody`/`TrainingBlade`/`TrainingLimbs` split; prefer a
  named constant or a small pose function.
- No physics or ragdoll. The design deliberately has none; fix the pose, not the engine.
- Re-capture after every change and compare the same timestamps.
- Run `TrainingScenesTest`, `SparringScenesTest` and the client renderer test after a change. The gates include the blade
  length, the step-in, the contact stop, the elbow, the legs, the flinch, the guard shield and the down state.
