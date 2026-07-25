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
