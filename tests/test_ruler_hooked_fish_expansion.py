"""The expanded Ruler Hooked fish roster must have a complete, paintable queue."""
from pathlib import Path

import yaml

from scripts import build_ruler_hooked_art_queue as queue


def test_expanded_fish_stays_balanced_and_staged():
    roster = yaml.safe_load(queue.FISH_ROSTER.read_text(encoding="utf-8"))
    fish = roster["fish"]
    entries = queue.fish_entries()
    slugs = [f["slug"] for f in fish]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    assert duplicates == [], f"duplicate fish roster slugs: {duplicates}"
    # Approved shipped catalog target is 40-60 species (t-031); the roster may
    # grow in batches toward it without editing this test each time.
    assert 36 <= len(fish) <= 60
    assert len(fish) == len(entries)
    assert {f["slug"] for f in fish} == {
        entry["id"].removeprefix("ruler-hooked-fish-") for entry in entries
    }
    for affinity in ("GOOD", "NEUTRAL", "EVIL"):
        assert sum(f["affinity"] == affinity for f in fish) * 3 == len(fish)

    staged = yaml.safe_load(
        (Path(__file__).resolve().parent.parent / "projects" / "art-prompts.yaml").read_text()
    )
    requests = {
        row["id"]: row for row in staged["requests"]
        if row.get("source") == "ruler-hooked" and row.get("lane") == "fish"
    }
    for entry in entries:
        request = requests[entry["id"]]
        assert request["image_path"] == entry["image_path"]
        assert request["status"] in {"pending", "queued", "running", "processing", "done"}
        assert request["target_repo"] == "silasfelinus/kind_robots"
        if entry["id"] not in {
            f"ruler-hooked-fish-{species['slug']}" for species in fish[:15]
        }:
            assert request.get("auto_submit") is True
            assert request["prompt"] == entry["prompt"]
            assert queue.contract_violations(request["prompt"]) == []
            assert len(request["prompt"]) <= 900
