#!/usr/bin/env python3
"""Run the project-art consumer with direct Kind Robots media destinations."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import consume_art_queue as consumer  # noqa: E402
from media_direct_consumer import CONDUCTOR_REPO, patch_consumer  # noqa: E402

patch_consumer(consumer, default_target_repo=CONDUCTOR_REPO)


if __name__ == "__main__":
    sys.exit(consumer.main())
