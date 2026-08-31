from __future__ import annotations

import copy
import json
from pathlib import Path

import scripts.build_dream_proposal as proposals
import scripts.repair_dream_prose_catalog as repair


def _proposal() -> dict:
    proposal = copy.deepcopy(proposals.SAMPLE_PROPOSAL)
    proposal["title"] = "Monsoon Static"
    proposal["slug"] = "monsoon-static"
    proposal["idea"] = (
        "A storm-battered neighborhood powers its flood barrier with live rooftop songs, "
        "forcing every block to choose what it will sing when the water rises."
    )
    proposal["vibe"]["title"] = "Monsoon Static"
    proposal["vibe"]["line"] = "The storm only spares the block that out-sings it."
    proposal["locations"][0].update(
        title="The Roofline Circuit",
        known_for="rooftop stages wired straight into the flood barriers",
        local_rule="the loudest verse gets the power",
        best_scene=(
            "the surge climbs the stairwell while the mast crew hauls glowing silk line "
            "back up hand over hand"
        ),
    )
    proposal["characters"][0]["name"] = "Mast Crew"
    proposal["scenarios"][0]["setup"] = (
        "In Monsoon Static at The Roofline Circuit, Mast Crew races a rising surge "
        "while the whole block sings current into a failing barrier."
    )
    return proposal


def test_audit_identifies_the_monsoon_static_fragment_shape(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    proposal = _proposal()
    text = proposals.render_markdown(proposal, "2026-08-30")
    text = text.replace("status: outline", "status: built")
    text += "\n<!-- built-data\n" + json.dumps({"records": {"world": {"id": 1}}}) + "\n-->\n"
    (backlog / "2026-08-30-monsoon-static.md").write_text(text, encoding="utf-8")

    rows = repair.audit(backlog)

    assert len(rows) == 1
    assert set(rows[0]["fields"]) == {
        "locations[0].known_for",
        "locations[0].local_rule",
        "locations[0].best_scene",
    }


def test_author_patch_changes_only_requested_fields(monkeypatch):
    proposal = _proposal()
    reply = {
        "known_for": (
            "Its rooftop stages feed sung verses directly into the flood barriers, turning "
            "every performance into emergency power for the block below."
        ),
        "local_rule": (
            "During a surge, the strongest live chorus receives the circuit's power first, "
            "so silence can leave an entire block unprotected."
        ),
        "best_scene": (
            "As floodwater climbs the stairwell, the mast crew hauls a glowing silk cable "
            "onto the roof while the crowd sings hard enough to keep the barrier alive."
        ),
    }
    monkeypatch.setattr(repair.author, "call_claude", lambda *args, **kwargs: json.dumps(reply))

    patch, candidate = repair._author_patch(
        proposal,
        [
            "locations[0].known_for",
            "locations[0].local_rule",
            "locations[0].best_scene",
        ],
        "test-key",
    )

    assert patch == reply
    assert candidate["idea"] == proposal["idea"]
    assert candidate["vibe"] == proposal["vibe"]
    assert candidate["locations"][0]["known_for"] == reply["known_for"]


def test_live_prose_patch_does_not_queue_or_replace_art(monkeypatch):
    old = _proposal()
    new = copy.deepcopy(old)
    new["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power for the flood barriers below.",
        local_rule="During a surge, the strongest live chorus receives the circuit's power before quieter rooftops do.",
        best_scene="Floodwater reaches the stairwell as the mast crew recovers a glowing silk cable and the crowd keeps singing.",
    )
    built = {
        "records": {
            "world": {"id": 10},
            "locations": [{"id": 11}],
            "scenarios": [{"id": 12}],
        },
        "sheets": {old["slug"]: 20, repair.records.slugify(old["locations"][0]["title"]): 21},
        "art": [{"request_id": "keep-this-art", "attached": True}],
    }
    calls = []
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch", lambda endpoint, entity_id, body: calls.append((endpoint, entity_id, body)))

    repair._patch_live(
        old,
        new,
        built,
        [
            "locations[0].known_for",
            "locations[0].local_rule",
            "locations[0].best_scene",
        ],
    )

    assert [call[:2] for call in calls] == [("/api/dreams", 11), ("/api/sheets", 21)]
    assert built["art"] == [{"request_id": "keep-this-art", "attached": True}]


def test_reward_paths_resolve_by_type_not_list_position():
    # Only "exactly one ITEM and one SKILL" is guaranteed; order is not. A path
    # that assumed rewards[0] was the ITEM would repair the wrong row.
    proposal = _proposal()
    proposal["rewards"].reverse()
    assert proposal["rewards"][0]["reward_type"] == "SKILL"

    repair._set(proposal, repair.FIELD_PATHS["rewards[item].grants"], "It does the item thing.")
    repair._set(proposal, repair.FIELD_PATHS["rewards[skill].grants"], "It does the skill thing.")

    item = next(r for r in proposal["rewards"] if r["reward_type"] == "ITEM")
    skill = next(r for r in proposal["rewards"] if r["reward_type"] == "SKILL")
    assert item["grants"] == "It does the item thing."
    assert skill["grants"] == "It does the skill thing."
    assert repair._get(proposal, repair.FIELD_PATHS["rewards[item].catch"]) == item["catch"]


def test_audit_reaches_character_and_reward_fragments(tmp_path: Path, monkeypatch):
    # The 2026-08-30 hand repair fixed every field this lane could address and
    # left the character/reward copy untouched, because the lane could not name
    # those fields at all. Regression guard for that blind spot.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    proposal = _proposal()
    proposal["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power for the barriers below.",
        local_rule="During a surge the strongest live chorus receives the circuit's power first.",
        best_scene="Floodwater reaches the stairwell as the mast crew hauls a glowing silk cable up.",
    )
    proposal["characters"][0].update(
        role_drive="keep the barrier lit",
        carries="a coil of silk line",
        complication="her verse is failing",
    )
    text = proposals.render_markdown(proposal, "2026-08-30").replace("status: outline", "status: built")
    text += "\n<!-- built-data\n" + json.dumps({"records": {"world": {"id": 1}}}) + "\n-->\n"
    (backlog / "2026-08-30-monsoon-static.md").write_text(text, encoding="utf-8")

    rows = repair.audit(backlog)

    assert len(rows) == 1
    assert set(rows[0]["fields"]) == {
        "characters[0].role_drive",
        "characters[0].carries",
        "characters[0].complication",
    }
    assert rows[0]["current"]["character_role_drive"] == "keep the barrier lit"


def test_live_patch_updates_character_and_reward_rows(monkeypatch):
    old = _proposal()
    new = copy.deepcopy(old)
    new["characters"][0].update(
        role_drive="She has to keep the block's barrier lit through the whole surge.",
        carries="A coil of glowing silk line is looped across her shoulder.",
        complication="Her own verse is the one the circuit keeps refusing.",
    )
    item = next(r for r in new["rewards"] if r["reward_type"] == "ITEM")
    item["grants"] = "It gives back the ten seconds you have just spent."
    item["catch"] = "Everyone else remembers the ten seconds you took back."
    built = {
        "records": {
            "world": {"id": 10},
            "locations": [{"id": 11}],
            "scenarios": [{"id": 12}],
            "characters": [{"id": 13}],
            "rewards": [{"id": 14, "reward_type": "ITEM"}, {"id": 15, "reward_type": "SKILL"}],
        },
        "sheets": {},
        "art": [{"request_id": "keep-this-art", "attached": True}],
    }
    calls = []
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch",
                        lambda endpoint, entity_id, body: calls.append((endpoint, entity_id, body)))

    repair._patch_live(old, new, built, [
        "characters[0].role_drive",
        "characters[0].carries",
        "characters[0].complication",
        "rewards[item].grants",
        "rewards[item].catch",
    ])

    by_endpoint = {(c[0], c[1]): c[2] for c in calls}
    assert ("/api/characters", 13) in by_endpoint
    assert ("/api/rewards", 14) in by_endpoint
    assert ("/api/rewards", 15) not in by_endpoint  # SKILL was not in the field set
    character = by_endpoint[("/api/characters", 13)]
    assert character["drive"] == new["characters"][0]["role_drive"]
    assert character["quirks"] == new["characters"][0]["complication"]
    assert character["backstory"].startswith("A coil of glowing silk line")
    assert not character["backstory"].startswith("Carries ")
    reward = by_endpoint[("/api/rewards", 14)]
    assert reward["description"] == item["grants"]
    assert reward["effect"] == item["grants"]
    assert reward["flavorText"] == item["catch"]
    assert built["art"] == [{"request_id": "keep-this-art", "attached": True}]


def test_live_location_description_carries_no_stems(monkeypatch):
    old = _proposal()
    new = copy.deepcopy(old)
    new["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power.",
        local_rule="The strongest chorus receives the circuit's power first.",
        best_scene="Floodwater reaches the stairwell while the crowd keeps singing.",
    )
    built = {
        "records": {"world": {"id": 10}, "locations": [{"id": 11}], "scenarios": [{"id": 12}]},
        "sheets": {},
        "art": [],
    }
    calls = []
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch",
                        lambda endpoint, entity_id, body: calls.append((endpoint, entity_id, body)))

    repair._patch_live(old, new, built, ["locations[0].known_for"])

    description = calls[0][2]["description"]
    assert description.startswith("Its rooftop stages")
    assert "Known for" not in description
    assert "Local rule:" not in description


def test_typography_pass_is_deterministic_and_semantics_free(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    proposal = _proposal()
    proposal["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power for the barriers.",
        local_rule="No verse, no current -- the loudest rooftop is the one that stays lit.",
        best_scene="Floodwater reaches the stairwell while the crowd keeps singing into the mast.",
    )
    text = proposals.render_markdown(proposal, "2026-08-30").replace("status: outline", "status: built")
    text += "\n<!-- built-data\n" + json.dumps({"records": {"world": {"id": 1}}}) + "\n-->\n"
    (backlog / "2026-08-30-monsoon-static.md").write_text(text, encoding="utf-8")

    rows = repair.typography_findings(backlog)

    assert len(rows) == 1
    assert rows[0]["fields"] == ["locations[0].local_rule"]
    fixed = proposals.normalize_typography(rows[0]["proposal"]["locations"][0]["local_rule"])
    assert " -- " not in fixed
    assert fixed == "No verse, no current — the loudest rooftop is the one that stays lit."


def test_typography_pass_finds_nothing_once_copy_is_clean(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    proposal = _proposal()
    proposal["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power for the barriers.",
        local_rule="No verse, no current — the loudest rooftop is the one that stays lit.",
        best_scene="Floodwater reaches the stairwell while the crowd keeps singing into the mast.",
    )
    text = proposals.render_markdown(proposal, "2026-08-30").replace("status: outline", "status: built")
    text += "\n<!-- built-data\n" + json.dumps({"records": {"world": {"id": 1}}}) + "\n-->\n"
    (backlog / "2026-08-30-monsoon-static.md").write_text(text, encoding="utf-8")

    assert repair.typography_findings(backlog) == []


def test_typography_apply_patches_live_and_rewrites_source(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    proposal = _proposal()
    proposal["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power for the barriers.",
        local_rule="No verse, no current -- the loudest rooftop is the one that stays lit.",
        best_scene="Floodwater reaches the stairwell while the crowd keeps singing into the mast.",
    )
    built = {
        "records": {"world": {"id": 10}, "locations": [{"id": 11}], "scenarios": [{"id": 12}]},
        "sheets": {}, "art": [{"request_id": "keep-this-art", "attached": True}],
    }
    text = proposals.render_markdown(proposal, "2026-08-30").replace("status: outline", "status: built")
    text += "\n<!-- built-data\n" + json.dumps(built) + "\n-->\n"
    path = backlog / "2026-08-30-monsoon-static.md"
    path.write_text(text, encoding="utf-8")

    calls = []
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch",
                        lambda endpoint, entity_id, body: calls.append((endpoint, entity_id, body)))
    monkeypatch.setattr(repair.author, "call_claude",
                        lambda *a, **k: pytest.fail("typography mode must not call a model"))
    request_path = tmp_path / "2026-08-30-typography-request.json"
    request_path.write_text(json.dumps({"mode": "typography", "scope": "all-built"}), encoding="utf-8")

    results = repair._apply_batch(request_path, json.loads(request_path.read_text()))

    assert len(results) == 1
    assert results[0]["fields"] == ["locations[0].local_rule"]
    assert " -- " not in path.read_text(encoding="utf-8")
    assert calls and calls[0][0] == "/api/dreams"
    # The request is consumed into a receipt, and the art ledger is untouched.
    assert not request_path.exists()
    assert (tmp_path / "2026-08-30-typography-applied.json").exists()
    assert repair.typography_findings(backlog) == []
