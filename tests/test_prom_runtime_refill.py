"""Prom of Doom runtime refill and franchise-safe re-render ledgers (2026-10-30 art refill)."""

from pathlib import Path

import yaml

from scripts.enqueue_art_requests import build_request, iter_cells
from scripts.repair_negation_art_prompts import violations

ART = Path(__file__).resolve().parents[1] / "projects/comet-city-academy/art"
HELD = {
    "identities/mutant-air/student",
    "identities/mutant-genius/hero",
    "encounters/the-class-list-has-two-endings",
    "identities/psychic-discipline/outcomes/villain",
    "identities/tech-genius/outcomes/student",
}
# The cues behind the rejected franchise look-alikes.
FRANCHISE_CUES = ("academy scarf", "lightning scar", "logo", "emblem", "round tortoiseshell glasses")


def _subjects(name, priority):
    data = yaml.safe_load((ART / name).read_text())
    assert data["auto_submit"] is True and data["is_public"] is False
    assert data["priority"] == priority
    (lane,) = data["lanes"]
    assert (lane["engine"], lane["prompt"]) == ("krea2", "prose")
    for subject, render_lane in iter_cells(data):
        text = subject["prompt_prose"].lower()
        assert violations(subject["prompt_prose"]) == [], subject["key"]
        assert not any(cue in text for cue in FRANCHISE_CUES), subject["key"]
        assert "unpeopled" not in text and "deserted" not in text, subject["key"]
        assert build_request(data, render_lane, subject)["priority"] == priority
    return data["subjects"]


def test_refill_covers_unshipped_slots_without_duplicates():
    subjects = _subjects("RUNTIME-REFILL-ROUND-1.yaml", 700)
    keys = [s["asset"].removeprefix("comet-city-academy/") for s in subjects]
    assert len(keys) == len(set(keys)) == 148
    assert not set(keys) & HELD
    groups = {k.split("/")[0] for k in keys}
    assert groups == {"identities", "incidents", "returns", "endings"}


def test_rerenders_replace_the_held_keys_and_old_jobs_are_rejected():
    subjects = _subjects("FRANCHISE-SAFE-RERENDERS-ROUND-1.yaml", 750)
    assert {s["asset"].removeprefix("comet-city-academy/") for s in subjects} == HELD
    for path in ART.glob("*.yaml"):
        if path.name == "FRANCHISE-SAFE-RERENDERS-ROUND-1.yaml":
            continue
        data = yaml.safe_load(path.read_text())
        for subject in data.get("subjects") or [] if isinstance(data, dict) else []:
            if (subject.get("asset") or "").removeprefix("comet-city-academy/") in HELD:
                assert all((art or {}).get("status") != "DONE" for art in (subject.get("art") or {}).values())
