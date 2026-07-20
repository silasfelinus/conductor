#!/usr/bin/env python3
"""
flag_stale_apps.py — Flag bare-scaffold apps/<slug>/ folders that never got built out.

appmaker/t-011 (kaizen from the PR #104 merge, 2026-07-03): PR #104 scaffolded
apps/ for every existing active project as bare `flutter create`-style shells,
with no roadmap task driving any of them to build-out. This surfaces any
apps/<slug>/ whose lib/main.dart still matches the untouched AppMaker scaffold
template after N days, so Silas can decide build vs. retire instead of the
fleet growing silently.

A folder is "still bare" when lib/ contains nothing but the original
scaffolded main.dart (identified by the "scaffolded by AppMaker" marker string
scripts/new_app.py writes into it). Age is the app's earliest commit on GitHub
(queried via the REST API, not local git log — this repo's local clones are
often shallow/squash-merged, so local git history is not a reliable source of
a file's true creation date).

Run from repo root: python scripts/flag_stale_apps.py [--days N] [--json]
Requires: GITHUB_TOKEN env var with repo read access (falls back to
unauthenticated, rate-limited requests if unset). If the API is unreachable,
matching apps are still reported, with age marked unknown rather than
crashing.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
APPS_DIR = REPO_ROOT / "apps"
REPO_SLUG = "silasfelinus/conductor"
BARE_MARKER = "scaffolded by AppMaker"
DEFAULT_DAYS = 14


def github_get(path: str, token: str | None):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "conductor-flag-stale-apps/1.0",
            **({"Authorization": f"token {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read()), resp.headers.get("Link", "")
    except urllib.error.HTTPError as e:
        return e.code, None, ""
    except urllib.error.URLError:
        return None, None, ""


def last_page_number(link_header: str) -> int | None:
    for part in link_header.split(","):
        if 'rel="last"' in part:
            match = re.search(r"[?&]page=(\d+)", part)
            if match:
                return int(match.group(1))
    return None


def earliest_commit_date(file_path: str, token: str | None) -> str | None:
    """Return the ISO date of the oldest commit touching file_path, via the GitHub API."""
    base = f"/repos/{REPO_SLUG}/commits?path={file_path}&per_page=1"
    status, body, link = github_get(base, token)
    if status != 200 or not body:
        return None

    last_page = last_page_number(link)
    if last_page:
        status, body, _ = github_get(f"{base}&page={last_page}", token)
        if status != 200 or not body:
            return None

    if not body:
        return None
    oldest = body[-1]
    return oldest["commit"]["committer"]["date"]


def find_apps() -> list[str]:
    if not APPS_DIR.is_dir():
        return []
    return sorted(
        p.name
        for p in APPS_DIR.iterdir()
        if p.is_dir() and (p / "lib" / "main.dart").is_file()
    )


def is_still_bare(slug: str) -> bool:
    main_dart = APPS_DIR / slug / "lib" / "main.dart"
    lib_files = list((APPS_DIR / slug / "lib").iterdir())
    if len(lib_files) != 1:
        return False
    return BARE_MARKER in main_dart.read_text()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--days", type=int, default=DEFAULT_DAYS,
        help=f"flag apps bare for at least this many days (default {DEFAULT_DAYS})",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a text report")
    parser.add_argument(
        "--strict", action="store_true",
        help="exit 1 if any app is flagged (for optional CI gating)",
    )
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    now = datetime.now(timezone.utc)

    findings = []
    for slug in find_apps():
        if not is_still_bare(slug):
            continue

        commit_date = earliest_commit_date(f"apps/{slug}/lib/main.dart", token)
        age_days = None
        if commit_date:
            created = datetime.fromisoformat(commit_date.replace("Z", "+00:00"))
            age_days = (now - created).days

        findings.append({
            "slug": slug,
            "created_at": commit_date,
            "age_days": age_days,
        })

    flagged = [
        f for f in findings
        if f["age_days"] is not None and f["age_days"] >= args.days
    ]
    unknown_age = [f for f in findings if f["age_days"] is None]

    if args.json:
        print(json.dumps({"flagged": flagged, "unknown_age": unknown_age}, indent=2))
    else:
        if not findings:
            print("No bare-scaffold apps/ found — nothing to flag.")
        else:
            if flagged:
                print(f"Bare-scaffold apps at or past {args.days} days (build vs. retire):")
                for f in sorted(flagged, key=lambda x: -x["age_days"]):
                    print(f"  apps/{f['slug']}/  — {f['age_days']}d old (scaffolded {f['created_at']})")
            else:
                print(f"No bare-scaffold apps have reached {args.days} days yet.")
            if unknown_age:
                print("\nStill bare, age unknown (GitHub API unreachable or no token):")
                for f in unknown_age:
                    print(f"  apps/{f['slug']}/")

    if args.strict and flagged:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
