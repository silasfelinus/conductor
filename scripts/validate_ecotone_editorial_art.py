#!/usr/bin/env python3
"""Validate the private Ecotone art reroll before any live queue submission."""
from __future__ import annotations

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "projects/weird-humboldt/art/ART-STANDARD.yaml"
REVISION = ROOT / "projects/weird-humboldt/art/ART-EDITORIAL-ROUND-1.yaml"
LANES = {"zimage", "krea2", "arthemy", "novacomic"}
HELD = re.compile(r"\b(?:wiyot|tuluwat|massacre|ceremon(?:y|ial)|tribal|indigenous|mara|wh-121|baduwa)\b", re.I)


def main() -> None:
    base = yaml.safe_load(BASE.read_text(encoding="utf-8"))
    reroll = yaml.safe_load(REVISION.read_text(encoding="utf-8"))
    originals = base["subjects"]
    revisions = reroll["subjects"]
    assert len(originals) == 237, "Original 237 Ecotone art subjects must be preserved"
    assert len(revisions) == 15, "This reviewed round must contain exactly 15 revision subjects"
    assert {lane["key"] for lane in reroll["lanes"]} == LANES
    assert reroll["is_public"] is False, "Rerolls must stay private"
    assert reroll["is_mature"] is False
    assert len({s["key"] for s in revisions}) == len(revisions)
    assert len({s["seed"] for s in revisions}) == len(revisions)
    original_keys = {s["key"] for s in originals}
    assert len(original_keys) == 237
    assert all(set(s.get("jobs", {})) == LANES for s in originals), (
        "Original 948 already-submitted ArtJobs must not be reset or duplicated"
    )
    for subject in revisions:
        key = subject["key"]
        assert key.startswith("edit-") and "std-" not in key
        assert subject["asset"].startswith("editorial-round-1/")
        assert "1344x768" == subject["size"]
        assert key.replace("edit-", "std-", 1) in original_keys, key
        assert len(subject["prompt_prose"]) > 150, key
        assert len(subject["prompt_tags"]) > 40, key
        assert not HELD.search(
            " ".join(str(subject.get(k, "")) for k in ("key", "asset", "title", "prompt_prose", "prompt_tags"))
        ), f"Consultation-held material cannot be enqueued: {key}"
        assert set(subject.get("jobs", {})) <= LANES, key
        assert all(isinstance(job, int) and job > 0 for job in subject.get("jobs", {}).values()), key
    print("Ecotone art OK: original 237 x 4 ArtJobs preserved; 15 safe revisions x 4 lanes ready.")


if __name__ == "__main__":
    main()
