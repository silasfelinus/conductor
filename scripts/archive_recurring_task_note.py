#!/usr/bin/env python3
"""
archive_recurring_task_note.py — move a LIVE (non-done) task's oversized `note:`
history to a dedicated `<TASK-ID>-HISTORY.md`, leaving a short status pointer.

WHY. `archive_done_task_notes.py` (conductor/t-158) only ever touches `status:
done` tasks, by design — its SCOPE note explains that several scripts
(select_role.py's recurring RAN/NO-OP staleness check, daily_gate.py,
audit_human_gates.py, audit_roadmaps.py) scan note text on live tasks, so
touching one there could break them. But a live `recurring: true` grinder task
(the front-end "polish and upgrade" pattern, or a production-pass task like
coloring-book/t-022) accumulates one cycle's prose per run indefinitely and has
no other path back under `check_roadmap_note_size.py`'s 50,000-byte
single-note threshold. Before this script, the only precedent was a fully
manual one-off: interface-vision/t-104's note was hand-archived to
`T104-HISTORY.md` at slice 234 (conductor/t-151, 2026-09-11), a pattern
`check_roadmap_note_size.py`'s own advisory text names but never automated.
This generalizes that pattern into a reusable, verified script instead of a
one-off manual edit repeated ad hoc each time a different task reaches the
threshold.

AUTHORIZATION. Same "Archival carve-out" as `archive_done_task_notes.py`
(AGENTS.md, authorized by Silas 2026-09-14 for conductor/t-158): moving
content VERBATIM into a named archive file is not deletion, provided the
round-trip is verified byte-for-byte before the source is rewritten, and a
pointer is left at the original location. Unlike the done-task script, THE
ENTIRE current note is archived (not summarized to one sentence) because a
live task's note is still actively read for current status by the next
session that claims it — the replacement pointer must say where things stand
now, not just where the history lives. Future cycles append fresh to the new,
short live note (this is exactly what happened to T104's own live note after
its slice-234 archival: it grew back to ~40KB over the following slices,
still comfortably under threshold).

SCOPE. Any task regardless of `status` — call it explicitly per (project,
task-id), never in bulk, since the replacement pointer text has to actually
describe current state and only a human/agent reading the note can write
that. This script does the mechanical, safety-critical half (archive, verify,
rewrite); the caller supplies the pointer text.

Usage:
  python scripts/archive_recurring_task_note.py <project> <task-id> \\
      --pointer-file <path to short replacement note text> [--dry-run]

Exit codes: 0 = archived (or dry-run showed what would happen),
            1 = round-trip verification failed — nothing was written.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from set_task_field import set_task_field_text  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

BEGIN = "<!-- note:begin {task_id} -->"
END = "<!-- note:end {task_id} -->"
MARKER_RE = re.compile(r"<!--\s*note:(begin|end)\s")


def history_filename(task_id: str) -> str:
    # t-104 -> T104-HISTORY.md, matching the interface-vision precedent exactly.
    digits = task_id.upper().replace("T-", "")
    return f"T{digits}-HISTORY.md"


def render_archive(project: str, task_id: str, title: str, note: str) -> str:
    header = (
        f"# {project}/{task_id} — full note history archive\n\n"
        f"This file is the archaeology index for {project}/{task_id} "
        f'("{title}"). Its `note:` field in `roadmap.yaml` grew past '
        "`check_roadmap_note_size.py`'s 50,000-byte single-note threshold "
        "through ordinary recurring-cycle accumulation. The complete verbatim "
        "history through the archival point is preserved below; `roadmap.yaml` "
        "keeps only a short current-status pointer going forward. Do not "
        "restore this text into the live roadmap — read it here when you need "
        "to know what a specific past cycle found or did.\n\n"
        "Archived under the AGENTS.md archival carve-out (byte-for-byte "
        "verified round-trip, pointer left behind, no history lost).\n"
    )
    body = (
        f"\n{BEGIN.format(task_id=task_id)}\n"
        f"{note if note.endswith(chr(10)) else note + chr(10)}"
        f"{END.format(task_id=task_id)}\n"
    )
    return header + body


def extract_note(history_text: str, task_id: str) -> str | None:
    pattern = re.compile(
        rf"<!-- note:begin {re.escape(task_id)} -->\n(?P<body>.*?)<!-- note:end {re.escape(task_id)} -->\n",
        re.DOTALL,
    )
    m = pattern.search(history_text)
    return m.group("body") if m else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project")
    parser.add_argument("task_id")
    parser.add_argument("--pointer-file", required=True, help="path to a text file with the replacement note")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    roadmap_path = ROOT / "projects" / args.project / "roadmap.yaml"
    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    data = yaml.safe_load(roadmap_text) or {}

    task = next(
        (t for t in (data.get("tasks") or []) if isinstance(t, dict) and t.get("id") == args.task_id),
        None,
    )
    if task is None:
        sys.exit(f"{args.project}/{args.task_id}: task not found")
    note = task.get("note")
    if not isinstance(note, str):
        sys.exit(f"{args.project}/{args.task_id}: note is not a plain string, refusing")
    if MARKER_RE.search(note):
        sys.exit(f"{args.project}/{args.task_id}: note already contains an archive marker, refusing")

    title = str(task.get("title", ""))
    history_path = ROOT / "projects" / args.project / history_filename(args.task_id)
    if history_path.exists():
        sys.exit(f"{history_path} already exists — refusing to overwrite an existing archive")

    archive_text = render_archive(args.project, args.task_id, title, note)

    if args.dry_run:
        recovered = extract_note(archive_text, args.task_id)
    else:
        history_path.write_text(archive_text, encoding="utf-8")
        recovered = extract_note(history_path.read_text(encoding="utf-8"), args.task_id)

    want = note if note.endswith("\n") else note + "\n"
    if recovered != want:
        sys.exit(1)  # round-trip failed; history_path (if written) is left for inspection, roadmap untouched

    pointer = Path(args.pointer_file).read_text(encoding="utf-8").rstrip("\n")

    if args.dry_run:
        print(f"[dry-run] would archive {len(note):,} bytes to {history_path}")
        print(f"[dry-run] would replace note with ({len(pointer)} bytes):\n{pointer}")
        return

    new_roadmap_text = set_task_field_text(
        roadmap_text, args.task_id, "note", pointer, force=True, force_block=">-"
    )
    reparsed = yaml.safe_load(new_roadmap_text)
    assert reparsed is not None, f"{args.project}: rewritten roadmap did not parse"
    assert len(reparsed.get("tasks") or []) == len(data.get("tasks") or []), (
        f"{args.project}: task count changed during rewrite"
    )
    roadmap_path.write_text(new_roadmap_text, encoding="utf-8")
    print(
        f"archived {args.project}/{args.task_id}: {len(note):,} -> {history_path.name}; "
        f"live note now {len(pointer):,} bytes"
    )


if __name__ == "__main__":
    main()
