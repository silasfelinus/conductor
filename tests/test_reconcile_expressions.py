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


# ---------------------------------------------------------------------------
# plan_owner — unit level (conductor/t-050)
# ---------------------------------------------------------------------------

def test_plan_owner_deactivates_row_whose_file_is_gone():
    # "sorrowful" has a known row but no still on disk anymore; "joyful" still
    # has both. Only judgeable when existing rows were actually readable.
    scanned = {"stills": {"joyful": "joyful_01.webp"}, "loops": {}}
    existing = {
        "joyful": {"imagePath": "/images/bots/expressions/brass-lampkeeper/joyful_01.webp"},
        "sorrowful": {"expression": "SORROWFUL", "kind": "EMOTION"},
    }

    creates, updates, missing, notes = rex.plan_owner(
        "bot", "brass-lampkeeper", 7, scanned, existing
    )

    assert creates == []
    assert updates == []
    assert missing == [{
        "botId": 7,
        "expressionKey": "sorrowful",
        "expression": "SORROWFUL",
        "kind": "EMOTION",
        "isActive": False,
    }]
    assert notes == []


def test_plan_owner_never_deactivates_when_rows_unreadable():
    # existing=None means rows couldn't be fetched -- never invent a
    # deactivation from an unknown baseline.
    scanned = {"stills": {}, "loops": {}}

    creates, updates, missing, notes = rex.plan_owner(
        "bot", "brass-lampkeeper", 7, scanned, None
    )

    assert missing == []


def test_plan_owner_reports_loop_with_no_matching_still():
    # A *_loop.webp with no numbered still for that key is flagged, not
    # silently upserted as a row carrying only videoPath.
    scanned = {"stills": {}, "loops": {"joyful": "joyful_loop.webp"}}

    creates, updates, missing, notes = rex.plan_owner(
        "bot", "brass-lampkeeper", 7, scanned, {}
    )

    assert creates == []
    assert updates == []
    assert notes == ["joyful: loop video with no still — skipped"]


# ---------------------------------------------------------------------------
# main() — --apply / --deactivate CLI gating (conductor/t-051)
# ---------------------------------------------------------------------------
#
# These cover the gate `if all_missing and args.deactivate:` in main() and the
# stderr `deactivate_note` — the CLI wiring around plan_owner()'s missing rows,
# which the unit tests above (t-050) did not exercise.

def _apply_setup(tmp_path, monkeypatch, slug="brass-lampkeeper"):
    """One matching 'joyful' still on disk; the narrator additionally reports a
    'sorrowful' row whose file is gone -> exactly one missing-file row, zero
    creates/updates. Returns the list of api() POST payloads to
    /api/bots/expressions so a test can assert whether missing rows were sent."""
    make_expr_tree(tmp_path, "bot", slug, ["joyful"])
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    monkeypatch.setattr(rex, "KR_API_TOKEN", "fake-token")  # --apply gate

    posts = []

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == f"/api/narrators/bot/{slug}":
            return {"data": {"id": 7, "ExpressionMedia": [
                # joyful: imagePath already matches the convention -> no update
                {"expressionKey": "joyful",
                 "imagePath": f"/images/bots/expressions/{slug}/joyful_01.webp"},
                # sorrowful: has a row but no file on disk -> missing
                {"expressionKey": "sorrowful",
                 "expression": "SORROWFUL", "kind": "EMOTION"},
            ]}}
        if path == "/api/bots/expressions":
            posts.append(payload)
            return {"data": []}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    return posts


def test_apply_without_deactivate_detects_but_never_posts_missing(tmp_path, monkeypatch, capsys):
    posts = _apply_setup(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "sys.argv",
        ["reconcile_expressions.py", "--apply", "--type", "bot", "--owner", "brass-lampkeeper"],
    )

    code = rex.main()

    totals = json.loads(capsys.readouterr().out.strip())
    # the missing row is still detected and counted ...
    assert totals["missing"] == 1
    assert totals["create"] == 0 and totals["update"] == 0
    # ... but with no creates/updates and no --deactivate, nothing is POSTed
    assert posts == []
    assert code == 0


def test_apply_with_deactivate_posts_missing_soft_disable(tmp_path, monkeypatch, capsys):
    posts = _apply_setup(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "sys.argv",
        ["reconcile_expressions.py", "--apply", "--deactivate",
         "--type", "bot", "--owner", "brass-lampkeeper"],
    )

    rex.main()

    # post_batch sends a dryRun payload then the real write -> 2 calls, both
    # carrying the single soft-disable (isActive False) row.
    assert len(posts) == 2
    assert posts[0].get("dryRun") is True
    assert posts[-1]["expressions"] == [{
        "botId": 7,
        "expressionKey": "sorrowful",
        "expression": "SORROWFUL",
        "kind": "EMOTION",
        "isActive": False,
    }]


def test_deactivate_note_shown_when_missing_and_not_deactivating(tmp_path, monkeypatch, capsys):
    _apply_setup(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "sys.argv",
        ["reconcile_expressions.py", "--apply", "--type", "bot", "--owner", "brass-lampkeeper"],
    )

    rex.main()

    assert "missing-file rows reported only" in capsys.readouterr().err


def test_deactivate_note_suppressed_when_deactivating(tmp_path, monkeypatch, capsys):
    _apply_setup(tmp_path, monkeypatch)
    monkeypatch.setattr(
        "sys.argv",
        ["reconcile_expressions.py", "--apply", "--deactivate",
         "--type", "bot", "--owner", "brass-lampkeeper"],
    )

    rex.main()

    assert "missing-file rows reported only" not in capsys.readouterr().err
