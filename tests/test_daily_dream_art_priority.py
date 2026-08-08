import scripts.consume_art_queue as consumer


def daily_dream_entry(**overrides):
    entry = {
        "id": "dream-cycle-moonlit-greenhouse-world",
        "source": "dream-cycle",
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/dreams/moonlit-greenhouse/world-card.webp",
        "source_url": "/images/dreams/moonlit-greenhouse/world-card.webp",
        "page_url": "https://kind-robots.vercel.app",
        "label": "Moonlit Greenhouse",
        "entity_type": "dream",
        "entity_id": 4242,
        "entity_field": "imagePath",
        "prompt": "a moonlit greenhouse",
        "engine": "krea2",
    }
    entry.update(overrides)
    return entry


def test_daily_dream_art_jobs_get_top_priority():
    job = consumer.entry_to_job(daily_dream_entry())
    assert job["priority"] == 100
    assert job["priority"] == consumer.DAILY_DREAM_PRIORITY


def test_daily_dream_source_matching_is_tolerant():
    job = consumer.entry_to_job(daily_dream_entry(source=" Dream-Cycle "))
    assert job["priority"] == 100


def test_daily_dream_jobs_preserve_target_and_request_provenance():
    entry = daily_dream_entry()
    job = consumer.entry_to_job(entry)
    payload = job["payload"]

    assert job["projectSlug"] == "dream-cycle"
    assert job["idempotencyKey"] == entry["id"]
    assert payload["collection"] == "dream-cycle"
    assert payload["targetRepo"] == entry["target_repo"]
    assert payload["imagePath"] == entry["image_path"]
    assert payload["sourceUrl"] == entry["source_url"]
    assert payload["pageUrl"] == entry["page_url"]
    assert payload["entityArt"] == {
        "entityType": "dream",
        "entityId": 4242,
        "field": "imagePath",
        "preserveOriginal": True,
        "mode": "recreate",
    }
    assert payload["conductorRequest"] == {
        "id": entry["id"],
        "source": "dream-cycle",
        "label": entry["label"],
        "targetRepo": entry["target_repo"],
        "imagePath": entry["image_path"],
        "sourceUrl": entry["source_url"],
        "pageUrl": entry["page_url"],
    }


def test_daily_dream_without_valid_target_still_keeps_priority_and_provenance():
    job = consumer.entry_to_job(
        daily_dream_entry(entity_type="dream", entity_id=None)
    )
    assert job["priority"] == 100
    assert "entityArt" not in job["payload"]
    assert job["payload"]["conductorRequest"]["id"] == job["idempotencyKey"]


def test_unrelated_art_keeps_existing_priority_behavior():
    job = consumer.entry_to_job(
        {
            "source": "kind-robots-missing-image",
            "image_path": "public/images/ordinary-fixture.webp",
            "prompt": "a moonlit greenhouse",
            "engine": "krea2",
        }
    )
    assert "priority" not in job
    assert "idempotencyKey" not in job
    assert "conductorRequest" not in job["payload"]
    assert "entityArt" not in job["payload"]
    assert "targetRepo" not in job["payload"]
    assert "imagePath" not in job["payload"]
