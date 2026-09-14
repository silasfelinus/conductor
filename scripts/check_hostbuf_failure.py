#!/usr/bin/env python3
"""Track the known ComfyUI host-buffer read fault through recovery.

The queue stats endpoint exposes the latest hostbuf failure and latest DONE
completion timestamps. A hostbuf incident is only considered recovered when a
successful render completed *after* that failure. This prevents an idle or
still-broken renderer from becoming a false green merely because the original
failure aged out of a time window.

For compatibility with an older Kind Robots deployment that does not expose the
recovery timestamps yet, the sentinel falls back to the two-hour filtered
recentFailed sample.

Exit codes:
  0: clear, recovered, or stale-but-unverified (warning only)
  1: queue stats could not be read
  2: a fresh unresolved hostbuf failure is present
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
    """Return recentFailed rows that fall inside the API's requested window."""
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
        groups = data.get("failuresBySignature") or group_failures_by_signature(recent_failed)

    return sum(
        int(group.get("count") or 0)
        for group in groups
        if group.get("signature") == HOSTBUF_SIGNATURE
    )


def hostbuf_state(data: dict, *, now: datetime | None = None) -> str:
    """Return clear, recovered, fresh-failure, or unverified.

    ``unverified`` means a hostbuf failure is known, it is older than the alert
    window, and no successful render has completed after it. That state exits
    successfully to avoid hourly duplicate mail, but is deliberately reported
    as a warning rather than healthy.
    """
    failure_at = _parse_iso8601(data.get("latestHostbufFailureAt"))
    done_at = _parse_iso8601(data.get("latestDoneAt"))

    # Older Kind Robots deployments do not expose these additive fields yet.
    if failure_at is None:
        return "fresh-failure" if hostbuf_failure_count(data) else "clear"

    if done_at is not None and done_at > failure_at:
        return "recovered"

    current = now or datetime.now(timezone.utc)
    age_hours = max(0.0, (current - failure_at).total_seconds() / 3600)
    if age_hours <= SENTINEL_WINDOW_HOURS:
        return "fresh-failure"
    return "unverified"


def main() -> int:
    try:
        data = fetch_queue_stats(window_hours=SENTINEL_WINDOW_HOURS, timeout=20.0)
    except RuntimeError as exc:
        print(f"ERROR: unable to read render queue stats: {exc}", file=sys.stderr)
        return 1

    state = hostbuf_state(data)
    failure_at = data.get("latestHostbufFailureAt")
    done_at = data.get("latestDoneAt")

    if state == "fresh-failure":
        count = hostbuf_failure_count(data)
        count_text = f"{count} fresh ArtJob failure(s)" if count else "a fresh hostbuf incident"
        print(
            "ERROR: recurring render-box hardware fault detected: "
            f"{count_text} match hostbuf_file_reader_read failed. "
            f"Latest hostbuf failure: {failure_at or 'within the requested 2h sample'}. "
            "A successful render has not completed after it. "
            "Inspect the render-box model/storage path before retrying affected jobs.",
            file=sys.stderr,
        )
        return 2

    if state == "unverified":
        print(
            "::warning::UNVERIFIED render recovery: the latest hostbuf failure "
            f"({failure_at}) is older than {SENTINEL_WINDOW_HOURS}h, but no successful "
            "render has completed after it. Suppressing duplicate hourly failure mail; "
            "do not treat the renderer as healthy until a render completes."
        )
        return 0

    if state == "recovered":
        print(
            "OK: render recovery verified. A successful render completed after the "
            f"latest hostbuf failure ({failure_at}); latest DONE: {done_at}."
        )
        return 0

    print(
        "OK: no fresh hostbuf_file_reader_read failure is present in the available "
        "queue diagnostics."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
