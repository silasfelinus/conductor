"""The expanded Ruler Hooked fish roster must have a complete, paintable queue."""
from pathlib import Path

import yaml

from scripts import build_ruler_hooked_art_queue as queue


def test_expanded_fish_stays_balanced_and_staged():
    roster = yaml.safe_load(queue.FISH_ROSTER.read_text(encoding="utf-8"))
    fish = roster["fish"]
    entries = queue.fish_entries()
    assert len(fish) == len(entries) == 36
    assert {f["slug"] for f in fish} == {
        entry["id"].removeprefix("ruler-hooked-fish-") for entry in entries
    }
    for affinity in ("GOOD", "NEUTRAL", "EVIL"):
        assert sum(f["affinity"] == affinity for f in fish) == 12

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
        assert request.get("auto_submit") is True
        assert request["prompt"] == entry["prompt"]
        assert queue.contract_violations(request["prompt"]) == []
        if entry["id"] not in {
            f"ruler-hooked-fish-{fish['slug']}" for fish in fish[:15]
        }:
            assert len(request["prompt"]) <= 900
