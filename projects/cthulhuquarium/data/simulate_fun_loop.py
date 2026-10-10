#!/usr/bin/env python3
"""
simulate_fun_loop.py -- pace check for the m4 "fun loop first" economy
(cthulhuquarium/t-079, LOOP.md).

Simulates one attentive player second by second against the `fun_loop`
block of data/economy.yaml: every fish drops a coin on its own timer, the
player clicks a share of them (capped by how fast a human can click), feeds
the tank when it gets hungry, and spends greedily:

  1. a free slot and an affordable fish -> buy the best tier it can afford
     (the cheapest tier whose payback is no worse than COMMON's);
  2. a full tank and an affordable expansion -> buy the expansion;
  3. a full tank, no expansion affordable, and a higher tier affordable after
     releasing the worst fish -> release it (flat refund) and buy up.

It prints the moments LOOP.md's pacing targets name (second fish, a dozen
fish, a full tank) and a 10-minute table, so the targets are simulated
results rather than hopes.

Usage:
    python3 projects/cthulhuquarium/data/simulate_fun_loop.py
"""

from __future__ import annotations

import pathlib

import yaml

ECONOMY_PATH = pathlib.Path(__file__).parent / "economy.yaml"
SECONDS = 2 * 60 * 60
TIERS = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"]


def main() -> None:
    econ = yaml.safe_load(ECONOMY_PATH.read_text())
    loop = econ["fun_loop"]
    tiers = econ["rarity_tiers"]
    drop_s = loop["coin_drop_seconds_per_fish"]
    coin_value = loop["coin_value_by_tier"]
    max_cps = loop["sim_max_clicks_per_second"]
    click_share = loop["sim_click_share"]
    feed_factor = loop["feed_cost_factor_of_unlock_cost"]
    release_factor = loop["release_refund_factor_of_unlock_cost"]
    cap = loop["starting_fish_slots"]
    expansions = list(loop["tank_expansions"])

    coins = float(loop["starting_coins"])
    fish: list[dict] = [{"tier": "COMMON", "hunger": 100.0}]
    events: dict[str, int] = {}
    rows = []

    def cost(tier: str) -> int:
        return tiers[tier]["unlock_cost"]

    def best_affordable(budget: float) -> str | None:
        pick = None
        for tier in TIERS:
            if cost(tier) <= budget:
                pick = tier
        return pick

    for t in range(1, SECONDS + 1):
        drops_per_s = len(fish) / drop_s
        share = min(click_share, max_cps / drops_per_s) if drops_per_s else 0
        for f in fish:
            if f["hunger"] <= 0:
                continue
            coins += share * coin_value[f["tier"]] / drop_s
        if t % 60 == 0:
            for f in fish:
                f["hunger"] = max(0.0, f["hunger"] - 1)
            hungry = [f for f in fish if f["hunger"] < 50]
            bill = sum(max(1, round(cost(f["tier"]) * feed_factor)) for f in hungry)
            if hungry and coins >= bill:
                coins -= bill
                for f in hungry:
                    f["hunger"] = 100.0

        if len(fish) < cap:
            tier = best_affordable(coins)
            if tier:
                coins -= cost(tier)
                fish.append({"tier": tier, "hunger": 100.0})
        elif expansions and coins >= expansions[0]["cost"]:
            exp = expansions.pop(0)
            coins -= exp["cost"]
            cap += exp["slots"]
            events.setdefault(f"expansion to {cap}", t)
        elif fish:
            worst = min(fish, key=lambda f: TIERS.index(f["tier"]))
            refund = cost(worst["tier"]) * release_factor
            tier = best_affordable(coins + refund)
            if tier and TIERS.index(tier) > TIERS.index(worst["tier"]):
                fish.remove(worst)
                coins += refund - cost(tier)
                fish.append({"tier": tier, "hunger": 100.0})

        n = len(fish)
        for label, target in (("second fish", 2), ("a dozen fish", 12), ("25 fish", 25), ("40 fish", 40)):
            if n >= target:
                events.setdefault(label, t)
        if t % 600 == 0:
            mix = {tier: sum(1 for f in fish if f["tier"] == tier) for tier in TIERS}
            rows.append((t // 60, n, cap, round(coins), round(len(fish) / drop_s, 2), mix))

    print("Pacing (minutes:seconds after the first fish):")
    for label, t in sorted(events.items(), key=lambda kv: kv[1]):
        print(f"  {label:<22} {t // 60:>3}:{t % 60:02d}")
    print()
    print(f"{'min':>4} {'fish':>5} {'slots':>5} {'coins':>8} {'drops/s':>8}  mix")
    for minute, n, slots, c, dps, mix in rows:
        compact = " ".join(f"{k[0]}{v}" for k, v in mix.items() if v)
        print(f"{minute:>4} {n:>5} {slots:>5} {c:>8} {dps:>8}  {compact}")


if __name__ == "__main__":
    main()
