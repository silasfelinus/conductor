"""Focused tests for parity-report mode in resync_vendored_scanner.py."""

import scripts.resync_vendored_scanner as resync_mod


def make_fetcher(originals):
    def fetcher(source_relative, ref, token):
        return originals[source_relative].encode("utf-8"), None

    return fetcher


def setup_vendor(tmp_path):
    vendor_dir = tmp_path / "vendor"
    vendor_dir.mkdir()
    for name in resync_mod.TRACKED_FILES:
        (vendor_dir / name).write_text(f"old {name}\n", encoding="utf-8")
    provenance = tmp_path / "PROVENANCE.md"
    provenance.write_text("# provenance\n", encoding="utf-8")
    return vendor_dir, provenance


def test_parity_report_resyncs_each_unique_drift_file(tmp_path):
    vendor_dir, provenance = setup_vendor(tmp_path)
    report = {
        "ref": "main",
        "findings": [
            {"file": "scan_loras.py", "shape": "content-drift"},
            {"file": "scan_models.py", "shape": "content-drift"},
            {"file": "scan_loras.py", "shape": "content-drift"},
        ],
        "unresolved": [],
    }
    originals = {
        "scan_loras.py": "new loras\n",
        "scan_models.py": "new models\n",
    }

    result = resync_mod.resync_from_parity_report(
        report,
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance,
        fetcher=make_fetcher(originals),
        today="2026-09-23",
    )

    assert result["ok"] is True
    assert [item["file"] for item in result["results"]] == ["scan_loras.py", "scan_models.py"]
    assert (vendor_dir / "scan_loras.py").read_text() == "new loras\n"
    assert (vendor_dir / "scan_models.py").read_text() == "new models\n"
    text = provenance.read_text()
    assert text.count("Re-synced 2026-09-23") == 2
    assert "parity report drift" in text


def test_parity_report_dry_run_reports_byte_deltas_without_writing(tmp_path):
    vendor_dir, provenance = setup_vendor(tmp_path)
    old_loras = (vendor_dir / "scan_loras.py").read_bytes()
    old_models = (vendor_dir / "scan_models.py").read_bytes()
    old_provenance = provenance.read_text()
    originals = {
        "scan_loras.py": "tiny\n",
        "scan_models.py": "a much longer replacement model scanner\n",
    }
    report = {
        "ref": "main",
        "findings": [
            {"file": "scan_loras.py", "shape": "content-drift"},
            {"file": "scan_models.py", "shape": "content-drift"},
        ],
        "unresolved": [],
    }

    result = resync_mod.resync_from_parity_report(
        report,
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance,
        fetcher=make_fetcher(originals),
        dry_run=True,
    )

    assert result["ok"] is True
    by_file = {item["file"]: item for item in result["results"]}
    for file_name, original in originals.items():
        item = by_file[file_name]
        current_size = len((f"old {file_name}\n").encode("utf-8"))
        source_size = len(original.encode("utf-8"))
        assert item["current_bytes"] == current_size
        assert item["source_bytes"] == source_size
        assert item["byte_delta"] == source_size - current_size
        assert item["dry_run"] is True

    assert (vendor_dir / "scan_loras.py").read_bytes() == old_loras
    assert (vendor_dir / "scan_models.py").read_bytes() == old_models
    assert provenance.read_text() == old_provenance


def test_parity_report_uses_report_ref_unless_overridden(tmp_path):
    vendor_dir, provenance = setup_vendor(tmp_path)
    seen_refs = []

    def fetcher(source_relative, ref, token):
        seen_refs.append(ref)
        return b"new\n", None

    report = {
        "ref": "known-good-sha",
        "findings": [{"file": "scan_loras.py", "shape": "content-drift"}],
        "unresolved": [],
    }
    result = resync_mod.resync_from_parity_report(
        report,
        token="fake-token",
        vendor_dir=vendor_dir,
        provenance_path=provenance,
        fetcher=fetcher,
    )
    assert result["ok"] is True
    assert seen_refs == ["known-good-sha"]


def test_parity_report_refuses_unresolved_or_untracked_findings():
    unresolved = {
        "findings": [{"file": "scan_loras.py", "shape": "content-drift"}],
        "unresolved": [{"file": "scan_models.py", "detail": "HTTP 503"}],
    }
    result = resync_mod.resync_from_parity_report(unresolved, token="fake-token")
    assert result["ok"] is False
    assert "unresolved" in result["error"]

    untracked = {
        "findings": [{"file": "surprise.py", "shape": "content-drift"}],
        "unresolved": [],
    }
    result = resync_mod.resync_from_parity_report(untracked, token="fake-token")
    assert result["ok"] is False
    assert "untracked" in result["error"]


def test_clean_parity_report_is_a_noop():
    result = resync_mod.resync_from_parity_report(
        {"ref": "main", "findings": [], "unresolved": []}, token="fake-token"
    )
    assert result == {"ok": True, "ref": "main", "results": []}
