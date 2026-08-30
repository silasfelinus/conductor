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
