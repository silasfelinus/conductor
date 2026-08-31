import sys
from pathlib import Path

import pytest

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


def test_recorded_prior_attempt_row_is_adopted_by_direct_id(monkeypatch):
    def original(endpoint, identity):
        return None

    def http_json(method, url, body=None, timeout=60):
        assert method == "GET"
        assert url.endswith("/api/characters/3314")
        return 200, {"success": True, "data": {"character": {"id": 3314, "name": "Vex Thistlemaw"}}}

    monkeypatch.setattr(retry.records, "http_json", http_json)
    matcher = retry.make_recovery_matcher(
        original,
        set(),
        [{"endpoint": "/api/characters", "id": 3314, "label": "Vex Thistlemaw", "source_run": 33343607764}],
    )
    row = matcher("/api/characters", {"name": "Vex Thistlemaw", "designer": "dream-cycle"})
    assert row == {"id": 3314, "name": "Vex Thistlemaw"}


def test_recorded_prior_attempt_row_must_still_have_expected_label(monkeypatch):
    def original(endpoint, identity):
        return None

    monkeypatch.setattr(
        retry.records,
        "http_json",
        lambda *args, **kwargs: (200, {"data": {"character": {"id": 3314, "name": "Someone Else"}}}),
    )
    matcher = retry.make_recovery_matcher(
        original,
        set(),
        [{"endpoint": "/api/characters", "id": 3314, "label": "Vex Thistlemaw", "source_run": 33343607764}],
    )
    with pytest.raises(RuntimeError, match="recorded retry row drift"):
        matcher("/api/characters", {"name": "Vex Thistlemaw"})


def test_retry_adoptions_require_source_run_and_are_unique():
    with pytest.raises(ValueError, match="retry_after_run"):
        retry._retry_adoptions(
            {"retry_adoptions": [{"endpoint": "/api/characters", "id": 3314, "name": "Vex Thistlemaw"}]}
        )
    with pytest.raises(ValueError, match="duplicate retry adoption"):
        retry._retry_adoptions(
            {
                "retry_after_run": 33343607764,
                "retry_adoptions": [
                    {"endpoint": "/api/characters", "id": 3314, "name": "Vex Thistlemaw"},
                    {"endpoint": "/api/characters", "id": 3314, "name": "Vex Thistlemaw"},
                ],
            }
        )


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


def test_recovery_matcher_does_not_relax_other_models_without_recorded_evidence(monkeypatch):
    def original(endpoint, identity):
        return None

    def forbidden(*args, **kwargs):
        raise AssertionError("network fallback must not run for non-PITCH records")

    monkeypatch.setattr(retry.records, "http_json", forbidden)
    matcher = retry.make_recovery_matcher(original, set())
    assert matcher("/api/rewards", {"name": "Coldwater Bell"}) is None
    assert matcher("/api/dreams", {"dreamType": "LOCATION", "title": "Kelphold Rig"}) is None
