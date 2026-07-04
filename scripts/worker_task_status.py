#!/usr/bin/env python3
"""Worker-cycle helper for safe roadmap task field updates."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SET_TASK_FIELD = ROOT / "scripts" / "set_task_field.py"


class WorkerTaskStatusError(Exception):
    pass


def run_set_task_field(
    project: str,
    task_id: str,
    field: str,
    value: str,
    *,
    dry_run: bool = False,
) -> None:
    if dry_run:
        print(f"would set {project}/{task_id} {field}={value!r}")
        return

    command = [sys.executable, str(SET_TASK_FIELD), project, task_id, field, value]
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode != 0:
        raise WorkerTaskStatusError(
            f"set_task_field.py failed for {project}/{task_id} {field}={value!r}"
        )


def set_many(
    project: str,
    task_id: str,
    updates: list[tuple[str, str]],
    *,
    dry_run: bool = False,
) -> None:
    for field, value in updates:
        run_set_task_field(project, task_id, field, value, dry_run=dry_run)


def handle_claim(project: str, task_id: str, *, dry_run: bool = False) -> None:
    set_many(
        project,
        task_id,
        [
            ("status", "claimed"),
            ("owner", "worker"),
            ("updated", "now"),
        ],
        dry_run=dry_run,
    )


def handle_status(
    project: str,
    task_id: str,
    status: str,
    note: str | None,
    *,
    dry_run: bool = False,
) -> None:
    updates = [("status", status), ("updated", "now")]
    if note is not None:
        updates.append(("note", note))
    set_many(project, task_id, updates, dry_run=dry_run)


def handle_passes(project: str, task_id: str, passes: str, *, dry_run: bool = False) -> None:
    set_many(project, task_id, [("passes", passes), ("updated", "now")], dry_run=dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply Worker lifecycle roadmap updates via scripts/set_task_field.py."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the field updates that would be applied without editing roadmap.yaml.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    claim = subparsers.add_parser("claim", help="Set status=claimed, owner=worker, updated=now")
    claim.add_argument("project")
    claim.add_argument("task_id")

    for name, help_text in {
        "review": "Set status=review and updated=now",
        "done": "Set status=done and updated=now",
        "ready": "Set status=ready and updated=now",
        "needs-human": "Set status=needs-human and updated=now",
        "blocked": "Set status=blocked and updated=now",
        "challenged": "Set status=challenged and updated=now",
    }.items():
        status_parser = subparsers.add_parser(name, help=help_text)
        status_parser.add_argument("project")
        status_parser.add_argument("task_id")
        status_parser.add_argument("--note", help="Optional replacement note text")

    passes = subparsers.add_parser("passes", help="Set passes=<count> and updated=now")
    passes.add_argument("project")
    passes.add_argument("task_id")
    passes.add_argument("count")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "claim":
            handle_claim(args.project, args.task_id, dry_run=args.dry_run)
        elif args.command == "passes":
            handle_passes(args.project, args.task_id, args.count, dry_run=args.dry_run)
        else:
            handle_status(args.project, args.task_id, args.command, args.note, dry_run=args.dry_run)
    except WorkerTaskStatusError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
