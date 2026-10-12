"""Versioned future Daily Dream contract. No live API or ArtJob calls."""
from copy import deepcopy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import daily_dream_v3_contract as v3  # noqa: E402


def _facet(slug):
    return {"title": slug.title(), "taxonomy": "THEME", "slug": slug}


def example_v3():
    loc = dict(
        title="Ashwater Cut", known_for="An exposed crossing divides the camps.",
        local_rule="The watch accepts safe passage only after a pledge.",
        best_scene="A refuge caravan waits under two rival banners.",
        art_direction="A dusty rift lined by splintered saltstone.",
        checkpoint_family="arthemy",
    )
    ch = dict(
        name="Vesper Trail", role_drive="She protects strays others abandoned.",
        carries="She wears a carved horn at her hip.",
        complication="Her patron commands the rival faction.",
        look="Older female fennec, scarred armor, dull indigo cloak.",
        checkpoint_family="illustrious",
    )
    reward = dict(
        name="The Red Thread", reward_type="ITEM", rarity="RARE",
        grants="It helps locate a hidden path.",
        best_used_when="A caravan crosses contested ground.",
        catch="Its owner leaves a trace in the dust.",
        look="Red braided cord on an old brass hook.",
        checkpoint_family="arthemy",
    )
    sc = dict(
        title="The Borrowed Crossing", setup="The caravan offers food to cross land held by an enemy.",
        choices=[
            {"label": "Give sanctuary", "tradeoff": "Cede precious grain.",
             "immediate_consequence": "Refugees survive.",
             "later_consequence": "The outpost's winter stores run thin."},
            {"label": "Hold the border", "tradeoff": "Refuse vulnerable travelers.",
             "immediate_consequence": "The granary stays secure.",
             "later_consequence": "The faction remembers the refusal."},
        ],
        checkpoint_family="illustrious",
    )
    result = dict(
        bundle_version=3, title="A Lantern for Nobody",
        slug="a-lantern-for-nobody",
        idea="An independent dream about an unexpected home.",
        vibe={"title": "Tomorrow's Elsewhere", "line": "A home appears only when needed.",
              "art_direction": "Bright prismatic towers and sharp clear sunlight."},
        locations=[], characters=[], rewards=[], scenarios=[],
        seed_facets={
            "version": 3,
            "elements": {slot: [_facet(slot)] for slot in v3.FACET_SLOTS},
        },
    )
    for target in v3.PROJECT_TARGETS:
        for key, base in (("locations", loc), ("characters", ch), ("rewards", reward), ("scenarios", sc)):
            row = deepcopy(base)
            row["project_target"] = target
            if key == "rewards" and target == "emperor-of-dust":
                row["reward_type"] = "SKILL"
            if key == "locations" and target == "emperor-of-dust":
                row["title"] = "Hollow Bell Outskirts"
            if key == "characters" and target == "emperor-of-dust":
                row["name"] = "Young Komodo's Scout"
            if key == "scenarios" and target == "emperor-of-dust":
                row["title"] = "The Winter Claim"
            result[key].append(row)
    return result


def test_valid_v3_has_nine_distinct_slots_with_one_independent_vibe():
    p = example_v3()
    assert v3.validate_v3(p) == []
    assets = v3.asset_manifest(p)
    assert len(assets) == 9
    assert len({a.slot for a in assets}) == 9
    assert assets[0].is_independent and assets[0].checkpoint_family is None
    assert not any(a.is_independent for a in assets[1:])
    for kind in ("locations", "characters", "rewards", "scenarios"):
        assert {a.project_target for a in assets if a.kind == kind} == set(v3.PROJECT_TARGETS)


def test_v3_rejects_six_asset_legacy_and_vibe_as_fake_parent():
    p = example_v3()
    p["locations"].pop()
    p["characters"].pop()
    p["scenarios"].pop()
    p["vibe"]["project_target"] = "zuzu-gamebook"
    p["seed_facets"]["link_zuzu_to_vibe"] = True
    errors = " ".join(v3.validate_v3(p))
    assert "locations has 1" in errors
    assert "characters has 1" in errors
    assert "scenarios has 1" in errors
    assert "independent vibe" in errors
    assert "must not be linked" in errors


def test_choices_must_be_meaningfully_structured_and_nonduplicative():
    p = example_v3()
    p["scenarios"][0]["choices"][1]["label"] = p["scenarios"][0]["choices"][0]["label"]
    p["scenarios"][1]["choices"] = [{"label": "Only choice"}]
    errors = " ".join(v3.validate_v3(p))
    assert "labels must be distinct" in errors
    assert "at least two moral choices" in errors


def test_checkpoint_family_is_named_not_guessed_id():
    p = example_v3()
    p["characters"][0]["checkpoint_family"] = "flux"
    p["characters"][1].pop("checkpoint_family")
    errors = v3.validate_v3(p)
    assert sum("Illustrious or Arthemy" in error for error in errors) == 2


def test_each_category_must_give_both_projects_material():
    p = example_v3()
    p["locations"][1]["project_target"] = "zuzu-gamebook"
    assert any("exactly one asset per Zuzu project" in x for x in v3.validate_v3(p))


def test_offline_outline_validator_accepts_v3_and_catches_invalid_v3(tmp_path):
    import json
    import scripts.check_dream_outlines as preflight

    p = example_v3()
    outline = tmp_path / "draft.md"
    outline.write_text(
        "---\\nslug: test\\ntitle: Test\\ntype: dream\\nstatus: outline\\n"
        "proposal: true\\n---\\n"
        + "<!-- proposal-data\\n" + json.dumps(p) + "\\n-->\\n"
    )
    assert preflight.check_outline(outline) == []
    p["scenarios"][0]["choices"] = []
    outline.write_text(
        "---\\nslug: test\\ntitle: Test\\ntype: dream\\nstatus: outline\\n"
        "proposal: true\\n---\\n"
        + "<!-- proposal-data\\n" + json.dumps(p) + "\\n-->\\n"
    )
    assert any("moral choices" in f.detail for f in preflight.check_outline(outline))


def test_old_builder_refuses_v3_without_any_api_writes(monkeypatch):
    import scripts.build_dream_records as builder

    def unexpected_api(*args, **kwargs):
        raise AssertionError("legacy transaction must never create v3 records")

    monkeypatch.setattr(builder, "http_json", unexpected_api)
    errors = builder._canonical_proposal_errors(example_v3())
    assert any("upgraded single writer" in error for error in errors)
    assert not builder._canonical_proposal_errors(example_v3()) == []
