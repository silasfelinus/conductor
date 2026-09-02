#!/usr/bin/env python3
"""check_render_box.py — is the self-hosted render/media box reachable?

The art pipeline renders on a home ComfyUI box and writes results to
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

`render_throughput_verdict` used to short-circuit on `if done: return True` --
ANY completion inside the window was treated as proof of health, no matter how
long ago it happened or what the queue looks like right now. Observed
2026-08-26 during the ruler-hooked art batch (conductor PRs #2945/#2947): 40
ArtJobs submitted into a queue that had been genuinely empty, the first job
claimed by the relay and then stuck RUNNING with no movement for 35+ minutes,
nothing else started -- while the probe kept reporting UP on the strength of
completions that all predated the batch. The stats payload already carries the
signal that distinguishes this from "healthy" or "merely idle" and it was being
ignored: `staleRunningCount` (a RUNNING job whose claim is older than
kind_robots' STALE_CLAIM_MINUTES, see server/api/art/queue/stats.get.ts) and
`queueDepth.PENDING`. A stale claim with pending work behind it is a stalled
queue regardless of what finished earlier in the window, so that check now
runs before the "any completion is healthy" shortcut, not after it.

Env: KR_MEDIA_ORIGIN (default https://media.acrocatranch.com),
KR_BASE_URL/KR_API_TOKEN for the throughput check (skipped without a token).
"""

import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
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


def render_throughput_verdict(data):
    """(healthy, reason) from the full ArtJob queue stats `data` block.

    `healthy` is None for "no opinion" -- an idle queue, or a stats payload we
    could not read. Two independent patterns are treated as positive evidence
    of a broken box, checked in this order:

    1. A stale RUNNING claim with PENDING work still behind it
       (`staleRunningCount > 0` and `queueDepth.PENDING > 0`). This must be
       checked before the "any completion is healthy" shortcut below, not
       after -- a completion earlier in the window does not mean the box is
       rendering *now* (2026-08-26: 40 ArtJobs submitted into an empty queue,
       the first stuck RUNNING for 35+ minutes with nothing else started,
       while stale completions from before the batch kept this reporting UP).
    2. Failures piling up with nothing completing at all in the window
       (2026-08-25: the media origin answered all day while the model share
       was unauthenticated, so completions and stale claims were both zero and
       only the failure count moved).
    """
    if not isinstance(data, dict):
        return None, "no throughput data"
    throughput = data.get("windowThroughput")
    throughput = throughput if isinstance(throughput, dict) else {}
    done = throughput.get("DONE") or 0
    failed = throughput.get("FAILED") or 0

    stale_running = data.get("staleRunningCount") or 0
    queue_depth = data.get("queueDepth")
    pending = queue_depth.get("PENDING") or 0 if isinstance(queue_depth, dict) else 0

    if stale_running > 0 and pending > 0:
        return False, (
            f"{stale_running} stale RUNNING claim(s) with {pending} PENDING job(s) "
            f"still waiting and nothing else moving -- the queue is stalled, not idle"
        )
    if done:
        return True, f"{done} render(s) completed in the last {THROUGHPUT_WINDOW_HOURS}h"
    if failed >= SUSTAINED_FAILURE_COUNT:
        return False, (
            f"{failed} render(s) failed and none completed in the last "
            f"{THROUGHPUT_WINDOW_HOURS}h"
        )
    return None, "queue idle"


def fetch_queue_stats():
    """The full queue stats `data` block, or None.

    Delegates to consume_art_queue_core's shared fetch_queue_stats (conductor/
    t-131) -- this is the "must never raise" probe side of that helper, so any
    failure (missing token, unreachable, bad payload) just means "no opinion"
    rather than a hard stop.
    """
    try:
        import consume_art_queue as consumer
    except ImportError:
        return None
    try:
        return consumer.fetch_queue_stats(window_hours=THROUGHPUT_WINDOW_HOURS)
    except Exception:  # noqa: BLE001 - a probe must never raise
        return None


def engine_heartbeat_verdict():
    """(healthy, reason) from the relay's own heartbeat. None = no opinion.

    Checked BEFORE the throughput heuristics below, for the same reason the
    stale-claim check runs before the "any completion is healthy" shortcut: it
    is the most CURRENT signal available, and the ones underneath it are all
    backward-looking.

    Two holes this closes, both seen on 2026-09-02:

    * `return None, "queue idle"` — a drained queue produced no opinion and
      main() printed "render box UP". ops/home-server/RENDER-BOX-STATUS read
      `up` through the entire 24-hour outage, so the state-change email in
      auto-art-generate.yml never had a change to fire on.
    * `if done: return True` — any completion in the six-hour window counts as
      health. A box that died two hours ago still looks healthy on the strength
      of what it finished five hours ago.

    The heartbeat has neither problem: kr-relay posts it every 60 seconds and
    it says nothing about the queue, so it answers "is the engine alive NOW"
    regardless of whether there is any work to do. Absent a token it returns no
    opinion, leaving the old behaviour exactly as it was.
    """
    try:
        import check_engine_heartbeat as engine

        data = engine.fetch_uptime()
        state, reason = engine.assess(data, datetime.now(timezone.utc))
    except Exception:  # noqa: BLE001 - a probe must never raise
        return None, "engine heartbeat unavailable"

    if state in (engine.SILENT, engine.DOWN):
        return False, reason
    if state == engine.OK:
        return True, reason
    return None, reason


def main():
    up, detail = render_box_reachable()
    if not up:
        print(
            f"render box DOWN: {MEDIA_ORIGIN} unreachable ({detail}).",
            file=sys.stderr,
        )
        return 1

    beat_healthy, beat_reason = engine_heartbeat_verdict()
    if beat_healthy is False:
        print(
            f"render box DOWN: {MEDIA_ORIGIN} answers (HTTP {detail}), but the "
            f"render engine is not reporting healthy — {beat_reason}. An idle "
            "queue is not proof of a working box; skipping the drain.",
            file=sys.stderr,
        )
        return 1

    healthy, reason = render_throughput_verdict(fetch_queue_stats())
    if healthy is False:
        print(
            f"render box DOWN: {MEDIA_ORIGIN} answers (HTTP {detail}), but the "
            f"pipeline is not rendering — {reason}. Reaching the media origin "
            "does not mean the box can read its models; skipping the drain "
            "rather than adding to the backlog.",
            file=sys.stderr,
        )
        return 1

    beat_note = f" Engine heartbeat: {beat_reason}." if beat_reason else ""
    print(f"render box UP: {MEDIA_ORIGIN} answered (HTTP {detail}); {reason}.{beat_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
