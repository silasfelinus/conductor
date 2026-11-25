#!/usr/bin/env python3
"""check_workflow_yaml.py -- fail when any .github/workflows/*.yml stops parsing.

WHY (memory-dungeon/t-071, kaizen from the t-070 review, conductor#7326).
Head 0bff092 left .github/workflows/ci.yml unparseable. GitHub does not report
a broken workflow file as a failed check: it just runs none of that file's
jobs. The PR showed 16 green checks instead of 26 and nothing was red, so the
break could have merged on a "green" PR.

The guard therefore runs from a workflow other than ci.yml (the Static checks
job in security-audit.yml). It yaml.safe_loads every workflow file and fails
on the first one that does not parse or is not a mapping with `jobs`. If the
file it runs from is itself broken, every other workflow still reports it.

Usage: python scripts/check_workflow_yaml.py [--dir .github/workflows]
Exit 0 when every file parses, 1 when any does not.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def workflow_problems(directory: Path) -> list[str]:
    """Return one line per workflow file that does not load as a workflow."""
    problems: list[str] = []
    files = sorted([*directory.glob("*.yml"), *directory.glob("*.yaml")])
    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            problems.append(f"{path}: does not parse: {exc}")
            continue
        if not isinstance(data, dict):
            problems.append(f"{path}: root is not a mapping")
        elif not isinstance(data.get("jobs"), dict) or not data["jobs"]:
            problems.append(f"{path}: has no `jobs` mapping")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dir", type=Path, default=ROOT / ".github" / "workflows")
    args = parser.parse_args(argv)
    files = [*args.dir.glob("*.yml"), *args.dir.glob("*.yaml")]
    if not files:
        print(f"no workflow files under {args.dir}", file=sys.stderr)
        return 1
    problems = workflow_problems(args.dir)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(
            f"{len(problems)} of {len(files)} workflow file(s) are broken; "
            "GitHub silently skips their jobs instead of failing a check.",
            file=sys.stderr,
        )
        return 1
    print(f"All {len(files)} workflow files parse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
