import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import retry_dream_identity_collision as retry  # noqa: E402


def test_recovery_matcher_prefers_normal_exact_adoption(monkeypatch):
    exact = {"id": 99, "title": "Fault Line Follies"}
    called = []

    def original(endpoint, identity):
        called.append((endpoint, identity))
        return exact

    matcher = retry.make_recovery_matcher(original, set())
    assert matcher("/api/dreams", {"dreamType": "PITCH"}) is exact
    assert len(called) == 1


def test_recovery_matcher_adopts_only_one_unprotected_stale_pitch(monkeypatch):
    calls = []

    def original(endpoint, identity):
        return None

    def http_json(method, url, body=None, timeout=60):
        calls.append((method, url, body))
        if method == "GET":
            return 200, {
                "data": {
                    "rows": [
                        {
                            "id": 777,
                            "title": "The Deep Shift",
                            "slug": "kelp-ink-transfer",
                            "dreamType": "PITCH",
                            "designer": "dream-cycle",
                            "description": "old prose",
                        }
                    ]
                }
            }
        assert method == "PATCH"
        assert url.endswith("/api/dreams/777")
        assert body == {
            "title": "The Deep Shift",
            "description": "current prose",
            "flavorText": "current vibe",
            "artPrompt": "current prompt",
        }
        return 200, {"success": True}

    monkeypatch.setattr(retry.records, "http_json", http_json)
    matcher = retry.make_recovery_matcher(original, set())
    row = matcher(
        "/api/dreams",
        {
            "title": "The Deep Shift",
            "slug": "kelp-ink-transfer",
            "dreamType": "PITCH",
            "designer": "dream-cycle",
            "description": "current prose",
            "flavorText": "current vibe",
            "artPrompt": "current prompt",
        },
    )

    assert row["id"] == 777
    assert row["description"] == "current prose"
    assert [call[0] for call in calls] == ["GET", "PATCH"]


def test_recovery_matcher_never_adopts_protected_pitch(monkeypatch):
    def original(endpoint, identity):
        return None

    def http_json(method, url, body=None, timeout=60):
        assert method == "GET"
        return 200, {
            "data": {
                "rows": [
                    {
                        "id": 5668,
                        "title": "Boundary Day",
                        "slug": "canopy-permit-office",
                        "dreamType": "PITCH",
                        "designer": "dream-cycle",
                    }
                ]
            }
        }

    monkeypatch.setattr(retry.records, "http_json", http_json)
    matcher = retry.make_recovery_matcher(original, {("/api/dreams", 5668)})
    assert matcher(
        "/api/dreams",
        {
            "title": "Boundary Day",
            "slug": "canopy-permit-office",
            "dreamType": "PITCH",
            "designer": "dream-cycle",
            "description": "do not overwrite",
        },
    ) is None


def test_recovery_matcher_does_not_relax_other_models(monkeypatch):
    def original(endpoint, identity):
        return None

    def forbidden(*args, **kwargs):
        raise AssertionError("network fallback must not run for non-PITCH records")

    monkeypatch.setattr(retry.records, "http_json", forbidden)
    matcher = retry.make_recovery_matcher(original, set())
    assert matcher("/api/rewards", {"name": "Coldwater Bell"}) is None
    assert matcher("/api/dreams", {"dreamType": "LOCATION", "title": "Kelphold Rig"}) is None
