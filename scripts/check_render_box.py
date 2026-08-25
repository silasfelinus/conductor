#!/usr/bin/env python3
"""check_render_box.py — is the self-hosted render/media box reachable?

The art pipeline renders on a home ComfyUI/A1111 box and writes results to
self-hosted media (media.acrocatranch.com). When that box is offline the
consumers can't tell the difference between "nothing to do" and "everything is
stuck waiting on a dead box" -- they just time out silently (auto-art-generate
marks the step continue-on-error, so a dead box is an invisible no-op).

This is the visibility probe: one cheap HTTP request at the media origin. If the
host answers with ANY status (even 404/403), it is up and reachable -- we only
treat connection failures / timeouts as "down". Exit 0 = up, 1 = down, and print
a one-line human-readable verdict either way.

Used by auto-art-generate.yml to gate the drain steps: skip generation cleanly
(and say so loudly) when the box is down, instead of draining the whole queue
into per-job timeouts.

An HTTP probe alone is not enough, and 2026-08-25 is the proof: the render box's
SMB model share (alexandria) stopped authenticating, so ComfyUI could not read a
single model file for ~15 hours -- while media.acrocatranch.com kept answering
HTTP 404 at its root, this gate kept reporting UP, and auto-art-generate kept
enqueuing. The FAILED backlog grew from 420 to 448 during the incident review
itself. A web origin answering says nothing about whether the box can render.

So the probe now has two parts: the cheap HTTP reachability check, then a look at
what the pipeline has actually *produced* lately (GET /api/art/queue/stats). The
second one is deliberately conservative -- it only reports DOWN on positive
evidence of sustained failure (failures piling up with nothing completing), and
falls back to the HTTP verdict whenever the queue is merely idle or the stats
call is unavailable. An idle queue is not a broken box.

Env: KR_MEDIA_ORIGIN (default https://media.acrocatranch.com),
KR_BASE_URL/KR_API_TOKEN for the throughput check (skipped without a token).
"""

import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from media_direct_consumer import MEDIA_ORIGIN  # noqa: E402

PROBE_TIMEOUT_SECONDS = 10

# How many failures in the window count as "sustained" rather than a one-off.
# Below this, a couple of failed jobs against an otherwise-idle queue is not
# enough to stop the pipeline.
SUSTAINED_FAILURE_COUNT = 5
THROUGHPUT_WINDOW_HOURS = 6


def render_box_reachable(origin=MEDIA_ORIGIN, timeout=PROBE_TIMEOUT_SECONDS):
    """True if the media origin answers at all (any HTTP status)."""
    request = urllib.request.Request(origin, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return True, response.status
    except urllib.error.HTTPError as exc:
        # The host answered -- it's up, just not 2xx at the root. That's fine.
        return True, exc.code
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return False, str(getattr(exc, "reason", exc))


def render_throughput_verdict(throughput):
    """(healthy, reason) from a queue stats `windowThroughput` block.

    `healthy` is None for "no opinion" -- an idle queue, or a stats payload we
    could not read. Only a window with failures piling up and nothing completing
    is treated as a broken box, because that is the one pattern an HTTP probe
    provably cannot see (2026-08-25: the media origin answered all day while the
    model share was unauthenticated).
    """
    if not isinstance(throughput, dict):
        return None, "no throughput data"
    done = throughput.get("DONE") or 0
    failed = throughput.get("FAILED") or 0
    if done:
        return True, f"{done} render(s) completed in the last {THROUGHPUT_WINDOW_HOURS}h"
    if failed >= SUSTAINED_FAILURE_COUNT:
        return False, (
            f"{failed} render(s) failed and none completed in the last "
            f"{THROUGHPUT_WINDOW_HOURS}h"
        )
    return None, "queue idle"


def fetch_throughput():
    """`windowThroughput` from the queue stats endpoint, or None."""
    try:
        import consume_art_queue as consumer
    except ImportError:
        return None
    if not consumer.KR_API_TOKEN:
        return None
    try:
        status, response = consumer.http_json(
            "GET",
            f"{consumer.KR_BASE_URL}/api/art/queue/stats"
            f"?window={THROUGHPUT_WINDOW_HOURS}",
        )
    except Exception:  # noqa: BLE001 - a probe must never raise
        return None
    if status != 200 or not response or not response.get("success"):
        return None
    return (response.get("data") or {}).get("windowThroughput")


def main():
    up, detail = render_box_reachable()
    if not up:
        print(
            f"render box DOWN: {MEDIA_ORIGIN} unreachable ({detail}).",
            file=sys.stderr,
        )
        return 1

    healthy, reason = render_throughput_verdict(fetch_throughput())
    if healthy is False:
        print(
            f"render box DOWN: {MEDIA_ORIGIN} answers (HTTP {detail}), but the "
            f"pipeline is not rendering — {reason}. Reaching the media origin "
            "does not mean the box can read its models; skipping the drain "
            "rather than adding to the backlog.",
            file=sys.stderr,
        )
        return 1

    print(f"render box UP: {MEDIA_ORIGIN} answered (HTTP {detail}); {reason}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
