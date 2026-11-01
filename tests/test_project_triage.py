"""scripts/project_triage.py: lane heuristics and tiering stay honest."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("project_triage", ROOT / "scripts" / "project_triage.py")
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)


def lane(title, **kw):
    return triage.lane_of({"title": title, "status": kw.pop("status", "ready"), **kw})


def test_lanes():
    assert lane("Deliver unique mission outcome, conversation and ending illustration coverage") == "art"
    assert lane("Pre-generate and verify curated 4,000 launch hybrids") == "art"
    assert lane("Accept user-submitted ingredient images securely") == "build"
    assert lane("Act II story and art pass: Days 11-20 quests") == "build"
    assert lane("Reward-layer adversarial QA across all endings", status="waiting") == "qa"
    assert lane("FINAL HUMAN GATE ONLY: approve the final design", status="waiting") == "human"
    assert lane("Anything", gate_human=True) == "human"
    assert lane("Some feature", status="review") == "review"
    assert lane("Zuzu Gamebook | Master completion roadmap") is None
    assert lane("Grow the fish roster", lane="art") == "art"


def test_triage_runs_on_live_roadmaps():
    rows = triage.triage()
    assert rows, "expected at least one active project"
    for r in rows:
        assert r["tier"] == ("A" if r["lanes"]["build"] == 0 else "B" if r["lanes"]["build"] <= 2 else "C")
