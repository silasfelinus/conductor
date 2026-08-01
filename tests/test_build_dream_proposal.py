import copy
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

import scripts.build_dream_proposal as bdp


def fallback_catalog():
    return {key: [bdp._fallback(key)[i] for i in range(len(rows))] for key, rows in bdp.FALLBACK_FACETS.items()}


def test_target_date_is_pacific_calendar_date():
    instant = datetime(2026, 8, 1, 1, 30, tzinfo=ZoneInfo("UTC"))
    assert bdp._target_date(instant) == "2026-07-31"


def test_facet_seed_plan_is_deterministic_and_connected():
    first = bdp.facet_seed_plan("2026-07-31", catalog=fallback_catalog())
    second = bdp.facet_seed_plan("2026-07-31", catalog=fallback_catalog())
    assert first == second
    assert len(first["umbrella"]["genres"]) == 2
    assert first["umbrella"]["creature"] in first["elements"]["location"]
    assert first["umbrella"]["creature"] in first["elements"]["character"]
    assert first["shared"]["material"] in first["elements"]["location"]
    assert first["shared"]["material"] in first["elements"]["reward_item"]
    assert first["extra_genres"]["scenario"] in first["elements"]["scenario"]
    assert len({facet["slug"] for facet in first["extra_genres"].values()}) == 5


def test_sample_enforces_exact_six_asset_contract():
    assert bdp.validate_proposal(bdp.SAMPLE_PROPOSAL) == []
    assert len(bdp.SAMPLE_PROPOSAL["locations"]) == 1
    assert len(bdp.SAMPLE_PROPOSAL["characters"]) == 1
    assert len(bdp.SAMPLE_PROPOSAL["rewards"]) == 2
    assert len(bdp.SAMPLE_PROPOSAL["scenarios"]) == 1
    assert sorted(row["reward_type"] for row in bdp.SAMPLE_PROPOSAL["rewards"]) == ["ITEM", "SKILL"]
    assert "narrator" not in bdp.SAMPLE_PROPOSAL


def test_validator_rejects_detached_scenario_and_wrong_counts():
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    proposal["locations"].append(copy.deepcopy(proposal["locations"][0]))
    proposal["scenarios"][0]["setup"] = "A completely unrelated event occurs elsewhere."
    problems = bdp.validate_proposal(proposal)
    assert "locations must be a list of exactly 1" in problems
    assert any("scenario setup must name the vibe" in problem for problem in problems)
    assert any("scenario setup must name the location" in problem for problem in problems)
    assert any("scenario setup must name the character" in problem for problem in problems)


def test_markdown_prints_seed_facets_and_six_sections():
    rendered = bdp.render_markdown(bdp.SAMPLE_PROPOSAL, "2026-07-31")
    assert "## Seed Facets" in rendered
    assert "## Dream vibe (1)" in rendered
    assert "## Dream location (1)" in rendered
    assert "## Character (1)" in rendered
    assert "## Reward item (1)" in rendered
    assert "## Reward skill (1)" in rendered
    assert "## Scenario (1, authored last)" in rendered
    assert '"seed_facets"' in rendered


def test_write_proposal_rechecks_remote_before_writing(tmp_path, monkeypatch):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    monkeypatch.setattr(bdp, "fetch_main", lambda quiet=True: True)
    monkeypatch.setattr(bdp, "remote_proposal_for", lambda date: "already-there.md")
    assert bdp.write_proposal(copy.deepcopy(bdp.SAMPLE_PROPOSAL), date="2026-07-31") is None
    assert list(tmp_path.iterdir()) == []


def test_write_proposal_normalizes_duplicate_slug(tmp_path, monkeypatch):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    existing = tmp_path / "2026-07-30-prism-appeal.md"
    existing.write_text("---\nslug: prism-appeal\nproposal: true\nproposal_date: '2026-07-30'\n---\n", encoding="utf-8")
    proposal = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    path = bdp.write_proposal(proposal, date="2026-07-31", fetch=False)
    assert path is not None
    assert path.name == "2026-07-31-prism-appeal-2.md"


def test_invalid_proposal_raises_before_file_write(tmp_path, monkeypatch):
    monkeypatch.setattr(bdp, "BACKLOG", tmp_path)
    bad = copy.deepcopy(bdp.SAMPLE_PROPOSAL)
    bad["rewards"] = bad["rewards"][:1]
    with pytest.raises(ValueError, match="rewards must be a list of exactly 2"):
        bdp.write_proposal(bad, date="2026-07-31", fetch=False)
