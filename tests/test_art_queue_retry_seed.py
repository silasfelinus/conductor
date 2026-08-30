"""Seed policy for the shared ArtJob queue consumer.

Every submission that does not name its own seed gets a fresh random one.

This file used to assert the opposite: a deterministic seed derived from the
entry's request identity, so re-running the same pending entry rebuilt a
byte-identical payload and the enqueue endpoint's attemptFingerprint dedupe
fired on the repeat. Silas, 2026-08-30: *"we do not want that infrastructure
choice to set deterministic seeds. I see no reason to do it that way. If we
resubmit the same prompt, we should always get a random seed."* The old
behavior meant a prompt could only ever produce one picture — there was no way
to re-roll a render without editing the prompt. Deduplication is carried by
consume_art_requests.has_unresolved_submission (conductor/t-133 + t-136), which
keys on the recorded in-flight job id rather than on payload bytes.
"""

import scripts.consume_art_queue as consumer
import scripts.consume_art_requests as requests


def generic_entry(image_path="projects/images/alpha-hero.webp"):
    return {
        "id": "alpha-hero",
        "project": "alpha",
        "image_path": image_path,
        "prompt": "a bright robot hero",
        "engine": "krea2",
    }


def _seeds(entry, times=8, build=None):
    build = build or consumer.entry_to_job
    return [build(entry)["resolvedSeed"] for _ in range(times)]


def test_resubmitting_the_same_prompt_gets_a_fresh_seed():
    # The regression this file exists for now. Eight rebuilds of one identical
    # entry must not collapse onto a single value.
    seeds = _seeds(generic_entry())
    assert len(set(seeds)) > 1, seeds


def test_a_fresh_seed_also_changes_the_workflow_it_is_baked_into():
    # resolvedSeed is only meaningful if it reaches the graph the relay POSTs.
    first = consumer.entry_to_job(generic_entry())
    second = consumer.entry_to_job(generic_entry())
    assert first["payload"]["workflow"] != second["payload"]["workflow"]
    assert (
        first["payload"]["workflow"]["7"]["inputs"]["seed"] == first["resolvedSeed"]
    )


def test_explicit_seed_remains_authoritative():
    # Reproducing a specific render is still possible — by asking for it.
    entry = generic_entry()
    entry["seed"] = 424242

    assert consumer.entry_to_job(entry)["resolvedSeed"] == 424242
    assert consumer.entry_to_job(entry)["resolvedSeed"] == 424242


def test_negative_seed_is_treated_as_unset_and_randomized():
    # -1 is the conventional "surprise me" value and must not survive into the
    # graph, where ComfyUI would reject it (the API format has no randomize
    # control; that is a UI-only affordance).
    entry = generic_entry()
    entry["seed"] = -1
    seeds = _seeds(entry)
    assert all(seed >= 0 for seed in seeds), seeds
    assert len(set(seeds)) > 1, seeds


def test_every_seed_stays_inside_the_db_column_range():
    # ArtImage.seed is a MySQL signed INT; an out-of-range value failed 18
    # consecutive coloring-book jobs (ids 2146-2184, 2026-07-26).
    for seed in _seeds(generic_entry(), times=25):
        assert 0 <= seed <= consumer.SEED_MAX


def test_specialized_coloring_attempts_keep_fresh_seed_policy(monkeypatch):
    # This lane always explored fresh seeds; it is now simply the same policy as
    # everything else, so it must not have regressed into determinism.
    seeds = iter(range(101, 201))
    # `consume_art_queue` replaces itself with the core module in sys.modules,
    # so this patches the one resolve_seed every lane actually calls.
    monkeypatch.setattr(
        consumer,
        "resolve_seed",
        lambda seed: next(seeds) if not isinstance(seed, int) or seed < 0 else seed,
    )
    entry = {
        **generic_entry(),
        "set": "monster-recast",
        "concept_id": "mr-001",
        "render_attempts": 0,
    }

    assert consumer.entry_to_job(entry)["resolvedSeed"] == 101
    assert consumer.entry_to_job(entry)["resolvedSeed"] == 102


def test_art_request_consumer_shares_the_fresh_seed_boundary():
    request = generic_entry("public/images/requests/alpha.webp")
    seeds = _seeds(request, build=requests.consumer.entry_to_job)
    assert len(set(seeds)) > 1, seeds
