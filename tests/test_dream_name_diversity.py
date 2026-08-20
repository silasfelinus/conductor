"""Regression coverage for daily-dream naming diversity.

The failure this protects against is not one forbidden name. It is the author
forgetting its own recent vocabulary and producing close remixes such as
Vex Thistlewick -> Vex Thistlemaw.
"""

import json

import scripts.author_dream_proposal as authoring


def _proposal_block(**overrides):
    data = {
        "title": "Archive Dream",
        "vibe": {"title": "Archive Vibe"},
        "locations": [{"title": "Archive Hall"}],
        "characters": [{"name": "Vex Thistlewick"}],
        "rewards": [{"name": "Archive Key"}, {"name": "Archive Skill"}],
        "scenarios": [{"title": "Archive Test"}],
    }
    data.update(overrides)
    return "<!-- proposal-data\n" + json.dumps(data) + "\n-->\n"


def test_recent_name_history_reads_the_persisted_proposal_archive(tmp_path):
    (tmp_path / "2026-08-01-one.md").write_text(
        _proposal_block(), encoding="utf-8"
    )
    (tmp_path / "2026-08-02-two.md").write_text(
        _proposal_block(
            title="Second Dream",
            vibe={"title": "Second Vibe"},
            locations=[{"title": "Second Place"}],
            characters=[{"name": "Odalys Marsh"}],
            rewards=[{"name": "Second Item"}, {"name": "Second Skill"}],
            scenarios=[{"title": "Second Scenario"}],
        ),
        encoding="utf-8",
    )
    # Same-day/future proposals must not leak into the author's memory.
    (tmp_path / "2026-08-03-future.md").write_text(
        _proposal_block(characters=[{"name": "Future Person"}]), encoding="utf-8"
    )

    history = authoring.recent_name_history(
        "2026-08-03", backlog_dir=tmp_path
    )

    assert history["characters"] == ["Vex Thistlewick", "Odalys Marsh"]
    assert history["dreams"] == [
        "Archive Dream",
        "Archive Vibe",
        "Second Dream",
        "Second Vibe",
    ]
    assert "Future Person" not in history["characters"]


def test_name_guard_catches_vex_thistle_style_remixes():
    complaints = authoring.name_diversity_complaints(
        "Vex Thistlemaw", ["Vex Thistlewick"]
    )

    assert any("given name" in complaint for complaint in complaints)
    assert any("surname" in complaint for complaint in complaints)


def test_name_guard_catches_near_spelled_given_name():
    complaints = authoring.name_diversity_complaints(
        "Vexa Alder", ["Vex Thistlewick"]
    )
    assert any("given name" in complaint for complaint in complaints)


def test_name_guard_allows_a_genuinely_different_name():
    assert authoring.name_diversity_complaints(
        "Odalys Marsh", ["Vex Thistlewick", "Portia Fivetooth"]
    ) == []


def test_naming_direction_rotates_across_consecutive_days():
    directions = {
        authoring.naming_direction(f"2026-08-{day:02d}")
        for day in range(20, 25)
    }
    assert directions == set(authoring.NAMING_DIRECTIONS)


def test_brief_prompt_carries_recent_names_as_spent_vocabulary():
    brief = {
        "proposal_date": "2026-08-20",
        "seed_facets": {"version": 2},
        "instructions": ["Keep the bundle coherent."],
    }
    history = {category: [] for category in authoring.HISTORY_CATEGORIES}
    history["characters"] = ["Vex Thistlewick", "Portia Fivetooth"]
    history["locations"] = ["Ninth Ledger Flood Deck"]

    prompt = authoring._brief_prompt(brief, history)

    assert "spent vocabulary" in prompt
    assert "Vex Thistlewick" in prompt
    assert "Portia Fivetooth" in prompt
    assert "Ninth Ledger Flood Deck" in prompt
    assert "Character naming direction for today" in prompt


def test_archive_echo_is_retried_with_a_specific_naming_complaint(monkeypatch):
    brief = {
        "proposal_date": "2026-08-20",
        "seed_facets": {"version": 2},
        "instructions": [],
    }
    history = {category: [] for category in authoring.HISTORY_CATEGORIES}
    history["characters"] = ["Vex Thistlewick"]
    prompts = []

    monkeypatch.setattr(authoring.dreams, "build_brief", lambda day: brief)
    monkeypatch.setattr(authoring, "recent_name_history", lambda day: history)
    monkeypatch.setattr(authoring.dreams, "existing_slugs", lambda: [])
    monkeypatch.setattr(authoring.dreams, "normalize", lambda proposal, slugs: proposal)
    monkeypatch.setattr(authoring.dreams, "validate_proposal", lambda proposal: [])

    def fake_call(prompt, *args, **kwargs):
        prompts.append(prompt)
        name = "Vex Thistlemaw" if len(prompts) == 1 else "Odalys Marsh"
        return json.dumps({"characters": [{"name": name}]})

    monkeypatch.setattr(authoring, "call_claude", fake_call)

    proposal = authoring.author("2026-08-20", "key", verbose=False)

    assert proposal["characters"][0]["name"] == "Odalys Marsh"
    assert len(prompts) == 2
    assert "failed validation" in prompts[1]
    assert "different given-name root" in prompts[1]
    assert "different surname construction" in prompts[1]
