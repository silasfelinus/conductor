"""Contract and creative-diversity tests for scripts/author_dream_proposal.py."""
import json
from pathlib import Path

import pytest

import scripts.author_dream_proposal as authoring

dreams = authoring.dreams
DAY = "2026-08-14"


def _valid_bundle(brief):
    return {
        "title": "Thunder Orchard Run",
        "slug": "thunder-orchard-run",
        "idea": "A courier crosses a levitating orchard while lightning predators tear open the storm canopy.",
        "vibe": {
            "title": "Live Current",
            "line": "Every branch stores a storm and every leap can release it.",
            "art_direction": (
                "Black fruit trees floating above a violet storm shelf, silver lightning crawling "
                "between exposed roots, wind flattening long grass below."
            ),
        },
        "locations": [{
            "title": "Stormglass Arena",
            "known_for": (
                "Floating fruit trees braid their exposed roots through captive lightning above the arena."
            ),
            "local_rule": (
                "Touching the ground wakes the lightning predators sleeping below the grass."
            ),
            "best_scene": (
                "Three trees collide overhead and release a rolling sphere of blue fire across the canopy."
            ),
            "art_direction": (
                "A broken ring of levitating black-barked trees above waist-high grass, forked "
                "lightning trapped in transparent roots, a bruised purple sky."
            ),
        }],
        "characters": [{
            "name": "Mira Sol",
            "role_drive": (
                "She has to deliver a living storm-seed across the canopy before the whole "
                "arena collapses under it."
            ),
            "carries": (
                "A copper sling at her back holds a fist-sized blue storm-seed."
            ),
            "complication": (
                "Every burst of speed she needs to make the run hatches the seed a little "
                "further open."
            ),
            "look": (
                "A lean courier in a rain-dark flight suit with copper knee braces, close-cropped "
                "hair blown sideways, translucent goggles lit blue from below."
            ),
        }],
        "rewards": [
            {
                "name": "Stormseed Sling",
                "reward_type": "ITEM",
                "rarity": "RARE",
                "grants": "It catches one bolt of lightning and redirects its momentum.",
                "best_used_when": "Use it when a jump falls short or a predator closes from below.",
                "catch": "The sling grows hot enough to scorch whoever carries it next.",
                "look": (
                    "A forearm-length copper sling with braided black cord, its cup holding a "
                    "glass-blue seed veined by tiny internal lightning."
                ),
            },
            {
                "name": "Branchstep",
                "reward_type": "SKILL",
                "rarity": "UNCOMMON",
                "grants": "It turns any falling branch into one extra midair step.",
                "best_used_when": "Use it when crossing a gap with nothing solid beneath it.",
                "catch": "The branch explodes into sparks the moment the step lands.",
                "look": (
                    "A boot sole meeting a falling black branch in midair as the impact blooms "
                    "into a bright circular shockwave of blue sparks."
                ),
            },
        ],
        "scenarios": [{
            "title": "The Canopy Breaks",
            "setup": (
                "Under Live Current, Mira Sol races across Stormglass Arena as the orchard splits "
                "apart and the last safe branch falls toward the lightning predators."
            ),
        }],
        "seed_facets": brief["seed_facets"],
    }


@pytest.fixture(scope="module")
def _live_brief():
    return dreams.build_brief(DAY)


@pytest.fixture
def brief(monkeypatch, _live_brief):
    frozen = json.loads(json.dumps(_live_brief))
    monkeypatch.setattr(dreams, "build_brief", lambda day=None, catalog=None: frozen)
    return frozen


@pytest.fixture
def no_history(monkeypatch):
    monkeypatch.setattr(
        authoring,
        "recent_name_history",
        lambda *a, **k: {category: [] for category in authoring.HISTORY_CATEGORIES},
    )
    monkeypatch.setattr(authoring, "recent_premise_history", lambda *a, **k: [])


def test_authored_bundle_passes_the_same_validator_a_human_bundle_does(monkeypatch, brief, no_history):
    monkeypatch.setattr(authoring, "call_claude", lambda *a, **k: json.dumps(_valid_bundle(brief)))
    proposal = authoring.author(DAY, "key", verbose=False)
    assert dreams.validate_proposal(dreams.normalize(proposal, dreams.existing_slugs())) == []


def test_seed_facets_are_ours_not_the_models(monkeypatch, brief, no_history):
    tampered = _valid_bundle(brief)
    tampered["seed_facets"] = {"version": 2, "umbrella": {"genres": []}}
    monkeypatch.setattr(authoring, "call_claude", lambda *a, **k: json.dumps(tampered))
    proposal = authoring.author(DAY, "key", verbose=False)
    assert proposal["seed_facets"] == brief["seed_facets"]


def test_a_narrator_is_stripped(monkeypatch, brief, no_history):
    with_narrator = _valid_bundle(brief)
    with_narrator["narrator"] = {"name": "The Archivist"}
    monkeypatch.setattr(authoring, "call_claude", lambda *a, **k: json.dumps(with_narrator))
    proposal = authoring.author(DAY, "key", verbose=False)
    assert "narrator" not in proposal


def test_invalid_bundle_is_retried_with_validator_complaints(monkeypatch, brief, no_history):
    broken = _valid_bundle(brief)
    broken["scenarios"][0]["setup"] = "Something happens somewhere to someone."
    prompts = []

    def fake(prompt, *a, **k):
        prompts.append(prompt)
        return json.dumps(broken if len(prompts) == 1 else _valid_bundle(brief))

    monkeypatch.setattr(authoring, "call_claude", fake)
    proposal = authoring.author(DAY, "key", verbose=False)
    assert len(prompts) == 2
    assert "failed validation" in prompts[1]
    assert "Mira Sol" in prompts[1]
    assert proposal["scenarios"][0]["title"] == "The Canopy Breaks"


def test_gives_up_rather_than_writing_a_bad_bundle(monkeypatch, brief, no_history):
    broken = _valid_bundle(brief)
    broken["rewards"] = [broken["rewards"][0]]
    monkeypatch.setattr(authoring, "call_claude", lambda *a, **k: json.dumps(broken))
    with pytest.raises(RuntimeError, match="Could not author a valid proposal"):
        authoring.author(DAY, "key", verbose=False)


def test_already_authored_is_success_not_failure(monkeypatch, capsys):
    monkeypatch.setattr(dreams, "proposal_exists_for", lambda day: True)
    monkeypatch.setattr(authoring, "call_claude", lambda *a, **k: pytest.fail("must not author"))
    assert authoring.main(["--date", DAY, "--no-fetch"]) == 0
    assert "already exists" in capsys.readouterr().out


def test_missing_api_key_fails_loudly_and_writes_nothing(monkeypatch, capsys):
    monkeypatch.setattr(dreams, "proposal_exists_for", lambda day: False)
    monkeypatch.setattr(dreams, "write_proposal", lambda *a, **k: pytest.fail("must not write"))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert authoring.main(["--date", DAY, "--no-fetch"]) == 1
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


def test_api_failure_is_reported_not_swallowed(monkeypatch, capsys):
    monkeypatch.setattr(dreams, "proposal_exists_for", lambda day: False)
    monkeypatch.setattr(dreams, "write_proposal", lambda *a, **k: pytest.fail("must not write"))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "key")

    def boom(*a, **k):
        raise RuntimeError("Claude returned an empty completion.")

    monkeypatch.setattr(authoring, "call_claude", boom)
    assert authoring.main(["--date", DAY, "--no-fetch"]) == 1
    assert "Could not author" in capsys.readouterr().err


@pytest.mark.parametrize("reply", [
    '```json\n{"a": 1}\n```',
    'Here you go:\n{"a": 1}',
    '{"a": 1}',
])
def test_parse_json_object_tolerates_a_chatty_or_fenced_reply(reply):
    assert authoring.parse_json_object(reply) == {"a": 1}


@pytest.mark.parametrize("reply", ["no json here", "", "{ truncated"])
def test_parse_json_object_rejects_junk(reply):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        authoring.parse_json_object(reply)


def test_story_direction_rotates_independently_from_naming_direction():
    story = [authoring.story_direction(f"2026-08-{day:02d}") for day in range(1, 21)]
    names = [authoring.naming_direction(f"2026-08-{day:02d}") for day in range(1, 21)]
    assert len(set(story)) == len(authoring.STORY_DIRECTIONS)
    assert len(set(names)) == len(authoring.NAMING_DIRECTIONS)
    assert len(authoring.STORY_DIRECTIONS) > len(authoring.NAMING_DIRECTIONS)


def test_brief_calls_recent_premises_spent_and_warns_against_reskins(brief):
    prompt = authoring._brief_prompt(
        brief,
        {category: [] for category in authoring.HISTORY_CATEGORIES},
        ["Canopy Permit Office | obtain a permit before the office closes"],
    )
    assert "Recent premise history" in prompt
    assert "spent" in prompt
    assert "Do not reskin" in prompt
    assert "Narrative engine for today" in prompt
    assert "screenshot from one of the recent worlds" in prompt


def test_system_prompt_explicitly_supports_radically_different_story_ontologies():
    prompt = authoring.SYSTEM_PROMPT.lower()
    for concept in ("superhero", "cosmic horror", "anthropomorphic animals"):
        assert concept in prompt
    assert "do not default to whimsical bureaucracy" in prompt


def test_bureaucracy_rut_is_rejected_when_facets_did_not_request_it(brief):
    proposal = _valid_bundle(brief)
    proposal["title"] = "The Moon Ledger"
    proposal["idea"] = "A filing office audits miracles and issues permits for moonlight."
    complaints = authoring.story_diversity_complaints(
        proposal,
        ["Canopy Permit Office | clerks issue travel permits from a filing desk"],
        {"umbrella": {"genres": ["superhero action"]}},
    )
    assert any("bureaucracy/record-keeping" in complaint for complaint in complaints)


def test_bureaucracy_can_be_intentional_when_a_facet_requests_it(brief):
    proposal = _valid_bundle(brief)
    proposal["title"] = "The Moon Ledger"
    proposal["idea"] = "A filing office audits miracles and issues permits for moonlight."
    complaints = authoring.story_diversity_complaints(
        proposal,
        [],
        {"umbrella": {"genres": ["bureaucratic satire"]}},
    )
    assert not any("bureaucracy/record-keeping" in complaint for complaint in complaints)


def test_story_rut_gets_a_corrective_retry(monkeypatch, brief):
    bad = _valid_bundle(brief)
    bad["title"] = "Tide Ledger Miracles"
    bad["idea"] = "A filing office tallies miracles in a ledger and issues tide permits."
    good = _valid_bundle(brief)
    prompts = []
    monkeypatch.setattr(
        authoring,
        "recent_name_history",
        lambda *a, **k: {category: [] for category in authoring.HISTORY_CATEGORIES},
    )
    monkeypatch.setattr(
        authoring,
        "recent_premise_history",
        lambda *a, **k: ["Canopy Permit Office | clerks issue permits from a filing office"],
    )

    def fake(prompt, *a, **k):
        prompts.append(prompt)
        return json.dumps(bad if len(prompts) == 1 else good)

    monkeypatch.setattr(authoring, "call_claude", fake)
    result = authoring.author(DAY, "key", verbose=False)
    assert len(prompts) == 2
    assert "bureaucracy/record-keeping" in prompts[1]
    assert result["title"] == good["title"]


def test_recent_premise_history_reads_story_fields_not_just_titles(tmp_path: Path):
    payload = _valid_bundle({"seed_facets": {"version": 2}})
    path = tmp_path / "2026-08-10-odd-world.md"
    path.write_text(
        "<!-- proposal-data\n" + json.dumps(payload) + "\n-->\n",
        encoding="utf-8",
    )
    history = authoring.recent_premise_history("2026-08-11", backlog_dir=tmp_path)
    assert len(history) == 1
    assert "lightning predators" in history[0]
    assert "Stormglass Arena" in history[0]
