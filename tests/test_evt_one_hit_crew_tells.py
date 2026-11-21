"""Validate unique private art requests for three playable one-hit enemy tiers."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/every-villain-tactics/art/ONE-HIT-CREW-TELEGRAPHS-2026-11-20.yaml"

EXPECTED = {
    'accident-earth': [
        'burrow-warning',
        'burrow-emergence',
        'burrow-blocked',
        'foreman-closeup'
    ],
    'alien-discipline': [
        'phase-warning',
        'phase-arrival',
        'phase-interrupted',
        'teakettle-closeup'
    ],
    'accident-birthright': [
        'seal-warning',
        'windup-swarm',
        'seal-broken',
        'sir-cap-closeup'
    ]
}


def test_t018_private_one_hit_telegraph_art_contract():
    data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert data["project_slug"] == "every-villain-tactics"
    assert data["auto_submit"] is True
    assert data["is_public"] is False
    assert data["is_mature"] is False
    assert data["lanes"] == [
        {
            "key": "krea2",
            "label": "Krea 2 original tactical animation plates",
            "engine": "krea2",
            "prompt": "prose",
            "suffix": data["lanes"][0]["suffix"],
        }
    ]
    items = data["subjects"]
    assert len(items) == 12
    assert len({s["key"] for s in items}) == 12
    assert len({s["asset"] for s in items}) == 12
    assert len({s["seed"] for s in items}) == 12
    for signature, variants in EXPECTED.items():
        for variant in variants:
            matches = [
                row for row in items
                if row["asset"] == f"every-villain-tactics/henchmen/{signature}/tells/{variant}"
            ]
            assert len(matches) == 1, (signature, variant)
            item = matches[0]
            assert item["lane"] == "krea2"
            if "closeup" in variant:
                assert item["size"] == "768x1024"
            elif "warning" in variant:
                assert item["size"] == "768x768"
            else:
                assert item["size"] == "1344x768"
            assert item["seed"] >= 995200
            prose = item["prompt_prose"]
            assert 120 <= len(prose) <= 900
            assert not re.search(r"\b(?:no|not|without|frame|caption|title|text)\b", prose, re.I)
            # Drafts carry no receipts; after the auto-submit checkpoint the only
            # allowed receipt is one real ArtJob id (plus status) for this lane.
            if "jobs" in item or "art" in item:
                assert set(item.get("jobs") or {}) == {item["lane"]}
                job_id = item["jobs"][item["lane"]]
                assert isinstance(job_id, int) and job_id > 0
                assert set(item.get("art") or {}) <= {item["lane"]}
                for state in (item.get("art") or {}).values():
                    assert state.get("status")
