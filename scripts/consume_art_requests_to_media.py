#!/usr/bin/env python3
"""Run ad-hoc art requests with direct Kind Robots media destinations.

The durable request ledger is intentionally broad: missing-image repair, project art,
voice requests, and Daily Dream art all share ``projects/art-prompts.yaml``. The
Kind Robots ArtJob queue has its own priority scheduler, but that scheduler cannot
help a request that has not been submitted yet. Keep the media consumer's staging
order aligned with the eventual ArtJob priority so time-sensitive Daily Dream work
cannot sit behind older generic repair requests before it reaches Kind Robots.
"""

from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import consume_art_queue as consumer  # noqa: E402
from art_request_staging_priority import (  # noqa: E402
    is_daily_dream_request,
    positive_job_id,
    prioritize_requests,
    should_consume_after_submission,
)
from media_direct_consumer import (  # noqa: E402
    _media_modified_at,
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
    # conductor/t-192: a `force: true` entry must ignore whatever already sits
    # at its destination, live media host included -- the whole point is a
    # stale render (or stale media-host copy) from before the prompt fix must
    # not count as fulfillment. Checked before the kind-robots-media branch,
    # since that branch never reaches original_already_satisfied() (and so
    # never reaches its own regeneration_forced() check) at all.
    if requests.regeneration_forced(entry):
        return forced_render_delivered(entry)
    if _is_kindrobots_media_target(entry, KIND_ROBOTS_REPO):
        return _media_exists(_image_path(entry, KIND_ROBOTS_REPO))
    return original_already_satisfied(entry)


def forced_render_delivered(entry):
    """True once a forced regeneration's own render is live at its path.

    2026-10-16: a forced kind_robots media row never closed. Its stale file
    must not count (t-192), so already_satisfied() returned False forever,
    even after the corrected render landed; 121 Shifting Desks Noir rows and
    the Jam in Tube 14 re-render sat "pending" with DONE ArtJobs. Staging a
    force clears last_art_job_id, so a recorded job is the regeneration's
    own. It is delivered when that job is DONE with an ArtImage and the live
    media file was written after the job was created (the relay writes these
    targets directly); an older file is the stale render and still waits.
    """
    if not _is_kindrobots_media_target(entry, KIND_ROBOTS_REPO):
        return False
    job_id = requests.positive_job_id(entry.get("last_art_job_id"))
    if job_id is None:
        return False
    job = requests.fetch_job(job_id)
    if not job or str(job.get("status") or "").upper() != "DONE":
        return False
    if requests.positive_job_id(job.get("artImageId")) is None:
        return False
    try:
        created = datetime.fromisoformat(
            str(job.get("createdAt") or "").replace("Z", "+00:00")
        )
    except ValueError:
        return False
    modified = _media_modified_at(_image_path(entry, KIND_ROBOTS_REPO))
    return modified is not None and modified >= created


def prioritized_load_requests():
    entries = []
    for entry in original_load_requests():
        # Daily Digest already submitted Daily Dream jobs should not be POSTed
        # again by the broad six-hour consumer. The relay owns them in flight.
        # Once their media path is live, include them again so requests.main()
        # marks the staging rows done during its satisfied pass.
        satisfied = False
        if is_daily_dream_request(entry) and positive_job_id(entry.get("last_art_job_id")):
            satisfied = already_satisfied(entry)
        if should_consume_after_submission(entry, already_satisfied=satisfied):
            entries.append(entry)
    return prioritize_requests(
        entries,
        daily_dream_priority=consumer.DAILY_DREAM_PRIORITY,
    )


requests.already_satisfied = already_satisfied
requests.load_requests = prioritized_load_requests


if __name__ == "__main__":
    sys.exit(requests.main())
