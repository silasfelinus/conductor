"""Tests for scripts/check_vendored_scanner_parity.py. No network, no real files."""

import scripts.check_vendored_scanner_parity as parity


def write_vendor_files(root, contents):
    vendor_dir = root / "ops" / "home-server" / "lora-catalog"
    vendor_dir.mkdir(parents=True, exist_ok=True)
    for name, text in contents.items():
        (vendor_dir / name).write_text(text, encoding="utf-8")
    return vendor_dir


def make_fetcher(originals, error_for=None):
    """A fake fetcher matching fetch_kind_robots_file's (bytes|None, error|None) signature."""

    def fetcher(source_relative, ref, token):
        if error_for and source_relative in error_for:
            return None, error_for[source_relative]
        return originals[source_relative].encode("utf-8"), None

    return fetcher


ALL_MATCHING = {
    "scan_loras.py": "print('loras')\n",
    "scan_models.py": "print('models')\n",
    "import_catalog.py": "print('import')\n",
}


def test_clean_when_all_files_match(tmp_path):
    vendor_dir = write_vendor_files(tmp_path, ALL_MATCHING)

    result = parity.scan(
        token="fake-token",
        vendor_dir=vendor_dir,
        fetcher=make_fetcher(ALL_MATCHING),
    )

    assert result["findings"] == []
    assert result["unresolved"] == []
    assert sorted(result["checked"]) == sorted(ALL_MATCHING)


def test_content_drift_flagged(tmp_path):
    vendor_dir = write_vendor_files(tmp_path, ALL_MATCHING)
    originals = dict(ALL_MATCHING)
    originals["scan_loras.py"] = "print('loras')\nprint('extra classifier')\n"

    result = parity.scan(
        token="fake-token",
        vendor_dir=vendor_dir,
        fetcher=make_fetcher(originals),
    )

    assert len(result["findings"]) == 1
    finding = result["findings"][0]
    assert finding["file"] == "scan_loras.py"
    assert finding["shape"] == "content-drift"
    assert "extra classifier" in finding["diff"]


def test_missing_vendor_file_flagged(tmp_path):
    partial = {k: v for k, v in ALL_MATCHING.items() if k != "scan_models.py"}
    vendor_dir = write_vendor_files(tmp_path, partial)

    result = parity.scan(
        token="fake-token",
        vendor_dir=vendor_dir,
        fetcher=make_fetcher(ALL_MATCHING),
    )

    shapes = {f["file"]: f["shape"] for f in result["findings"]}
    assert shapes["scan_models.py"] == "vendor-file-missing"


def test_fetch_error_is_unresolved_not_a_finding(tmp_path):
    vendor_dir = write_vendor_files(tmp_path, ALL_MATCHING)

    result = parity.scan(
        token="fake-token",
        vendor_dir=vendor_dir,
        fetcher=make_fetcher(ALL_MATCHING, error_for={"scan_loras.py": "HTTP 404 fetching scan_loras.py"}),
    )

    assert result["findings"] == []
    assert len(result["unresolved"]) == 1
    assert result["unresolved"][0]["file"] == "scan_loras.py"


def test_no_token_marks_everything_unresolved(tmp_path):
    vendor_dir = write_vendor_files(tmp_path, ALL_MATCHING)

    result = parity.scan(token="", vendor_dir=vendor_dir, fetcher=make_fetcher(ALL_MATCHING))

    assert result["findings"] == []
    assert len(result["unresolved"]) == len(ALL_MATCHING)
    assert result["checked"] == []


def test_main_exit_codes(tmp_path, monkeypatch, capsys):
    import sys

    vendor_dir = write_vendor_files(tmp_path, ALL_MATCHING)
    monkeypatch.setattr(parity, "VENDOR_DIR", vendor_dir)
    monkeypatch.setattr(parity, "fetch_kind_robots_file", make_fetcher(ALL_MATCHING))
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
    monkeypatch.setattr(sys, "argv", ["check_vendored_scanner_parity.py"])

    try:
        parity.main()
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("main() should call sys.exit")
