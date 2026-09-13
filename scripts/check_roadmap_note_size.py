#!/usr/bin/env python3
"""
check_roadmap_note_size.py — Flag a roadmap task's `note:` field before it
grows large enough to blow the Kind-Robots projection payload limit.

Kaizen from conductor/t-151 (filed 2026-09-11 from interface-vision/t-104
slice 234's close-out): that task's `note:` field had grown to ~395KB across
234 appended slice-history paragraphs and was the single dominant contributor
pushing the whole Kind-Robots projection snapshot
(`scripts/sync_kind_robots_projection.py`) to 4,000,134 bytes against its
4,000,000-byte `MAX_PAYLOAD_BYTES` transport limit, failing
`tests/test_sync_kind_robots_projection.py` and `scripts/sync_projects.py` in
CI on conductor PR #4117. Fixed in that PR by archiving the full history to
`projects/interface-vision/T104-HISTORY.md` and trimming the live note to a
short pointer.

That was not an isolated case: a repo-wide sweep at filing time found several
other large `note:` fields on similarly recurring tasks (model-builder/t-029
~118KB, storybook/t-010 ~63KB, dream-cycle/t-006 ~38KB, and others). The
pattern is the same on every one: a `recurring: true` task whose Worker/
Reviewer close-out convention appends full prose history to the live roadmap
`note:` field every cycle, forever. The next one to cross a few hundred KB
trips the same CI failure with no advance warning -- exactly what happened to
t-104.

This is a "(b) periodic sweep" advisory guard, the shape t-151 itself
proposed as an alternative to a CI/pre-merge check: it never blocks a merge
or a task claim, it only reports tasks whose `note:` field has crossed a
size threshold (default 50,000 bytes) so a session can proactively archive
the history the same way t-104 was archived, before the aggregate
Kind-Robots projection snapshot is ever at risk. It never auto-truncates a
note itself -- deciding what is safe to move to an archive file needs the
same judgment applied to t-104's own fix.

Excludes paused, retired, and finished projects by default according to
project-overrides.yaml, matching check_milestone_status_drift.py,
check_pr_merged_drift.py, check_project_scaffold_drift.py, and
audit_human_gates.py. Use --include-inactive for an intentional archive
sweep. Purely local YAML analysis -- no network access, no KR_API_TOKEN
needed.

Usage:
  python scripts/check_roadmap_note_size.py
  python scripts/check_roadmap_note_size.py --json
  python scripts/check_roadmap_note_size.py --threshold-bytes 100000
  python scripts/check_roadmap_note_size.py --include-inactive

Exit codes: 0 = clean (or nothing to check), 1 = at least one task's note is
over the threshold. This is advisory -- a non-zero exit is a "worth
archiving soon" prompt, not a genuine gate; nothing here blocks a merge or a
task claim.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
OVERRIDES_PATH = ROOT / "project-overrides.yaml"
ACTIVE_STATUS = "active"

# t-151's own note suggested 50-100KB; default to the low end of that range
# so a session sees the warning well before the aggregate 4MB snapshot ceiling
# is anywhere near at risk (t-104 alone was ~395KB before it tripped CI).
DEFAULT_THRESHOLD_BYTES = 50_000


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_project_statuses(path: Path | None = None) -> dict[str, str]:
    path = path or OVERRIDES_PATH
    if not path.exists():
        return {}
    data = load_yaml(path)
    statuses: dict[str, str] = {}
    for entry in data.get("overrides", []) or []:
        if not isinstance(entry, dict):
            continue
        slug = str(entry.get("slug") or "").strip()
        if not slug:
            continue
        statuses[slug] = str(entry.get("status") or ACTIVE_STATUS).strip().lower()
    return statuses


def project_roadmap_paths(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[Path]:
    projects_dir = projects_dir or PROJECTS_DIR
    statuses = load_project_statuses(overrides_path)
    paths = []
    for path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = path.parent.name
        if slug == "_template":
            continue
        if not include_inactive and statuses.get(slug, ACTIVE_STATUS) != ACTIVE_STATUS:
            continue
        paths.append(path)
    return paths


def _display_path(path: Path) -> str:
    """Path relative to ROOT for display, falling back to the raw path when
    it isn't actually under ROOT (e.g. a test's tmp_path fixture)."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def note_size_bytes(note: Any) -> int:
    """Byte length of a task's `note:` field, tolerant of the string/list/None
    shapes seen across this repo's roadmaps."""
    if note is None:
        return 0
    if isinstance(note, str):
        text = note
    elif isinstance(note, list):
        text = "\n".join(str(item) for item in note)
    else:
        text = str(note)
    return len(text.encode("utf-8"))


def note_findings(
    project: str, roadmap: dict[str, Any], threshold_bytes: int
) -> list[dict[str, Any]]:
    """Return over-threshold findings for one project's task notes."""
    findings = []
    for task in roadmap.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        size = note_size_bytes(task.get("note"))
        if size < threshold_bytes:
            continue
        findings.append(
            {
                "project": project,
                "task": str(task.get("id")),
                "title": task.get("title"),
                "recurring": bool(task.get("recurring")),
                "note_bytes": size,
                "threshold_bytes": threshold_bytes,
                "detail": (
                    f"note: field is {size:,} bytes (over the {threshold_bytes:,}-byte "
                    "threshold)"
                ),
            }
        )
    findings.sort(key=lambda f: f["note_bytes"], reverse=True)
    return findings


def scan(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
    threshold_bytes: int = DEFAULT_THRESHOLD_BYTES,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for path in project_roadmap_paths(projects_dir, overrides_path, include_inactive):
        project = path.parent.name
        try:
            roadmap = load_yaml(path)
        except yaml.YAMLError as error:  # noqa: BLE001 - report, don't crash the sweep
            findings.append(
                {
                    "project": project,
                    "task": None,
                    "title": None,
                    "recurring": None,
                    "note_bytes": None,
                    "threshold_bytes": threshold_bytes,
                    "detail": f"{_display_path(path)} failed to parse: {error}",
                }
            )
            continue
        findings.extend(note_findings(project, roadmap, threshold_bytes))
    findings.sort(key=lambda f: f["note_bytes"] or 0, reverse=True)
    return {"findings": findings, "threshold_bytes": threshold_bytes}


def render(result: dict[str, Any]) -> str:
    findings = result["findings"]
    threshold = result["threshold_bytes"]
    if not findings:
        return (
            "No oversized roadmap note fields found — every task's note: is under "
            f"the {threshold:,}-byte threshold."
        )
    lines = [f"Oversized roadmap note: fields ({len(findings)}, threshold {threshold:,} bytes):"]
    for f in findings:
        if f["note_bytes"] is None:
            lines.append(f"  - {f['project']}: {f['detail']}")
            continue
        recurring_tag = " [recurring]" if f["recurring"] else ""
        lines.append(
            f"  - {f['project']}/{f['task']}{recurring_tag} {f['title']!r}: "
            f"{f['note_bytes']:,} bytes"
        )
    lines.append(
        "\nAdvisory only -- this never blocks a merge or a task claim, and never "
        "auto-truncates a note. Archive the full prose history to a dedicated "
        "<project>/<task-id>-HISTORY.md file and trim the live note: to a short "
        "pointer, the same pattern conductor/t-151 used for interface-vision/t-104 "
        "(see T104-HISTORY.md)."
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also check paused, retired, and finished projects",
    )
    parser.add_argument(
        "--threshold-bytes",
        type=int,
        default=DEFAULT_THRESHOLD_BYTES,
        help=f"note: size in bytes to flag (default: {DEFAULT_THRESHOLD_BYTES:,})",
    )
    args = parser.parse_args()

    result = scan(
        include_inactive=args.include_inactive,
        threshold_bytes=args.threshold_bytes,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))

    sys.exit(1 if result["findings"] else 0)


if __name__ == "__main__":
    main()
