"""Supplement Capes checkpoint style gate with map geometry and portrait acting."""
from pathlib import Path

import yaml

from scripts.enqueue_art_requests import build_request, compose_prompt

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "projects/comet-city-academy/art"
FIRST = BASE / "CAPES-WESTERN-STYLE-CHECK-ROUND-1.yaml"
EXTENSION = BASE / "CAPES-WESTERN-STYLE-CHECK-MAP-PORTRAIT.yaml"


def test_style_check_covers_six_core_production_categories():
    first = yaml.safe_load(FIRST.read_text())
    added = yaml.safe_load(EXTENSION.read_text())
    assert len(first["lanes"]) == len(added["lanes"]) == 6
    assert {x["key"] for x in first["lanes"]} == {x["key"] for x in added["lanes"]}
    assert [x["checkpoint"] for x in first["lanes"] if x.get("checkpoint")] == [
        x["checkpoint"] for x in added["lanes"] if x.get("checkpoint")
    ]
    old_keys = {x["key"] for x in first["subjects"]}
    assert {"cornerstone-hero", "backdraft-villain", "warren-wreckers", "science-lab"} <= old_keys
    assert {x["key"] for x in added["subjects"]} == {
        "academy-city-quad-map", "firewall-alert-portrait"
    }
    assert not old_keys & {x["key"] for x in added["subjects"]}
    assert {x["seed"] for x in first["subjects"]}.isdisjoint(
        x["seed"] for x in added["subjects"]
    )
    assert added["auto_submit"] is False
    assert added["is_public"] is False
    assert added["priority"] == 900
    assert added["project_slug"] == first["project_slug"]
    for lane in added["lanes"]:
        label = (lane.get("checkpoint") or lane["key"]).lower()
        assert not any(word in label for word in ("pony", "furry", "flux"))
        assert lane["engine"] in ("comfy", "krea2")
    cells = []
    for s in added["subjects"]:
        assert s["asset"].startswith("comet-city-academy/style-check-v1/")
        assert s["prompt_prose"] and s["prompt_tags"] and s["negative"]
        assert 629107 <= s["seed"] <= 629108
        for lane in added["lanes"]:
            r = build_request(added, lane, s)
            assert r["projectSlug"] == "comet-city-academy"
            assert r["priority"] == 900
            assert r["isPublic"] is False
            assert r["seed"] == s["seed"]
            assert r["promptString"] == compose_prompt(lane, s)
            assert r["width"] > 0 and r["height"] > 0
            saved = (s.get("jobs") or {}).get(lane["key"])
            assert saved is None or (isinstance(saved, int) and saved > 0)
            cells.append((s["key"], lane["key"]))
    assert len(set(cells)) == 12


def test_map_has_real_topology_and_portrait_tests_facial_acting():
    extra = yaml.safe_load(EXTENSION.read_text())
    subjects = {x["key"]: x for x in extra["subjects"]}
    map_scene = subjects["academy-city-quad-map"]
    portrait = subjects["firewall-alert-portrait"]
    assert map_scene["size"] == "1344x768"
    for landmark in ("fountain", "library", "dormitory", "science", "plaza", "northwest"):
        assert landmark in map_scene["prompt_prose"].lower()
    assert portrait["size"] == "896x1152"
    for feature in ("brown skin", "eyebrows", "dark expressive eyes", "determination"):
        assert feature in portrait["prompt_prose"].lower()
    assert "no words" in portrait["prompt_prose"].lower()
