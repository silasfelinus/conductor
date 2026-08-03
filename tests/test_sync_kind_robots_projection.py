"""Tests for the one-way Conductor -> Kind Robots projection builder."""

import json
from pathlib import Path

import pytest

import scripts.sync_kind_robots_projection as projection


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_build_snapshot_preserves_complete_coordination_inputs(tmp_path, monkeypatch):
    write(
        tmp_path / "project-overrides.yaml",
        "overrides:\n"
        "  - slug: active-project\n"
        "    status: active\n"
        "  - slug: paused-project\n"
        "    status: paused\n",
    )
    write(
        tmp_path / "projects" / "active-project" / "roadmap.yaml",
        "project: Active Project\ntasks: []\n",
    )
    write(
        tmp_path / "projects" / "paused-project" / "roadmap.yaml",
        "project: Paused Project\ntasks: []\n",
    )
    write(
        tmp_path / "projects" / "_template" / "roadmap.yaml",
        "project: Template\ntasks: []\n",
    )
    write(
        tmp_path / "pitches" / "2026-08-03-projection.md",
        "# Pitch: Projection\nstatus: awaiting-silas\n",
    )
    image = tmp_path / "projects" / "images" / "active-project-card.webp"
    image.parent.mkdir(parents=True, exist_ok=True)
    image.write_bytes(b"card-image")

    monkeypatch.setattr(projection, "ROOT", tmp_path)
    monkeypatch.setattr(projection, "source_commit_sha", lambda: "a" * 40)

    snapshot = projection.build_snapshot()

    assert snapshot["sourceRepo"] == "silasfelinus/conductor"
    assert snapshot["sourceRef"] == "main"
    assert snapshot["sourceCommitSha"] == "a" * 40
    assert set(snapshot["roadmaps"]) == {"active-project", "paused-project"}
    assert "paused-project" in snapshot["registryYaml"]
    assert set(snapshot["pitches"]) == {"2026-08-03-projection.md"}
    assert len(snapshot["imageVersions"][image.name]) == 64


def test_encoded_snapshot_is_compact_valid_json():
    snapshot = {
        "version": 1,
        "sourceRepo": "silasfelinus/conductor",
        "sourceRef": "main",
        "sourceCommitSha": "b" * 40,
        "generatedAt": "2026-08-03T11:30:00Z",
        "registryYaml": "overrides: []\n",
        "roadmaps": {},
        "pitches": {},
        "imageVersions": {},
    }

    encoded = projection.encoded_snapshot(snapshot)

    assert b"\n" not in encoded
    assert json.loads(encoded) == snapshot


def test_encoded_snapshot_rejects_oversized_payload(monkeypatch):
    monkeypatch.setattr(projection, "MAX_PAYLOAD_BYTES", 20)

    with pytest.raises(RuntimeError, match="projection payload"):
        projection.encoded_snapshot({"payload": "larger than twenty bytes"})
