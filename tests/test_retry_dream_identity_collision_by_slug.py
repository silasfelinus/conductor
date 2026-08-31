import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import retry_dream_identity_collision_by_slug as slug_retry  # noqa: E402


def test_slug_fallback_converts_old_non_pitch_owner(monkeypatch):
    calls = []

    def base(endpoint, identity):
        return None

    def http_json(method, url, body=None, timeout=60):
        calls.append((method, url, body))
        if method == "GET":
            assert "dreamType=" not in url
            assert "search=" not in url
            return 200, {
                "data": [
                    {
                        "id": 555,
                        "title": "The Kelp-Ink Transfer",
                        "slug": "kelp-ink-transfer",
                        "dreamType": "LOCATION",
                        "designer": "legacy-daily-dream",
                        "description": "historical prose",
                    }
                ]
            }
        assert method == "PATCH"
        assert url.endswith("/api/dreams/555")
        assert body == {
            "title": "The Deep Shift",
            "dreamType": "PITCH",
            "designer": "dream-cycle",
            "description": "current prose",
        }
        return 200, {"success": True}

    monkeypatch.setattr(slug_retry.records, "http_json", http_json)
    matcher = slug_retry.make_slug_recovery_matcher(base, set())
    row = matcher(
        "/api/dreams",
        {
            "title": "The Deep Shift",
            "slug": "kelp-ink-transfer",
            "dreamType": "PITCH",
            "designer": "dream-cycle",
            "description": "current prose",
        },
    )
    assert row["id"] == 555
    assert row["title"] == "The Deep Shift"
    assert row["dreamType"] == "PITCH"
    assert [call[0] for call in calls] == ["GET", "PATCH"]


def test_slug_fallback_never_adopts_protected_owner(monkeypatch):
    def base(endpoint, identity):
        return None

    monkeypatch.setattr(
        slug_retry.records,
        "http_json",
        lambda *args, **kwargs: (
            200,
            {
                "data": [
                    {
                        "id": 5670,
                        "title": "The Silk Bargain",
                        "slug": "kelp-ink-transfer",
                        "dreamType": "LOCATION",
                    }
                ]
            },
        ),
    )
    matcher = slug_retry.make_slug_recovery_matcher(base, {("/api/dreams", 5670)})
    assert matcher(
        "/api/dreams",
        {"title": "The Deep Shift", "slug": "kelp-ink-transfer", "dreamType": "PITCH", "designer": "dream-cycle"},
    ) is None


def test_slug_fallback_rejects_ambiguous_rows(monkeypatch):
    def base(endpoint, identity):
        return None

    rows = [
        {"id": 600, "title": "Old A", "slug": "kelp-ink-transfer", "dreamType": "LOCATION"},
        {"id": 601, "title": "Old B", "slug": "kelp-ink-transfer", "dreamType": "PITCH"},
    ]
    monkeypatch.setattr(slug_retry.records, "http_json", lambda *args, **kwargs: (200, {"data": rows}))
    matcher = slug_retry.make_slug_recovery_matcher(base, set())
    with pytest.raises(RuntimeError, match="ambiguous"):
        matcher(
            "/api/dreams",
            {"title": "The Deep Shift", "slug": "kelp-ink-transfer", "dreamType": "PITCH", "designer": "dream-cycle"},
        )


def test_slug_fallback_does_not_relax_non_pitch_create_conflicts(monkeypatch):
    def base(endpoint, identity):
        return None

    monkeypatch.setattr(
        slug_retry.records,
        "http_json",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("network should not run")),
    )
    matcher = slug_retry.make_slug_recovery_matcher(base, set())
    assert matcher("/api/characters", {"name": "Imogen Halvard"}) is None
    assert matcher("/api/dreams", {"dreamType": "LOCATION", "slug": "kelphold-rig"}) is None
