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


def test_long_fish_prompts_show_exactly_one_complete_specimen():
    roster = yaml.safe_load(queue.FISH_ROSTER.read_text(encoding="utf-8"))["fish"]
    staged = queue.staged_rows(queue.ART_PROMPTS.read_text(encoding="utf-8"))
    entries = {
        entry["id"].removeprefix("ruler-hooked-fish-"): entry
        for entry in queue.fish_entries()
    }
    elongated = {
        "bridgeback-sturgeon", "crown-of-reeds-pike", "tollbell-sturgeon",
        "ashbelly-gar", "tithe-lamprey", "clockwork-riffle-loach",
        "parcelglass-eel", "lockjaw-burbot", "treaty-sailfish",
        "pierlock-eel", "border-accordionfish",
    }
    assert elongated <= entries.keys()
    for species in roster:
        slug = species["slug"]
        entry = entries[slug]
        prompt = entry["prompt"]
        if slug == "choirfish":
            assert "all three fish of the trio" in prompt
            assert "exactly one single fish" not in prompt
        elif slug in elongated or queue.LONG_FISH_BODY.search(species["silhouette"]):
            assert "exactly one single" in prompt, slug
            assert "head to tail fully visible" in prompt, slug
            assert "no other fish" in prompt, slug
            assert " ".join(staged[entry["id"]]["prompt"].split()) == prompt, slug
        else:
            assert (
                "the whole creature clearly visible in profile" in prompt
                or "one complete fish shown clearly in side profile" in prompt
            ), slug
        assert queue.contract_violations(prompt) == [], slug
