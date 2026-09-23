"""Tests for scripts/resync_vendored_scanner.py. No network, no real files."""

import sys

import scripts.resync_vendored_scanner as resync_mod


def write_vendor_file(root, name, text):
    vendor_dir = root / "ops" / "home-server" / "lora-catalog"
    vendor_dir.mkdir(parents=True, exist_ok=True)
    (vendor_dir / name).write_text(text, encoding="utf-8")
    return vendor_dir


def make_fetcher(originals, error_for=None):
    """A fake fetcher matching fetch_kind_robots_file's (bytes|None, error|None) signature."""

    def fetcher(source_relative, ref, token):
        if error_for and source_relative in error_for:
            return None, error_for[source_relative]
        return originals[source_relative].encode("utf-8"), None

    return fetcher


def test_resync_writes_changed_file_and_appends_note(tmp_path):
    vendor_dir = write_vendor_file(tmp_path, "scan_loras.py", "print('old')\n")
    provenance_path = tmp_path / "PROVENANCE.md"
    provenance_path.write_text("# Vendored LoRA catalog tools\n", encoding="utf-8")

    result = resync_mod.resync(
        file_name="scan_loras.py",
        reason="adds the XYZ field",
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance_path,
        fetcher=make_fetcher({"scan_loras.py": "print('new')\n"}),
        today="2026-09-23",
    )

    assert result["ok"] is True
    assert result["changed"] is True
    assert (vendor_dir / "scan_loras.py").read_text(encoding="utf-8") == "print('new')\n"
    provenance_text = provenance_path.read_text(encoding="utf-8")
    assert "Re-synced 2026-09-23 (`scan_loras.py`) for adds the XYZ field." in provenance_text
    assert "kind_robots@main" in provenance_text


def test_resync_no_change_when_already_matching(tmp_path):
    vendor_dir = write_vendor_file(tmp_path, "scan_loras.py", "print('same')\n")
    provenance_path = tmp_path / "PROVENANCE.md"
    provenance_path.write_text("# header\n", encoding="utf-8")

    result = resync_mod.resync(
        file_name="scan_loras.py",
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance_path,
        fetcher=make_fetcher({"scan_loras.py": "print('same')\n"}),
    )

    assert result == {
        "ok": True,
        "changed": False,
        "file": "scan_loras.py",
        "current_bytes": 14,
        "source_bytes": 14,
        "byte_delta": 0,
    }
    assert provenance_path.read_text(encoding="utf-8") == "# header\n"


def test_resync_dry_run_does_not_write(tmp_path):
    vendor_dir = write_vendor_file(tmp_path, "scan_loras.py", "print('old')\n")
    provenance_path = tmp_path / "PROVENANCE.md"
    provenance_path.write_text("# header\n", encoding="utf-8")

    result = resync_mod.resync(
        file_name="scan_loras.py",
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance_path,
        fetcher=make_fetcher({"scan_loras.py": "print('new')\n"}),
        dry_run=True,
        today="2026-09-23",
    )

    assert result["ok"] is True
    assert result["changed"] is True
    assert result["dry_run"] is True
    assert (vendor_dir / "scan_loras.py").read_text(encoding="utf-8") == "print('old')\n"
    assert provenance_path.read_text(encoding="utf-8") == "# header\n"


def test_resync_unknown_file_is_an_error(tmp_path):
    vendor_dir = tmp_path / "ops" / "home-server" / "lora-catalog"
    provenance_path = tmp_path / "PROVENANCE.md"

    result = resync_mod.resync(
        file_name="not_tracked.py",
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance_path,
        fetcher=make_fetcher({}),
    )

    assert result["ok"] is False
    assert "not_tracked.py" in result["error"]


def test_resync_no_token_is_an_error(tmp_path):
    vendor_dir = write_vendor_file(tmp_path, "scan_loras.py", "print('old')\n")
    provenance_path = tmp_path / "PROVENANCE.md"

    result = resync_mod.resync(
        file_name="scan_loras.py",
        token="",
        vendor_dir=vendor_dir,
        provenance_path=provenance_path,
        fetcher=make_fetcher({"scan_loras.py": "print('old')\n"}),
    )

    assert result["ok"] is False
    assert "GITHUB_TOKEN" in result["error"]


def test_resync_fetch_error_is_an_error(tmp_path):
    vendor_dir = write_vendor_file(tmp_path, "scan_loras.py", "print('old')\n")
    provenance_path = tmp_path / "PROVENANCE.md"

    result = resync_mod.resync(
        file_name="scan_loras.py",
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance_path,
        fetcher=make_fetcher({}, error_for={"scan_loras.py": "HTTP 404 fetching scan_loras.py"}),
    )

    assert result["ok"] is False
    assert result["error"] == "HTTP 404 fetching scan_loras.py"


def test_main_exit_codes_success_and_error(tmp_path, monkeypatch):
    vendor_dir = write_vendor_file(tmp_path, "scan_loras.py", "print('old')\n")
    provenance_path = tmp_path / "PROVENANCE.md"
    provenance_path.write_text("# header\n", encoding="utf-8")

    monkeypatch.setattr(resync_mod, "VENDOR_DIR", vendor_dir)
    monkeypatch.setattr(resync_mod, "PROVENANCE_PATH", provenance_path)
    monkeypatch.setattr(
        resync_mod, "fetch_kind_robots_file", make_fetcher({"scan_loras.py": "print('new')\n"})
    )
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
    monkeypatch.setattr(sys, "argv", ["resync_vendored_scanner.py", "--file", "scan_loras.py"])

    try:
        resync_mod.main()
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("main() should call sys.exit")

    assert (vendor_dir / "scan_loras.py").read_text(encoding="utf-8") == "print('new')\n"

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.setattr(sys, "argv", ["resync_vendored_scanner.py", "--file", "scan_loras.py"])
    try:
        resync_mod.main()
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("main() should call sys.exit")
