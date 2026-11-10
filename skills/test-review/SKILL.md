---
name: test-review
description: Review whether a pull request tests what it changed — coverage of the changed lines, the BDD scene conventions, history-to-far scenes for a sim change, the golden and headless checks, and any test removed or skipped. Use when a PR is opened, or when asked to review tests.
---

# Test review

Read-only. It judges whether the change is tested, not whether the code is good.

## Inputs

- The diff: `git diff <base>...HEAD`.
- `docs/coverage.generated.md` for the branch, especially
  `## Changed files against <base>`.
- `sim-scenario/build/test-results/test/TEST-*.xml` from the run.
- `docs/build-and-test.md` and the test rules in `CLAUDE.md`.

## Check

**Each changed behaviour has a test that would fail before the change.** Name
the test, or record the absence. A test that only exercises the line without
asserting the behaviour does not count.

**Coverage of the changed lines.**
- A changed main file with 0 covered lines is a finding unless the PR explains
  why (a constant table, generated code, a pure shape).
- New behaviour with no new test is a finding even when coverage rises.

**A sim change** needs:
- history-to-far scenes for its area (`*BddTest`, `Lab*`);
- the golden and headless hashes, or an explicit statement that they were not
  run;
- a `FORMAT_VERSION` bump if the snapshot shape changed.

**Nothing weakened.** No `@Test` deleted or renamed, no `@Disabled`/`@Ignore`,
no `assumeTrue`, no assertion removed or loosened. Report it even when the
guard-change review also will.

**Scene conventions** (`CLAUDE.md`, "How we test"): one behaviour, a plain name,
about ten lines, no setup code in the test file, under a second a seed,
`about`/`in most seeds` rather than an exact number, several seeds.

**The run:** every test passed, and no skip without a reason and a date.

## Verdict

```markdown
VERDICT: PASS | FAIL
- [Critical|Important|Minor] file:line — finding — evidence (test name, coverage line, or rule)
  Fix: the test or scene that would close it (advice, never an edit)
```

**Critical and Important block.** A Minor finding is advice: list it, but it
does not fail the verdict. PASS requires no Critical and no Important finding.

Do not report style or architecture; the other reviews own those.
