#!/usr/bin/env python3
"""
build_learning_summary.py — generate LEARNING-REPORT.md from LEARNING.yaml.

Usage:
    python scripts/build_learning_summary.py [--dry-run] [--output PATH] [--ledger PATH]

Reads the append-only task-outcome ledger (LEARNING.yaml) and emits:
  1. OVERALL — totals, success rate, average passes on successful tasks
  2. BY PROJECT / BY KIND — success rates where there is enough signal
  3. FAILURE CATEGORIES — how failed passes distribute across the triage taxonomy
  4. KAIZEN TARGETS — systematic weaknesses the Reviewer should aim kaizen tasks at
     (success rate < 60% with 3+ records, or a failure category recurring 3+ times)
  5. RECENT LESSONS — the last 10 one-line lessons

Output: LEARNING-REPORT.md at repo root (or --output path). Auto-generated and
read-only, same rules as STATUS.md / KAIZEN.md — never hand-edit.
"""

import argparse
import pathlib
import sys
from collections import Counter
from datetime import datetime, timezone

import yaml


LEDGER_FILE = pathlib.Path("LEARNING.yaml")

SUCCESS_OUTCOMES = {"done"}
FAILURE_OUTCOMES = {"blocked", "cancelled"}
FAILURE_CATEGORIES = ("transient", "actionable", "quality", "scope")

# Thresholds for calling something a systematic weakness (AGENTS.md "Learning ledger")
TARGET_MIN_RECORDS = 3
TARGET_MAX_SUCCESS_RATE = 0.60
TARGET_MIN_CATEGORY_COUNT = 3

RECENT_LESSONS = 10


# ---------------------------------------------------------------------------
# Ledger loading
# ---------------------------------------------------------------------------

def load_records(ledger_path: pathlib.Path) -> list[dict]:
    if not ledger_path.exists():
        return []
    try:
        raw = yaml.safe_load(ledger_path.read_text()) or {}
    except yaml.YAMLError:
        return []
    records = raw.get("records") if isinstance(raw, dict) else None
    if not isinstance(records, list):
        return []
    return [r for r in records if isinstance(r, dict)]


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def success_rate(records: list[dict]) -> float | None:
    """Fraction of closed records that ended `done`. None when no closed records."""
    closed = [r for r in records if r.get("outcome") in SUCCESS_OUTCOMES | FAILURE_OUTCOMES]
    if not closed:
        return None
    done = sum(1 for r in closed if r.get("outcome") in SUCCESS_OUTCOMES)
    return done / len(closed)


def average_passes(records: list[dict]) -> float | None:
    """Average final pass count on successful tasks (rework indicator)."""
    passes = [
        r.get("passes")
        for r in records
        if r.get("outcome") in SUCCESS_OUTCOMES and isinstance(r.get("passes"), (int, float))
    ]
    if not passes:
        return None
    return sum(passes) / len(passes)


def group_by(records: list[dict], key: str) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for r in records:
        val = r.get(key)
        if not isinstance(val, str) or not val:
            continue
        groups.setdefault(val, []).append(r)
    return groups


def failure_category_counts(records: list[dict]) -> Counter:
    """Count records carrying a real failure category (i.e. something went wrong)."""
    return Counter(
        r["failure_category"]
        for r in records
        if r.get("failure_category") in FAILURE_CATEGORIES
    )


def kaizen_targets(records: list[dict]) -> list[str]:
    """Systematic weaknesses worth aiming kaizen tasks at."""
    targets: list[str] = []

    for label, key in (("project", "project"), ("kind", "kind")):
        for name, group in sorted(group_by(records, key).items()):
            if len(group) < TARGET_MIN_RECORDS:
                continue
            rate = success_rate(group)
            if rate is not None and rate < TARGET_MAX_SUCCESS_RATE:
                targets.append(
                    f"{label} `{name}` — {rate:.0%} success over {len(group)} closed tasks; "
                    f"aim the next kaizen task here"
                )

    for category, count in failure_category_counts(records).most_common():
        if count >= TARGET_MIN_CATEGORY_COUNT:
            targets.append(
                f"failure category `{category}` — {count} occurrences; "
                f"look for the shared cause across its records"
            )

    return targets


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fmt_rate(rate: float | None) -> str:
    return f"{rate:.0%}" if rate is not None else "n/a"


def build_report(records: list[dict]) -> str:
    lines: list[str] = []
    ts = now_iso()

    lines.append("# LEARNING-REPORT.md — task-outcome summary")
    lines.append("")
    lines.append(f"Generated: {ts}")
    lines.append("")
    lines.append(
        "Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults "
        "this before creating kaizen tasks — systematic weaknesses beat generic "
        "improvements (AGENTS.md § \"Learning ledger\")."
    )
    lines.append("")

    if not records:
        lines.append("_No records yet. The ledger fills as tasks close._")
        lines.append("")
        lines.append("---")
        lines.append(f"_Auto-generated by `scripts/build_learning_summary.py` at {ts}_")
        lines.append("")
        return "\n".join(lines)

    # ---------------------------------------------------------------- overall
    lines.append("## Overall")
    lines.append("")
    rate = success_rate(records)
    avg = average_passes(records)
    outcome_counts = Counter(r.get("outcome") for r in records)
    lines.append(f"- Closed tasks recorded: **{len(records)}**")
    lines.append(
        "- Outcomes: "
        + ", ".join(f"{k}: {v}" for k, v in sorted(outcome_counts.items()) if k)
    )
    lines.append(f"- Success rate: **{fmt_rate(rate)}**")
    if avg is not None:
        lines.append(f"- Average passes on successful tasks: **{avg:.1f}**")
    lines.append("")

    # ---------------------------------------------------- by project / by kind
    for title, key in (("By project", "project"), ("By kind", "kind")):
        groups = group_by(records, key)
        if not groups:
            continue
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| " + key.title() + " | Closed | Success rate |")
        lines.append("|---|---|---|")
        for name, group in sorted(groups.items()):
            lines.append(f"| {name} | {len(group)} | {fmt_rate(success_rate(group))} |")
        lines.append("")

    # ------------------------------------------------------ failure categories
    cat_counts = failure_category_counts(records)
    lines.append("## Failure categories")
    lines.append("")
    if not cat_counts:
        lines.append("_No failures recorded yet._")
    else:
        lines.append("| Category | Count |")
        lines.append("|---|---|")
        for category, count in cat_counts.most_common():
            lines.append(f"| {category} | {count} |")
    lines.append("")

    # ----------------------------------------------------------- kaizen targets
    targets = kaizen_targets(records)
    lines.append("## Kaizen targets")
    lines.append("")
    if not targets:
        lines.append("_No systematic weaknesses above thresholds. Kaizen freely._")
    else:
        for t in targets:
            lines.append(f"- {t}")
    lines.append("")

    # ----------------------------------------------------------- recent lessons
    lessons = [
        (r.get("date", "?"), r.get("project", "?"), r.get("task", "?"), r["lesson"])
        for r in records
        if isinstance(r.get("lesson"), str) and r["lesson"].strip()
    ]
    lines.append("## Recent lessons")
    lines.append("")
    if not lessons:
        lines.append("_No lessons recorded yet._")
    else:
        for date, project, task, lesson in lessons[-RECENT_LESSONS:][::-1]:
            lines.append(f"- {date} `{project}/{task}` — {lesson}")
    lines.append("")

    lines.append("---")
    lines.append(f"_Auto-generated by `scripts/build_learning_summary.py` at {ts}_")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build LEARNING-REPORT.md")
    parser.add_argument("--dry-run", action="store_true", help="Print report; do not write file")
    parser.add_argument("--output", default="LEARNING-REPORT.md", help="Output file path (default: LEARNING-REPORT.md)")
    parser.add_argument("--ledger", default=str(LEDGER_FILE), help="Ledger file path (default: LEARNING.yaml)")
    args = parser.parse_args()

    ledger_path = pathlib.Path(args.ledger)
    records = load_records(ledger_path)

    if not ledger_path.exists():
        print(f"WARNING: ledger not found at {ledger_path}", file=sys.stderr)

    report = build_report(records)

    if args.dry_run:
        print(report)
    else:
        out = pathlib.Path(args.output)
        out.write_text(report)
        print(f"Written: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
