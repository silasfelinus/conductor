"""Contract for Shifting Lands' new source-backed art generation round."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects" / "zuzu-shifting-lands" / "art"


def test_round_four_card_coverage_and_continuity():
    source = json.loads((ART / "V6-CARD-BRIEFS.json").read_text())
    ledger = yaml.safe_load((ART / "ROUND-4.yaml").read_text())
    entries = ledger["subjects"]
    v6 = entries[:-2]
    fixes = entries[-2:]
    canonical = {c["card"]: c for c in source["cards"]}

    assert len(canonical) == 72
    assert len(entries) == 74
    assert len({entry["key"] for entry in entries}) == 74
    assert len({entry["seed"] for entry in entries}) == 74
    assert {entry["card"] for entry in v6} == set(canonical)
    assert ledger["is_public"] is False
    assert ledger["cast_loras"] is False
    assert len(ledger["lanes"]) == 1
    assert ledger["lanes"][0]["checkpoint"] == "Illustrious/arthemyWesternArt_v30.safetensors"

    for entry in v6:
        card = canonical[entry["card"]]
        assert entry["land"] == card["land"]
        assert entry["task"] == "t-033"
        assert card["brief"].split(".")[0] in entry["prompt_prose"]
        assert len(entry["prompt_tags"]) > 120
        assert entry["lane"] == "arthemy-house"
        assert entry["size"] == "1344x768"

    for entry in fixes:
        assert entry["card"] == "three-cups-on-the-table"
        assert "THREE" in entry["prompt_tags"]
        assert "mouse" in entry["prompt_tags"]
        assert "cups" in entry["prompt_prose"]
        assert entry["land"] == "dustwater"


def test_round_four_cast_is_not_replaced_by_random_species():
    entries = yaml.safe_load((ART / "ROUND-4.yaml").read_text())["subjects"]
    assert all("species" in s["negative"] for s in entries)
    assert all(s["lane"] == "arthemy-house" for s in entries)
    assert all("Zuzu" not in s["prompt_tags"] for s in entries)
