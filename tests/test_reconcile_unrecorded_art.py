"""Unrecorded art: lost ArtJob ids are found, written back, and strays become triage work.

Silas, 2026-11-11 PT: "we keep finding art that was requested and made but not linked ... it
should be both corrected and linked and be a part of the normal conductor agent task rotation".
"""

from datetime import datetime, timedelta, timezone

import yaml

import scripts.art_request_key as keys
import scripts.reconcile_unrecorded_art as rec

LANE = {"key": "krea", "engine": "krea2", "prompt": "prose", "suffix": "Painted gouache, bare surfaces."}


def _subject(key="cell-a", prose="A lizard welder on a bridge.", **extra):
    return {"key": key, "lane": "krea", "prompt_prose": prose, "seed": 7, "jobs": {}, "art": {}, **extra}


def _write_ledger(root, project="slime-city", name="ROUND-1.yaml", subjects=None):
    path = root / "projects" / project / "art" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"round": "r1", "project_slug": project, "lanes": [dict(LANE)], "subjects": subjects or [_subject()]}
    path.write_text("# a header kept verbatim\n" + yaml.safe_dump(data, sort_keys=False))
    return path


# ------------------------------------------------------------------ keys


def test_ledger_key_is_stable_and_ignores_curation_fields():
    subject = _subject()
    key = keys.ledger_cell_key("projects/x/art/R.yaml", LANE, subject)
    assert key.startswith("conductor:ledger:projects/x/art/R.yaml#cell-a@krea=")
    curated = dict(subject, jobs={"krea": 5}, art={"krea": {"status": "DONE"}}, review="keeper", rejected=[4])
    assert keys.ledger_cell_key("projects/x/art/R.yaml", LANE, curated) == key


def test_ledger_key_changes_when_the_render_changes():
    base = keys.ledger_cell_key("p.yaml", LANE, _subject())
    assert keys.ledger_cell_key("p.yaml", LANE, _subject(prose="Another scene.")) != base
    assert keys.ledger_cell_key("p.yaml", dict(LANE, suffix="Ink."), _subject()) != base
    assert keys.ledger_cell_key("p.yaml", LANE, _subject(seed=8)) != base


def test_request_key_tracks_force_and_skips_rows_without_id():
    row = {"id": "ruler-hooked-character-druid-sela", "prompt": "Portrait of Sela", "image_path": "a.webp"}
    key = keys.request_key(row)
    assert key.startswith("conductor:request:ruler-hooked-character-druid-sela=")
    assert keys.request_key(dict(row, last_art_job_id=9, status="pending")) == key
    assert keys.request_key(dict(row, force=True)) != key
    assert keys.request_key({"prompt": "x"}) is None


def test_keys_fit_the_server_pattern_and_length():
    long_subject = _subject(key="k" * 400 + " with spaces;")
    key = keys.ledger_cell_key("projects/x/art/" + "D" * 200 + ".yaml", LANE, long_subject)
    assert len(key) <= keys.KEY_MAX_LENGTH
    assert not keys._ALLOWED.search(key)


# ------------------------------------------------------------------ targets + keyed pass


def test_targets_cover_open_ledger_cells_and_pending_requests(tmp_path):
    _write_ledger(tmp_path, subjects=[_subject("open"), _subject("done", jobs={"krea": 3})])
    prompts = tmp_path / "projects" / "art-prompts.yaml"
    prompts.write_text(yaml.safe_dump({"requests": [
        {"id": "r-open", "prompt": "a", "image_path": "a.webp", "status": "pending"},
        {"id": "r-sent", "prompt": "b", "image_path": "b.webp", "status": "pending", "last_art_job_id": 4},
        {"id": "r-done", "prompt": "c", "image_path": "c.webp", "status": "done"},
    ]}))
    ledger_targets, _ = rec.ledger_targets(tmp_path)
    assert [t.subject["key"] for t in ledger_targets] == ["open"]
    assert [t.request["id"] for t in rec.request_targets(prompts)] == ["r-open"]


def test_lookup_reports_unavailable_before_the_endpoint_deploys():
    # Before kind_robots#5031 the path falls through to the site's HTML page.
    state, found = rec.lookup_keys(["k"], post=lambda body: (None, {"message": "JSONDecodeError: Expecting value"}))
    assert (state, found) == ("unavailable", {})
    state, found = rec.lookup_keys(["k"], post=lambda body: (200, {"success": True, "data": {"jobs": [
        {"requestKey": "k", "jobId": 5, "status": "DONE", "artImageId": 9}]}}))
    assert state == "ok" and found["k"]["jobId"] == 5


def test_apply_ledger_writes_job_and_art(tmp_path):
    path = _write_ledger(tmp_path)
    targets, loaded = rec.ledger_targets(tmp_path)
    targets[0].job = {"jobId": 67889, "status": "DONE", "artImageId": 269585, "via": "key"}
    rec.apply_ledger(targets[0])
    header, data = loaded[path]
    rec.ledgers.save_ledger(path, header, data)
    text = path.read_text()
    assert text.startswith("# a header kept verbatim\n")
    saved = yaml.safe_load(text)["subjects"][0]
    assert saved["jobs"] == {"krea": 67889}
    assert saved["art"] == {"krea": {"status": "DONE", "art_image_id": 269585}}


# ------------------------------------------------------------------ backfill


def test_prompt_match_prefers_newest_done_and_counts_duplicates(tmp_path):
    _write_ledger(tmp_path, subjects=[_subject("a", prose="Union Millwright bolts armor."), _subject("b", prose="A quiet dock.")])
    targets, _ = rec.ledger_targets(tmp_path)
    full = rec.ledgers.compose_prompt(LANE, targets[0].subject)
    jobs = [
        {"id": 10, "status": "DONE", "artImageId": 100, "prompt": full},
        {"id": 12, "status": "DONE", "artImageId": 120, "prompt": full + ", extra facet"},
        {"id": 13, "status": "FAILED", "artImageId": None, "prompt": full},
        {"id": 14, "status": "DONE", "artImageId": 140, "prompt": "unrelated"},
    ]
    matched, duplicates = rec.match_by_prompt(targets, jobs)
    assert matched == 1 and duplicates == 1
    assert targets[0].job["jobId"] == 12 and targets[0].job["via"] == "prompt"
    assert targets[1].job is None


def test_prompt_shared_by_two_cells_is_ambiguous_not_guessed(tmp_path):
    same = "A twin prompt rendered on two lanes."
    _write_ledger(tmp_path, subjects=[_subject("a", prose=same), _subject("b", prose=same)])
    targets, _ = rec.ledger_targets(tmp_path)
    prompt = rec.ledgers.compose_prompt(LANE, targets[0].subject)
    matched, _ = rec.match_by_prompt(targets, [{"id": 1, "status": "DONE", "prompt": prompt}])
    assert matched == 0 and all(t.ambiguous for t in targets)


def test_exact_prompt_beats_a_shorter_prompt_contained_in_it(tmp_path):
    _write_ledger(tmp_path, subjects=[_subject("short", prose="A dock."), _subject("long", prose="A dock. At night.")])
    targets, _ = rec.ledger_targets(tmp_path)
    short, long_ = (rec.ledgers.compose_prompt(LANE, t.subject) for t in targets)
    jobs = [{"id": 1, "status": "DONE", "prompt": long_}, {"id": 2, "status": "DONE", "prompt": short}]
    # "A dock., Painted..." is not inside "A dock. At night., Painted..." here, so make it so:
    jobs.append({"id": 3, "status": "DONE", "prompt": short + " " + long_})
    matched, _ = rec.match_by_prompt(targets, jobs)
    assert matched == 2
    assert {t.subject["key"]: t.job["jobId"] for t in targets} == {"short": 2, "long": 1}
    assert not any(t.ambiguous for t in targets)


# ------------------------------------------------------------------ strays


def test_find_strays_skips_referenced_young_and_foreign_jobs():
    old = (datetime.now(timezone.utc) - timedelta(hours=10)).isoformat()
    young = datetime.now(timezone.utc).isoformat()
    jobs = [
        {"id": 1, "status": "DONE", "projectSlug": "slime-city", "artImageId": 11, "createdAt": old},
        {"id": 2, "status": "DONE", "projectSlug": "slime-city", "artImageId": 22, "createdAt": old},
        {"id": 3, "status": "DONE", "projectSlug": "slime-city", "artImageId": 33, "createdAt": young},
        {"id": 4, "status": "DONE", "projectSlug": "not-a-project", "artImageId": 44, "createdAt": old},
        {"id": 5, "status": "DONE", "projectSlug": "slime-city", "artImageId": 55, "createdAt": old},
        {"id": 6, "status": "FAILED", "projectSlug": "slime-city", "artImageId": None, "createdAt": old},
    ]
    min_age = datetime.now(timezone.utc) - timedelta(hours=3)
    strays, extra = rec.find_strays(jobs, refs={22}, projects={"slime-city"}, claimed={5}, min_age=min_age)
    assert [j["id"] for j in strays] == [1] and extra == 0


def test_extra_renders_of_known_prompts_are_duplicates_not_strays(tmp_path):
    _write_ledger(tmp_path, subjects=[_subject("done", prose="Choirfish sings under the dock at dawn.", jobs={"krea": 3})])
    (tmp_path / "projects" / "art-prompts.yaml").write_text(yaml.safe_dump({"requests": [
        {"id": "r", "status": "done", "prompt": "Portrait of Sela the Keeper, druid of the lake.", "image_path": "a"}]}))
    known = rec.known_prompts(tmp_path, tmp_path / "projects" / "art-prompts.yaml")
    old = (datetime.now(timezone.utc) - timedelta(hours=10)).isoformat()
    full = rec.ledgers.compose_prompt(LANE, {"prompt_prose": "Choirfish sings under the dock at dawn."})
    jobs = [
        {"id": 1, "status": "DONE", "projectSlug": "x", "artImageId": 9, "createdAt": old, "prompt": full},
        {"id": 2, "status": "DONE", "projectSlug": "x", "artImageId": 8, "createdAt": old,
         "prompt": "Portrait of Sela the Keeper, druid of the lake. psychedelic style"},
        {"id": 3, "status": "DONE", "projectSlug": "x", "artImageId": 7, "createdAt": old, "prompt": "A brand new idea nobody asked for in Conductor."},
    ]
    min_age = datetime.now(timezone.utc) - timedelta(hours=3)
    strays, extra = rec.find_strays(jobs, set(), {"x"}, set(), min_age, known)
    assert [j["id"] for j in strays] == [3] and extra == 2


def test_write_strays_appends_without_duplicates_and_is_triage_work(tmp_path):
    job = {"id": 67735, "artImageId": 269077, "projectSlug": "monstress-convention",
           "prompt": "hand-painted  adventure art", "designer": None, "createdAt": "2026-11-11T10:04:12Z"}
    rec.write_strays([job], "2026-11-11", tmp_path)
    rec.write_strays([job, dict(job, id=67736, artImageId=269078)], "2026-11-11", tmp_path)
    path = tmp_path / "projects" / "monstress-convention" / "art" / "RECOVERED-2026-11-11.yaml"
    data = yaml.safe_load(path.read_text())
    assert data["auto_submit"] is False
    assert [s["jobs"]["recovered"] for s in data["subjects"]] == [67735, 67736]
    assert data["subjects"][0]["art"]["recovered"]["art_image_id"] == 269077
    assert path.read_text().startswith("# Renders Kind Robots finished")
    assert rec.untriaged_recovered(tmp_path) == [
        {"ledger": "projects/monstress-convention/art/RECOVERED-2026-11-11.yaml", "untriaged": 2, "subjects": 2}
    ]
    data["subjects"][0]["triage"] = "duplicate"
    data["subjects"][1]["triage"] = "linked"
    path.write_text(yaml.safe_dump(data))
    assert rec.untriaged_recovered(tmp_path) == []


def test_recovered_ledgers_are_never_reopened_as_unrecorded_cells(tmp_path):
    rec.write_strays([{"id": 1, "artImageId": 2, "projectSlug": "x", "prompt": "p", "createdAt": None}], "2026-11-11", tmp_path)
    targets, _ = rec.ledger_targets(tmp_path)
    assert targets == []


# ------------------------------------------------------------------ rotation


def test_actionable_names_triage_staleness_and_missing_lookup(tmp_path):
    now = datetime(2026, 11, 12, 12, tzinfo=timezone.utc)
    assert rec.actionable({}, tmp_path, now) == []
    fresh = {"generated_at": "2026-11-12T11:30:00Z", "lookup": "ok", "lookup_unavailable_since": None}
    assert rec.actionable(fresh, tmp_path, now) == []
    stale = dict(fresh, generated_at="2026-11-12T01:00:00Z")
    assert "stopped running" in rec.actionable(stale, tmp_path, now)[0]
    no_lookup = dict(fresh, lookup="unavailable", lookup_unavailable_since="2026-11-09T00:00:00Z")
    assert "unavailable for over 48h" in rec.actionable(no_lookup, tmp_path, now)[0]
    rec.write_strays([{"id": 1, "artImageId": 2, "projectSlug": "x", "prompt": "p", "createdAt": None}], "2026-11-11", tmp_path)
    assert rec.actionable(fresh, tmp_path, now)[0].startswith("triage 1 unrecorded render(s)")
