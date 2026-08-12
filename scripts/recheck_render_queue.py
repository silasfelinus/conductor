#!/usr/bin/env python3
"""
recheck_render_queue.py — probe the shared kind_robots ComfyUI render queue
(`GET /api/art/queue/stats`) and append a stamped summary to RENDER-BACKLOG.md.

Replaces the copy-pasted "RECHECKED <date>: still PENDING=N, oldest ~Nh old" prose
paragraphs that had independently accumulated across ai-art-academy/t-004,
coloring-book/t-022, and newsfeed/t-022 (see conductor/t-081) — one append-only
ledger, one line per recheck, greppable from any task instead of hand-written
each time. Mirrors recheck_egress_blocks.py's ledger pattern (conductor/t-052).

Usage:
    python scripts/recheck_render_queue.py --task ai-art-academy/t-004
    python scripts/recheck_render_queue.py --no-append   # dry run

Requires KR_API_TOKEN (admin-capable machine token) in the environment; the
underlying endpoint is admin-gated. KR_BASE_URL defaults to
https://kindrobots.org.

This script never changes a roadmap task's status — it only records what it
observed. The calling agent still applies normal Failure-triage rules.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LEDGER_FILE = REPO_ROOT / "RENDER-BACKLOG.md"
LOG_MARKER = "## Log"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()


def fetch_queue_stats(window_hours: int = 24, timeout: float = 20.0) -> dict:
    """Fetch and return the `data` object from GET /api/art/queue/stats.

    Raises RuntimeError with a descriptive message on any failure (missing
    token, network error, non-2xx response, unexpected payload shape) so the
    caller can surface a clear error instead of a bare traceback.
    """
    if not KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN is required to query the render queue.")

    url = f"{KR_BASE_URL}/api/art/queue/stats?window={window_hours}"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"queue/stats returned HTTP {e.code}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"queue/stats unreachable: {e.reason}") from e

    if not isinstance(payload, dict) or not payload.get("success"):
        raise RuntimeError(f"queue/stats returned an unsuccessful payload: {payload}")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(f"queue/stats payload missing 'data': {payload}")
    return data


def summarize_failures(recent_failed: list[dict]) -> str:
    """Group recentFailed entries by a normalized error signature and return a
    one-line-per-signature summary, most common first."""
    if not recent_failed:
        return "recentFailed: none"

    def signature(entry: dict) -> str:
        error = str(entry.get("error") or "").strip()
        if "actively refused" in error or "10061" in error or "ConnectionRefused" in error:
            return "connection-refused to ComfyUI"
        if "workflow error" in error:
            return "generic workflow error (no node/exception detail forwarded)"
        return error[:120] if error else "(no error text)"

    counts = collections.Counter(signature(e) for e in recent_failed)
    total = len(recent_failed)
    lines = [f"{n}/{total} = {sig}" for sig, n in counts.most_common()]
    return "recentFailed (last " + str(total) + "): " + "; ".join(lines)


def classify(queue_depth: dict, window_throughput: dict) -> str:
    """Return 'growing', 'draining', or 'healthy' from PENDING depth/throughput."""
    pending_depth = queue_depth.get("PENDING", 0) or 0
    if pending_depth == 0:
        return "healthy"
    done = window_throughput.get("DONE", 0) or 0
    new_pending = window_throughput.get("PENDING", 0) or 0
    if new_pending > done:
        return "growing"
    return "draining"


def format_entry(data: dict, task: str | None) -> tuple[str, str]:
    """Return (status_label, detail_text) for the given queue_stats data."""
    queue_depth = data.get("queueDepth") or {}
    window_throughput = data.get("windowThroughput") or {}
    oldest_pending = data.get("oldestPending")
    recent_failed = data.get("recentFailed") or []

    status_label = classify(queue_depth, window_throughput)

    depth_parts = ", ".join(f"{k}={v}" for k, v in queue_depth.items())
    throughput_parts = ", ".join(f"{k}={v}" for k, v in window_throughput.items())

    if oldest_pending:
        age_seconds = oldest_pending.get("ageSeconds", 0) or 0
        age_hours = age_seconds / 3600
        oldest_part = (
            f"oldestPending: id={oldest_pending.get('id')}, age={age_seconds}s "
            f"(~{age_hours:.1f}h), engine={oldest_pending.get('engine')}."
        )
    else:
        oldest_part = "oldestPending: none."

    lines = [
        f"queueDepth: {depth_parts} (all-time).",
        oldest_part,
        f"windowThroughput ({data.get('windowHours', 24)}h): {throughput_parts}.",
        summarize_failures(recent_failed) + ".",
    ]
    return status_label, " ".join(lines)


def append_entry(
    task: str | None,
    status_label: str,
    detail: str,
    ledger_path: Path = LEDGER_FILE,
) -> None:
    if not ledger_path.exists():
        raise SystemExit(f"{ledger_path} not found — was it removed?")

    text = ledger_path.read_text(encoding="utf-8")
    if LOG_MARKER not in text:
        raise SystemExit(f"{ledger_path} missing a '{LOG_MARKER}' section marker")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    task_part = f" | {task}" if task else ""
    entry = f"\n## {ts}{task_part} | {status_label}\n{detail}\n"

    ledger_path.write_text(text.rstrip("\n") + "\n" + entry, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task", help="project/task-id this recheck relates to, e.g. ai-art-academy/t-004"
    )
    parser.add_argument("--window", type=int, default=24, help="stats window in hours")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Print the result without writing to RENDER-BACKLOG.md (dry run)",
    )
    args = parser.parse_args(argv)

    try:
        data = fetch_queue_stats(window_hours=args.window, timeout=args.timeout)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    status_label, detail = format_entry(data, args.task)
    print(f"{status_label}: {detail}")
    if not args.no_append:
        append_entry(args.task, status_label, detail, ledger_path=LEDGER_FILE)

    return 0


if __name__ == "__main__":
    sys.exit(main())
