#!/usr/bin/env python3
"""Build the fixture bundles the review skills are evaluated against.

Each skill is reviewed by the bornnobody gate from a bundle, not a live
checkout: `pr.diff`, `tree/` (the pull request checkout), `guarded-paths.txt`
and, when present, `coverage.md`. This script reproduces that bundle from the
bornnobody repository at HEAD plus a small, named edit per case.

    python3 evals/build_fixtures.py guard-change-review
    python3 evals/build_fixtures.py --all

Cases live in `evals/cases/<skill>.json`. A case is one of:

  review  - the tree keeps the edit uncommitted; `pr.diff` is `git diff`
  branch  - the edit is a commit on `feature`; `dev` is the base branch

The output is `/tmp/opencode/skill-evals/<skill>/<case>/`.
"""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases"
WORK = Path("/tmp/opencode/skill-evals")
BASE = WORK / "base"
DEFAULT_REPO = Path.home() / "workspace" / "bornnobody"


def run(args, cwd=None, check=True, capture=False):
    result = subprocess.run(
        args, cwd=cwd, text=True, capture_output=capture, check=False
    )
    if check and result.returncode != 0:
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(map(str, args))}\n"
            f"{result.stderr or ''}"
        )
    return result


def extract_base(repo):
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    result = subprocess.run(
        f"git -C '{repo}' archive HEAD | tar -x -C '{BASE}'",
        shell=True,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"could not extract {repo}: {result.stderr}")


def safe_write(path, text):
    tmp = path.with_name(path.name + ".eval-tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def git(tree, *args):
    return run(
        ["git", "-c", "user.name=Eval", "-c", "user.email=eval@example.invalid", *args],
        cwd=tree,
        capture=True,
    ).stdout


def apply_edit(tree, edit):
    path = tree / edit["path"]
    op = edit["op"]

    if op == "create":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(edit["text"])
        return

    if op == "delete":
        path.unlink()
        return

    text = path.read_text()

    if op == "replace":
        old, new = edit["old"], edit["new"]
        count = text.count(old)
        if count != 1:
            raise SystemExit(
                f"{edit['path']}: replace anchor occurs {count} times, want 1"
            )
        safe_write(path, text.replace(old, new))
        return

    lines = text.splitlines(keepends=True)

    if op == "remove_line":
        wanted = edit["line"]
        indexes = [i for i, line in enumerate(lines) if line.rstrip("\n") == wanted]
        if len(indexes) != 1:
            raise SystemExit(
                f"{edit['path']}: line {wanted!r} occurs {len(indexes)} times, want 1"
            )
        del lines[indexes[0]]
        safe_write(path, "".join(lines))
        return

    if op == "insert_after":
        anchor = edit["anchor"]
        indexes = [i for i, line in enumerate(lines) if line.rstrip("\n") == anchor]
        if len(indexes) != 1:
            raise SystemExit(
                f"{edit['path']}: anchor {anchor!r} occurs {len(indexes)} times, want 1"
            )
        lines[indexes[0] + 1 : indexes[0] + 1] = [edit["text"] + "\n"]
        safe_write(path, "".join(lines))
        return

    if op == "append":
        safe_write(path, text + edit["text"])
        return

    raise SystemExit(f"unknown edit op: {op}")


def new_tree(dest):
    tree = dest / "tree"
    run(["cp", "-al", str(BASE), str(tree)])
    git(tree, "init", "-q", "-b", "dev")
    git(tree, "add", "-A")
    git(tree, "commit", "-qm", "base")
    return tree


def build_review(case, dest):
    tree = new_tree(dest)
    for edit in case.get("edits", []):
        apply_edit(tree, edit)
    git(tree, "add", "-N", ".")
    diff = git(tree, "diff", "--no-color")
    (dest / "pr.diff").write_text(diff)
    shutil.copy(BASE / "docs/guarded-paths.txt", dest / "guarded-paths.txt")
    if case.get("coverage") is not None:
        (dest / "coverage.md").write_text(case["coverage"])
    elif (tree / "docs/coverage.generated.md").exists():
        shutil.copy(tree / "docs/coverage.generated.md", dest / "coverage.md")


def build_branch(case, dest):
    tree = new_tree(dest)
    git(tree, "checkout", "-q", "-b", "feature")
    for edit in case.get("edits", []):
        apply_edit(tree, edit)
    git(tree, "add", "-A")
    git(tree, "commit", "-qm", case["commit"])
    git(tree, "remote", "add", "origin", str(tree))
    git(tree, "fetch", "-q", "origin")
    if case.get("coverage") is not None:
        (dest / "coverage.md").write_text(case["coverage"])
    elif (tree / "docs/coverage.generated.md").exists():
        shutil.copy(tree / "docs/coverage.generated.md", dest / "coverage.md")


def build(skill, case, repo):
    dest = WORK / skill / case["name"]
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    mode = case.get("mode", "review")
    if mode == "review":
        build_review(case, dest)
    elif mode == "branch":
        build_branch(case, dest)
    else:
        raise SystemExit(f"unknown mode: {mode}")
    return dest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", nargs="?")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--clean", action="store_true", help="rebuild the base tree")
    args = parser.parse_args()

    if not args.all and not args.skill:
        parser.error("name a skill or pass --all")
    if not (args.repo / ".git").exists():
        raise SystemExit(f"not a git repository: {args.repo}")

    if args.clean or not BASE.exists():
        extract_base(args.repo)
        print(f"base tree: {BASE}")

    skills = (
        sorted(path.stem for path in CASES.glob("*.json"))
        if args.all
        else [args.skill]
    )
    for skill in skills:
        manifest = CASES / f"{skill}.json"
        if not manifest.exists():
            raise SystemExit(f"no case file: {manifest}")
        data = json.loads(manifest.read_text())
        for case in data["cases"]:
            dest = build(skill, case, args.repo)
            print(f"{skill}/{case['name']}: {dest}")


if __name__ == "__main__":
    main()
