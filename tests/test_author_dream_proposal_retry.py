"""Regression tests for parser failures in unattended Daily Dream authoring."""

import json

import scripts.author_dream_proposal as authoring


DAY = "2026-08-22"


def test_malformed_json_consumes_the_existing_retry_budget(monkeypatch):
    brief = {
        "proposal_date": DAY,
        "seed_facets": {"version": 1, "umbrella": {"genres": []}},
        "instructions": [],
    }
    history = {category: [] for category in authoring.HISTORY_CATEGORIES}
    prompts: list[str] = []
    replies = iter(
        [
            '{"title": "broken" "characters": []}',
            json.dumps({"title": "recovered", "characters": []}),
        ]
    )

    monkeypatch.setattr(authoring.dreams, "build_brief", lambda day: brief)
    monkeypatch.setattr(authoring, "recent_name_history", lambda day: history)
    monkeypatch.setattr(authoring.dreams, "existing_slugs", lambda: set())
    monkeypatch.setattr(authoring.dreams, "normalize", lambda proposal, slugs: proposal)
    monkeypatch.setattr(authoring.dreams, "validate_proposal", lambda proposal: [])

    def fake_call(prompt, *args, **kwargs):
        prompts.append(prompt)
        return next(replies)

    monkeypatch.setattr(authoring, "call_claude", fake_call)

    proposal = authoring.author(DAY, "key", verbose=False)

    assert proposal["title"] == "recovered"
    assert proposal["seed_facets"] == brief["seed_facets"]
    assert len(prompts) == authoring.MAX_ATTEMPTS == 2
    assert "completion was not valid JSON" in prompts[1]
