"""The live Facet coverage check must actually fail on the shape it was written for.

A check that has only ever passed proves nothing, and this one exists precisely
because the previous guard (apply_daily_dream_facets.py's own recorded status)
reported "complete" over 36 empty Characters for six weeks. So the case that
matters here is the failing one.
"""

import json

import pytest

import scripts.check_live_facet_coverage as coverage


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    """One built bundle with the six Facet targets a daily dream produces."""
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    built = {
        "facet_assignments": {
            "status": "complete",
            "errors": [],
            "targets": [
                {"element": "vibe", "model": "Dream", "record_id": 1,
                 "facet_ids": [10, 11, 12, 13], "facet_keys": ["a", "b", "c", "d"]},
                {"element": "location", "model": "Dream", "record_id": 2,
                 "facet_ids": [10, 11], "facet_keys": ["a", "b"]},
                {"element": "character", "model": "Character", "record_id": 3,
                 "facet_ids": [10, 11, 12], "facet_keys": ["a", "b", "c"]},
                {"element": "reward_item", "model": "Reward", "record_id": 4,
                 "facet_ids": [10], "facet_keys": ["a"]},
                {"element": "reward_skill", "model": "Reward", "record_id": 5,
                 "facet_ids": [10], "facet_keys": ["a"]},
                {"element": "scenario", "model": "Scenario", "record_id": 6,
                 "facet_ids": [10, 11], "facet_keys": ["a", "b"]},
            ],
        }
    }
    (backlog / "bundle.md").write_text(
        "---\nproposal: true\n---\n\n"
        f"<!-- built-data\n{json.dumps(built)}\n-->\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(coverage, "BACKLOG", backlog)
    monkeypatch.setenv("KR_API_TOKEN", "fake-token")
    return backlog


def _rows(count):
    return {"success": True, "data": [{"id": 100 + i} for i in range(count)]}


def test_passes_when_every_record_carries_what_it_was_built_with(bundle, monkeypatch):
    by_path = {"/api/dreams/1/facets": 4, "/api/dreams/2/facets": 2,
               "/api/characters/3/facets": 3, "/api/rewards/4/facets": 1,
               "/api/rewards/5/facets": 1, "/api/scenarios/6/facets": 2}
    monkeypatch.setattr(coverage, "_get", lambda path, token, **kw: _rows(by_path[path]))
    assert coverage.main([]) == 0


def test_fails_on_the_empty_character_that_prompted_this(bundle, monkeypatch, capsys):
    """The exact 2026-09-02 shape: everything green except the Character."""
    def fake_get(path, token, **kwargs):
        if "/characters/" in path:
            return {"success": True, "data": []}
        return _rows(4)

    monkeypatch.setattr(coverage, "_get", fake_get)
    assert coverage.main([]) == 1

    out = capsys.readouterr().out
    assert "carry NO Facets they were built with" in out
    assert "Character #3" in out
    assert "character        1 empty / 1" in out


def test_fails_when_a_record_is_short_rather_than_empty(bundle, monkeypatch, capsys):
    """A record that lost SOME links is drift too, not just a fully empty one."""
    def fake_get(path, token, **kwargs):
        return _rows(1) if "/dreams/1/" in path else _rows(4)

    monkeypatch.setattr(coverage, "_get", fake_get)
    assert coverage.main([]) == 1
    assert "requested 4, live 1" in capsys.readouterr().out


def test_no_token_is_unresolved_not_clean(bundle, monkeypatch):
    """Exit 2, matching check_project_scaffold_drift.py -- never a vacuous pass."""
    monkeypatch.delenv("KR_API_TOKEN", raising=False)
    assert coverage.main([]) == 2


def test_an_unreachable_record_is_unresolved_not_clean(bundle, monkeypatch):
    monkeypatch.setattr(
        coverage, "_get",
        lambda path, token, **kw: {"success": False, "message": "HTTP 502", "data": None},
    )
    assert coverage.main([]) == 2
