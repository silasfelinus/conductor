#!/usr/bin/env python3
"""
fetch_todos.py — Fetch open Todos from kind_robots for the Worker to action.

Run at the START of every Worker cycle, BEFORE resolve_deps.py.
If any OPEN todos are returned, the Worker handles the highest-priority one
before picking from roadmaps.

Requires: KR_API_TOKEN env var (a valid kind_robots JWT for Silas's account)
API:      GET https://kind-robots.vercel.app/api/todos
          Authorization: Bearer <token>

Exit codes: 0 = success (even if no todos), 1 = auth/network failure
Stdout: JSON list of OPEN todos sorted HIGH->NORMAL->LOW, then newest-first
"""
import json, os, sys, urllib.request, urllib.error

API_URL = "https://kind-robots.vercel.app/api/todos"
PRIORITY_ORDER = {"HIGH": 0, "NORMAL": 1, "LOW": 2}


def main():
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("⚠️  KR_API_TOKEN not set — skipping todo check.", file=sys.stderr)
        print("[]")
        return

    req = urllib.request.Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"⚠️  kind_robots API returned {e.code} — skipping todo check.", file=sys.stderr)
        print("[]")
        return
    except Exception as e:
        print(f"⚠️  Could not reach kind_robots API: {e}", file=sys.stderr)
        print("[]")
        return

    todos = body.get("data", [])
    open_todos = [t for t in todos if t.get("status") == "OPEN"]
    open_todos.sort(
        key=lambda t: (
            PRIORITY_ORDER.get(t.get("priority", "NORMAL"), 1),
            -(t.get("id") or 0),  # newest first within same priority
        )
    )

    print(json.dumps(open_todos, indent=2))

    if open_todos:
        print(f"\n\U0001f4cb {len(open_todos)} open todo(s) — handle before roadmap tasks:", file=sys.stderr)
        for t in open_todos:
            pri = t.get("priority", "NORMAL")
            print(f"  [{pri}] #{t['id']}: {t['title']}", file=sys.stderr)
    else:
        print("✅ No open todos.", file=sys.stderr)


if __name__ == "__main__":
    main()
