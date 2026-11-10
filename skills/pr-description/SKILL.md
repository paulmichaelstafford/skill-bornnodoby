---
name: pr-description
description: Build a pull request title and body for bornnobody from the branch diff — what changed, why, the required Realism line, and the verification actually run. Use when opening a PR to dev, or when asked to write or check a PR description.
---

# PR description

The description states facts from the branch. Never invent a test result, a
ruling, or a hash. If something was not run, say it was not run.

## 1. Read the change

```sh
git fetch origin
BASE=origin/dev          # or the base the caller names
git log --oneline "$BASE"..HEAD
git diff --stat "$BASE"...HEAD
git diff --name-only "$BASE"...HEAD
```

Title: `S<number>: <one sentence>` — the same shape as the commits, lowercase
after the colon, no full stop. If the commits disagree on the number, stop and
ask; do not invent one.

## 2. Checks before writing a word

Run these against the changed file list. Any "yes" changes the body; it is not
a reason to stop unless marked.

**Scope**
- One concern? Name any unrelated hunk as a separate finding.
- Which modules changed, and what kind is each touched file?
  `docs/architecture.generated.md` has the answer.

**Guarded and rule files** — a "yes" here is a `Guarded` line in the body.
- A path matching `docs/guarded-paths.txt` (the authority; globs match across
  folders). Includes the guard tests, `style/*` lists, build files,
  `CLAUDE.md`, `config/*`, `.github/*`.
- A `*Guard*.kt`, `StyleGuards.kt`, `CodeStyleSources.kt` or `LabAllow.kt`.
- A burn-down list in `sim-scenario/src/test/resources/style/arch-*.txt`
  (these may only shrink).
- A new `@Suppress`, a detekt baseline, or a disabled test.
- A new entry in `docs/exceptions.md`.

**Records**
- Does the change cite its ruling or plan (`docs/superpowers/plans/...`) or a
  record entry? A new decision belongs in the record, never invented in the PR.
- `docs/code-map.md` is current if a feature, owner or event changed:
  `python3 docs/tools/code-map.py && git diff --exit-code docs/code-map.md`
- `docs/architecture.generated.md` is current if imports, features, module
  dependencies or guard tests changed: run `docs/tools/architecture-report.sh`
  (it runs the guards first) and check the page is in the commit.
- `docs/coverage.generated.md` must be regenerated and committed for **every**
  PR: run `docs/tools/coverage-report.sh --base origin/dev`. `cert/tests` fails
  when the committed page differs from the one the run produces.
- A design change is a new design-plan version plus a changelog note; never an
  edit to an old version.

**Behaviour**
- Snapshot shape changed? `FORMAT_VERSION` in
  `sim-core/src/main/kotlin/bornnobody/core/Snapshots.kt` must be bumped.
- A sim change needs history-to-far scenes for its area, and the golden and
  headless hashes checked. Note the hashes or say they were not run.
- The client or a per-frame path changed? State the 60 fps evidence.
- A new listener, sink or step-phase change? It names its phase
  (`docs/step-order.md`).

**Verification actually run** — record the exact commands and results.
Do not list a command that did not run.

- `./gradlew test` (every module)
- `./gradlew worldTests` (before-play scenes)
- `./gradlew nightly` (tagged nightly)
- `./gradlew phase0Gate` (determinism, two JVMs)
- a headless run, or the golden check, when the sim changed

## 3. Body template

```markdown
## What changed

One paragraph. The behaviour or structure, not a file list.

## Why

The ruling, plan section or record entry. One or two sentences.
If there is no ruling and the four golden rules decide it, say which rule.

## How

The modules and kinds touched; the one mechanism that carries the change.
Call out a moved boundary, a new event, or a new owner.

## Realism

Required. The sources used, the targets in `docs/realism-targets.md` that moved,
and the `DEPARTURE-n` ids relied on. "None" is a valid answer only when the
change does not touch the world; say why.

## Verification

- `./gradlew test` — pass, <count> tests, <n> skipped
- `./gradlew worldTests` — pass / not run
- golden: <hash> / unchanged / not run
- headless: <hashes> / not run
- `docs/tools/architecture-report.sh` — page current
- `docs/tools/coverage-report.sh --base origin/dev` — coverage page committed

## Guarded

List every guarded or rule file touched, and why. If none, say "none".
This is where the signature requirement is visible.

## Risks and rollout

Snapshot version, performance, a behaviour that changes under an existing
seed, or "none".

## Not done

What was deferred, with the record or "wanted, not built" pointer. Omit the
section when empty.

<!-- pr-description: v1 -->
```

The final line is the marker the description check looks for. Keep it.

## 4. Create the PR

```sh
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_personal" git push -u origin HEAD
gh pr create --base dev --title "S<N>: <sentence>" --body-file <file>
```

This skill is the only supported way to open a pull request. The body must
carry the `pr-description` marker; without it, `cert/description` fails and the
PR cannot merge.

`gh` may not be installed; if it is not, write the title and body to a file and
report the path instead of inventing another route. Do not create the PR when
a check in section 2 is unresolved — report the finding first.

## What this skill does not do

- It does not judge architecture, quality or coverage; the review skills do.
- It does not approve, sign or merge anything.
- It does not run the full test suite unless the caller asks; it reports what
  was run.
