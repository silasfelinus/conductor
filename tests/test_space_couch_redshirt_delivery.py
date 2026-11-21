"""Regression tests for the Space Couch redshirt delivery audit."""
import importlib.util
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "audit_space_couch_redshirt_delivery.py"
spec = importlib.util.spec_from_file_location("redshirt_audit", MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def write_webp(root: Path, kind: str, number: int, valid: bool = True) -> None:
    path = root / f"public/game-of-captains/redshirts/{kind}/rs-{number:03d}.webp"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"RIFF" + b"\x10\x00\x00\x00" + b"WEBP" + b"VP8 " + b"payload"
        if valid else b"not a webp"
    )


def test_empty_checkout_reports_all_missing(tmp_path):
    result = audit.inspect(tmp_path)
    assert result["total"] == 200
    assert result["delivered_count"] == 0
    assert len(result["missing"]) == 200
    assert not result["complete"]


def test_rejects_corrupt_and_truncated_files(tmp_path):
    write_webp(tmp_path, "portraits", 1)
    write_webp(tmp_path, "secret-powers", 1, valid=False)
    result = audit.inspect(tmp_path)
    assert result["delivered_count"] == 1
    assert len(result["invalid"]) == 1
    assert len(result["missing"]) == 198
    assert not result["complete"]


def test_complete_requires_both_images_for_every_redshirt(tmp_path):
    for kind in audit.KINDS:
        for number in range(1, 101):
            write_webp(tmp_path, kind, number)
    result = audit.inspect(tmp_path)
    assert result["delivered_count"] == 200
    assert result["complete"]
    assert result["missing"] == []
    assert result["invalid"] == []
