#!/usr/bin/env python3
"""
complete_todo.py — Mark a kind_robots Todo as DONE.

Usage: python scripts/complete_todo.py <todo_id>

Call this after the Worker finishes handling a Todo. If the work produced a PR,
call it after the PR is opened (not after merge — the Reviewer handles merge).

Requires: KR_API_TOKEN env var (same token used by fetch_todos.py)
"""
import json, os, sys, urllib.request, urllib.error

API_BASE = "https://kind-robots.vercel.app/api/todos"


def main():
    if len(sys.argv) < 2:
        print("Usage: complete_todo.py <todo_id>", file=sys.stderr)
        sys.exit(1)

    todo_id = sys.argv[1].strip()
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("❌ KR_API_TOKEN not set.", file=sys.stderr)
        sys.exit(1)

    payload = json.dumps({"status": "DONE"}).encode()
    req = urllib.request.Request(
        f"{API_BASE}/{todo_id}",
        data=payload,
        method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        if body.get("success"):
            title = body.get("data", {}).get("title", f"#{todo_id}")
            print(f"✅ Todo #{todo_id} marked DONE: {title}")
        else:
            print(f"⚠️  Unexpected response: {body}", file=sys.stderr)
            sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"❌ API returned {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
