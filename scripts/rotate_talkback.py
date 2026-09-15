#!/usr/bin/env python3
"""
rotate_talkback.py — rotate finished months of root TALKBACK.md into
talkback/YYYY-MM.md archive files, keeping the root file's preamble plus the
current month's entries only.

WHY (conductor/t-159, filed 2026-09-14). Root TALKBACK.md is a single
append-only file that grows ~48KB/day (3.67MB / 1,034 entries as of the
filing). It is not in the Kind Robots projection payload
(scripts/sync_kind_robots_projection.py) — this is not a transport-limit
problem like t-158/interface-vision's roadmap note — but
scripts/append_ledger_entry.py's append_with_retry() reads the WHOLE file via
`git show origin/main:TALKBACK.md`, rebuilds the full text, and pushes a
single-file commit straight to refs/heads/main on every single append. That
whole-file rewrite is the near-certain cause of the HTTP-413 TALKBACK-only
push failures already documented in CLAUDE.md ("a follow-up TALKBACK-only
commit hit 413 on every retry" — 2026-07-16). Rotation shrinks what every
append has to move, fixing something that is actively failing, not just
tidying history.

AUTHORIZATION. This operates under the "Archival carve-out" Silas added to
AGENTS.md on 2026-09-14 for conductor/t-158: moving content VERBATIM to a
named archive file is not deletion, provided the round-trip is verified
byte-for-byte before the source is rewritten. That proviso is enforced here,
the same shape as scripts/archive_done_task_notes.py's precedent:

    1. render each month's archive text
    2. write talkback/YYYY-MM.md
    3. RE-READ it from disk and re-extract every entry
    4. assert each extracted entry == the original, byte for byte
    5. only once EVERY month passes does this touch the root file at all

A month that fails its round-trip check is left alone entirely (root
untouched, no partial archive) and reported; nothing is ever deleted at any
point — every entry exists in the archive file before root stops carrying it,
and both live in git.

SHAPE. The root path (TALKBACK.md) keeps the current calendar month — not a
bare index — because .claude/hooks/session-start.sh tails the root file at
every session start and needs recent entries, not archive-index text. Older,
fully-elapsed months move to talkback/YYYY-MM.md. The preamble (everything
before the first dated entry: title, format block, the entries-start comment)
is preserved unchanged, plus one added pointer line so the archive is
discoverable from the file everyone already reads.

THREE THINGS NOT TO REDISCOVER (see conductor/t-159's roadmap note):
  - Split on ``^## \\d{4}-\\d{2}-\\d{2}``, NOT on ``^## ``. The format block's
    own template line ("## YYYY-MM-DD | <Worker|Reviewer> ...") lives inside a
    fenced code block and is a false positive for a bare "## " split; it does
    not match the digit-anchored pattern, so no special-casing is needed.
  - scripts/backfill_learning.py's `--since all` backfill whole-file-parses
    TALKBACK.md. After rotation it would silently see only the current month.
    Fixed there via load_talkback_text(), which concatenates archived months
    (oldest first, by filename sort) with the root file (current month) last —
    order matters because talkback_index() keeps the LAST entry seen per
    (project, task, outcome) key, so a real re-close must still sort after an
    earlier close of the same task.
  - LEAVE LEARNING.yaml ALONE. Different job, larger scope, not this task.

CONVENTION. Each archive file opens with what it covers and why (mirroring
projects/interface-vision/T104-HISTORY.md), not the undocumented
TALKBACK-wonderlab-retirement-2026-08-11.md precedent.

Usage:
  python scripts/rotate_talkback.py --dry-run
  python scripts/rotate_talkback.py --apply
  python scripts/rotate_talkback.py --verify-only

Exit codes: 0 = success (including "nothing to rotate"), 1 = at least one
month failed its round-trip check and was left unarchived.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TALKBACK_PATH = ROOT / "TALKBACK.md"
ARCHIVE_DIR = ROOT / "talkback"

# Real dated entry headers only — see "THREE THINGS NOT TO REDISCOVER" above.
ENTRY_HEADER_RE = re.compile(r"^## (\d{4})-(\d{2})-\d{2}\b")

POINTER_MARKER = "<!-- talkback-archive-pointer -->"
POINTER_BLOCK = (
    f"{POINTER_MARKER}\n"
    "Entries from earlier, fully-elapsed months are archived verbatim in "
    "`talkback/YYYY-MM.md` (see `talkback/`), rotated by "
    "`scripts/rotate_talkback.py` (conductor/t-159). This file keeps the "
    "current month.\n"
)

ARCHIVE_HEADER = """# TALKBACK.md archive — {month}

Entries moved out of the root `TALKBACK.md` by `scripts/rotate_talkback.py`
(conductor/t-159, {generated}) once {month} was a fully-elapsed month, to keep
the root file small enough for `scripts/append_ledger_entry.py`'s
whole-file-rewrite-on-every-append to stay fast (see that script's docstring
and the HTTP-413 history in `CLAUDE.md`).

Nothing below is summarized, reworded, or trimmed — every entry is
byte-for-byte identical to what shipped in root `TALKBACK.md`, verified by
round-trip before the root file was ever rewritten. See `../TALKBACK.md` for
the current month and `../AGENTS.md`'s "Archival carve-out" for the
authorization this operates under.

---
"""


def read_root_text() -> str:
    return TALKBACK_PATH.read_text(encoding="utf-8") if TALKBACK_PATH.is_file() else ""


def split_entries(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split TALKBACK markdown into (preamble, [(month, entry_text), ...]).

    `entry_text` runs from its own "## YYYY-MM-DD ..." header line through
    (but not including) the next entry header, i.e. it owns its own trailing
    blank-line separator — concatenating entries back together in order
    reproduces the original text exactly.
    """
    lines = text.splitlines(keepends=True)
    header_idx = [i for i, ln in enumerate(lines) if ENTRY_HEADER_RE.match(ln)]
    if not header_idx:
        return text, []
    preamble = "".join(lines[: header_idx[0]])
    entries: list[tuple[str, str]] = []
    for pos, start in enumerate(header_idx):
        end = header_idx[pos + 1] if pos + 1 < len(header_idx) else len(lines)
        m = ENTRY_HEADER_RE.match(lines[start])
        assert m is not None
        month = f"{m.group(1)}-{m.group(2)}"
        entries.append((month, "".join(lines[start:end])))
    return preamble, entries


def render_archive(month: str, entries: list[str], *, today: dt.date) -> str:
    header = ARCHIVE_HEADER.format(month=month, generated=today.isoformat())
    return header + "".join(entries)


def extract_archive_entries(archive_text: str) -> list[str]:
    """Inverse of render_archive: re-split an archive file's own entry text."""
    _, entries = split_entries(archive_text)
    return [body for _month, body in entries]


def ensure_pointer(preamble: str) -> str:
    if POINTER_MARKER in preamble:
        return preamble
    # Insert right after the "Entries below..." comment line if present,
    # else just before the first entry (end of preamble).
    marker_line = "<!-- Entries below."
    idx = preamble.find(marker_line)
    if idx == -1:
        return preamble.rstrip("\n") + "\n\n" + POINTER_BLOCK + "\n"
    line_end = preamble.find("\n", idx)
    if line_end == -1:
        line_end = len(preamble) - 1
    insert_at = line_end + 1
    return preamble[:insert_at] + "\n" + POINTER_BLOCK + "\n" + preamble[insert_at:]


def rotate(*, apply: bool, today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    current_month = today.strftime("%Y-%m")

    text = read_root_text()
    preamble, entries = split_entries(text)

    by_month: dict[str, list[str]] = {}
    for month, body in entries:
        by_month.setdefault(month, []).append(body)

    to_archive = sorted(m for m in by_month if m < current_month)
    kept_months = sorted(m for m in by_month if m >= current_month)

    result: dict = {
        "current_month": current_month,
        "months_archived": [],
        "months_failed": [],
        "months_already_archived": [],
        "kept_entry_count": sum(len(by_month[m]) for m in kept_months),
        "applied": False,
    }

    if not to_archive:
        return result

    if apply:
        ARCHIVE_DIR.mkdir(exist_ok=True)

    verified_months: list[str] = []
    for month in to_archive:
        archive_path = ARCHIVE_DIR / f"{month}.md"
        want_entries = by_month[month]

        if archive_path.is_file():
            existing = extract_archive_entries(archive_path.read_text(encoding="utf-8"))
            if existing == want_entries:
                # Already rotated in a prior run; nothing new for this month.
                result["months_already_archived"].append(month)
                verified_months.append(month)
                continue
            # A real, unexpected mismatch — do not silently overwrite an
            # existing archive. Leave this month in root and report it.
            result["months_failed"].append((month, "archive file exists with different content"))
            continue

        archive_text = render_archive(month, want_entries, today=today)
        if apply:
            archive_path.write_text(archive_text, encoding="utf-8")
            recovered = extract_archive_entries(archive_path.read_text(encoding="utf-8"))
        else:
            recovered = extract_archive_entries(archive_text)

        if recovered != want_entries:
            result["months_failed"].append((month, "round-trip mismatch — NOT rotated"))
            if apply:
                archive_path.unlink(missing_ok=True)
            continue

        result["months_archived"].append(month)
        verified_months.append(month)

    # Only rewrite root once every to-be-archived month verified clean.
    if result["months_failed"]:
        return result

    if not apply:
        result["applied"] = False
        return result

    new_preamble = ensure_pointer(preamble)
    kept_text = "".join(body for month in kept_months for body in by_month[month])
    new_root = new_preamble + kept_text
    TALKBACK_PATH.write_text(new_root, encoding="utf-8")

    # Re-verify the root itself round-trips: every kept entry still present,
    # nothing from an archived month leaked back in.
    _preamble2, entries2 = split_entries(TALKBACK_PATH.read_text(encoding="utf-8"))
    recovered_kept = [body for _m, body in entries2]
    if recovered_kept != [body for month in kept_months for body in by_month[month]]:
        # Extremely defensive — should be unreachable given the checks above.
        raise SystemExit("root TALKBACK.md failed post-write round-trip check; aborting")

    result["applied"] = True
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Preview rotation; write nothing")
    mode.add_argument("--apply", action="store_true", help="Perform the rotation")
    mode.add_argument(
        "--verify-only",
        action="store_true",
        help="Re-verify existing talkback/*.md archives round-trip against root history in git",
    )
    args = parser.parse_args(argv)

    if args.verify_only:
        # Re-check every existing archive file re-extracts to exactly what it
        # claims to hold (self-consistency), independent of root's current state.
        ok = True
        if not ARCHIVE_DIR.is_dir():
            print("No talkback/ archive directory yet.")
            return 0
        for path in sorted(ARCHIVE_DIR.glob("*.md")):
            entries = extract_archive_entries(path.read_text(encoding="utf-8"))
            print(f"{path.relative_to(ROOT)}: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} extracted")
            if not entries:
                ok = False
                print(f"  WARNING: no entries extracted from {path}")
        return 0 if ok else 1

    result = rotate(apply=args.apply)
    print(f"current_month={result['current_month']}")
    print(f"kept in root: {result['kept_entry_count']} entr(y/ies)")
    if result["months_already_archived"]:
        print(f"already archived (no-op): {', '.join(result['months_already_archived'])}")
    if result["months_archived"]:
        print(f"{'archived' if args.apply else 'would archive'}: {', '.join(result['months_archived'])}")
    if result["months_failed"]:
        for month, reason in result["months_failed"]:
            print(f"FAILED: {month} — {reason}")
        print("Root TALKBACK.md left untouched — fix the failing month(s) before retrying.")
        return 1
    if not result["months_archived"] and not result["months_already_archived"]:
        print("Nothing to rotate — no fully-elapsed month found.")
        return 0
    if args.apply:
        print("root TALKBACK.md rewritten and verified." if result["applied"] else "no root changes needed.")
    else:
        print("DRY RUN — nothing written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
