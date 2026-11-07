#!/usr/bin/env python3
"""Flag roadmap tasks whose note text describes a different task.

Kaizen from weird-humboldt/t-024 (PR #7143): t-023 carried t-024's note. A task is
flagged when its note shares no significant word with its own title but shares at
least MIN_OTHER_HITS with a sibling task's title, or when its note's opening text is
copied verbatim from a sibling's note. Advisory heuristic: exit 1 on findings.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MIN_OTHER_HITS = 3
MIN_OTHER_SHARE = 0.75  # fraction of the sibling title's words found in this note
MIN_NOTE_CHARS = 80
PREFIX_CHARS = 120
STOP = {
    "the", "and", "for", "with", "that", "this", "from", "into", "are", "was", "not", "all",
    "its", "has", "have", "task", "tasks", "add", "new", "one", "each", "per", "any", "when",
    "after", "before", "only", "then", "than", "but", "can", "will", "use", "run",
}


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9-]{3,}", text.lower()) if w not in STOP}


def norm(text: str) -> str:
    return " ".join(text.split())


def find_mismatches(tasks: list) -> list[str]:
    rows = [t for t in tasks if isinstance(t, dict) and t.get("id")]
    out: list[str] = []
    prefixes: dict[str, str] = {}
    for t in rows:
        note = t.get("note")
        if isinstance(note, str) and len(norm(note)) >= MIN_NOTE_CHARS:
            prefixes.setdefault(norm(note)[:PREFIX_CHARS], str(t["id"]))
    for t in rows:
        note = t.get("note")
        if not isinstance(note, str) or len(norm(note)) < MIN_NOTE_CHARS:
            continue
        tid = str(t["id"])
        owner = prefixes.get(norm(note)[:PREFIX_CHARS])
        if owner and owner != tid:
            out.append(f"{tid}: note opens with the same text as {owner}'s note")
            continue
        note_words = words(note)
        if note_words & words(str(t.get("title", ""))):
            continue
        best_id, best = None, 0
        for other in rows:
            if other is t:
                continue
            other_words = words(str(other.get("title", "")))
            hits = len(note_words & other_words)
            if hits >= MIN_OTHER_HITS and hits >= MIN_OTHER_SHARE * len(other_words) and hits > best:
                best_id, best = str(other["id"]), hits
        if best_id:
            out.append(f"{tid}: note shares no word with its title but {best} with {best_id}'s title")
    return out


def main(root: Path = ROOT) -> int:
    bad = 0
    for path in sorted((root / "projects").glob("*/roadmap.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        for line in find_mismatches(data.get("tasks") or []):
            print(f"{path.parent.name}/{line}")
            bad += 1
    if bad:
        print(f"{bad} possible note/title mismatch(es)", file=sys.stderr)
        return 1
    print("No note/title mismatches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
