"""Zuzu extra art renders on real source-backed checkpoints, not Krea."""
from copy import deepcopy

import pytest

from scripts import consume_art_queue as queue
from scripts import consume_art_queue_core as core
from scripts.dream_sdxl_checkpoint_art import (
    CHECKPOINT_LANES, ENGINE, make_checkpoint_job, resolve_registered_checkpoint,
)


CATALOG = {"CHECKPOINT": {
    row["checkpoint"].rsplit("/", 1)[-1].lower(): row["checkpoint"]
    for row in CHECKPOINT_LANES.values()
}}


def _entry(family="arthemy", **overrides):
    entry = {
        "source": "dream-cycle",
        "engine": ENGINE,
        "checkpoint_family": family,
        "project_target": "zuzu-gamebook",
        "id": "dream-cycle-test-zuzu-character-1",
        "size": "512x768",
        "prompt": "a fox samurai at an old crossroads",
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/dreams/test/fox-card.webp",
        "entity_type": "character",
        "entity_id": 21,
    }
    return {**entry, **overrides}


@pytest.mark.parametrize("family", ["arthemy", "illustrious"])
def test_artjob_workflow_uses_exact_registered_checkpoint(family, monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    monkeypatch.setattr(core, "resolve_seed", lambda *_: 123456)
    job = queue.entry_to_job(_entry(family, project_target="emperor-of-dust"))
    graph = job["payload"]["workflow"]
    assert job["engine"] == "COMFY"
    assert job["projectSlug"] == "emperor-of-dust"
    assert job["priority"] == queue.DAILY_DREAM_PRIORITY
    assert job["idempotencyKey"] == _entry()["id"]
    assert job["resolvedSeed"] == graph["5"]["inputs"]["seed"] == 123456
    assert graph["1"]["class_type"] == "CheckpointLoaderSimple"
    assert graph["1"]["inputs"]["ckpt_name"] == CHECKPOINT_LANES[family]["checkpoint"]
    assert graph["8"]["inputs"]["stop_at_clip_layer"] == -2
    assert graph["2"]["inputs"]["clip"] == ["8", 0]
    assert graph["3"]["inputs"]["clip"] == ["8", 0]
    assert graph["5"]["inputs"]["sampler_name"] == CHECKPOINT_LANES[family]["sampler"]
    assert job["payload"]["resources"]["checkpointFamily"] == family
    assert job["payload"]["conductorRequest"]["projectTarget"] == "emperor-of-dust"
    assert job["payload"]["entityArt"] == {
        "entityType": "character", "entityId": 21,
        "field": "imagePath", "preserveOriginal": True, "mode": "recreate",
    }
    assert job["payload"]["imagePath"] == "public/images/dreams/test/fox-card.webp"


def test_unregistered_checkpoint_fails_closed_and_does_not_substitute_krea(monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: {"CHECKPOINT": {}})
    with pytest.raises(RuntimeError, match="not confirmed"):
        queue.entry_to_job(_entry("arthemy"))


def test_partial_resource_catalog_mismatch_fails_closed():
    bad_catalog = {"CHECKPOINT": {
        "arthemywesternart_v30.safetensors": "SDXL/another.ckpt",
    }}
    with pytest.raises(RuntimeError, match="not confirmed"):
        resolve_registered_checkpoint("arthemy", bad_catalog)


def test_invalid_family_and_project_are_rejected_before_any_queueing(monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    with pytest.raises(ValueError, match="known project_target"):
        queue.entry_to_job(_entry(project_target="not-a-project"))
    with pytest.raises(ValueError, match="unsupported Zuzu checkpoint family"):
        queue.entry_to_job(_entry("krea"))


def test_existing_original_dream_requests_keep_the_old_engine(monkeypatch):
    monkeypatch.setattr(core, "entry_to_job", lambda e: {
        "engine": "COMFY",
        "projectSlug": None,
        "payload": {"workflow": {"legacy": "preserved"}, "promptString": "dream"},
    })
    original = {
        "source": "dream-cycle",
        "id": "dream-cycle-test-world",
        "target_repo": "silasfelinus/kind_robots",
    }
    job = queue.entry_to_job(original)
    assert job["projectSlug"] == "dream-cycle"
    assert job["payload"]["workflow"] == {"legacy": "preserved"}
    assert job["idempotencyKey"] == original["id"]
