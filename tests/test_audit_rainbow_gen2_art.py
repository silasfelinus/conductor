"""Regression coverage for the read-only Rainbow X1-X4 production-art audit."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import audit_rainbow_gen2_art as audit


def write_ledger(directory: Path, filename: str, subjects: str) -> None:
    (directory / filename).write_text(
        "round: test\nsubjects:\n" + subjects,
        encoding="utf-8",
    )


def test_per_stage_art_ids_and_missing_paths(tmp_path, capsys):
    write_ledger(
        tmp_path,
        "GEN2-CORAL-COMET-X2.yaml",
        """- key: x2-guardian
  entity: stage-guardian
  stage: X2
  lane: krea2
  asset: rainbow-princess-art/enemies/guardian-comet-herder
  jobs: {krea2: 76599}
  art: {krea2: {status: DONE, art_image_id: 278620}}
- key: x2-pickup
  entity: stage-collectible
  stage: X2
  lane: krea2
  asset: rainbow-princess-art/pickups/cadet
  jobs: {krea2: 76598}
  art: {krea2: {status: QUEUED, art_image_id: 777}}
- key: x2-hazard
  entity: stage-hazard
  stage: X2
  lane: krea2
  asset: rainbow-princess-art/hazards/asteroid
  art: {krea2: {status: DONE, art_image_id: 0}}
""",
    )
    assert audit.main(["--art-dir", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert "ArtImage 278620: rainbow-princess-art/enemies/guardian-comet-herder" in output
    assert "MISSING: rainbow-princess-art/pickups/cadet" in output
    assert "MISSING: rainbow-princess-art/hazards/asteroid" in output
    assert "MISSING: no authored asset" in output
    assert audit.main(["--art-dir", str(tmp_path), "--strict"]) == 1


def test_x4_pose_ledger_recognizes_guardian_without_entity_or_stage(tmp_path):
    write_ledger(
        tmp_path,
        "MIRROR-SHOAL-X4.yaml",
        """- key: x4-shoal-koi-idle
  lane: krea2
  asset: rainbow-princess-art/doodle/alt/x4-shoalkoi-idle
  art: {krea2: {status: DONE, art_image_id: 277844}}
- key: x4-shoal-far
  lane: krea2
  asset: rainbow-princess-art/doodle/alt/x4-far
  art: {krea2: {status: DONE, art_image_id: 277840}}
""",
    )
    items = audit.scan(tmp_path)
    assert [(item.stage, item.role, item.image_id) for item in items] == [
        ("X4", "guardian", 277844)
    ]


def test_duplicate_ledgers_deduplicate_same_id_and_flag_conflict(tmp_path):
    content = """- key: guardian
  entity: stage-guardian
  stage: X3
  lane: krea2
  asset: rainbow-princess-art/enemies/guardian-bellkeeper
  art: {krea2: {status: DONE, art_image_id: 277699}}
"""
    write_ledger(tmp_path, "GEN2-A.yaml", content)
    write_ledger(tmp_path, "GEN2-B.yaml", content)
    output, _ = audit.report(audit.scan(tmp_path))
    assert output.count("ArtImage 277699") == 1
    write_ledger(tmp_path, "GEN2-B.yaml", content.replace("277699", "277700"))
    output, missing = audit.report(audit.scan(tmp_path))
    assert "CONFLICT: rainbow-princess-art/enemies/guardian-bellkeeper" in output
    assert missing > 0


def test_non_gameplay_gen2_planes_not_reported(tmp_path):
    write_ledger(
        tmp_path,
        "GEN2-ROUND-2.yaml",
        """- key: x1-sky
  entity: stage-plane
  stage: X1
  lane: krea2
  asset: rainbow-princess-art/scenery/x1-sky
  art: {krea2: {status: DONE, art_image_id: 252085}}
""",
    )
    assert audit.scan(tmp_path) == []


def test_bad_ledger_rejected(tmp_path):
    import pytest

    (tmp_path / "GEN2-BROKEN.yaml").write_text("subjects: {}\n")
    with pytest.raises(ValueError, match="expected a subjects list"):
        audit.scan(tmp_path)
