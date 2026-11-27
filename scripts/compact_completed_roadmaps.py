#!/usr/bin/env python3
"""Close fully satisfied finite milestones and compact done notes on workable roadmaps.

Run inside the serialized task-event writer, not a second main writer. No task
status, ID, approval, dependency or claim is changed here. Existing history is
preserved; unsafe archives are declined with a diagnostic.
"""
from pathlib import Path

import yaml

import archive_done_task_notes as archive
from project_lifecycle import (
    WORKABLE_PROJECT_STATUSES,
    lifecycle_status,
    load_project_overrides,
)
from roadmap_deps import dependency_satisfied

ROOT = Path(__file__).resolve().parents[1]


def fields(node):
    return {key.value: value for key, value in node.value}


def reconcile_milestones(text):
    """Surgical scalar replacements; do not reserialize the roadmap."""
    data = yaml.safe_load(text) or {}
    completed = {
        milestone["id"]
        for milestone in data.get("milestones") or []
        if milestone.get("status") not in ("done", "complete")
        and (
            finite := [
                task
                for task in data.get("tasks") or []
                if task.get("milestone") == milestone["id"]
                and not task.get("recurring")
            ]
        )
        and all(dependency_satisfied(task) for task in finite)
    }
    if not completed:
        return text, []
    milestones = fields(yaml.compose(text))["milestones"]
    edits = []
    for item in milestones.value:
        values = fields(item)
        if values["id"].value in completed:
            status = values.get("status")
            if status is None:
                # A malformed or underspecified milestone is not silently edited.
                continue
            edits.append((status.start_mark.index, status.end_mark.index, values["id"].value))
    for start, end, _ in sorted(edits, reverse=True):
        text = text[:start] + "done" + text[end:]
    expected = data
    changed = [mid for _, _, mid in edits]
    for milestone in expected["milestones"]:
        if milestone["id"] in changed:
            milestone["status"] = "done"
    assert yaml.safe_load(text) == expected
    return text, changed


def main():
    overrides = load_project_overrides(ROOT / "project-overrides.yaml")
    for path in sorted((ROOT / "projects").glob("*/roadmap.yaml")):
        slug = path.parent.name
        if slug == "_template" or lifecycle_status(overrides, slug) not in WORKABLE_PROJECT_STATUSES:
            continue
        before = path.read_text(encoding="utf-8")
        after, closed = reconcile_milestones(before)
        if closed:
            path.write_text(after, encoding="utf-8")
            print(f"{slug}: completed milestones {', '.join(closed)}")
        result = archive.archive_project(slug)
        if result["archived"]:
            print(f"{slug}: compacted {len(result['archived'])} completed tasks")
        for task_id, reason in result["failed"]:
            print(f"::warning::{slug}/{task_id}: archive declined: {reason}")


if __name__ == "__main__":
    main()
