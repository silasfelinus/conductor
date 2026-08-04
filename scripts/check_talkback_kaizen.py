#!/usr/bin/env python3
"""Reject a TALKBACK entry that promises a kaizen task id nobody ever created.

Why this exists
---------------
Every cycle's TALKBACK entry carries a `**Kaizen task:**` line naming the
follow-on it filed. That line is the only record that the follow-on was
promised — nothing checked it was actually written to `roadmap.yaml`.

Found 2026-08-04 (interface-vision/t-093, kaizen from kind_robots PR #1431):
interface-vision/TALKBACK.md contained

    **Kaizen task:** t-093 -- investigate animation-manager.vue, which
    reappeared in the one-scroll flagged list ...

while `scripts/next_free_task_id.py interface-vision` still handed out `t-093`
as unclaimed, because the task had never been added to the roadmap. Promised
scope evaporates silently in that gap: nothing fails, nothing warns, and the
next session hands the same id to different work.

A sweep at the time this was written found 214 promised ids across the active
projects and every one of them present — so this is a leak that happens rarely,
which is exactly the kind CI has to hold rather than a human remembering to
look.

What counts as a promise
------------------------
A `Kaizen task:` lead-in (bold or not) followed, within the same short span, by
a `t-NNN` id. An explicit "none" is not a promise and is skipped — sessions
legitimately close a cycle without filing one. A `project/t-NNN` prefix resolves
against that project's roadmap, since TALKBACK entries routinely file work into
a sibling project.

Inactive projects (paused, retired, finished in `project-overrides.yaml`) are
skipped, matching every other conductor sweep: resurfacing a closed project's
stale promises is the exact noise CLAUDE.md's session-startup rule warns about.

Exit codes: 0 = every promised id exists, 1 = at least one was never created.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
OVERRIDES = ROOT / "project-overrides.yaml"

ACTIVE_STATUS = "active"

# "Kaizen task:", with or without markdown bold, plus whatever follows on the
# same line. 60 characters is enough to reach the id in every entry written so
# far while staying far short of the next sentence's own t-NNN references.
LEAD = re.compile(r"\*{0,2}Kaizen task:?\*{0,2}\s*(.{0,60})", re.IGNORECASE)
REFERENCE = re.compile(r"`?(?:([a-z0-9-]+)/)?(t-\d{3})`?")
NO_TASK_FILED = re.compile(r"^\s*\**\s*(none|n/?a|—\s*none)", re.IGNORECASE)


def project_statuses(overrides: Path) -> dict[str, str]:
    """slug -> status, read the same way scripts/audit_human_gates.py reads it.

    project-overrides.yaml is a LIST under an `overrides:` key, not a mapping
    keyed by slug. Getting that wrong silently returns an empty map, which makes
    the inactive-project filter a no-op instead of an error — the exact shape of
    the bug CLAUDE.md's session-startup rule already warns about.
    """
    if not overrides.exists():
        return {}
    document = yaml.safe_load(overrides.read_text()) or {}
    statuses: dict[str, str] = {}
    for entry in document.get("overrides", []) or []:
        if not isinstance(entry, dict):
            continue
        slug = str(entry.get("slug") or "").strip()
        if slug:
            statuses[slug] = str(entry.get("status") or ACTIVE_STATUS).strip().lower()
    return statuses


def task_ids(roadmap: Path) -> set[str]:
    document = yaml.safe_load(roadmap.read_text()) or {}
    return {
        str(task.get("id"))
        for task in (document.get("tasks") or [])
        if isinstance(task, dict)
    }


def promised_ids(talkback: str, home_project: str, known: set[str]):
    """Yield (owning_project, task_id, context) for each promise in one file."""
    for lead in LEAD.finditer(talkback):
        tail = lead.group(1)
        if NO_TASK_FILED.match(tail):
            continue
        reference = REFERENCE.search(tail)
        if not reference:
            continue
        owner = reference.group(1) or home_project
        # A leading word that isn't a project (e.g. "see foo/t-012" prose) falls
        # back to the file's own project rather than inventing a roadmap.
        if owner not in known:
            owner = home_project
        yield owner, reference.group(2), tail.strip()[:70]


def scan(projects: Path, overrides: Path) -> tuple[list[str], int, int]:
    """(missing, promises_checked, projects_scanned)."""
    statuses = project_statuses(overrides)
    ids: dict[str, set[str]] = {}
    for roadmap in sorted(projects.glob("*/roadmap.yaml")):
        if roadmap.parent.name == "_template":
            continue
        ids[roadmap.parent.name] = task_ids(roadmap)

    missing: list[str] = []
    checked = 0
    scanned = 0

    for project in sorted(ids):
        if statuses.get(project, ACTIVE_STATUS) != ACTIVE_STATUS:
            continue
        talkback = projects / project / "TALKBACK.md"
        if not talkback.exists():
            continue
        scanned += 1
        for owner, task_id, context in promised_ids(
            talkback.read_text(), project, set(ids)
        ):
            checked += 1
            if task_id not in ids.get(owner, set()):
                missing.append(
                    f"{owner}/{task_id} promised in projects/{project}/TALKBACK.md "
                    f'— "{context}"'
                )

    return missing, checked, scanned


def main() -> int:
    missing, checked, scanned = scan(PROJECTS, OVERRIDES)

    if missing:
        print(f"{len(missing)} promised kaizen task(s) were never created:\n")
        for entry in missing:
            print(f"  {entry}")
        print(
            "\nA TALKBACK entry naming a kaizen id is a promise that the id "
            "exists in the matching roadmap.yaml. Create the task, or reword "
            "the entry to say none was filed."
        )
        return 1

    print(
        f"checked {checked} promised kaizen id(s) across {scanned} active "
        "project(s) — all present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
