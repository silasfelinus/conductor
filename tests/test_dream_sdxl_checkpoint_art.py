"""Zuzu extra art renders on real source-backed checkpoints, not Krea."""
from copy import deepcopy

import pytest

from scripts import consume_art_queue as queue
from scripts import consume_art_queue_core as core
from scripts.dream_sdxl_checkpoint_art import (
    CHECKPOINT_LANES, ENGINE, ILLUSTRIOUS_PREFIX, ZUZU_CANON_TAGS, compose_checkpoint_prompt,
    make_checkpoint_job, resolve_registered_checkpoint, sdxl_render_size,
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
    with pytest.raises(RuntimeError, match="conflicts with Resource registry"):
        resolve_registered_checkpoint("arthemy", bad_catalog)


def test_invalid_family_and_project_are_rejected_before_any_queueing(monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    with pytest.raises(ValueError, match="known project_target"):
        queue.entry_to_job(_entry(project_target="not-a-project"))
    with pytest.raises(ValueError, match="unsupported checkpoint family"):
        queue.entry_to_job(_entry("krea"))


def test_existing_original_dream_requests_keep_the_old_engine(monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: {})
    monkeypatch.setattr(core, "resolve_seed", lambda *_: 123456)
    original = {
        "source": "dream-cycle",
        "id": "dream-cycle-test-world",
        "target_repo": "silasfelinus/kind_robots",
        "prompt": "an independent daydream about an inverted city",
        "size": "512x768",
    }
    job = queue.entry_to_job(original)
    assert job["projectSlug"] == "dream-cycle"
    assert "CheckpointLoaderSimple" not in {
        node.get("class_type") for node in job["payload"]["workflow"].values()
    }
    assert job["idempotencyKey"] == original["id"]


@pytest.mark.parametrize("family", ["corporate-noir", "western-cartoon"])
def test_shifting_desks_illustrious_jobs_keep_style_and_destination(family, monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    monkeypatch.setattr(core, "resolve_seed", lambda *_: 987654)
    request = _entry(
        family,
        source="shifting-desks",
        id=f"shifting-desks-art-{family}-gus-shop-steward",
        project_target="shifting-desks",
        image_path=f"public/images/shifting-desks/styles/{family}/cards/orientation/gus-shop-steward.webp",
        project_slug="shifting-desks",
        priority=10,
    )
    job = queue.entry_to_job(request)
    assert job["engine"] == "COMFY"
    assert job["projectSlug"] == "shifting-desks"
    assert job["idempotencyKey"] == request["id"]
    assert job["priority"] == 10
    assert job["payload"]["imagePath"] == request["image_path"]
    assert job["payload"]["collection"] == "shifting-desks"
    assert job["payload"]["resources"]["checkpointName"] == "Illustrious/arthemyWesternArt_v30.safetensors"
    assert job["payload"]["workflow"]["8"]["inputs"]["stop_at_clip_layer"] == -2
    assert job["payload"]["workflow"]["5"]["inputs"]["seed"] == 987654
    assert job["payload"]["workflow"]["7"]["inputs"]["filename_prefix"] == f"shifting_desks_{family}"
    assert "western animated feature" in job["payload"]["promptString"] if family == "western-cartoon" else "dramatic graphic novel" in job["payload"]["promptString"]


def test_shifting_desks_cannot_use_rejected_or_unregistered_checkpoint(monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    with pytest.raises(ValueError, match="reserved for its own project"):
        queue.entry_to_job(_entry("illustrious", project_target="shifting-desks"))
    with pytest.raises(ValueError, match="reserved for its own project"):
        queue.entry_to_job(_entry("western-cartoon", project_target="zuzu-gamebook"))


@pytest.mark.parametrize("family", ["corporate-noir", "western-cartoon"])
def test_shifting_desks_pinned_arhemy_survives_filtered_gallery(monkeypatch, family):
    # /api/resources is filtered by owner, publicity and maturity. A house
    # checkpoint whose public gallery row is hidden still has a known Comfy path.
    monkeypatch.setattr(core, "_load_resource_index", lambda: {"CHECKPOINT": {}})
    monkeypatch.setattr(core, "resolve_seed", lambda *_: 333)
    job = queue.entry_to_job(_entry(family, project_target="shifting-desks", source="shifting-desks"))
    assert job["payload"]["workflow"]["1"]["inputs"]["ckpt_name"] == (
        "Illustrious/arthemyWesternArt_v30.safetensors"
    )


def test_shifting_desks_rejects_conflicting_catalog_record():
    with pytest.raises(RuntimeError, match="conflicts with Resource registry"):
        resolve_registered_checkpoint(
            "western-cartoon",
            {"CHECKPOINT": {"arthemywesternart_v30.safetensors": "SDXL/something-else.safetensors"}},
        )


# The 2026-10-17 Bloomrig Jubilee Zuzu prompts, verbatim in the parts that
# went wrong (Silas, 2026-10-18).
FARRIER = (
    "Ash, Brass and the Last Hundred Days palette: a roadside forge, a grey-muzzled badger smith "
    "at an anvil, set in the world of Emperor of Dust, a post-human shrine where people gather, "
    + CHECKPOINT_LANES["illustrious"]["style"] + ", every surface bare and unmarked"
)
ORCHARD = (
    "an orchard of glass trees, a koala samurai traveller in a straw hat and travel cloak reaching up, "
    "Zuzu hums a nonsense tune, " + CHECKPOINT_LANES["arthemy"]["style"]
)


@pytest.mark.parametrize("family,project,prompt", [
    ("illustrious", "emperor-of-dust", FARRIER),
    ("arthemy", "zuzu-gamebook", ORCHARD),
])
def test_zuzu_prompt_leads_with_quality_and_style_exactly_once(family, project, prompt, monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    job = make_checkpoint_job(_entry(family, project_target=project, prompt=prompt), core)
    positive = job["payload"]["promptString"]
    style = CHECKPOINT_LANES[family]["style"]
    assert positive.startswith(ILLUSTRIOUS_PREFIX + ", " + style)
    assert positive.count(style) == 1
    assert job["payload"]["workflow"]["2"]["inputs"]["text"] == positive


def test_sd15_card_size_renders_at_native_sdxl_bucket(monkeypatch):
    monkeypatch.setattr(core, "_load_resource_index", lambda: deepcopy(CATALOG))
    job = make_checkpoint_job(_entry(), core)
    assert (job["payload"]["width"], job["payload"]["height"]) == (832, 1216)
    latent = job["payload"]["workflow"]["4"]["inputs"]
    assert (latent["width"], latent["height"]) == (832, 1216)
    assert sdxl_render_size(1216, 832) == (1216, 832)
    assert sdxl_render_size(512, 512) == (1024, 1024)


def test_literal_words_and_banned_terms_are_rewritten_for_zuzu_world():
    positive, negative = compose_checkpoint_prompt(FARRIER, "illustrious", "emperor-of-dust")
    assert "grey-snouted badger" in positive
    for word in ("muzzle", "post-human", "people", " human"):
        assert word not in positive
    assert "townsfolk" in positive and "human" in negative


def test_zuzu_in_frame_gets_canon_tags_costume_and_negatives():
    positive, negative = compose_checkpoint_prompt(ORCHARD, "arthemy", "zuzu-gamebook")
    assert ZUZU_CANON_TAGS in positive
    assert "straw hat" not in positive and "cloak" not in positive
    assert "conical straw kasa" in positive and "poncho" in positive
    for tag in ("straw boater", "cloak", "cape", "lanky"):
        assert tag in negative
    # A Zuzu-world asset with no koala in it keeps the generic Zuzu negatives only.
    _, plain = compose_checkpoint_prompt("a heron courier", "arthemy", "zuzu-gamebook")
    assert "lanky" not in plain and "human" in plain


def test_shifting_desks_prompt_and_negative_are_unchanged_apart_from_dedup():
    style = CHECKPOINT_LANES["western-cartoon"]["style"]
    positive, negative = compose_checkpoint_prompt("Gus at the shop desk, people waiting", "western-cartoon", "shifting-desks")
    assert positive == f"{style}, Gus at the shop desk, people waiting"
    assert negative == "low quality, blurry, bad anatomy, disfigured, writing, text, watermark"
