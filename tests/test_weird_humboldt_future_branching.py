"""Weird Humboldt t-013: future-state branching, sober parity and no forced ideal outcome (text-only)."""
import importlib.util
import re
from collections import Counter
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_weird_humboldt_cards.py"
spec = importlib.util.spec_from_file_location("wh_validate_branching", SCRIPT)
wh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wh)

CARDS = wh.load_cards()
ANCHORS = wh.load_anchors()
ENDINGS = wh.load_endings()
SIGS = wh.load_signatures()["signatures"]
CORES = {e["id"]: e for e in ENDINGS if e["kind"] == "core"}
COUNTY = [e for e in ENDINGS if e["kind"] == "county"]

# Flag-name vocabulary that would make an ending depend on who the player is or what they took.
IDENTITY_GATES = re.compile(
    r"wiyot|tuluwat|hmong|hispanic|latino|latina|asian|native|tribal|ethnic|disab|"
    r"sober|tipsy|stoned|tripping|cocaine|meth|mdma|drunk|high_",
    re.I,
)


def flag_sources() -> dict[str, list[tuple[str, str]]]:
    """flag -> [(card id, 'base' | opening state)] for every card or anchor effect that sets it."""
    out: dict[str, list[tuple[str, str]]] = {}
    for card in CARDS + ANCHORS:
        groups = [("base", card["options"])]
        for state, extra in (card.get("by_state") or {}).items():
            if "extra_option" in extra:
                groups.append((state, [extra["extra_option"]]))
        for where, opts in groups:
            for opt in opts:
                for branch in ("success", "failure"):
                    for eff in opt.get(branch, {}).get("effects", []):
                        if eff.startswith("flag:"):
                            out.setdefault(eff[5:], []).append((card["id"], where))
    return out


SOURCES = flag_sources()


def test_every_ending_flag_is_settable_in_base_play_so_sober_parity_holds():
    # A flag reachable only through a by_state extra option would gate an ending behind a state.
    for e in ENDINGS:
        for flag in e["requires_flags"]:
            assert any(w == "base" for _, w in SOURCES.get(flag, [])), (e["id"], flag)


def test_flags_never_name_identity_or_substance_gates():
    for flag in SOURCES:
        assert not IDENTITY_GATES.search(flag), flag
    for e in ENDINGS:
        for flag in e["requires_flags"]:
            assert not IDENTITY_GATES.search(flag), (e["id"], flag)


def test_all_four_hopeful_personal_outcomes_reachable_without_fixed_opening():
    for lead in wh.LEADS:
        core = CORES[f"E-{lead}.hope"]
        for flag in core["requires_flags"]:
            assert SOURCES.get(flag), (core["id"], flag)
    ids = {s["id"] for s in SIGS}
    for lead in wh.LEADS:
        for opening in wh.OPENINGS:
            assert f"{lead}.{opening}.hope" in ids
            assert f"{lead}.{opening}.dark" in ids


def test_hope_and_dark_cores_do_not_share_a_forced_path():
    for lead in wh.LEADS:
        hope = frozenset(CORES[f"E-{lead}.hope"]["requires_flags"])
        dark = frozenset(CORES[f"E-{lead}.dark"]["requires_flags"])
        assert hope - dark, lead
        assert dark - hope, lead


def test_anchor5_and_6_offer_more_than_one_outcome_flag():
    for anchor_id in ("WH-A5", "WH-A6"):
        anchor = next(a for a in ANCHORS if a["id"] == anchor_id)
        flags = {
            eff[5:]
            for opt in anchor["options"]
            for br in ("success", "failure")
            for eff in opt.get(br, {}).get("effects", [])
            if eff.startswith("flag:")
        }
        assert len(flags) >= 3, anchor_id


def test_no_single_county_vote_wins_every_future():
    votes = {f for f in SOURCES if f.startswith("vote_")}
    assert len(votes) >= 5
    uses = Counter(f for e in COUNTY for f in e["requires_flags"] if f.startswith("vote_"))
    assert votes == frozenset(uses), "every vote outcome must be able to shape a county future"
    for flag, n in uses.items():
        assert n <= len(COUNTY) // 2, (flag, n)


def test_no_unreachable_county_futures():
    assert len(COUNTY) >= wh.MIN_COUNTY_MOTIFS
    for e in COUNTY:
        for flag in e["requires_flags"]:
            assert flag in SOURCES, (e["id"], flag)


def test_county_futures_are_distinct_and_all_carry_a_cost():
    pairs = [tuple(sorted(e["requires_flags"])) for e in COUNTY]
    assert len(frozenset(pairs)) == len(pairs)
    for e in COUNTY:
        assert e["cost"].strip(), e["id"]


def test_ending_flags_do_not_depend_on_solving_the_transmitter_mystery():
    for e in ENDINGS:
        for flag in e["requires_flags"]:
            assert not re.search(r"transmitter|solved|culprit", flag, re.I), (e["id"], flag)


def test_cedar_parents_never_split_in_endings_signatures_or_cards():
    breakup = re.compile(r"divorc|separated|split up|broke up|remarried|widow", re.I)
    cedar = [e for e in ENDINGS if e.get("lead") == "cedar"]
    assert len(cedar) == 2
    for e in cedar:
        assert not breakup.search(str(e)), e["id"]
    for s in SIGS:
        if s["id"].startswith("cedar."):
            assert not breakup.search(s["paragraph"]), s["id"]
    for card in CARDS + ANCHORS:
        text = " ".join(str(card.get(k, "")) for k in ("scene", "lead_reactions", "options"))
        if "parents" in text.lower() or "cedar" in text.lower():
            assert not breakup.search(text), card["id"]


def test_signatures_do_not_invent_stay_follow_jumps_or_assign_outcomes_by_opening():
    jump = re.compile(r"\byou (stayed with|stayed behind|followed (her|him|them|mara|kit|juniper|cedar)|switched|left (her|him|them))\b", re.I)
    caused = re.compile(r"because you (were|got) (sober|drunk|high|stoned|tipsy)", re.I)
    for s in SIGS:
        assert not jump.search(s["paragraph"]), s["id"]
        assert not caused.search(s["paragraph"]), s["id"]


def test_callbacks_reference_real_flags_across_several_chapters():
    chapters = Counter(c["chapter"] for c in CARDS if c.get("callbacks"))
    assert len(chapters) >= 4
    for card in CARDS + ANCHORS:
        for flag in card.get("callbacks", []):
            assert flag in SOURCES, (card["id"], flag)
