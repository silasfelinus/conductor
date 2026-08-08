"""Focused safety tests for scripts/repair_dream_art.py."""
import importlib.util
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location(
    "repair_dream_art", SCRIPTS / "repair_dream_art.py")
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)


def _item(**overrides):
    item = {
        "kind": "character",
        "id": 2800,
        "label": "Perrin Voss",
        "prompt": "new prompt",
        "source": "2026-08-08-example.md",
        "old_prompt": "old prompt",
        "is_public": True,
        "is_mature": False,
    }
    item.update(overrides)
    return item


def test_needs_repair_requires_existing_art_and_old_prompt():
    assert repair.needs_repair({"imagePath": "/images/old.webp", "artPrompt": "legacy"})
    assert not repair.needs_repair({"imagePath": None, "artPrompt": "legacy"})
    assert not repair.needs_repair({
        "imagePath": "/images/new.webp",
        "artPrompt": f"subject, {repair.STYLE}",
    })


def test_rewards_are_matched_by_name_when_built_order_differs():
    proposal = {
        "title": "Test World",
        "vibe": {"line": "Odd tides remember names."},
        "rewards": [
            {
                "name": "First Item",
                "reward_type": "ITEM",
                "look": "a brass compass",
                "grants": "points toward forgotten doors",
                "rarity": "RARE",
            },
            {
                "name": "Second Skill",
                "reward_type": "SKILL",
                "look": "a blue afterimage around one hand",
                "grants": "briefly echoes a practiced motion",
                "rarity": "UNCOMMON",
            },
        ],
    }
    built = {
        "records": {
            "rewards": [
                {"id": 22, "name": "Second Skill"},
                {"id": 11, "name": "First Item"},
            ]
        }
    }

    rewards = [row for row in repair.elements(proposal, built) if row["kind"] == "reward"]
    assert [(row["id"], row["label"]) for row in rewards] == [
        (22, "Second Skill"),
        (11, "First Item"),
    ]
    assert "Second Skill" in rewards[0]["prompt"]
    assert "First Item" in rewards[1]["prompt"]


def test_enqueue_failure_does_not_hide_row_from_future_retry(monkeypatch):
    events = []
    monkeypatch.setattr(repair, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair, "plan", lambda kinds, only: [_item()])
    monkeypatch.setattr(repair, "enqueue_render", lambda item: events.append("enqueue") or None)
    monkeypatch.setattr(repair, "patch_prompt", lambda item: events.append("patch") or True)

    assert repair.main(["--apply"]) == 0
    assert events == ["enqueue"]


def test_success_enqueues_before_patching_prompt(monkeypatch):
    events = []
    monkeypatch.setattr(repair, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair, "plan", lambda kinds, only: [_item()])
    monkeypatch.setattr(repair, "enqueue_render", lambda item: events.append("enqueue") or 9001)
    monkeypatch.setattr(repair, "patch_prompt", lambda item: events.append("patch") or True)

    assert repair.main(["--apply"]) == 0
    assert events == ["enqueue", "patch"]


def test_skip_render_updates_prompt_without_enqueue(monkeypatch):
    events = []
    monkeypatch.setattr(repair, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair, "plan", lambda kinds, only: [_item()])
    monkeypatch.setattr(repair, "enqueue_render", lambda item: events.append("enqueue") or 9001)
    monkeypatch.setattr(repair, "patch_prompt", lambda item: events.append("patch") or True)

    assert repair.main(["--apply", "--skip-render"]) == 0
    assert events == ["patch"]
