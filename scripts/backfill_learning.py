#!/usr/bin/env python3
"""backfill_learning.py — seed LEARNING.yaml from recently-closed roadmap tasks
and TALKBACK, de-duped against the existing ledger (conductor/t-032).

The learning ledger only auto-fills when a close goes through a task-event with a
`learning:` payload, so most historically-closed tasks never got a record. This
walks `projects/*/roadmap.yaml` for tasks at `done`/`blocked`, enriches each with
any TALKBACK narrative, and appends a best-effort record — reusing the exact
dedup + append-only writer the live path uses, so it is safe to re-run.

Reuse (no reinvention):
  - process_task_events.prepare_learning  — the (project, task, outcome) dedup +
    field validation gate. Returns None for an already-recorded tuple.
  - process_task_events.write_learning_record — append-only writer that never
    rewrites existing bytes and emits the fixed field order.

Every backfilled lesson is prefixed with ``backfilled:`` per the task note, so the
inferred records are greppable and visibly distinct from live closes.

Usage:
    python scripts/backfill_learning.py --dry-run          # preview + counts, write nothing
    python scripts/backfill_learning.py                    # append (default: last 7 days + curated)
    python scripts/backfill_learning.py --since 2026-07-01  # widen the window
    python scripts/backfill_learning.py --since all         # exhaustive sweep of every unrecorded close
    python scripts/backfill_learning.py --source roadmap    # skip TALKBACK enrichment
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import process_task_events as pte  # noqa: E402  (reuse prepare_learning / write_learning_record / ROOT)

BACKFILL_PREFIX = "backfilled: "
DEFAULT_LOOKBACK_DAYS = 7

VALID_KINDS = {"software", "content", "proposal"}
VALID_STAKES = {"reversible", "outward-facing", "irreversible"}
VALID_FAILURE = {"transient", "actionable", "quality", "scope"}

# TALKBACK newer-format header: "## DATE | role → role | project/task | status ..."
TALKBACK_HEADER_RE = re.compile(
    r"^##\s+(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.*)$"
)
SUBJECT_TASK_RE = re.compile(r"^([a-z0-9][a-z0-9-]*)/([A-Za-z0-9][A-Za-z0-9._-]*)$")

# Curated, hand-authored lessons for genuinely high-signal closes the auto-appender
# missed. Keyed by (project, task, outcome); these bypass the --since window.
# failure_category is inferred from the Reviewer's stated reason where unambiguous.
# (The HTTP-413 push lesson is deliberately absent — it already lives in the ledger
# under conductor/t-041.)
CURATED: dict[tuple[str, str, str], dict[str, object]] = {
    ("conductor", "t-014", "done"): {
        "failure_category": "actionable",
        "lesson": (
            "A safety-net test suite that runs in only one CI job gives false green: "
            "the authz regression passed on main yet never ran in Worker PR CI, so a "
            "breaking change could merge unseen — run merge-gating suites in every job "
            "that gates the merge, not just the post-merge job."
        ),
    },
}


@dataclass
class Candidate:
    project: str
    task: str
    outcome: str  # "done" | "blocked"
    kind: str
    stakes: str
    passes: int
    date: str  # YYYY-MM-DD
    lesson: str
    failure_category: str | None
    source: str  # "curated" | "talkback" | "roadmap"


# --------------------------------------------------------------------------- #
# Small text helpers
# --------------------------------------------------------------------------- #

# Abbreviations whose trailing period must not be treated as a sentence end.
_ABBREV = ("e.g.", "i.e.", "etc.", "vs.", "cf.", "al.", "no.", "fig.", "approx.")


def first_sentence(text: str) -> str:
    """First sentence of a note, whitespace-collapsed, length-capped.

    Treats a terminator as a sentence end only when it is end-of-string or
    followed by whitespace and is not the period of a known abbreviation — so
    "run X (e.g. Y) then Z." is not cut after "e.g.".
    """
    collapsed = " ".join((text or "").split())
    if not collapsed:
        return ""
    for m in re.finditer(r"[.!?]", collapsed):
        end = m.end()
        if end < len(collapsed) and not collapsed[end].isspace():
            continue  # mid-token period (e.g. "e.g.," or a decimal) — not a break
        preceding = collapsed[:end].lower()
        if any(preceding.endswith(abbr) for abbr in _ABBREV):
            continue
        return collapsed[:end].strip()[:280]
    return collapsed[:280].rstrip()


def apply_backfill_prefix(lesson: str) -> str:
    """Prefix a lesson with the backfill marker exactly once (idempotent)."""
    lesson = (lesson or "").strip()
    if lesson.startswith(BACKFILL_PREFIX.strip()):
        return lesson
    return f"{BACKFILL_PREFIX}{lesson}" if lesson else BACKFILL_PREFIX.strip()


def roadmap_kind(data: dict) -> str:
    kind = data.get("kind")
    return kind if kind in VALID_KINDS else "software"


# --------------------------------------------------------------------------- #
# TALKBACK parsing (pure — operates on text)
# --------------------------------------------------------------------------- #

def talkback_outcome(status_field: str) -> str | None:
    """Map a TALKBACK header's status field to a terminal outcome, else None."""
    head = (status_field or "").strip().lower()
    if head.startswith(("closed", "merged", "done")):
        return "done"
    if head.startswith("blocked"):
        return "blocked"
    return None


def split_talkback_entries(text: str) -> list[dict]:
    """Split TALKBACK markdown into task-scoped closed/blocked entries.

    Returns dicts {date, project, task, outcome, body} only for entries whose
    header names a `project/task` subject and a terminal status. System-level
    entries (subject == "system" or free text) and non-terminal statuses
    (pattern/critique/response/security-flag/update) are skipped.
    """
    lines = text.splitlines()
    header_idx = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    entries: list[dict] = []
    for pos, start in enumerate(header_idx):
        end = header_idx[pos + 1] if pos + 1 < len(header_idx) else len(lines)
        header = lines[start]
        m = TALKBACK_HEADER_RE.match(header)
        if not m:
            continue
        date, _who, subject, status = m.groups()
        subj = SUBJECT_TASK_RE.match(subject.strip())
        if not subj:
            continue
        outcome = talkback_outcome(status)
        if outcome is None:
            continue
        entries.append(
            {
                "date": date,
                "project": subj.group(1),
                "task": subj.group(2),
                "outcome": outcome,
                "body": "\n".join(lines[start + 1 : end]),
            }
        )
    return entries


def extract_field(body: str, name: str) -> str | None:
    """Return the text of a `**Name:**` block up to the next bold marker/blank run."""
    pat = re.compile(rf"\*\*{re.escape(name)}:\*\*\s*(.+?)(?=\n\s*\n|\n\*\*|\Z)", re.DOTALL)
    m = pat.search(body or "")
    if not m:
        return None
    return " ".join(m.group(1).split()).strip() or None


def talkback_index(text: str) -> dict[tuple[str, str, str], dict]:
    """Index the latest TALKBACK entry per (project, task, outcome).

    Value carries a distilled `lesson` (from **What to improve:** → **Decision:**
    → **Subject:**) and the entry `date`. Later entries overwrite earlier ones.
    """
    index: dict[tuple[str, str, str], dict] = {}
    for entry in split_talkback_entries(text):
        key = (entry["project"], entry["task"], entry["outcome"])
        body = entry["body"]
        raw = (
            extract_field(body, "What to improve")
            or extract_field(body, "Decision")
            or extract_field(body, "Subject")
        )
        index[key] = {"date": entry["date"], "lesson": first_sentence(raw) if raw else None}
    return index


# --------------------------------------------------------------------------- #
# Candidate assembly
# --------------------------------------------------------------------------- #

def iter_roadmaps(projects_dir: Path):
    for path in sorted(projects_dir.glob("*/roadmap.yaml")):
        if path.parent.name in ("_template", "images"):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and data.get("project"):
            yield data


def build_candidates(
    projects_dir: Path,
    talkback_text: str,
    since: str,
    sources: str,
) -> list[Candidate]:
    """Enumerate closed roadmap tasks not filtered out by the recency window.

    `since` is an inclusive YYYY-MM-DD cutoff (use "0000-00-00" for all). The
    curated set always survives the window. Field precedence for the lesson:
    curated > TALKBACK improve-text > roadmap note first-sentence.
    """
    tb = talkback_index(talkback_text) if sources in ("all", "talkback") else {}
    use_roadmap = sources in ("all", "roadmap")
    candidates: list[Candidate] = []

    for data in iter_roadmaps(projects_dir):
        project = data["project"]
        kind = roadmap_kind(data)
        for task in data.get("tasks", []) or []:
            if not isinstance(task, dict):
                continue
            outcome = task.get("status")
            if outcome not in ("done", "blocked"):
                continue
            task_id = str(task.get("id") or "").strip()
            if not task_id:
                continue
            key = (project, task_id, outcome)
            curated = CURATED.get(key)
            tb_hit = tb.get(key)

            updated = str(task.get("updated") or "")[:10]
            date = updated or (tb_hit or {}).get("date") or dt.date.today().isoformat()

            # Recency gate — curated always passes; TALKBACK-sourced closes count
            # toward the window via their own date too.
            if not curated and date < since:
                continue
            if not use_roadmap and not (curated or tb_hit):
                continue

            stakes = task.get("stakes")
            stakes = stakes if stakes in VALID_STAKES else "reversible"
            try:
                passes = int(task.get("passes", 0))
            except (TypeError, ValueError):
                passes = 0

            # Precedence: curated hand-authored > roadmap note (authoritative task
            # summary) > TALKBACK narrative (only when a note is absent). Roadmap
            # notes beat TALKBACK bodies, which are conversational and often carry
            # status noise ("merged (PR #NNN)") rather than a reusable lesson.
            note_lesson = first_sentence(str(task.get("note") or ""))
            if curated:
                lesson = str(curated["lesson"])
                failure = curated.get("failure_category")
                source = "curated"
            elif note_lesson:
                lesson = note_lesson
                failure = None
                source = "roadmap"
            elif tb_hit and tb_hit.get("lesson"):
                lesson = tb_hit["lesson"]
                failure = None
                source = "talkback"
            else:
                lesson = ""
                failure = None
                source = "roadmap"

            failure = failure if failure in VALID_FAILURE else None
            if not lesson:
                lesson = f"{project}/{task_id} closed ({outcome}); no note recorded."

            candidates.append(
                Candidate(
                    project=project,
                    task=task_id,
                    outcome=outcome,
                    kind=kind,
                    stakes=stakes,
                    passes=passes,
                    date=date,
                    lesson=apply_backfill_prefix(lesson),
                    failure_category=failure,
                    source=source,
                )
            )
    candidates.sort(key=lambda c: (c.date, c.project, c.task))
    return candidates


def to_event(candidate: Candidate) -> dict:
    """Shape a Candidate into the {"learning": {...}} event prepare_learning wants."""
    return {
        "learning": {
            "date": candidate.date,
            "kind": candidate.kind,
            "stakes": candidate.stakes,
            "passes": candidate.passes,
            "failure_category": candidate.failure_category,
            "lesson": candidate.lesson,
        }
    }


def run_backfill(candidates: list[Candidate], dry_run: bool) -> tuple[int, int]:
    """Append each candidate through the shared dedup+writer. Returns (appended, skipped)."""
    appended = skipped = 0
    for c in candidates:
        record = pte.prepare_learning(to_event(c), c.project, c.task, c.outcome)
        if record is None:  # already recorded (dedup) or nothing to append
            skipped += 1
            continue
        if not dry_run:
            pte.write_learning_record(record)
        appended += 1
    return appended, skipped


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def resolve_since(raw: str | None) -> str:
    if raw and raw.lower() == "all":
        return "0000-00-00"
    if raw:
        return raw
    cutoff = dt.date.today() - dt.timedelta(days=DEFAULT_LOOKBACK_DAYS)
    return cutoff.isoformat()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Backfill LEARNING.yaml (conductor/t-032)")
    parser.add_argument("--dry-run", action="store_true", help="Preview candidates; write nothing")
    parser.add_argument(
        "--since",
        default=None,
        help=f"Inclusive YYYY-MM-DD cutoff, or 'all'. Default: {DEFAULT_LOOKBACK_DAYS} days ago.",
    )
    parser.add_argument(
        "--source",
        choices=("all", "roadmap", "talkback"),
        default="all",
        help="Candidate sources to use (default: all).",
    )
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of candidates processed.")
    args = parser.parse_args(argv)

    since = resolve_since(args.since)
    projects_dir = pte.ROOT / "projects"
    talkback_file = pte.ROOT / "TALKBACK.md"
    talkback_text = talkback_file.read_text(encoding="utf-8") if talkback_file.is_file() else ""

    candidates = build_candidates(projects_dir, talkback_text, since, args.source)
    if args.limit is not None:
        candidates = candidates[: args.limit]

    # Predict dedup outcomes without writing so the summary is accurate in both modes.
    appended, skipped = run_backfill(candidates, dry_run=True)

    by_source: dict[str, int] = {}
    for c in candidates:
        by_source[c.source] = by_source.get(c.source, 0) + 1

    print(f"since={since}  source={args.source}  candidates={len(candidates)}")
    print(f"  by source: " + ", ".join(f"{k}={v}" for k, v in sorted(by_source.items())))
    print(f"  would append: {appended}   skip as duplicate: {skipped}")

    if args.dry_run:
        for c in candidates:
            fc = c.failure_category or "-"
            print(f"    [{c.source:8}] {c.date} {c.project}/{c.task} {c.outcome} fc={fc}")
        print("DRY RUN — nothing written.")
        return 0

    appended, skipped = run_backfill(candidates, dry_run=False)
    print(f"DONE — appended {appended} record(s), skipped {skipped} duplicate(s).")
    print("Next: python scripts/build_learning_summary.py  # regenerate LEARNING-REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
