"""Dead Air's morning digest includes real private finals, never queued films."""
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_digest import dead_air_private_film_payload
from build_digest_email_v2_impl import dead_air_section


def test_digest_includes_private_final_only_with_probe(tmp_path):
    date = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    episodes = tmp_path / "episodes"
    episodes.mkdir()
    (episodes / f"{date}-clip.yaml").write_text("title: A weird fake ad\n", encoding="utf-8")
    path = tmp_path / "state.json"
    data = {"episodes": {"clip": {
        "status": "rendering", "music_video_id": 18, "final_art_image_id": None,
        "episode": "projects/dead-air/episodes/clip.yaml",
        "updated_pt": f"{date}T05:00:00-08:00",
    }}}
    path.write_text(json.dumps(data), encoding="utf-8")
    film = dead_air_private_film_payload(str(path), str(episodes))
    assert film["status"] == "rendering"
    assert not film.get("url")
    assert "Not finished" in dead_air_section(film)

    data["episodes"]["clip"].update({
        "status": "completed", "final_art_image_id": 76, "completed_pt": date,
        "quality_probe": {"duration_seconds": 15.01, "width": 1280, "height": 720},
        "gpu_animated_shots": 0,
    })
    path.write_text(json.dumps(data), encoding="utf-8")
    film = dead_air_private_film_payload(str(path), str(episodes))
    assert film["status"] == "ready"
    assert film["title"] == "A weird fake ad"
    assert film["url"].endswith("studio=music&video=18")
    html = dead_air_section(film)
    assert "Watch verified commercial" in html
    assert film["fresh_today"] is True
    assert "private premiere" in html


def test_unprobed_or_invalid_final_never_links(tmp_path):
    date = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    path = tmp_path / "state.json"
    path.write_text(json.dumps({"episodes": {"notdone": {
        "status": "completed", "completed_pt": date,
        "music_video_id": 18, "final_art_image_id": 47,
        "quality_probe": {"duration_seconds": 8},
    }}}), encoding="utf-8")
    film = dead_air_private_film_payload(str(path), str(tmp_path))
    assert film["status"] != "ready"
    assert not film.get("url")


def test_yesterdays_verified_film_is_not_a_new_premiere(tmp_path):
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    yesterday = (datetime.now(ZoneInfo("America/Los_Angeles")).date()
                 - timedelta(days=1)).isoformat()
    episodes = tmp_path / "episodes"
    episodes.mkdir()
    (episodes / f"{yesterday}-clip.yaml").write_text(
        "title: Yesterday's commercial\n", encoding="utf-8"
    )
    ledger = tmp_path / "state.json"
    ledger.write_text(json.dumps({"episodes": {"clip": {
        "status": "completed", "completed_pt": yesterday,
        "music_video_id": 18, "final_art_image_id": 100,
        "quality_probe": {"duration_seconds": 15.0},
    }}}), encoding="utf-8")
    film = dead_air_private_film_payload(str(ledger), str(episodes))
    assert film["fresh_today"] is False
    assert film["final_art_image_id"] == 100
    html = dead_air_section(film)
    assert "No film was completed today" in html
    assert "private premiere" not in html
