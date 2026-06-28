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

try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("America/Los_Angeles")
except ImportError:
    # Python < 3.9 fallback — hardcoded PDT; close enough
    _TZ = datetime.timezone(datetime.timedelta(hours=-7))

def _pacific_hour():
    return datetime.datetime.now(_TZ).hour

def _pacific_time_of_day():
    hour = _pacific_hour()
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def _openai_generate(prompt, fallback=""):
    """Call OpenAI chat completions; return the text or fallback if unavailable."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return fallback
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=1.0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[digest] OpenAI call failed: {e}", file=sys.stderr)
        return fallback

def time_greeting():
    tod = _pacific_time_of_day()
    date_str = datetime.date.today().strftime("%A, %B %-d")
    prompt = (
        f"Write a single short greeting for Silas Knight, a creative developer who runs an "
        f"AI coordination system called AI_Networker on the Humboldt coast. "
        f"It's {tod} on {date_str}. "
        f"Be warm, a little funny, and specific — reference the time of day, the coast, robots, "
        f"or his work. One or two sentences max. No quotes around your response."
    )
    fallback = f"Good {tod}, Silas."
    return _openai_generate(prompt, fallback=fallback)

def daily_spark(context=""):
    """Ask OpenAI for a fresh daily spark: character, dream, or wild project idea."""
    date_str = datetime.date.today().strftime("%A, %B %-d, %Y")
    prompt = (
        f"Today is {date_str}. You're writing a fun daily spark for Silas Knight's AI digest. "
        f"He runs an AI coordination system, does creative/AI art, lives on the Humboldt coast, "
        f"and has projects like Kind Robots, Mermaids of Venice, a coloring book, and a poop-scoop CMS.\n"
        f"{('Active context: ' + context + chr(10)) if context else ''}"
        f"Generate ONE of the following (your choice, vary it across categories):\n"
        f"- A quirky fictional character that would fit his world\n"
        f"- A whimsical dream scenario for him to ponder\n"
        f"- A wild creative project idea worth considering\n\n"
        f"Respond in exactly this format (no extra text):\n"
        f"LABEL: [emoji + short label, e.g. '🎭 Today's character' or '🌊 Dream scenario' or '💡 Wild idea']\n"
        f"TEXT: [one or two vivid, specific, imaginative sentences]\n"
    )
    raw = _openai_generate(prompt, fallback="")
    if not raw:
        return {}
    label, text = "", ""
    for line in raw.splitlines():
        if line.startswith("LABEL:"):
            label = line[6:].strip()
        elif line.startswith("TEXT:"):
            text = line[5:].strip()
    if not label or not text:
        return {}
    return {"label": label, "text": text}

_SEP = "|||CDSEP|||"

def _iter_commits(since):
    """Yield (author, subject) for commits in the since window."""
    raw = git("log", f"--since={since}", f"--pretty=format:%an{_SEP}%s")
    for line in raw.splitlines():
        if _SEP not in line:
            continue
        author, subject = line.split(_SEP, 1)
        yield author.strip(), subject.strip()

def significant_activity(since):
    """All meaningful commits — no bot status refreshes, no [skip ci] noise, no git housekeeping merges."""
    out = []
    for author, subject in _iter_commits(since):
        if "[skip ci]" in subject or subject.startswith("chore: refresh STATUS"):
            continue
        if re.match(r"Merge branch '.*' into ", subject):
            continue
        out.append(subject)
    return out

def autonomous_work(since):
    """Commits made by the autonomous agents (Claude Reviewer + Worker claims + merged Worker PRs)."""
    out = []
    for author, subject in _iter_commits(since):
        if "[skip ci]" in subject or subject.startswith("chore: refresh STATUS"):
            continue
        if author == "Claude":
            out.append(f"[Reviewer] {subject}")
        elif author == "conductor-bot" and not subject.startswith("chore:"):
            out.append(f"[Bot] {subject}")
        elif subject.startswith("claim:"):
            # Worker atomically claims tasks under Silas's git identity
            out.append(f"[Worker] {subject}")
        elif re.search(r"Merge pull request #\d+ from .*/worker[-/]", subject):
            # PR merge from a worker/* or worker-* branch — Worker-generated deliverable
            pr_ref = re.sub(r"Merge pull request #(\d+) from \S+/(worker[-/]\S+)", r"PR #\1 (\2)", subject)
            out.append(f"[Worker PR merged] {pr_ref}")
    return out

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

def scan_branches():
    """Return summary strings for remote branches not yet merged to main."""
    raw = git("branch", "-r", "--no-merged", "origin/main")
    out = []
    for line in raw.splitlines():
        ref = line.strip()
        if not ref or "HEAD" in ref or ref == "origin/main":
            continue
        name = ref.removeprefix("origin/")
        age = git("log", "-1", "--pretty=format:%ar", ref)
        author = git("log", "-1", "--pretty=format:%an", ref)
        out.append(f"{name} — last commit {age} by {author}")
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
        "greeting": time_greeting(),
        "daily_spark": daily_spark(
            context=", ".join(p["name"] for p in projects) if projects else ""
        ),
        "commits_since": (git("log", f"--since={args.since}", "--pretty=format:%h %s (%an)") or "").splitlines(),
        "merges_since": (git("log", f"--since={args.since}", "--merges", "--pretty=format:%h %s") or "").splitlines(),
        "activity_since": significant_activity(args.since),
        "autonomous_work": autonomous_work(args.since),
        "projects": projects,
        "all_needs_attention": [x for p in projects for x in p["needs_attention"]],
        "pitches_awaiting_vote": scan_pitches(),
        "open_branches": scan_branches(),
    }
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
