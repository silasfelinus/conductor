"""Selected Shifting Desks art skins must cover every published station safely."""
import json
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects" / "shifting-desks" / "art"
PREFIX = "shifting-desks-style-v2-"


def test_style_catalog_covers_388_plates_and_pending_queue_is_a_valid_subset():
    # The queue is a work ledger, not an immutable archive. Fulfilled rows are
    # pruned by the art consumer (see projects/art-prompts.yaml header), so a
    # completed batch may legitimately have zero live requests.
    catalog = json.loads((ART / "STYLE-CATALOG.json").read_text())
    assert {s["id"] for s in catalog["styles"]} == {
        "classic", "corporate-noir", "western-cartoon"
    }
    subjects = catalog["subjects"]
    assert len(subjects) == 194
    assert len({(s["kind"], s["id"]) for s in subjects}) == 194
    assert all(s["prompt"] for s in subjects)
    assert all(s["classicImage"].startswith("/images/shifting-desks/") for s in subjects)

    expected_by_style = {
        style: {
            f"public/images/shifting-desks/styles/{style}/{s['classicImage'][len('/images/shifting-desks/'):]}"
            for s in subjects
        }
        for style in ("corporate-noir", "western-cartoon")
    }
    expected = set().union(*expected_by_style.values())
    # Coverage is certified by the durable source manifest, even after renders
    # leave the live queue. Neither style may quietly lose an authored station.
    assert all(len(paths) == 194 for paths in expected_by_style.values())
    assert len(expected) == 388

    all_requests = yaml.safe_load((ROOT / "projects/art-prompts.yaml").read_text())["requests"]
    entries = [e for e in all_requests if e.get("id", "").startswith(PREFIX)]
    ids = [e["id"] for e in entries]
    targets = [e["image_path"] for e in entries]
    assert len(entries) <= 388
    assert len(set(ids)) == len(entries)
    assert len(set(targets)) == len(entries)
    assert set(targets).issubset(expected)
    assert all(e["source"] == "shifting-desks" and e["variant"] == "image" for e in entries)
    assert all(e["project_target"] == e["project_slug"] == "shifting-desks" for e in entries)

    noir = [e for e in entries if e.get("style_family") == "corporate-noir"]
    cartoon = [e for e in entries if e.get("checkpoint_family") == "western-cartoon"]
    assert len(noir) + len(cartoon) == len(entries)
    assert len(noir) <= 194 and len(cartoon) <= 194
    assert all(e["engine"] == "krea2" and "checkpoint_family" not in e for e in noir)
    assert all(e["engine"] == "sdxl-checkpoint" for e in cartoon)
    assert all(e["prompt"].startswith("Black-and-white 1940s film noir") for e in noir)
    assert all("monochrome with no color" in e["prompt"] for e in noir)
    assert all(not re.search(r"\\bframe\\b", e["prompt"]) for e in noir)
    assert all("western comics" not in e["prompt"] and "masterpiece" not in e["prompt"] for e in noir)
    assert all("color" in e["negative_prompt"] and "nudity" in e["negative_prompt"] for e in noir)
    assert all(e["status"] in ("pending", "done") for e in entries)
    assert all(e.get("priority") == 10 for e in entries)
    assert all("mid-century safety-manual illustration" not in e["prompt"].lower() for e in entries)
    assert all(e["source_url"] == "https://media.acrocatranch.com/" + e["image_path"][len("public/"):] for e in entries)
    assert all(not e["image_path"].startswith("public/images/shifting-desks/cards/") for e in entries)
    counts = Counter(e.get("checkpoint_family") or e["style_family"] for e in entries)
    assert all(counts[style] <= 194 for style in ("corporate-noir", "western-cartoon"))


def test_western_cartoon_is_arhemy_not_rejected_furrytoonmix():
    from scripts.dream_sdxl_checkpoint_art import CHECKPOINT_LANES
    assert CHECKPOINT_LANES["western-cartoon"]["checkpoint"] == (
        "Illustrious/arthemyWesternArt_v30.safetensors"
    )
    assert CHECKPOINT_LANES["corporate-noir"]["checkpoint"] == (
        "Illustrious/arthemyWesternArt_v30.safetensors"
    )
    assert "western animated feature" in CHECKPOINT_LANES["western-cartoon"]["style"]


def test_shifting_desks_220_job_batch_is_submitted_before_serial_render_wait():
    workflow = (ROOT / ".github/workflows/auto-art-generate.yml").read_text()
    submit = workflow.index("name: Bulk-submit Shifting Desks style ArtJobs")
    slow = workflow.index("name: Submit + wait + verify art requests")
    assert submit < slow
    block = workflow[submit:slow]
    assert "--live --submit-only" in block
    assert "--id-prefix shifting-desks-style-v2-" in block
    assert "continue-on-error: true" in block
    assert "KR_API_TOKEN:" in block
    assert "steps.boxhealth.outputs.up == 'true'" in block
    assert "steps.krhealth.outputs.up == 'true'" in block
    # One concurrency group serializes submissions, so the next run sees
    # last_art_job_id instead of POSTing copies.
    assert "group: auto-art-generate" in workflow
    assert "cancel-in-progress: false" in workflow
