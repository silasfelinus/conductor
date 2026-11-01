#!/usr/bin/env python3
"""Completion triage for active projects: what kind of work is left?

Sorts every open task in each active/continuous project into one lane and ranks
projects by how close they are to "only art and Silas remain":

  build   agent writing/code/design work still to do
  art     image generation / delivery (Art pipeline, not an LLM session)
  qa      verification that waits on art or build (status waiting/ready, QA-shaped title)
  review  status review: confirm the PR merged, then close -- usually minutes of work
  human   Silas's decision or acceptance gate
  (umbrella / recurring tasks are ignored -- they never "finish")

Tiers:  A = no build work left (art, QA, review and gates only)
        B = 1-2 build tasks left
        C = everything else

The lane is a title heuristic. A task can pin its lane with `lane: build|art|qa|human`.

    python scripts/project_triage.py              # one line per project, tier order
    python scripts/project_triage.py -v           # plus each open task and its lane
    python scripts/project_triage.py --tier A     # only tier-A projects
    python scripts/project_triage.py --json

Read-only. Use this instead of opening roadmaps when you need the portfolio view.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CLOSED = {"done", "cancelled", "superseded", "dropped", "closed", "wontfix", "skipped", "retired"}
LANES = ("build", "art", "qa", "review", "human")

HUMAN_RE = re.compile(
    r"final human|human gate|silas|approv|acceptance and public|public release|verdict|"
    r"confirm scope|creative direction review|scope feedback|course correction|authori[sz]e",
    re.I,
)
ART_RE = re.compile(
    r"\billustrat|\bart\b|artwork|\brender|\bplates?\b|portrait|\bicons?\b|\bimages?\b|"
    r"\blora|sprite|hero artwork|badges?\b",
    re.I,
)
WRITING_RE = re.compile(r"story|writing|dialogue|quest|rewrite|polish|editorial|\bpass\b|ui\b|build", re.I)
QA_RE = re.compile(r"\bqa\b|audit|acceptance|verify|adversarial|playtest|dossier|red-team", re.I)
UMBRELLA_RE = re.compile(r"master completion|^continuing\b", re.I)
# Engineering work that merely mentions images/renders (uploads, ledgers, schema) is build work.
BUILD_RE = re.compile(r"securely|user-submitted|upload|persist|schema|ledger|pipeline|migration", re.I)
GENERATE_RE = re.compile(r"\bgenerat|\bdeliver\b|re-renders?|art round", re.I)


def lane_of(task: dict) -> str | None:
    pinned = task.get("lane")
    if pinned in LANES:
        return pinned
    title = str(task.get("title", ""))
    status = str(task.get("status", ""))
    if task.get("recurring") or UMBRELLA_RE.search(title):
        return None
    if task.get("gate_human") or status == "needs-human" or HUMAN_RE.search(title):
        return "human"
    if status == "review":
        return "review"
    if BUILD_RE.search(title):
        return "build"
    if (ART_RE.search(title) or GENERATE_RE.search(title)) and not WRITING_RE.search(title):
        return "art"
    if QA_RE.search(title) and not WRITING_RE.search(title):
        return "qa"
    return "build"


def active_projects() -> list[dict]:
    data = yaml.safe_load((ROOT / "project-overrides.yaml").read_text()) or {}
    return [o for o in data.get("overrides", []) if o.get("status") in ("active", "continuous")]


def triage() -> list[dict]:
    rows = []
    for o in active_projects():
        path = ROOT / "projects" / o["slug"] / "roadmap.yaml"
        if not path.is_file():
            continue
        tasks = (yaml.safe_load(path.read_text()) or {}).get("tasks") or []
        counts = {lane: 0 for lane in LANES}
        open_tasks = []
        for t in tasks:
            if str(t.get("status")) in CLOSED:
                continue
            lane = lane_of(t)
            if lane is None:
                continue
            counts[lane] += 1
            open_tasks.append({"id": t.get("id"), "status": t.get("status"), "lane": lane, "title": t.get("title", "")})
        done = sum(1 for t in tasks if str(t.get("status")) in CLOSED)
        tier = "A" if counts["build"] == 0 else "B" if counts["build"] <= 2 else "C"
        rows.append(
            {
                "slug": o["slug"],
                "status": o.get("status"),
                "parent": o.get("parent"),
                "tier": tier,
                "done": done,
                "total": len(tasks),
                "lanes": counts,
                "open": open_tasks,
            }
        )
    rows.sort(key=lambda r: (r["status"] != "active", r["tier"], r["lanes"]["build"], -r["done"]))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--tier", choices=["A", "B", "C"])
    ap.add_argument("--include-continuous", action="store_true", help="also list continuous programs")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = triage()
    if not args.include_continuous:
        rows = [r for r in rows if r["status"] == "active"]
    if args.tier:
        rows = [r for r in rows if r["tier"] == args.tier]
    if args.json:
        print(json.dumps(rows, indent=1))
        return 0
    print(f"{'tier':<5}{'project':<36}{'done':>9}  " + " ".join(f"{lane:>6}" for lane in LANES))
    for r in rows:
        lanes = " ".join(f"{r['lanes'][lane]:>6}" for lane in LANES)
        print(f"{r['tier']:<5}{r['slug']:<36}{r['done']:>4}/{r['total']:<4}  {lanes}")
        if args.verbose:
            for t in r["open"]:
                print(f"       {t['id']:<7}{t['lane']:<7}[{t['status']}] {t['title'][:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
