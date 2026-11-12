#!/usr/bin/env python3
"""branch_janitor.py — keep conductor's remote branch list clean.

Conductor accumulates stale `claude/*` / `worker/*` / `close/*` / `conductor/*` branches: merged-PR branches
are only auto-removed when the repo's "delete head branch on merge" setting fires,
and branches whose work never got a PR (or whose PR was superseded) have no cleanup
path at all. Session credentials 403 on ref deletion, so this runs from a GitHub
Actions workflow whose GITHUB_TOKEN *can* delete refs (.github/workflows/branch-janitor.yml).

Two tiers, deliberately conservative (mirrors AGENTS.md "rescue stranded work"):
  - MERGED   — a strict ancestor of origin/main (fully merged, nothing unique) → delete.
  - FORCE    — named explicitly via --force-delete (one-shot removal of branches an
               operator has already verified superseded) → delete.
  - STRANDED — has unique commits, older than --stale-hours → REPORT ONLY, never
               auto-deleted (could be real un-PR'd work; a human/session rescues it).
  - ACTIVE   — has unique commits, recent → leave alone.

It never creates commits or branches — delete-and-report only — so it can't add to
the mess it cleans.

Usage:
  python scripts/branch_janitor.py [--dry-run] [--prefixes claude/,worker/,close/,conductor/]
      [--stale-hours 12] [--force-delete b1,b2] [--no-fetch] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PREFIXES = ("claude/", "worker/", "close/", "conductor/")
DEFAULT_STALE_HOURS = 12.0
RETIREMENTS_FILE = REPO_ROOT / 'ops' / 'branch-retirements.json'

MERGED = "merged"
FORCE = "force"
STRANDED = "stranded"
ACTIVE = "active"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False
    ).stdout.strip()


def refresh_remotes() -> None:
    git("fetch", "origin", "+refs/heads/*:refs/remotes/origin/*", "--prune")


def list_remote_branches(prefixes: tuple[str, ...]) -> list[str]:
    """Return short branch names (no 'origin/') under the given prefixes, minus main."""
    raw = git("branch", "-r", "--format=%(refname:short)")
    out: list[str] = []
    for line in raw.splitlines():
        ref = line.strip()
        if not ref.startswith("origin/"):
            continue
        name = ref[len("origin/"):]
        if name in ("main", "HEAD") or "->" in ref:
            continue
        if any(name.startswith(p) for p in prefixes):
            out.append(name)
    return out


def list_all_remote_branches() -> list[str]:
    """Return every remote branch short name (no 'origin/'), minus main/HEAD — no prefix filter."""
    raw = git("branch", "-r", "--format=%(refname:short)")
    out: list[str] = []
    for line in raw.splitlines():
        ref = line.strip()
        if not ref.startswith("origin/"):
            continue
        name = ref[len("origin/"):]
        if name in ("main", "HEAD") or "->" in ref:
            continue
        out.append(name)
    return out


def is_merged(branch: str, base: str = "origin/main") -> bool:
    """True if branch tip is a strict ancestor of base (fully merged)."""
    rc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", f"origin/{branch}", base],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    ).returncode
    return rc == 0


def branch_age_hours(branch: str, now: datetime | None = None) -> float:
    ts = git("log", "-1", "--format=%ct", f"origin/{branch}")
    if not ts:
        return 0.0
    committed = datetime.fromtimestamp(int(ts), tz=timezone.utc)
    now = now or datetime.now(timezone.utc)
    return (now - committed).total_seconds() / 3600.0


def classify(
    branches: list[str],
    *,
    is_merged_fn,
    age_fn,
    force_set: set[str],
    stale_hours: float,
) -> dict[str, list[str]]:
    """Pure classifier — inject is_merged_fn(branch)->bool and age_fn(branch)->hours.

    Precedence: FORCE (explicit operator intent) > MERGED > STRANDED > ACTIVE.
    """
    result: dict[str, list[str]] = {MERGED: [], FORCE: [], STRANDED: [], ACTIVE: []}
    for b in branches:
        if b in force_set:
            result[FORCE].append(b)
        elif is_merged_fn(b):
            result[MERGED].append(b)
        elif age_fn(b) >= stale_hours:
            result[STRANDED].append(b)
        else:
            result[ACTIVE].append(b)
    return result


def read_retirements(path: Path) -> dict[str, str]:
    """Explicit, reviewed branches and their exact disposable head SHA."""
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("retirements"), dict):
        raise ValueError(f"Malformed branch-retirements manifest: {path}")
    entries = data["retirements"]
    for branch, sha in entries.items():
        if (
            not isinstance(branch, str)
            or branch in ("main", "master", "HEAD")
            or not isinstance(sha, str)
            or not re.fullmatch(r"[0-9a-f]{40}", sha)
        ):
            raise ValueError(f"Invalid branch retirement entry: {branch!r}")
    return entries


def open_pr_head_branches() -> set[str] | None:
    """Fail closed on any GitHub API error. Never retire work with an open PR."""
    repo, token = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN")
    if not repo or not token:
        return None
    heads: set[str] = set()
    try:
        page = 1
        while True:
            req = urllib.request.Request(
                f"https://api.github.com/repos/{repo}/pulls?state=open&per_page=100&page={page}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "conductor-branch-janitor",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                prs = json.load(response)
            if not isinstance(prs, list):
                return None
            heads.update(pr["head"]["ref"] for pr in prs if pr["head"]["repo"]["full_name"] == repo)
            if len(prs) < 100:
                return heads
            page += 1
    except (OSError, ValueError, KeyError, TypeError):
        return None


def eligible_retirements(
    manifest: dict[str, str],
    existing: set[str],
    *,
    head_fn,
    open_heads: set[str] | None,
) -> tuple[set[str], dict[str, str]]:
    """Never force-delete a moved branch, a PR head, or an unverified head."""
    eligible: set[str] = set()
    skipped: dict[str, str] = {}
    for branch, expected in manifest.items():
        if branch not in existing:
            continue  # Already deleted.
        if open_heads is None:
            skipped[branch] = "open PR lookup unavailable"
        elif branch in open_heads:
            skipped[branch] = "open PR"
        elif head_fn(branch) != expected:
            skipped[branch] = "branch head changed"
        else:
            eligible.add(branch)
    return eligible, skipped


def delete_branch(branch: str, dry_run: bool) -> bool:
    if dry_run:
        return True
    # Deletion must fail if the branch moved after our fetch. A plain
    # "git push --delete" would discard a newly pushed commit in that race.
    expected = git("rev-parse", f"refs/remotes/origin/{branch}")
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        return False
    rc = subprocess.run(
        [
            "git", "push", "origin", f":refs/heads/{branch}",
            f"--force-with-lease=refs/heads/{branch}:{expected}",
        ],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    ).returncode
    return rc == 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Prune merged/superseded conductor branches")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; delete nothing")
    parser.add_argument("--prefixes", default=",".join(DEFAULT_PREFIXES),
                        help="Comma-separated branch prefixes to consider")
    parser.add_argument("--stale-hours", type=float, default=DEFAULT_STALE_HOURS,
                        help="Age past which an unmerged branch is reported as stranded")
    parser.add_argument("--force-delete", default="",
                        help="Comma-separated branch names to delete regardless of merge state")
    parser.add_argument("--retirements-file", type=Path, default=RETIREMENTS_FILE,
                        help="Reviewed exact-SHA branch retirements (never broad age-based deletion)")
    parser.add_argument("--no-fetch", action="store_true", help="Skip git fetch (tests)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    if not args.no_fetch:
        refresh_remotes()

    prefixes = tuple(p for p in (s.strip() for s in args.prefixes.split(",")) if p)
    force_set = {b.strip() for b in args.force_delete.split(",") if b.strip()}
    branches = list_remote_branches(prefixes)

    retirements = read_retirements(args.retirements_file)
    eligible, skipped = eligible_retirements(
        retirements, set(list_all_remote_branches()),
        head_fn=lambda branch: git("rev-parse", f"refs/remotes/origin/{branch}"),
        open_heads=open_pr_head_branches() if retirements else set(),
    )
    force_set.update(eligible)

    # A forced name is explicit operator/agent intent regardless of naming convention —
    # it must not be silently dropped just because it falls outside --prefixes.
    if force_set:
        existing = force_set & set(list_all_remote_branches())
        for b in existing:
            if b not in branches:
                branches.append(b)

    plan = classify(
        branches,
        is_merged_fn=is_merged,
        age_fn=branch_age_hours,
        force_set=force_set,
        stale_hours=args.stale_hours,
    )

    deleted, failed = [], []
    for b in plan[MERGED] + plan[FORCE]:
        (deleted if delete_branch(b, args.dry_run) else failed).append(b)

    summary = {
        "considered": len(branches),
        "deleted": deleted,
        "delete_failed": failed,
        "stranded_reported": plan[STRANDED],
        "active_left": plan[ACTIVE],
        "retirements_skipped": skipped,
        "dry_run": args.dry_run,
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        verb = "Would delete" if args.dry_run else "Deleted"
        print(f"Considered {len(branches)} {'/'.join(prefixes)} branch(es).")
        print(f"{verb} (merged/forced): {', '.join(deleted) or '(none)'}")
        if failed:
            print(f"Delete FAILED (perms?): {', '.join(failed)}")
        if plan[STRANDED]:
            print(f"Stranded (unmerged, >{args.stale_hours}h — review, NOT deleted): "
                  f"{', '.join(plan[STRANDED])}")
        if plan[ACTIVE]:
            print(f"Active (recent, left alone): {', '.join(plan[ACTIVE])}")
        if skipped:
            print(f"Retirements skipped (safety): {skipped}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
