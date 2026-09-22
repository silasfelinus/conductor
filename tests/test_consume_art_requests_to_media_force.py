"""conductor/t-192: the actual production entrypoint for the choirfish bug.

auto-art-generate.yml calls consume_art_requests_to_media.py, not
consume_art_requests.py directly. For a kind_robots media target, its
already_satisfied() override bypasses original_already_satisfied() (and so
regeneration_forced()) entirely, going straight to a HEAD check against the
live media host instead -- so the force: true fix has to be verified at this
wrapper too, not just in the underlying module.

Loaded via importlib (mirrors tests/test_media_direct.py's
load_relay_media_module) under fresh sys.modules entries so this doesn't
share module OBJECTS with the rest of the suite -- but consume_art_queue.py
ends with `sys.modules[__name__] = _core`, aliasing itself to the shared
scripts.consume_art_queue_core singleton, so patch_consumer()'s
entry_to_job/save_result reassignment still lands on that one shared object
no matter which name it was imported under. The fixture snapshots and
restores those two attributes explicitly for exactly that reason.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

import scripts.consume_art_queue as _shared_core

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"


@pytest.fixture()
def to_media_module():
    original_entry_to_job = _shared_core.entry_to_job
    original_save_result = _shared_core.save_result

    sys.path.insert(0, str(SCRIPTS_DIR))
    for name in (
        "consume_art_queue",
        "consume_art_requests",
        "media_direct_consumer",
        "art_request_staging_priority",
        "consume_art_requests_to_media",
    ):
        sys.modules.pop(name, None)

    spec = importlib.util.spec_from_file_location(
        "consume_art_requests_to_media", SCRIPTS_DIR / "consume_art_requests_to_media.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    try:
        yield module
    finally:
        _shared_core.entry_to_job = original_entry_to_job
        _shared_core.save_result = original_save_result
        sys.path.remove(str(SCRIPTS_DIR))
        for name in (
            "consume_art_queue",
            "consume_art_requests",
            "media_direct_consumer",
            "art_request_staging_priority",
            "consume_art_requests_to_media",
        ):
            sys.modules.pop(name, None)


def test_forced_entry_never_reaches_the_media_host_check(to_media_module, monkeypatch):
    """The exact ruler-hooked/t-019 choirfish shape: a kind_robots media
    target whose file (here, on the live media host) already exists from the
    rejected render. force: true must short-circuit before the HEAD check
    that would otherwise report it satisfied."""

    def boom(image_path):
        raise AssertionError("must not HEAD-check the media host for a forced entry")

    monkeypatch.setattr(to_media_module, "_media_exists", boom)

    entry = {
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/ruler-hooked/fish/choirfish.webp",
        "force": True,
    }
    assert to_media_module.already_satisfied(entry) is False


def test_unforced_kindrobots_media_target_still_checks_the_media_host(
    to_media_module, monkeypatch
):
    """The fix must not disable the media-host check for ordinary entries."""
    calls = []

    def fake_media_exists(image_path):
        calls.append(image_path)
        return True

    monkeypatch.setattr(to_media_module, "_media_exists", fake_media_exists)

    entry = {
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/ruler-hooked/fish/choirfish.webp",
    }
    assert to_media_module.already_satisfied(entry) is True
    assert calls == ["public/images/ruler-hooked/fish/choirfish.webp"]
