#!/usr/bin/env python3
"""Shared patches for ArtJob consumers that use direct self-hosted media writes.

The existing consumers remain the source of truth for queueing, polling, and
status updates. This module only adds the logical destination to each ArtJob
payload and avoids downloading a second copy into projects/process/ after the
home relay has successfully written a Kind Robots target to the media share.
"""

import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
CONDUCTOR_REPO = "silasfelinus/conductor"
MEDIA_ORIGIN = os.environ.get(
    "KR_MEDIA_ORIGIN", "https://media.acrocatranch.com"
).rstrip("/")

# A HEAD existence check against a static file host, not a render wait -- keep
# this short. consume_art_requests.py calls already_satisfied() once per
# pending request (unbounded by --limit, since satisfied requests self-drain
# regardless of this run's batch size), so a slow or unreachable media host
# multiplies straight into the workflow step's total wall time. 30s per call
# against a backlog of 100+ requests was enough on its own to blow well past
# the step's intended --timeout-bounded runtime (conductor art-generator-
# connect/t-022).
MEDIA_EXISTS_TIMEOUT_SECONDS = 8


def _target_repo(entry, default_target_repo):
    return str(entry.get("target_repo") or default_target_repo).strip()


def _image_path(entry):
    return str(entry.get("image_path") or "").strip()


def _is_kindrobots_media_target(entry, default_target_repo):
    image_path = _image_path(entry)
    return (
        _target_repo(entry, default_target_repo) == KIND_ROBOTS_REPO
        and image_path.startswith("public/images/")
    )


def _media_url(image_path):
    public_relative = Path(image_path).relative_to("public").as_posix()
    return f"{MEDIA_ORIGIN}/{urllib.parse.quote(public_relative, safe='/')}"


def _media_exists(image_path):
    request = urllib.request.Request(_media_url(image_path), method="HEAD")
    try:
        with urllib.request.urlopen(
            request, timeout=MEDIA_EXISTS_TIMEOUT_SECONDS
        ) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def patch_consumer(consumer, default_target_repo):
    """Patch one imported consume_art_queue module in place.

    `default_target_repo` differs by lane: the project-art batch defaults to
    conductor, while ad-hoc requests historically default to kind_robots.
    """

    original_entry_to_job = consumer.entry_to_job
    original_save_result = consumer.save_result

    def entry_to_job(entry):
        job = original_entry_to_job(entry)
        payload = job.setdefault("payload", {})
        payload["targetRepo"] = _target_repo(entry, default_target_repo)
        payload["imagePath"] = _image_path(entry)
        return job

    def save_result(entry, image_b64):
        if _is_kindrobots_media_target(entry, default_target_repo):
            image_path = _image_path(entry)
            if _media_exists(image_path):
                relative = Path(image_path).relative_to("public/images")
                virtual_path = consumer.ROOT / ".media-direct" / relative
                return virtual_path, "home relay wrote directly to self-hosted media"

            out, warning = original_save_result(entry, image_b64)
            fallback = (
                "direct media URL did not verify; saved fallback in projects/process"
            )
            return out, f"{fallback}; {warning}" if warning else fallback

        return original_save_result(entry, image_b64)

    consumer.entry_to_job = entry_to_job
    consumer.save_result = save_result
    return consumer
