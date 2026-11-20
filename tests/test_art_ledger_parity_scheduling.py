"""Guard the exhaustive art-ledger loader regression's CI scheduling split."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_art_ledger_parity_is_exhaustive_but_not_every_pr():
    ci = (ROOT / ".github/workflows/ci.yml").read_text()
    daily = (ROOT / ".github/workflows/art-ledger-loader-parity.yml").read_text()
    config = (ROOT / "pytest.ini").read_text()
    test = (ROOT / "tests/test_sweep_art_ledgers.py").read_text()

    assert 'pytest -m "not art_parity" tests/ --durations=10' in ci
    assert "@pytest.mark.art_parity" in test
    assert "art_parity:" in config
    assert "schedule:" in daily
    assert "workflow_dispatch:" in daily
    assert (
        "pytest -q -m art_parity tests/test_sweep_art_ledgers.py --durations=3"
        in daily
    )
    assert "yaml.SafeLoader" in test
    assert "fast_data == python_data" in test
