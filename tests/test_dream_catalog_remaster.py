"""Coverage for the Daily Dream catalog freshness remaster (conductor issue #3184)."""

from __future__ import annotations

import copy
import datetime
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_dream_catalog as audit  # noqa: E402
import author_dream_proposal as author  # noqa: E402
import dream_creative_ruts as ruts  # noqa: E402
import remaster_dream_catalog as remaster  # noqa: E402


def facet(title: str, slug: str, taxonomy: str) -> dict:
    return {"title": title, "slug": slug, "taxonomy": taxonomy, "randomWeight": 1.0}


def seed_facets(day: str) -> dict:
    """A schema-valid version-2 seed block; the audit judges prose, not Facet luck."""
    low = facet("Low Fantasy", "low-fantasy", "GENRE")
    magical = facet("Magical Girl", "magical-girl", "GENRE")
    creature = facet("Sea Cucumber", "sea-cucumber", "ANIMAL")
    occupation = facet("Amazonian Scout", "amazonian-scout", "OCCUPATION")
    material = facet("Demonic Bone", "demonic-bone", "MATERIAL")
    personality = facet("Serious", "serious", "PERSONALITY")
    cozy = facet("Cozy Mystery", "cozy-mystery", "GENRE")
    scifi = facet("Sci-Fi", "sci-fi", "GENRE")
    vampire = facet("Vampire Gothic", "vampire-gothic", "GENRE")
    folk = facet("Folk Fantasy", "folk-fantasy", "GENRE")
    pastoral = facet("Revolutionary Pastoral", "revolutionary-pastoral", "GENRE")
    return {
        "version": 2,
        "date": day,
        "deterministic_seed": 42,
        "catalog_source": "test",
        "umbrella": {
            "genres": [low, magical],
            "creature": creature,
            "wildcard": occupation,
            "wildcard_role": "occupation",
        },
        "shared": {"material": material, "personality": personality},
        "extra_genres": {
            "location": cozy,
            "character": scifi,
            "reward_item": vampire,
            "reward_skill": folk,
            "scenario": pastoral,
        },
        "elements": {
            "vibe": [low, magical, creature, occupation],
            "location": [low, magical, cozy, creature, material],
            "character": [low, magical, scifi, creature, occupation, personality],
            "reward_item": [low, magical, vampire, material],
            "reward_skill": [low, magical, folk, occupation],
            "scenario": [low, magical, pastoral, cozy, scifi, creature],
        },
    }


CLEAN_PROPOSAL = {
    "title": "Salt Memory",
    "slug": "salt-memory",
    "idea": "A bioluminescent engineer wades through a flooded gearworks temple where "
    "every drowned machine still hums the god that built it.",
    "vibe": {
        "title": "Salt Memory",
        "line": "Every drowned machine remembers the god that built it.",
        "art_direction": "Coral-pink pulse-metal pipes glowing along flooded basalt walls, "
        "green tide light rippling across submerged brass gears and wet stone.",
    },
    "locations": [
        {
            "title": "Regrowth Yards",
            "known_for": "The yards are known for hulls that regrow torn steel plates overnight.",
            "local_rule": "Never wake a hull while its living seams are still knitting shut.",
            "best_scene": "A scar in the hull hums, flushes pink, and closes over while the tide rises.",
            "art_direction": "A coral-pink dry-dock of wet iron ribs and glowing resin "
            "veins, cold blue worklight raking across barnacled steel plate.",
        }
    ],
    "characters": [
        {
            "name": "Odalys Nunes",
            "role_drive": "She has to wake the last temple engine before the tide turns and seals the shrine.",
            "carries": "A pressure wrench grown from living coral hangs from her belt.",
            "complication": "The engines answer her in her mother's voice, and she has never learned to ignore it.",
            "look": "A wiry engineer in a patched grey drysuit, copper bio-lamps stitched "
            "along both sleeves, wet dark hair flattened under a cracked visor.",
        }
    ],
    "rewards": [
        {
            "name": "Tide Wrench",
            "reward_type": "ITEM",
            "rarity": "RARE",
            "grants": "It loosens any fitting that has rusted shut.",
            "best_used_when": "Use it when a hull seam refuses to open.",
            "catch": "The wrench rusts a little further every time it is used.",
            "look": "A forearm-length wrench of pitted brass and pink coral, its jaws "
            "worn mirror-bright, handle wrapped in salt-stiffened cord.",
        },
        {
            "name": "Deep Listening",
            "reward_type": "SKILL",
            "rarity": "UNCOMMON",
            "grants": "It hears which machine in a flooded room is still alive.",
            "best_used_when": "Use it when the water is too dark to see through.",
            "catch": "Living voices and engine noise become impossible to tell apart.",
            "look": "Pale green concentric ripples spreading outward through dark water "
            "from a single lifted palm, silt glittering in the wavefront.",
        },
    ],
    "scenarios": [
        {
            "title": "The Waking Tide",
            "setup": "In Salt Memory at the Regrowth Yards, Odalys Nunes wakes the last "
            "temple engine while the tide climbs past the gantry.",
        }
    ],
    "seed_facets": seed_facets("2026-08-06"),
}


def rut_proposal() -> dict:
    """A bundle dragged through every historical groove at once, sharing no prose
    with CLEAN_PROPOSAL so the two are judged on their own merits."""
    return {
        "title": "The Chittering Archive",
        "slug": "chittering-archive",
        "idea": "A clerk stamps the ledger of a drowned archive while the permit office "
        "tallies every unfiled confession.",
        "vibe": {
            "title": "The Chittering Archive",
            "line": "Every ledger outlives the clerk who kept it.",
            "art_direction": "shelves",
        },
        "locations": [
            {
                "title": "The Permit Lighthouse",
                "known_for": "beacons that refuse unstamped ships",
                "local_rule": "no lamp lights without a countersigned docket",
                "best_scene": "the registry window slams shut at high water",
                "art_direction": "a tower of files",
            }
        ],
        "characters": [
            {
                "name": "Undersecretary Bramble",
                "role_drive": "close the quarter's outstanding filings before audit",
                "carries": "a brass stamp kit and a bound ledger",
                "complication": "his own name appears in the unfiled drawer",
                "look": "tidy",
            }
        ],
        "rewards": [
            {
                "name": "The Stamp of Provenance",
                "reward_type": "ITEM",
                "rarity": "RARE",
                "grants": "makes any document count as filed",
                "best_used_when": "the bureau demands paperwork nobody kept",
                "catch": "the record it invents becomes true",
                "look": "a crowd of people waiting at the registry window",
            },
            {
                "name": "Plausible Deniability",
                "reward_type": "SKILL",
                "rarity": "UNCOMMON",
                "grants": "shifts blame onto a missing clerk",
                "best_used_when": "an inspector arrives unannounced",
                "catch": "the missing clerk starts existing",
                "look": "paperwork",
            },
        ],
        "scenarios": [
            {
                "title": "The Filing of Small Suns",
                "setup": "In The Chittering Archive at The Permit Lighthouse, "
                "Undersecretary Bramble must file a sunrise before the bureau revokes it.",
            }
        ],
        "seed_facets": seed_facets("2026-08-12"),
    }


def write_bundle(
    backlog: Path,
    day: str,
    proposal: dict,
    *,
    built: dict | None = None,
    status: str = "built",
) -> Path:
    text = (
        "---\n"
        f"slug: {proposal['slug']}\n"
        f"title: {proposal['title']}\n"
        "type: dream\n"
        f"status: {status}\n"
        "proposal: true\n"
        f"proposal_date: '{day}'\n"
        "---\n\n"
        "## The idea\n"
        f"{proposal['idea']}\n\n"
        "<!-- proposal-data\n" + json.dumps(proposal) + "\n-->\n"
    )
    if built is not None:
        text += "\n<!-- built-data\n" + json.dumps(built) + "\n-->\n"
    path = backlog / f"{day}-{proposal['slug']}.md"
    path.write_text(text, encoding="utf-8")
    return path


def built_data(*, first_id: int = 100, attached: bool = True) -> dict:
    return {
        "built_at": "2026-08-06T09:00:00-07:00",
        "designer": "dream-cycle",
        "records": {
            "world": {"id": first_id, "model": "Dream", "title": "world"},
            "locations": [{"id": first_id + 1, "model": "Dream", "title": "location"}],
            "characters": [{"id": first_id + 2, "model": "Character", "name": "character"}],
            "rewards": [
                {"id": first_id + 3, "model": "Reward", "reward_type": "ITEM", "name": "item"},
                {"id": first_id + 4, "model": "Reward", "reward_type": "SKILL", "name": "skill"},
            ],
            "scenarios": [{"id": first_id + 5, "model": "Scenario", "title": "scenario"}],
        },
        "art": [
            {"request_id": f"dream-cycle-old-{index}", "attached": attached}
            for index in range(6)
        ],
    }


@pytest.fixture
def backlog(tmp_path: Path) -> Path:
    root = tmp_path / "backlog"
    root.mkdir()
    return root


# ── rut vocabulary ───────────────────────────────────────────────────────────


def test_motif_families_separate_the_historical_ruts():
    hits = ruts.motif_hits(
        "the ledger office, the drowned archive, a cozy market bazaar, a lighthouse spire, "
        "and a weary concierge"
    )
    assert set(hits) == {
        "bureaucracy",
        "archive",
        "cozy-market",
        "tower-beacon",
        "occupational-archetype",
    }


def test_context_gated_markers_do_not_fire_on_ordinary_english():
    """A choir stall is furniture; a market stall is the rut."""
    assert "cozy-market" not in ruts.motif_hits("choir stalls carved from bone-pale reef")
    assert "cozy-market" in ruts.motif_hits("market stalls of haggling vendors")


def test_a_family_the_facets_actually_requested_is_not_a_rut():
    facets = json.dumps({"genres": [{"slug": "bureaucratic-fantasy"}]})
    assert ruts.facets_request("bureaucracy", facets)
    assert not ruts.facets_request("tower-beacon", facets)


def test_surname_factory_detection_spares_ordinary_family_names():
    assert ruts.surname_factory_complaint("Undersecretary Bramble")
    assert ruts.surname_factory_complaint("Wren Thistlemaw")
    assert ruts.surname_factory_complaint("Odalys Nunes") is None


def test_name_scoped_ruts_reach_the_live_creative_contract():
    complaints = author.story_diversity_complaints(rut_proposal(), [], {"version": 2})
    joined = " ".join(complaints)
    assert "bureaucracy/record-keeping" in joined  # the pre-existing whole-text guard
    assert "archive / library" in joined  # added by the remaster
    assert "tower / lighthouse" in joined


def test_clean_proposal_still_passes_the_live_contract():
    assert author.story_diversity_complaints(CLEAN_PROPOSAL, [], {"version": 2}) == []


# ── audit ────────────────────────────────────────────────────────────────────


def test_audit_keeps_a_clean_bundle_and_condemns_a_rut_bundle(backlog: Path):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data())
    write_bundle(backlog, "2026-08-12", rut_proposal(), built=built_data(first_id=200))

    audits = {a.bundle.day: a for a in audit.audit_catalog(audit.load_bundles(backlog))}

    assert audits["2026-08-06"].classification == audit.KEEP
    assert audits["2026-08-12"].classification in {audit.SUBSTANTIAL, audit.RETIRE}
    assert audits["2026-08-12"].score > audits["2026-08-06"].score


def test_audit_flags_weak_visual_fields_and_person_shaped_reward_looks(backlog: Path):
    write_bundle(backlog, "2026-08-12", rut_proposal(), built=built_data())
    result = audit.audit_catalog(audit.load_bundles(backlog))[0]

    item_findings = " ".join(result.assets["reward_item"]["visual_findings"])
    assert "describes people" in item_findings
    assert any("thin" in finding for finding in result.assets["vibe"]["visual_findings"])
    assert result.art["verdict"] == audit.ART_REGENERATE


def test_audit_marks_pre_v2_bundles_as_rebuild_rather_than_in_place(backlog: Path):
    legacy = copy.deepcopy(CLEAN_PROPOSAL)
    legacy["slug"] = "comet-market"
    legacy["title"] = "The Comet Market"
    legacy["locations"] = legacy["locations"] * 2  # the pre-v2 multi-location shape
    write_bundle(backlog, "2026-07-16", legacy, built=built_data())

    result = audit.audit_catalog(audit.load_bundles(backlog))[0]

    assert result.legacy_shape is True
    assert "cannot be revised in place" in " ".join(result.reasons)
    assert result.as_dict()["remaster_path"] == "rebuild"


def test_unbuilt_proposals_past_the_window_are_reported_as_poisoned(backlog: Path):
    old = (datetime.date.today() - datetime.timedelta(days=9)).isoformat()
    fresh = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    stale = copy.deepcopy(CLEAN_PROPOSAL)
    stale["slug"] = "stale-idea"
    write_bundle(backlog, old, stale, status="outline")
    recent = copy.deepcopy(CLEAN_PROPOSAL)
    recent["slug"] = "fresh-idea"
    write_bundle(backlog, fresh, recent, status="outline")

    poisoned = audit.stale_unbuilt(backlog, window_days=2)

    assert [row["slug"] for row in poisoned] == ["stale-idea"]
    assert "never build as written" in poisoned[0]["disposition"]


def test_built_bundles_are_never_treated_as_poisoned_proposals(backlog: Path):
    old = (datetime.date.today() - datetime.timedelta(days=40)).isoformat()
    write_bundle(backlog, old, CLEAN_PROPOSAL, built=built_data())

    assert audit.stale_unbuilt(backlog, window_days=2) == []


def test_manifest_records_records_ids_for_every_element(backlog: Path):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data(first_id=500))
    audits = audit.audit_catalog(audit.load_bundles(backlog))
    manifest = audit.build_manifest(audits, window_days=2, backlog=backlog)

    records = manifest["bundles"][0]["records"]
    assert sorted(records) == sorted(audit.ELEMENTS)
    assert records["reward_skill"]["id"] == 504


# ── remaster planning and art lane ───────────────────────────────────────────


def _manifest(backlog: Path) -> dict:
    audits = audit.audit_catalog(audit.load_bundles(backlog))
    return audit.build_manifest(audits, window_days=2, backlog=backlog)


def test_plan_routes_each_bundle_to_the_lane_that_can_actually_fix_it(backlog: Path):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data())
    write_bundle(backlog, "2026-08-12", rut_proposal(), built=built_data(first_id=200))
    legacy = copy.deepcopy(rut_proposal())
    legacy["slug"] = "marrow-library"
    legacy["title"] = "The Marrow Library"
    legacy["characters"] = []  # pre-v2 shape
    write_bundle(backlog, "2026-07-17", legacy, built=built_data(first_id=300))

    plan = remaster.build_plan(_manifest(backlog))
    lanes = {
        row["day"]: wave
        for wave, rows in plan["waves"].items()
        for row in rows
    }

    assert lanes["2026-08-12"] == "1-rewrite-in-place"
    assert lanes["2026-07-17"] == "2-legacy-canonicalization"
    assert lanes["2026-08-06"] in {"3-art-only", "4-keep"}


def test_art_lane_builds_six_distinct_requests_bound_to_the_live_records(backlog: Path):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data(first_id=700))
    bundle = audit.load_bundles(backlog)[0]

    specs = remaster.remaster_art_specs(bundle, variant=2)

    assert len(specs) == 6
    assert len({spec[0] for spec in specs}) == 6
    assert [spec[4] for spec in specs] == [700, 701, 702, 703, 704, 705]
    assert [spec[3] for spec in specs] == [
        "dream", "dream", "character", "reward", "reward", "scenario"
    ]


def test_restyle_variant_moves_a_world_off_its_default_visual_language(backlog: Path):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data())
    bundle = audit.load_bundles(backlog)[0]

    default = remaster.remaster_art_specs(bundle, variant=0)[0][2]
    restyled = remaster.remaster_art_specs(bundle, variant=1)[0][2]

    assert default != restyled


def test_art_lane_is_dry_run_until_apply(backlog: Path, monkeypatch):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data())
    catalog = {bundle.day: bundle for bundle in audit.load_bundles(backlog)}
    manifest = _manifest(backlog)
    plan = remaster.build_plan(manifest)
    plan["waves"]["3-art-only"] = [
        {**row, "art": audit.ART_REGENERATE}
        for row in plan["waves"]["3-art-only"] + plan["waves"]["4-keep"]
    ]
    appended: list[list[str]] = []
    monkeypatch.setattr(
        remaster.records, "append_art_requests", lambda entries, dry_run: appended.append(entries)
    )
    before = catalog["2026-08-06"].path.read_text(encoding="utf-8")

    receipt = remaster.regenerate_art(
        plan, catalog, manifest, limit=5, apply=False, include_rewrites=False, stamp="TESTSTAMP"
    )

    assert receipt["requests"] == 6
    assert appended == []
    assert catalog["2026-08-06"].path.read_text(encoding="utf-8") == before


def test_applying_the_art_lane_supersedes_old_evidence_and_stages_requests(
    backlog: Path, monkeypatch
):
    path = write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data())
    catalog = {bundle.day: bundle for bundle in audit.load_bundles(backlog)}
    manifest = _manifest(backlog)
    plan = remaster.build_plan(manifest)
    plan["waves"]["3-art-only"] = [
        {**row, "art": audit.ART_REGENERATE}
        for row in plan["waves"]["3-art-only"] + plan["waves"]["4-keep"]
    ]
    appended: list[list[str]] = []
    monkeypatch.setattr(
        remaster.records, "append_art_requests", lambda entries, dry_run: appended.append(entries)
    )

    remaster.regenerate_art(
        plan, catalog, manifest, limit=5, apply=True, include_rewrites=False, stamp="TESTSTAMP"
    )

    assert len(appended) == 1 and len(appended[0]) == 6
    assert all("source: dream-cycle" in entry for entry in appended[0])
    assert all("entity_field: imagePath" in entry for entry in appended[0])
    rebuilt = audit.load_bundles(backlog)[0].built
    assert len(rebuilt["superseded_art"]) == 6
    assert len(rebuilt["art"]) == 6
    assert all(row["attached"] is False for row in rebuilt["art"])
    assert rebuilt["remasters"][0]["stamp"] == "TESTSTAMP"
    assert "## The idea" in path.read_text(encoding="utf-8")  # prose untouched


def test_stubs_are_inert_until_an_author_renames_them(backlog: Path, monkeypatch, tmp_path: Path):
    write_bundle(backlog, "2026-08-12", rut_proposal(), built=built_data())
    catalog = {bundle.day: bundle for bundle in audit.load_bundles(backlog)}
    manifest = _manifest(backlog)
    revisions = tmp_path / "revisions"
    monkeypatch.setattr(remaster, "REVISIONS_DIR", revisions)

    written = remaster.write_stubs(
        remaster.build_plan(manifest), catalog, manifest, limit=5, apply=True
    )

    assert len(written) == 1
    stub = json.loads(written[0].read_text(encoding="utf-8"))
    assert written[0].name.endswith("-stub.json")  # apply_dream_revision only takes -request.json
    assert stub["status"] == "needs-authoring"
    assert stub["proposal"]["slug"] == "chittering-archive"
    assert stub["audit"]["reasons"]


def test_legacy_bundles_get_a_reseed_stub_that_names_the_deterministic_plan(
    backlog: Path, monkeypatch, tmp_path: Path
):
    legacy = copy.deepcopy(rut_proposal())
    legacy["slug"] = "marrow-library"
    legacy["title"] = "The Marrow Library"
    legacy["characters"] = legacy["characters"] * 3  # the retired eight-stage shape
    write_bundle(backlog, "2026-07-17", legacy, built=built_data())
    catalog = {bundle.day: bundle for bundle in audit.load_bundles(backlog)}
    manifest = _manifest(backlog)
    monkeypatch.setattr(remaster, "REVISIONS_DIR", tmp_path / "revisions")

    written = remaster.write_stubs(
        remaster.build_plan(manifest), catalog, manifest, limit=5, apply=True
    )

    stub = json.loads(written[0].read_text(encoding="utf-8"))
    assert stub["legacy_reseed"] is True
    assert "facet_seed_plan" in stub["seed_facets_for_this_date"]
    assert "retires the leftover staged rows" in stub["instructions"]


def test_verify_reports_missing_records_without_network_access(backlog: Path):
    broken = built_data()
    broken["records"]["scenarios"] = []
    broken["art"] = []
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=broken)
    catalog = {bundle.day: bundle for bundle in audit.load_bundles(backlog)}

    report = remaster.verify_catalog(catalog, offline=True)

    problems = " ".join(report["bundles"][0]["missing"])
    assert "scenario: no recorded id" in problems
    assert "no art evidence" in problems
    assert report["problems"] == 2



# ── legacy canonicalization (pre-v2 staged bundles) ──────────────────────────


def legacy_built_data() -> dict:
    """The retired eight-stage shape: a second vibe Dream, extra rows, a narrator Bot."""
    return {
        "built_at": "2026-07-17T09:00:00-07:00",
        "designer": "dream-cycle",
        "records": {
            "world": {"id": 100, "model": "Dream", "title": "world"},
            "vibe": {"id": 101, "model": "Dream", "title": "a second vibe Dream"},
            "locations": [
                {"id": 110, "model": "Dream", "title": "first location"},
                {"id": 111, "model": "Dream", "title": "second location"},
            ],
            "characters": [
                {"id": 120, "model": "Character", "name": "first"},
                {"id": 121, "model": "Character", "name": "second"},
                {"id": 122, "model": "Character", "name": "third"},
            ],
            "rewards": [
                {"id": 130, "model": "Reward", "reward_type": "ITEM", "name": "item"},
                {"id": 131, "model": "Reward", "reward_type": "SKILL", "name": "skill"},
            ],
            "scenarios": [
                {"id": 140, "model": "Scenario", "title": "first scenario"},
                {"id": 141, "model": "Scenario", "title": "second scenario"},
            ],
            "narrator": {"id": 150, "model": "Bot", "name": "a legacy narrator"},
        },
        "art": [],
    }


@pytest.fixture
def stub_api(monkeypatch):
    """Record every call instead of touching Kind Robots."""
    import apply_dream_revision as revision

    calls: list[tuple[str, str, dict | None]] = []

    def fake(method, url, body=None, timeout=60):
        calls.append((method, url, body))
        return 200, {"success": True, "data": {"id": 1}}

    monkeypatch.setattr(revision.records, "http_json", fake)
    monkeypatch.setattr(revision.records, "append_art_requests", lambda entries, dry_run: None)
    monkeypatch.setattr(revision.records, "KR_API_TOKEN", "test-token")
    return calls


def test_a_bundle_that_never_had_a_seed_cannot_be_asked_to_preserve_one():
    import apply_dream_revision as revision

    pre_v2 = {k: v for k, v in CLEAN_PROPOSAL.items() if k != "seed_facets"}
    assert revision.lacks_canonical_seed(pre_v2)
    assert not revision.lacks_canonical_seed(CLEAN_PROPOSAL)

    with pytest.raises(ValueError, match="preserve seed_facets"):
        revision.validate_revision(pre_v2, CLEAN_PROPOSAL, "2026-07-17", built=True)

    revision.validate_revision(
        pre_v2, CLEAN_PROPOSAL, "2026-07-17", built=True, legacy_reseed=True
    )


def test_a_legacy_reseed_still_requires_a_valid_version_two_seed():
    """The exemption is "you cannot preserve a seed that never existed", not "no seed"."""
    import apply_dream_revision as revision

    pre_v2 = {k: v for k, v in CLEAN_PROPOSAL.items() if k != "seed_facets"}

    bogus_seed = dict(CLEAN_PROPOSAL, seed_facets={"version": 2, "elements": "not-an-object"})
    with pytest.raises(ValueError, match="valid version-2 seed"):
        revision.validate_revision(
            pre_v2, bogus_seed, "2026-07-17", built=True, legacy_reseed=True
        )

    still_seedless = dict(pre_v2)
    with pytest.raises(ValueError, match="seed_facets must be an object"):
        revision.validate_revision(
            pre_v2, still_seedless, "2026-07-17", built=True, legacy_reseed=True
        )


def test_legacy_canonicalization_remasters_six_rows_and_retires_the_rest(stub_api):
    import apply_dream_revision as revision

    built = revision._patch_built_bundle(
        {"slug": "marrow-library", "locations": [{"title": "first location"}]},
        copy.deepcopy(CLEAN_PROPOSAL),
        legacy_built_data(),
        revision_stamp="TESTSTAMP",
        legacy=True,
    )

    retired = {row["id"] for row in built["retired_legacy_rows"]}
    assert retired == {101, 111, 121, 122, 141}  # second vibe, extra rows
    assert all(
        call[2] == {"isActive": False, "isPublic": False}
        for call in stub_api
        if call[0] == "PATCH" and call[1].rsplit("/", 1)[-1] in {"101", "111", "121", "122", "141"}
    )
    # the ledger is canonical afterwards, so the bundle never needs this path again
    records = built["records"]
    assert [row["id"] for row in records["locations"]] == [110]
    assert [row["id"] for row in records["characters"]] == [120]
    assert [row["id"] for row in records["scenarios"]] == [140]
    assert "vibe" not in records
    # narrator Bots belong to a separately scoped cleanup, so they are recorded, not touched
    assert built["legacy_narrator_left_in_place"]["id"] == 150
    assert not any(call[1].endswith("/api/bots/150") for call in stub_api)


def test_legacy_lane_skips_a_row_that_is_already_gone(stub_api, monkeypatch):
    import apply_dream_revision as revision

    monkeypatch.setattr(revision, "_row_is_live", lambda endpoint, entity_id: entity_id != 110)

    built = revision._patch_built_bundle(
        {"slug": "marrow-library", "locations": [{"title": "first location"}]},
        copy.deepcopy(CLEAN_PROPOSAL),
        legacy_built_data(),
        revision_stamp="TESTSTAMP",
        legacy=True,
    )

    assert [row["id"] for row in built["records"]["locations"]] == [111]


def test_a_canonical_bundle_still_refuses_the_legacy_shape(stub_api):
    import apply_dream_revision as revision

    with pytest.raises(ValueError, match="canonical six-asset bundle"):
        revision._patch_built_bundle(
            {"slug": "marrow-library", "locations": [{"title": "first location"}]},
            copy.deepcopy(CLEAN_PROPOSAL),
            legacy_built_data(),
            revision_stamp="TESTSTAMP",
        )


def test_a_spire_crystal_facet_licenses_the_spire_it_asked_for():
    facets = json.dumps({"shared": {"material": {"slug": "spire-crystal"}}})
    assert ruts.facets_request("tower-beacon", facets)
    assert ruts.name_rut_complaints(["The Spire That Remembers"], facets) == []
    assert ruts.name_rut_complaints(["The Spire That Remembers"], "{}")


def test_renders_this_pass_staged_are_pending_not_a_second_regeneration(backlog: Path):
    """A re-run must not queue a replacement for a replacement still in the relay."""
    built = built_data(attached=False)
    built["art"] = [
        {"request_id": f"dream-cycle-remaster-TESTSTAMP-{index}", "attached": False}
        for index in range(6)
    ]
    built["remasters"] = [
        {"stamp": "TESTSTAMP", "art_request_ids": [row["request_id"] for row in built["art"]]}
    ]
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built)

    result = audit.audit_catalog(audit.load_bundles(backlog))[0]

    assert result.art["verdict"] == audit.ART_PENDING
    assert "still working through the relay" in " ".join(result.art["reasons"])

    manifest = audit.build_manifest([result], window_days=2, backlog=backlog)
    plan = remaster.build_plan(manifest)
    assert plan["waves"]["3-art-only"] == []  # nothing to re-queue
    assert manifest["summary"]["art"][audit.ART_PENDING] == 1


def test_art_never_attached_outside_this_pass_still_reads_as_regenerate(backlog: Path):
    write_bundle(backlog, "2026-08-06", CLEAN_PROPOSAL, built=built_data(attached=False))

    result = audit.audit_catalog(audit.load_bundles(backlog))[0]

    assert result.art["verdict"] == audit.ART_REGENERATE
    assert "ever attached" in " ".join(result.art["reasons"])
