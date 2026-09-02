#!/usr/bin/env python3
"""Warn when a PR appears to reuse an existing roadmap task id for different work."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


def load_roadmap(ref: str, path: str) -> dict | None:
    proc = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    data = yaml.safe_load(proc.stdout)
    return data if isinstance(data, dict) else None


def task_map(data: dict | None) -> dict[str, dict]:
    if not data:
        return {}
    return {
        str(task["id"]): task
        for task in data.get("tasks", [])
        if isinstance(task, dict) and task.get("id")
    }


def suspicious_reuse(base: dict | None, head: dict | None) -> list[tuple[str, str, str, str, str]]:
    before, after = task_map(base), task_map(head)
    findings = []
    for task_id in sorted(before.keys() & after.keys()):
        old, new = before[task_id], after[task_id]
        old_title, new_title = str(old.get("title", "")), str(new.get("title", ""))
        old_milestone, new_milestone = str(old.get("milestone", "")), str(new.get("milestone", ""))
        if old_title != new_title and old_milestone != new_milestone:
            findings.append((task_id, old_milestone, new_milestone, old_title, new_title))
    return findings


def changed_roadmaps(base: str, head: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", base, head, "--", "projects/*/roadmap.yaml"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in proc.stdout.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--github-annotations", action="store_true")
    args = parser.parse_args()

    found = False
    for path in changed_roadmaps(args.base, args.head):
        for task_id, old_m, new_m, old_title, new_title in suspicious_reuse(
            load_roadmap(args.base, path), load_roadmap(args.head, path)
        ):
            found = True
            message = (
                f"possible roadmap task id reuse in {path}: {task_id} changed milestone "
                f"{old_m!r} -> {new_m!r} and title {old_title!r} -> {new_title!r}"
            )
            if args.github_annotations:
                print(f"::warning file={path}::{message}")
            else:
                print(f"WARNING: {message}", file=sys.stderr)

    if found:
        return 1
    print("No suspicious roadmap task id reuse detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
