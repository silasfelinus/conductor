#!/usr/bin/env python3
"""Fail loudly when the known ComfyUI host-buffer read fault is present.

This is a narrow standing sentinel for the recurring
``hostbuf_file_reader_read failed`` CLIPTextEncode failure.  It deliberately
uses the same queue/stats source and signature classifier as
``recheck_render_queue.py`` so alerting and the render backlog cannot disagree
about what constitutes the hardware-fault signature.

Exit codes:
  0: no hostbuf failure is present in recentFailed
  1: queue stats could not be read
  2: one or more recent failures match the hostbuf signature
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from consume_art_queue_core import fetch_queue_stats  # noqa: E402
from recheck_render_queue import group_failures_by_signature  # noqa: E402

HOSTBUF_SIGNATURE = "hostbuf-file-reader-read"


def hostbuf_failure_count(data: dict) -> int:
    """Return the number of recent failures carrying the hostbuf signature."""
    recent_failed = data.get("recentFailed") or []
    groups = data.get("failuresBySignature") or group_failures_by_signature(recent_failed)
    return sum(
        int(group.get("count") or 0)
        for group in groups
        if group.get("signature") == HOSTBUF_SIGNATURE
    )


def main() -> int:
    try:
        data = fetch_queue_stats(window_hours=24, timeout=20.0)
    except RuntimeError as exc:
        print(f"ERROR: unable to read render queue stats: {exc}", file=sys.stderr)
        return 1

    count = hostbuf_failure_count(data)
    if count:
        print(
            "ERROR: recurring render-box hardware fault detected: "
            f"{count} recent ArtJob failure(s) match hostbuf_file_reader_read failed. "
            "Inspect the Alexandria/render-box storage path before retrying affected jobs.",
            file=sys.stderr,
        )
        return 2

    print("OK: no hostbuf_file_reader_read failures in recentFailed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
