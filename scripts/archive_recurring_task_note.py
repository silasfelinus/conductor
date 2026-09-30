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
  python scripts/archive_recurring_task_note.py <project> <task-id> \\
      --keep-head 2500 --keep-tail 4000 [--pointer-file extra.txt] [--dry-run]

ROUNDS AND AUTO-POINTERS (2026-09-30, token essentialization; closes coloring-book/t-060).
A live note re-grows after archival (T104 went from 0 back to ~43KB), and every session
that claims the task re-reads the whole note. So:
  * An existing `<TASK-ID>-HISTORY.md` is no longer a refusal: the current note is
    appended as the next round (`<!-- note:begin t-104 round 2 -->`), verified the
    same byte-for-byte way. Earlier rounds are never touched.
  * `--keep-head N` / `--keep-tail M` build the pointer automatically: the note's
    first paragraphs (up to ~N chars: the task's own spec/contract) and last
    paragraphs (up to ~M chars: the latest cycles, with their dates and RAN/NO-OP
    markers) are kept VERBATIM around a one-line archive pointer. `--pointer-file`
    text, if also given, goes right after the pointer line.
  * Signals other scripts parse from live notes are checked before writing and the
    run refuses if any would change: daily_gate's "Pacific calendar day" contract and
    its latest recorded Pacific date, and select_role's latest RAN/NO-OP marker.

Exit codes: 0 = archived (or dry-run showed what would happen),
            1 = round-trip verification failed — nothing was written.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
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


def extract_note(history_text: str, task_id: str, round_no: int = 1) -> str | None:
    tag = re.escape(task_id) + ("" if round_no == 1 else rf" round {round_no}")
    pattern = re.compile(
        rf"<!-- note:begin {tag} -->\n(?P<body>.*?)<!-- note:end {tag} -->\n",
        re.DOTALL,
    )
    m = pattern.search(history_text)
    return m.group("body") if m else None


def next_round(history_text: str, task_id: str) -> int:
    rounds = [1] if f"<!-- note:begin {task_id} -->" in history_text else []
    rounds += [int(n) for n in re.findall(rf"<!-- note:begin {re.escape(task_id)} round (\d+) -->", history_text)]
    return max(rounds, default=0) + 1


def render_round(task_id: str, round_no: int, note: str, when: str) -> str:
    tag = f"{task_id} round {round_no}"
    return (
        f"\n## Round {round_no} (archived {when})\n"
        f"\n<!-- note:begin {tag} -->\n"
        f"{note if note.endswith(chr(10)) else note + chr(10)}"
        f"<!-- note:end {tag} -->\n"
    )


def _paragraphs(note: str) -> list[str]:
    # Literal (`|`) notes are hard-wrapped, with blank lines between paragraphs;
    # folded (`>`) notes load with a single newline between paragraphs. Split on
    # blank lines whenever there are any, so a hard-wrapped sentence stays whole.
    text = note.strip("\n")
    sep = r"\n\s*\n" if re.search(r"\n\s*\n", text) else r"\n+"
    return [p for p in re.split(sep, text) if p.strip()]


_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[`*])")


def _clip(para: str, limit: int) -> str:
    """First sentences of an oversized paragraph, up to ~limit chars (at least one)."""
    out, used = [], 0
    for sentence in _SENTENCE_RE.split(para):
        if out and used + len(sentence) > limit:
            break
        out.append(sentence)
        used += len(sentence) + 1
    clipped = " ".join(out)
    return clipped if len(clipped) >= len(para) else clipped + " [...]"


def _sentences_with(paras: list[str], needles: list[str]) -> list[str]:
    found = []
    for para in paras:
        for sentence in _SENTENCE_RE.split(para):
            if any(n in sentence for n in needles) and sentence not in found:
                found.append(sentence)
    return found


def auto_pointer(note: str, history_rel: str, keep_head: int, keep_tail: int, extra: str = "") -> str:
    """Head + archive pointer + signal-carrying sentences + tail; text kept verbatim
    except that one oversized paragraph at either end is clipped at a sentence
    boundary (the full note is in the archive)."""
    from daily_gate import DAILY_GATE_MARKER

    paras = _paragraphs(note)
    head: list[str] = []
    used = 0
    for para in paras:
        if used >= keep_head:
            break
        if used + len(para) > keep_head:
            head.append(_clip(para, max(keep_head - used, 400)))
            used = keep_head
            break
        head.append(para)
        used += len(para)
    head_full = sum(1 for h in head if not h.endswith(" [...]"))
    rest = paras[len(head):]
    tail: list[str] = []
    used = 0
    for para in reversed(rest):
        if tail and used + len(para) > keep_tail:
            break
        tail.insert(0, para)
        used += len(para)
    archived_span = paras[head_full:len(paras) - len(tail)]

    # Keep, verbatim, the sentences other scripts read from live notes when they
    # would otherwise leave with the archived span: the daily-gate contract phrase,
    # the latest Pacific date, the latest RAN/NO-OP marker.
    kept_text = "\n".join(head + tail)
    signals = parsed_signals(note)
    needles = [v for v in (signals["latest_pacific_date"], signals["latest_recurring_marker"]) if v]
    if signals["daily_gated"]:
        needles.append(DAILY_GATE_MARKER)
    needles = [n for n in needles if n not in kept_text]
    pinned = _sentences_with(archived_span, needles) if needles else []

    parts = head[:]
    if archived_span:
        parts.append(
            f"[Earlier history ({sum(map(len, archived_span)):,} chars) archived verbatim to "
            f"{history_rel} -- read it there only when you need a specific past cycle. "
            "Append new cycles below, one short paragraph each.]"
        )
    if extra.strip():
        parts.append(extra.strip())
    if pinned:
        parts.append("[Kept from the archived history because other scripts read it:] " + " ".join(pinned))
    parts += tail
    return "\n\n".join(parts)


def parsed_signals(note: str) -> dict:
    """Signals other scripts read from live notes; archival must not change them."""
    from daily_gate import dates_recorded_in_note, is_daily_gated

    marker = re.compile(r"\b(?:RAN|NO-OP)\s+(\d{4}-\d{2}-\d{2})")
    dates = dates_recorded_in_note(note)
    runs = marker.findall(note)
    return {
        "daily_gated": is_daily_gated(note),
        "latest_pacific_date": max(dates) if dates else None,
        "latest_recurring_marker": max(runs) if runs else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project")
    parser.add_argument("task_id")
    parser.add_argument("--pointer-file", help="path to a text file with the replacement note (or extra pointer text with --keep-*)")
    parser.add_argument("--keep-head", type=int, help="keep the note's first paragraphs, up to ~N chars, verbatim")
    parser.add_argument("--keep-tail", type=int, help="keep the note's last paragraphs, up to ~N chars, verbatim")
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
    history_rel = str(history_path.relative_to(ROOT))
    existing = history_path.read_text(encoding="utf-8") if history_path.exists() else None
    if existing is None:
        round_no = 1
        archive_text = render_archive(args.project, args.task_id, title, note)
    else:
        # A pre-existing archive without markers (T104's hand archive) is round 1.
        round_no = max(next_round(existing, args.task_id), 2)
        when = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        archive_text = existing.rstrip("\n") + "\n" + render_round(args.task_id, round_no, note, when)

    extra = Path(args.pointer_file).read_text(encoding="utf-8") if args.pointer_file else ""
    if args.keep_head is not None or args.keep_tail is not None:
        pointer = auto_pointer(note, history_rel, args.keep_head or 0, args.keep_tail or 0, extra)
    elif extra:
        pointer = extra.rstrip("\n")
    else:
        sys.exit("give --pointer-file, or --keep-head/--keep-tail to build the pointer automatically")

    before, after = parsed_signals(note), parsed_signals(pointer)
    if before != after:
        sys.exit(
            f"{args.project}/{args.task_id}: refusing -- the new live note would change signals other "
            f"scripts parse from it: before={before} after={after}. Keep more head/tail."
        )

    if args.dry_run:
        recovered = extract_note(archive_text, args.task_id, round_no)
    else:
        history_path.write_text(archive_text, encoding="utf-8")
        recovered = extract_note(history_path.read_text(encoding="utf-8"), args.task_id, round_no)

    want = note if note.endswith("\n") else note + "\n"
    if recovered != want:
        sys.exit(1)  # round-trip failed; history_path (if written) is left for inspection, roadmap untouched
    if existing is not None and not archive_text.startswith(existing.rstrip("\n")):
        sys.exit(1)  # earlier rounds must be untouched

    if args.dry_run:
        print(f"[dry-run] would archive {len(note):,} bytes to {history_path} (round {round_no})")
        print(f"[dry-run] would replace note with ({len(pointer):,} bytes); signals kept: {after}")
        return

    # Folded style re-wraps lines, which can split a "<date> ... Pacific" pair that
    # daily_gate reads line by line; fall back to literal style when that happens.
    for block in (">-", "|-"):
        new_roadmap_text = set_task_field_text(
            roadmap_text, args.task_id, "note", pointer, force=True, force_block=block
        )
        reparsed = yaml.safe_load(new_roadmap_text)
        assert reparsed is not None, f"{args.project}: rewritten roadmap did not parse"
        assert len(reparsed.get("tasks") or []) == len(data.get("tasks") or []), (
            f"{args.project}: task count changed during rewrite"
        )
        new_task = next(t for t in reparsed["tasks"] if isinstance(t, dict) and t.get("id") == args.task_id)
        if parsed_signals(str(new_task.get("note") or "")) == before:
            break
    else:
        if existing is None:
            history_path.unlink()
        else:
            history_path.write_text(existing, encoding="utf-8")
        sys.exit(f"{args.project}/{args.task_id}: signals changed after YAML round-trip; nothing written")
    roadmap_path.write_text(new_roadmap_text, encoding="utf-8")
    print(
        f"archived {args.project}/{args.task_id}: {len(note):,} -> {history_path.name} (round {round_no}); "
        f"live note now {len(pointer):,} bytes"
    )


if __name__ == "__main__":
    main()
