---
name: model-review
description: Review a Born Nobody simulation model, rule or mechanism for coherence, causality, realism and evidence — not code style, test coverage or module boundaries. Use whenever the user asks whether a model makes sense, asks for feedback on a model, reviews a PR that changes a rule or mechanism, compares a near rule with its far twin, or wants the economy, society, war, trade, movement, fight or any other model judged against the world it claims to simulate. Report findings and experiments; never edit the code.
---

# Model review

## Purpose

This is a manual review skill, not a PR certificate. The bornnobody gate does not load it; the gate names its skills and pins a commit in `.github/workflows/pr-dev.yml`.

A model is a rule or system that turns state into a decision or a number: a fight's blow, a household's meal, a leader's raid, a
price, a route, a birth. Review it as **a claim about the world** and as **a contract with the rest of the simulation**, not as a
piece of code style.

This skill is read-only. It reports findings, questions and experiments. It never edits a model, a config, a test or a document.

## Inputs

Read only what the model needs:

- the model's code and its input/output parcels;
- the design plan section and any ruling that introduced it;
- `docs/architecture.md` for the kind and the one path to a verb;
- `docs/world-rules.md`, `docs/realism-targets.md` and the glossary;
- the tests: unit, property, BDD and the measured bands;
- `docs/code-map.md` for the feature's place and its events;
- the diff, when the review is of a change (`git diff <base>...HEAD`).

For a model with measured figures, read the measurement, not just the test name: seeds, sample size, tolerance, and the date the
band was installed.

## Procedure

### 1. State the model in one paragraph

Write, before judging:

- **Question:** what decision or quantity does it produce?
- **Inputs:** what state and constants does it read?
- **Mechanism:** how does it turn them into the output?
- **Output:** what does it return, and who applies it?
- **Scope:** what does it deliberately ignore?

If you cannot state it in a paragraph, that is the first finding: the model's claim is not clear.

### 2. Check the causal chain

Trace one case end to end:

```text
state and cues -> decision -> action -> consequence -> next state
```

Look for:

- the model reading the outcome it is supposed to produce, or reading another person's private action;
- a decision that is declared rather than produced by the mechanism;
- a hidden second clock, a wall clock, or a per-frame delta in sim code;
- a coefficient that has no unit, no source and no range;
- a rule that depends on iteration order or on a hash map;
- a result that is applied before every contact has been resolved.

### 3. Check the evidence

- Are the coefficients sourced, measured or explicitly named as a first guess?
- Is the sample large enough, and are the seeds and the tolerance stated?
- Is the measured band fresh? A stale measurement is a finding.
- Is there a **far twin** for a near rule, with its own test and tolerance?
- Does the model hit a realism target, or is it only self-consistent?
- What observation would falsify it? If nothing would, the model is not yet a model.

### 3b. Check the model against its picture

The client draws the same numbers the rule reads. Compare them:

- Does the reach the brain measures equal the hand plus the blade the pose draws? A rule that measures 1.7 m while the
  drawn sword reaches 1.6 m will miss at the top of its own measure band.
- Is every key hand inside the arm's reach? A parry at knee height puts the hand 1 m below the shoulder; the two-bone IK
  clamps the reach but the drawn forearm runs to the real hand, and the arm stretches to 0.8 m. A low line is a block
  with a crouch or a step, not a sword parry.
- Does the blade keep one length, and does it stop at the body, blade or shield it met? A sword that stretches, or comes
  out of a man's back, is a model and picture disagreeing.
- Does the shield the pose holds in front of the body appear in the swept boxes? A shield that a blade passes through is
  decoration, not a defence.
- Does a man at the knockout line stop acting and go down, or does he keep fencing at zero health?
- If he does go down, does the scene hold the result and start the next bout, or does the same crouch stay on screen?
- Does the HUD show the state the rule is in, or a stale or impossible value?

A picture that lies about the rule is a modelling finding, not a drawing finding.

### 4. Check the behaviour

Try the edges:

- zero, negative, one, and a very large value;
- an empty group, one person, a leaderless group, a dead leader;
- two equal candidates, a tie, a missing id;
- a feedback loop: can it explode, collapse, oscillate, or lock?
- an incentive: can a person or group game it in an unintended way?
- path dependence: does the order of two events change the result?
- saturation: what stops a value running away?

A model that is only checked at the average is not checked.

### 5. Check the tests

- Does the test assert **behaviour**, or only pin a constant or a hash?
- Is the scene plain English, one behaviour, about ten lines, and over several seeds?
- Does a property law exist for each pure rule?
- Is the measured gate a fresh sample of the model, not a re-pin of an old one?
- Was a test deleted, disabled or weakened? Say so; do not approve it.
- Does the test run through the scenario builder or the feature's own harness, as the kind requires?

### 6. Check the documentation

- Is the feature and its owner in `docs/glossary.md`?
- Is the feature in `docs/code-map.md`?
- Does the design plan or a ruling explain **why** this model, not only what it does?
- Are the code anchors and the config names current?

## Output

```markdown
MODEL: <name>
QUESTION: <one sentence>
MECHANISM: <one paragraph>
VERDICT: SOUND | NEEDS WORK | INSUFFICIENT EVIDENCE

SOUND:
- <what is well founded, with evidence>

FINDINGS:
- [Critical|Important|Minor] file:line — finding — evidence — why it matters
  Experiment: <the smallest observation that would settle it>

A useful recent example: "the pose places the tip on a circle of `weapon.reach` while the hilt moves, so the blade
stretches from 0.7 to 2.25 m through a swing; the contact sweep reads the same segment, so a blow's speed and its
contact point are not the blow the picture shows. Experiment: sample the hilt-to-tip length at 40 phases of one action."

QUESTIONS:
- <a question the model does not answer>

EXPERIMENTS:
- <a named sample, seed set, comparison or measurement that would test the claim>
```

- **Critical:** the model cannot be trusted to produce the behaviour it claims, or it breaks a non-negotiable rule.
- **Important:** the model works but its evidence, edge cases or twin are missing; fix before relying on it.
- **Minor:** clarity, naming, a missing explanation.
- `SOUND` means the mechanism and evidence are adequate for the claim; it does not mean the design choice is Paul's favourite.
- `INSUFFICIENT EVIDENCE` is the honest verdict for a plausible model with no measurement.

## Rules

- Quote the file and line, the test, or the measured figure. A finding without evidence is an opinion.
- Separate **what the model does** from **what you would prefer**; the second is advice.
- Do not invent a source, a band, a seed set or a measurement.
- Do not edit code, config, tests or docs.
- Do not approve a design question that is Paul's; state the question and the cost of each answer.
- Do not review formatting, detekt, ktlint, test coverage, module imports or guard loosening; other skills own those.
- Do not review animation or drawing as such; `animation-review` owns those, its `fight.md` the fighting part. Do report when the
  drawn picture and the rule disagree, because that is a model claim failing its own evidence.
