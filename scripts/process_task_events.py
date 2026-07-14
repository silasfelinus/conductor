#!/usr/bin/env python3
"""Apply small task-event files to authoritative conductor roadmaps.

The GitHub connector can reliably create tiny files but may truncate large roadmap
reads. This processor runs inside the repository checkout, applies task mutations
against the complete YAML file, validates the result, resolves dependencies, and
removes successfully consumed events.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "task-events"
PROJECT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TASK_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ALLOWED_OPERATIONS = {
    "claim",
    "done",
    "ready",
    "review",
    "needs-human",
    "blocked",
    "rearm",
}
CLOSED_OPERATIONS = {"done", "blocked"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, default_flow_style=False, width=100),
        encoding="utf-8",
    )


def event_files() -> list[Path]:
    if not EVENT_DIR.exists():
        return []
    return sorted(
        path
        for path in EVENT_DIR.glob("*.yaml")
        if path.name not in {"example.yaml"}
    )


def require_string(event: dict[str, Any], key: str, pattern: re.Pattern[str] | None = None) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"event field {key!r} must be a non-empty string")
    value = value.strip()
    if pattern and not pattern.fullmatch(value):
        raise ValueError(f"event field {key!r} contains unsupported characters")
    return value


def find_task(roadmap: dict[str, Any], task_id: str) -> dict[str, Any]:
    tasks = roadmap.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("roadmap tasks must be a list")
    matches = [task for task in tasks if isinstance(task, dict) and task.get("id") == task_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one task {task_id!r}; found {len(matches)}")
    return matches[0]


def append_note(task: dict[str, Any], note: str) -> None:
    existing = task.get("note")
    if existing:
        task["note"] = f"{existing}\n\n{note}"
    else:
        task["note"] = note


def apply_transition(task: dict[str, Any], event: dict[str, Any], operation: str) -> None:
    current = task.get("status")
    force = bool(event.get("force", False))

    if operation == "claim":
        if current == "claimed" and task.get("owner") == event.get("owner", "worker"):
            return
        if current != "ready" and not force:
            raise ValueError(f"claim requires status ready, found {current!r}")
        task["status"] = "claimed"
        task["owner"] = event.get("owner", "worker")
    elif operation == "rearm":
        if not task.get("recurring") and not force:
            raise ValueError("rearm requires recurring: true")
        task["status"] = "ready"
        task.pop("owner", None)
    else:
        target = operation
        if operation in CLOSED_OPERATIONS and current == target:
            pass
        else:
            task["status"] = target
        if target not in {"claimed", "review"}:
            task.pop("owner", None)

    if operation == "needs-human":
        task["soft_gate"] = bool(event.get("soft_gate", False))
    elif operation in {"ready", "claim", "done", "blocked", "rearm"}:
        task.pop("soft_gate", None)

    timestamp = event.get("updated")
    if timestamp is None:
        timestamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    task["updated"] = timestamp

    note = event.get("note")
    if note is not None:
        if not isinstance(note, str) or not note.strip():
            raise ValueError("note must be a non-empty string when supplied")
        append_note(task, note.strip())


def append_learning(event: dict[str, Any], project: str, task_id: str, operation: str) -> None:
    learning = event.get("learning")
    if learning is None:
        return
    if operation not in CLOSED_OPERATIONS:
        raise ValueError("learning may only accompany done or blocked events")
    if not isinstance(learning, dict):
        raise ValueError("learning must be a mapping")

    path = ROOT / "LEARNING.yaml"
    ledger = load_yaml(path)
    records = ledger.setdefault("records", [])
    if not isinstance(records, list):
        raise ValueError("LEARNING.yaml records must be a list")
    if any(
        isinstance(record, dict)
        and record.get("project") == project
        and record.get("task") == task_id
        and record.get("outcome") == operation
        for record in records
    ):
        return

    required = {"kind", "stakes", "lesson"}
    missing = sorted(required - learning.keys())
    if missing:
        raise ValueError(f"learning is missing required fields: {', '.join(missing)}")

    records.append(
        {
            "date": learning.get("date", dt.date.today().isoformat()),
            "project": project,
            "task": task_id,
            "kind": learning["kind"],
            "stakes": learning["stakes"],
            "passes": int(learning.get("passes", 0)),
            "outcome": operation,
            "failure_category": learning.get("failure_category"),
            "lesson": learning["lesson"],
        }
    )
    dump_yaml(path, ledger)


def process(path: Path, dry_run: bool) -> str:
    event = load_yaml(path)
    version = event.get("version", 1)
    if version != 1:
        raise ValueError(f"unsupported event version {version!r}")

    project = require_string(event, "project", PROJECT_RE)
    task_id = require_string(event, "task", TASK_RE)
    operation = require_string(event, "operation")
    if operation not in ALLOWED_OPERATIONS:
        raise ValueError(f"unsupported operation {operation!r}")

    roadmap_path = ROOT / "projects" / project / "roadmap.yaml"
    if not roadmap_path.is_file():
        raise ValueError(f"unknown project roadmap: {roadmap_path.relative_to(ROOT)}")

    roadmap = load_yaml(roadmap_path)
    task = find_task(roadmap, task_id)
    apply_transition(task, event, operation)

    if not dry_run:
        dump_yaml(roadmap_path, roadmap)
        load_yaml(roadmap_path)
        append_learning(event, project, task_id, operation)
        path.unlink()

    return f"{project}/{task_id}: {operation}"


def run_resolver(dry_run: bool) -> None:
    command = [sys.executable, str(ROOT / "scripts" / "resolve_deps.py")]
    if dry_run:
        command.append("--dry-run")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files = event_files()
    if not files:
        print("No task events to process.")
        return 0

    had_error = False
    for path in files:
        try:
            print(process(path, args.dry_run))
        except Exception as error:
            had_error = True
            print(f"ERROR {path.relative_to(ROOT)}: {error}", file=sys.stderr)

    run_resolver(args.dry_run)
    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
