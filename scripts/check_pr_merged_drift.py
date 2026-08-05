#!/usr/bin/env python3
"""
check_pr_merged_drift.py — Flag conductor tasks stuck at claimed/review whose
implementing cross-repo PR has already merged.

Kaizen from conductor/t-071 (Reviewer, burst-mode, 2026-07-19, from
newsfeed/t-020): the conductor claim commit for a task can land, and then the
real implementation (a PR in a target repo like kind_robots) can merge minutes
later with no `status: review` checkpoint ever recorded in between. Roadmap
state alone then gives no signal the work is already done — the last session
that hit this only caught it by manually re-checking kind_robots' commit
history on its next sweep. This script closes that gap: it scans every active
projects/*/roadmap.yaml for tasks at `status: claimed` or `status: review` and
looks for the PR that actually implemented them.

conductor/t-098: a task's `note` legitimately cites TWO kinds of PR — the one
that IMPLEMENTED the task, and the one whose "Kaizen suggestion" section
proposed the task in the first place. A note-quoted-PR-only checker cannot
tell them apart, which produces both a false positive (the kaizen-filing PR
merges, flagging a task that never moved) and a false negative (the real
implementation PR, never mentioned in the note, merges silently and the
checker has nothing to say). interface-vision/t-081 hit both at once.

Three-pass design (conductor/t-099 added pass 0):
  0. FIELD (strongest) — if the task carries a dedicated `implementation_pr`
     roadmap field (written by close_task.py's `--implementation-pr`, e.g.
     "silasfelinus/kind_robots#1464"), check that exact PR directly. This is
     evidence the implementing session itself recorded, not a heuristic --
     stronger than a title-text search and immune to a close-out PR whose
     title doesn't follow the "<project>/<task-id>:" convention. A task with
     this field set skips the title-search pass entirely (it's already the
     authoritative answer); a failed lookup lands in `unresolved`, same as a
     failed search.
  1. AUTHORITATIVE (title search) — for tasks with no `implementation_pr`
     field, search every tracked repo for a merged PR whose TITLE names this
     exact "<project>/<task-id>" (the convention every close-out PR already
     follows, e.g. "ai-art-academy/t-010: add role=group..."). A hit here is
     strong, task-authored evidence and is reported as a high-confidence
     finding.
  2. FALLBACK (weak) — only for tasks neither pass above confirmed: fall back
     to the old note-quoted-PR-reference heuristic, but label the result
     explicitly as weak/unconfirmed (it may be the kaizen-filing PR, not the
     implementation) rather than asserting drift.

Read-only: never edits a roadmap. Paused, retired, and finished projects are
excluded by default according to project-overrides.yaml; pass
--include-inactive for an intentional archive sweep.

Usage:
  python scripts/check_pr_merged_drift.py
  python scripts/check_pr_merged_drift.py --json
  python scripts/check_pr_merged_drift.py --include-inactive

Requires: GITHUB_TOKEN env var (recommended; avoids rate limits, required for
private repos, and the search API in particular has a much tighter
unauthenticated rate limit than the REST PR-lookup endpoint).

Exit codes:
  0 = verified clean (no high-confidence or weak findings, nothing unresolved)
  1 = high-confidence drift found (implementation_pr field or task-id-named
      PR already merged)
  2 = could not fully verify (a search or PR lookup call failed) — a clean
      read here would be a false "all good", so this outranks a bare weak
      signal below
  3 = only weak/unconfirmed signals found (note-quoted PR merged, but no
      task-id-named PR confirmed it as the actual implementation) — worth a
      look, not proof of drift
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
OVERRIDES = ROOT / "project-overrides.yaml"
IN_PROGRESS = {"claimed", "review"}
ACTIVE_STATUS = "active"

# Repos this conductor instance tracks cross-repo work against. Keep in sync
# with the actual GitHub remotes agents push to (see CLAUDE.md repo scope).
REPO_ALIASES = {
    "conductor": "silasfelinus/conductor",
    "kind_robots": "silasfelinus/kind_robots",
    "kind-robots": "silasfelinus/kind_robots",
    "kindrobots-unraid": "silasfelinus/kindrobots-unraid",
    "serendipity-voice": "silasfelinus/serendipity-voice",
    "comfyui": "silasfelinus/comfyui",
    "ComfyUI": "silasfelinus/comfyui",
    "portos": "silasfelinus/PortOS",
    "PortOS": "silasfelinus/PortOS",
}

# Every distinct repo the aliases above resolve to, for the authoritative
# task-id search pass (which doesn't know in advance which repo implemented
# a given task).
ALL_TRACKED_REPOS = sorted(set(REPO_ALIASES.values()))

PR_REF_RE = re.compile(
    r"\b(" + "|".join(re.escape(a) for a in REPO_ALIASES) + r")\s+PR\s+#(\d+)\b"
)

# Matches close_task.py's `--implementation-pr` format, e.g.
# "silasfelinus/kind_robots#1464". Deliberately not restricted to REPO_ALIASES --
# the field is free-form owner/repo, unlike the note-reference heuristic above
# which only recognizes known short aliases.
IMPLEMENTATION_PR_RE = re.compile(r"^([\w.-]+/[\w.-]+)#(\d+)$")


def parse_implementation_pr(value: Any) -> tuple[str, int] | None:
    """Parse a task's `implementation_pr` field into (repo, number).

    Returns None if the field is absent, blank, or doesn't match the
    "owner/repo#number" shape close_task.py writes.
    """
    if not value:
        return None
    match = IMPLEMENTATION_PR_RE.match(str(value).strip())
    if not match:
        return None
    return match.group(1), int(match.group(2))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_project_statuses(path: Path) -> dict[str, str]:
    """Return normalized lifecycle status by project slug.

    Missing override files or missing slugs default to active. That preserves
    historical behavior while still honoring every explicit pause/retirement.
    """
    if not path.exists():
        return {}
    data = load_yaml(path)
    statuses: dict[str, str] = {}
    for entry in data.get("overrides", []) or []:
        if not isinstance(entry, dict):
            continue
        slug = str(entry.get("slug") or "").strip()
        if not slug:
            continue
        statuses[slug] = str(entry.get("status") or ACTIVE_STATUS).strip().lower()
    return statuses


def find_pr_refs(text: str) -> list[tuple[str, int]]:
    """Return deduped (owner/repo, pr_number) pairs referenced in text."""
    seen: list[tuple[str, int]] = []
    for alias, number in PR_REF_RE.findall(text or ""):
        pair = (REPO_ALIASES[alias], int(number))
        if pair not in seen:
            seen.append(pair)
    return seen


def _iter_in_progress_tasks(
    projects_dir: Path,
    overrides_path: Path | None,
    include_inactive: bool,
):
    """Yield (slug, lifecycle, task) for every claimed/review task in scope."""
    lifecycle_path = overrides_path or projects_dir.parent / "project-overrides.yaml"
    project_statuses = load_project_statuses(lifecycle_path)
    for roadmap_path in sorted(projects_dir.glob("*/roadmap.yaml")):
        slug = roadmap_path.parent.name
        if slug == "_template":
            continue
        lifecycle = project_statuses.get(slug, ACTIVE_STATUS)
        if not include_inactive and lifecycle != ACTIVE_STATUS:
            continue
        data = load_yaml(roadmap_path)
        for task in data.get("tasks", []) or []:
            if task.get("status") not in IN_PROGRESS:
                continue
            yield slug, lifecycle, task


def scan(
    projects_dir: Path = PROJECTS,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[dict[str, Any]]:
    """Find claimed/review tasks with a resolvable note-quoted cross-repo PR
    reference. This is the WEAK evidence pass (conductor/t-098) — a note
    legitimately cites either the implementing PR or the PR whose kaizen
    suggestion filed the task, and this function cannot tell them apart.
    Callers should prefer `scan_in_progress_tasks` + `gh_search_task_prs`
    (the authoritative pass) and only fall back to this for tasks that pass
    doesn't confirm.
    """
    candidates = []
    for slug, lifecycle, task in _iter_in_progress_tasks(
        projects_dir, overrides_path, include_inactive
    ):
        text = f"{task.get('title', '')}\n{task.get('note', '')}"
        for repo, number in find_pr_refs(text):
            candidates.append({
                "project": slug,
                "project_status": lifecycle,
                "task_id": task.get("id"),
                "title": task.get("title"),
                "status": task.get("status"),
                "repo": repo,
                "pr_number": number,
            })
    return candidates


def scan_in_progress_tasks(
    projects_dir: Path = PROJECTS,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[dict[str, Any]]:
    """Return every claimed/review task in scope, regardless of whether its
    note quotes a PR — the authoritative task-id-search pass needs to check
    ALL in-progress tasks, not just the ones a note happens to reference
    (conductor/t-098's false-negative half: the real implementation PR is
    sometimes never mentioned in the note at all)."""
    tasks = []
    for slug, lifecycle, task in _iter_in_progress_tasks(
        projects_dir, overrides_path, include_inactive
    ):
        tasks.append({
            "project": slug,
            "project_status": lifecycle,
            "task_id": task.get("id"),
            "title": task.get("title"),
            "status": task.get("status"),
            "implementation_pr": task.get("implementation_pr"),
        })
    return tasks


def gh_pr(repo: str, number: int, token: str | None) -> dict | None:
    url = f"https://api.github.com/repos/{repo}/pulls/{number}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "conductor-check-pr-merged-drift/1.0",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  [gh] {repo}#{number}: HTTP {e.code}", file=sys.stderr)
        return None
    except Exception as e:  # noqa: BLE001 — best-effort network call, never fatal
        print(f"  [gh] {repo}#{number}: {e}", file=sys.stderr)
        return None


def _repo_from_repository_url(url: str | None) -> str | None:
    m = re.match(r"^https://api\.github\.com/repos/(.+)$", url or "")
    return m.group(1) if m else None


def gh_search_task_prs(
    repos: list[str], project: str, task_id: str, token: str | None
) -> list[dict[str, Any]] | None:
    """Search the given repos for a merged PR whose TITLE names this exact
    "<project>/<task-id>" (the convention close-out PRs already follow, e.g.
    "ai-art-academy/t-010: add role=group..."). Returns a list of
    {"repo": owner/name, "number": int} candidates (title match only — the
    caller confirms merge state via `gh_pr`), or None if the search call
    itself failed (network/API error — distinct from "found nothing").

    This is the authoritative pass (conductor/t-098): a title the implementing
    session itself wrote about its own work is much stronger evidence than a
    PR merely quoted somewhere in the task's note history.
    """
    if not repos or not project or not task_id:
        return []
    phrase = f'"{project}/{task_id}"'
    query = " ".join(
        [phrase, "in:title", "is:pr", "is:merged"] + [f"repo:{r}" for r in repos]
    )
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": query, "per_page": 10}
    )
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "conductor-check-pr-merged-drift/1.0",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  [gh-search] {project}/{task_id}: HTTP {e.code}", file=sys.stderr)
        return None
    except Exception as e:  # noqa: BLE001 — best-effort network call, never fatal
        print(f"  [gh-search] {project}/{task_id}: {e}", file=sys.stderr)
        return None

    results = []
    for item in data.get("items", []) or []:
        repo = _repo_from_repository_url(item.get("repository_url"))
        number = item.get("number")
        if repo and number:
            results.append({"repo": repo, "number": number})
    return results


def check(
    candidates: list[dict[str, Any]], token: str | None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Verify a list of (repo, pr_number) candidates against the GitHub API.

    Return (findings, unresolved). `findings` holds candidates whose PR is
    confirmed merged; `unresolved` holds candidates whose PR lookup failed —
    these were not verified either way and must not be reported as clean.
    Confidence-agnostic: callers (the authoritative and fallback passes) tag
    their own candidates before calling this, and this function passes those
    tags through untouched via the dict spread below.
    """
    findings = []
    unresolved = []
    for candidate in candidates:
        pr = gh_pr(candidate["repo"], candidate["pr_number"], token)
        if not pr:
            unresolved.append(candidate)
            continue
        if pr.get("merged") or pr.get("merged_at"):
            findings.append({
                **candidate,
                "pr_merged_at": pr.get("merged_at"),
                "pr_title": pr.get("title"),
            })
    return findings, unresolved


def check_drift(
    projects_dir: Path = PROJECTS,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
    token: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Run all three passes and return {"high": [...], "weak": [...], "unresolved": [...]}.

    `high` — either a task's own `implementation_pr` field (strongest,
      conductor/t-099) or a task-id-named merged PR (authoritative title
      search) confirmed merged.
    `weak` — neither of the above confirmed, but a note-quoted PR is merged
      (may be the kaizen-filing PR, not the implementation — say so, don't
      assert drift).
    `unresolved` — a field lookup, search, or PR-lookup call itself failed
      for a task with no other confirmation either way; a clean result must
      not be reported for it.
    """
    all_tasks = scan_in_progress_tasks(projects_dir, overrides_path, include_inactive)
    note_candidates = scan(projects_dir, overrides_path, include_inactive)
    note_by_task = {}
    for candidate in note_candidates:
        note_by_task.setdefault((candidate["project"], candidate["task_id"]), []).append(candidate)

    # Pass 0 (strongest): a task carrying a dedicated `implementation_pr`
    # field is checked directly against that PR and never falls through to
    # the title-search pass -- the field is itself stronger, task-authored
    # evidence than a search heuristic, so a task that has one is either
    # confirmed or unresolved here, not silently re-evaluated by pass 1.
    field_candidates = []
    search_tasks = []
    for task in all_tasks:
        parsed = parse_implementation_pr(task.get("implementation_pr"))
        if parsed is None:
            search_tasks.append(task)
            continue
        repo, number = parsed
        field_candidates.append({**task, "repo": repo, "pr_number": number})

    field_findings, field_unresolved = check(field_candidates, token)
    for finding in field_findings:
        finding["confidence"] = "high"
        finding["source"] = "implementation-pr-field"

    confirmed_keys = {(f["project"], f["task_id"]) for f in field_findings}

    # Pass 1 (authoritative title search): only for tasks with no usable
    # implementation_pr field.
    search_candidates = []
    search_failed_tasks = []
    for task in search_tasks:
        results = gh_search_task_prs(
            ALL_TRACKED_REPOS, task["project"], task["task_id"], token
        )
        if results is None:
            search_failed_tasks.append(task)
            continue
        for result in results:
            search_candidates.append({
                **task,
                "repo": result["repo"],
                "pr_number": result["number"],
            })

    search_findings, search_unresolved = check(search_candidates, token)
    for finding in search_findings:
        finding["confidence"] = "high"
        finding["source"] = "task-id-search"

    high_findings = field_findings + search_findings
    confirmed_keys |= {(f["project"], f["task_id"]) for f in search_findings}

    # Pass 2 (fallback, weak): only for title-search tasks neither pass above
    # confirmed, AND whose title search actually completed (a task whose
    # search call itself failed belongs in `unresolved`, not a downgraded
    # "weak" finding presented as if the authoritative pass came back empty).
    searched_keys = {(t["project"], t["task_id"]) for t in search_tasks} - {
        (t["project"], t["task_id"]) for t in search_failed_tasks
    }
    fallback_candidates = [
        candidate
        for key in searched_keys - confirmed_keys
        for candidate in note_by_task.get(key, [])
    ]
    weak_findings, weak_unresolved = check(fallback_candidates, token)
    for finding in weak_findings:
        finding["confidence"] = "low"
        finding["source"] = "note-reference"

    unresolved = (
        field_unresolved
        + list(search_failed_tasks)
        + search_unresolved
        + weak_unresolved
    )
    return {"high": high_findings, "weak": weak_findings, "unresolved": unresolved}


def render(
    findings: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
    total: int,
    weak: list[dict[str, Any]] | None = None,
) -> str:
    weak = weak or []
    lines = []
    if unresolved:
        lines.append(
            f"⚠  {len(unresolved)}/{total} candidate(s) could NOT be verified (API lookup failed — "
            f"see stderr for HTTP codes). This is common in sandboxed sessions that only have "
            f"GitHub MCP tools, not direct API/token access — a raw urllib call to api.github.com "
            f"will 403 there even with GITHUB_TOKEN set. Do not treat this run as a clean audit; "
            f"re-check the unresolved task(s) via the GitHub connector instead:"
        )
        for candidate in unresolved:
            ref = (
                f"{candidate['repo']}#{candidate['pr_number']}"
                if "repo" in candidate and "pr_number" in candidate
                else "task-id search"
            )
            lines.append(f"    {candidate['project']}/{candidate['task_id']} -> {ref}")
        lines.append("")
    if findings:
        lines.append(
            f"Found {len(findings)} task(s) at claimed/review whose implementing PR already merged "
            "(high confidence — PR title names this task):\n"
        )
        for finding in findings:
            lines.append(
                f"  {finding['project']}/{finding['task_id']} (status: {finding['status']}) — "
                f"{finding['repo']}#{finding['pr_number']} \"{finding['pr_title']}\", "
                f"merged {finding['pr_merged_at']}"
            )
        lines.append("")
    if weak:
        lines.append(
            f"{len(weak)} task(s) at claimed/review quote a merged PR in their note, but no "
            "task-id-named PR confirmed it as the actual implementation (weak evidence — this may "
            "be the PR whose kaizen suggestion FILED the task, not the one that implemented it; "
            "confirm manually before closing):\n"
        )
        for finding in weak:
            lines.append(
                f"  {finding['project']}/{finding['task_id']} (status: {finding['status']}) references "
                f"{finding['repo']}#{finding['pr_number']} \"{finding['pr_title']}\", "
                f"merged {finding['pr_merged_at']}"
            )
        lines.append("")
    if not findings and not weak and not unresolved:
        lines.append(
            f"No drift found — all {total} active-project claimed/review task(s) "
            "verified clean (no task-id-named or note-quoted merged PR found)."
        )
    elif not findings and not weak and unresolved and len(unresolved) < total:
        lines.append(
            f"No drift found among the {total - len(unresolved)} task(s) successfully verified."
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also scan paused, retired, and finished projects",
    )
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("⚠  GITHUB_TOKEN not set — rate limits apply", file=sys.stderr)

    result = check_drift(include_inactive=args.include_inactive, token=token)
    high, weak, unresolved = result["high"], result["weak"], result["unresolved"]
    total = len(scan_in_progress_tasks(include_inactive=args.include_inactive))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(high, unresolved, total, weak=weak))

    # Exit codes: 0 = verified clean, 1 = high-confidence drift found,
    # 2 = could not fully verify, 3 = only weak/unconfirmed signals found.
    # Distinguishing these prevents an unverified or merely-weak run from
    # reading as either "clean" or "confirmed drift".
    if high:
        sys.exit(1)
    if unresolved:
        sys.exit(2)
    if weak:
        sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
