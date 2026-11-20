"""Regression tests for the Rainbow Fever Dream export preflight.

A curated boss is a single painted encounter. Missing render phases or key art
must stop the exporter before it writes a partial atlas or manifest.
"""

from pathlib import Path

import yaml

import scripts.export_rainbow_doodle_art as exporter


def _subject(asset: str, image_id: int | None, status: str = "DONE") -> dict:
    return {
        "asset": f"{exporter.ART}/doodle/{asset}",
        "art": {"krea": {"status": status, "art_image_id": image_id}},
    }


def _setup_export(tmp_path, monkeypatch, *, unfinished_phase=None, missing_key_art=False):
    app = tmp_path / "kind_robots"
    classic = app / "public" / exporter.ART / "bosses"
    classic.mkdir(parents=True)
    subjects = []
    for phase in (1, 2, 3):
        rel = f"bosses/b01-phase{phase}"
        (classic / f"b01-phase{phase}.webp").write_bytes(b"classic")
        subjects.append(
            _subject(
                rel,
                phase + 100,
                "RUNNING" if phase == unfinished_phase else "DONE",
            )
        )
    if not missing_key_art:
        subjects.append(_subject("key-art", 901))

    ledger = tmp_path / "ledger.yaml"
    ledger.write_text(yaml.safe_dump({"subjects": subjects}))
    review = tmp_path / "review.yaml"
    review.write_text(
        yaml.safe_dump({"decisions": {"bosses/b01": "keep", "key-art": "keep"}})
    )
    monkeypatch.setattr(exporter, "LEDGERS", [ledger])
    monkeypatch.setattr(exporter, "REVIEW", review)
    monkeypatch.setattr(
        exporter,
        "render_path",
        lambda subjects, rel, cache: Path("/unused/preflight-only.png"),
    )
    return app


def test_missing_boss_phase_fails_before_any_export(tmp_path, monkeypatch, capsys):
    app = _setup_export(tmp_path, monkeypatch, unfinished_phase=2)

    result = exporter.main(["--kind-robots", str(app), "--cache", str(tmp_path / "cache")])

    assert result == 1
    assert "cannot keep bosses/b01" in capsys.readouterr().err
    assert not (app / "public" / exporter.ART / "doodle").exists()
    assert not (app / exporter.MANIFEST).exists()


def test_missing_key_art_fails_before_any_export(tmp_path, monkeypatch, capsys):
    app = _setup_export(tmp_path, monkeypatch, missing_key_art=True)

    result = exporter.main(["--kind-robots", str(app), "--dry-run"])

    assert result == 1
    assert "cannot keep key-art: no finished render" in capsys.readouterr().err
    assert not (app / exporter.MANIFEST).exists()


def test_all_finished_phases_and_key_art_pass_dry_run(tmp_path, monkeypatch, capsys):
    app = _setup_export(tmp_path, monkeypatch)

    result = exporter.main(["--kind-robots", str(app), "--dry-run"])

    assert result == 0
    captured = capsys.readouterr()
    for phase in (1, 2, 3):
        assert f"keep  bosses/b01-phase{phase}" in captured.out
    assert "keep  key-art" in captured.out
    assert "4 Fever Dream pictures" in captured.err
    assert not (app / exporter.MANIFEST).exists()
