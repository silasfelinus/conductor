#!/usr/bin/env python3
"""Bridge GitHub issues into Conductor roadmaps, and close them when their task is done.

Silas, 2026-10-01: four kind_robots issues (#2663/#2664/#2667/#2668) sat open for
three weeks because nothing in Conductor ever read GitHub issues -- agents only
pick `status: ready` tasks out of projects/*/roadmap.yaml, and the only issue code
in the repo (build_conductor_summary.py) just counted them. This is the bridge.

For every repo in repos.yaml it lists open issues and, for each one not already
mirrored, appends a `ready` task to the owning project's roadmap carrying
`source_issue: <owner/repo>#<n>`. That field is the idempotency key: an issue is
imported at most once, ever, however many times this runs.

Routing:
  * a `project:<slug>` label on the issue wins, when that project exists;
  * otherwise the FIRST repos.yaml entry for the repo owns it (kind_robots ->
    kind-robots, not music-mentor, which shares the repo);
  * a `conductor:skip` label leaves the issue alone.

Trust. A task note is something the next agent acts on, so only issues opened
by the repo's OWNER / MEMBER / COLLABORATOR are imported. Anyone else's issue is
reported for Silas to triage, never turned into agent work -- that is the same
line AGENTS.md's security model draws for external content.

Lifecycle. Issues whose owning project is paused/retired/finished are reported,
not imported: an import there would be invisible to every Worker (they skip
inactive projects), which is exactly the silent-sitting failure this fixes.

Closing the loop. With --close-done, an open issue whose mirrored task is
`done` gets one comment naming the task and is closed as completed. The
implementing PR's own `Closes owner/repo#N` usually beats it to that; this is
the backstop for work that landed without the keyword.

Modes:
  python scripts/sync_github_issues.py              # --check: report only
  python scripts/sync_github_issues.py --apply      # append tasks to roadmaps
  python scripts/sync_github_issues.py --apply --imported-json out.json
  python scripts/sync_github_issues.py --comment-from out.json --close-done
                                                    # the workflow: import, push, THEN write
                                                    # to GitHub, so a retried push never
                                                    # double-comments

Exit status (--check): 0 nothing to do, 1 something to import/triage/close,
2 unresolved (a repo could not be read -- usually a missing token).

Requires: GITHUB_TOKEN, or ISSUE_BRIDGE_TOKEN for --comment-from / --close-done and
for private repos. The workflow prefers ISSUE_BRIDGE_TOKEN: Actions' default
token cannot write issues in any repo but this one.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from next_free_task_id import next_free_task_id  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
REPOS_FILE = ROOT / "repos.yaml"
OVERRIDES_FILE = ROOT / "project-overrides.yaml"

TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
SKIP_LABEL = "conductor:skip"
PROJECT_LABEL_PREFIX = "project:"
INACTIVE_LIFECYCLES = {"paused", "retired", "finished"}
BODY_LIMIT = 3000
SOURCE_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+$")


@dataclass
class Plan:
    imports: list[dict] = field(default_factory=list)
    untrusted: list[dict] = field(default_factory=list)
    inactive: list[dict] = field(default_factory=list)
    close: list[dict] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)

    def has_work(self) -> bool:
        return bool(self.imports or self.untrusted or self.inactive or self.close)


# --------------------------------------------------------------------------- io


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None
    return data if isinstance(data, dict) else {}


def repo_owners(repos_doc: dict) -> dict[str, str]:
    """repo -> owning project slug: the first repos.yaml entry naming that repo."""
    owners: dict[str, str] = {}
    for entry in repos_doc.get("repos", []) or []:
        if not isinstance(entry, dict):
            continue
        repo, slug = entry.get("repo"), entry.get("slug")
        if repo and slug and repo not in owners:
            owners[str(repo)] = str(slug)
    return owners


def lifecycles(overrides_doc: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for entry in overrides_doc.get("overrides", []) or []:
        if isinstance(entry, dict) and entry.get("slug"):
            out[str(entry["slug"])] = str(entry.get("status", "active"))
    return out


def load_roadmaps() -> dict[str, tuple[Path, dict]]:
    out: dict[str, tuple[Path, dict]] = {}
    for path in sorted(PROJECTS_DIR.glob("*/roadmap.yaml")):
        if path.parent.name.startswith("_"):
            continue
        out[path.parent.name] = (path, load_yaml(path))
    return out


def mirrored_tasks(roadmaps: dict[str, tuple[Path, dict]]) -> dict[str, tuple[str, dict]]:
    """source_issue -> (project slug, task) across every roadmap."""
    index: dict[str, tuple[str, dict]] = {}
    for slug, (_, doc) in roadmaps.items():
        for task in doc.get("tasks", []) or []:
            if isinstance(task, dict) and task.get("source_issue"):
                index[str(task["source_issue"])] = (slug, task)
    return index


def gh(method: str, path: str, token: str | None, body: dict | None = None,
       params: dict | None = None) -> object:
    url = f"https://api.github.com/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "conductor-issue-bridge",
            **({"Authorization": f"Bearer {token}"} if token else {}),
            **({"Content-Type": "application/json"} if data else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def fetch_open_issues(repo: str, token: str | None) -> list[dict]:
    issues: list[dict] = []
    for page in range(1, 11):
        batch = gh("GET", f"repos/{repo}/issues", token,
                   params={"state": "open", "per_page": "100", "page": str(page)})
        if not isinstance(batch, list) or not batch:
            break
        issues.extend(i for i in batch if "pull_request" not in i)
        if len(batch) < 100:
            break
    return issues


def fetch_issue(source: str, token: str | None) -> dict | None:
    repo, number = source.split("#", 1)
    data = gh("GET", f"repos/{repo}/issues/{number}", token)
    return data if isinstance(data, dict) else None


# ------------------------------------------------------------------- planning


def route(issue: dict, repo: str, owners: dict[str, str], projects: set[str]) -> str | None:
    for label in issue.get("labels", []) or []:
        name = label.get("name", "") if isinstance(label, dict) else str(label)
        if name.startswith(PROJECT_LABEL_PREFIX):
            slug = name[len(PROJECT_LABEL_PREFIX):].strip()
            if slug in projects:
                return slug
    return owners.get(repo)


def label_names(issue: dict) -> set[str]:
    return {
        (label.get("name", "") if isinstance(label, dict) else str(label))
        for label in issue.get("labels", []) or []
    }


def build_plan(token: str | None, *, close_done: bool) -> tuple[Plan, dict]:
    owners = repo_owners(load_yaml(REPOS_FILE))
    life = lifecycles(load_yaml(OVERRIDES_FILE))
    roadmaps = load_roadmaps()
    mirrored = mirrored_tasks(roadmaps)
    plan = Plan()
    open_sources: set[str] = set()

    for repo in sorted(owners):
        try:
            issues = fetch_open_issues(repo, token)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            plan.unresolved.append(f"{repo}: {exc}")
            continue
        for issue in issues:
            source = f"{repo}#{issue['number']}"
            open_sources.add(source)
            if source in mirrored or SKIP_LABEL in label_names(issue):
                continue
            entry = {
                "source": source,
                "repo": repo,
                "number": issue["number"],
                "title": str(issue.get("title", "")).strip(),
                "body": issue.get("body") or "",
                "url": issue.get("html_url", f"https://github.com/{repo}/issues/{issue['number']}"),
                "author": (issue.get("user") or {}).get("login", "?"),
                "created": str(issue.get("created_at", ""))[:10],
            }
            if str(issue.get("author_association", "")).upper() not in TRUSTED_ASSOCIATIONS:
                plan.untrusted.append(entry)
                continue
            slug = route(issue, repo, owners, set(roadmaps))
            if not slug or slug not in roadmaps:
                plan.unresolved.append(f"{source}: no roadmap for owning project {slug!r}")
                continue
            entry["project"] = slug
            if life.get(slug, "active") in INACTIVE_LIFECYCLES:
                entry["lifecycle"] = life[slug]
                plan.inactive.append(entry)
                continue
            plan.imports.append(entry)

    if close_done:
        for source, (slug, task) in sorted(mirrored.items()):
            if task.get("status") != "done" or source not in open_sources:
                continue
            plan.close.append({"source": source, "project": slug, "task": str(task.get("id"))})

    return plan, roadmaps


# ------------------------------------------------------------------- rendering


def _quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def task_note(entry: dict) -> str:
    body = entry["body"].replace("\r\n", "\n").strip()
    if len(body) > BODY_LIMIT:
        body = body[:BODY_LIMIT].rstrip() + f"\n\n[... truncated; read the full issue at {entry['url']}]"
    header = (
        f"FROM GITHUB ISSUE {entry['source']} ({entry['url']}), opened by @{entry['author']}"
        f" on {entry['created']}. Imported by scripts/sync_github_issues.py. Reference the issue"
        f" in the implementing PR (`Closes {entry['source']}`) so it closes on merge; the bridge"
        " closes it otherwise once this task is done."
    )
    return f"{header}\n\n{body}" if body else header


def render_task(entry: dict, task_id: str, indent: str, today: str) -> str:
    inner = indent + "  "
    lines = [
        f"{indent}- id: {task_id}",
        f"{inner}title: {_quote(entry['title'] or entry['source'])}",
        f"{inner}status: ready",
        f"{inner}stakes: reversible",
        f"{inner}owner: null",
        f"{inner}passes: 0",
        f"{inner}source_issue: {_quote(entry['source'])}",
        f"{inner}updated: '{today}'",
        f"{inner}note: |-",
    ]
    for line in task_note(entry).split("\n"):
        lines.append(f"{inner}  {line}" if line else "")
    return "\n".join(lines) + "\n"


def append_task_text(text: str, block: str) -> str:
    """Insert `block` after the last item of the top-level `tasks:` list.

    A text insert rather than a yaml.safe_dump rewrite, for the same reason as
    roadmap_text_patch.py: a dump reflows every task in the file.
    """
    lines = text.splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if re.match(r"^tasks:\s*(#.*)?$", l)), None)
    if start is None:
        raise ValueError("roadmap has no top-level `tasks:` key")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.strip() and not line.startswith((" ", "-", "#", "\t")):
            end = i
            break
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    if end > 0 and not lines[end - 1].endswith("\n"):
        lines[end - 1] += "\n"
    return "".join(lines[:end]) + block + "".join(lines[end:])


def item_indent(text: str) -> str:
    in_tasks = False
    for line in text.splitlines():
        if re.match(r"^tasks:\s*(#.*)?$", line):
            in_tasks = True
            continue
        if in_tasks:
            match = re.match(r"^(\s*)- ", line)
            if match:
                return match.group(1)
    return ""


def apply_imports(plan: Plan, roadmaps: dict[str, tuple[Path, dict]]) -> list[tuple[dict, str]]:
    today = datetime.date.today().isoformat()
    done: list[tuple[dict, str]] = []
    for entry in plan.imports:
        path, _ = roadmaps[entry["project"]]
        text = path.read_text(encoding="utf-8")
        doc = yaml.safe_load(text) or {}
        task_id = next_free_task_id(doc)
        new_text = append_task_text(text, render_task(entry, task_id, item_indent(text), today))
        reparsed = yaml.safe_load(new_text) or {}
        added = [t for t in reparsed.get("tasks", []) if isinstance(t, dict) and t.get("id") == task_id]
        if len(reparsed.get("tasks", [])) != len(doc.get("tasks", [])) + 1 or len(added) != 1 \
                or added[0].get("source_issue") != entry["source"]:
            raise RuntimeError(f"{path}: append of {task_id} did not round-trip; refusing to write")
        path.write_text(new_text, encoding="utf-8")
        roadmaps[entry["project"]] = (path, reparsed)
        done.append((entry, task_id))
    return done


# ---------------------------------------------------------------------- output


def footer() -> str:
    return "\n\n---\n_Posted by Conductor's issue bridge (`scripts/sync_github_issues.py`)._"


def report(plan: Plan) -> None:
    for e in plan.imports:
        print(f"IMPORT    {e['source']} -> {e['project']}: {e['title']}")
    for e in plan.inactive:
        print(f"INACTIVE  {e['source']} -> {e['project']} is {e['lifecycle']}; add a "
              f"`project:<slug>` label or reactivate it: {e['title']}")
    for e in plan.untrusted:
        print(f"TRIAGE    {e['source']} by @{e['author']} (not a collaborator; not imported): {e['title']}")
    for e in plan.close:
        print(f"CLOSE     {e['source']} -- {e['project']}/{e['task']} is done")
    for u in plan.unresolved:
        print(f"UNRESOLVED {u}")
    if not (plan.has_work() or plan.unresolved):
        print("Issue bridge: every open issue is mirrored; nothing to close.")


def post_import_comments(imported: list[dict], token: str | None) -> int:
    failures = 0
    for entry in imported:
        try:
            gh("POST", f"repos/{entry['repo']}/issues/{entry['number']}/comments", token, body={
                "body": f"Mirrored to Conductor as `{entry['project']}/{entry['task']}`; the next Worker "
                        f"cycle picks it up from `projects/{entry['project']}/roadmap.yaml`." + footer()})
        except urllib.error.URLError as exc:
            failures += 1
            print(f"WARN comment on {entry['source']} failed: {exc}", file=sys.stderr)
    return failures


def close_done_issues(plan: Plan, token: str | None) -> int:
    failures = 0
    for e in plan.close:
        repo, number = e["source"].split("#", 1)
        try:
            gh("POST", f"repos/{repo}/issues/{number}/comments", token, body={
                "body": f"Closing: the mirrored Conductor task `{e['project']}/{e['task']}` is done." + footer()})
            gh("PATCH", f"repos/{repo}/issues/{number}", token,
               body={"state": "closed", "state_reason": "completed"})
        except urllib.error.URLError as exc:
            failures += 1
            print(f"WARN closing {e['source']} failed: {exc}", file=sys.stderr)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report only (the default)")
    parser.add_argument("--apply", action="store_true", help="append tasks for unmirrored issues")
    parser.add_argument("--imported-json", type=Path,
                        help="with --apply: record what was imported, for a later --comment-from")
    parser.add_argument("--comment-from", type=Path,
                        help="post one 'mirrored to' comment per entry of an --imported-json file. "
                             "Run only after the roadmap commit has landed, so a retried push never "
                             "comments twice")
    parser.add_argument("--close-done", action="store_true",
                        help="close open issues whose mirrored task is done (needs a write token)")
    args = parser.parse_args(argv)

    token = os.environ.get("ISSUE_BRIDGE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    writes_github = bool(args.comment_from or args.close_done)
    if writes_github and not token:
        print("UNRESOLVED --comment-from/--close-done need ISSUE_BRIDGE_TOKEN or GITHUB_TOKEN", file=sys.stderr)
        return 2

    if args.comment_from:
        imported = json.loads(args.comment_from.read_text(encoding="utf-8")) if args.comment_from.exists() else []
        failures = post_import_comments(imported, token)
        if not args.close_done:
            print(f"Commented on {len(imported) - failures} imported issue(s).")
            return 1 if failures else 0
    else:
        failures = 0

    plan, roadmaps = build_plan(token, close_done=args.close_done or not args.apply)
    if not args.comment_from:
        report(plan)

    if args.apply:
        imported = [
            {**entry, "task": task_id, "body": ""}
            for entry, task_id in apply_imports(plan, roadmaps)
        ]
        if args.imported_json:
            args.imported_json.write_text(json.dumps(imported, indent=2), encoding="utf-8")
        print(f"Imported {len(imported)} issue(s).")
        if not args.close_done:
            return 0
    elif not args.close_done:
        if plan.has_work():
            return 1
        return 2 if plan.unresolved else 0

    failures += close_done_issues(plan, token)
    print(f"Closed {len(plan.close)} issue(s) whose task is done.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
