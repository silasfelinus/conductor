#!/usr/bin/env python3
"""tzaddik_review.py -- Silas's daily review surface for the Tzaddik discovery docket (t-015).

build_tzaddik_discovery.py (t-014) writes each day's 10-living + 10-deceased
docket to projects/tzaddik-gallery/discovery/<date>.md. DESIGN-BRIEF.md's "Daily
discovery roster" section calls this roster "explicitly human-vetted": Silas may
approve, reject, defer, or investigate any suggestion, and a rejected suggestion
should not immediately boomerang back into a future docket.

This script is that review surface, in the same spirit as this repo's other
daily-creative attention/digest patterns (Daily Dream's proposal/build state is
surfaced the same conductor-native way: a script Silas or a session runs, not a
separate live web app). Decisions are recorded in
projects/tzaddik-gallery/discovery-decisions.yaml -- a small, human-editable
ledger Silas can also hand-edit directly, exactly like roadmap.yaml task fields.

Usage:
    python scripts/tzaddik_review.py --check
    python scripts/tzaddik_review.py --pending
    python scripts/tzaddik_review.py --show "Full Name"
    python scripts/tzaddik_review.py --decide "Full Name" approved --note "..."
    python scripts/tzaddik_review.py --decide "Full Name" rejected
    python scripts/tzaddik_review.py --decide "Full Name" deferred
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DECISIONS_PATH = ROOT / "projects" / "tzaddik-gallery" / "discovery-decisions.yaml"

VALID_DECISIONS = ("approved", "rejected", "deferred")

_BTD_SPEC = importlib.util.spec_from_file_location(
    "build_tzaddik_discovery", ROOT / "scripts" / "build_tzaddik_discovery.py"
)
btd = importlib.util.module_from_spec(_BTD_SPEC)
sys.modules[_BTD_SPEC.name] = btd
_BTD_SPEC.loader.exec_module(btd)


def _pacific_today() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d")


def _norm(name: str) -> str:
    return " ".join(name.strip().split()).casefold()


def load_decisions() -> dict[str, dict[str, Any]]:
    """Return {normalized_name: decision_record} from the ledger, if any."""
    if not DECISIONS_PATH.exists():
        return {}
    data = yaml.safe_load(DECISIONS_PATH.read_text(encoding="utf-8")) or {}
    records = data.get("decisions") or []
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if isinstance(record, dict) and record.get("name"):
            result[_norm(str(record["name"]))] = record
    return result


def save_decisions(records: list[dict[str, Any]]) -> None:
    DECISIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Silas's decisions on Daily Tzaddik discovery suggestions (tzaddik-gallery/t-015).\n"
        "# Edit by hand, or via: python scripts/tzaddik_review.py --decide \"Name\" "
        "approved|rejected|deferred [--note TEXT]\n"
        "# A name here is excluded from ever reappearing in a future docket by\n"
        "# build_tzaddik_discovery.py's excluded_names() dedup pool, same as any other\n"
        "# previously-suggested name -- recording a decision does not change that; it\n"
        "# only tells the next human/session what already happened and why.\n"
    )
    payload = {"decisions": records}
    DECISIONS_PATH.write_text(header + yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def all_entries() -> list[dict[str, Any]]:
    """Every suggestion ever docketed, each tagged with its docket date."""
    entries: list[dict[str, Any]] = []
    for docket in btd.all_dockets():
        for entry in docket["entries"]:
            enriched = dict(entry)
            enriched["date"] = docket["date"]
            entries.append(enriched)
    return entries


def entries_by_name() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in all_entries():
        result.setdefault(_norm(entry["name"]), entry)
    return result


def pending_entries() -> list[dict[str, Any]]:
    """Suggestions with no recorded decision yet, oldest docket first."""
    decided = load_decisions()
    return [e for e in all_entries() if _norm(e["name"]) not in decided]


def decide(name: str, decision: str, note: str | None, decided_by: str = "silas") -> int:
    if decision not in VALID_DECISIONS:
        print(f"error: decision must be one of {VALID_DECISIONS}, got {decision!r}", file=sys.stderr)
        return 2

    known = entries_by_name()
    key = _norm(name)
    if key not in known:
        print(f"error: {name!r} does not appear in any discovery docket", file=sys.stderr)
        return 1
    entry = known[key]

    decisions = load_decisions()
    record = {
        "name": entry["name"],
        "docket_date": entry.get("date"),
        "decision": decision,
        "decided_by": decided_by,
        "decided_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if note:
        record["note"] = note
    decisions[key] = record

    save_decisions(list(decisions.values()))
    print(f"Recorded: {entry['name']} -> {decision}")
    return 0


def show(name: str) -> int:
    known = entries_by_name()
    key = _norm(name)
    if key not in known:
        print(f"error: {name!r} does not appear in any discovery docket", file=sys.stderr)
        return 1
    entry = known[key]
    decisions = load_decisions()
    record = decisions.get(key)

    print(f"{entry['name']} -- {entry.get('region', '?')} -- {entry.get('domain', '?')}")
    print(f"Status: {entry.get('status', '?')}   Tags: {', '.join(entry.get('tags') or []) or '(none recorded)'}")
    print(f"Docket date: {entry.get('date', '?')}")
    if record:
        note = f" -- {record['note']}" if record.get("note") else ""
        print(f"Decision: {record['decision']} (by {record.get('decided_by', '?')} at {record.get('decided_at', '?')}){note}")
    else:
        print("Decision: PENDING")
    return 0


def pending(as_report: bool = False) -> int:
    items = pending_entries()
    if not items:
        print("No pending Daily Tzaddik suggestions -- every docketed name has a decision.")
        return 0
    by_date: dict[str, list[dict[str, Any]]] = {}
    for entry in items:
        by_date.setdefault(entry.get("date") or "?", []).append(entry)
    for date in sorted(by_date):
        print(f"## {date}")
        for entry in by_date[date]:
            print(f"  [{entry.get('status', '?')}] {entry['name']} -- {entry.get('region', '?')} -- {entry.get('domain', '?')}")
    return 0


def check() -> int:
    entries = all_entries()
    if not entries:
        print("No discovery dockets found yet -- nothing to review.")
        return 0
    decisions = load_decisions()
    counts = {"approved": 0, "rejected": 0, "deferred": 0}
    pending_count = 0
    for entry in entries:
        record = decisions.get(_norm(entry["name"]))
        if record and record.get("decision") in counts:
            counts[record["decision"]] += 1
        else:
            pending_count += 1
    print(f"{len(entries)} suggestion(s) docketed across {len(btd.all_dockets())} discovery docket(s).")
    print(
        f"Approved: {counts['approved']}   Rejected: {counts['rejected']}   "
        f"Deferred: {counts['deferred']}   Pending: {pending_count}"
    )
    if pending_count:
        print()
        pending()
    return 1 if pending_count else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Report review-queue counts (for the session digest)")
    group.add_argument("--pending", action="store_true", help="List every undecided suggestion")
    group.add_argument("--show", metavar="NAME", help="Print the full sourced profile for one suggestion")
    group.add_argument("--decide", metavar="NAME", help="Record a decision for one suggestion")
    parser.add_argument("decision", nargs="?", choices=VALID_DECISIONS, help="Required with --decide")
    parser.add_argument("--note", help="Optional note to attach to a --decide")
    parser.add_argument("--decided-by", default="silas", help="Who made the decision (default: silas)")
    args = parser.parse_args(argv)

    if args.check:
        return check()
    if args.pending:
        return pending()
    if args.show:
        return show(args.show)
    if not args.decision:
        print("error: --decide requires a decision (approved|rejected|deferred)", file=sys.stderr)
        return 2
    return decide(args.decide, args.decision, args.note, args.decided_by)


if __name__ == "__main__":
    raise SystemExit(main())
