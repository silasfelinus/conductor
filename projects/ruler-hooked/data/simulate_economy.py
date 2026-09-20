#!/usr/bin/env python3
"""
simulate_economy.py -- simulate coin accrual from fishing against
data/economy.yaml's numbers, so the shop's pacing is a simulated result
rather than a guess (ruler-hooked/t-034, kaizen from t-029: "costs/odds
are a first-pass guess", following Cthulhuquarium's simulate_economy.py
precedent).

Deterministic, not Monte Carlo -- same house style as Cthulhuquarium's
sim: every rarity tier contributes its EXPECTED coin value per turn
(draw-weight-share * treasure chance * average payout), so the curve
below is the long-run average a real weighted-random player converges
to, not one noisy rollout. See economy.yaml's `fishing.turn_definition`
comment for exactly what one "turn" means here (one resolved catch, not
one cast attempt -- escape/miss rate isn't a modeled number anywhere in
the live game).

Usage:
    python3 projects/ruler-hooked/data/simulate_economy.py
    python3 projects/ruler-hooked/data/simulate_economy.py --check-drift
        Compare this file's copied numbers against the live TypeScript in
        a kind_robots checkout (default: ../../../kind_robots relative to
        this repo's root, override with --kind-robots-path). Exits 1 on
        any mismatch instead of printing the simulation, so a future
        economy.ts edit that isn't hand-synced here fails loudly rather
        than silently going stale.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ECONOMY_PATH = pathlib.Path(__file__).parent / "economy.yaml"
TURNS = 300
CHECKPOINT_EVERY = 20


def expected_coins_per_turn(econ: dict) -> float:
    """Expected coin value of one resolved catch, averaged across rarity
    tiers by draw-weight share (see economy.yaml's rarity_draw_weights
    comment for what this approximates and what it deliberately ignores)."""
    weights = econ["rarity_draw_weights"]
    treasure = econ["treasure_by_rarity"]
    total_weight = sum(weights.values())
    expected = 0.0
    for rarity, weight in weights.items():
        t = treasure[rarity]
        avg_payout = (t["min"] + t["max"]) / 2
        expected += (weight / total_weight) * t["chance"] * avg_payout
    return expected


def turns_to_afford(cost: float, income_per_turn: float) -> int:
    if income_per_turn <= 0:
        return -1
    import math

    return math.ceil(cost / income_per_turn)


def run_curve(income_per_turn: float) -> list[dict]:
    rows = []
    coins = 0.0
    for turn in range(1, TURNS + 1):
        coins += income_per_turn
        if turn % CHECKPOINT_EVERY == 0:
            rows.append({"turn": turn, "coins": round(coins, 1)})
    return rows


def check_drift(kind_robots_path: pathlib.Path, econ: dict) -> list[str]:
    """Best-effort regex extraction of the live TypeScript numbers this
    file mirrors, compared against economy.yaml. Not a TS parser -- if the
    source shape changes enough to break these patterns, that mismatch
    itself is worth a human's attention, so this reports it as a drift
    finding rather than crashing silently."""
    problems: list[str] = []

    economy_ts = kind_robots_path / "utils" / "rulerHooked" / "economy.ts"
    fish_ts = kind_robots_path / "utils" / "rulerHooked" / "fish.ts"
    if not economy_ts.exists() or not fish_ts.exists():
        return [f"kind_robots checkout not found at {kind_robots_path} (looked for economy.ts / fish.ts)"]

    economy_src = economy_ts.read_text()
    fish_src = fish_ts.read_text()

    # rarity_draw_weights vs rarityWeight
    m = re.search(r"const rarityWeight: Record<Rarity, number> = \{(.*?)\}", fish_src, re.S)
    if m:
        live_weights = dict(re.findall(r"(\w+):\s*(\d+)", m.group(1)))
        for rarity, weight in econ["rarity_draw_weights"].items():
            live = live_weights.get(rarity)
            if live is None:
                problems.append(f"rarityWeight: {rarity} not found in fish.ts")
            elif int(live) != weight:
                problems.append(f"rarityWeight[{rarity}]: economy.yaml has {weight}, fish.ts has {live}")
    else:
        problems.append("could not locate rarityWeight table in fish.ts")

    # treasure_by_rarity vs TREASURE_BY_RARITY
    m = re.search(r"TREASURE_BY_RARITY: Record<Rarity, TreasureRoll> = \{(.*?)\n\}", economy_src, re.S)
    if m:
        for rarity, expected in econ["treasure_by_rarity"].items():
            row = re.search(
                rf"{rarity}:\s*\{{\s*chance:\s*([\d.]+),\s*min:\s*(\d+),\s*max:\s*(\d+)\s*\}}",
                m.group(1),
            )
            if not row:
                problems.append(f"TREASURE_BY_RARITY: {rarity} not found in economy.ts")
                continue
            live_chance, live_min, live_max = float(row.group(1)), int(row.group(2)), int(row.group(3))
            if (live_chance, live_min, live_max) != (expected["chance"], expected["min"], expected["max"]):
                problems.append(
                    f"TREASURE_BY_RARITY[{rarity}]: economy.yaml has "
                    f"{expected}, economy.ts has chance={live_chance} min={live_min} max={live_max}"
                )
    else:
        problems.append("could not locate TREASURE_BY_RARITY table in economy.ts")

    # gear_catalog / kingdom_catalog costs, by id
    for catalog_key, ts_const in (("gear_catalog", "GEAR_CATALOG"), ("kingdom_catalog", "KINGDOM_CATALOG")):
        m = re.search(rf"{ts_const}[^=]*=\s*\[(.*?)\n\]", economy_src, re.S)
        if not m:
            problems.append(f"could not locate {ts_const} in economy.ts")
            continue
        block = m.group(1)
        for item in econ[catalog_key]:
            entry = re.search(rf"id:\s*'{re.escape(item['id'])}'.*?cost:\s*(\d+)", block, re.S)
            if not entry:
                problems.append(f"{ts_const}: id '{item['id']}' not found in economy.ts")
            elif int(entry.group(1)) != item["cost"]:
                problems.append(
                    f"{ts_const}[{item['id']}].cost: economy.yaml has {item['cost']}, "
                    f"economy.ts has {entry.group(1)}"
                )

    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--check-drift",
        action="store_true",
        help="Compare economy.yaml against the live kind_robots TypeScript instead of simulating.",
    )
    parser.add_argument(
        "--kind-robots-path",
        default=str(pathlib.Path(__file__).resolve().parents[4] / "kind_robots"),
        help="Path to a kind_robots checkout (default: sibling checkout next to this conductor repo).",
    )
    args = parser.parse_args()

    with open(ECONOMY_PATH) as fh:
        econ = yaml.safe_load(fh)

    if args.check_drift:
        problems = check_drift(pathlib.Path(args.kind_robots_path), econ)
        if problems:
            print(f"DRIFT: economy.yaml is out of sync with kind_robots ({len(problems)} finding(s)):")
            for p in problems:
                print(f"  - {p}")
            sys.exit(1)
        print("No drift -- economy.yaml matches the live kind_robots TypeScript.")
        return

    income_per_turn = expected_coins_per_turn(econ)
    print(f"Expected coins per turn (one resolved catch): {income_per_turn:.4f}")
    print()

    rows = run_curve(income_per_turn)
    print("| turn | cumulative coins |")
    print("|---|---|")
    for row in rows:
        print(f"| {row['turn']} | {row['coins']} |")

    print()
    print("Turns to afford each shop item (from zero, ignoring other spending):")
    for catalog_key, label in (("gear_catalog", "Gear"), ("kingdom_catalog", "Kingdom")):
        for item in econ[catalog_key]:
            turns = turns_to_afford(item["cost"], income_per_turn)
            print(f"  [{label}] {item['name']} (cost {item['cost']}): {turns} turns")

    all_gear_cost = sum(i["cost"] for i in econ["gear_catalog"])
    all_kingdom_cost = sum(i["cost"] for i in econ["kingdom_catalog"])
    everything_cost = all_gear_cost + all_kingdom_cost
    print()
    print(f"All gear ({all_gear_cost} coins): {turns_to_afford(all_gear_cost, income_per_turn)} turns")
    print(f"All kingdom items ({all_kingdom_cost} coins): {turns_to_afford(all_kingdom_cost, income_per_turn)} turns")
    print(f"Everything ({everything_cost} coins): {turns_to_afford(everything_cost, income_per_turn)} turns")


if __name__ == "__main__":
    main()
