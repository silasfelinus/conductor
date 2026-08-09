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
        "htmlContent": (
            stub.proposal_section("🌙 Tomorrow's dream", digest.get("tomorrow_proposal"), cta=True)
            + stub.proposal_section("🖼️ Previous completed output", digest.get("yesterday_output"))
        ),
    }
    sys.modules["build_digest_email"] = stub
    path = Path(__file__).parents[1] / "scripts" / "build_digest_email_v2.py"
    spec = importlib.util.spec_from_file_location("email_v2", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def assets(*, submitted: bool = False):
    rows = []
    for index, key in enumerate(
        ("vibe", "location", "character", "reward_item", "reward_skill", "scenario"),
        start=1,
    ):
        row = {
            "key": key,
            "label": key,
            "title": key.title(),
            "summary": "summary",
            "facets": ["GENRE: One"],
            "image_url": f"https://example.com/{key}.webp" if key != "scenario" else "",
            "art_status": "ready" if key != "scenario" else "queued",
            "request_id": f"dream-{key}",
        }
        if submitted:
            row["art_job_id"] = 8100 + index
        rows.append(row)
    return rows


def test_art_rich_section_renders_images_and_pending_art_slot():
    module = load_module()
    html = module.proposal_section(
        "ignored",
        {
            "title": "Previous",
            "idea": "Idea",
            "display_mode": "art-rich",
            "assets": assets(),
        },
    )
    assert "Previous completed output" in html
    assert html.count("Seed Facets") == 6
    assert "height:190px" in html
    assert "Art queued" in html


def test_just_built_section_has_no_image_boxes_at_all():
    module = load_module()
    html = module.proposal_section(
        "ignored",
        {
            "title": "Just Built",
            "idea": "Idea",
            "display_mode": "just-built",
            "assets": assets(submitted=True),
        },
    )
    assert "Just built this cycle" in html
    assert html.count("Seed Facets") == 6
    assert "height:190px" not in html
    assert "Art queued" not in html
    assert "6/6 ArtJobs submitted" in html
    assert "No image space is reserved here" in html


def test_payload_orders_previous_art_before_just_built_and_hides_next_proposal():
    module = load_module()
    digest = {
        "previous_dream_output": {
            "slug": "previous",
            "title": "Previous With Art",
            "idea": "Older output.",
            "display_mode": "art-rich",
            "assets": assets(),
        },
        "current_dream_output": {
            "slug": "current",
            "title": "Current Just Built",
            "idea": "Fresh output.",
            "display_mode": "just-built",
            "assets": assets(submitted=True),
        },
        "next_dream_proposal": {
            "slug": "next",
            "title": "Do Not Show Me",
            "idea": "Steering only.",
            "assets": assets(),
        },
    }
    payload = module.build_payload(digest)
    html = payload["htmlContent"]
    assert html.index("Previous With Art") < html.index("Current Just Built")
    assert "Do Not Show Me" not in html
    assert "height:90px" not in html


def test_payload_does_not_render_older_recent_history():
    module = load_module()
    digest = {
        "previous_dream_output": {
            "slug": "previous",
            "title": "Previous",
            "idea": "Idea",
            "display_mode": "art-rich",
            "assets": assets(),
        },
        "current_dream_output": {
            "slug": "current",
            "title": "Current",
            "idea": "Idea",
            "display_mode": "just-built",
            "assets": assets(submitted=True),
        },
        "recent_dream_outputs": [
            {"slug": "old", "title": "Too Old", "idea": "Old", "assets": assets()}
        ],
    }
    payload = module.build_payload(digest)
    assert "Too Old" not in payload["htmlContent"]
    assert "Earlier completed bundles" not in payload["htmlContent"]
