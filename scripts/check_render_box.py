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

Env: KR_MEDIA_ORIGIN (default https://media.acrocatranch.com).
"""

import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from media_direct_consumer import MEDIA_ORIGIN  # noqa: E402

PROBE_TIMEOUT_SECONDS = 10


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


def main():
    up, detail = render_box_reachable()
    if up:
        print(f"render box UP: {MEDIA_ORIGIN} answered (HTTP {detail}).")
        return 0
    print(f"render box DOWN: {MEDIA_ORIGIN} unreachable ({detail}).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
