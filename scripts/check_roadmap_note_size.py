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

# conductor/t-158 (2026-09-14). The single-note threshold above watches the shape
# that broke t-104: ONE note growing without bound. It does not see the shape that
# actually put the payload back at 93.4% three days after t-104 was archived --
# 154 medium notes summing to 411KB in one file, none individually over 50KB. So
# two aggregate checks sit alongside it.
#
# Per-file: a roadmap.yaml this large is a projection risk on its own and is worth
# an archival pass (post-t-158 the largest is ~90KB).
DEFAULT_FILE_THRESHOLD_BYTES = 150_000

# The real ceiling. sync_kind_robots_projection.py POSTs {"roadmaps": {slug: raw
# text}} and refuses over MAX_PAYLOAD_BYTES; exceeding it fails
# tests/test_sync_kind_robots_projection.py and stops the Kind Robots board from
# syncing. Kept in step with that module rather than duplicated by hand.
try:  # pragma: no cover - trivial import shim
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sync_kind_robots_projection import MAX_PAYLOAD_BYTES
except Exception:  # noqa: BLE001 - the check degrades, the sweep still runs
    MAX_PAYLOAD_BYTES = 4_000_000

# Warn while there is still room to act. t-104 went from "fine" to over the limit
# with no warning at all; ~45KB/day of growth makes 80% roughly a fortnight out.
PAYLOAD_WARN_RATIO = 0.80


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


def file_findings(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = True,
    file_threshold_bytes: int = DEFAULT_FILE_THRESHOLD_BYTES,
) -> list[dict[str, Any]]:
    """Roadmap FILES over the per-file threshold.

    Defaults to include_inactive=True unlike the per-note check: roadmap_map()
    ships every projects/*/roadmap.yaml regardless of project status, so a
    retired project's file counts against the ceiling exactly as much.
    """
    findings = []
    for path in project_roadmap_paths(projects_dir, overrides_path, include_inactive):
        size = len(path.read_bytes())
        if size < file_threshold_bytes:
            continue
        findings.append(
            {
                "project": path.parent.name,
                "file_bytes": size,
                "threshold_bytes": file_threshold_bytes,
                "detail": (
                    f"{_display_path(path)} is {size:,} bytes (over the "
                    f"{file_threshold_bytes:,}-byte per-file threshold)"
                ),
            }
        )
    findings.sort(key=lambda f: f["file_bytes"], reverse=True)
    return findings


def payload_status() -> dict[str, Any]:
    """Measure the real Kind Robots projection payload against its hard limit.

    Built with sync_kind_robots_projection's own functions and encoder rather
    than an approximation, so the number here is the number that module will
    refuse on. The git SHA and timestamp it also sends are a few dozen bytes and
    are omitted to keep this check free of subprocess calls.
    """
    try:
        import sync_kind_robots_projection as proj

        snapshot = {
            "registryYaml": proj.read_text(ROOT / "project-overrides.yaml"),
            "roadmaps": proj.roadmap_map(),
            "pitches": proj.text_map(ROOT / "pitches", "*.md"),
            "imageVersions": proj.image_versions(),
        }
        size = len(
            json.dumps(snapshot, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        )
    except Exception as error:  # noqa: BLE001 - never break the sweep over this
        return {"measured": False, "detail": f"payload not measured: {error}"}

    ratio = size / MAX_PAYLOAD_BYTES if MAX_PAYLOAD_BYTES else 0.0
    return {
        "measured": True,
        "payload_bytes": size,
        "limit_bytes": MAX_PAYLOAD_BYTES,
        "headroom_bytes": MAX_PAYLOAD_BYTES - size,
        "ratio": ratio,
        "over_warn": ratio >= PAYLOAD_WARN_RATIO,
    }


def scan(
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
    threshold_bytes: int = DEFAULT_THRESHOLD_BYTES,
    file_threshold_bytes: int = DEFAULT_FILE_THRESHOLD_BYTES,
    check_payload: bool = True,
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
    return {
        "findings": findings,
        "threshold_bytes": threshold_bytes,
        "file_findings": file_findings(
            projects_dir, overrides_path, True, file_threshold_bytes
        ),
        "file_threshold_bytes": file_threshold_bytes,
        "payload": payload_status() if check_payload else {"measured": False},
    }


def render_payload_line(payload: dict[str, Any]) -> str:
    """One line for the CLAUDE.md startup sweep: how much room is actually left."""
    if not payload.get("measured"):
        return f"Projection payload: {payload.get('detail', 'not measured')}"
    return (
        f"Projection payload: {payload['payload_bytes']:,} / {payload['limit_bytes']:,} bytes "
        f"({payload['ratio'] * 100:.1f}%), headroom {payload['headroom_bytes']:,}"
    )


def render(result: dict[str, Any]) -> str:
    findings = result["findings"]
    threshold = result["threshold_bytes"]
    files = result.get("file_findings") or []
    payload = result.get("payload") or {}
    lines: list[str] = []

    if findings:
        lines.append(
            f"Oversized roadmap note: fields ({len(findings)}, threshold {threshold:,} bytes):"
        )
        for f in findings:
            if f["note_bytes"] is None:
                lines.append(f"  - {f['project']}: {f['detail']}")
                continue
            recurring_tag = " [recurring]" if f["recurring"] else ""
            lines.append(
                f"  - {f['project']}/{f['task']}{recurring_tag} {f['title']!r}: "
                f"{f['note_bytes']:,} bytes"
            )
    else:
        lines.append(
            "No oversized roadmap note fields found — every task's note: is under "
            f"the {threshold:,}-byte threshold."
        )

    if files:
        lines.append(
            f"\nOversized roadmap FILES ({len(files)}, threshold "
            f"{result['file_threshold_bytes']:,} bytes):"
        )
        for f in files:
            lines.append(f"  - {f['project']}: {f['file_bytes']:,} bytes")

    lines.append("\n" + render_payload_line(payload))
    if payload.get("measured") and payload.get("over_warn"):
        lines.append(
            f"  !! at or past {PAYLOAD_WARN_RATIO * 100:.0f}% of the hard limit. Crossing it "
            "fails tests/test_sync_kind_robots_projection.py and stops the Kind Robots "
            "board syncing (it happened 2026-09-11 at 4,000,134 bytes). Run "
            "`python scripts/archive_done_task_notes.py --all`."
        )

    lines.append(
        "\nAdvisory only -- this never blocks a merge or a task claim, and never "
        "auto-truncates a note. Archive done-task history with "
        "`scripts/archive_done_task_notes.py` (verified byte-for-byte into "
        "projects/<slug>/HISTORY.md under AGENTS.md's archival carve-out); for a single "
        "oversized note on a live recurring task, the t-104 pattern of a dedicated "
        "<project>/<task-id>-HISTORY.md plus a short pointer still applies (see "
        "T104-HISTORY.md)."
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
    parser.add_argument(
        "--file-threshold-bytes",
        type=int,
        default=DEFAULT_FILE_THRESHOLD_BYTES,
        help=f"roadmap.yaml size in bytes to flag (default: {DEFAULT_FILE_THRESHOLD_BYTES:,})",
    )
    parser.add_argument(
        "--payload-only",
        action="store_true",
        help="print just the projection headroom line (for the startup sweep)",
    )
    args = parser.parse_args()

    if args.payload_only:
        payload = payload_status()
        print(render_payload_line(payload))
        sys.exit(1 if payload.get("over_warn") else 0)

    result = scan(
        include_inactive=args.include_inactive,
        threshold_bytes=args.threshold_bytes,
        file_threshold_bytes=args.file_threshold_bytes,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))

    sys.exit(
        1
        if result["findings"]
        or result["file_findings"]
        or result["payload"].get("over_warn")
        else 0
    )


if __name__ == "__main__":
    main()
