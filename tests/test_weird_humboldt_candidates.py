from pathlib import Path

from scripts import validate_weird_humboldt_candidates as v


def test_candidates_validate():
    for f in sorted(v.CAND_DIR.glob("*.yaml")):
        assert v.validate(f) == []


def test_validator_flags_bad_record(tmp_path):
    p = tmp_path / "x.yaml"
    p.write_text("publish: true\nart_enqueue: false\ncandidates:\n- id: X\n  title: t\n  axis: nope\n")
    errs = v.validate(p)
    assert any("publish" in e for e in errs) and any("axis" in e for e in errs)
