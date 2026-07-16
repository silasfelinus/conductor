#!/usr/bin/env python3
"""branch_janitor.py — keep conductor's remote branch list clean.

Conductor accumulates stale `claude/*` / `worker/*` branches: merged-PR branches
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
  python scripts/branch_janitor.py [--dry-run] [--prefixes claude/,worker/]
      [--stale-hours 12] [--force-delete b1,b2] [--no-fetch] [--json]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PREFIXES = ("claude/", "worker/")
DEFAULT_STALE_HOURS = 12.0

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


def delete_branch(branch: str, dry_run: bool) -> bool:
    if dry_run:
        return True
    rc = subprocess.run(
        ["git", "push", "origin", "--delete", branch],
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
    parser.add_argument("--no-fetch", action="store_true", help="Skip git fetch (tests)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    if not args.no_fetch:
        refresh_remotes()

    prefixes = tuple(p for p in (s.strip() for s in args.prefixes.split(",")) if p)
    force_set = {b.strip() for b in args.force_delete.split(",") if b.strip()}
    branches = list_remote_branches(prefixes)

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

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
