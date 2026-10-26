"""The forty-eight 2-step Capes powers and 113 literal image requests."""
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
STORY=ROOT/"projects/comet-city-academy/content/COMPOSITE-POWERS-ROUND-1.json"
ART=ROOT/"projects/comet-city-academy/art/COMPOSITE-POWERS-ROUND-1.yaml"

def test_capes_48_unique_composites_and_vows():
    d=json.loads(STORY.read_text())
    assert d["counts"]=={"forms":6,"elements":8,"combinations":48,"vows":3}
    assert len(d["powers"])==48
    seen=set()
    for form in d["forms"]:
        for element in d["elements"]:
            matching=[p for p in d["powers"] if p["form"]==form["id"] and p["element"]==element["id"]]
            assert len(matching)==1
            p=matching[0]
            assert p["id"] not in seen
            seen.add(p["id"])
            assert p["name"] and len(p["training"])>65 and p["special_route"]["tradeoff"]
            assert set(p["finales"])=={"shelter","unmask","claim"}
            assert len({*p["finales"].values()})==3
    assert next(p["name"] for p in d["powers"] if p["id"]=="impact-fire")=="Flaming Fists"

def test_capes_113_krea2_prompts_are_unique_and_reproducible():
    d=json.loads(STORY.read_text())
    art=yaml.safe_load(ART.read_text())
    expected=set()
    expected|={f'picker-form-{form["id"]}' for form in d["forms"]}
    expected|={f'picker-element-{element["id"]}' for element in d["elements"]}
    expected|={f'picker-vow-{vow["id"]}' for vow in d["vows"]}
    for p in d["powers"]:
        expected.add(f'signature-{p["id"]}')
        expected.add(f'prom-{p["id"]}')
    assert len(expected)==113
    assert art["project_slug"]=="comet-city-academy"
    assert art["auto_submit"] is True
    assert art["lanes"][0]["engine"]=="krea2"
    rows=art["subjects"]
    assert len(rows)==113
    assert set(row["key"] for row in rows)==expected
    for row in rows:
        assert row["lane"]=="krea2" and row["prompt_prose"] and row["size"]=="1344x768"
        assert row["asset"]==f'comet-city-academy/powers/{row["key"]}'
        assert not row.get("jobs"), "Generator must assign real jobs, never authored IDs"
