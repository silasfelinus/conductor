from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "projects" / "animation-manager" / "roadmap.yaml"
PITCHES = ROOT / "projects" / "animation-manager" / "PITCHES.yaml"


def test_daily_completion_has_matching_release_ledger_entry():
    roadmap = yaml.safe_load(ROADMAP.read_text(encoding="utf-8")) or {}
    task = next(
        task
        for task in roadmap.get("tasks", [])
        if isinstance(task, dict) and task.get("id") == "t-007"
    )
    completed = date.fromisoformat(str(task["daily_last_completed"]))

    pitches = yaml.safe_load(PITCHES.read_text(encoding="utf-8")) or {}
    releases = []
    for pitch in pitches.get("pitches", []):
        if not isinstance(pitch, dict):
            continue
        for build in pitch.get("builds") or []:
            if not isinstance(build, dict) or not build.get("released_at"):
                continue
            released = str(build["released_at"])
            releases.append((date.fromisoformat(released[:10]), pitch.get("id")))

    assert releases, "Animation Manager has no machine-readable release provenance"
    latest_date, latest_id = max(releases)
    assert latest_date >= completed, (
        "animation-manager/t-007 says a new screensaver completed on "
        f"{completed}, but the newest PITCHES.yaml released_at is "
        f"{latest_date} ({latest_id}); record the shipped build in the release ledger "
        "in the same cycle that daily_last_completed advances"
    )
