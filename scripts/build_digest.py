#!/usr/bin/env python3
"""
build_digest.py — daily digest for Conductor across all projects + pitches.

Reads every projects/*/roadmap.yaml (skipping _template), scans pitches/ for items
awaiting Silas, plus recent git history. Prints a JSON digest for the emailer.

Projects whose project-overrides.yaml status is not "active" (paused, retired,
finished) are skipped entirely -- same rule CLAUDE.md's session-startup sweep
already applies, so a paused/retired/finished project's stale needs-human tasks
and frozen milestones don't keep surfacing in the daily email after the tasks
that made them stale are long gone.

Usage: python scripts/build_digest.py [--since "24 hours ago"]
"""
import subprocess, sys, json, argparse, datetime, glob, os, re

try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ACTIVE_STATES = {"active"}


def load_inactive_project_slugs():
    """Set of project slugs whose project-overrides.yaml status is NOT
    "active" (paused, retired, finished) -- the digest skips these entirely.
    A project with no override entry at all is treated as active
    (missing-override is its own separate audit finding, not a reason to
    silently hide a project from the digest). Missing project-overrides.yaml
    itself degrades to "nothing is inactive" rather than crashing the digest."""
    try:
        data = yaml.safe_load(open("project-overrides.yaml")) or {}
    except FileNotFoundError:
        return set()
    overrides = {
        str(entry.get("slug")): entry
        for entry in data.get("overrides", [])
        if isinstance(entry, dict) and entry.get("slug")
    }
    return {
        slug for slug, entry in overrides.items()
        if entry.get("status") not in ACTIVE_STATES
    }

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

def time_greeting():
    tod = _pacific_time_of_day()
    date_str = datetime.datetime.now(_TZ).strftime("%A, %B %-d")
    return f"Good {tod}, Silas. It's {date_str} on the Humboldt coast, and Conductor has the queue lights on."

def daily_spark(context=""):
    """Return a deterministic daily spark without contacting a model provider."""
    date = datetime.datetime.now(_TZ).date()
    context_hint = ""
    if context:
        first_project = context.split(", ")[0].strip()
        context_hint = f" Bonus nudge: give {first_project} one tiny clean win before chasing side quests."

    sparks = [
        {
            "label": "🤖 Today's robot",
            "text": "A tiny teal bookkeeper-bot named Ledgerbell patrols the roadmap, ringing once for ready tasks and twice for anything pretending not to need a human." + context_hint,
        },
        {
            "label": "🌊 Dream scenario",
            "text": "A moonlit control room floats above Humboldt Bay, each project card glowing like a buoy while patient robots sort the tide of todos." + context_hint,
        },
        {
            "label": "💡 Wild idea",
            "text": "Turn one recurring annoyance into a named micro-tool today: small, specific, testable, and impossible for Future Silas to misplace." + context_hint,
        },
    ]
    return sparks[date.toordinal() % len(sparks)]

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

def progress(milestones, tasks=None):
    tasks = tasks or []
    total = sum(m.get("weight", 0) for m in milestones)
    done = sum(m.get("weight", 0) for m in milestones if m.get("status") == "done")
    partial = sum(m.get("weight", 0) * 0.5 for m in milestones if m.get("status") == "in-progress")
    if total and (done + partial) > 0:
        return round((done + partial) / total * 100)
    # Fall back to task-completion ratio when milestones are all not-started.
    if tasks:
        done_t = sum(1 for t in tasks if t.get("status") == "done")
        return round(done_t / len(tasks) * 100)
    return 0

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

REPO = "silasfelinus/conductor"
DEFAULT_BRANCH = "main"
BACKLOG_DIR = "projects/dream-cycle/backlog"
SHIPPED_PATH = "projects/dream-cycle/SHIPPED.md"
CONDUCTOR_RAW = f"https://raw.githubusercontent.com/{REPO}/{DEFAULT_BRANCH}"
KR_BASE_URL = "https://kindrobots.org"
# Rendered art serves 200 from the self-hosted media origin; the app origin only
# 307-redirects /images/, which email clients render unreliably.
KR_MEDIA_ORIGIN = os.environ.get(
    "KR_MEDIA_ORIGIN", "https://media.acrocatranch.com").rstrip("/")
# The /daily-dream front page was removed from kind_robots; the digest no longer
# links to it (the dream-cycle art still renders inline).
DAILY_DREAM_PAGE = ""


def _public_url(rel):
    return f"{CONDUCTOR_RAW}/{rel.lstrip('/')}"


def _frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _section(text, heading):
    """Body text under a `## heading` up to the next `## ` (or end)."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", text, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else ""


def _json_block(text, name):
    m = re.search(rf"<!--\s*{name}\s*\n(.*?)\n-->", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def parse_proposal(path):
    """Parse a daily-proposal backlog file into card-ready data. None if not a proposal."""
    text = open(path, encoding="utf-8").read()
    fm = _frontmatter(text)
    if not fm.get("proposal"):
        return None
    idea = _section(text, "The idea")
    filename = os.path.basename(path)
    return {
        "slug": str(fm.get("slug", "")),
        "title": str(fm.get("title", filename)),
        "date": str(fm.get("proposal_date") or fm.get("created") or ""),
        "idea": idea,
        "edit_link": f"https://github.com/{REPO}/blob/{DEFAULT_BRANCH}/{BACKLOG_DIR}/{filename}#notes-from-silas",
        "data": _json_block(text, "proposal-data") or {},
        "built": _json_block(text, "built-data"),  # Phase 2: real records live
    }


def collect_proposals():
    """(tomorrow's fresh proposal, yesterday's proposal) — prefer built for yesterday."""
    props = []
    for path in sorted(glob.glob(f"{BACKLOG_DIR}/*.md")):
        name = os.path.basename(path)
        if name.startswith("_") or name == "README.md":
            continue
        parsed = parse_proposal(path)
        if parsed:
            props.append((parsed.get("date", ""), name, parsed))
    props.sort(key=lambda t: (t[0], t[1]))
    unbuilt = [p for _, _, p in props if not p.get("built")]
    built = [p for _, _, p in props if p.get("built")]
    tomorrow = unbuilt[-1] if unbuilt else (props[-1][2] if props else None)
    yesterday = built[-1] if built else (props[-2][2] if len(props) >= 2 else None)
    if yesterday is tomorrow:
        yesterday = None
    return tomorrow, yesterday


def match_images_for(slug):
    """Best-effort: conductor-tracked images whose filename starts with the dream slug."""
    if not slug:
        return []
    out = []
    for path in sorted(glob.glob("projects/images/*")):
        name = os.path.basename(path)
        if name.startswith(slug) and os.path.splitext(name)[1].lower() in (".webp", ".png", ".jpg", ".jpeg"):
            out.append({"name": name, "url": _public_url(path)})
    return out


def art_highlights(top_n=6):
    """Retired: the digest no longer ranks art.

    This gallery was fed by `curate_art.py --daily`, a vision-model pass that
    scored every render against AESTHETIC-GUIDELINES.md. Judging art is a human
    job, so that pass is gone and this returns nothing -- `gallery_section()`
    omits the section entirely on an empty list. The key stays in the payload
    because validate_digest.py requires it.
    """

    del top_n
    return []

def new_creations(limit=5):
    """Recent shipped creations, newest first, from the dream-cycle ledger."""
    if not os.path.exists(SHIPPED_PATH):
        return []
    text = open(SHIPPED_PATH, encoding="utf-8").read()
    entries = []
    for m in re.finditer(r"^##\s+(\d{4}-\d{2}-\d{2})\s+—\s+(.+?)\s+\(`([^`]+)`", text, re.MULTILINE):
        entries.append(f"{m.group(2)} ({m.group(1)})")
    return list(reversed(entries))[:limit]


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

    inactive_slugs = load_inactive_project_slugs()

    projects = []
    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if os.sep + "_template" + os.sep in path:
            continue
        slug = os.path.basename(os.path.dirname(path))
        if slug in inactive_slugs:
            continue
        rm = yaml.safe_load(open(path)) or {}
        name = rm.get("project", slug)
        milestones = rm.get("milestones", [])
        tasks = rm.get("tasks", [])
        projects.append({
            "name": name,
            "kind": rm.get("kind", "software"),
            "progress_pct": progress(milestones, tasks),
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

    tomorrow_proposal, yesterday_proposal = collect_proposals()
    yesterday_output = None
    if yesterday_proposal:
        yesterday_output = dict(yesterday_proposal)
        built = yesterday_output.get("built") or {}
        # Prefer art the record builder has attached to the live pitch sheets;
        # fall back to slug-matched conductor images.
        attached = [
            {"name": os.path.basename(a.get("public_path", "")),
             "url": KR_MEDIA_ORIGIN + a.get("public_path", "")}
            for a in built.get("art", []) if a.get("attached")
        ]
        yesterday_output["images"] = attached or match_images_for(
            yesterday_proposal.get("slug", ""))
        if built:
            records = built.get("records", {})
            yesterday_output["records_summary"] = {
                key: (len(val) if isinstance(val, list) else 1)
                for key, val in records.items()
            }
            yesterday_output["page"] = ""  # /daily-dream page removed

    payload = {
        "date": datetime.datetime.now(_TZ).date().isoformat(),
        "greeting": time_greeting(),
        "daily_spark": daily_spark(
            context=", ".join(p["name"] for p in projects) if projects else ""
        ),
        "tomorrow_proposal": tomorrow_proposal,
        "yesterday_output": yesterday_output,
        "daily_dream_page": DAILY_DREAM_PAGE,
        "art_highlights": art_highlights(),
        "new_creations": new_creations(),
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
