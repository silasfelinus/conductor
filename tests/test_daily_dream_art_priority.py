import scripts.consume_art_queue as consumer


def daily_dream_entry(**overrides):
    entry = {
        "source": "dream-cycle",
        "image_path": "public/images/daily-dream-fixture.webp",
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
