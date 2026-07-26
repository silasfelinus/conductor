"""Tests for scripts/rename_bot_slugs_to_avatar.py (kind-robots/t-011
follow-up: make slug the single source of truth instead of teaching
reconcile_expressions.py an ever-growing fallback tier to bridge slug vs.
avatarImage).
"""
import json

import scripts.rename_bot_slugs_to_avatar as r


def test_build_rename_plan_flags_mismatches_only(monkeypatch):
    def fake_api(path, payload=None, method=None, timeout=30):
        assert path == "/api/bots?page=1&pageSize=100"
        return {"data": [
            {"id": 42, "slug": "pip-the-lampkeeper",
             "avatarImage": "/images/bots/brass-lampkeeper.webp"},
            {"id": 9, "slug": "barkeep-vox",
             "avatarImage": "/images/bots/barkeep-vox.webp"},  # already matches
            {"id": 3, "slug": "no-avatar-bot", "avatarImage": ""},  # no avatarImage, skip
        ]}

    monkeypatch.setattr(r, "api", fake_api)
    plan = r.build_rename_plan("bot")

    assert plan == [(42, "pip-the-lampkeeper", "brass-lampkeeper")]


def test_build_rename_plan_paginates_defensively(monkeypatch):
    calls = []

    def fake_api(path, payload=None, method=None, timeout=30):
        calls.append(path)
        if path == "/api/bots?page=1&pageSize=100":
            return {"data": [
                {"id": i, "slug": f"slug-{i}", "avatarImage": f"/images/bots/avatar-{i}.webp"}
                for i in range(100)
            ]}
        if path == "/api/bots?page=2&pageSize=100":
            return {"data": []}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(r, "api", fake_api)
    plan = r.build_rename_plan("bot")

    assert len(plan) == 100
    assert calls == ["/api/bots?page=1&pageSize=100", "/api/bots?page=2&pageSize=100"]


def test_main_dry_run_prints_plan_without_calling_patch(monkeypatch, capsys):
    def fake_api(path, payload=None, method=None, timeout=30):
        if method == "PATCH":
            raise AssertionError("dry-run must never PATCH")
        if path == "/api/bots?page=1&pageSize=100":
            return {"data": [{"id": 42, "slug": "pip-the-lampkeeper",
                               "avatarImage": "/images/bots/brass-lampkeeper.webp"}]}
        if path == "/api/characters?page=1&pageSize=100":
            return {"data": []}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(r, "api", fake_api)
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_avatar.py"])

    code = r.main()

    out = capsys.readouterr().out
    assert "pip-the-lampkeeper -> brass-lampkeeper" in out
    summary = json.loads(out.strip().splitlines()[-1])
    assert summary == {"mode": "dry-run", "planned": 1, "applied": 0, "errors": 0}
    assert code == 0


def test_main_apply_without_token_returns_1_before_any_work(monkeypatch, capsys):
    def exploding_api(path, payload=None, method=None, timeout=30):
        raise AssertionError("api() must not be called without a token")

    monkeypatch.setattr(r, "api", exploding_api)
    monkeypatch.setattr(r, "KR_API_TOKEN", "")
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_avatar.py", "--apply"])

    code = r.main()

    assert code == 1
    assert "--apply requires KR_API_TOKEN" in capsys.readouterr().err


def test_main_apply_patches_each_mismatched_owner(monkeypatch, capsys):
    patched = []

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/bots?page=1&pageSize=100":
            return {"data": [{"id": 42, "slug": "pip-the-lampkeeper",
                               "avatarImage": "/images/bots/brass-lampkeeper.webp"}]}
        if path == "/api/characters?page=1&pageSize=100":
            return {"data": []}
        if path == "/api/bots/42" and method == "PATCH":
            patched.append(payload)
            return {"success": True, "data": {"id": 42, "slug": "brass-lampkeeper"}}
        raise AssertionError(f"unexpected call: {path} {method}")

    monkeypatch.setattr(r, "api", fake_api)
    monkeypatch.setattr(r, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_avatar.py", "--apply"])

    code = r.main()

    assert patched == [{"slug": "brass-lampkeeper"}]
    summary = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert summary == {"mode": "applied", "planned": 1, "applied": 1, "errors": 0}
    assert code == 0


def test_main_type_filter_skips_other_owner_type(monkeypatch):
    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/bots?page=1&pageSize=100":
            return {"data": [{"id": 42, "slug": "pip-the-lampkeeper",
                               "avatarImage": "/images/bots/brass-lampkeeper.webp"}]}
        raise AssertionError(f"unexpected call for characters: {path}")

    monkeypatch.setattr(r, "api", fake_api)
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_avatar.py", "--type", "bot"])

    code = r.main()
    assert code == 0
