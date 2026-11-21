"""Acceptance contract for the Oct 29 private, source-backed Prom art queue."""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/comet-city-academy/art/OCT-29-CAST-KREA2-ROUND-1.yaml"
SOURCE = ROOT / "projects/comet-city-academy/content/DAILY-CHARACTER-PITCHES-2026-10-29.json"


def test_oct29_private_production_contract():
    data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    pitch = json.loads(SOURCE.read_text(encoding="utf-8"))
    subjects = data["subjects"]
    assert data["project_slug"] == "comet-city-academy"
    assert data["auto_submit"] is True
    assert data["is_public"] is False
    assert data["is_mature"] is False
    assert data["lanes"][0]["engine"] == "krea2"
    assert len(pitch["characters"]) == 8
    assert len(subjects) == 24
    assert len({row["key"] for row in subjects}) == 24
    assert len({row["asset"] for row in subjects}) == 24
    assert len({row["seed"] for row in subjects}) == 24
    slugs = [
        "madame-afterparty", "the-asterisk", "coach-event-horizon",
        "choir-of-one", "pledgebreaker", "miss-reflection",
        "standing-ovation", "lady-hemline",
    ]
    assert len(slugs) == len(set(slugs)) == 8
    for slug in slugs:
        for variant in ("portrait", "splash", "encounter"):
            key = f"pod-oct29-{slug}-{variant}"
            matching = [row for row in subjects if row["key"] == key]
            assert len(matching) == 1
            item = matching[0]
            assert item["asset"] == f"comet-city-academy/cast/{slug}/{variant}"
            assert item["lane"] == "krea2"
            assert item["size"] == ("768x1024" if variant == "portrait" else "1344x768")
            assert 120 <= len(item["prompt_prose"]) <= 900
            assert not re.search(r"\b(?:no|not|without|frame|chapter)\b", item["prompt_prose"], re.I)
            # Drafts carry no receipts; after the auto-submit checkpoint the only
            # allowed receipt is one real ArtJob id (plus status) for this lane.
            if "jobs" in item or "art" in item:
                assert set(item.get("jobs") or {}) == {item["lane"]}, "receipt lane matches request"
                job_id = item["jobs"][item["lane"]]
                assert isinstance(job_id, int) and job_id > 0, "receipt is a real accepted ArtJob id"
                assert set(item.get("art") or {}) <= {item["lane"]}
                for state in (item.get("art") or {}).values():
                    assert state.get("status"), "ArtImage receipt records a status"
    for cast_member in pitch["characters"]:
        assert any(row["title"].startswith(cast_member["name"]) for row in subjects)
