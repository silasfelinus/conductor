import json
from pathlib import Path

import scripts.apply_daily_dream_facets as assign


def write_bundle(path: Path):
    facets = {key: [{"id": index + 10, "title": key, "slug": key, "taxonomy": "GENRE"}]
              for index, key in enumerate(("vibe", "location", "character", "reward_item", "reward_skill", "scenario"))}
    proposal = {"seed_facets": {"version": 2, "elements": facets}}
    built = {"records": {"world": {"id": 1}, "locations": [{"id": 3}], "characters": [{"id": 4}], "rewards": [{"id": 5, "reward_type": "ITEM"}, {"id": 6, "reward_type": "SKILL"}], "scenarios": [{"id": 7}]}}
    path.write_text("---\nproposal: true\n---\n\n" f"<!-- proposal-data\n{json.dumps(proposal)}\n-->\n\n" f"<!-- built-data\n{json.dumps(built)}\n-->\n", encoding="utf-8")


def test_sidecar_applies_world_and_five_dependent_records(tmp_path, monkeypatch):
    path = tmp_path / "bundle.md"; write_bundle(path); calls = []
    def fake_put(endpoint, payload, token, dry_run=False):
        calls.append((endpoint, payload)); return {"success": True, "data": [{"id": value} for value in payload["facetIds"]]}
    monkeypatch.setattr(assign, "_put", fake_put)
    changed, status = assign.apply_file(path, "token")
    assert changed is True and status == "complete"
    assert [endpoint for endpoint, _ in calls] == ["/api/dreams/1/facets", "/api/dreams/3/facets", "/api/characters/4/facets", "/api/rewards/5/facets", "/api/rewards/6/facets", "/api/scenarios/7/facets"]
    built = assign._json_comment(assign.BUILT_RE, path.read_text(encoding="utf-8"))
    assert built["facet_assignments"]["status"] == "complete"
    assert len(built["facet_assignments"]["targets"]) == 6


def test_sidecar_is_idempotent_after_complete_assignment(tmp_path, monkeypatch):
    path = tmp_path / "bundle.md"; write_bundle(path)
    monkeypatch.setattr(assign, "_put", lambda *args, **kwargs: {"success": True, "data": []})
    assert assign.apply_file(path, "token") == (True, "complete")
    assert assign.apply_file(path, "token") == (False, "already complete")
