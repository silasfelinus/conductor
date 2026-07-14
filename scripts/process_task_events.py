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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_text_patch import apply_task_field_ops  # noqa: E402

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


def compute_transition_ops(
    task: dict[str, Any], event: dict[str, Any], operation: str
) -> list[tuple[str, str, Any]]:
    """Decide which fields change for this event, without mutating `task` or
    touching any file. Returns a list of ("set"|"unset", field, value) ops in
    application order; an empty list means the event is a true no-op (e.g. a
    repeat claim by the same owner)."""
    current = task.get("status")
    force = bool(event.get("force", False))
    ops: list[tuple[str, str, Any]] = []

    if operation == "claim":
        if current == "claimed" and task.get("owner") == event.get("owner", "worker"):
            return []
        if current != "ready" and not force:
            raise ValueError(f"claim requires status ready, found {current!r}")
        ops.append(("set", "status", "claimed"))
        ops.append(("set", "owner", event.get("owner", "worker")))
    elif operation == "rearm":
        if not task.get("recurring") and not force:
            raise ValueError("rearm requires recurring: true")
        ops.append(("set", "status", "ready"))
        ops.append(("unset", "owner", None))
    else:
        target = operation
        if not (operation in CLOSED_OPERATIONS and current == target):
            ops.append(("set", "status", target))
        if target not in {"claimed", "review"}:
            ops.append(("unset", "owner", None))

    if operation == "needs-human":
        ops.append(("set", "soft_gate", "true" if event.get("soft_gate") else "false"))
    elif operation in {"ready", "claim", "done", "blocked", "rearm"}:
        ops.append(("unset", "soft_gate", None))

    timestamp = event.get("updated")
    if timestamp is None:
        timestamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    ops.append(("set", "updated", timestamp))

    note = event.get("note")
    if note is not None:
        if not isinstance(note, str) or not note.strip():
            raise ValueError("note must be a non-empty string when supplied")
        existing = task.get("note")
        new_note = f"{existing}\n\n{note.strip()}" if existing else note.strip()
        ops.append(("set", "note", new_note))

    return ops


def prepare_learning(
    event: dict[str, Any], project: str, task_id: str, operation: str
) -> dict[str, Any] | None:
    """Validate the event's optional `learning` payload and return the record to
    append, or None if there's nothing to append (absent, or already recorded).

    Pure/read-only: raises on invalid payloads but never writes, so callers can
    validate learning data BEFORE mutating the roadmap -- a bad learning payload
    must not leave an already-applied, now-unrepeatable transition stuck with its
    event file undeleted (see process()'s ordering)."""
    learning = event.get("learning")
    if learning is None:
        return None
    if operation not in CLOSED_OPERATIONS:
        raise ValueError("learning may only accompany done or blocked events")
    if not isinstance(learning, dict):
        raise ValueError("learning must be a mapping")

    required = {"kind", "stakes", "lesson"}
    missing = sorted(required - learning.keys())
    if missing:
        raise ValueError(f"learning is missing required fields: {', '.join(missing)}")

    path = ROOT / "LEARNING.yaml"
    ledger = load_yaml(path) if path.is_file() else {"records": []}
    records = ledger.get("records") or []
    if not isinstance(records, list):
        raise ValueError("LEARNING.yaml records must be a list")
    if any(
        isinstance(record, dict)
        and record.get("project") == project
        and record.get("task") == task_id
        and record.get("outcome") == operation
        for record in records
    ):
        return None

    return {
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


def write_learning_record(record: dict[str, Any]) -> None:
    """Append one record to LEARNING.yaml as new trailing text -- never touches
    the bytes of any existing record, so prior entries keep whatever quoting/
    escaping style they were originally written with."""
    path = ROOT / "LEARNING.yaml"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        ledger = yaml.safe_load(text) or {}
    else:
        text = "records: []\n"
        ledger = {"records": []}

    fragment = yaml.safe_dump(
        [record], sort_keys=False, default_flow_style=False, width=100, allow_unicode=True
    )

    if ledger.get("records"):
        if not text.endswith("\n"):
            text += "\n"
        path.write_text(text + fragment, encoding="utf-8")
    else:
        path.write_text("records:\n" + fragment, encoding="utf-8")


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

    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    roadmap = yaml.safe_load(roadmap_text)
    if not isinstance(roadmap, dict):
        raise ValueError(f"{roadmap_path}: expected a YAML mapping")
    task = find_task(roadmap, task_id)

    # Compute everything (transition + learning validation) before writing anything,
    # so an invalid learning payload can't leave a half-applied, now-unrepeatable
    # transition behind with its event file stranded (atomicity requirement).
    ops = compute_transition_ops(task, event, operation)
    learning_record = prepare_learning(event, project, task_id, operation)

    if not dry_run:
        if ops:
            new_text = apply_task_field_ops(roadmap_text, task_id, ops)
            yaml.safe_load(new_text)  # re-parse to confirm the edit produced valid YAML
            if new_text != roadmap_text:
                roadmap_path.write_text(new_text, encoding="utf-8")
        if learning_record is not None:
            write_learning_record(learning_record)
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
