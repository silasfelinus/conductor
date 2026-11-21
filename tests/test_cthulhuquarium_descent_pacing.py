"""Pin the Cthulhuquarium descent pacing (cthulhuquarium/t-106).

economy.yaml `floor_keys` (150 / 3,000 / 30,000 / 400,000) were tuned with
data/simulate_descent.py to Silas's 2026-11-21 targets for a casual player (two
10-minute visits a day): floor II on day 1, III on day 1-2, IV on day 3-5, V
within week 1-2 (t-105). Nothing asserted either the result or that kind_robots
mirrors the prices, so a change to one could drift silently.

The roster is a committed snapshot (data/descent_roster.json; regenerate with
`simulate_descent.py <canon>/fish --write-roster data/descent_roster.json`)
because CI has no canon checkout.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "projects/cthulhuquarium/data"


def _simulator():
    spec = importlib.util.spec_from_file_location("simulate_descent", DATA / "simulate_descent.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _floor_keys() -> dict[int, int]:
    econ = yaml.safe_load((DATA / "economy.yaml").read_text())
    return {int(k): int(v) for k, v in econ["floor_keys"].items()}


def test_roster_snapshot_is_the_whole_book():
    roster = json.loads((DATA / "descent_roster.json").read_text())
    assert len(roster) == 151
    assert {fish["tier"] for fish in roster} == {1, 2, 3, 4, 5}
    # The free starters ("the first one is on the house") are floor I commons.
    free = [fish for fish in roster if fish["cost"] <= 0]
    assert all(fish["tier"] == 1 for fish in free) and len(free) <= 3, free


def test_casual_player_opens_each_floor_on_schedule():
    sim = _simulator()
    econ = yaml.safe_load((DATA / "economy.yaml").read_text())
    roster = json.loads((DATA / "descent_roster.json").read_text())
    result = sim.simulate(roster, econ, "casual", 21, _floor_keys())
    day = {label: minutes / (24 * 60) + 1 for label, minutes in result["events"].items()}
    # Day numbers are 1-based: day 1 is the first day of play.
    assert day.get("floor 2 opens", 99) < 2, "floor II in the first day"
    assert day.get("floor 3 opens", 99) < 3, "floor III by day 2"
    assert 3 <= day.get("floor 4 opens", 99) < 6, "floor IV on day 3-5"
    assert 7 <= day.get("floor 5 opens", 99) < 16, "floor V within week 1-2"


def test_kind_robots_mirrors_the_key_prices():
    floors = ROOT.parent / "kind_robots/utils/cthulhuquariumFloors.ts"
    if not floors.exists():
        pytest.skip("kind_robots is not checked out next to conductor")
    block = re.search(r"FLOOR_KEY_COSTS[^=]*=\s*\{([^}]*)\}", floors.read_text())
    assert block, "FLOOR_KEY_COSTS found"
    mirrored = {int(k): int(v.replace("_", "")) for k, v in re.findall(r"(\d)\s*:\s*([\d_]+)", block.group(1))}
    assert mirrored == _floor_keys()
