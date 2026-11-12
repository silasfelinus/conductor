#!/usr/bin/env python3
"""Read-only Shifting Desks art acceptance inventory across all round ledgers.

An existing media URL (or a DONE ArtJob) proves neither the *new* forced render
nor an editorial KEEP. Later rounds supersede earlier render verdicts at the
same destination path. This audit never submits art, changes a verdict or makes
a playtest decision.

Usage:
    python scripts/shifting_desks_art_readiness.py
    python scripts/shifting_desks_art_readiness.py --json
    python scripts/shifting_desks_art_readiness.py --markdown
    python scripts/shifting_desks_art_readiness.py --strict
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects" / "shifting-desks" / "art"
PATTERN = re.compile(r"^ROUND-(\d+)\.yaml$")
PUBLIC_PREFIX = "kind_robots public/images/shifting-desks/"


def classify(row: dict) -> str:
    """No implicit approval, even for a delivered image with valid ArtJob IDs."""
    status = str(row.get("status") or "").strip().lower()
    verdict = str(row.get("verdict") or "").strip().lower()
    if status != "delivered":
        return "not_delivered"
    if verdict.startswith("redo"):
        return "redo"
    if not verdict.startswith("keep"):
        return "unreviewed"
    if not row.get("delivery_check"):
        return "missing_provenance"
    return "accepted"


def inventory(art_dir: Path = ART) -> dict:
    """Return effective state per unique target path; highest round wins."""
    targets: dict[str, dict] = {}
    problems: list[str] = []
    rounds: dict[int, int] = {}
    files = sorted(
        (p for p in art_dir.glob("ROUND-*.yaml") if PATTERN.fullmatch(p.name)),
        key=lambda p: int(PATTERN.fullmatch(p.name).group(1)),  # type: ignore[union-attr]
    )
    for path in files:
        number = int(PATTERN.fullmatch(path.name).group(1))  # type: ignore[union-attr]
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            problems.append(f"{path.name}: unreadable YAML ({type(exc).__name__})")
            continue
        subjects = data.get("subjects") if isinstance(data, dict) else None
        if not isinstance(subjects, list):
            problems.append(f"{path.name}: missing subjects list")
            continue
        rounds[number] = len(subjects)
        seen: set[str] = set()
        for index, row in enumerate(subjects):
            if not isinstance(row, dict):
                problems.append(f"{path.name} subjects[{index}]: not a mapping")
                continue
            target = str(row.get("target_path") or "")
            if not target.startswith(PUBLIC_PREFIX) or not target.endswith(".webp"):
                problems.append(f"{path.name} subjects[{index}]: invalid target path")
                continue
            if target in seen:
                problems.append(f"{path.name}: duplicate target {target}")
                continue
            seen.add(target)
            targets[target] = {
                "round": number,
                "key": str(row.get("key") or ""),
                "path": target,
                "request_id": str(row.get("request_id") or ""),
                "state": classify(row),
                "status": str(row.get("status") or ""),
                "job": row.get("art_job_id"),
                "image": row.get("art_image_id"),
            }

    entries = sorted(targets.values(), key=lambda x: (x["round"], x["path"]))
    counts = dict(sorted(Counter(row["state"] for row in entries).items()))
    styles: dict[str, dict[str, int]] = {}
    for row in entries:
        relative = row["path"][len(PUBLIC_PREFIX):]
        style = relative.split("/")[1] if relative.startswith("styles/") else "classic"
        stats = styles.setdefault(style, {"total": 0, "accepted": 0, "not_delivered": 0, "unreviewed": 0, "redo": 0, "missing_provenance": 0})
        stats["total"] += 1
        stats[row["state"]] += 1
    return {
        "rounds": rounds,
        "targets": len(entries),
        "counts": counts,
        "styles": styles,
        "blocked": [row for row in entries if row["state"] != "accepted"],
        "errors": problems,
        "ready": not problems and all(row["state"] == "accepted" for row in entries) and bool(entries),
    }


def markdown(result: dict) -> str:
    lines = [
        "# Shifting Desks art readiness (ledger evidence only)",
        "",
        "This is **not** a visual review and does not certify a deployed asset.",
        "The newest round for each destination wins. A delivered render without a",
        "recorded KEEP is unreviewed, **not** complete. Do not requeue an existing",
        "ArtJob from this report alone; reconcile production jobs and media first.",
        "",
        f"**Targets:** {result['targets']}  |  **Art-ready:** {'yes' if result['ready'] else 'NO'}",
        "",
        "| Style | Accepted | Delivered, awaiting review | Not delivered | Redo | Missing evidence | Total |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, counts in sorted(result["styles"].items()):
        lines.append(
            f"| {name} | {counts['accepted']} | {counts['unreviewed']} | "
            f"{counts['not_delivered']} | {counts['redo']} | "
            f"{counts['missing_provenance']} | {counts['total']} |"
        )
    lines += ["", "## Required work (highest-impact slots first)", ""]
    pending = [x for x in result["blocked"] if x["state"] == "not_delivered"]
    review = [x for x in result["blocked"] if x["state"] != "not_delivered"]
    for title, rows in (("Delivery evidence required", pending), ("Visual decision required", review)):
        lines += [f"### {title} ({len(rows)})", ""]
        for row in rows[:25]:
            lines.append(
                f"- ROUND-{row['round']} `{row['key']}` ({row['state']}): "
                f"`{row['path']}`"
            )
        if len(rows) > 25:
            lines.append(f"- ... and {len(rows) - 25} more; use `--json` for every row")
        lines.append("")
    if result["errors"]:
        lines += ["## Ledger errors", ""] + [f"- {error}" for error in result["errors"]]
    lines += [
        "## Handoff",
        "",
        "1. Reconcile pending rows against DONE ArtJobs and newer actual media. A",
        "   preexisting HTTP 200 is insufficient proof of a forced rerender.",
        "2. Inspect actual images for their prompt's core gag, cast, no-gore tone,",
        "   and style; record KEEP or REDO explicitly. Do not mass-approve.",
        "3. For kept Classic imagery, run `projects/shifting-desks/encounters/link_art.py --write --probe`.",
        "4. Re-run this audit in `--strict` mode, then verify runtime/device/QA",
        "   separately before any Playtest lifecycle change.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="full machine-readable evidence")
    parser.add_argument("--markdown", action="store_true", help="report with open slots")
    parser.add_argument("--strict", action="store_true", help="fail while any art slot is unaccepted")
    parser.add_argument("--art-dir", type=Path, default=ART, help="ledger directory, for tests")
    args = parser.parse_args()
    report = inventory(args.art_dir)
    if args.json:
        print(json.dumps(report, indent=2))
    elif args.markdown:
        print(markdown(report))
    else:
        print(f"Shifting Desks: {report['targets']} destinations; {report['counts']}")
        print(f"By style: {report['styles']}")
        for error in report["errors"]:
            print("ERROR:", error)
    return 1 if report["errors"] or (args.strict and not report["ready"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
