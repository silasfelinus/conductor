"""Daily committed roadmap snapshots; no credit for claims, comments or PR attempts."""
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import subprocess
import urllib.request

import yaml

PT = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parents[1]
# The index also contains infrastructure, creative studios and non-game tools.
NON_GAME_MASTERS = {
    "animation-manager", "dead-air", "dream-cycle", "interface-vision",
    "kind-economy", "playbook-kit", "tarot-studio",
}


def git(root, *args):
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, check=True,
    ).stdout.strip()


def task_counts(roadmap):
    tasks = [
        task for task in roadmap.get("tasks", [])
        if not task.get("recurring") and task.get("status") != "cancelled"
    ]
    return {"done": sum(t.get("status") == "done" for t in tasks), "total": len(tasks)}


def open_game_masters(root=ROOT):
    index = yaml.safe_load((root / "docs/agents/master-issues.yaml").read_text())["master_issues"]
    # One public, paginated search of open indexed master issues.
    numbers = set()
    for page in range(1, 11):
        url = (
            "https://api.github.com/repos/silasfelinus/kind_robots/issues"
            f"?state=open&labels=conductor%3Askip&per_page=100&page={page}"
        )
        with urllib.request.urlopen(url, timeout=12) as response:
            issues = json.load(response)
        numbers.update(issue["number"] for issue in issues if "pull_request" not in issue)
        if len(issues) < 100:
            break
    else:
        raise RuntimeError("Master issue pagination limit exceeded")
    return {
        slug: url for slug, url in index.items()
        if slug not in NON_GAME_MASTERS and int(url.rsplit("/", 1)[1]) in numbers
    }


def history(root=ROOT, days=14, now=None, slugs=None):
    """One point per Pacific day, today's point as of HEAD. Missing is not zero."""
    now = now or datetime.now(PT)
    dates = [now.date() - timedelta(days=i) for i in reversed(range(days + 1))]
    paths = {
        path.parent.name: str(path.relative_to(root))
        for path in (root / "projects").glob("*/roadmap.yaml")
        if path.parent.name != "_template" and (slugs is None or path.parent.name in slugs)
    }
    series = {slug: [] for slug in paths}
    for day in dates:
        if day == now.date():
            sha = git(root, "rev-parse", "HEAD")
        else:
            cutoff = datetime.combine(day + timedelta(days=1), time.min, PT) - timedelta(seconds=1)
            sha = git(root, "rev-list", "--first-parent", "-1", f"--before={cutoff.isoformat()}", "HEAD")
        for slug, path in paths.items():
            point = None
            if sha:
                # A missing file at a historical commit is a genuine gap.
                result = subprocess.run(
                    ["git", "show", f"{sha}:{path}"], cwd=root,
                    capture_output=True, text=True,
                )
                if result.returncode == 0:
                    point = task_counts(yaml.safe_load(result.stdout) or {})
            series[slug].append(point)
    return {"dates": [day.isoformat() for day in dates], "series": series}


def digest_history(root=ROOT):
    try:
        masters = open_game_masters(root)
        payload = history(root, slugs=masters)
        return {**payload, "masters": masters, "status": "ready"}
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError, yaml.YAMLError):
        return {"status": "unavailable", "dates": [], "series": {}, "masters": {}}
