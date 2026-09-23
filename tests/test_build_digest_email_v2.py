import importlib.util
import sys
import types
from pathlib import Path


def load_module():
    stub = types.ModuleType("build_digest_email")
    stub._button = lambda href, text, color="#000": f'<a href="{href}" style="background:{color}">{text}</a>'
    stub.proposal_section = None
    stub.container_log_review_section = lambda digest: (
        "<p>Detailed error review</p>"
        if isinstance((digest.get("container_logs") or {}).get("review"), dict)
        else ""
    )
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


def test_legacy_just_built_mode_stays_text_only():
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


def test_current_art_rich_section_shows_latest_images_and_queue_placeholders():
    module = load_module()
    html = module.proposal_section(
        "ignored",
        {
            "title": "Current",
            "idea": "Idea",
            "display_mode": "current-art-rich",
            "assets": assets(submitted=True),
        },
    )
    assert "Previous pitch, now generated" in html
    assert "Previous completed output" not in html
    assert "5/6 latest asset images ready" in html
    assert "height:190px" in html
    assert "Art queued" in html


def test_payload_leads_with_just_built_then_health_then_tomorrow_pitch():
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
            "display_mode": "current-art-rich",
            "assets": assets(submitted=True),
        },
        "next_dream_proposal": {
            "slug": "next",
            "title": "Tomorrow Is Weird",
            "idea": "Steering becomes a visible promise.",
            "proposal_date": "2026-09-12",
            "edit_link": "https://example.com/pitch",
            "assets": assets(),
        },
        "animation_release": {
            "state": "fresh",
            "id": "candlelit-reliquary",
            "title": "Candlelit Reliquary",
            "released_label": "Sep 21, 2026 at 4:12 PM Pacific",
            "try_url": "https://kindrobots.org/build/animation-manager?effect=candlelit-reliquary&preview=1",
        },
        "render_engine": {"state": "down", "reason": "ComfyUI is unreachable."},
        "container_logs": {
            "state": "findings",
            "new": 2,
            "spiking": 1,
            "reason": "Three signatures changed.",
            "review": {"headline": "Review exists"},
        },
    }
    payload = module.build_payload(digest)
    html = payload["htmlContent"]

    assert html.index("Current Just Built") < html.index("New Animation Manager release")
    assert html.index("New Animation Manager release") < html.index("Render engine DOWN")
    assert html.index("Render engine DOWN") < html.index("Detailed error review")
    assert html.index("Detailed error review") < html.index("Tomorrow’s pitch")
    assert html.index("Tomorrow’s pitch") < html.index("Tomorrow Is Weird")
    assert "Previous With Art" not in html
    assert "Steering becomes a visible promise." in html
    assert "5/6 latest asset images ready" in html
    assert "height:90px" not in html


def test_tomorrow_pitch_is_compact_and_does_not_pretend_assets_are_built():
    module = load_module()
    html = module.next_pitch_section(
        {
            "title": "Tomorrow",
            "idea": "A compact pitch.",
            "proposal_date": "2026-09-13",
            "edit_link": "https://example.com/tomorrow",
            "assets": assets(),
        }
    )
    assert "Tomorrow’s pitch" in html
    assert "Tomorrow" in html
    assert "A compact pitch." in html
    assert "Read tomorrow’s pitch" in html
    assert "Seed Facets" not in html
    assert "ArtJobs" not in html
    assert "height:190px" not in html


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


def test_animation_release_section_links_directly_to_preview():
    module = load_module()
    html = module.animation_release_section(
        {
            "animation_release": {
                "state": "fresh",
                "id": "candlelit-reliquary",
                "title": "Candlelit Reliquary",
                "released_label": "Sep 21, 2026 at 4:12 PM Pacific",
                "try_url": "https://kindrobots.org/build/animation-manager?effect=candlelit-reliquary&preview=1",
            }
        }
    )

    assert "New Animation Manager release" in html
    assert "Candlelit Reliquary" in html
    assert "Try Candlelit Reliquary" in html
    assert "effect=candlelit-reliquary&amp;preview=1" not in html
    assert "effect=candlelit-reliquary&preview=1" in html


def test_animation_release_section_calls_out_stale_daily_cadence():
    module = load_module()
    html = module.animation_release_section(
        {
            "animation_release": {
                "state": "stale",
                "id": "geode-bloom",
                "title": "Geode Bloom",
                "released_label": "Sep 5, 2026 at 12:55 AM Pacific",
                "try_url": "https://kindrobots.org/build/animation-manager?effect=geode-bloom&preview=1",
            }
        }
    )

    assert "Animation Manager cadence" in html
    assert "No new screensaver shipped in the last 24 hours" in html
    assert "Try Geode Bloom" in html
