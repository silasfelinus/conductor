#!/usr/bin/env python3
"""Run ad-hoc art requests with direct Kind Robots media destinations."""

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


def already_satisfied(entry):
    if _is_kindrobots_media_target(entry, KIND_ROBOTS_REPO):
        return _media_exists(_image_path(entry))
    return original_already_satisfied(entry)


requests.already_satisfied = already_satisfied


if __name__ == "__main__":
    sys.exit(requests.main())
