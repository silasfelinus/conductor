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


def test_generic_retry_rebuilds_identical_seed_and_workflow():
    first = consumer.entry_to_job(generic_entry())
    second = consumer.entry_to_job(generic_entry())

    assert first["resolvedSeed"] == second["resolvedSeed"]
    assert first["payload"]["workflow"] == second["payload"]["workflow"]


def test_retry_seed_changes_with_stable_request_identity():
    first = consumer.entry_to_job(generic_entry("projects/images/alpha-hero.webp"))
    second = consumer.entry_to_job(generic_entry("projects/images/alpha-card.webp"))

    assert first["resolvedSeed"] != second["resolvedSeed"]


def test_explicit_seed_remains_authoritative():
    entry = generic_entry()
    entry["seed"] = 424242

    assert consumer.entry_to_job(entry)["resolvedSeed"] == 424242


def test_specialized_coloring_attempts_keep_fresh_seed_policy(monkeypatch):
    seeds = iter((101, 202))
    monkeypatch.setattr(consumer._core, "resolve_seed", lambda _seed: next(seeds))
    entry = {
        **generic_entry(),
        "set": "monster-recast",
        "concept_id": "mr-001",
        "semantic_attempts": 0,
    }

    first = consumer.entry_to_job(entry)
    second = consumer.entry_to_job(entry)

    assert first["resolvedSeed"] == 101
    assert second["resolvedSeed"] == 202


def test_art_request_consumer_uses_retry_stable_shared_boundary():
    request = generic_entry("public/images/requests/alpha.webp")

    first = requests.consumer.entry_to_job(request)
    second = requests.consumer.entry_to_job(request)

    assert first["resolvedSeed"] == second["resolvedSeed"]
