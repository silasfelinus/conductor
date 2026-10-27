"""Daily playbook pitches carry authored design prompts from 2026-10-27."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from daily_playbook_challenge import brief, design_errors

PROMPT = (
    "A small brass lighthouse on a moonlit shoal, its keeper waving a lantern at a fishing boat "
    "while gulls circle in silver light."
)


def good(n=4):
    return [{"kind": "place", "title": f"Design {i}", "prompt": PROMPT} for i in range(n)]


def test_designs_optional_before_the_cutover():
    assert design_errors("pitch 1", {}, "2026-10-26") == []


def test_designs_required_from_the_cutover():
    assert design_errors("pitch 1", {}, "2026-10-27")
    assert design_errors("pitch 1", {"designs": good(3)}, "2026-10-27")
    assert design_errors("pitch 1", {"designs": good(4)}, "2026-10-27") == []


def test_prompts_are_pictures_not_titles():
    bad = good()
    bad[0] = {"kind": "other", "title": "Key art", "prompt": PROMPT + " The title Moon Laundry across the top."}
    assert any("lettering" in e for e in design_errors("pitch 1", {"designs": bad}, "2026-10-27"))
    short = good()
    short[1] = {"kind": "villain", "title": "Villain", "prompt": "A villain."}
    assert any("plain prose" in e for e in design_errors("pitch 1", {"designs": short}, "2026-10-27"))
    odd = good()
    odd[2] = {"kind": "spaceship", "title": "Ship", "prompt": PROMPT}
    assert any("kind must be" in e for e in design_errors("pitch 1", {"designs": odd}, "2026-10-27"))


def test_brief_asks_for_designs():
    assert "DESIGNS" in brief("2026-10-27")
