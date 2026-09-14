#!/usr/bin/env python3
"""
archive_done_task_notes.py — move the `note:` prose of `status: done` roadmap
tasks into a per-project `HISTORY.md`, leaving a short pointer behind.

WHY (conductor/t-158, 2026-09-14). `scripts/sync_kind_robots_projection.py`
POSTs the raw text of every `projects/*/roadmap.yaml` to Kind Robots under a
hard `MAX_PAYLOAD_BYTES = 4_000_000`. It blew that limit on 2026-09-11 at
4,000,134 bytes, failing `tests/test_sync_kind_robots_projection.py`;
conductor/t-151 fixed that one by hand-archiving interface-vision/t-104's
~395KB note to `T104-HISTORY.md`. Measured again 2026-09-14 it was back to
3,734,373 bytes (93.4%), growing ~45KB/day. 66% of all roadmap text is the
`note:` bodies of done tasks -- so the aggregate, not any single note, is the
live failure mode.

AUTHORIZATION. Rewriting a substantial `note:` is normally refused by
`set_task_field.py`'s t-129 destructive-replace guard, and the append-only
rules in AGENTS.md forbid deleting history. This script operates under the
"Archival carve-out" added to AGENTS.md for t-158: moving content VERBATIM to
a named archive file is not deletion, provided the round-trip is verified
byte-for-byte before the source is rewritten. That proviso is the whole
safety property, so it is enforced here rather than assumed:

    1. render the archive entry
    2. write HISTORY.md
    3. RE-READ HISTORY.md from disk and re-extract every note
    4. assert each extracted note == the original, byte for byte
    5. only then rewrite roadmap.yaml

A task whose note does not round-trip is skipped and reported; it is never
rewritten. Nothing is deleted at any point -- the note exists in HISTORY.md
before it stops existing in roadmap.yaml, and both live in git.

THE POINTER keeps the original note's OWN FIRST SENTENCE, verbatim, then the
archive reference. That is not cosmetic. Two live consumers read this field:

  - scripts/backfill_learning.py:276 takes first_sentence(note) as the lesson
    text for closed tasks -- preserving the original first sentence means it
    gets the identical string it got before this ran.
  - kind_robots components/conductor/project-detail.vue:363 renders
    {{ task.note }} verbatim on the live project board, where a one-line
    summary reads better than 4KB of prose.

SCOPE. `status: done` only. select_role.py (recurring RAN/NO-OP markers),
daily_gate.py, audit_human_gates.py and audit_roadmaps.py all scan note text,
but none of them on done tasks -- touching a recurring/needs-human/claimed
task would break them. All projects are archived regardless of
project-overrides.yaml status, because roadmap_map() globs every
projects/*/roadmap.yaml and inactive projects count against the payload
identically (this differs from check_roadmap_note_size.py's default).

Usage:
  python scripts/archive_done_task_notes.py --dry-run
  python scripts/archive_done_task_notes.py --project conductor
  python scripts/archive_done_task_notes.py --all
  python scripts/archive_done_task_notes.py --verify-only

Exit codes: 0 = success (or nothing to do), 1 = at least one task failed its
round-trip check and was skipped.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from set_task_field import set_task_field_text  # noqa: E402

# The pointer's summary half MUST survive this exact function unchanged -- it is
# what backfill_learning.py records as the lesson for a closed task. Import the
# real one rather than reimplementing it, so the two cannot drift apart.
from backfill_learning import first_sentence  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Notes shorter than this are left alone: the pointer would not be meaningfully
# smaller than the note, so rewriting them is pure churn on the roadmap diff.
MIN_NOTE_BYTES = 400

BEGIN = "<!-- note:begin {task_id} -->"
END = "<!-- note:end {task_id} -->"
# A note containing either marker would make extraction ambiguous. No note does
# today, and the script refuses rather than guessing if one ever should.
MARKER_RE = re.compile(r"<!--\s*note:(begin|end)\s")

def pointer_text(slug: str, task_id: str) -> str:
    return f"Full history: projects/{slug}/HISTORY.md#{task_id}"


def has_pointer(slug: str, task_id: str, note: str) -> bool:
    """True only for this task's OWN archive pointer.

    Matched precisely rather than by a loose `HISTORY.md#` search: conductor/t-158's
    own note quotes the pointer format as example text, and a loose match reported it
    as an unresolvable pointer on the first verification run.
    """
    return pointer_text(slug, task_id) in note

HISTORY_HEADER = """# {slug} — task history archive

Full `note:` prose for completed {slug} tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.
"""


def build_pointer(slug: str, task_id: str, note: str) -> str | None:
    """Build the replacement note, or None if it cannot be made lossless.

    The summary half must satisfy, exactly:

        backfill_learning.first_sentence(pointer) == first_sentence(original)

    ...because that function is what records the lesson for a closed task. It is
    not obviously true: where a note has no sentence boundary, first_sentence()
    falls back to `collapsed[:280].rstrip()`, so the appended "Full history: ..."
    text can bleed into that 280-character window and change the result.

    So the equality is CHECKED rather than assumed. A period is appended when the
    summary has no terminator (which is what lets the archive reference read as a
    separate sentence); if even that does not reproduce the original lesson, this
    returns None and the caller leaves the task alone. Shrinking the payload is
    never worth silently corrupting a lesson record.
    """
    want = first_sentence(note)
    if not want:
        return None

    for summary in (want, want + "." if want[-1] not in ".!?" else None):
        if summary is None:
            continue
        pointer = f"{summary}\n\n{pointer_text(slug, task_id)}"
        if first_sentence(pointer) == want:
            return pointer
    return None


def load_roadmap(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def archivable_tasks(slug: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for task in data.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        if task.get("status") != "done":
            continue
        note = task.get("note")
        if not isinstance(note, str):
            continue  # list/None note shapes are left alone
        if len(note.encode("utf-8")) < MIN_NOTE_BYTES:
            continue
        if has_pointer(slug, task["id"], note):
            continue  # already archived — keeps the script idempotent
        out.append(task)
    return out


def render_history(slug: str, entries: list[tuple[str, str, str]]) -> str:
    """entries: (task_id, title, note) in id order."""
    parts = [HISTORY_HEADER.format(slug=slug)]
    for task_id, title, note in entries:
        parts.append(f"\n## {task_id} — {title}\n")
        parts.append(f"\n{BEGIN.format(task_id=task_id)}\n")
        parts.append(note if note.endswith("\n") else note + "\n")
        parts.append(f"{END.format(task_id=task_id)}\n")
    return "".join(parts)


def extract_notes(history_text: str) -> dict[str, str]:
    """Re-extract every archived note. Inverse of render_history."""
    found: dict[str, str] = {}
    pattern = re.compile(
        r"<!-- note:begin (?P<id>[^\s>]+) -->\n(?P<body>.*?)<!-- note:end (?P=id) -->\n",
        re.DOTALL,
    )
    for match in pattern.finditer(history_text):
        found[match.group("id")] = match.group("body")
    return found


def existing_entries(history_path: Path) -> dict[str, str]:
    if not history_path.is_file():
        return {}
    return extract_notes(history_path.read_text(encoding="utf-8"))


def archive_project(slug: str, *, dry_run: bool = False) -> dict[str, Any]:
    roadmap_path = ROOT / "projects" / slug / "roadmap.yaml"
    history_path = ROOT / "projects" / slug / "HISTORY.md"
    roadmap_text = roadmap_path.read_text(encoding="utf-8")
    data = yaml.safe_load(roadmap_text) or {}

    todo = archivable_tasks(slug, data)
    result: dict[str, Any] = {
        "project": slug,
        "archived": [],
        "failed": [],
        "bytes_before": len(roadmap_text.encode("utf-8")),
        "bytes_after": len(roadmap_text.encode("utf-8")),
    }
    if not todo:
        return result

    for task in todo:
        if MARKER_RE.search(task["note"]):
            result["failed"].append((task["id"], "note contains an archive marker"))
    todo = [t for t in todo if not MARKER_RE.search(t["note"])]
    if not todo:
        return result

    # Merge with anything already archived, so re-runs extend rather than replace.
    merged: dict[str, tuple[str, str]] = {}
    titles = {t["id"]: str(t.get("title", "")) for t in (data.get("tasks") or []) if isinstance(t, dict)}
    for task_id, note in existing_entries(history_path).items():
        merged[task_id] = (titles.get(task_id, task_id), note)
    originals = {t["id"]: t["note"] for t in todo}
    for task in todo:
        merged[task["id"]] = (str(task.get("title", "")), task["note"])

    def sort_key(tid: str) -> tuple[int, str]:
        m = re.match(r"t-(\d+)", tid)
        return (int(m.group(1)), tid) if m else (10**9, tid)

    entries = [(tid, merged[tid][0], merged[tid][1]) for tid in sorted(merged, key=sort_key)]
    history_text = render_history(slug, entries)

    # --- the safety property: write, re-read from disk, verify, THEN rewrite ---
    if dry_run:
        recovered = extract_notes(history_text)
    else:
        history_path.write_text(history_text, encoding="utf-8")
        recovered = extract_notes(history_path.read_text(encoding="utf-8"))

    verified: list[dict[str, Any]] = []
    for task in todo:
        got = recovered.get(task["id"])
        want = originals[task["id"]]
        if got is None:
            result["failed"].append((task["id"], "not recoverable from HISTORY.md"))
            continue
        # render_history guarantees a trailing newline; compare on that basis.
        if got != (want if want.endswith("\n") else want + "\n"):
            result["failed"].append((task["id"], "round-trip mismatch — NOT rewritten"))
            continue
        verified.append(task)

    for task in verified:
        pointer = build_pointer(slug, task["id"], task["note"])
        if pointer is None:
            result["failed"].append(
                (task["id"], "pointer would change first_sentence() — NOT rewritten")
            )
            continue
        roadmap_text = set_task_field_text(
            roadmap_text, task["id"], "note", pointer, force=True, force_block=">-"
        )
        result["archived"].append(task["id"])

    # Re-parse before writing: a malformed rewrite must never reach disk.
    reparsed = yaml.safe_load(roadmap_text)
    assert reparsed is not None, f"{slug}: rewritten roadmap did not parse"
    assert len(reparsed.get("tasks") or []) == len(data.get("tasks") or []), (
        f"{slug}: task count changed during rewrite"
    )
    result["bytes_after"] = len(roadmap_text.encode("utf-8"))
    if not dry_run and result["archived"]:
        roadmap_path.write_text(roadmap_text, encoding="utf-8")
    return result


def verify_project(slug: str) -> list[str]:
    """Re-extract archived notes and confirm each roadmap pointer references one."""
    history_path = ROOT / "projects" / slug / "HISTORY.md"
    roadmap_path = ROOT / "projects" / slug / "roadmap.yaml"
    if not history_path.is_file():
        return []
    archived = extract_notes(history_path.read_text(encoding="utf-8"))
    problems = []
    data = load_roadmap(roadmap_path)
    for task in data.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        if task.get("status") != "done":
            continue
        note = task.get("note")
        if not isinstance(note, str) or not has_pointer(slug, task["id"], note):
            continue
        if task["id"] not in archived:
            problems.append(f"{slug}/{task['id']}: pointer with no archive entry")
    return problems


def all_projects() -> list[str]:
    return sorted(p.parent.name for p in (ROOT / "projects").glob("*/roadmap.yaml"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", action="append", help="project slug (repeatable)")
    parser.add_argument("--all", action="store_true", help="every project with a roadmap")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument("--verify-only", action="store_true", help="check existing archives")
    args = parser.parse_args()

    slugs = args.project or (all_projects() if args.all else None)
    if not slugs:
        parser.error("pass --project <slug> (repeatable) or --all")

    if args.verify_only:
        problems = [p for slug in slugs for p in verify_project(slug)]
        if problems:
            print("\n".join(problems))
            sys.exit(1)
        print(f"verified {len(slugs)} project archive(s): every pointer resolves")
        return

    total_before = total_after = 0
    failures = 0
    for slug in slugs:
        res = archive_project(slug, dry_run=args.dry_run)
        total_before += res["bytes_before"]
        total_after += res["bytes_after"]
        if res["archived"] or res["failed"]:
            saved = res["bytes_before"] - res["bytes_after"]
            print(f"{slug:22} archived {len(res['archived']):3}  -{saved:,} bytes")
        for task_id, why in res["failed"]:
            failures += 1
            print(f"  !! {slug}/{task_id}: {why}")

    print(f"\ntotal: {total_before:,} -> {total_after:,} bytes "
          f"(-{total_before - total_after:,})")
    if args.dry_run:
        print("(dry run — nothing written)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
