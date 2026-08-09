"""Contract tests for scripts/author_dream_proposal.py.

The point of this script is that a dream gets authored on a day when no human
and no session happened to be looking, so the failure mode that matters is a
SILENT one: a bundle that writes but is subtly wrong, or a run that reports
success having done nothing. Every test here is about that.

No network: `call_claude` is monkeypatched throughout.
"""

import json

import pytest

import scripts.author_dream_proposal as authoring

# The script imports its helper by bare name, so `scripts.build_dream_proposal`
# is a different module object than the one it calls. Patch through the script's
# own reference or the monkeypatch silently does nothing — the first draft of
# this file had two tests passing for that reason rather than on their merits.
dreams = authoring.dreams


DAY = "2026-08-14"


def _valid_bundle(brief):
    """A bundle that satisfies validate_proposal, built off the real brief."""
    return {
        "title": "The Sounding Ledger",
        "slug": "the-sounding-ledger",
        "idea": "A tidal archive files the noises a town would rather forget.",
        "vibe": {
            "title": "Quiet Accounting",
            "line": "Every silence in town is owed to someone.",
            "art_direction": (
                "A flooded record hall at dusk, brass tubes rising from black "
                "water, lamplight caught on wet ledger paper."
            ),
        },
        "locations": [
            {
                "title": "The Sounding Hall",
                "known_for": "brass listening tubes grown over with barnacles",
                "local_rule": "no sound leaves without a signature",
                "best_scene": "the tide arrives and every tube speaks at once",
                "art_direction": (
                    "Barnacled brass tubes above black water, lamplit, "
                    "condensation beading on green-tarnished metal."
                ),
            }
        ],
        "characters": [
            {
                "name": "Oris Vale",
                "role_drive": "keeps the town's unpaid silences from compounding",
                "carries": "a wax cylinder and a bone stylus",
                "complication": "one cylinder is their own voice, unfiled",
                "look": (
                    "A short figure in an oilskin coat stiff with salt, "
                    "ink-black gloves worn through at the fingertips."
                ),
            }
        ],
        "rewards": [
            {
                "name": "The Listening Cylinder",
                "reward_type": "ITEM",
                "rarity": "RARE",
                "grants": "replays a sound the room has forgotten",
                "best_used_when": "a room insists nothing happened",
                "catch": "it replays at the original volume",
                "look": (
                    "A palm-length wax cylinder the colour of old butter, "
                    "hairline grooves catching lamplight, one end chipped."
                ),
            },
            {
                "name": "Tidal Bookkeeping",
                "reward_type": "SKILL",
                "rarity": "UNCOMMON",
                "grants": "balances a debt of silence against a debt of noise",
                "best_used_when": "two accounts of one night disagree",
                "catch": "the balance must fall on someone",
                "look": (
                    "Columns of wet ink spreading outward across ruled paper, "
                    "seen from directly above, no hands in frame."
                ),
            },
        ],
        "scenarios": [
            {
                "title": "The Night Account",
                "setup": (
                    "Under Quiet Accounting, Oris Vale opens The Sounding Hall "
                    "on the one tide a year when the tubes speak together."
                ),
            }
        ],
        "seed_facets": brief["seed_facets"],
    }


@pytest.fixture(scope="module")
def _live_brief():
    """One real brief, so the fixtures below are shaped like production."""
    return dreams.build_brief(DAY)


@pytest.fixture
def brief(monkeypatch, _live_brief):
    """A FROZEN brief.

    `author()` calls build_brief itself, and build_brief reads the live Facet
    catalog with a network-free fallback. Letting both the test and the code
    fetch independently made "the seeds the script kept" and "the seeds the test
    expected" two different objects whenever the catalog moved or one call fell
    back — a real flake, and one that would have read as a seed-handling bug.
    Freeze it: one brief, both sides.
    """
    frozen = json.loads(json.dumps(_live_brief))
    monkeypatch.setattr(dreams, "build_brief", lambda day=None, catalog=None: frozen)
    return frozen


def test_authored_bundle_passes_the_same_validator_a_human_bundle_does(
    monkeypatch, brief
):
    monkeypatch.setattr(
        authoring, "call_claude", lambda *a, **k: json.dumps(_valid_bundle(brief))
    )
    proposal = authoring.author(DAY, "key", verbose=False)
    assert dreams.validate_proposal(
        dreams.normalize(proposal, dreams.existing_slugs())
    ) == []


def test_seed_facets_are_ours_not_the_models(monkeypatch, brief):
    """A model that "tidies" the Facets would detach the bundle from the live
    catalog while still looking well-formed. Overwrite, never trust."""
    tampered = _valid_bundle(brief)
    tampered["seed_facets"] = {"version": 2, "umbrella": {"genres": []}}
    monkeypatch.setattr(
        authoring, "call_claude", lambda *a, **k: json.dumps(tampered)
    )
    proposal = authoring.author(DAY, "key", verbose=False)
    assert proposal["seed_facets"] == brief["seed_facets"]


def test_a_narrator_is_stripped(monkeypatch, brief):
    """Six assets, no narrator — the validator rejects one, so the script must
    not let a helpful extra key fail an otherwise good bundle."""
    with_narrator = _valid_bundle(brief)
    with_narrator["narrator"] = {"name": "The Archivist"}
    monkeypatch.setattr(
        authoring, "call_claude", lambda *a, **k: json.dumps(with_narrator)
    )
    proposal = authoring.author(DAY, "key", verbose=False)
    assert "narrator" not in proposal


def test_invalid_bundle_is_retried_with_the_validator_complaints(
    monkeypatch, brief
):
    """The retry has to carry WHY it failed, or it is just a second dice roll."""
    broken = _valid_bundle(brief)
    broken["scenarios"][0]["setup"] = "Something happens somewhere to someone."
    prompts: list[str] = []

    def fake(prompt, *a, **k):
        prompts.append(prompt)
        return json.dumps(broken if len(prompts) == 1 else _valid_bundle(brief))

    monkeypatch.setattr(authoring, "call_claude", fake)
    proposal = authoring.author(DAY, "key", verbose=False)

    assert len(prompts) == 2, "an invalid bundle must be retried"
    assert "failed validation" in prompts[1]
    assert "Oris Vale" in prompts[1], "the retry must name what was missing"
    assert proposal["scenarios"][0]["title"] == "The Night Account"


def test_gives_up_rather_than_writing_a_bad_bundle(monkeypatch, brief):
    broken = _valid_bundle(brief)
    broken["rewards"] = [broken["rewards"][0]]  # no SKILL
    monkeypatch.setattr(
        authoring, "call_claude", lambda *a, **k: json.dumps(broken)
    )
    with pytest.raises(RuntimeError, match="Could not author a valid proposal"):
        authoring.author(DAY, "key", verbose=False)


def test_already_authored_is_success_not_failure(monkeypatch, capsys):
    """This runs on every digest. "Already done" is the common case and must not
    look like an error, or the scheduled caller cries wolf daily."""
    monkeypatch.setattr(dreams, "proposal_exists_for", lambda day: True)
    monkeypatch.setattr(
        authoring, "call_claude", lambda *a, **k: pytest.fail("must not author")
    )
    assert authoring.main(["--date", DAY, "--no-fetch"]) == 0
    assert "already exists" in capsys.readouterr().out


def test_missing_api_key_fails_loudly_and_writes_nothing(monkeypatch, capsys):
    monkeypatch.setattr(dreams, "proposal_exists_for", lambda day: False)
    monkeypatch.setattr(
        dreams, "write_proposal", lambda *a, **k: pytest.fail("must not write")
    )
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert authoring.main(["--date", DAY, "--no-fetch"]) == 1
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


def test_api_failure_is_reported_not_swallowed(monkeypatch, capsys):
    monkeypatch.setattr(dreams, "proposal_exists_for", lambda day: False)
    monkeypatch.setattr(
        dreams, "write_proposal", lambda *a, **k: pytest.fail("must not write")
    )
    monkeypatch.setenv("ANTHROPIC_API_KEY", "key")

    def boom(*a, **k):
        raise RuntimeError("Claude returned an empty completion.")

    monkeypatch.setattr(authoring, "call_claude", boom)
    assert authoring.main(["--date", DAY, "--no-fetch"]) == 1
    assert "Could not author" in capsys.readouterr().err


@pytest.mark.parametrize(
    "reply",
    [
        '```json\n{"a": 1}\n```',
        'Here you go:\n{"a": 1}',
        '{"a": 1}',
    ],
)
def test_parse_json_object_tolerates_a_chatty_or_fenced_reply(reply):
    assert authoring.parse_json_object(reply) == {"a": 1}


@pytest.mark.parametrize("reply", ["no json here", "", "{ truncated"])
def test_parse_json_object_rejects_junk(reply):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        authoring.parse_json_object(reply)
