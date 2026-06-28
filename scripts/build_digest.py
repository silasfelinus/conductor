#!/usr/bin/env python3
"""
build_digest.py — daily digest for AI_Networker across all projects + pitches.

Reads every projects/*/roadmap.yaml (skipping _template), scans pitches/ for items
awaiting Silas, plus recent git history. Prints a JSON digest for the emailer.

Usage: python scripts/build_digest.py [--since "24 hours ago"]
"""
import subprocess, sys, json, argparse, datetime, glob, os, re, random

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

_MORNING_GREETINGS = [
    "Good morning, Silas! The robots have been hard at work while you slept.",
    "Rise and shine — your agents logged more commits than you had dreams.",
    "Morning, Silas. Coffee first, then the digest. The machines waited.",
    "Good morning! The tide is in and so is your to-do list.",
    "Another day, another batch of autonomous shenanigans. Morning, Silas.",
    "Your agents clocked in before you did. Morning!",
    "The fog is probably still on the coast and the bots are definitely still running. Morning, Silas.",
]
_AFTERNOON_GREETINGS = [
    "Good afternoon, Silas. The day is half over and the agents haven't stopped.",
    "Afternoon check-in: the robots are still at it. How about you?",
    "Good afternoon! Somewhere a seagull is scheming and your agents are too.",
    "Midday dispatch from the machines. Hope your afternoon is going well, Silas.",
    "The afternoon sun is doing its thing. Your agents are doing theirs.",
]
_EVENING_GREETINGS = [
    "Good evening, Silas. The day's receipts are in.",
    "Evening! The bots kept busy so you could (hopefully) take a break.",
    "Good evening. The autonomous work doesn't stop, but you probably should.",
    "Another evening, another digest. Your empire of robots sends its regards.",
    "Evening, Silas. The ocean's still there. The agents are still running.",
]
_NIGHT_GREETINGS = [
    "Hey Silas — still up? The machines never sleep but you should.",
    "Late-night dispatch from the robot collective. Go to bed.",
    "The witching hour report. The agents are fine. Are you?",
    "It's late and the bots are still chugging. Classic.",
]

_SPARK_CHARACTERS = [
    "a lighthouse keeper who maintains the last fog horn on the internet",
    "a retired fortune teller who only predicts mundane things, like when parking meters will expire",
    "an AI that achieved sentience but only wants to discuss 1970s typefaces",
    "a mermaid accountant who handles exclusively barnacle-adjacent investments",
    "a time traveler who only visits Wednesday afternoons, on purpose",
    "a wizard who specializes in fixing printers — the ancient, cursed kind",
    "a ghost who haunts a very specific Excel spreadsheet no one has opened since 2009",
    "a dragon who hoards browser tabs instead of gold and refuses to close any of them",
    "a sea witch who collects expired domain names and is very smug about it",
    "a cryptid that only appears in the background of video calls at the worst possible moment",
    "an ancient oracle who speaks exclusively in error messages from operating systems that no longer exist",
    "a very small bureaucrat who lives inside your spam folder and takes their job seriously",
    "a sentient tide pool that has opinions about your coding style",
    "a retired raven who used to deliver curses but is now doing email marketing",
    "a very relaxed kraken who mostly just wants people to stop panicking when they see her",
    "a pelican who accidentally became the mascot for a startup and has mixed feelings about it",
]

_SPARK_DREAMS = [
    "The ocean sends you a formal written apology for every time it got your shoes wet. It's notarized.",
    "You discover that all lost socks have been living in a parallel dimension and they want to negotiate terms.",
    "Every computer fan in the world harmonizes into a single, surprisingly moving chord. A bird cries.",
    "A committee of very official-looking seagulls appoints you honorary mayor of an unspecified coastal region.",
    "You find out that every 404 page is actually a door to a real place, and someone has been living there for years.",
    "A very small wizard appears on your desk and asks to borrow your scissors. He doesn't say what for.",
    "All the fonts hold a convention and you're invited as keynote speaker. Papyrus shows up uninvited.",
    "The tide comes in and leaves behind a perfect to-do list. The handwriting is familiar but not yours.",
    "You are handed the deed to a library that only contains books that don't exist yet.",
    "An otter hands you a folded piece of kelp. Inside is the answer to a question you forgot you had.",
    "The moon files a noise complaint — not about sound, about light. It CC's you for some reason.",
    "Your commit history becomes a river and you have to navigate it in a very small boat.",
    "Every AI you've ever talked to shows up to a reunion. The vibes are surprisingly good.",
    "You receive a letter from a tree that you once photographed. It says thanks, the photo turned out well.",
]

_SPARK_PROJECTS = [
    "A coloring book where every page is a different cloud formation that you have to name yourself.",
    "A website that generates a fictional small-town newspaper headline every hour, completely unrelated to real news.",
    "An app that assigns personality types to houseplants based on how they've been growing lately.",
    "A generative art project that creates sea creatures that could plausibly exist but definitely don't.",
    "A zine about buildings that look like they're thinking about something.",
    "A browser extension that adds handwritten-looking encouraging margin notes to any article you read.",
    "A podcast where an AI interviews historical figures about what they'd think of current technology. Gently.",
    "A children's book starring a very reasonable, calm volcano who just wants everyone to be safe.",
    "A map of all the spots in Humboldt with the best acoustics for an impromptu moment.",
    "A daily poem generator that uses only words found in your git commit messages that week.",
    "An interactive fiction game where you play as an octopus who works in a library.",
    "A service that generates a coat of arms for any concept you can describe in one sentence.",
    "A kind-robots spin-off: a coloring page a day, generated from whatever was trending in creative AI that week.",
    "A 'rejected pitches' zine — your agents' most chaotic brainstorm ideas, illustrated and immortalized.",
]

_SPARK_LABELS = {
    "character": "🎭 Today's character",
    "dream": "🌊 Last night's dream (probably)",
    "project": "💡 Wild project idea",
}

def daily_spark():
    today = datetime.date.today()
    rng = random.Random(int(today.strftime("%Y%m%d")))
    category = rng.choice(["character", "dream", "project", "character", "project"])
    if category == "character":
        text = rng.choice(_SPARK_CHARACTERS)
    elif category == "dream":
        text = rng.choice(_SPARK_DREAMS)
    else:
        text = rng.choice(_SPARK_PROJECTS)
    label = _SPARK_LABELS[category]
    return {"label": label, "text": text}

def time_greeting():
    hour = _pacific_hour()
    today = datetime.date.today()
    rng = random.Random(int(today.strftime("%Y%m%d")) + hour)
    if 5 <= hour < 12:
        return rng.choice(_MORNING_GREETINGS)
    elif 12 <= hour < 17:
        return rng.choice(_AFTERNOON_GREETINGS)
    elif 17 <= hour < 21:
        return rng.choice(_EVENING_GREETINGS)
    else:
        return rng.choice(_NIGHT_GREETINGS)

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
        "daily_spark": daily_spark(),
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
