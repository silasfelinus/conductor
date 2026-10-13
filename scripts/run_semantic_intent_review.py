#!/usr/bin/env python3
"""Prepare a zero-API-cost semantic review packet for a Conductor agent."""
import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import yaml

ROOT = Path(__file__).resolve().parents[1]
LEADS = ("kind-pinball", "zuzu-lair", "kr-arcade", "zuzu-showdown")


def due(root, today):
    dates = []
    for p in (root / "projects/conductor").glob("INTENT-AUDIT-????-??-??.md"):
        try:
            dates.append(date.fromisoformat(p.stem[-10:]))
        except ValueError:
            continue
    return not dates or (today - max(dates)).days >= 3


def gather(root):
    ctrl = (root / "CONTROL.md").read_text()
    priority = yaml.safe_load((root / "projects/priority.yaml").read_text())["order"]
    overrides = yaml.safe_load((root / "project-overrides.yaml").read_text())["overrides"]
    registry = {o.get("slug"): o for o in overrides if isinstance(o, dict)}
    selected = list(dict.fromkeys([*LEADS, *priority[:15], *[
        p for p in priority if registry.get(p, {}).get("priority") in ("high", "urgent")
    ]]))[:18]
    parts = ["CONTROL.md:\n" + ctrl.split("## Per-project direction")[0][-5000:],
             "projects/priority.yaml:\n" + json.dumps(priority),
             "project-overrides.yaml:\n" + json.dumps({
                 p: {k: registry.get(p, {}).get(k) for k in ("status", "priority")}
                 for p in selected})]
    for slug in selected:
        start = ctrl.find("### " + slug + " ")
        if start >= 0:
            end = ctrl.find("\n### ", start + 4)
            parts.append("CONTROL.md " + ctrl[start:end if end >= 0 else None][:900])
        p = root / "projects" / slug / "roadmap.yaml"
        if not p.exists():
            parts.append("MISSING projects/" + slug + "/roadmap.yaml")
            continue
        data = yaml.safe_load(p.read_text()) or {}
        opened = [t for t in data.get("tasks", []) if isinstance(t, dict)
                  and t.get("status") != "done"]
        parts.append(str(p.relative_to(root)) + ":\n" + json.dumps({
            "goal": str(data.get("goal", ""))[:1100],
            "human_notes": str(data.get("notes_from_silas", ""))[-1000:],
            "milestones": data.get("milestones", [])[:12],
            "open_tasks": [{k: t.get(k) for k in ("id", "title", "status")}
                           for t in opened[:14]],
            "open_count": len(opened),
        }, default=str))
    audit = root / "ROADMAP-AUDIT.md"
    if audit.exists():
        s = audit.read_text()
        parts.append("ROADMAP-AUDIT.md:\n" + s[s.find("### Warning"):][:2000])
    log = subprocess.run(["git", "log", "-16", "--pretty=format:%as %h %s"],
                         cwd=root, capture_output=True, text=True, check=False)
    parts.append("Recent commits:\n" + log.stdout)
    return "\n\n".join(parts)[:30000]


def prepare_brief(root, today, force=False, brief_path=None):
    """Prepare evidence for the existing agent lane, never a completed audit."""
    if not force and not due(root, today):
        return {"status": "skipped", "reason": "semantic review is current"}
    packet = gather(root)
    if len(packet) < 3000 or any(lead not in packet for lead in LEADS):
        raise ValueError("Insufficient semantic review context")
    brief_path = brief_path or (root / "semantic-intent-brief.md")
    next_report = root / "projects/conductor" / (
        "INTENT-AUDIT-" + today.isoformat() + ".md")
    brief_path.write_text(
        "# Semantic intent audit: agent evidence packet — " + today.isoformat() + "\n\n"
        "**NOT A COMPLETED AUDIT.** Prepared deterministically by GitHub Actions; "
        "the assigned roadmap-intent-auditor must inspect original evidence and author judgment. "
        "This packet does not advance the 3-day deadline.\n\n"
        "Read `projects/conductor/OVERSIGHT-AGENT.md`, then cross-check "
        "`CONTROL.md`, `project-overrides.yaml`, `projects/priority.yaml`, "
        "lead project roadmaps, relevant TALKBACK and actual PR/commit evidence. "
        "Examine all four lead projects and at least three others. "
        "Do not equate roadmap `done` with shipped behavior.\n\n"
        "If and only if a substantive review is completed, write "
        "`" + str(next_report.relative_to(root)) + "` with "
        "`## Verified`, `## Corrected`, `## Still questionable`, "
        "and `## Next review`. Open a PR, verify CI, merge safe review work. "
        "An agent that cannot complete the review must leave it due.\n\n"
        "## Bounded source context (not independently verified)\n\n"
        + packet + "\n",
        encoding="utf-8",
    )
    return {"status": "awaiting-agent",
            "brief": str(brief_path.relative_to(root)),
            "context_chars": len(packet),
            "date": today.isoformat()}



def main():
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true")
    p.add_argument("--check", action="store_true")
    p.add_argument("--state", default="semantic-intent-attempt.json")
    p.add_argument("--brief", default="semantic-intent-brief.md")
    args = p.parse_args()
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    try:
        if args.check:
            context = gather(ROOT)
            if len(context) < 3000 or any(s not in context for s in LEADS):
                raise ValueError("Insufficient semantic review context")
            result = {"status": "input-verified", "context_chars": len(context)}
        else:
            result = prepare_brief(ROOT, today, args.force, ROOT / args.brief)
    except Exception as error:
        result = {"status": "failed", "error_type": type(error).__name__,
                  "date": today.isoformat()}
        Path(args.state).write_text(json.dumps(result) + "\n")
        print("::error::Semantic review failed: " + result["error_type"], file=sys.stderr)
        return 1
    Path(args.state).write_text(json.dumps(result) + "\n")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
