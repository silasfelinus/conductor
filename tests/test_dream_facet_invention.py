"""Each dream invents 1-2 brand-new Facets that fill a measured gap.

Silas, 2026-09-02: "I would like each dream to include 1-2 new facets ... they
should be different and fill a gap that we don't have", and "(rotating which
kind of facets we grab from and which ones we create)", with the authoring order
"we pull from previous facets to create a general vibe, draft 2 new facets to
fill in gaps, and THEN create the other elements".

Three separate promises, tested separately: the gap is measured, the rotation
actually rotates, and a Facet that is not new is rejected before it reaches the
catalog.
"""

import random

import pytest

import scripts.apply_daily_dream_facets as assign
import scripts.build_dream_proposal as build


def facet(slug, taxonomy="GENRE"):
    return {"slug": slug, "title": slug.replace("-", " ").title(),
            "taxonomy": taxonomy, "randomWeight": 1}


@pytest.fixture
def catalog():
    """A stand-in catalog with a deliberate depth spread, mirroring the live one.

    On 2026-09-02 the real catalog ran from SETTING at 11 rows to PERSONALITY at
    206, which is the spread the gap weighting exists to exploit.
    """
    depths = {"GENRE": 40, "ANIMAL": 30, "SPECIES": 25, "OCCUPATION": 8,
              "MATERIAL": 20, "PERSONALITY": 60, "ARCHETYPE": 50, "QUIRK": 30,
              "THEME": 20, "STYLE": 20, "SETTING": 3, "BACKSTORY": 12,
              "ROLE": 4, "ALIGNMENT": 4}
    return {tax: [facet(f"{tax.lower()}-{i}", tax) for i in range(n)]
            for tax, n in depths.items()}


def test_every_day_plans_two_inventions(catalog):
    for day in ("2026-09-03", "2026-09-04", "2026-10-01", "2027-01-01"):
        plan = build.facet_seed_plan(day, catalog)
        assert len(plan["invent"]) == 2, day
        for entry in plan["invent"]:
            assert entry["taxonomy"] in build.INVENTABLE_TAXONOMIES
            assert len(entry["assign_to"]) == 2


def test_inventions_favour_the_thin_taxonomies(catalog):
    """A gap is measured, not asserted -- thin taxonomies must win over deep ones."""
    rng = random.Random(11)
    picks = []
    for _ in range(400):
        picks += [e["taxonomy"] for e in build.plan_inventions(rng, catalog, set())]

    thin = sum(picks.count(t) for t in ("SETTING", "ROLE", "ALIGNMENT"))   # depth 3-4
    deep = sum(picks.count(t) for t in ("PERSONALITY", "ARCHETYPE"))       # depth 50-60
    assert thin > deep * 5, f"thin={thin} deep={deep}"
    # ...but never impossible: a deep taxonomy still comes up sometimes, so the
    # catalog does not ossify into three growing corners.
    assert deep > 0


def test_structural_taxonomies_are_never_invented_into():
    """REWARD_TYPE and friends are schema values, not story vocabulary."""
    for taxonomy in ("DREAM_TYPE", "REWARD_TYPE", "RARITY", "BOT_TYPE",
                     "GENDER", "COLOR", "ART_DIRECTION", "PROMPT_ENHANCEMENT"):
        assert taxonomy not in build.INVENTABLE_TAXONOMIES


def test_seed_taxonomies_rotate_across_days(catalog):
    """The six fixed taxonomies were why bundles rhymed. They must vary now."""
    seen = {tuple(build.facet_seed_plan(f"2026-09-{d:02d}", catalog)["seeded_taxonomies"])
            for d in range(1, 29)}
    assert len(seen) > 6, f"only {len(seen)} distinct seed sets across 28 days"


def test_invention_avoids_what_the_day_already_seeds(catalog):
    """Rotating what we grab from AND what we create means preferring different corners."""
    rng = random.Random(5)
    overlaps = 0
    for _ in range(200):
        seeded = {"SETTING", "ROLE"}
        picks = [e["taxonomy"] for e in build.plan_inventions(rng, catalog, seeded)]
        overlaps += len(seeded.intersection(picks))
    # The two thinnest taxonomies, deliberately seeded, are still chosen
    # sometimes -- they are down-weighted, not banned -- but not most of the time.
    assert overlaps < 200, "seeded taxonomies were never avoided"


# ---- validation ----------------------------------------------------------

def _seeds_with(invented, *, assign_to=("character", "location")):
    element = [facet("existing-genre"), *invented]
    return {
        "invent": [{"taxonomy": "SETTING", "catalog_depth": 3, "assign_to": list(assign_to)}],
        "invented": invented,
        # The plan's own draws: what the catalog already held and handed over.
        "umbrella": {"genres": [facet("existing-genre"), facet("second-genre")],
                     "creature": facet("otter", "ANIMAL"),
                     "wildcard": facet("courier", "ROLE")},
        "shared": {"material": facet("bone-glass", "MATERIAL"),
                   "personality": facet("cautious", "PERSONALITY")},
        "extra_genres": {},
        "elements": {key: list(element) for key in
                     ("vibe", "location", "character", "reward_item", "reward_skill", "scenario")},
    }


def _good_facet():
    return {"title": "Cable Ferry", "slug": "cable-ferry", "taxonomy": "SETTING",
            "description": "A crossing that only goes where its cable already goes. "
                           "It cannot be diverted, and everyone waiting knows the schedule.",
            "art_prompt": "A steel cable ferry mid-crossing, paint blistered to primer."}


def test_a_well_formed_invention_validates():
    assert build.validate_inventions(_seeds_with([_good_facet()])) == []


def test_an_invention_duplicating_a_seeded_facet_is_rejected():
    """'They should be different' -- enforced, not merely requested."""
    dupe = {**_good_facet(), "slug": "existing-genre", "title": "Existing Genre"}
    problems = build.validate_inventions(_seeds_with([dupe]))
    assert any("duplicates a Facet already in play" in p for p in problems)


def test_punctuation_does_not_smuggle_a_duplicate_past_the_check():
    """"Night Market", "night-market" and "nightmarket" are one concept."""
    assert build._lookup_key("Night Market") == build._lookup_key("night-market")
    assert build._lookup_key("night-market") == build._lookup_key("nightmarket")


def test_an_invention_outside_todays_gap_is_rejected():
    off = {**_good_facet(), "taxonomy": "PERSONALITY"}
    problems = build.validate_inventions(_seeds_with([off]))
    assert any("is not one of today's gaps" in p for p in problems)


def test_an_invention_missing_from_its_assigned_elements_is_rejected():
    """A Facet created and then linked to nothing is worse than no Facet."""
    seeds = _seeds_with([_good_facet()])
    seeds["elements"]["character"] = [facet("existing-genre")]
    problems = build.validate_inventions(seeds)
    assert any("missing from seed_facets.elements.character" in p for p in problems)


def test_missing_inventions_are_rejected():
    seeds = _seeds_with([])
    seeds["invented"] = []
    assert build.validate_inventions(seeds)


# ---- creation ------------------------------------------------------------

def test_a_new_facet_is_posted_once_and_only_when_absent(monkeypatch):
    posts = []
    monkeypatch.setattr(assign, "_facet_exists", lambda slug, timeout=20: slug == "already-here")
    monkeypatch.setattr(assign, "_post",
                        lambda path, payload, token, dry_run=False:
                        (posts.append(payload), {"success": True, "data": {"id": 9001}})[1])

    proposal = {"seed_facets": {"invented": [
        _good_facet(),
        {**_good_facet(), "slug": "already-here", "title": "Already Here"},
    ]}}
    records, errors = assign.ensure_invented_facets(proposal, "token")

    assert errors == []
    assert [r["slug"] for r in records] == ["cable-ferry", "already-here"]
    assert [r["created"] for r in records] == [True, False]
    assert len(posts) == 1
    assert posts[0]["slug"] == "cable-ferry"
    assert posts[0]["taxonomy"] == "SETTING"
    # A new Facet that cannot be drawn is a dead row.
    assert posts[0]["isRandomizable"] is True


def test_an_unreachable_catalog_never_reads_as_absent(monkeypatch):
    """Treating "cannot check" as "not there" mints a duplicate every night."""
    def boom(slug, timeout=20):
        raise RuntimeError(f"could not check whether Facet {slug} already exists")

    monkeypatch.setattr(assign, "_facet_exists", boom)
    monkeypatch.setattr(assign, "_post", lambda *a, **k: pytest.fail("must not POST"))

    records, errors = assign.ensure_invented_facets(
        {"seed_facets": {"invented": [_good_facet()]}}, "token")
    assert records == []
    assert errors and "could not check" in errors[0]
