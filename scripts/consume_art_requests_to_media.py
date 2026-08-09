#!/usr/bin/env python3
"""Run ad-hoc art requests with direct Kind Robots media destinations.

The durable request ledger is intentionally broad: missing-image repair, project art,
voice requests, and Daily Dream art all share ``projects/art-prompts.yaml``.  The
Kind Robots ArtJob queue has its own priority scheduler, but that scheduler cannot
help a request that has not been submitted yet.  Keep the media consumer's staging
order aligned with the eventual ArtJob priority so time-sensitive Daily Dream work
cannot sit behind older generic repair requests before it reaches Kind Robots.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import consume_art_queue as consumer  # noqa: E402
from media_direct_consumer import (  # noqa: E402
    KIND_ROBOTS_REPO,
    _is_kindrobots_media_target,
    _media_exists,
    _image_path,
    patch_consumer,
)

patch_consumer(consumer, default_target_repo=KIND_ROBOTS_REPO)

import consume_art_requests as requests  # noqa: E402

original_already_satisfied = requests.already_satisfied
original_load_requests = requests.load_requests


def already_satisfied(entry):
    if _is_kindrobots_media_target(entry, KIND_ROBOTS_REPO):
        return _media_exists(_image_path(entry, KIND_ROBOTS_REPO))
    return original_already_satisfied(entry)


def submission_priority(entry):
    """Return the pre-ArtJob scheduling priority for one staged request.

    Canonical Daily Dream requests get the same reserved tier used once they are
    converted into ArtJobs. Other callers may opt into an explicit numeric
    priority; ordinary repair/filler work stays at zero. ``sorted`` is stable,
    so FIFO order is preserved inside each priority tier.
    """
    if str(entry.get("source") or "").strip().lower() == "dream-cycle":
        return consumer.DAILY_DREAM_PRIORITY
    try:
        return int(entry.get("priority") or 0)
    except (TypeError, ValueError):
        return 0


def prioritized_load_requests():
    return sorted(original_load_requests(), key=submission_priority, reverse=True)


requests.already_satisfied = already_satisfied
requests.load_requests = prioritized_load_requests


if __name__ == "__main__":
    sys.exit(requests.main())
