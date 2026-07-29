from pathlib import Path

import yaml

import scripts.queue_missing_project_art as art_queue


def make_catalog() -> dict:
    return {
        "images": [
            {
                "project": "alpha",
                "icon": {
                    "image_path": "projects/images/alpha-icon.webp",
                    "size": "256x256",
                    "status": "pending",
                    "prompt": "  bright   alpha   icon  ",
                    "model": " gpt-image-1 ",
                },
                "card": {
                    "image_path": "projects/images/alpha-card.webp",
                    "size": "512x768",
                    "status": "done",
                    "prompt": "already generated",
                },
                "hero": {
                    "image_path": "projects/images/alpha-hero.webp",
                    "size": "1280x720",
                    "status": "pending",
                    "prompt": "alpha hero prompt",
                    "engine": "openai",
                },
            },
            {
                "project": "beta",
                "icon": {
                    "image_path": "projects/images/beta-icon.webp",
                    "status": "pending",
                    "prompt": "beta icon prompt",
                },
                "card": {
                    "image_path": "projects/images/beta-card.webp",
                    "status": "pending",
                    "prompt": "beta card prompt",
                },
                "hero": {
                    "image_path": "projects/images/beta-hero.webp",
                    "status": "pending",
                    "prompt": "beta hero prompt",
                },
            },
        ]
    }


def test_iter_missing_project_assets_skips_existing_and_done_assets(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(art_queue, "ROOT", tmp_path)
    existing_hero = tmp_path / "projects" / "images" / "alpha-hero.webp"
    existing_hero.parent.mkdir(parents=True, exist_ok=True)
    existing_hero.write_bytes(b"already generated")

    entries = art_queue.iter_missing_project_assets(make_catalog())

    queued_paths = [entry["image_path"] for entry in entries]
    assert queued_paths == [
        "projects/images/alpha-icon.webp",
        "projects/images/beta-icon.webp",
        "projects/images/beta-card.webp",
        "projects/images/beta-hero.webp",
    ]
    assert "projects/images/alpha-card.webp" not in queued_paths
    assert "projects/images/alpha-hero.webp" not in queued_paths


def test_iter_missing_project_assets_normalizes_prompt_default_sizes_and_engine(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(art_queue, "ROOT", tmp_path)
    monkeypatch.setattr(art_queue, "DEFAULT_PROJECT_ART_ENGINE", "krea2")

    entries = art_queue.iter_missing_project_assets(make_catalog())
    by_project_variant = {(entry["project"], entry["variant"]): entry for entry in entries}

    alpha_icon = by_project_variant[("alpha", "icon")]
    assert alpha_icon == {
        "project": "alpha",
        "variant": "icon",
        "target_repo": "silasfelinus/conductor",
        "image_path": "projects/images/alpha-icon.webp",
        "size": "256x256",
        "status": "pending",
        "prompt": "bright alpha icon",
        "engine": "gpt-image-1",
    }

    assert by_project_variant[("alpha", "hero")]["engine"] == "openai"
    assert by_project_variant[("alpha", "hero")]["size"] == "1280x720"
    assert by_project_variant[("beta", "icon")]["size"] == "256x256"
    assert by_project_variant[("beta", "card")]["size"] == "512x768"
    assert by_project_variant[("beta", "hero")]["size"] == "1280x720"
    assert by_project_variant[("beta", "icon")]["engine"] == "krea2"
    assert by_project_variant[("beta", "card")]["engine"] == "krea2"
    assert by_project_variant[("beta", "hero")]["engine"] == "krea2"


def test_iter_missing_project_assets_uses_configured_default_engine(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(art_queue, "ROOT", tmp_path)
    monkeypatch.setattr(art_queue, "DEFAULT_PROJECT_ART_ENGINE", "flux2-klein")

    entries = art_queue.iter_missing_project_assets(make_catalog())
    by_project_variant = {(entry["project"], entry["variant"]): entry for entry in entries}

    assert by_project_variant[("beta", "icon")]["engine"] == "flux2-klein"
    assert by_project_variant[("beta", "card")]["engine"] == "flux2-klein"
    assert by_project_variant[("beta", "hero")]["engine"] == "flux2-klein"


def test_load_active_queue_entries_keeps_only_in_flight_work(tmp_path: Path) -> None:
    output_path = tmp_path / "projects" / "art-generate.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(
            {
                "batch": {
                    "entries": [
                        {
                            "project": "alpha",
                            "variant": "icon",
                            "image_path": "projects/images/alpha-icon.webp",
                            "status": "pending",
                            "prompt": "replace the old icon",
                            "engine": "krea2",
                        },
                        {
                            "project": "beta",
                            "variant": "hero",
                            "image_path": "projects/images/beta-hero.webp",
                            "status": "done",
                            "prompt": "already finished",
                            "engine": "krea2",
                        },
                    ]
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    active = art_queue.load_active_queue_entries(output_path)

    assert [entry["image_path"] for entry in active] == [
        "projects/images/alpha-icon.webp"
    ]


def test_merge_queue_entries_preserves_manual_retry_for_existing_path() -> None:
    retry = {
        "project": "alpha",
        "variant": "icon",
        "target_repo": "silasfelinus/conductor",
        "image_path": "projects/images/alpha-icon.webp",
        "status": "pending",
        "prompt": "rich replacement prompt",
        "engine": "krea2",
    }
    regenerated_duplicate = {
        **retry,
        "prompt": "generic regenerated prompt",
    }
    newly_missing = {
        "project": "beta",
        "variant": "hero",
        "target_repo": "silasfelinus/conductor",
        "image_path": "projects/images/beta-hero.webp",
        "status": "pending",
        "prompt": "newly missing hero",
        "engine": "krea2",
    }

    merged = art_queue.merge_queue_entries(
        [retry], [regenerated_duplicate, newly_missing], limit=2
    )

    assert merged == [retry, newly_missing]
    assert merged[0]["prompt"] == "rich replacement prompt"


def test_merge_queue_entries_never_drops_active_work_when_over_limit() -> None:
    active = [
        {
            "project": f"project-{index}",
            "variant": "icon",
            "target_repo": "silasfelinus/conductor",
            "image_path": f"projects/images/project-{index}-icon.webp",
            "status": "pending",
            "prompt": f"retry {index}",
            "engine": "krea2",
        }
        for index in range(3)
    ]

    merged = art_queue.merge_queue_entries(active, [], limit=2)

    assert merged == active


def test_write_queue_outputs_expected_dry_run_shape(tmp_path: Path) -> None:
    output_path = tmp_path / "projects" / "art-generate.yaml"
    entries = [
        {
            "project": "alpha",
            "variant": "icon",
            "target_repo": "silasfelinus/conductor",
            "image_path": "projects/images/alpha-icon.webp",
            "size": "256x256",
            "status": "pending",
            "prompt": "bright alpha icon",
            "engine": "krea2",
        }
    ]

    art_queue.write_queue(entries, output_path)

    written = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert written == {
        "generated_by": "scripts/queue_missing_project_art.py",
        "mode": "dry-run",
        "description": (
            "Concrete project image requests ready for generation; active retries are "
            "preserved until the consumer marks them complete."
        ),
        "batch": {"entries": entries},
    }
