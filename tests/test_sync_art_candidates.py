"""Every render Conductor knows about becomes a candidate for its art slot; true duplicates go.

Silas, 2026-11-11 PT: "support having multiple art sources for art ... manageable from a back
end ... If the art is actually duplicated (same seed), they can be deleted."
"""

import yaml

import scripts.sync_art_candidates as sync

LANE_A = {"key": "krea", "engine": "krea2", "prompt": "prose", "suffix": "Painted gouache."}
LANE_B = {"key": "arthemy", "engine": "comfy", "prompt": "prose", "suffix": "Painted gouache."}


def _ledger(root, name, subjects, project="slime-city", lanes=(LANE_A,)):
    path = root / "projects" / project / "art" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"round": name, "project_slug": project, "lanes": [dict(l) for l in lanes], "subjects": subjects}
    path.write_text("# header\n" + yaml.safe_dump(data, sort_keys=False))
    return path


def _subject(key, asset=None, image=None, job=None, prose="A lizard welder on a bridge at dusk."):
    subject = {"key": key, "prompt_prose": prose, "jobs": {}, "art": {}}
    if asset:
        subject["asset"] = asset
    if image:
        subject["jobs"] = {"krea": job or image + 1000}
        subject["art"] = {"krea": {"status": "DONE", "art_image_id": image}}
    return subject


def test_slot_keys_are_project_namespaced():
    assert sync.project_slot("slime-city", "slime-city/cards/x") == "slime-city/cards/x"
    assert sync.project_slot("emperor-of-dust", "outcomes/a/b") == "emperor-of-dust/outcomes/a/b"
    assert sync.request_slot({"project_slug": "ruler-hooked",
                              "image_path": "public/images/ruler-hooked/characters/druid-sela.webp"}) \
        == "ruler-hooked/characters/druid-sela"
    assert sync.ledger_slot("x", "projects/x/art/R-1.yaml", {"key": "s"}, {"key": "l"}) == "x/ledger/R-1/s@l"


def test_redo_rounds_of_one_asset_share_a_slot_and_unchanged_ledgers_are_skipped(tmp_path):
    _ledger(tmp_path, "ROUND-1.yaml", [_subject("a1", asset="slime-city/cards/rivet", image=11),
                                       _subject("pending", asset="slime-city/cards/other")])
    _ledger(tmp_path, "REDO-1.yaml", [_subject("a1-redo", asset="slime-city/cards/rivet", image=12)])
    found, hashes = sync.ledger_candidates(tmp_path)
    assert sorted((c["slotKey"], c["artImageId"]) for c in found) == [
        ("slime-city/cards/rivet", 11), ("slime-city/cards/rivet", 12)]
    assert all(c["source"] == "conductor-ledger" and c["artJobId"] for c in found)
    again, _ = sync.ledger_candidates(tmp_path, synced=hashes)
    assert again == []


def test_harvest_matches_unrecorded_renders_and_chooses_the_recorded_job(tmp_path):
    _ledger(tmp_path, "R.yaml", [_subject("s", asset="slime-city/cards/rivet", prose="Rivet, a welder lizard on a girder.")])
    prompts = tmp_path / "projects" / "art-prompts.yaml"
    prompts.write_text(yaml.safe_dump({"requests": [{
        "id": "ruler-hooked-character-druid-sela", "project_slug": "ruler-hooked", "status": "pending",
        "image_path": "public/images/ruler-hooked/characters/druid-sela.webp", "last_art_job_id": 501,
        "prompt": "Portrait of Sela the Keeper, druid preservationist of a lakeside kingdom."}]}))
    targets = sync.prompt_targets(tmp_path, prompts)
    sela = "Portrait of Sela the Keeper, druid preservationist of a lakeside kingdom. psychedelic style"
    jobs = [
        {"id": 500, "status": "DONE", "artImageId": 9000, "projectSlug": "ruler-hooked", "prompt": sela},
        {"id": 501, "status": "DONE", "artImageId": 9001, "projectSlug": "ruler-hooked", "prompt": sela},
        {"id": 502, "status": "FAILED", "artImageId": None, "projectSlug": "ruler-hooked", "prompt": sela},
        {"id": 503, "status": "DONE", "artImageId": 9003, "projectSlug": "ruler-hooked", "prompt": "Something else entirely here."},
    ]
    found = sync.match_jobs(targets["ruler-hooked"], jobs)
    assert [(c["artImageId"], c["selectIfEmpty"]) for c in found] == [(9000, False), (9001, True)]
    assert {c["slotKey"] for c in found} == {"ruler-hooked/characters/druid-sela"}
    ledger_prompt = sync.rec.ledgers.compose_prompt(LANE_A, {"prompt_prose": "Rivet, a welder lizard on a girder."})
    found = sync.match_jobs(targets["slime-city"], [{"id": 7, "status": "DONE", "artImageId": 70, "projectSlug": "slime-city",
                                                     "prompt": ledger_prompt}])
    assert found[0]["slotKey"] == "slime-city/cards/rivet"


def test_a_prompt_shared_by_two_slots_is_not_guessed(tmp_path):
    _ledger(tmp_path, "R.yaml", [_subject("a", asset="p/one", prose="Same words twice over here."),
                                 _subject("b", asset="p/two", prose="Same words twice over here.")], project="p")
    targets = sync.prompt_targets(tmp_path, tmp_path / "none.yaml")
    prompt = sync.rec.ledgers.compose_prompt(LANE_A, {"prompt_prose": "Same words twice over here."})
    assert sync.match_jobs(targets["p"], [{"id": 1, "status": "DONE", "artImageId": 2, "prompt": prompt}]) == []


def test_register_batches_and_reports_an_undeployed_backend():
    sent = []

    def ok(path, body):
        sent.append(len(body["candidates"]))
        return 200, {"success": True, "data": {"results": [{"status": "created"}] * len(body["candidates"])}}

    outcome, created = sync.register([{"slotKey": "a", "artImageId": i} for i in range(450)], send=ok)
    assert (outcome, created, sent) == ("ok", 450, [400, 50])
    outcome, _ = sync.register([{"slotKey": "a", "artImageId": 1}],
                               send=lambda p, b: (None, {"message": "JSONDecodeError: Expecting value"}))
    assert outcome == "unavailable"


def test_dedupe_protects_referenced_ids_and_only_applies_with_removals():
    calls = []
    plan = {"success": True, "data": {"slots": [{"groups": [
        {"keepArtImageId": 10, "removeArtImageIds": [11, 12]},
        {"keepArtImageId": 20, "removeArtImageIds": [21]},
    ]}]}}

    def send(path, body):
        calls.append(body)
        if body.get("apply"):
            return 200, {"success": True, "data": {"removed": 2}}
        return 200, plan

    planned, removed = sync.dedupe(["slime-city"], refs={12, 99}, apply=True, send=send)
    assert (planned, removed) == (2, 2)
    assert calls[1] == {"projectSlug": "slime-city", "apply": True, "protectArtImageIds": [12]}

    calls.clear()
    sync.dedupe(["x"], refs=set(), apply=True, send=lambda p, b: (calls.append(b), (200, {"success": True, "data": {"slots": []}}))[1])
    assert len(calls) == 1 and calls[0]["apply"] is False
