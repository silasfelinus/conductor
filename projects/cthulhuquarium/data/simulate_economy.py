#!/usr/bin/env python3
"""
simulate_economy.py -- simulate the first two hours of Cthulhuquarium play
against data/economy.yaml's numbers, so ECONOMY.md's curve is a simulated
result rather than a guess (per cthulhuquarium/t-004's own task note: "a spec
nobody simulated is a guess").

Runs two scenarios side by side, both starting from one COMMON fish and zero
coins:

  active -- a player who periodically feeds a hungry fish, clicks down
            debris, and buys the next affordable fish when a slot is free.
  idle   -- the same starting tank, left alone: no feeding, no clicking, no
            buying, for the full two hours.

The point of the comparison is DESIGN-BRIEF.md's MVP requirement 6: offline/
idle income must be rewarding but strictly worse than active play. This
script's job is to confirm that's actually true of the numbers in
economy.yaml, not just asserted in prose.

Usage:
    python3 projects/cthulhuquarium/data/simulate_economy.py
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass, field

import yaml

ECONOMY_PATH = pathlib.Path(__file__).parent / "economy.yaml"
TICKS = 120  # 2 hours at 60s/tick
CHECKPOINT_EVERY = 10  # print a row every 10 ticks (10 minutes)


def band_multiplier(bands: list[dict], value: float) -> float:
    """bands is a list of {min, multiplier}, sorted high-to-low min in the
    YAML; pick the first band whose min the value meets or exceeds."""
    for band in bands:
        if value >= band["min"]:
            return band["multiplier"]
    return 0.0


@dataclass
class Fish:
    tier: str
    hunger: float = 100.0


@dataclass
class TankState:
    coins: float = 0.0
    debris: float = 0.0
    fish: list = field(default_factory=list)
    slots_cap: int = 4
    gross_income_earned: float = 0.0  # cumulative production, ignoring spend -- the real "how much did this play style produce" number
    asset_value: float = 0.0  # sum of unlock_cost for every fish owned -- coins converted into a fish aren't lost, they're invested


def run(econ: dict, active: bool) -> list[dict]:
    tiers = econ["rarity_tiers"]
    hunger_cfg = econ["hunger"]
    debris_cfg = econ["debris"]

    tank = TankState(fish=[Fish(tier="COMMON")])
    rows = []

    for tick in range(1, TICKS + 1):
        # 1. production
        debris_mult = band_multiplier(debris_cfg["production_multiplier_by_band"], tank.debris)
        total_income = 0.0
        for f in tank.fish:
            base = tiers[f.tier]["income_per_tick"]
            hunger_mult = band_multiplier(hunger_cfg["production_multiplier_by_band"], f.hunger)
            total_income += base * hunger_mult * debris_mult
        tank.coins += total_income
        tank.gross_income_earned += total_income

        # 2. hunger decay
        for f in tank.fish:
            f.hunger = max(0.0, f.hunger - hunger_cfg["decay_per_tick"])

        # 3. debris accrual
        tank.debris = min(
            debris_cfg["range"][1],
            tank.debris + debris_cfg["accrual_per_occupant_per_tick"] * len(tank.fish),
        )

        if active:
            # 4a. feed the hungriest fish under 50 hunger, if affordable
            hungry = [f for f in tank.fish if f.hunger < 50]
            if hungry:
                target = min(hungry, key=lambda f: f.hunger)
                feed_cost = round(
                    tiers[target.tier]["unlock_cost"] * hunger_cfg["feed"]["cost_factor_of_unlock_cost"]
                )
                if tank.coins >= feed_cost:
                    tank.coins -= feed_cost
                    target.hunger = hunger_cfg["feed"]["restores_hunger_to"]

            # 4b. click debris down once per tick if it's built up
            if tank.debris > 20:
                tank.debris = max(0.0, tank.debris - debris_cfg["clean"]["click_clears"])

            # 4c. buy the next COMMON fish if a slot is free and affordable
            if len(tank.fish) < tank.slots_cap:
                cost = tiers["COMMON"]["unlock_cost"]
                if tank.coins >= cost:
                    tank.coins -= cost
                    tank.fish.append(Fish(tier="COMMON"))
                    tank.asset_value += cost

        if tick % CHECKPOINT_EVERY == 0:
            rows.append(
                {
                    "tick": tick,
                    "minute": tick,  # tick_seconds == 60, so tick count == minutes
                    "coins": round(tank.coins, 1),
                    "fish": len(tank.fish),
                    "avg_hunger": round(sum(f.hunger for f in tank.fish) / len(tank.fish), 1),
                    "debris": round(tank.debris, 1),
                    "gross_income": round(tank.gross_income_earned, 1),
                    "net_worth": round(tank.coins + tank.asset_value, 1),
                }
            )

    return rows


def main() -> None:
    with open(ECONOMY_PATH) as fh:
        econ = yaml.safe_load(fh)

    active_rows = run(econ, active=True)
    idle_rows = run(econ, active=False)

    print("| minute | active: coins | active: fish | active: net worth | active: gross income "
          "| idle: coins | idle: fish | idle: net worth | idle: gross income |")
    print("|---|---|---|---|---|---|---|---|---|")
    for a, i in zip(active_rows, idle_rows):
        print(
            f"| {a['minute']} | {a['coins']} | {a['fish']} | {a['net_worth']} | {a['gross_income']} "
            f"| {i['coins']} | {i['fish']} | {i['net_worth']} | {i['gross_income']} |"
        )

    final_active = active_rows[-1]
    final_idle = idle_rows[-1]
    nw_ratio = final_active["net_worth"] / final_idle["net_worth"] if final_idle["net_worth"] else float("inf")
    gross_ratio = final_active["gross_income"] / final_idle["gross_income"] if final_idle["gross_income"] else float("inf")
    print()
    print(f"After {TICKS} minutes: active net worth={final_active['net_worth']} vs idle={final_idle['net_worth']} "
          f"(ratio {nw_ratio:.2f}x); active gross income earned={final_active['gross_income']} vs "
          f"idle={final_idle['gross_income']} (ratio {gross_ratio:.2f}x)")


if __name__ == "__main__":
    main()
