"""Contract for the first private, canonical Prom/Tactics Unstable production batch."""

from pathlib import Path

import yaml

from scripts.enqueue_art_requests import build_request, iter_cells


LEDGER = (
    Path(__file__).resolve().parents[1]
    / "projects/comet-city-academy/art/UNSTABLE-PRODUCTION-FAMILY-ROUND-1.yaml"
)
CHECKPOINT = "SDXL/sdxlUnstableDiffusers_nihilmania.safetensors"
EXPECTED_VARIANTS = {
    "accident-earth": {
        "poster-villain",
        "model-hero-2x1",
        "model-villain-2x1",
        "portrait-resolve",
    },
    "accident-fire": {
        "poster-hero",
        "model-hero-2x1",
        "model-villain-2x1",
        "portrait-doubt",
    },
    "tech-genius": {
        "poster-hero",
        "poster-villain",
        "model-hero-2x1",
        "model-villain-2x1",
        "story-transformation",
        "portrait-heel",
    },
}


def test_private_canonical_house_checkpoint_and_no_duplicate_benchmarks():
    data = yaml.safe_load(LEDGER.read_text())
    assert data["auto_submit"] is True
    assert data["is_public"] is False
    assert data["cast_loras"] is False
    assert data["project_slug"] == "comet-city-academy"
    assert data["priority"] == 900
    assert data["benchmark_reference_jobs"] == {
        "cornerstone_hero_poster": 50509,
        "backdraft_villain_poster": 50515,
        "dr_frog_science_story": 50530,
    }
    lane, = data["lanes"]
    assert lane["key"] == "unstable-production"
    assert lane["engine"] == "comfy"
    assert lane["checkpoint"] == CHECKPOINT
    assert lane["prompt"] == "prose"
    assert (lane["steps"], lane["cfg"], lane["sampler"]) == (28, 7, "dpmpp_2m")
    assert len(data["subjects"]) == 14
    assert len({row["seed"] for row in data["subjects"]}) == 14
    assert len({row["asset"] for row in data["subjects"]}) == 14

    actual = {signature: set() for signature in EXPECTED_VARIANTS}
    for subject, render_lane in iter_cells(data):
        signature = subject["entity"]
        assert signature in EXPECTED_VARIANTS
        expected_prefix = f"comet-city-academy/identities/{signature}/"
        assert subject["asset"].startswith(expected_prefix)
        actual[signature].add(subject["asset"][len(expected_prefix):])
        jobs = subject.get("jobs") or {}
        assert set(jobs).issubset({"unstable-production"})
        assert all(
            isinstance(job_id, int)
            and job_id > 0
            and job_id not in data["benchmark_reference_jobs"].values()
            for job_id in jobs.values()
        )
        assert subject["prompt_prose"]
        assert subject["negative"]
        request = build_request(data, render_lane, subject)
        assert request["engine"] == "comfy"
        assert request["checkpoint"] == CHECKPOINT
        assert request["steps"] == 28
        assert request["cfg"] == 7
        assert request["sampler"] == "dpmpp_2m"
        assert request["seed"] == subject["seed"]
        assert request["priority"] == 900
        assert request["isPublic"] is False
        assert request["width"] > 0 and request["height"] > 0
        if "2x1" in subject["asset"]:
            assert request["width"] == 2 * request["height"]
    assert actual == EXPECTED_VARIANTS
    assert not any("firewall" in subject["asset"] for subject in data["subjects"])
