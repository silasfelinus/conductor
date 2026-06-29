#!/usr/bin/env python3
"""
run_worker.py — Worker agent: executes one task cycle and merges its own PR.

Step 0: Fetch open todos from kind_robots API
Step 1: Run resolve_deps.py to unblock waiting tasks
Step 2: Find highest-priority ready task
Step 3: Claim it (update roadmap YAML, commit to main)
Step 4: Gather context and call OpenAI to generate the work
Step 5: Create worker/* branch, write files, commit, push, open PR
Step 6: Attempt to merge the PR; on conflict, rebase+resolve and retry
Step 7: Update task status (done on merge, or leave PR open for Reviewer)

Usage:  python scripts/run_worker.py [--dry-run]
Env:    OPENAI_API_KEY     (required)
        GITHUB_TOKEN       (required for PR creation and merge)
        KR_API_TOKEN       (optional; kind_robots todos)
        GIT_USER_NAME      (default: worker-bot)
        GIT_USER_EMAIL     (default: worker-bot@users.noreply.github.com)
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not installed — run: pip install pyyaml")

REPO_OWNER = "silasfelinus"
REPO_NAME = "conductor"
PRIORITY_FILE = "projects/priority.yaml"
MAX_CONTEXT_CHARS = 60_000
MAX_MERGE_ATTEMPTS = 3
UTC = datetime.timezone.utc


# ── Git helpers ───────────────────────────────────────────────────────────────

def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def git_config_bot() -> None:
    git("config", "user.name", os.environ.get("GIT_USER_NAME", "worker-bot"))
    git("config", "user.email", os.environ.get("GIT_USER_EMAIL", "worker-bot@users.noreply.github.com"))


# ── GitHub API ────────────────────────────────────────────────────────────────

def _gh(path: str, token: str | None, *, method: str = "GET", body: dict | None = None) -> object:
    url = f"https://api.github.com/{path}"
    data = json.dumps(body).encode() if body else None
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "conductor-worker/1.0",
        **({"Authorization": f"Bearer {token}"} if token else {}),
        **({"Content-Type": "application/json"} if data else {}),
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  [gh] {method} {path}: HTTP {e.code} — {e.read().decode(errors='replace')[:200]}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"  [gh] {method} {path}: {e}", file=sys.stderr)
        return {}


# ── Todos ─────────────────────────────────────────────────────────────────────

def fetch_todos(kr_token: str | None) -> list[dict]:
    if not kr_token:
        return []
    req = urllib.request.Request(
        "https://kind-robots.vercel.app/api/todos",
        headers={"Authorization": f"Bearer {kr_token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        prio = {"HIGH": 0, "NORMAL": 1, "LOW": 2}
        open_todos = [t for t in body.get("data", []) if t.get("status") == "OPEN"]
        return sorted(open_todos, key=lambda t: (prio.get(t.get("priority", "NORMAL"), 1), -(t.get("id") or 0)))
    except Exception as e:
        print(f"  [todos] {e}", file=sys.stderr)
        return []


def complete_todo(todo_id: int, kr_token: str | None) -> None:
    if not kr_token:
        return
    subprocess.run(
        [sys.executable, "scripts/complete_todo.py", str(todo_id)],
        check=False,
        env={**os.environ, "KR_API_TOKEN": kr_token},
    )


# ── Roadmap operations ────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_priority() -> list[str]:
    try:
        return (yaml.safe_load(Path(PRIORITY_FILE).read_text()) or {}).get("order", [])
    except Exception:
        return []


def load_roadmaps() -> list[dict]:
    roadmaps = []
    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if "_template" in path:
            continue
        rm = yaml.safe_load(open(path)) or {}
        rm["_path"] = path
        roadmaps.append(rm)
    return roadmaps


def find_ready_task(priority_order: list[str], roadmaps: list[dict]) -> dict | None:
    by_project = {rm.get("project"): rm for rm in roadmaps}
    ordered = [by_project[p] for p in priority_order if p in by_project]
    remaining = [rm for rm in roadmaps if rm.get("project") not in priority_order]
    for rm in ordered + remaining:
        for task in rm.get("tasks", []):
            if task.get("status") == "ready":
                return {
                    "project": rm.get("project"),
                    "kind": rm.get("kind", "software"),
                    "task": task,
                    "roadmap_path": rm["_path"],
                    "roadmap": rm,
                    "is_todo": False,
                }
    return None


def todo_to_item(todo: dict, roadmaps: list[dict]) -> dict:
    desc = (todo.get("description") or "").lower()
    project, kind = "conductor", "software"
    for rm in roadmaps:
        p = rm.get("project", "")
        if p and p in desc:
            project, kind = p, rm.get("kind", "software")
            break
    return {
        "project": project,
        "kind": kind,
        "is_todo": True,
        "todo_id": todo.get("id"),
        "task": {
            "id": f"todo-{todo.get('id')}",
            "title": todo.get("title", "todo"),
            "status": "ready",
            "note": todo.get("description", ""),
            "stakes": "reversible",
        },
        "roadmap_path": None,
        "roadmap": None,
    }


def write_roadmap(item: dict) -> None:
    if item["is_todo"] or not item["roadmap_path"]:
        return
    with open(item["roadmap_path"], "w") as f:
        yaml.safe_dump(item["roadmap"], f, sort_keys=False, default_flow_style=False, width=100)


def claim_task(item: dict, dry_run: bool) -> None:
    if item["is_todo"] or not item["roadmap_path"]:
        return
    task = item["task"]
    task["status"] = "claimed"
    task["owner"] = "worker"
    task["updated"] = _now_iso()
    write_roadmap(item)
    commit_msg = f"claim: {item['project']}/{task['id']}"
    if dry_run:
        print(f"  [dry-run] {commit_msg}")
        return
    git("add", item["roadmap_path"])
    git("commit", "-m", commit_msg)
    git("push", "origin", "main")


def set_task_status(item: dict, status: str) -> None:
    if item["is_todo"] or not item["roadmap_path"]:
        return
    item["task"]["status"] = status
    item["task"]["updated"] = _now_iso()
    write_roadmap(item)


# ── Context gathering ─────────────────────────────────────────────────────────

def _read(path: str, max_chars: int = 8_000) -> str:
    try:
        text = Path(path).read_text(errors="replace")
        return text[:max_chars] if len(text) > max_chars else text
    except Exception:
        return ""


def gather_context(item: dict) -> str:
    parts = []
    project = item["project"]
    task = item["task"]

    control = _read("CONTROL.md", 4_000)
    if control:
        parts.append(f"## CONTROL.md\n{control}")

    parts.append(
        f"## Task\n"
        f"Project: {project} (kind: {item['kind']})\n"
        f"Task ID: {task.get('id')}\n"
        f"Title: {task.get('title')}\n"
        f"Stakes: {task.get('stakes', 'reversible')}\n"
        f"Notes: {task.get('note') or 'None'}"
    )

    tb = _read(f"projects/{project}/TALKBACK.md", 4_000)
    if tb:
        parts.append(f"## Project TALKBACK (prior feedback)\n{tb}")

    project_dir = f"projects/{project}"
    if Path(project_dir).is_dir():
        try:
            ls = git("ls-files", project_dir)
            non_binary = [f for f in ls.splitlines() if not f.endswith((".webp", ".png", ".jpg", ".ico"))]
            parts.append(f"## Files in {project_dir}/\n" + "\n".join(non_binary))
            for fname in ["SPEC.md", "SCHEMA.md", "STACK.md", "CHANGELOG.md", "BOUNDARY.md"]:
                content = _read(f"{project_dir}/{fname}", 4_000)
                if content:
                    parts.append(f"## {project_dir}/{fname}\n{content}")
        except Exception:
            pass

    full = "\n\n".join(parts)
    return full[:MAX_CONTEXT_CHARS] + "\n\n... [context truncated]" if len(full) > MAX_CONTEXT_CHARS else full


# ── OpenAI calls ──────────────────────────────────────────────────────────────

WORKER_SYSTEM = """\
You are the Worker agent for an autonomous AI coordination system called AI_Networker.
Execute the given task and return a JSON object. No prose — JSON only.

Project kinds:
- software: write code. Produce the actual implementation files.
- content: write content files (marketing, copy, drafts). Goes to needs-human.
- proposal: write pitches/<YYYY-MM-DD>-<slug>.md using the pitch template. Goes to needs-human.

Return exactly this JSON shape:
{
  "decision": "do_task" | "escalate",
  "reason": "one sentence",
  "files": [
    {"path": "path/from/repo/root", "content": "full file content", "action": "create" | "modify"}
  ],
  "pr_title": "short descriptive title",
  "pr_body": "### Task\\n<project>/<id>: <title> (kind: <kind>)\\n\\n### What changed / what I produced\\n- ...\\n\\n### How I verified\\n- ...\\n\\n### Stakes\\nreversible | outward-facing | irreversible\\n\\n### Flags for Reviewer\\n- ..."
}

Escalate if: task requires secrets, live deploys, outward-facing actions, or you lack enough context.
Safety: no real secrets in files; no DNS/billing/deploy changes; keep scope tight.
"""

PITCH_TEMPLATE = """\
# Pitch: {title}
date: {date}
project-target: {project}
status: awaiting-silas

## The idea


## Why it's worth doing


## Rough effort
small | medium | large

## Suggested first task
What the Worker would do first if you approve.
"""

CONFLICT_SYSTEM = """\
You are resolving git merge conflicts. You will receive files with conflict markers.
For each file, output the fully resolved content with no conflict markers remaining.
Return JSON only:
{"files": [{"path": "...", "content": "resolved file content with no conflict markers"}]}
"""


def _call_openai(messages: list[dict], api_key: str, max_tokens: int = 4096) -> str:
    payload = json.dumps({
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "max_tokens": max_tokens,
        "messages": messages,
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read())
    return body["choices"][0]["message"]["content"]


def call_openai_work(item: dict, context: str, api_key: str) -> dict:
    today = datetime.datetime.now(UTC).strftime("%Y-%m-%d")
    kind = item["kind"]
    extra = f"\n\nThis is a PROPOSAL task. Output a single file: pitches/{today}-<slug>.md\nTemplate:\n{PITCH_TEMPLATE}" if kind == "proposal" else ""
    try:
        raw = _call_openai([
            {"role": "system", "content": WORKER_SYSTEM},
            {"role": "user", "content": f"Today: {today}\n\nContext:\n{context}{extra}\n\nExecute the task. Return JSON."},
        ], api_key)
        return json.loads(raw)
    except Exception as e:
        print(f"  [openai] {e}", file=sys.stderr)
        return {"decision": "escalate", "reason": f"OpenAI call failed: {e}", "files": [], "pr_title": "", "pr_body": ""}


def call_openai_resolve_conflicts(conflicted_files: dict[str, str], api_key: str) -> dict[str, str]:
    """Ask OpenAI to resolve conflict markers in the given files. Returns {path: resolved_content}."""
    files_text = "\n\n".join(
        f"=== {path} ===\n{content}" for path, content in conflicted_files.items()
    )
    try:
        raw = _call_openai([
            {"role": "system", "content": CONFLICT_SYSTEM},
            {"role": "user", "content": f"Resolve these conflicted files:\n\n{files_text[:30_000]}"},
        ], api_key, max_tokens=4096)
        result = json.loads(raw)
        return {f["path"]: f["content"] for f in result.get("files", [])}
    except Exception as e:
        print(f"  [conflict-resolve] {e}", file=sys.stderr)
        return {}


# ── Work execution ────────────────────────────────────────────────────────────

def execute_branch(item: dict, result: dict, dry_run: bool) -> str:
    project = item["project"]
    task_id = item["task"]["id"]
    branch = f"worker/{project}-{task_id}"

    if dry_run:
        print(f"  [dry-run] branch: {branch}")
        for f in result.get("files", []):
            print(f"    {f.get('action', 'create')}: {f['path']}")
        return branch

    git("checkout", "-b", branch)
    for file_entry in result.get("files", []):
        path = file_entry["path"]
        action = file_entry.get("action", "create")
        if action == "delete":
            if Path(path).exists():
                Path(path).unlink()
                git("rm", path, check=False)
        else:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(file_entry["content"])
            git("add", path)

    if item["roadmap_path"] and Path(item["roadmap_path"]).exists():
        git("add", item["roadmap_path"])

    git("commit", "-m", f"feat({project}): {item['task'].get('title', task_id)}")
    git("push", "-u", "origin", branch)
    return branch


def open_pr(item: dict, result: dict, branch: str, token: str | None) -> int | None:
    task = item["task"]
    project = item["project"]
    pr_title = result.get("pr_title") or f"{project}/{task['id']}: {task.get('title', '')}"
    pr_body = result.get("pr_body") or "(no body generated)"
    resp = _gh(
        f"repos/{REPO_OWNER}/{REPO_NAME}/pulls",
        token,
        method="POST",
        body={"title": pr_title, "head": branch, "base": "main", "body": pr_body},
    )
    pr_number = resp.get("number")
    print(f"  {'opened PR #' + str(pr_number) if pr_number else 'PR creation failed'}", file=sys.stderr)
    return pr_number


# ── Auto-merge with conflict resolution ───────────────────────────────────────

def _try_gh_merge(pr_number: int, token: str | None) -> bool:
    resp = _gh(
        f"repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/merge",
        token,
        method="PUT",
        body={"merge_method": "squash"},
    )
    return bool(resp.get("merged"))


def _get_conflicted_files() -> dict[str, str]:
    """Return {path: content} for files with conflict markers after a failed rebase."""
    try:
        output = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True
        ).stdout.strip()
        if not output:
            return {}
        result = {}
        for path in output.splitlines():
            try:
                result[path] = Path(path).read_text(errors="replace")
            except Exception:
                pass
        return result
    except Exception:
        return {}


def auto_merge(
    pr_number: int,
    branch: str,
    item: dict,
    openai_key: str,
    token: str | None,
) -> bool:
    """Attempt to merge the PR. On conflict, rebase+resolve and retry. Returns True if merged."""
    for attempt in range(1, MAX_MERGE_ATTEMPTS + 1):
        print(f"  merge attempt {attempt}/{MAX_MERGE_ATTEMPTS}...", file=sys.stderr)
        time.sleep(3)  # let GitHub settle after push

        merged = _try_gh_merge(pr_number, token)
        if merged:
            print("  merged successfully", file=sys.stderr)
            return True

        # Check PR state — if not mergeable, try rebase
        pr_info = _gh(f"repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}", token)
        mergeable = pr_info.get("mergeable")
        if mergeable is None:
            time.sleep(5)  # GitHub is still computing mergeability
            continue
        if mergeable is False:
            print("  merge conflict detected — attempting rebase+resolve", file=sys.stderr)
            try:
                git("fetch", "origin", "main")
                result = subprocess.run(
                    ["git", "rebase", "origin/main"],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    # Rebase failed — resolve conflicts with OpenAI
                    conflicted = _get_conflicted_files()
                    if not conflicted:
                        print("  rebase failed with no identifiable conflicts — giving up", file=sys.stderr)
                        _abort_rebase()
                        return False

                    print(f"  resolving {len(conflicted)} conflicted file(s) with OpenAI...", file=sys.stderr)
                    resolved = call_openai_resolve_conflicts(conflicted, openai_key)
                    if not resolved:
                        print("  conflict resolution failed — giving up", file=sys.stderr)
                        _abort_rebase()
                        return False

                    for path, content in resolved.items():
                        Path(path).write_text(content)
                        git("add", path)

                    git("rebase", "--continue", check=False)

                git("push", "--force-with-lease", "origin", branch)
                time.sleep(5)
                continue  # retry merge
            except RuntimeError as e:
                print(f"  rebase error: {e}", file=sys.stderr)
                _abort_rebase()
                return False

        if mergeable:
            merged = _try_gh_merge(pr_number, token)
            if merged:
                print("  merged successfully", file=sys.stderr)
                return True

    print(f"  could not merge after {MAX_MERGE_ATTEMPTS} attempts — leaving PR open", file=sys.stderr)
    return False


def _abort_rebase() -> None:
    subprocess.run(["git", "rebase", "--abort"], capture_output=True)


def comment_pr(pr_number: int, body: str, token: str | None) -> None:
    _gh(
        f"repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments",
        token,
        method="POST",
        body={"body": body},
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    github_token = os.environ.get("GITHUB_TOKEN")
    kr_token = os.environ.get("KR_API_TOKEN")

    if not openai_key:
        sys.exit("OPENAI_API_KEY not set")

    git_config_bot()
    print("[worker] starting cycle", file=sys.stderr)

    # Step 0: todos
    todos = fetch_todos(kr_token)

    # Step 1: resolve deps
    print("  resolving deps...", file=sys.stderr)
    subprocess.run([sys.executable, "scripts/resolve_deps.py"], check=False)

    # Step 2: find task
    roadmaps = load_roadmaps()
    if todos:
        print(f"  {len(todos)} open todo(s) — taking top one", file=sys.stderr)
        item = todo_to_item(todos[0], roadmaps)
    else:
        item = find_ready_task(load_priority(), roadmaps)

    if not item:
        print("  no work available — all tasks claimed, done, or waiting", file=sys.stderr)
        return

    task = item["task"]
    kind = item["kind"]
    print(f"  task: {item['project']}/{task['id']} — {task.get('title')}", file=sys.stderr)

    # Step 3: claim
    print("  claiming...", file=sys.stderr)
    claim_task(item, args.dry_run)

    # Step 4: generate work
    print("  gathering context...", file=sys.stderr)
    context = gather_context(item)
    print("  calling OpenAI...", file=sys.stderr)
    result = call_openai_work(item, context, openai_key)

    decision = result.get("decision", "escalate")
    print(f"  decision: {decision} — {result.get('reason', '')}", file=sys.stderr)

    if decision == "escalate":
        set_task_status(item, "needs-human")
        if not item["is_todo"] and item["roadmap_path"] and not args.dry_run:
            git("add", item["roadmap_path"])
            git("commit", "-m", f"escalate: {item['project']}/{task['id']} to needs-human")
            git("push", "origin", "main")
        print("  escalated to needs-human", file=sys.stderr)
        return

    # Step 5: create branch + open PR
    status_after = "review" if kind == "software" else "needs-human"
    set_task_status(item, status_after)

    print("  writing files...", file=sys.stderr)
    branch = execute_branch(item, result, args.dry_run)

    if args.dry_run:
        return

    pr_number = open_pr(item, result, branch, github_token)

    # Step 6: auto-merge (software only — content/proposal go to needs-human for Silas)
    if pr_number and kind == "software":
        print("  attempting auto-merge...", file=sys.stderr)
        merged = auto_merge(pr_number, branch, item, openai_key, github_token)
        if merged:
            # Pull main and update task to done
            git("checkout", "main")
            git("pull", "origin", "main")
            set_task_status(item, "done")
            git("add", item["roadmap_path"] or ".")
            try:
                git("commit", "-m", f"done: {item['project']}/{task['id']} [skip ci]")
                git("push", "origin", "main")
            except RuntimeError:
                pass  # might be nothing to commit if roadmap was part of the squash
        else:
            comment_pr(
                pr_number,
                "⚠️ Auto-merge failed after retries. Leaving open for Reviewer.",
                github_token,
            )

    # Step 7: complete todo if applicable
    if todos and item["is_todo"]:
        complete_todo(todos[0].get("id"), kr_token)

    print(f"  done — {branch}", file=sys.stderr)


if __name__ == "__main__":
    main()
