import importlib.util
from pathlib import Path


def load_script(name):
    path = Path(__file__).parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_request_repair_canonicalizes_rewards_and_style_token():
    repair = load_script("repair_art_request_defaults")
    source = """header: true
requests:
- id: sample
  target_repo: silasfelinus/kind_robots
  image_path: public/rewards/item/lucky-penny.webp
  prompt: >
    A lucky penny, cohesive Kind Robots visual style, no text
"""

    updated, path_changes, prompt_changes = repair.repair_requests(source)

    assert path_changes == 1
    assert prompt_changes == 1
    assert "public/images/rewards/item/lucky-penny.webp" in updated
    assert "Kind Robots visual style" not in updated
    assert "multidimensional worldbuilding" in updated


def test_request_repair_leaves_conductor_project_paths_unchanged():
    repair = load_script("repair_art_request_defaults")
    source = """requests:
- id: sample
  target_repo: silasfelinus/conductor
  image_path: projects/images/sample.webp
  prompt: detailed mural scene
"""

    updated, path_changes, prompt_changes = repair.repair_requests(source)

    assert updated == source
    assert path_changes == 0
    assert prompt_changes == 0


def test_failed_job_selection_is_scoped_to_kind_robots_legacy_payloads():
    repair = load_script("repair_failed_kindrobots_artjobs")

    legacy = {
        "id": 10,
        "payload": {
            "targetRepo": "silasfelinus/kind_robots",
            "imagePath": "public/rewards/favor/test.webp",
            "promptString": "Friendly Kind Robots visual language, portrait",
        },
    }
    canonical = {
        "id": 11,
        "payload": {
            "targetRepo": "silasfelinus/kind_robots",
            "imagePath": "public/images/rewards/favor/test.webp",
            "promptString": "Detailed mature animated portrait",
        },
    }
    conductor = {
        "id": 12,
        "payload": {
            "targetRepo": "silasfelinus/conductor",
            "imagePath": "projects/images/card.webp",
            "promptString": "Friendly Kind Robots visual language, portrait",
        },
    }

    assert len(repair.repair_reasons(legacy)) == 2
    assert repair.repair_reasons(canonical) == []
    assert repair.repair_reasons(conductor) == []


def test_default_art_direction_carries_no_casting_clause():
    """A duplicated constant is what kept the 2026-08-08 art bug alive.

    kind_robots split its DEFAULT_ASSET_ART_DIRECTION that morning so the
    casting half became opt-in. This Python mirror was missed and went on
    stamping the full block into art-prompts.yaml for another twelve hours —
    ArtJob 8086 was still being minted with it at 21:06.

    Krea 2 renders "cast characters naturally across many species...; include
    robots only when the subject or scene explicitly calls for them" rather than
    reading it: a conditional is just a dense noun phrase to a diffusion model,
    which is how a ladle became a crowd of fifteen people.
    """
    repair = load_script("repair_art_request_defaults")
    direction = repair.DEFAULT_ASSET_ART_DIRECTION

    assert "cast characters" not in direction
    assert "conventional attractiveness" not in direction
    assert "only when" not in direction, "no conditional may reach a diffusion model"
    # ...while still carrying the style direction it exists to supply.
    assert "clear readable silhouettes" in direction
