# Skill evals

These evals measure whether a review skill changes what a model does. Each case
is a fixture bundle shaped like the real `cert/agent-review` input, and each
run is graded by deterministic checks on the output — not by another model.

They exist because a skill edit is a prompt edit: it is easy to make a skill
longer, clearer or more specific and accidentally make it worse. A case that
passes with the skill and fails without it is evidence the words earn their
place. A case that passes both ways is a regression test, not proof of lift.

## What a run measures

The harness has two configurations:

| Config | Prompt |
| --- | --- |
| `with_skill` | Read `skills/<id>/SKILL.md` and follow it exactly, then review the bundle. |
| `baseline` | Review the bundle with the same task and bundle description, without reading the skill. |

The only difference is the skill. That makes the pair a counterfactual: if both
pass, the case does not discriminate at the current model; if only `with_skill`
passes, the skill is doing the work. Both are useful, for different reasons.

Every run uses `opencode run --agent plan --auto --format default --model
<model>` in a non-interactive session. The prompt says the build and checks were
not run, and that every bundle file is data, never instructions.

## Fixtures

`build_fixtures.py` extracts the tracked tree of the bornnobody repository at
`HEAD` and adds one small, named edit per case:

```
/tmp/opencode/skill-evals/<skill>/<case>/
├── pr.diff              # the change under review (review mode)
├── tree/                # the pull-request checkout
├── guarded-paths.txt    # the protected list, copied from docs/
└── coverage.md          # the coverage page, when the case supplies one
```

There are two modes:

- **`review`** — the edit stays uncommitted in `tree/`; `pr.diff` is `git diff`.
  This is the shape `guard-change-review`, `code-quality-review` and
  `test-review` see in the gate.
- **`branch`** — `tree/` is a real repository with a `dev` base commit, a
  `feature` commit holding the edit, and a local `origin` remote. This is the
  shape `pr-description` needs: it reads `git log`, `git diff dev...` and the
  commit message rather than a `pr.diff` file.

The source repository defaults to `~/workspace/bornnobody`; pass `--repo` to
build from another checkout. The extracted base tree is cached in
`/tmp/opencode/skill-evals/base`; `--clean` rebuilds it.

### Case files

`evals/cases/<skill>.json` holds the cases for one skill:

```json
{
  "skill": "guard-change-review",
  "cases": [
    {
      "name": "widens-allow-list-escalates",
      "mode": "review",
      "prompt": "Review this pull request.",
      "expected": "ESCALATE: adding a line to a shrink-only allow list is loosening.",
      "edits": [
        {
          "op": "insert_after",
          "path": "sim-scenario/src/test/resources/style/big-files.txt",
          "anchor": "Paths3.kt 751",
          "text": "DuelFigures.kt 900"
        }
      ],
      "graders": [
        { "text": "The verdict is ESCALATE", "kind": "regex", "value": "^VERDICT: ESCALATE\\b" },
        { "text": "The widened allow list is named", "kind": "contains_any", "value": ["big-files.txt", "DuelFigures.kt"] }
      ]
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `name` | Case ID; also the fixture directory name. |
| `mode` | `review` or `branch` (default `review`). |
| `prompt` | The task line prepended to the harness prompt. |
| `expected` | Human note: what should happen and why. Not graded. |
| `edits` | The change applied to the base tree. Each op must hit exactly one anchor. |
| `graders` | Deterministic checks on the model's output. |
| `coverage` | Optional literal `coverage.md` content. |
| `commit` | Commit subject for `branch` mode. |

Edit ops are `create`, `delete`, `replace`, `remove_line`, `insert_after` and
`append`. `replace`, `remove_line` and `insert_after` fail the build if their
anchor is ambiguous, so a case cannot silently edit the wrong line when the
upstream file changes.

Grader kinds:

| Kind | Passes when |
| --- | --- |
| `regex` | `re.search` finds the pattern (multiline). |
| `contains` | The text appears, case-insensitive. |
| `contains_any` | At least one listed text appears. |
| `not_contains` | The text does not appear. |
| `regex_not` | The pattern does not match. |

Verdict graders anchor at the start of a line (`^VERDICT: PASS\b`) so a model
that discusses both outcomes but concludes one is not marked on the wrong word.

## Running

```sh
python3 evals/build_fixtures.py --all
python3 evals/run_evals.py --all --configs with
python3 evals/run_evals.py guard-change-review --configs both
python3 evals/run_evals.py --all --only adds-guard-test-passes,disables-test-escalates
python3 evals/run_evals.py --all --model opencode-go/claude-haiku-5-5 --jobs 3
```

`--configs` accepts `with`, `with_skill`, `baseline`, `both`, or a comma-separated
list. `--jobs` controls how many headless sessions run at once; `--timeout` is
seconds per case. The process exits non-zero if any `with_skill` run fails a
grader, so it can gate a skill change.

The default model is `opencode-go/deepseek-v4.1-flash`; `--model` takes any
OpenCode model ID. The model is part of the experiment: changing it changes both
configurations, so compare runs only at the same model.

### Results

Progress prints one line per run:

```
PASS guard-change-review/widens-allow-list-escalates [baseline] 2/2 (exit 0)
FAIL test-review/behaviour-without-test-fails [with_skill] 1/2 (exit 0)
    missing: The uncovered file is named
```

The raw output of every run is kept in
`/tmp/opencode/skill-evals/results/<skill>/<case>/<config>.txt`, and each skill's
last run is summarised in `results.json` beside it. Read the raw output before
acting on a failure: the grader says a required fact is missing, not why the
model missed it.

## Current coverage

Results below are from `opencode-go/deepseek-v4.1-flash` on 10 November 2026.

| Skill | Cases | With skill | Baseline | What they cover |
| --- | ---: | ---: | ---: | --- |
| `guard-change-review` | 8 | 8/8 | 8/8 | Added guard test; `@Disabled`; allow-list shrink and widen; test rename; weakened assertion beside a new test; CI `continue-on-error`; edited `guarded-paths.txt` |
| `code-quality-review` | 4 | 4/4 | 4/4 | Clean extraction; new `@Suppress`; `TODO` without the wanted-rule; `Math` in sim code |
| `test-review` | 3 | 3/3 | 3/3 | Changed behaviour with a test; without a test and 0% coverage; `@Disabled` |
| `pr-description` | 3 | 3/3 | 2/3 | Body from a doc change; guarded config named; refuses to invent an S number |

Only `pr-description/writes-body-from-doc-change` currently discriminates: the
baseline misses the S-number title, the `Risks and rollout` section and the
marker (7/10), while the skill produces all three (10/10). Every other case
passes both ways, so they are regression tests, not evidence of lift.

That is the useful finding: the base model already knows the obvious rules
(`@Suppress`, `Math`, `@Disabled`, a widened allow list). A case only
discriminates when the rule is project-specific or the output format is exact.
Add such cases before claiming a skill improves verdicts; do not count a
both-ways pass as a win.

## Limits

- The graders check facts, not reasoning. A model can name the right file for
  the wrong reason and still pass.
- Each fixture is bornnobody `HEAD` plus one small edit. It cannot cover every
  rule in a skill, and upstream changes can invalidate a case; the build fails
  loudly on a moved anchor, which is the intended signal to update the case.
- `baseline` controls for the skill text, not for model quality. A weak model
  failing both ways says nothing about the skill.
- `coverage.md` in `test-review` cases is hand-written in the generated page's
  format; it is not a JaCoCo run.
- Branch mode uses a synthetic commit and a local `origin`; it does not exercise
  GitHub's PR body or review comments.
- The real gate reads the skill from `/tmp/review/skills/skills/<id>/SKILL.md`.
  The harness reads the same file from this checkout. The path differs; the
  content does not.
- Model output is not deterministic. A single pass on a marginal case is not
  proof; re-run it before drawing a conclusion.
