"""Prom identity anatomy gates are evaluated before paying for another ArtJob."""

from pathlib import Path

import yaml

from scripts import enqueue_art_requests as enqueue
from scripts.prom_canon_art_anatomy import (
    CANON_TRAITS,
    identity_for_subject,
    missing_canon_traits,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGERS = ROOT / "projects/comet-city-academy/art"
ORIGINS = ("accident", "mutant", "tech", "magic", "alien", "psychic")
AFFINITIES = (
    "fire", "air", "earth", "water", "discipline", "genius",
    "birthright", "social",
)


def subject(signature, prose):
    return {
        "key": "test-canon-anatomy",
        "asset": f"comet-city-academy/identities/{signature}/outcomes/hero",
        "prompt_prose": prose,
        "size": "1344x768",
    }


def test_all_48_stable_personalities_have_a_defining_visual_trait():
    expected = {f"{o}-{a}" for o in ORIGINS for a in AFFINITIES}
    assert set(CANON_TRAITS) == expected
    assert all(CANON_TRAITS[k] for k in expected)


def test_four_arm_morphology_cannot_be_replaced_by_a_dance_or_weapons():
    bad = subject(
        "mutant-discipline",
        "Asha dances and catches four falling people with her hands, "
        "then points two floating guns over the harbor.",
    )
    assert missing_canon_traits(bad) == [
        "canon-anatomy:mutant-discipline:four biological arms"
    ]
    rescued = dict(
        bad,
        prompt_prose=(
            "A poised young woman with a second pair of slender arms below "
            "her first grips a rescue cable and steadies a falling child."
        ),
    )
    assert missing_canon_traits(rescued) == []


def test_granny_and_dr_frog_reject_wrong_age_or_wrong_species():
    granny = subject("magic-earth", "A smiling child rides a patchwork bus.")
    assert len(missing_canon_traits(granny)) == 2
    granny["prompt_prose"] = (
        "An elderly woman with silver hair in two high buns directs a school bus."
    )
    assert missing_canon_traits(granny) == []
    frog = subject(
        "tech-genius",
        "A green cartoon frog with a brass wrench hops over a computer.",
    )
    assert len(missing_canon_traits(frog)) == 2
    frog["prompt_prose"] = (
        "An adult human inventor with oversized brass safety goggles "
        "adjusts his frog-footed mechanical suit."
    )
    assert missing_canon_traits(frog) == []


def test_only_structured_cast_identity_slots_activate_the_guard():
    unknown = {
        "key": "crowd-shot",
        "entity": "generic-crowd",
        "asset": "comet-city-academy/maps/courtyard",
        "prompt_prose": "Four people run beneath orange lights.",
    }
    assert identity_for_subject(unknown) is None
    assert missing_canon_traits(unknown) == []
    assert identity_for_subject({
        "entity": "mutant-discipline", "asset": "other-project/characters"
    }) == "mutant-discipline"


def test_submission_contract_rejects_bad_morphology_even_without_web_contract():
    bad = subject(
        "mutant-discipline",
        "Asha in a maroon jacket dances across a pier, tossing a "
        "dangerous glowing crate toward two distant enemies.",
    )
    good = subject(
        "mutant-discipline",
        "Asha has four biological arms naturally attached at her torso. "
        "She dances across a pier while her lower two arms hold a crate.",
    )
    lane = {"key": "krea2", "engine": "krea2", "prompt": "prose"}
    checks = enqueue.contract_rules(
        [(bad, lane), (good, lane)],
        live=lambda rows: [{"id": row["id"], "violations": []} for row in rows],
    )
    assert any(r.startswith("canon-anatomy:") for r in checks[0])
    assert not any(r.startswith("canon-anatomy:") for r in checks[1])


def test_bad_prompt_never_reaches_production_art_enqueue(tmp_path):
    bad = subject(
        "mutant-discipline",
        "An academy dancer with maroon clothes fights a robot in a "
        "flooded alley. She has two hands and throws a pair of blades.",
    )
    bad["lane"] = "krea2"
    ledger = {
        "project_slug": "comet-city-academy",
        "lanes": [{"key": "krea2", "engine": "krea2", "prompt": "prose"}],
        "subjects": [bad],
    }
    path = tmp_path / "ashas-art.yaml"
    path.write_text(yaml.safe_dump(ledger), encoding="utf-8")
    called = []
    assert enqueue.submit(
        path,
        "",
        ledger,
        list(enqueue.iter_cells(ledger)),
        post=lambda body: called.append(body) or (200, {"data": {"jobId": 42}}),
        live=lambda rows: [{"id": row["id"], "violations": []} for row in rows],
    ) == (0, 1)
    assert called == []
    assert not bad.get("jobs")


def test_all_prom_art_ledgers_have_no_unsubmitted_canon_anatomy_gaps():
    """Inspect every current Prom ledger, grandfathering only durable jobs.

    Older submitted images include obsolete canon (pre-2026-10-28 three-name
    personalities). Never rewrite/delete or resubmit their ArtJob receipts
    just to make a static prompt check green.
    """
    visited, matching = 0, 0
    new_violations, legacy_violations = [], []
    for path in sorted(LEDGERS.glob("*.yaml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for item in document.get("subjects") or []:
            if not isinstance(item, dict):
                continue
            visited += 1
            if identity_for_subject(item) is None:
                continue
            matching += 1
            problems = missing_canon_traits(item)
            if not problems:
                continue
            jobs = item.get("jobs") or {}
            lanes = document.get("lanes") or []
            for lane in lanes:
                key = lane.get("key")
                if item.get("lane") and item["lane"] != key:
                    continue
                accepted = type(jobs.get(key)) is int and jobs[key] > 0
                detail = (
                    f"{path.name}:{item.get('key')}[{key}]:"
                    + ",".join(problems)
                )
                (legacy_violations if accepted else new_violations).append(detail)
    assert visited > 600
    assert matching >= 400
    assert not new_violations, (
        "Rewrite these unsubmitted prompts before enqueue: "
        + "; ".join(new_violations[:40])
    )
    # Provenance remains inspectable: this is not approval of the known
    # already-enqueued wrong-person designs. Existing jobs are retained.
    assert all("canon-anatomy:" in detail for detail in legacy_violations)
