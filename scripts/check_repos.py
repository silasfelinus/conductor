#!/usr/bin/env python3
"""
check_repos.py — Verify each repo in repos.yaml is reachable via GitHub API.

Run from repo root: python scripts/check_repos.py
Requires: GITHUB_TOKEN env var (or works with public repos without it).
"""

import os
import sys
import yaml
import urllib.request
import urllib.error
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REPOS_FILE = REPO_ROOT / "repos.yaml"


def github_get(path: str, token: str | None) -> tuple[int, dict]:
    url = f"https://api.github.com/repos/{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "conductor-check-repos/1.0",
            **({"Authorization": f"token {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {}


def main():
    if not REPOS_FILE.exists():
        print("repos.yaml not found — run from repo root")
        sys.exit(1)

    with open(REPOS_FILE) as f:
        data = yaml.safe_load(f)

    repos = data.get("repos", [])
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("⚠  GITHUB_TOKEN not set — rate limits apply to public repos")

    ok = True
    for entry in repos:
        repo = entry.get("repo")
        slug = entry.get("slug", "?")
        if not repo:
            print(f"  {slug:<30} — (no external repo)")
            continue

        status, body = github_get(repo, token)
        if status == 200:
            default_branch = body.get("default_branch", "main")
            private = body.get("private", False)
            print(f"  ✓ {slug:<30} {repo}  [{default_branch}] {'(private)' if private else '(public)'}")
        elif status == 404:
            print(f"  ✗ {slug:<30} {repo}  NOT FOUND (404)")
            ok = False
        elif status == 403:
            print(f"  ✗ {slug:<30} {repo}  FORBIDDEN (403) — check token permissions")
            ok = False
        else:
            print(f"  ? {slug:<30} {repo}  HTTP {status}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
