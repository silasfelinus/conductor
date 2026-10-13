"""Contract tests for Shifting Desks encounter packs.

projects/shifting-desks/encounters/validate_pack.py is the authority; these tests
pin that every committed pack passes it, and that its core design rule (NO CLEAN
WINS: every choice's cost + success contains a harmful effect) actually bites.
"""

import copy
import importlib.util
import json
from pathlib import Path

import re

import pytest

ROOT = Path(__file__).resolve().parent.parent
ENC_DIR = ROOT / "projects" / "shifting-desks" / "encounters"
PACK = ENC_DIR / "ORIENTATION-12.json"
RECORDS = ENC_DIR / "RECORDS-12.json"

_spec = importlib.util.spec_from_file_location("shifting_desks_validate_pack", ENC_DIR / "validate_pack.py")
vp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vp)


def _validate(tmp_path, pack):
    path = tmp_path / "PACK.json"
    path.write_text(json.dumps(pack), encoding="utf-8")
    return vp.validate_pack(path)


@pytest.fixture
def pack():
    return json.loads(PACK.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", vp.pack_paths([]), ids=lambda p: p.name)
def test_every_committed_pack_is_valid(path):
    assert vp.validate_pack(path) == []


def test_orientation_pack_shape(pack):
    assert len(pack["locations"]) == 3
    assert all(len(loc["encounter_ids"]) == 4 for loc in pack["locations"])
    polarity = [e["polarity"] for e in pack["encounters"]]
    assert {p: polarity.count(p) for p in set(polarity)} == {"good": 4, "bad": 4, "mixed": 4}
    assert len(pack["boss"]["choices"]) >= 3


def test_records_pack_shape():
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    assert records["department"]["id"] == "records"
    assert records["department"]["order"] == 2
    assert [loc["location_id"] for loc in records["locations"]] == [
        "pneumatic-tube-exchange", "sub-archive", "window-9",
    ]
    assert all(len(loc["encounter_ids"]) == 4 for loc in records["locations"])
    polarity = [e["polarity"] for e in records["encounters"]]
    assert {p: polarity.count(p) for p in set(polarity)} == {"good": 4, "bad": 4, "mixed": 4}
    lead = [e for e in records["encounters"] if vp.LEAD_TAGS & set(e["tags"])]
    assert len(lead) >= 9
    assert 4 <= len(records["boss"]["choices"]) <= 7
    outcomes = {o["id"] for o in records["boss"]["department_outcomes"]}
    assert "refiled" in outcomes and len(outcomes - {"refiled"}) >= 3


def test_records_pays_off_orientation_flags():
    """At least one Records choice is gated on a flag only Orientation grants."""
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    orientation_flags = vp.granted_flags(json.loads(PACK.read_text(encoding="utf-8")))
    own = vp.granted_flags(records)
    choices = [c for e in records["encounters"] for c in e["choices"]] + records["boss"]["choices"]
    carried = {(c.get("requires") or {}).get("flag") for c in choices} - {None} - own
    assert carried and carried <= orientation_flags


DEFAULT_MEMO = {
    "id": "nothing-has-changed",
    "kind": "none",
    "location_ids": [],
    "title": None,
    "when": None,
    "reason": "The department has been restructured overnight. Nothing has changed. Please act surprised.",
}


def test_requires_flag_may_come_from_a_lower_department(tmp_path, pack):
    earlier = copy.deepcopy(pack)
    (tmp_path / "EARLIER.json").write_text(json.dumps(earlier), encoding="utf-8")
    later = copy.deepcopy(pack)
    later["department"] = {
        **later["department"],
        "id": "later",
        "title": "Later",
        "order": 2,
        "boss_id": later["boss"]["id"],
    }
    later["restructurings"] = [DEFAULT_MEMO]
    # Remove every in-pack source of the gated flag, so only the earlier pack can grant it.
    gated = next(c for c in later["boss"]["choices"] if c["requires"])
    flag = gated["requires"]["flag"]
    for choice in [c for e in later["encounters"] for c in e["choices"]] + later["boss"]["choices"]:
        for key in ("success", "failure"):
            out = choice.get(key) or {}
            out["add_flags"] = [f for f in out.get("add_flags", []) if f != flag]
    later_path = tmp_path / "LATER.json"
    later_path.write_text(json.dumps(later), encoding="utf-8")
    assert vp.validate_pack(later_path) == []
    # The same flag from a pack of the same or a higher order does not count.
    earlier["department"]["order"] = 2
    (tmp_path / "EARLIER.json").write_text(json.dumps(earlier), encoding="utf-8")
    errors = vp.validate_pack(later_path)
    assert any(f"requires flag {flag!r}" in e for e in errors)
    # An explicit earlier_flags set overrides the sibling scan.
    assert vp.validate_pack(later_path, earlier_flags={flag}) == []


def test_clean_win_is_rejected(tmp_path, pack):
    bad = copy.deepcopy(pack)
    choice = bad["encounters"][0]["choices"][0]
    choice["cost"] = {}
    choice["success"]["effects"] = {"clearance": 1, "composure": 1}
    errors = _validate(tmp_path, bad)
    assert any("clean win" in e for e in errors)


def test_suspicion_rise_counts_as_harm(tmp_path, pack):
    ok = copy.deepcopy(pack)
    choice = ok["encounters"][0]["choices"][0]
    choice["cost"] = {}
    choice["success"]["effects"] = {"clearance": 2, "suspicion": 1}
    assert _validate(tmp_path, ok) == []


def test_rolled_choice_needs_failure_and_certain_choice_must_not(tmp_path, pack):
    bad = copy.deepcopy(pack)
    rolled = next(c for c in bad["encounters"][0]["choices"] if c["roll"])
    rolled["failure"] = None
    certain = next(c for c in bad["encounters"][0]["choices"] if c["roll"] is None)
    certain["failure"] = copy.deepcopy(rolled["success"])
    errors = _validate(tmp_path, bad)
    assert any("failure" in e and "outcome must be an object" in e for e in errors)
    assert any("without a roll must have failure: null" in e for e in errors)


def test_art_prompts_are_positive_only(tmp_path, pack):
    bad = copy.deepcopy(pack)
    bad["encounters"][0]["art"]["brief"] = (
        "A worker at a desk with no text and no logos, halftone grain, every surface bare and unmarked"
    )
    assert any("positive-only" in e for e in _validate(tmp_path, bad))


def test_boss_route_requirement_must_be_grantable(tmp_path, pack):
    bad = copy.deepcopy(pack)
    gated = next(c for c in bad["boss"]["choices"] if c["requires"])
    gated["requires"] = {"flag": "a-flag-nothing-grants"}
    assert any("nothing in this pack grants" in e for e in _validate(tmp_path, bad))


def test_unknown_meter_and_skill_rejected(tmp_path, pack):
    bad = copy.deepcopy(pack)
    rolled = next(c for c in bad["encounters"][1]["choices"] if c["roll"])
    rolled["roll"]["skill"] = "steel"
    rolled["cost"] = {"hp": -1}
    errors = _validate(tmp_path, bad)
    assert any("unknown meter" in e for e in errors)
    assert any("skill 'steel'" in e for e in errors)


def test_lead_flavor_quota_is_enforced(tmp_path, pack):
    bad = copy.deepcopy(pack)
    for enc in bad["encounters"]:
        enc["tags"] = ["deathtrap"]
    assert any("lead tag" in e for e in _validate(tmp_path, bad))


DECKS = ENC_DIR / "DECKS.json"


def test_decks_reference_only_granted_flags():
    assert vp.validate_decks(DECKS, vp.pack_paths([])) == []


def test_decks_cover_every_department_pack():
    """Every society names an objective and a betrayal for each committed department."""
    decks = json.loads(DECKS.read_text(encoding="utf-8"))
    departments = {json.loads(p.read_text(encoding="utf-8"))["department"]["id"] for p in vp.pack_paths([])}
    for soc in decks["societies"]:
        assert departments <= set(soc["objectives"]), soc["id"]
        assert departments <= set(soc["betrayals"]), soc["id"]


def test_decks_reject_a_society_flag_nothing_grants(tmp_path):
    decks = json.loads(DECKS.read_text(encoding="utf-8"))
    decks["societies"][0]["objectives"]["orientation"].append("a-flag-nothing-grants")
    path = tmp_path / "DECKS.json"
    path.write_text(json.dumps(decks), encoding="utf-8")
    errors = vp.validate_decks(path, vp.pack_paths([]))
    assert any("no pack grants" in e for e in errors)


def test_decks_are_not_validated_as_packs():
    assert DECKS not in vp.pack_paths([])


def test_every_location_and_department_needs_an_image_prompt(tmp_path, pack):
    bad = copy.deepcopy(pack)
    del bad["locations"][0]["art"]
    del bad["department"]["arrival_art"]
    errors = _validate(tmp_path, bad)
    assert any("locations[" in e and "art" in e for e in errors)
    assert any("department.arrival_art" in e for e in errors)


def test_art_contract_vocabulary_is_rejected(tmp_path, pack):
    bad = copy.deepcopy(pack)
    bad["locations"][0]["art"]["brief"] = (
        "A safety poster of a marble lobby with readable labels on every desk, halftone grain, "
        "every surface bare and unmarked"
    )
    errors = _validate(tmp_path, bad)
    assert sum("art-contract vocabulary" in e for e in errors) >= 2


def test_every_deck_card_needs_an_image_prompt(tmp_path):
    decks = json.loads(DECKS.read_text(encoding="utf-8"))
    decks["mutations"][0].pop("art_prompt")
    path = tmp_path / "DECKS.json"
    path.write_text(json.dumps(decks), encoding="utf-8")
    errors = vp.validate_decks(path, vp.pack_paths([]))
    assert any("art_prompt" in e for e in errors)


# Hidden Test Results (t-022)

def _grade_gated(pack):
    return [c for c in pack["boss"]["choices"] if (c["requires"] or {}).get("grade")]


def test_every_card_grades_and_every_pack_grades_all_four_axes():
    for path in vp.pack_paths([]):
        pack = json.loads(path.read_text(encoding="utf-8"))
        raised = set()
        for card in pack["encounters"]:
            card_grades = [
                (ch.get(k) or {}).get("grades") for ch in card["choices"] for k in ("success", "failure")
            ]
            assert any(card_grades), f"{path.name}:{card['id']} grades nothing"
            for g in filter(None, card_grades):
                raised.update(k for k, v in g.items() if v > 0)
        assert raised == set(vp.GRADES), path.name
        assert _grade_gated(pack), f"{path.name}: some review route should need a grade"


def test_a_card_with_no_grades_is_rejected(tmp_path, pack):
    bad = copy.deepcopy(pack)
    for ch in bad["encounters"][0]["choices"]:
        for k in ("success", "failure"):
            if ch.get(k):
                ch[k].pop("grades", None)
    assert any("grades the player" in e for e in _validate(tmp_path, bad))


def test_grade_values_are_small_nonzero_integers(tmp_path, pack):
    bad = copy.deepcopy(pack)
    bad["encounters"][0]["choices"][0]["success"]["grades"] = {"spite": 3, "charisma": 1}
    errors = _validate(tmp_path, bad)
    assert any("spite must be a nonzero integer in -2..2" in e for e in errors)
    assert any("unknown grade 'charisma'" in e for e in errors)


def test_only_a_review_may_gate_on_a_grade(tmp_path, pack):
    bad = copy.deepcopy(pack)
    bad["encounters"][0]["choices"][0]["requires"] = {"grade": {"spite": 1}}
    assert any("only a department review may gate" in e for e in _validate(tmp_path, bad))


def test_grade_gate_must_be_reachable(tmp_path, pack):
    bad = copy.deepcopy(pack)
    _grade_gated(bad)[0]["requires"] = {"grade": {"spite": 6}}
    assert any("a run can earn at most" in e for e in _validate(tmp_path, bad))


def test_records_gates_count_grades_earned_in_orientation():
    """Records' review may ask for more than Records alone can grant: Orientation's grades carry down."""
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    alone = vp.grade_reach(records)
    above = vp.earlier_grade_reach(RECORDS, records["department"]["order"])
    assert all(above[axis] > 0 for axis in vp.GRADES)
    for ch in _grade_gated(records):
        (axis, minimum), = ch["requires"]["grade"].items()
        assert minimum <= alone[axis] + above[axis]


def test_decks_need_a_verdict_for_every_axis(tmp_path):
    decks = json.loads(DECKS.read_text(encoding="utf-8"))
    decks["test_results"]["verdicts"] = [v for v in decks["test_results"]["verdicts"] if v["axis"] != "spite"]
    path = tmp_path / "DECKS.json"
    path.write_text(json.dumps(decks), encoding="utf-8")
    assert any("verdicts must cover" in e for e in vp.validate_decks(path, vp.pack_paths([])))


# Restructuring (t-023)

@pytest.fixture
def records():
    return json.loads(RECORDS.read_text(encoding="utf-8"))


def _validate_records(tmp_path, records):
    """Validate an edited Records pack beside a copy of Orientation, so earlier outcomes and flags resolve."""
    (tmp_path / PACK.name).write_text(PACK.read_text(encoding="utf-8"), encoding="utf-8")
    path = tmp_path / RECORDS.name
    path.write_text(json.dumps(records), encoding="utf-8")
    return vp.validate_pack(path)


def test_records_restructures_on_every_orientation_outcome(records):
    orientation = json.loads(PACK.read_text(encoding="utf-8"))
    memos = records["restructurings"]
    assert memos[-1]["when"] is None
    kinds = {m["kind"] for m in memos}
    assert {"eliminate", "merge", "add"} <= kinds
    keyed = {o for m in memos if m["when"] for o in m["when"]["outcomes"]}
    outcomes = {o["id"] for o in orientation["boss"]["department_outcomes"]} - {"reorientation"}
    assert outcomes <= keyed, outcomes - keyed


def test_surface_department_may_not_restructure(tmp_path, pack):
    bad = copy.deepcopy(pack)
    bad["restructurings"] = [DEFAULT_MEMO]
    assert any("nothing above it" in e for e in _validate(tmp_path, bad))


def test_a_lower_department_needs_restructurings(tmp_path, records):
    records.pop("restructurings")
    assert any("needs Restructuring memos" in e for e in _validate_records(tmp_path, records))


def test_restructuring_shape_is_enforced(tmp_path, records):
    memos = records["restructurings"]
    merge = next(m for m in memos if m["kind"] == "merge")
    merge["location_ids"] = merge["location_ids"][:1]
    eliminate = next(m for m in memos if m["kind"] == "eliminate")
    eliminate["location_ids"] = ["the-moon"]
    eliminate["when"] = {"outcomes": ["not-an-outcome"], "flags": ["not-a-flag"]}
    memos.append(memos.pop(memos.index(next(m for m in memos if m["when"] is None))) | {"id": "x"})
    memos.insert(0, dict(DEFAULT_MEMO, id="early-default"))
    errors = _validate_records(tmp_path, records)
    assert any("names exactly 2" in e for e in errors)
    assert any("unknown location 'the-moon'" in e for e in errors)
    assert any("outcome 'not-an-outcome'" in e for e in errors)
    assert any("flag 'not-a-flag'" in e for e in errors)
    assert any("must come last" in e for e in errors)


def test_restructuring_reason_is_written_out(tmp_path, records):
    records["restructurings"][0]["reason"] = "Closed"
    assert any("reason" in e for e in _validate_records(tmp_path, records))


# Toy Division (t-011)

TOYS = ENC_DIR / "TOY-DIVISION-12.json"


def test_toy_division_pack_shape():
    toys = json.loads(TOYS.read_text(encoding="utf-8"))
    assert toys["department"]["id"] == "toy-division"
    assert toys["department"]["order"] == 3
    assert [loc["location_id"] for loc in toys["locations"]] == ["concept-lab", "focus-group-room", "proving-grounds"]
    assert all(len(loc["encounter_ids"]) == 4 for loc in toys["locations"])
    polarity = [e["polarity"] for e in toys["encounters"]]
    assert {p: polarity.count(p) for p in set(polarity)} == {"good": 4, "bad": 4, "mixed": 4}
    assert toys["boss"]["id"] == "snuggle-sentinels-launch-party"
    assert toys["boss"]["department_outcomes"][-1]["id"] == "back-to-the-drawing-board"


def test_toy_division_pays_off_earlier_flags():
    toys = json.loads(TOYS.read_text(encoding="utf-8"))
    required = {
        (ch["requires"] or {}).get("flag")
        for card in toys["encounters"] + [toys["boss"]]
        for ch in card["choices"]
    }
    assert {"bear-imprinted", "defused-mk0", "mailed-the-bear-upstairs", "sent-dale-to-toys", "owes-gus-a-favor"} <= required


def test_toy_division_restructures_on_every_records_outcome():
    toys = json.loads(TOYS.read_text(encoding="utf-8"))
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    keyed = {o for m in toys["restructurings"] if m["when"] for o in m["when"]["outcomes"]}
    outcomes = {o["id"] for o in records["boss"]["department_outcomes"]} - {"refiled"}
    assert outcomes <= keyed, outcomes - keyed


def test_toy_art_keeps_children_out_of_frame():
    """Tone guardrail (DESIGN-BRIEF): no child is ever pictured near the bears; adults play the children."""
    toys = json.loads(TOYS.read_text(encoding="utf-8"))
    briefs = [e["art"]["brief"] for e in toys["encounters"]] + [toys["boss"]["art"]["brief"]]
    briefs += [loc["art"]["brief"] for loc in toys["locations"]] + [toys["department"]["arrival_art"]["brief"]]
    for brief in briefs:
        assert not re.search(r"\b(child|children|kid|kids|toddler|baby|infant)\b", brief, re.I), brief


# Wellness & Testing (t-012)

WELLNESS = ENC_DIR / "WELLNESS-12.json"


def test_wellness_pack_shape():
    vault = json.loads(WELLNESS.read_text(encoding="utf-8"))
    assert vault["department"]["id"] == "wellness"
    assert vault["department"]["order"] == 4
    assert [loc["location_id"] for loc in vault["locations"]] == [
        "nutrition-studies", "cognitive-testing-chamber", "mutation-suite",
    ]
    psych = [e for e in vault["encounters"] if "psych-test" in e["tags"]]
    assert len(psych) >= 9, "the Vault carries the heaviest psych-test density in the game"
    assert vault["boss"]["id"] == "the-final-wellness-exam"
    assert vault["boss"]["department_outcomes"][-1]["id"] == "retest"


def test_wellness_pays_off_earlier_flags():
    vault = json.loads(WELLNESS.read_text(encoding="utf-8"))
    required = {
        (ch["requires"] or {}).get("flag")
        for card in vault["encounters"] + [vault["boss"]]
        for ch in card["choices"]
    }
    assert {"saved-pip", "assigned-as-proctor", "knows-the-incident", "heard-the-squeak-code",
            "kevin-owes-you", "has-true-minutes"} <= required


def test_wellness_restructures_on_every_toy_division_outcome():
    vault = json.loads(WELLNESS.read_text(encoding="utf-8"))
    toys = json.loads(TOYS.read_text(encoding="utf-8"))
    keyed = {o for m in vault["restructurings"] if m["when"] for o in m["when"]["outcomes"]}
    outcomes = {o["id"] for o in toys["boss"]["department_outcomes"]} - {"back-to-the-drawing-board"}
    assert outcomes <= keyed, outcomes - keyed


def test_wellness_avoids_borrowed_facilities():
    """Original facility only (t-012): no Aperture or Vault-Tec likeness anywhere in the pack."""
    text = WELLNESS.read_text(encoding="utf-8").lower()
    for borrowed in ("aperture", "vault-tec", "vault boy", "portal", "turret", "companion cube", "cake"):
        assert not re.search(rf"\b{re.escape(borrowed)}\b", text), borrowed
