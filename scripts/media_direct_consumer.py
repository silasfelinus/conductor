#!/usr/bin/env python3
"""Shared patches for ArtJob consumers that use direct self-hosted media writes.

The existing consumers remain the source of truth for queueing, polling, and
status updates. This module only adds the logical destination to each ArtJob
payload and avoids downloading a second copy into projects/process/ after the
home relay has successfully written a Kind Robots target to the media share.
"""

from pathlib import Path

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
CONDUCTOR_REPO = "silasfelinus/conductor"


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
            relative = Path(_image_path(entry)).relative_to("public/images")
            virtual_path = consumer.ROOT / ".media-direct" / relative
            return virtual_path, "home relay wrote directly to self-hosted media"
        return original_save_result(entry, image_b64)

    consumer.entry_to_job = entry_to_job
    consumer.save_result = save_result
    return consumer
