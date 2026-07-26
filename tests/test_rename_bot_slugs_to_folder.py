"""Tests for scripts/rename_bot_slugs_to_folder.py (kind-robots/t-011
follow-up: make slug the single source of truth, derived from the actual
expression-image folder name -- not the bot's avatarImage field, which
Silas confirmed was just a rough-draft title superseded by the real
folders on the media share).
"""
import json
from pathlib import Path

import scripts.reconcile_expressions as rex
import scripts.rename_bot_slugs_to_folder as r


def make_expr_folder(tmp_path: Path, owner_type: str, folder_name: str) -> Path:
    """A bare expression folder -- this script only needs the folder to
    exist, not any files inside it, since it derives owner-resolution the
    same way reconcile_expressions.py does."""
    rel = rex.OWNER_DIRS[owner_type]
    folder = tmp_path / rel / folder_name
    folder.mkdir(parents=True)
    return tmp_path


def test_build_rename_plan_renames_to_the_iterated_folder_name(tmp_path, monkeypatch):
    # The folder is named "brass-lampkeeper" -- direct narrator lookup under
    # that name 404s, so resolution falls through to the avatarImage
    # fallback (whose stem must equal the folder name for this tier to
    # match at all -- that's the same constraint reconcile_expressions.py
    # has), recovering the real owner (CURRENT slug "pip-the-lampkeeper").
    # The plan target is the folder name itself (rex.Path(...).stem of the
    # directory being iterated), never re-derived from any API field --
    # this is what makes it immune to a stale avatarImage going forward.
    base = make_expr_folder(tmp_path, "bot", "brass-lampkeeper")

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/narrators/bot/brass-lampkeeper":
            import urllib.error, io
            raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))
        if path == "/api/narrators/bot/pip-the-lampkeeper":
            return {"data": {"id": 42, "ExpressionMedia": []}}
        if path.startswith("/api/bots?"):
            return {"data": [{
                "slug": "pip-the-lampkeeper", "id": 42,
                "avatarImage": "/images/bots/brass-lampkeeper.webp",
            }]}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    base_dir = base / rex.OWNER_DIRS["bot"]
    plan = r.build_rename_plan("bot", base_dir)

    assert plan == [(42, "pip-the-lampkeeper", "brass-lampkeeper")]


def test_build_rename_plan_skips_folder_already_matching_slug(tmp_path, monkeypatch):
    base = make_expr_folder(tmp_path, "bot", "barkeep-vox")

    def fake_api(path, payload=None, method=None, timeout=30):
        assert path == "/api/narrators/bot/barkeep-vox"
        return {"data": {"id": 9, "ExpressionMedia": []}}

    monkeypatch.setattr(rex, "api", fake_api)
    base_dir = base / rex.OWNER_DIRS["bot"]
    plan = r.build_rename_plan("bot", base_dir)

    assert plan == []


def test_build_rename_plan_skips_unresolvable_folder(tmp_path, monkeypatch):
    base = make_expr_folder(tmp_path, "bot", "nobody-owns-this")

    def fake_api(path, payload=None, method=None, timeout=30):
        import urllib.error, io
        if path.startswith("/api/bots?"):
            return {"data": []}
        raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))

    monkeypatch.setattr(rex, "api", fake_api)
    base_dir = base / rex.OWNER_DIRS["bot"]
    plan = r.build_rename_plan("bot", base_dir)

    assert plan == []  # left for reconcile_expressions.py's own reporting


def test_main_dry_run_prints_plan_without_patching(tmp_path, monkeypatch, capsys):
    make_expr_folder(tmp_path, "bot", "brass-lampkeeper")
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    monkeypatch.setattr(rex, "KR_MEDIA_IMAGES_DIR", "")

    def fake_api(path, payload=None, method=None, timeout=30):
        if method == "PATCH":
            raise AssertionError("dry-run must never PATCH")
        if path == "/api/narrators/bot/brass-lampkeeper":
            import urllib.error, io
            raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))
        if path.startswith("/api/bots?"):
            return {"data": [{"id": 42, "slug": "pip-the-lampkeeper",
                               "avatarImage": "/images/bots/brass-lampkeeper.webp"}]}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_folder.py", "--type", "bot"])

    code = r.main()

    out = capsys.readouterr().out
    assert "pip-the-lampkeeper -> brass-lampkeeper" in out
    summary = json.loads(out.strip().splitlines()[-1])
    assert summary == {"mode": "dry-run", "planned": 1, "applied": 0, "errors": 0}
    assert code == 0


def test_main_apply_without_token_returns_1_before_any_work(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    monkeypatch.setattr(rex, "KR_API_TOKEN", "")

    def exploding_api(path, payload=None, method=None, timeout=30):
        raise AssertionError("api() must not be called without a token")

    monkeypatch.setattr(rex, "api", exploding_api)
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_folder.py", "--apply"])

    code = r.main()

    assert code == 1
    assert "--apply requires KR_API_TOKEN" in capsys.readouterr().err


def test_main_apply_patches_the_resolved_owner_to_the_folder_name(tmp_path, monkeypatch, capsys):
    make_expr_folder(tmp_path, "bot", "brass-lampkeeper")
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    monkeypatch.setattr(rex, "KR_MEDIA_IMAGES_DIR", "")
    monkeypatch.setattr(rex, "KR_API_TOKEN", "test-token")
    patched = []

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/narrators/bot/brass-lampkeeper":
            import urllib.error, io
            raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))
        if path.startswith("/api/bots?"):
            return {"data": [{"id": 42, "slug": "pip-the-lampkeeper",
                               "avatarImage": "/images/bots/brass-lampkeeper.webp"}]}
        if path == "/api/bots/42" and method == "PATCH":
            patched.append(payload)
            return {"success": True, "data": {"id": 42, "slug": "brass-lampkeeper"}}
        raise AssertionError(f"unexpected call: {path} {method}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_folder.py", "--apply", "--type", "bot"])

    code = r.main()

    assert patched == [{"slug": "brass-lampkeeper"}]
    summary = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert summary == {"mode": "applied", "planned": 1, "applied": 1, "errors": 0}
    assert code == 0


def test_main_media_images_dir_takes_precedence_over_kind_robots_root(tmp_path, monkeypatch, capsys):
    media_root = tmp_path / "media"
    checkout_root = tmp_path / "checkout"
    make_expr_folder(media_root, "bot", "brass-lampkeeper")
    make_expr_folder(checkout_root, "bot", "some-other-bot")
    monkeypatch.setattr(rex, "KR_MEDIA_IMAGES_DIR", str(media_root))
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", checkout_root)

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/narrators/bot/brass-lampkeeper":
            import urllib.error, io
            raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))
        if path.startswith("/api/bots?"):
            return {"data": [{"id": 42, "slug": "pip-the-lampkeeper",
                               "avatarImage": "/images/bots/brass-lampkeeper.webp"}]}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr("sys.argv", ["rename_bot_slugs_to_folder.py", "--type", "bot"])

    r.main()

    assert "some-other-bot" not in capsys.readouterr().err


# ---------------------------------------------------------------------------
# --rename OLD=NEW explicit override (Silas, 2026-07-26: he's also renaming
# the physical folders themselves for ami-bot -> ami-matriarch and
# ami-butterfly -> ami-swarm -- the folder scan can't resolve these, since
# the NEW folder name was never the owner's slug, avatarImage, or anything
# else the three lookup tiers would find. An explicit, known-current-slug
# override is the escape hatch for this kind of deliberate one-off rename.)
# ---------------------------------------------------------------------------

def test_rename_arg_dry_run_resolves_and_prints(tmp_path, monkeypatch, capsys):
    # No expression folders at all needed for this path -- it's a direct
    # narrator lookup by the CURRENT slug the caller already knows.
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    (tmp_path / rex.OWNER_DIRS["bot"]).mkdir(parents=True)
    (tmp_path / rex.OWNER_DIRS["character"]).mkdir(parents=True)

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/narrators/bot/ami-bot":
            return {"data": {"id": 7, "ExpressionMedia": []}}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr(
        "sys.argv",
        ["rename_bot_slugs_to_folder.py", "--rename", "ami-bot=ami-matriarch"],
    )

    code = r.main()

    out = capsys.readouterr().out
    assert "ami-bot -> ami-matriarch" in out
    summary = json.loads(out.strip().splitlines()[-1])
    assert summary == {"mode": "dry-run", "planned": 1, "applied": 0, "errors": 0}
    assert code == 0


def test_rename_arg_apply_patches_resolved_owner(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    (tmp_path / rex.OWNER_DIRS["bot"]).mkdir(parents=True)
    (tmp_path / rex.OWNER_DIRS["character"]).mkdir(parents=True)
    monkeypatch.setattr(rex, "KR_API_TOKEN", "test-token")
    patched = []

    def fake_api(path, payload=None, method=None, timeout=30):
        if path == "/api/narrators/bot/ami-bot":
            return {"data": {"id": 7, "ExpressionMedia": []}}
        if path == "/api/bots/7" and method == "PATCH":
            patched.append(payload)
            return {"success": True, "data": {"id": 7, "slug": "ami-matriarch"}}
        raise AssertionError(f"unexpected call: {path} {method}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr(
        "sys.argv",
        ["rename_bot_slugs_to_folder.py", "--apply",
         "--rename", "ami-bot=ami-matriarch"],
    )

    code = r.main()

    assert patched == [{"slug": "ami-matriarch"}]
    summary = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert summary == {"mode": "applied", "planned": 1, "applied": 1, "errors": 0}
    assert code == 0


def test_rename_arg_multiple_overrides_and_falls_back_to_character_type(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    (tmp_path / rex.OWNER_DIRS["bot"]).mkdir(parents=True)
    (tmp_path / rex.OWNER_DIRS["character"]).mkdir(parents=True)

    def fake_api(path, payload=None, method=None, timeout=30):
        import urllib.error, io
        if path == "/api/narrators/bot/ami-bot":
            return {"data": {"id": 7, "ExpressionMedia": []}}
        if path == "/api/narrators/bot/ami-butterfly":
            raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))
        if path == "/api/narrators/character/ami-butterfly":
            return {"data": {"sourceCharacterId": 55, "ExpressionMedia": []}}
        raise AssertionError(f"unexpected call: {path}")

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr(
        "sys.argv",
        ["rename_bot_slugs_to_folder.py",
         "--rename", "ami-bot=ami-matriarch",
         "--rename", "ami-butterfly=ami-swarm"],
    )

    code = r.main()

    out = capsys.readouterr().out
    assert "ami-bot -> ami-matriarch" in out
    assert "ami-butterfly -> ami-swarm" in out
    summary = json.loads(out.strip().splitlines()[-1])
    assert summary == {"mode": "dry-run", "planned": 2, "applied": 0, "errors": 0}
    assert code == 0


def test_rename_arg_unresolvable_slug_is_an_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    (tmp_path / rex.OWNER_DIRS["bot"]).mkdir(parents=True)
    (tmp_path / rex.OWNER_DIRS["character"]).mkdir(parents=True)

    def fake_api(path, payload=None, method=None, timeout=30):
        import urllib.error, io
        raise urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b""))

    monkeypatch.setattr(rex, "api", fake_api)
    monkeypatch.setattr(
        "sys.argv",
        ["rename_bot_slugs_to_folder.py", "--rename", "nobody=somebody"],
    )

    code = r.main()

    assert code == 1
    assert "could not resolve current slug 'nobody'" in capsys.readouterr().err


def test_rename_arg_malformed_value_rejected(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rex, "KIND_ROBOTS_ROOT", tmp_path)
    monkeypatch.setattr(
        "sys.argv",
        ["rename_bot_slugs_to_folder.py", "--rename", "no-equals-sign"],
    )

    code = r.main()

    assert code == 1
    assert "--rename must be OLD=NEW" in capsys.readouterr().err
