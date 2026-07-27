"""
Tests for consume_animation_pitches.py — draining dated pitch artifacts (the
connector-only-Worker workaround from conductor PR #1043) into the canonical
animation-manager PITCHES.yaml.
"""

import textwrap
from pathlib import Path

import pytest
import yaml

import scripts.consume_animation_pitches as cap


PITCHES = textwrap.dedent(
    """\
    updated: "2026-07-20T00:00:00+00:00"

    pitches:
      - id: existing-one
        title: Existing One
        status: shipped
        priority: 1
        surprise: A thing that already happened.
        passive_loop: It loops.
        optional_interaction: Click it.
        technique: Canvas 2D.
        reduced_motion: Less motion.
        performance_risk: Low.
        novelty: It is the only one.
        acceptance:
          - it loops without interaction
    """
)

ARTIFACT = textwrap.dedent(
    """\
    id: new-pitch
    title: New Pitch
    status: pitched
    priority: 99
    created: '2026-07-25T07:10:34-07:00'
    surprise: A brand new surprising glow drifts across the screen.
    passive_loop: It drifts around gently forever.
    optional_interaction: Pointer nudges it.
    technique: WebGL shader particles with a twist.
    reduced_motion: One slow particle.
    performance_risk: Cap particle count.
    novelty: Totally distinct from existing-one's approach.
    acceptance:
      - it renders without interaction
    """
)


@pytest.fixture(autouse=True)
def sandbox(tmp_path, monkeypatch):
    pitches_file = tmp_path / "PITCHES.yaml"
    pitches_file.write_text(PITCHES, encoding="utf-8")
    pitch_dir = tmp_path / "pitches"
    pitch_dir.mkdir()
    monkeypatch.setattr(cap, "PITCHES_FILE", pitches_file)
    monkeypatch.setattr(cap, "PITCH_DIR", pitch_dir)
    return pitches_file, pitch_dir


def write_artifact(pitch_dir, name, text=ARTIFACT):
    path = pitch_dir / name
    path.write_text(text, encoding="utf-8")
    return path


def test_no_artifacts_is_a_noop(sandbox, capsys):
    assert cap.main(["--live"]) == 0
    assert "No pending pitch artifacts" in capsys.readouterr().out


def test_dry_run_does_not_write_or_delete(sandbox):
    pitches_file, pitch_dir = sandbox
    artifact = write_artifact(pitch_dir, "2026-07-25-new-pitch.yaml")
    before = pitches_file.read_text(encoding="utf-8")

    assert cap.main([]) == 0

    assert pitches_file.read_text(encoding="utf-8") == before
    assert artifact.exists()


def test_live_run_consolidates_and_deletes_artifact(sandbox):
    pitches_file, pitch_dir = sandbox
    artifact = write_artifact(pitch_dir, "2026-07-25-new-pitch.yaml")

    assert cap.main(["--live"]) == 0

    assert not artifact.exists()
    data = yaml.safe_load(pitches_file.read_text(encoding="utf-8"))
    ids = {p["id"] for p in data["pitches"]}
    assert ids == {"existing-one", "new-pitch"}


def test_priority_is_recomputed_not_trusted(sandbox):
    """The artifact claims priority: 99; the processor must renumber it to
    max(existing) + 1 so two artifacts queued out of order can't collide."""
    pitches_file, pitch_dir = sandbox
    write_artifact(pitch_dir, "2026-07-25-new-pitch.yaml")

    cap.main(["--live"])

    data = yaml.safe_load(pitches_file.read_text(encoding="utf-8"))
    new_pitch = next(p for p in data["pitches"] if p["id"] == "new-pitch")
    assert new_pitch["priority"] == 2


def test_created_field_is_dropped_from_canonical_entry(sandbox):
    pitches_file, pitch_dir = sandbox
    write_artifact(pitch_dir, "2026-07-25-new-pitch.yaml")

    cap.main(["--live"])

    data = yaml.safe_load(pitches_file.read_text(encoding="utf-8"))
    new_pitch = next(p for p in data["pitches"] if p["id"] == "new-pitch")
    assert "created" not in new_pitch


def test_existing_id_is_skipped_and_stale_artifact_removed(sandbox):
    pitches_file, pitch_dir = sandbox
    duplicate = ARTIFACT.replace("id: new-pitch", "id: existing-one")
    artifact = write_artifact(pitch_dir, "2026-07-25-dup.yaml", duplicate)

    assert cap.main(["--live"]) == 0

    assert not artifact.exists()
    data = yaml.safe_load(pitches_file.read_text(encoding="utf-8"))
    assert len(data["pitches"]) == 1


def test_invalid_artifact_is_skipped_not_fatal(sandbox, capsys):
    pitch_dir = sandbox[1]
    write_artifact(pitch_dir, "2026-07-25-broken.yaml", "id: broken\ntitle: Broken\n")

    assert cap.main([]) == 0
    assert "missing required field" in capsys.readouterr().out


def test_novelty_collision_aborts_without_writing(sandbox):
    pitches_file, pitch_dir = sandbox
    colliding = ARTIFACT.replace(
        "surprise: A brand new surprising glow drifts across the screen.",
        "surprise: A thing that already happened.",
    ).replace(
        "technique: WebGL shader particles with a twist.",
        "technique: Canvas 2D.",
    )
    artifact = write_artifact(pitch_dir, "2026-07-25-colliding.yaml", colliding)
    before = pitches_file.read_text(encoding="utf-8")

    assert cap.main(["--live"]) == 1

    assert pitches_file.read_text(encoding="utf-8") == before
    assert artifact.exists()


def test_folded_long_field_wraps_with_folded_scalar_style():
    long_text = " ".join(["word"] * 40)
    block = cap.format_field("surprise", long_text)
    assert block.startswith("    surprise: >\n")
    assert "word word" not in block.split(">\n", 1)[1].splitlines()[0][:6]


def test_short_field_stays_plain():
    block = cap.format_field("technique", "Canvas 2D.")
    assert block == "    technique: Canvas 2D."
