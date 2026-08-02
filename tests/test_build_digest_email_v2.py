import importlib.util
import sys
import types
from pathlib import Path


def load_module():
    stub = types.ModuleType("build_digest_email")
    stub._button = lambda href, text, color="#000": f'<a href="{href}" style="background:{color}">{text}</a>'
    stub.proposal_section = None
    stub.build_payload = lambda digest: {
        "subject": "Digest",
        "htmlContent": stub.proposal_section("🌙 Tomorrow's dream", digest.get("tomorrow_proposal"), cta=True),
    }
    sys.modules["build_digest_email"] = stub
    path = Path(__file__).parents[1] / "scripts" / "build_digest_email_v2.py"
    spec = importlib.util.spec_from_file_location("email_v2", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def assets():
    return [
        {"key": key, "label": key, "title": key.title(), "summary": "summary", "facets": ["GENRE: One"],
         "image_url": f"https://example.com/{key}.webp" if key != "scenario" else "", "art_status": "ready" if key != "scenario" else "queued"}
        for key in ("vibe", "location", "character", "reward_item", "reward_skill", "scenario")
    ]


def test_email_renders_all_six_assets_with_large_images_and_pending_card():
    module = load_module()
    html = module.proposal_section("Tomorrow", {"title": "Bundle", "idea": "Idea", "assets": assets()})
    assert html.count("Seed Facets") == 6
    assert "height:190px" in html
    assert "Art queued" in html
    for key in ("Vibe", "Location", "Character", "Reward_Item", "Reward_Skill", "Scenario"):
        assert key in html


def test_payload_uses_v2_section_without_tiny_90px_strip():
    module = load_module()
    payload = module.build_payload({"tomorrow_proposal": {"title": "Bundle", "idea": "Idea", "assets": assets()}})
    assert "height:90px" not in payload["htmlContent"]
    assert payload["htmlContent"].count("Seed Facets") == 6


def test_payload_renders_additional_recent_bundles_without_duplication():
    module = load_module()
    digest = {
        "tomorrow_proposal": {"slug": "today", "title": "Today", "idea": "Idea", "assets": assets()},
        "yesterday_output": {"slug": "main-yesterday", "title": "Main", "idea": "Idea", "assets": assets()},
        "recent_dream_outputs": [
            {"slug": "main-yesterday", "title": "Main", "idea": "Idea", "assets": assets()},
            {"slug": "another-yesterday", "title": "Another Build", "idea": "Idea", "assets": assets()},
        ],
    }
    payload = module.build_payload(digest)
    assert "Earlier completed bundles" in payload["htmlContent"]
    assert "Another Build" in payload["htmlContent"]


def test_payload_labels_previous_output_without_calendar_claim():
    module = load_module()
    payload = module.build_payload({
        "projects": [],
        "date": "2026-08-02",
        "pitches_awaiting_vote": [],
        "all_needs_attention": [],
        "yesterday_output": {
            "slug": "previous",
            "title": "Previous",
            "idea": "Built earlier.",
            "assets": assets(),
        },
    })
    assert "Previous completed output" in payload["htmlContent"]
    assert "Yesterday's output" not in payload["htmlContent"]
