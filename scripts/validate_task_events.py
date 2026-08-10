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
    continuous_improvement_fields,
    extract_pr_references,
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

    # A claim event MUST name its session so the processor can tell two concurrent
    # Worker claims apart (owner alone collapses them). Any other event may carry a
    # session (used for the later ownership check) but must not carry an empty one.
    session = event.get("session")
    if operation == "claim":
        if not isinstance(session, str) or not session.strip():
            return "claim events require a non-empty 'session' field"
    elif session is not None and (not isinstance(session, str) or not session.strip()):
        return "session must be a non-empty string when supplied"

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
        if isinstance(learning, str):
            # process_task_events.py's prepare_learning() coerces a bare string
            # into {kind, stakes, lesson} (conductor/t-097) rather than
            # rejecting it, so this PR-time gate accepts the same shape.
            if not learning.strip():
                return "learning must be a non-empty string when supplied as a string"
        elif isinstance(learning, dict):
            required = {"kind", "stakes", "lesson"}
            missing = sorted(required - learning.keys())
            if missing:
                return f"learning is missing required fields: {', '.join(missing)}"
        else:
            return "learning must be a mapping or a plain string lesson"

    try:
        continuous_improvement_fields(event)
    except ValueError as error:
        return str(error)

    # conductor/t-112: catch a malformed `verify_pr` at PR time, the same way
    # `continuous_improvement_pr` already is above -- shape only (owner/repo#number),
    # never the live GitHub merge check itself (this validator is offline-only).
    try:
        extract_pr_references(event)
    except ValueError as error:
        return str(error)

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
