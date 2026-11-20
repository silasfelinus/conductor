"""Regression coverage for the art receipt signal in the startup health report."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_auto_art_receipts_is_visible_in_session_sweep():
    spec = importlib.util.spec_from_file_location(
        "session_sweep", ROOT / "scripts" / "session_sweep.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    checks = [check for check in module.CHECKS if check[0] == "auto_art_receipts"]
    assert len(checks) == 1
    name, argv, needs_network, always_show = checks[0]
    assert name == "auto_art_receipts"
    assert argv == ["scripts/check_auto_art_receipts.py"]
    assert needs_network is False
    assert always_show is False
    assert (ROOT / argv[0]).is_file()
