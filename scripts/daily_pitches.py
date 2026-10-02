#!/usr/bin/env python3
"""daily_pitches.py -- the daily project-pitch docket: five new project ideas per day.

Silas, 2026-10-02: Kind Robots has a lot of features locked behind LLM API access, while
image generation and authoring tokens are plentiful. Every day's digest therefore carries
FIVE new project pitches, biased toward things anyone can use with zero tokens at runtime
(games, toys, pre-written content, pre-generated art).

Sessions own the docket, like the Dream docket: a session authors pitches/daily/<date>.yaml
(Pacific date), the digest shows it, and Silas decides each pitch. Approved pitches are
scaffolded with scripts/intake.py (they become projects); rejected and deferred pitches never
come back (the dedupe below reads every decision).

Usage:
    python scripts/daily_pitches.py --check [--date YYYY-MM-DD]   # today's docket exists and is valid
    python scripts/daily_pitches.py --payload [--date YYYY-MM-DD] # JSON for the digest
    python scripts/daily_pitches.py --pending                     # undecided pitches, newest first
    python scripts/daily_pitches.py --decide SLUG approved|rejected|deferred [--note "..."]

Exit codes: 0 ok, 1 missing/invalid docket (author one), 2 unresolved (bad arguments).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = ROOT / "pitches" / "daily"
DECISIONS_PATH = DAILY_DIR / "decisions.yaml"

PITCHES_PER_DAY = 5
MIN_ZERO_LLM = 3  # at least this many of the five must need no LLM at runtime
VALID_DECISIONS = ("approved", "rejected", "deferred")
LLM_AT_RUNTIME = ("none", "optional", "required")
EFFORTS = ("small", "medium", "large")
REQUIRED = ("slug", "title", "hook", "llm_at_runtime", "effort", "art_plan", "first_slice")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MIN_HOOK_WORDS = 15


def pacific_today() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d")


def load_decisions() -> dict[str, dict[str, Any]]:
    if not DECISIONS_PATH.exists():
        return {}
    data = yaml.safe_load(DECISIONS_PATH.read_text(encoding="utf-8")) or {}
    return data.get("decisions") or {}


def docket_path(date: str) -> Path:
    return DAILY_DIR / f"{date}.yaml"


def load_docket(date: str) -> dict[str, Any] | None:
    path = docket_path(date)
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def all_docket_dates() -> list[str]:
    return sorted(p.stem for p in DAILY_DIR.glob("????-??-??.yaml"))


def existing_slugs() -> set[str]:
    """Slugs that already exist as projects or canonical pitch files."""
    slugs = {p.name for p in (ROOT / "projects").iterdir() if p.is_dir()}
    for path in (ROOT / "pitches").glob("*.md"):
        slugs.add(re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem))
    return slugs


def validate(date: str, docket: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    pitches = docket.get("pitches")
    if not isinstance(pitches, list) or len(pitches) != PITCHES_PER_DAY:
        return [f"{date}: needs exactly {PITCHES_PER_DAY} pitches, found "
                f"{len(pitches) if isinstance(pitches, list) else 'none'}"]
    prior: set[str] = set()
    for other in all_docket_dates():
        if other != date:
            prior |= {p.get("slug", "") for p in (load_docket(other) or {}).get("pitches", []) if isinstance(p, dict)}
    # An approved pitch becomes a project (intake.py); its own docket entry must stay valid.
    approved = {slug for slug, d in load_decisions().items() if d.get("decision") == "approved"}
    taken = existing_slugs() - approved
    seen: set[str] = set()
    zero_llm = 0
    for i, pitch in enumerate(pitches, 1):
        where = f"{date} pitch {i}"
        if not isinstance(pitch, dict):
            errors.append(f"{where}: must be a mapping")
            continue
        for key in REQUIRED:
            if not str(pitch.get(key) or "").strip():
                errors.append(f"{where}: missing '{key}'")
        slug = str(pitch.get("slug") or "")
        where = f"{where} ({slug or '?'})"
        if slug and not SLUG_RE.match(slug):
            errors.append(f"{where}: slug must be lowercase-hyphenated")
        if slug in seen:
            errors.append(f"{where}: duplicate slug inside the day")
        seen.add(slug)
        if slug in prior:
            errors.append(f"{where}: slug already pitched on an earlier day")
        if slug in taken:
            errors.append(f"{where}: slug already exists as a project or pitch")
        if str(pitch.get("llm_at_runtime")) not in LLM_AT_RUNTIME:
            errors.append(f"{where}: llm_at_runtime must be one of {LLM_AT_RUNTIME}")
        if pitch.get("llm_at_runtime") == "none":
            zero_llm += 1
        if str(pitch.get("effort")) not in EFFORTS:
            errors.append(f"{where}: effort must be one of {EFFORTS}")
        if len(str(pitch.get("hook") or "").split()) < MIN_HOOK_WORDS:
            errors.append(f"{where}: hook needs at least {MIN_HOOK_WORDS} words (a complete idea, not a label)")
    if zero_llm < MIN_ZERO_LLM:
        errors.append(f"{date}: at least {MIN_ZERO_LLM} of {PITCHES_PER_DAY} pitches must be llm_at_runtime: none "
                      f"(found {zero_llm})")
    return errors


def with_decisions(pitches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    decisions = load_decisions()
    out = []
    for pitch in pitches:
        record = dict(pitch)
        decision = decisions.get(pitch.get("slug"))
        record["decision"] = (decision or {}).get("decision", "pending")
        out.append(record)
    return out


def payload(date: str) -> dict[str, Any] | None:
    docket = load_docket(date)
    if not docket:
        return None
    return {"date": date, "pitches": with_decisions(docket.get("pitches") or [])}


def cmd_check(date: str) -> int:
    docket = load_docket(date)
    if docket is None:
        print(f"daily_pitches: no docket for {date}; author pitches/daily/{date}.yaml "
              f"({PITCHES_PER_DAY} pitches, >= {MIN_ZERO_LLM} with llm_at_runtime: none)")
        return 1
    errors = validate(date, docket)
    if errors:
        print(f"daily_pitches: {date} docket invalid")
        for error in errors:
            print("  - " + error)
        return 1
    pending = sum(1 for p in with_decisions(docket["pitches"]) if p["decision"] == "pending")
    print(f"daily_pitches: {date} docket ok ({PITCHES_PER_DAY} pitches, {pending} undecided; "
          f"{len(_pending_all())} undecided overall)")
    return 0


def _pending_all() -> list[tuple[str, dict[str, Any]]]:
    rows = []
    for date in reversed(all_docket_dates()):
        for pitch in with_decisions((load_docket(date) or {}).get("pitches") or []):
            if pitch["decision"] == "pending":
                rows.append((date, pitch))
    return rows


def cmd_pending() -> int:
    rows = _pending_all()
    if not rows:
        print("daily_pitches: nothing pending")
        return 0
    for date, pitch in rows:
        print(f"{date}  {pitch['slug']}  [{pitch['effort']}, llm:{pitch['llm_at_runtime']}]  {pitch['title']}")
    return 0


def cmd_decide(slug: str, decision: str, note: str) -> int:
    if decision not in VALID_DECISIONS:
        print(f"decision must be one of {VALID_DECISIONS}", file=sys.stderr)
        return 2
    known = {p.get("slug") for d in all_docket_dates() for p in (load_docket(d) or {}).get("pitches", [])}
    if slug not in known:
        print(f"unknown pitch slug: {slug}", file=sys.stderr)
        return 2
    decisions = load_decisions()
    decisions[slug] = {"decision": decision, "decided": pacific_today(), **({"note": note} if note else {})}
    DECISIONS_PATH.write_text(
        "# Silas's decisions on the daily pitch docket. Hand-editable; same pattern as tzaddik discovery-decisions.\n"
        + yaml.safe_dump({"decisions": decisions}, sort_keys=True, allow_unicode=True),
        encoding="utf-8",
    )
    follow = (f"\nNext: python scripts/intake.py {slug} --kind software --title \"...\" --goal \"...\" "
              f"--repo silasfelinus/kind_robots  (then write the brief and roadmap)") if decision == "approved" else ""
    print(f"recorded {slug}: {decision}{follow}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--date", default=pacific_today())
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--payload", action="store_true")
    group.add_argument("--pending", action="store_true")
    group.add_argument("--decide", nargs=2, metavar=("SLUG", "DECISION"))
    parser.add_argument("--note", default="")
    args = parser.parse_args()
    if args.check:
        return cmd_check(args.date)
    if args.payload:
        print(json.dumps(payload(args.date)))
        return 0
    if args.pending:
        return cmd_pending()
    return cmd_decide(args.decide[0], args.decide[1], args.note)


if __name__ == "__main__":
    sys.exit(main())
