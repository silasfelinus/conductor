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


def _forced_with_job(job_id=4242):
    return {
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/shifting-desks/styles/corporate-noir/departments/orientation.webp",
        "force": True,
        "last_art_job_id": job_id,
    }


def _fake_job(monkeypatch, module, job):
    monkeypatch.setattr(module.requests, "fetch_job", lambda job_id, timeout=20: job)


def test_forced_row_closes_once_its_own_render_is_live(to_media_module, monkeypatch):
    """2026-10-16: the regeneration's DONE job wrote the media after it was
    created, so the forced row is fulfilled and can be marked done."""
    from datetime import datetime, timezone

    _fake_job(monkeypatch, to_media_module, {
        "status": "DONE", "artImageId": 247132, "createdAt": "2026-10-15T01:00:00.000Z",
    })
    monkeypatch.setattr(
        to_media_module, "_media_modified_at",
        lambda path: datetime(2026, 10, 15, 1, 4, tzinfo=timezone.utc),
    )
    assert to_media_module.already_satisfied(_forced_with_job()) is True


def test_forced_row_waits_while_the_media_is_the_stale_render(to_media_module, monkeypatch):
    """A DONE job whose media predates it never delivered: still pending."""
    from datetime import datetime, timezone

    _fake_job(monkeypatch, to_media_module, {
        "status": "DONE", "artImageId": 247132, "createdAt": "2026-10-15T01:00:00.000Z",
    })
    monkeypatch.setattr(
        to_media_module, "_media_modified_at",
        lambda path: datetime(2026, 10, 14, 6, 20, tzinfo=timezone.utc),
    )
    assert to_media_module.already_satisfied(_forced_with_job()) is False


def test_forced_row_with_running_job_never_checks_the_media_host(to_media_module, monkeypatch):
    def boom(path):
        raise AssertionError("must not HEAD-check while the regeneration renders")

    _fake_job(monkeypatch, to_media_module, {"status": "RUNNING", "createdAt": "2026-10-15T01:00:00Z"})
    monkeypatch.setattr(to_media_module, "_media_modified_at", boom)
    assert to_media_module.already_satisfied(_forced_with_job()) is False


def test_forced_row_without_a_recorded_job_stays_pending(to_media_module, monkeypatch):
    def boom(*args, **kwargs):
        raise AssertionError("no job recorded: nothing to look up")

    monkeypatch.setattr(to_media_module.requests, "fetch_job", boom)
    entry = _forced_with_job()
    entry.pop("last_art_job_id")
    assert to_media_module.already_satisfied(entry) is False
