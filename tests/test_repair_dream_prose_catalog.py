from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

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


def _built_bundle(backlog, name="2026-08-30-monsoon-static.md", *, broken=True):
    proposal = _proposal()
    proposal["locations"][0].update(
        known_for="Its rooftop stages turn every live chorus into emergency power for the barriers.",
        local_rule="During a surge the strongest live chorus receives the circuit's power first.",
        best_scene="Floodwater reaches the stairwell as the mast crew hauls a glowing silk cable up.",
    )
    if broken == "grants":
        for reward in proposal["rewards"]:
            reward["grants"] = "It grants the ability to steady a failing barrier."
    elif broken:
        for reward in proposal["rewards"]:
            reward["best_used_when"] = "It works best when the barrier lamps are already dimming."
    built = {
        "records": {"world": {"id": 10}, "locations": [{"id": 11}], "scenarios": [{"id": 12}],
                    "characters": [{"id": 13}],
                    "rewards": [{"id": 14, "reward_type": "ITEM"}, {"id": 15, "reward_type": "SKILL"}]},
        "sheets": {}, "art": [{"request_id": "keep-this-art", "attached": True}],
        "built_at": "2026-08-30T10:00:00+00:00",
    }
    text = proposals.render_markdown(proposal, "2026-08-30").replace("status: outline", "status: built")
    text += "\n<!-- built-data\n" + json.dumps(built) + "\n-->\n"
    (backlog / name).write_text(text, encoding="utf-8")
    return backlog / name


def test_authoring_phase_writes_source_and_touches_nothing_live(tmp_path, monkeypatch):
    # The ordering guarantee. Run 33450722225 patched 16 bundles' live rows and
    # then failed to push, stranding the repaired copy in a discarded runner tree.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    path = _built_bundle(backlog)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    calls = []
    monkeypatch.setattr(repair.revision, "_patch",
                        lambda *a, **k: calls.append(a))
    fixed = "The barrier lamps are already dimming and the crowd has gone quiet."
    monkeypatch.setattr(repair.author, "call_claude",
                        lambda *a, **k: json.dumps({"item_best_used_when": fixed,
                                                    "skill_best_used_when": fixed}))
    request_path = tmp_path / "2026-09-01-editorial-pass-request.json"
    request_path.write_text(json.dumps({"scope": "all-built"}), encoding="utf-8")

    repair._apply_batch(request_path, json.loads(request_path.read_text()))

    assert calls == [], "authoring phase must not PATCH production"
    assert fixed in path.read_text(encoding="utf-8"), "source must be repaired on disk"
    receipt = json.loads((tmp_path / "2026-09-01-editorial-pass-applied.json").read_text())
    assert receipt["status"] == "source-written"
    assert len(receipt["pending_live"]) == 1


def test_publish_phase_patches_live_and_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    path = _built_bundle(backlog, broken="grants")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    calls = []
    monkeypatch.setattr(repair.revision, "_patch",
                        lambda endpoint, entity_id, body: calls.append((endpoint, entity_id)))
    # `grants` is used rather than `best_used_when`: build_dream_records never
    # writes best_used_when to a Reward row, so repairing it alone produces no
    # live PATCH at all -- which is exactly why the 16 values stranded by run
    # 33450722225 could not be recovered from production.
    fixed_grants = "It reveals the single hidden variable everyone else misreads."
    monkeypatch.setattr(repair.author, "call_claude",
                        lambda *a, **k: json.dumps({"item_grants": fixed_grants,
                                                    "skill_grants": fixed_grants}))
    request_path = tmp_path / "2026-09-01-editorial-pass-request.json"
    request_path.write_text(json.dumps({"scope": "all-built"}), encoding="utf-8")
    repair._apply_batch(request_path, json.loads(request_path.read_text()))
    receipt_path = tmp_path / "2026-09-01-editorial-pass-applied.json"

    assert repair.publish_live(receipt_path) == 0
    assert calls, "publish phase must PATCH production"
    assert "live_pending" not in path.read_text(encoding="utf-8")
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "applied" and receipt["pending_live"] == []

    # Re-running after a partial failure must not double-patch.
    before = len(calls)
    assert repair.publish_live(receipt_path) == 0
    assert len(calls) == before


def test_extra_fields_repairs_a_sentence_no_check_generalizes(tmp_path, monkeypatch):
    # The contract catches defect classes. An editor reading the catalog also
    # finds one-offs -- a local_rule whose second clause restates its first, a
    # definite reference to someone never introduced -- that no honest regex
    # generalizes. Without this lane the only way to repair a sentence you can
    # see is wrong is to invent a detector for its whole class.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    path = _built_bundle(backlog)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch", lambda *a, **k: None)
    fixed = "The barrier lamps are already dimming and the crowd has gone quiet."
    rule = "No performance may finish the final aria, and none ever has."
    seen: dict = {}

    def _call(prompt, system, key):
        seen["prompt"] = prompt
        return json.dumps({"item_best_used_when": fixed, "skill_best_used_when": fixed,
                           "local_rule": rule})

    monkeypatch.setattr(repair.author, "call_claude", _call)
    request_path = tmp_path / "2026-09-01-extra-request.json"
    request_path.write_text(json.dumps({
        "scope": "all-built",
        "extra_fields": {"2026-08-30": ["locations[0].local_rule"]},
    }), encoding="utf-8")

    repair._apply_batch(request_path, json.loads(request_path.read_text()))

    assert "local_rule" in seen["prompt"], "the hand-picked field must reach the model"
    assert rule in path.read_text(encoding="utf-8")


def test_extra_fields_rejects_a_field_the_repair_lane_cannot_resolve(tmp_path, monkeypatch):
    # A label with no FIELD_PATHS entry would be dropped silently on the way in
    # and still be there on the way out, so fail on the request instead.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    _built_bundle(backlog)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    request_path = tmp_path / "2026-09-01-bad-request.json"
    request = {"scope": "all-built", "extra_fields": {"2026-08-30": ["locations[0].smell"]}}
    request_path.write_text(json.dumps(request), encoding="utf-8")

    with pytest.raises(ValueError, match="unknown field"):
        repair._apply_batch(request_path, request)


def test_a_noted_editorial_field_must_actually_change(tmp_path, monkeypatch):
    # Run 33464442851 handed the model two hand-picked fields with no reason
    # attached and got both back byte-identical -- a silent no-op, because a
    # field with no complaint has nothing to re-check afterwards. The note is
    # what makes it actionable, so a noted field returned verbatim is an error.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    path = _built_bundle(backlog)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch", lambda *a, **k: None)
    original = repair._get(
        repair.revision._data_block(path.read_text(encoding="utf-8"), "proposal-data"),
        repair.FIELD_PATHS["locations[0].local_rule"],
    )
    fixed = "The barrier lamps are already dimming and the crowd has gone quiet."
    prompts = []

    def _call(prompt, system, key):
        prompts.append(prompt)
        return json.dumps({"item_best_used_when": fixed, "skill_best_used_when": fixed,
                           "local_rule": original})

    monkeypatch.setattr(repair.author, "call_claude", _call)
    request_path = tmp_path / "2026-09-01-noted-request.json"
    request = {"scope": "all-built", "extra_fields": {
        "2026-08-30": {"locations[0].local_rule": "the second clause restates the first"}}}
    request_path.write_text(json.dumps(request), encoding="utf-8")

    with pytest.raises(RuntimeError, match="returned unchanged"):
        repair._apply_batch(request_path, request)

    assert "the second clause restates the first" in prompts[0], "the note must reach the model"


def test_a_stranded_receipt_is_found_so_the_publish_can_be_resumed(tmp_path, monkeypatch):
    # Run 33477217234 wrote 17 bundles to main and then died partway through
    # publishing on a Kind Robots timeout. Source-ahead-of-live is the safe
    # failure direction, but the request file had already been consumed, so no
    # later run could reach the receipt and finish the job. Every run now looks
    # for a receipt still carrying pending_live.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    folder = tmp_path / "projects" / "dream-cycle" / "prose-repairs"
    folder.mkdir(parents=True)
    (folder / "2026-09-01-done-applied.json").write_text(
        json.dumps({"status": "applied", "pending_live": []}), encoding="utf-8"
    )
    assert repair.stranded_receipt() is None, "a finished receipt is not stranded"

    stranded = folder / "2026-09-03-reward-census-applied.json"
    stranded.write_text(
        json.dumps({
            "status": "source-written",
            "pending_live": [{"path": "projects/dream-cycle/backlog/x.md", "fields": ["idea"]}],
        }),
        encoding="utf-8",
    )
    assert repair.stranded_receipt() == stranded


def test_resume_pending_is_a_no_op_when_nothing_is_stranded(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    (tmp_path / "projects" / "dream-cycle" / "prose-repairs").mkdir(parents=True)

    assert repair.main(["--resume-pending"]) == 0
    assert "waiting on a live publish" in capsys.readouterr().out


def test_an_empty_completion_retries_without_spending_a_correction_attempt(monkeypatch):
    # Run 33485900585 lost a 16-bundle batch to this: five bundles authored
    # cleanly, the sixth came back empty twice, and the all-or-nothing batch
    # discarded all of them. An empty completion carries nothing to correct, so
    # it is a transport failure, not a bad answer.
    monkeypatch.setattr(repair.time, "sleep", lambda *_: None)
    calls = []

    def _flaky(prompt, system, key):
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("Claude returned an empty completion.")
        return "recovered"

    monkeypatch.setattr(repair.author, "call_claude", _flaky)

    assert repair._call_with_transport_retries("p", "k") == "recovered"
    assert len(calls) == 3


def test_a_wrong_answer_is_not_treated_as_a_transport_failure(monkeypatch):
    # A response that arrived and was wrong belongs to the correction loop, which
    # can feed the complaint back into the prompt. Retrying it blindly here would
    # just repeat the same mistake with no new information.
    monkeypatch.setattr(repair.time, "sleep", lambda *_: None)
    calls = []

    def _wrong(prompt, system, key):
        calls.append(1)
        raise RuntimeError("model refused the request")

    monkeypatch.setattr(repair.author, "call_claude", _wrong)

    with pytest.raises(RuntimeError, match="refused"):
        repair._call_with_transport_retries("p", "k")
    assert len(calls) == 1, "a wrong answer must not consume the transport budget"


def test_one_failing_bundle_does_not_discard_the_others(tmp_path, monkeypatch):
    # Three batches in a row were thrown away because a single bundle came back
    # empty, taking 13 good repairs with them each time. Atomicity that matters
    # is per bundle: repaired-and-validated, or untouched and still flagged.
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    good = _built_bundle(backlog, name="2026-08-30-good.md")
    _built_bundle(backlog, name="2026-08-31-bad.md")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.revision, "_patch", lambda *a, **k: None)
    monkeypatch.setattr(repair.time, "sleep", lambda *_: None)
    fixed = "The barrier lamps are already dimming and the crowd has gone quiet."

    calls = []

    def _call(prompt, system, key):
        calls.append(1)
        # First bundle authors cleanly; the second is the one that comes back
        # empty, exhausting both its transport retries and its correction
        # attempts. The two fixtures render identical prompts, so order is the
        # only thing that can tell them apart here.
        if len(calls) > 1:
            raise RuntimeError("Claude returned an empty completion.")
        return json.dumps({"item_best_used_when": fixed, "skill_best_used_when": fixed})

    monkeypatch.setattr(repair.author, "call_claude", _call)
    request_path = tmp_path / "2026-09-05-partial-request.json"
    request_path.write_text(json.dumps({"scope": "all-built"}), encoding="utf-8")

    results = repair._apply_batch(request_path, json.loads(request_path.read_text()))

    assert len(results) == 1, "the healthy bundle must still be repaired"
    assert fixed in good.read_text(encoding="utf-8")
    receipt = json.loads((tmp_path / "2026-09-05-partial-applied.json").read_text())
    assert len(receipt["failed_bundles"]) == 1
    assert "empty completion" in receipt["failed_bundles"][0]["error"]


def test_a_batch_where_nothing_succeeds_still_fails_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(repair, "ROOT", tmp_path)
    backlog = tmp_path / "projects" / "dream-cycle" / "backlog"
    backlog.mkdir(parents=True)
    monkeypatch.setattr(repair, "BACKLOG", backlog)
    _built_bundle(backlog)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(repair.records, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(repair.time, "sleep", lambda *_: None)
    monkeypatch.setattr(repair.author, "call_claude",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("Claude returned an empty completion.")))
    request_path = tmp_path / "2026-09-05-none-request.json"
    request_path.write_text(json.dumps({"scope": "all-built"}), encoding="utf-8")

    with pytest.raises(RuntimeError, match="no bundle could be repaired"):
        repair._apply_batch(request_path, json.loads(request_path.read_text()))
