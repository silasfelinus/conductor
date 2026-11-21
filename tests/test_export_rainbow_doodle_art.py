"""Regression tests for the Rainbow Fever Dream export preflight.

A curated boss is a single painted encounter. Missing render phases or key art
must stop the exporter before it writes a partial atlas or manifest.
"""

from pathlib import Path

import yaml

import scripts.export_rainbow_doodle_art as exporter
from rainbow_doodle_fixture import make_doodle_subject, write_doodle_ledger


def _setup_export(tmp_path, monkeypatch, *, unfinished_phase=None, missing_key_art=False):
    app = tmp_path / "kind_robots"
    subjects = []
    for phase in (1, 2, 3):
        subjects.append(
            make_doodle_subject(
                tmp_path,
                f"bosses/b01-phase{phase}",
                phase + 100,
                status="RUNNING" if phase == unfinished_phase else "DONE",
            )
        )
    if not missing_key_art:
        subjects.append(
            make_doodle_subject(tmp_path, "key-art", 901, classic=False)
        )

    ledger = write_doodle_ledger(tmp_path, subjects, filename="ledger.yaml")
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


def test_shared_fixture_matches_finished_set_2_render_schema(tmp_path):
    subject = make_doodle_subject(tmp_path, "ships/halo-fin", 263272)
    ledger = write_doodle_ledger(tmp_path, [subject])
    data = yaml.safe_load(ledger.read_text())

    assert data["project_slug"] == "rainbow-bullet-hell-space-princess"
    assert data["lanes"][0]["engine"] == "kontext"
    assert subject["jobs"]["kontext"] > 0
    assert subject["source_image_id"] > 0
    assert subject["art"]["kontext"] == {
        "status": "DONE",
        "art_image_id": 263272,
    }
    assert exporter.finished_id(subject) == 263272
    assert exporter.classic_file(tmp_path / "kind_robots", "ships/halo-fin").is_file()
    assert (tmp_path / "cache/ships/halo-fin-263272.png").is_file()
