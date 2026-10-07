"""zuzu-showdown t-018: matchups.yaml stays complete and every line keeps to the rules."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "projects" / "zuzu-showdown" / "tools" / "check_matchups.py"


def load():
    spec = importlib.util.spec_from_file_location("check_matchups", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_shipped_lines_are_complete_and_clean():
    assert load().main() == 0


def test_the_check_catches_a_missing_pair_a_long_line_and_a_banned_term():
    check = load().check
    roster = ["zuzu", "river-croc"]
    matchups = {
        "matchups": [
            {
                "pair": ["zuzu", "river-croc"],
                "intro": [
                    {"speaker": "river-croc", "line": "HSSSS."},
                    {"speaker": "zuzu", "line": "Not today, all of you people."},
                ],
                "win": {"zuzu": "...", "river-croc": "I talk now. " + "x" * 60},
            },
        ],
        "boss": {"intro": {"zuzu": "..."}},
    }
    errors = "\n".join(check(matchups, roster))
    assert "('zuzu', 'zuzu'): 0 entries" in errors
    assert "('river-croc', 'river-croc'): 0 entries" in errors
    assert "banned term 'people'" in errors
    assert "zuzu says more than three words" in errors
    assert "river-croc speaks words" in errors
    assert "chars:" in errors
    assert "boss: no intro line for river-croc" in errors
