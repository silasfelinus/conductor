import scripts.import_comic_studio as importer


def test_payload_covers_both_rounds_and_checks_round2_request_ids():
    payload = importer.build_payload()
    keys = {slot["key"] for slot in payload["slots"]}
    entity_keys = {entity["key"] for entity in payload["entities"]}
    assert "r3-komodo-maw" in keys and "r2-kid-08-fennec" in keys
    assert all(slot["entityKey"] in entity_keys for slot in payload["slots"])
    assert all(attempt["slotKey"] in keys for attempt in payload["attempts"])
    job_ids = [attempt["artJobId"] for attempt in payload["attempts"]]
    assert len(job_ids) == len(frozenset(job_ids))
    round2 = [a for a in payload["attempts"] if a["slotKey"].startswith("r2-")]
    assert round2 and all(a["expectRequestId"].endswith(a["slotKey"][3:]) for a in round2)
    secret = [e for e in payload["entities"] if e["secretUntil"]]
    assert [e["key"] for e in secret] == ["human-ruins"]
    assert "fennec" in payload["series"]["notes"].lower()


def test_cast_slots_carry_the_locked_picks_as_selected():
    payload = importer.build_payload()
    cast = {s["key"]: s for s in payload["slots"] if s["key"].startswith("cast-")}
    assert len(cast) == 42
    selected = {a["slotKey"] for a in payload["attempts"] if a.get("verdict") == "selected"}
    assert "cast-zuzu-front" in selected and "cast-coyote-stump-bandaged" in selected
    assert "Same render as cast-zuzu-profile-left" in cast["cast-zuzu-profile-right"]["notes"]
    assert "cast-zuzu-profile-right" not in selected
