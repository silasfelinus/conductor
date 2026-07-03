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


def test_iter_missing_project_assets_skips_existing_and_done_assets(tmp_path: Path, monkeypatch) -> None:
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


def test_iter_missing_project_assets_normalizes_prompt_and_default_sizes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(art_queue, "ROOT", tmp_path)

    entries = art_queue.iter_missing_project_assets(make_catalog())

    alpha_icon = entries[0]
    assert alpha_icon == {
        "project": "alpha",
        "variant": "icon",
        "target_repo": "silasfelinus/conductor",
        "image_path": "projects/images/alpha-icon.webp",
        "size": "256x256",
        "status": "pending",
        "prompt": "bright alpha icon",
    }

    beta_icon = entries[1]
    beta_card = entries[2]
    beta_hero = entries[3]
    assert beta_icon["size"] == "256x256"
    assert beta_card["size"] == "512x768"
    assert beta_hero["size"] == "1280x720"


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
        }
    ]

    art_queue.write_queue(entries, output_path)

    written = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert written == {
        "generated_by": "scripts/queue_missing_project_art.py",
        "mode": "dry-run",
        "description": "Concrete project image requests ready for manual generation; no live API was called.",
        "images": entries,
    }
