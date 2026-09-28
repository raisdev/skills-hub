#!/usr/bin/env python3
"""Vendor the four document-processing skills from the anthropics-skills
submodule into this plugin's dist/ tree.

The plugin root is plugins/document-skills/dist/. Claude Code scans that
root's skills/ directory for exactly the skills listed here, so nothing else
from the submodule leaks into the install. This script is only a sync tool
-- it never ships with the plugin.

Usage: python3 plugins/document-skills/sync.py
"""
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILLS = ("xlsx", "docx", "pptx", "pdf")
SRC_ROOT = ROOT / "submodules" / "anthropics-skills" / "skills"
DEST_ROOT = pathlib.Path(__file__).resolve().parent / "dist" / "skills"


def main():
    if not SRC_ROOT.is_dir():
        print(f"ERROR: submodule not present at {SRC_ROOT}; run scripts/vendor_subtree.py first")
        sys.exit(1)

    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    for skill in SKILLS:
        src = SRC_ROOT / skill
        dest = DEST_ROOT / skill
        if not src.is_dir():
            print(f"ERROR: missing skill directory {src}")
            sys.exit(1)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        print(f"synced {skill}")

    print(f"done: {len(SKILLS)} skills -> {DEST_ROOT}")


if __name__ == "__main__":
    main()