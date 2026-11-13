#!/usr/bin/env python3
"""Report why the latest Shifting Desks classic rerenders are not yet delivered.

Read-only. Examines the durable Conductor staging queue without creating or
repeating ArtJobs. The latest ledger row at a destination overrides older
requests; never confuse an older image at a live URL with a completed rerender.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "projects" / "shifting-desks" / "art"
QUEUE = ROOT / "projects" / "art-prompts.yaml"
ROUNDS = (13, 14, 15, 17, 19)
PREFIX = "kind_robots public/images/shifting-desks/"


def outstanding(art_dir: Path, queue_path: Path) -> dict:
    latest: dict[str, dict] = {}
    for num in ROUNDS:
        ledger_path = art_dir / f"ROUND-{num}.yaml"
        data = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
        for item in data.get("subjects") or []:
            path = str(item.get("target_path") or "")
            if path.startswith(PREFIX):
                latest[path] = {**item, "round": num}
    queued = (yaml.safe_load(queue_path.read_text(encoding="utf-8")) or {}).get("requests") or []
    queue_by_id: dict[str, list[dict]] = {}
    for item in queued:
        if isinstance(item, dict) and item.get("id"):
            queue_by_id.setdefault(str(item["id"]), []).append(item)
    findings = []
    for target, row in sorted(latest.items(), key=lambda p: (p[1]["round"], p[0])):
        if str(row.get("status") or "").lower() == "delivered":
            continue
        req_id = str(row.get("request_id") or "")
        matches = queue_by_id.get(req_id, [])
        current = matches[-1] if matches else {}
        findings.append({
            "round": row["round"],
            "key": row.get("key"),
            "request_id": req_id,
            "target_path": target,
            "ledger_status": row.get("status"),
            "art_job_id": row.get("art_job_id"),
            "queue_matches": len(matches),
            "queue_status": current.get("status") if current else None,
            "queue_job_id": current.get("last_art_job_id") if current else None,
            "queue_priority": current.get("priority") if current else None,
            "queue_force": current.get("force") if current else None,
            "queue_path_matches": (
                current.get("image_path") == target.replace("kind_robots ", "")
                if current else None
            ),
        })
    return {
        "outstanding": len(findings),
        "queued": sum(bool(x["queue_matches"]) for x in findings),
        "missing_from_queue": sum(not x["queue_matches"] for x in findings),
        "duplicates": [x["request_id"] for x in findings if x["queue_matches"] > 1],
        "status_counts": dict(Counter(str(x["queue_status"]) for x in findings)),
        "requests": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--queue", type=Path, default=QUEUE)
    ap.add_argument("--art-dir", type=Path, default=ART)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    data = outstanding(args.art_dir, args.queue)
    result = json.dumps(data, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result + "\n", encoding="utf-8")
    print(f"Shifting Desks classic queue: {data['outstanding']} latest unmet, "
          f"{data['queued']} queued, {data['missing_from_queue']} missing, "
          f"{len(data['duplicates'])} duplicate IDs; statuses {data['status_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
