---
name: Code Quality Review
description: Review a pull request's diff for bornnobody's code quality — detekt and ktlint, the style guards, suppressions, dead code, naming, and the comment rules. Use when a PR is opened, or when asked to review code quality.
---

# Code quality review

Read-only. Report findings; never fix, suppress or approve.

## Inputs

- The diff: `git diff <base>...HEAD`.
- `config/detekt.yml`, `.editorconfig`.
- `docs/exceptions.md` and `sim-scenario/src/test/resources/style/*`.
- The rule text in `CLAUDE.md` (the non-negotiables).

## Run

If the environment gives you a shell:

```sh
./gradlew detekt ktlint
./gradlew :sim-scenario:test \
  --tests '*CodeStyleGuardTest' \
  --tests '*ExceptionsGuardTest'
```

If it does not, say the commands were not run and judge from the diff and the
test results the PR provides. Never claim a command ran when it did not.

A failure is at least **Important**. Quote the rule and the file.

## Check the diff

- `@Suppress` — banned. A detekt baseline — banned. A disabled test — a finding.
- A `TODO` with no "wanted, not built" line.
- A comment naming a round, a fix, or a commit hash.
- A line or file over the limit beyond a named exception.
- `Math` or a wall clock outside the named places; iteration over a `HashMap`
  or `HashSet` in sim code; an inline qualified name beyond the named places.
- Naming, duplication, dead code, a public action or owner that no test calls.
- A new `docs/exceptions.md` entry: report it, never grant it; it is Paul's.

## Verdict

```markdown
VERDICT: PASS | FAIL
- [Critical|Important|Minor] file:line — finding — evidence
```

Do not report architecture boundaries (the architecture review owns them) or
missing tests (the test review owns them).
