#!/usr/bin/env python3
"""Fail loudly when the known ComfyUI host-buffer read fault is freshly recurring.

This is a narrow standing sentinel for the recurring
``hostbuf_file_reader_read failed`` CLIPTextEncode failure. It deliberately
uses the same queue/stats source and signature classifier as
``recheck_render_queue.py`` so alerting and the render backlog cannot disagree
about what constitutes the hardware-fault signature.

The queue stats endpoint returns the latest 25 failed jobs regardless of age,
so this script must apply its own timestamp window before classifying failures.
Otherwise a repaired outage can keep failing the hourly workflow indefinitely
until 25 newer failures happen to displace the stale rows.

Exit codes:
  0: no fresh hostbuf failure is present
  1: queue stats could not be read
  2: one or more fresh failures match the hostbuf signature
"""

from __future__ import annotations

from datetime import datetime, timezone
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from consume_art_queue_core import fetch_queue_stats  # noqa: E402
from recheck_render_queue import group_failures_by_signature  # noqa: E402

HOSTBUF_SIGNATURE = "hostbuf-file-reader-read"
SENTINEL_WINDOW_HOURS = 2


def _parse_iso8601(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _fresh_recent_failures(data: dict) -> list[dict]:
    """Return recentFailed rows that fall inside the API's requested window.

    The endpoint includes ``since`` in its response but does not currently use
    that value to constrain ``recentFailed``. Rows with an unparseable timestamp
    are retained conservatively so malformed metadata cannot hide a real fault.
    """
    recent_failed = data.get("recentFailed") or []
    since = _parse_iso8601(data.get("since"))
    if since is None:
        return recent_failed

    fresh: list[dict] = []
    for failure in recent_failed:
        updated_at = _parse_iso8601(failure.get("updatedAt"))
        if updated_at is None or updated_at >= since:
            fresh.append(failure)
    return fresh


def hostbuf_failure_count(data: dict) -> int:
    """Return the number of fresh failures carrying the hostbuf signature."""
    recent_failed = data.get("recentFailed") or []
    if _parse_iso8601(data.get("since")) is not None:
        groups = group_failures_by_signature(_fresh_recent_failures(data))
    else:
        # Preserve the old fallback for callers/tests that provide no window
        # metadata. Live queue stats always include ``since``.
        groups = data.get("failuresBySignature") or group_failures_by_signature(recent_failed)

    return sum(
        int(group.get("count") or 0)
        for group in groups
        if group.get("signature") == HOSTBUF_SIGNATURE
    )


def main() -> int:
    try:
        data = fetch_queue_stats(window_hours=SENTINEL_WINDOW_HOURS, timeout=20.0)
    except RuntimeError as exc:
        print(f"ERROR: unable to read render queue stats: {exc}", file=sys.stderr)
        return 1

    count = hostbuf_failure_count(data)
    if count:
        print(
            "ERROR: recurring render-box hardware fault detected: "
            f"{count} ArtJob failure(s) within the last {SENTINEL_WINDOW_HOURS}h "
            "match hostbuf_file_reader_read failed. "
            "Inspect the Alexandria/render-box storage path before retrying affected jobs.",
            file=sys.stderr,
        )
        return 2

    print(
        "OK: no fresh hostbuf_file_reader_read failures within the last "
        f"{SENTINEL_WINDOW_HOURS}h."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
