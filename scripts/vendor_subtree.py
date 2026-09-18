#!/usr/bin/env python3
"""Vendor forked marketplace repositories as git subtrees.

Reads ./submodules.json and, for each listed repository:

  - First run:  git subtree add    --prefix=<path> --squash <remote> <branch>
  - Later runs: git subtree pull   --prefix=<path> --squash <remote> <branch>

Uses --squash so the fork's history collapses into a single commit per sync,
keeping this repo's history clean. Updates merge upstream changes into any
local modifications.

Usage: python scripts/vendor_subtree.py
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "submodules.json"


def run_git(args, check=True):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True
    )
    if check and result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        sys.exit(result.returncode)
    return result


def load_config():
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: {CONFIG}: invalid JSON ({e})")
        sys.exit(1)
    repos = data.get("repositories", [])
    if not repos:
        print(f"ERROR: no repositories listed in {CONFIG}")
        sys.exit(1)
    return repos


def main():
    repos = load_config()

    for repo in repos:
        name = repo["name"]
        remote = repo["remote"]
        branch = repo.get("branch", "main")
        path = repo["path"]

        print(f"=== {name} ===")
        print(f"  remote: {remote} (branch: {branch})")
        print(f"  path:   {path}")

        if (ROOT / path).exists():
            action = "pull"
            print("  local path exists -> updating with git subtree pull")
        else:
            action = "add"
            print("  local path missing -> adding with git subtree add")

        cmd = ["subtree", action, "--prefix", path, "--squash", remote, branch]
        result = run_git(cmd)
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
        print(f"  {name}: done\n")


if __name__ == "__main__":
    main()