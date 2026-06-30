#!/usr/bin/env python3
"""
setup_hooks.py — Install git hooks for this repo.

Run once after a fresh clone:
    python scripts/setup_hooks.py

Installs:
  pre-commit — auto-distributes images from projects/process/ when staged
"""

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
HOOKS_SOURCE = REPO_ROOT / "scripts" / "hooks"
HOOKS_TARGET = REPO_ROOT / ".git" / "hooks"

HOOKS_SOURCE.mkdir(exist_ok=True)

PRE_COMMIT = """#!/bin/sh
# Auto-distribute images from projects/process/ before committing.
# Runs distribute_images.py if any files are staged under projects/process/.

REPO_ROOT="$(git rev-parse --show-toplevel)"

if git diff --cached --name-only | grep -q "^projects/process/"; then
    echo "[pre-commit] projects/process/ has staged files — running distribute_images.py..."
    python3 "$REPO_ROOT/scripts/distribute_images.py"
    if [ $? -ne 0 ]; then
        echo "[pre-commit] distribute_images.py failed — aborting commit"
        exit 1
    fi
    git add projects/images/ projects/process/ projects/art-generate.yaml projects/art-prompts.yaml
    echo "[pre-commit] Distribution done."
fi
"""

(HOOKS_SOURCE / "pre-commit").write_text(PRE_COMMIT)

for hook_file in HOOKS_SOURCE.iterdir():
    dest = HOOKS_TARGET / hook_file.name
    shutil.copy2(hook_file, dest)
    dest.chmod(0o755)
    print(f"  installed: .git/hooks/{hook_file.name}")

print("Done.")
