"""Ensure Conductor's clip batch size matches the Kind Robots API route."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "kind_robots"
ROUTE = APP / "server/api/music-video/[id]/scenes/clips.post.ts"
SCRIPT = ROOT / "scripts/build_music_video.py"


def test_clip_batch_limit_matches_kind_robots_route():
    if not APP.is_dir():
        pytest.skip("kind_robots checkout not available")
    assert ROUTE.is_file(), "kind_robots clips route missing"

    route = re.findall(
        r"(?m)^const MAX_CLIPS_PER_CALL = (\d+)$",
        ROUTE.read_text(encoding="utf-8"),
    )
    script = re.findall(
        r"(?m)^MAX_CLIPS_PER_CALL = (\d+)$",
        SCRIPT.read_text(encoding="utf-8"),
    )
    assert len(route) == len(script) == 1
    assert int(route[0]) == int(script[0])
