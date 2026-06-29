#!/usr/bin/env python3
"""
run_reviewer.py — Reviewer agent: reviews one open worker/* PR per cycle.

Finds the oldest open worker/* PR, reads the diff and context, calls Claude
to make a review decision, then executes the decision directly:
- merge: squash-merges the PR; on conflict, rebase+resolve and retry
- reject: posts actionable feedback, sets task back to ready
- escalate: flags needs-human, posts explanation

Updates the roadmap and appends a TALKBACK entry after every decision.

Usage:  python scripts/run_reviewer.py [--dry-run]
Env:    ANTHROPIC_API_KEY  (required)
        GITHUB_TOKEN       (required)
        GIT_USER_NAME      (default: reviewer-bot)
        GIT_USER_EMAIL     (default: reviewer-bot@users.noreply.github.com)
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
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
MAX_MERGE_ATTEMPTS = 3
UTC = datetime.timezone.utc


# ── Git helpers ───────────────────────────────────────────────────────────────

def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def git_config_bot() -> None:
    git("config", "user.name", os.environ.get("GIT_USER_NAME", "reviewer-bot"))
    git("config", "user.email", os.environ.get("GIT_USER_EMAIL", "reviewer-bot@users.noreply.github.com"))


# ── GitHub API ────────────────────────────────────────────────────────────────

def _gh(path: str, token: str | None, *, method: str = "GET", body: dict | None = None, accept: str | None = None) -> object:
    url = f"https://api.github.com/{path}"
    data = json.dumps(body).encode() if body else None
    headers = {
        "Accept": accept or "application/vnd.github.v3+json",
        "User-Agent": "conductor-reviewer/1.0",
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


# ── PR discovery ──────────────────────────────────────────────────────────────

def find_worker_prs(token: str | None) -> list[dict]:
    raw = _gh(f"repos/{REPO_OWNER}/{REPO_NAME}/pulls", token)
    if not isinstance(raw, list):
        return []
    prs = [
        pr for pr in raw
        if pr.get("head", {}).get("ref", "").startswith("worker/") and not pr.get("draft")
    ]
    prs.sort(key=lambda pr: pr.get("created_at", ""))
    return prs


def get_pr_diff(pr_number: int, token: str | None) -> str:
    raw = _gh(f"repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files", token)
    if not isinstance(raw, list):
        return "(diff unavailable)"
    parts = []
    total = 0
    for f in raw:
        patch = f.get("patch", "")
        if not patch:
            parts.append(f"--- {f.get('filename', '?')} (binary or no patch)")
            continue
        chunk = f"--- {f.get('filename', '?')}\n{patch}"
        if total + len(chunk) > 40_000:
            parts.append(f"--- {f.get('filename', '?')} (truncated)")
            break
        parts.append(chunk)
        total += len(chunk)
    return "\n\n".join(parts)


# ── Context gathering ─────────────────────────────────────────────────────────

def _read(path: str, max_chars: int = 8_000) -> str:
    try:
        text = Path(path).read_text(errors="replace")
        return text[:max_chars] if len(text) > max_chars else text
    except Exception:
        return ""


def extract_task_ref(pr: dict) -> tuple[str, str] | None:
    branch = pr.get("head", {}).get("ref", "")
    if branch.startswith("worker/"):
        rest = branch[len("worker/"):]
        m = re.search(r"^(.*?)-(t-\d+|todo-\d+)$", rest)
        if m:
            return m.group(1), m.group(2)
    return None


def gather_context(pr: dict) -> dict:
    ref = extract_task_ref(pr)
    project, task_id = ref if ref else (None, None)

    roadmap, roadmap_path, task, kind = None, None, None, "software"
    if project:
        path = f"projects/{project}/roadmap.yaml"
        if Path(path).exists():
            roadmap_path = path
            roadmap = yaml.safe_load(open(path)) or {}
            kind = roadmap.get("kind", "software")
            for t in roadmap.get("tasks", []):
                if t.get("id") == task_id:
                    task = t
                    break

    return {
        "project": project,
        "task_id": task_id,
        "kind": kind,
        "task": task or {},
        "roadmap": roadmap,
        "roadmap_path": roadmap_path,
        "talkback": _read(f"projects/{project}/TALKBACK.md", 5_000) if project else "",
        "control": _read("CONTROL.md", 3_000),
    }


# ── Claude review call ────────────────────────────────────────────────────────

REVIEWER_SYSTEM = """\
You are the Reviewer agent for an autonomous AI coordination system called AI_Networker.
Review the given worker/* PR and call the submit_review tool with your decision.

Merge rules:
- software, reversible, scoped, does the task → merge. task_status_after: done.
- software, needs changes → reject with specific actionable feedback. task_status_after: ready.
  If task passes >= 3: reject with task_status_after: blocked.
- content or proposal → escalate. task_status_after: needs-human.
- outward-facing or irreversible → escalate. task_status_after: needs-human.

Always write a TALKBACK entry. Reference the diff. Be specific. This is how the Worker improves.
Call submit_review — no prose response.
"""

REVIEW_TOOL = {
    "name": "submit_review",
    "description": "Submit your review decision.",
    "input_schema": {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["merge", "reject", "escalate"],
            },
            "reason": {"type": "string", "description": "One sentence."},
            "pr_comment": {
                "type": "string",
                "description": "Posted on the PR if rejecting or escalating. Empty string for merge.",
            },
            "talkback_entry": {
                "type": "string",
                "description": "Full formatted TALKBACK.md entry. Required for all decisions.",
            },
            "task_status_after": {
                "type": "string",
                "enum": ["done", "ready", "blocked", "needs-human"],
            },
        },
        "required": ["decision", "reason", "pr_comment", "talkback_entry", "task_status_after"],
    },
}


def call_claude(pr: dict, diff: str, ctx: dict, api_key: str) -> dict:
    today = datetime.datetime.now(UTC).strftime("%Y-%m-%d")
    project = ctx.get("project", "?")
    task_id = ctx.get("task_id", "?")
    task = ctx.get("task") or {}
    passes = task.get("passes", 0)

    user_msg = (
        f"Today: {today}\n\n"
        f"PR #{pr['number']}: {pr['title']}\n"
        f"Branch: {pr.get('head', {}).get('ref')}\n"
        f"Author: {pr.get('user', {}).get('login')}\n\n"
        f"Project: {project} (kind: {ctx.get('kind', 'software')})\n"
        f"Task: {task_id} — {task.get('title', 'unknown')}\n"
        f"Current passes: {passes}\n\n"
        f"PR body:\n{pr.get('body') or '(none)'}\n\n"
        f"Diff:\n{diff}\n\n"
        f"CONTROL.md direction:\n{ctx.get('control') or '(none)'}\n\n"
        f"Project TALKBACK history:\n{ctx.get('talkback') or '(none)'}\n\n"
        f"Call submit_review."
    )

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 2048,
        "system": REVIEWER_SYSTEM,
        "tools": [REVIEW_TOOL],
        "tool_choice": {"type": "tool", "name": "submit_review"},
        "messages": [{"role": "user", "content": user_msg}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read())
        for block in body.get("content", []):
            if block.get("type") == "tool_use" and block.get("name") == "submit_review":
                return block["input"]
        raise ValueError(f"No submit_review in response: {body}")
    except Exception as e:
        print(f"  [claude] {e}", file=sys.stderr)
        return {
            "decision": "escalate",
            "reason": f"Reviewer API unavailable: {e}",
            "pr_comment": "Escalated to needs-human — Reviewer API unavailable.",
            "talkback_entry": (
                f"## {today} | Reviewer → Worker | {project}/{task_id} | pattern\n\n"
                f"**Decision:** escalated to needs-human\n\n"
                f"**Reason:** Reviewer API call failed."
            ),
            "task_status_after": "needs-human",
        }


# ── Merge with conflict resolution ────────────────────────────────────────────

def _try_gh_merge(pr_number: int, token: str | None) -> bool:
    resp = _gh(
        f"repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/merge",
        token,
        method="PUT",
        body={"merge_method": "squash"},
    )
    return bool(resp.get("merged"))


def _get_conflicted_files() -> dict[str, str]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True
        ).stdout.strip()
        return {p: Path(p).read_text(errors="replace") for p in out.splitlines() if p}
    except Exception:
        return {}


def _call_anthropic_text(system: str, user: str, api_key: str) -> str:
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 4096,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read())
    return body["content"][0]["text"].strip()


def resolve_conflicts_with_claude(conflicted_files: dict[str, str], api_key: str) -> dict[str, str]:
    """Ask Claude Haiku to resolve git conflict markers. Returns {path: resolved_content}."""
    files_text = "\n\n".join(f"=== {p} ===\n{c}" for p, c in conflicted_files.items())
    system = (
        "You are resolving git merge conflicts. Remove all conflict markers and produce clean, "
        "correct merged content. Respond with JSON only: "
        '{"files": [{"path": "...", "content": "resolved content"}]}'
    )
    try:
        raw = _call_anthropic_text(system, f"Resolve:\n\n{files_text[:30_000]}", api_key)
        # Strip markdown code fences if present
        raw = raw.strip()
        if raw.startswith("```"):
            raw = "\n".join(raw.splitlines()[1:])
        if raw.endswith("```"):
            raw = "\n".join(raw.splitlines()[:-1])
        result = json.loads(raw)
        return {f["path"]: f["content"] for f in result.get("files", [])}
    except Exception as e:
        print(f"  [conflict-resolve] {e}", file=sys.stderr)
        return {}


def merge_with_retry(pr_number: int, branch: str, api_key: str, token: str | None) -> bool:
    for attempt in range(1, MAX_MERGE_ATTEMPTS + 1):
        print(f"  merge attempt {attempt}/{MAX_MERGE_ATTEMPTS}...", file=sys.stderr)
        time.sleep(3)

        merged = _try_gh_merge(pr_number, token)
        if merged:
            return True

        pr_info = _gh(f"repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}", token)
        mergeable = pr_info.get("mergeable")
        if mergeable is None:
            time.sleep(5)
            continue

        if mergeable is False:
            print("  conflict — attempting rebase+resolve", file=sys.stderr)
            try:
                git("fetch", "origin", "main")
                r = subprocess.run(["git", "rebase", "origin/main"], capture_output=True, text=True)
                if r.returncode != 0:
                    conflicted = _get_conflicted_files()
                    if not conflicted:
                        subprocess.run(["git", "rebase", "--abort"], capture_output=True)
                        return False
                    resolved = resolve_conflicts_with_claude(conflicted, api_key)
                    if not resolved:
                        subprocess.run(["git", "rebase", "--abort"], capture_output=True)
                        return False
                    for path, content in resolved.items():
                        Path(path).write_text(content)
                        git("add", path)
                    subprocess.run(["git", "rebase", "--continue"], capture_output=True)

                git("push", "--force-with-lease", "origin", branch)
                time.sleep(5)
                continue
            except RuntimeError as e:
                print(f"  rebase error: {e}", file=sys.stderr)
                subprocess.run(["git", "rebase", "--abort"], capture_output=True)
                return False

    return False


# ── Decision execution ────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def comment_pr(pr_number: int, body: str, token: str | None) -> None:
    _gh(
        f"repos/{REPO_OWNER}/{REPO_NAME}/issues/{pr_number}/comments",
        token,
        method="POST",
        body={"body": body},
    )


def update_roadmap(ctx: dict, result: dict) -> None:
    if not ctx.get("roadmap") or not ctx.get("roadmap_path") or not ctx.get("task"):
        return
    task = ctx["task"]
    task["status"] = result.get("task_status_after", "done")
    task["updated"] = _now_iso()
    if result.get("decision") == "reject":
        task["passes"] = task.get("passes", 0) + 1
    with open(ctx["roadmap_path"], "w") as f:
        yaml.safe_dump(ctx["roadmap"], f, sort_keys=False, default_flow_style=False, width=100)


def append_talkback(ctx: dict, result: dict) -> None:
    project = ctx.get("project", "unknown")
    tb_path = f"projects/{project}/TALKBACK.md"
    entry = (result.get("talkback_entry") or "").strip()
    if not entry:
        return
    try:
        existing = Path(tb_path).read_text() if Path(tb_path).exists() else ""
        Path(tb_path).write_text(existing.rstrip() + "\n\n" + entry + "\n")
    except Exception as e:
        print(f"  [talkback] {e}", file=sys.stderr)


def commit_review_artifacts(ctx: dict) -> None:
    project = ctx.get("project", "unknown")
    task_id = ctx.get("task_id", "?")
    changed = []
    if ctx.get("roadmap_path") and Path(ctx["roadmap_path"]).exists():
        changed.append(ctx["roadmap_path"])
    tb_path = f"projects/{project}/TALKBACK.md"
    if Path(tb_path).exists():
        changed.append(tb_path)
    if not changed:
        return
    for path in changed:
        git("add", path)
    try:
        git("commit", "-m", f"review: {project}/{task_id} [skip ci]")
        git("push", "origin", "main")
    except RuntimeError as e:
        print(f"  [review commit] {e}", file=sys.stderr)


def execute_decision(pr: dict, result: dict, ctx: dict, api_key: str, token: str | None, dry_run: bool) -> None:
    pr_number = pr["number"]
    decision = result["decision"]
    branch = pr.get("head", {}).get("ref", "")

    print(f"  decision: {decision} — {result.get('reason')}", file=sys.stderr)

    if dry_run:
        print(f"  [dry-run] would {decision} PR #{pr_number}")
        print(f"  [dry-run] TALKBACK entry:\n{result.get('talkback_entry', '')[:300]}")
        return

    if decision == "merge":
        # Checkout branch to enable rebase if needed
        git("fetch", "origin", branch)
        git("checkout", branch, check=False)
        merged = merge_with_retry(pr_number, branch, api_key, token)
        if merged:
            git("checkout", "main")
            git("pull", "origin", "main")
            print(f"  merged PR #{pr_number}", file=sys.stderr)
        else:
            # Couldn't merge — escalate instead
            comment_pr(pr_number, "⚠️ Reviewer could not merge after conflict resolution attempts. Escalating to needs-human.", token)
            result["task_status_after"] = "needs-human"
            print(f"  merge failed — escalated PR #{pr_number}", file=sys.stderr)
        git("checkout", "main", check=False)

    elif decision == "reject":
        comment_pr(pr_number, result.get("pr_comment") or "Changes requested.", token)
        print(f"  requested changes on PR #{pr_number}", file=sys.stderr)

    elif decision == "escalate":
        comment_pr(pr_number, result.get("pr_comment") or "Escalated to needs-human.", token)
        print(f"  escalated PR #{pr_number}", file=sys.stderr)

    update_roadmap(ctx, result)
    append_talkback(ctx, result)
    commit_review_artifacts(ctx)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not anthropic_key:
        sys.exit("ANTHROPIC_API_KEY not set")

    git_config_bot()
    print("[reviewer] starting cycle", file=sys.stderr)

    prs = find_worker_prs(github_token)
    if not prs:
        print("  no open worker/* PRs", file=sys.stderr)
        return

    pr = prs[0]
    print(f"  reviewing PR #{pr['number']}: {pr['title']}", file=sys.stderr)

    print("  fetching diff...", file=sys.stderr)
    diff = get_pr_diff(pr["number"], github_token)

    print("  gathering context...", file=sys.stderr)
    ctx = gather_context(pr)

    print("  calling Claude...", file=sys.stderr)
    result = call_claude(pr, diff, ctx, anthropic_key)

    execute_decision(pr, result, ctx, anthropic_key, github_token, args.dry_run)
    print("  done", file=sys.stderr)


if __name__ == "__main__":
    main()
