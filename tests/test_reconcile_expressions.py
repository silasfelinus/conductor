"""Tests for scripts/reconcile_expressions.py (conductor/t-029).

Promotes the throwaway stubbed-API harness used to verify PR #360's
narrator-first/bulk-fallback owner resolution into a real, committed
pytest suite. All API calls go through a fake `api()` — no network, no
real kind_robots checkout.
"""
import io
import json
import urllib.error
from pathlib import Path

import scripts.reconcile_expressions as rex


def http_404(path):
    return urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))


def make_expr_tree(tmp_path: Path, owner_type: str, slug: str, keys) -> Path:
    """Fake kind_robots checkout with one owner folder containing a
    lowest-take still per key (e.g. {"joyful": "joyful_01.webp"})."""
    rel = rex.OWNER_DIRS[owner_type]
    folder = tmp_path / rel / slug
    folder.mkdir(parents=True)
    for key in keys:
        (folder / f"{key}_01.webp").write_bytes(b"x")
    return tmp_path


# ---------------------------------------------------------------------------
# fetch_narrator — unit level
# ---------------------------------------------------------------------------

def test_fetch_narrator_bot_returns_id_and_keyed_rows(monkeypatch):
    def fake_api(path, payload=None, method=None, timeout=30):
        assert path == "/api/narrators/bot/brass-lampkeeper"
        return {"data": {"id": 42, "ExpressionMedia": [
            {"expressionKey": "joyful", "imagePath": "/x.webp"},
            {"expressionKey": "sorrowful", "imagePath": "/y.webp"},
        ]}}

    monkeypatch.setattr(rex, "api", fake_api)
    owner_id, existing = rex.fetch_narrator("bot", "brass-lampkeeper")
    assert owner_id == 42
    assert set(existing) == {"joyful", "sorrowful"}


def test_fetch_narrator_404_returns_none_none(monkeypatch):
    def fake_api(path, payload=None, method=None, timeout=30):
        raise http_404(path)

    monkeypatch.setattr(rex, "api", fake_api)
    assert rex.fetch_narrator("bot", "unknown-slug") == (None, None)


def test_fetch_narrator_character_uses_source_character_id(monkeypatch):
    # data.id is the default narrator BOT id, not the character's own id —
    # the real owner id lives in sourceCharacterId (see fetch_narrator docstring).
    def fake_api(path, payload=None, method=None, timeout=30):
        assert path == "/api/narrators/character/glitch-pixl"
        return {"data": {"id": 999, "sourceCharacterId": 55, "ExpressionMedia": []}}

    monkeypatch.setattr(rex, "api", fake_api)
    owner_id, existing = rex.fetch_narrator("character", "glitch-pixl")
    assert owner_id == 55
    assert existing == {}


# ---------------------------------------------------------------------------
# fetch_owner_ids — first-100-truncation regression (PR #360 root cause)
# ---------------------------------------------------------------------------

def test_fetch_owner_ids_stops_when_pagination_stalls(monkeypatch):
    # kind_robots' /api/bots historically ignored paging params and returned
    # the same first 100 rows for every page. fetch_owner_ids must detect
    # "no new slugs added" and stop instead of looping forever or silently
    # believing there are more than 100 owners.
    calls = []
    same_100 = [{"slug": f"bot-{i}", "id": i + 1} for i in range(100)]

    def fake_api(path, payload=None, method=None, timeout=30):
        calls.append(path)
        return {"data": same_100}

    monkeypatch.setattr(rex, "api", fake_api)
    ids = rex.fetch_owner_ids("bot")

    assert len(ids) == 100
    assert calls == ["/api/bots?page=1&pageSize=100", "/api/bots?page=2&pageSize=100"]


# ---------------------------------------------------------------------------
# main() — narrator-first / bulk-fallback resolution (integration, dry-run)
# ---------------------------------------------------------------------------

def test_narrator_lookup_wins_and_skips_bulk_list(tmp_path, monkeypatch, capsys):
    make_expr_tree(tmp_path, "bot", "brass-lampkeeper", ["joyful"])
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)

    calls = []

    def fake_api(path, payload=None, method=None, timeout=30):
        calls.append(path)
        assert not path.startswith("/api/bots?"), "bulk list must not be queried"
        assert path == "/api/narrators/bot/brass-lampkeeper"
        return {"data": {"id": 7, "ExpressionMedia": [
            {"expressionKey": "joyful", "imagePath": "/other.webp"},
        ]}}

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr(
        "sys.argv",
        ["reconcile_expressions.py", "--check", "--type", "bot", "--owner", "brass-lampkeeper"],
    )

    exit_code = rex.main()

    assert calls == ["/api/narrators/bot/brass-lampkeeper"]
    totals = json.loads(capsys.readouterr().out.strip())
    assert totals["update"] == 1  # imagePath drifted from convention path
    assert totals["create"] == 0
    assert exit_code == 2  # --check: drift found


def test_narrator_404_falls_back_to_bulk_list_rows_unknown_create_only(tmp_path, monkeypatch, capsys):
    make_expr_tree(tmp_path, "bot", "glitch-pixl", ["joyful"])
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/narrators/bot/glitch-pixl":
            raise http_404(path)
        if path.startswith("/api/bots?"):
            return {"data": [{"slug": "glitch-pixl", "id": 13}]}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr(
        "sys.argv",
        ["reconcile_expressions.py", "--check", "--type", "bot", "--owner", "glitch-pixl"],
    )

    rex.main()

    captured = capsys.readouterr()
    totals = json.loads(captured.out.strip())
    # rows unknown (existing=None) -> creates only, never a "missing" deactivation.
    assert totals["create"] == 1
    assert totals["update"] == 0
    assert totals["missing"] == 0
    assert "rows unreadable" in captured.err
