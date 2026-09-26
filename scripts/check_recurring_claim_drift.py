#!/usr/bin/env python3
"""
check_recurring_claim_drift.py — flag a task stuck at `status: claimed` whose
own `claimed_by`/`claimed_at` are already null.

Root-caused for conductor/t-195: model-builder/t-029 (a recurring
regression-audit grinder) drifted twice (2026-08-12, 2026-09-25) into
`status: claimed` with `claimed_by`/`claimed_at` already null, while its own
cycle note said "re-arming to ready". Both times this was only caught
incidentally, by check_pr_merged_drift.py noticing a stale `implementation_pr`
-- nothing directly watched for the drift itself.

The actual mechanism (traced via the 2026-09-23 cycle-101 close, PR #5150):
claim_task.py and close_task.py both write `status`, `claimed_by`, and
`claimed_at` together as one atomic edit, so a single close_task.py run is
never the cause. The drift happened one layer up, in a *manual* merge-conflict
resolution: the close branch had correctly set `status: ready`, but merging
`origin/main` into it hit a real conflict on the same file (another task's
concurrent claim landed on `main` first) and the conflict was resolved by
keeping `origin/main`'s copy of the *whole* conflicted region -- which
included model-builder/t-029's now-stale `status: claimed` alongside the
other task's genuinely newer content. AGENTS.md already says to resolve
conflicts per-task, not per-file; this is a mechanical backstop for exactly
the case where that didn't happen.

This is a general roadmap invariant, not a recurring-only one: both
claim_task.py and process_task_events.py's claim handling only ever write
`status: claimed` together with non-null `claimed_by`/`claimed_at` in the same
edit, and only ever clear `claimed_by`/`claimed_at` when moving status away
from `claimed`/`review`. A task showing `status: claimed` with both already
null is therefore never a live claim -- it is always this drift.

Advisory only, same discipline as check_priority_queue_starvation.py and
check_daily_commitment_staleness.py: never blocks task selection or gates
anything. Excludes paused/retired/finished projects by default per
project-overrides.yaml, matching the other roadmap-reading checks;
--include-inactive for an intentional archive sweep. Purely local YAML
analysis -- no network access, no KR_API_TOKEN needed.

Usage:
  python scripts/check_recurring_claim_drift.py
  python scripts/check_recurring_claim_drift.py --json
  python scripts/check_recurring_claim_drift.py --include-inactive

Exit codes: 0 = clean (or nothing to check), 1 = at least one task flagged.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
OVERRIDES_PATH = ROOT / "project-overrides.yaml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_lifecycle import load_project_overrides, lifecycle_status  # noqa: E402

# Matches the several phrasings past cycle notes have used for "this task's
# work is done for now, hand it back" -- purely informational corroboration,
# never load-bearing for the finding itself.
REARM_RE = re.compile(r"re-arm(?:ed|ing|s)?\s+to\s+ready|releasing the claim", re.IGNORECASE)


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def project_roadmap_paths(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[Path]:
    projects_dir = projects_dir or PROJECTS_DIR
    overrides = load_project_overrides(overrides_path or OVERRIDES_PATH)
    paths = []
    for path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = path.parent.name
        if slug == "_template":
            continue
        if not include_inactive and lifecycle_status(overrides, slug) not in (
            "active",
            "continuous",
        ):
            continue
        paths.append(path)
    return paths


def note_mentions_rearm(note: object) -> bool:
    if not isinstance(note, str) or not note.strip():
        return False
    last_paragraph = note.strip().split("\n\n")[-1]
    return bool(REARM_RE.search(last_paragraph))


def scan(
    *,
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for path in project_roadmap_paths(projects_dir, overrides_path, include_inactive):
        roadmap = load_yaml(path)
        if not isinstance(roadmap, dict):
            continue
        project = roadmap.get("project") or path.parent.name

        for task in roadmap.get("tasks", []) or []:
            if not isinstance(task, dict):
                continue
            if task.get("status") != "claimed":
                continue
            if task.get("claimed_by") or task.get("claimed_at"):
                continue

            findings.append(
                {
                    "project": project,
                    "task_id": task.get("id"),
                    "title": task.get("title"),
                    "recurring": bool(task.get("recurring")),
                    "note_mentions_rearm": note_mentions_rearm(task.get("note")),
                }
            )

    return findings


def render(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return (
            "No recurring-claim drift found -- every status: claimed task still "
            "carries a live claimed_by/claimed_at."
        )

    lines = [
        f"Recurring-claim drift: {len(findings)} task(s) stuck at status: claimed "
        "with claimed_by/claimed_at already null.",
        "",
    ]
    for entry in findings:
        recurring_tag = " [recurring]" if entry["recurring"] else ""
        lines.append(f"  {entry['project']}/{entry['task_id']}{recurring_tag} {entry['title']}")
        if entry["note_mentions_rearm"]:
            lines.append(
                "      note's own last paragraph already says it re-armed/released "
                "the claim -- status write did not land"
            )
        lines.append("")

    lines.append(
        "This combination (status: claimed with both claimed_by and claimed_at "
        "null) never occurs from a live claim -- claim_task.py and "
        "process_task_events.py always write all three together. It means a "
        "close/re-arm's status write was lost, most often in a manual "
        "merge-conflict resolution that kept origin/main's stale copy of this "
        "task's status alongside another task's genuinely newer change in the "
        "same file (see conductor/t-195). Fix: set status back to ready (or "
        "whatever the note's last paragraph says actually happened) via "
        "scripts/close_task.py, same as any other close-out."
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also scan paused/retired/finished projects",
    )
    args = parser.parse_args()

    findings = scan(include_inactive=args.include_inactive)

    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        print(render(findings))

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
