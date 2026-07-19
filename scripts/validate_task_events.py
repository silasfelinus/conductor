#!/usr/bin/env python3
"""Validate task-events/*.yaml files without applying them.

Catches malformed event files (YAML syntax errors, missing/invalid required
fields) at PR time, before they can land on main and break the shared
`process-task-events` CI job for every unrelated PR (conductor/t-067 found
the incident, conductor/t-068 closes the gap: that job already survives a
malformed file per-run, but a broken file left on main keeps failing it for
every PR until someone happens to notice and fix it).

Usage: python scripts/validate_task_events.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_task_events import (  # noqa: E402
    ALLOWED_OPERATIONS,
    CLOSED_OPERATIONS,
    PROJECT_RE,
    TASK_RE,
    require_string,
)

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "task-events"


def event_files() -> list[Path]:
    # Deliberately not imported from process_task_events: that module's
    # event_files() closes over *its own* module-global EVENT_DIR, which a
    # test patching this module's EVENT_DIR would never see.
    if not EVENT_DIR.exists():
        return []
    return sorted(
        path for path in EVENT_DIR.glob("*.yaml") if path.name not in {"example.yaml"}
    )


def validate(path: Path) -> str | None:
    """Return an error string, or None if `path` is a well-formed event.

    Deliberately lighter than process_task_events.process(): it checks shape
    (parses, required fields, known operation, target roadmap exists) but not
    live transition legality (e.g. "claim requires status ready"), since that
    can legitimately go stale between a PR opening and the event actually
    running -- this check exists to catch syntax/shape errors, not races.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return f"cannot read file: {error}"

    try:
        event = yaml.safe_load(text)
    except yaml.YAMLError as error:
        return f"invalid YAML syntax: {error}"

    if not isinstance(event, dict):
        return "expected a YAML mapping"

    version = event.get("version", 1)
    if version != 1:
        return f"unsupported event version {version!r}"

    try:
        project = require_string(event, "project", PROJECT_RE)
        require_string(event, "task", TASK_RE)
        operation = require_string(event, "operation")
    except ValueError as error:
        return str(error)

    if operation not in ALLOWED_OPERATIONS:
        return f"unsupported operation {operation!r}"

    roadmap_path = ROOT / "projects" / project / "roadmap.yaml"
    if not roadmap_path.is_file():
        return f"unknown project roadmap: projects/{project}/roadmap.yaml"

    note = event.get("note")
    if note is not None and (not isinstance(note, str) or not note.strip()):
        return "note must be a non-empty string when supplied"

    learning = event.get("learning")
    if learning is not None:
        if operation not in CLOSED_OPERATIONS:
            return "learning may only accompany done or blocked events"
        if not isinstance(learning, dict):
            return "learning must be a mapping"
        required = {"kind", "stakes", "lesson"}
        missing = sorted(required - learning.keys())
        if missing:
            return f"learning is missing required fields: {', '.join(missing)}"

    return None


def main() -> int:
    files = event_files()
    if not files:
        print("No task events to validate.")
        return 0

    errors = []
    for path in files:
        error = validate(path)
        if error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(files)} task-events file(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
