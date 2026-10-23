"""Krea composition -> verified editorial keeper -> Arthemy img2img contract."""
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from scripts import activate_zuzu_gamebook_stylepass as activate
from scripts import enqueue_art_requests as enqueue
from scripts import sweep_art_ledgers as sweep
from scripts.repair_negation_art_prompts import violations

ART = Path(__file__).resolve().parents[1] / "projects/zuzu-gamebook/art"


def fixture_review():
    round18 = yaml.safe_load((ART / "ROUND-18-KREA-COMPOSITION.yaml").read_text())
    selections = yaml.safe_load((ART / "ROUND-18-SELECTIONS.yaml").read_text())
    receipt = {"round": round18["round"], "complete": True, "fetched": 9, "candidates": []}
    for i, s in enumerate(round18["subjects"]):
        s["jobs"] = {"krea-composition": 47000 + i}
        s["art"] = {"krea-composition": {"status": "DONE", "art_image_id": 27000 + i}}
        receipt["candidates"].append({
            "section": s["section"], "seed": s["seed"],
            "artJobId": 47000 + i, "artImageId": 27000 + i,
            "verified": True, "sha256": (f"{i+1:064x}"),
        })
    for section, checks in activate.CRITICAL.items():
        pick = next(s for s in round18["subjects"] if s["section"] == section)
        i = round18["subjects"].index(pick)
        selections["selections"][section] = {
            "candidate_key": pick["key"],
            "image_sha256": f"{i+1:064x}",
            "ratings": {key: 2 for key in activate.SCORES},
            "critical": {key: True for key in checks},
            "notes": "Actual image reviewed, all subject details visibly present in frame.",
        }
    return round18, selections, receipt


def test_round18_krea_is_live_and_does_not_start_style_jobs_early():
    data = yaml.safe_load((ART / "ROUND-18-KREA-COMPOSITION.yaml").read_text())
    assert sweep.is_auto_ledger(data)
    assert data["auto_submit"] is True and data["is_public"] is False
    assert data["cast_loras"] is False
    assert data["series"] == "zuzu-koala-assassin"
    lane, = data["lanes"]
    assert lane["engine"] == "krea2"
    subjects = data["subjects"]
    assert len(subjects) == 9
    assert len({s["key"] for s in subjects}) == 9
    assert set(s["section"] for s in subjects) == set(activate.CRITICAL)
    assert {sec: sum(s["section"] == sec for s in subjects) for sec in activate.CRITICAL} == {
        sec: 3 for sec in activate.CRITICAL
    }
    for subject in subjects:
        req = enqueue.build_request(data, lane, subject)
        assert req["engine"] == "krea2"
        assert req["isPublic"] is False and req["projectSlug"] == "zuzu-gamebook"
        assert req["promptString"] and len(req["promptString"]) > 200
        assert "sourceImageBase64" not in req
        assert list(violations(req["promptString"])) == [], "Krea positive prompt must not contain negation traps"
    template = yaml.safe_load((ART / "ROUND-19-ARTHEMY-STYLEPASS.yaml").read_text())
    assert not sweep.is_auto_ledger(template)
    assert template["auto_submit"] is False and template["subjects"] == []


def test_only_verified_selected_krea_keepers_activate_six_img2img_jobs():
    r18, selection, receipt = fixture_review()
    chosen = activate.approved_sources(r18, selection, receipt)
    template = yaml.safe_load((ART / "ROUND-19-ARTHEMY-STYLEPASS.yaml").read_text())
    result = activate.build_stage19(template, chosen)
    assert sweep.is_auto_ledger(result)
    assert len(result["subjects"]) == 6
    keys = {s["key"] for s in result["subjects"]}
    assert len(keys) == 6
    ids = [s["source_image_id"] for s in result["subjects"]]
    assert len(set(ids)) == 3
    lane, = result["lanes"]
    assert lane["engine"] == "sdxl-img2img"
    for s in result["subjects"]:
        req = enqueue.build_request(result, lane, s, source_image="data:image/png;base64,AA==")
        assert req["sourceImageBase64"].startswith("data:image/png")
        assert req["engine"] == "sdxl-img2img"
        assert req["checkpoint"] == "Illustrious/arthemyWesternArt_v30.safetensors"
        assert req["projectSlug"] == "zuzu-gamebook"
        assert req["isPublic"] is False
        assert req["denoise"] in (0.28, 0.43)
        assert "negativePrompt" in req
        assert s["source_krea_key"].startswith("gb18-")
    with pytest.raises(AssertionError):
        activate.build_stage19(result, chosen)


@pytest.mark.parametrize("alter", [
    lambda d,s,r: s["selections"]["a2-gift"]["ratings"].update(scene_truth=0),
    lambda d,s,r: s["selections"]["a2-gift"]["critical"].update(single_nail=False),
    lambda d,s,r: s["selections"]["a2-gift"].update(image_sha256="0"*64),
    lambda d,s,r: s["selections"]["a2-gift"].update(candidate_key="gb18-fake"),
    lambda d,s,r: s["selections"]["a2-gift"].update(notes="Review actual Krea image"),
    lambda d,s,r: d["subjects"][3]["art"]["krea-composition"].update(status="PENDING"),
    lambda d,s,r: r["candidates"][3].update(verified=False),
    lambda d,s,r: s["selections"]["a2-bell-view"]["ratings"].update(scene_truth=True),
])
def test_fidelity_or_provenance_failure_blocks_style_activation(alter):
    r18, selection, receipt = fixture_review()
    alter(r18, selection, receipt)
    with pytest.raises(AssertionError):
        activate.approved_sources(r18, selection, receipt)


def test_review_ledger_main_does_not_contain_preapproved_candidates():
    selections = yaml.safe_load((ART / "ROUND-18-SELECTIONS.yaml").read_text())["selections"]
    for item in selections.values():
        assert item["candidate_key"] is None
        assert item["image_sha256"] is None
        assert set(item["ratings"].values()) == {None}
        assert not any(item["critical"].values())
