#!/usr/bin/env python3
"""
build_digest.py — daily digest for AI_Networker across all projects + pitches.

Reads every projects/*/roadmap.yaml (skipping _template), scans pitches/ for items
awaiting Silas, plus recent git history. Prints a JSON digest for the emailer.

Usage: python scripts/build_digest.py [--since "24 hours ago"]
"""
import subprocess, sys, json, argparse, datetime, glob, os, re

try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()

def progress(milestones):
    total = sum(m.get("weight", 0) for m in milestones)
    if total == 0:
        return 0
    done = sum(m.get("weight", 0) for m in milestones if m.get("status") == "done")
    partial = sum(m.get("weight", 0) * 0.5 for m in milestones if m.get("status") == "in-progress")
    return round((done + partial) / total * 100)

def scan_pitches():
    out = []
    for path in sorted(glob.glob("pitches/*.md")):
        if path.endswith("README.md"):
            continue
        text = open(path).read()
        title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), os.path.basename(path))
        m = re.search(r"^status:\s*(.+)$", text, re.MULTILINE)
        status = m.group(1).strip() if m else "unknown"
        if status == "awaiting-silas":
            out.append(title)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="24 hours ago")
    args = ap.parse_args()

    projects = []
    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if os.sep + "_template" + os.sep in path:
            continue
        rm = yaml.safe_load(open(path)) or {}
        name = rm.get("project", os.path.basename(os.path.dirname(path)))
        milestones = rm.get("milestones", [])
        tasks = rm.get("tasks", [])
        projects.append({
            "name": name,
            "kind": rm.get("kind", "software"),
            "progress_pct": progress(milestones),
            "milestones": [{"title": m["title"], "status": m["status"]} for m in milestones],
            "needs_attention": [
                f'{name}/{t["id"]}: {t["title"]} ({t.get("status")})'
                for t in tasks if t.get("status") in ("blocked", "needs-human")
            ],
            "in_flight": [
                f'{name}/{t["id"]}: {t["title"]}'
                for t in tasks if t.get("status") in ("claimed", "review")
            ],
            "waiting_count": sum(1 for t in tasks if t.get("status") == "waiting"),
            "ready_count": sum(1 for t in tasks if t.get("status") == "ready"),
        })

    payload = {
        "date": datetime.date.today().isoformat(),
        "commits_since": (git("log", f"--since={args.since}", "--pretty=format:%h %s (%an)") or "").splitlines(),
        "merges_since": (git("log", f"--since={args.since}", "--merges", "--pretty=format:%h %s") or "").splitlines(),
        "projects": projects,
        "all_needs_attention": [x for p in projects for x in p["needs_attention"]],
        "pitches_awaiting_vote": scan_pitches(),
    }
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
