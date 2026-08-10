import scripts.consume_art_queue as consumer


def test_generic_kind_robots_request_preserves_delivery_destination():
    entry = {
        "id": "taskmaster-dashboard-tab",
        "source": "kind-robots-missing-image",
        "project_slug": "taskmaster",
        "variant": "image",
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/dashboard-tabs/scenario/taskmaster.webp",
        "source_url": "/images/dashboard-tabs/scenario/taskmaster.webp",
        "page_url": "/taskmaster",
        "label": "Taskmaster dashboard tab",
        "size": "512x512",
        "prompt": "Taskmaster dashboard artwork",
        "engine": "krea2",
    }

    job = consumer.entry_to_job(entry)

    assert job["projectSlug"] == "taskmaster"
    assert job["idempotencyKey"] == "taskmaster-dashboard-tab"
    assert job["payload"]["targetRepo"] == "silasfelinus/kind_robots"
    assert (
        job["payload"]["imagePath"]
        == "public/images/dashboard-tabs/scenario/taskmaster.webp"
    )
    assert job["payload"]["sourceUrl"] == "/images/dashboard-tabs/scenario/taskmaster.webp"
    assert job["payload"]["pageUrl"] == "/taskmaster"
    assert job["payload"]["conductorRequest"] == {
        "id": "taskmaster-dashboard-tab",
        "source": "kind-robots-missing-image",
        "label": "Taskmaster dashboard tab",
        "targetRepo": "silasfelinus/kind_robots",
        "imagePath": "public/images/dashboard-tabs/scenario/taskmaster.webp",
        "sourceUrl": "/images/dashboard-tabs/scenario/taskmaster.webp",
        "pageUrl": "/taskmaster",
    }


def test_untargeted_generic_request_keeps_existing_behavior():
    job = consumer.entry_to_job(
        {
            "image_path": "projects/images/example.webp",
            "prompt": "example art",
            "engine": "krea2",
        }
    )

    assert "targetRepo" not in job["payload"]
    assert "conductorRequest" not in job["payload"]
    assert "idempotencyKey" not in job
