#!/usr/bin/env python3
"""
simulate_descent.py -- pace check for the descent (cthulhuquarium/t-102).

The fun loop (simulate_fun_loop.py) counts fish; the descent counts *species
known*, because that is what opens each floor of the building (10 / 25 / 50 /
95 known, kind_robots utils/cthulhuquariumFloors.ts). This simulates one
attentive collector second by second against the real roster:

  * every species from the canon bible (fish/*.yaml), priced the way the server
    prices it: its own unlock_cost, or -- for a species reached only by
    evolution, whose canon price is 0 -- its rarity's default, where rarity is
    the highest of its six stat rarities (aquariumEconomy.ts
    deriveFishRarityTier, luck = the bible's rarity);
  * each fish drops coin_value_by_tier[rarity] every coin_drop_seconds_per_fish,
    and the player clicks sim_click_share of them (capped per second);
  * strategy: with room, buy the cheapest species not yet known on an open floor;
    with a full tank, buy the next expansion if affordable, else release the
    least valuable fish when that lets a new species in.

It prints when each floor opens and when the book fills, so the floor
thresholds are checked against a simulated player, not hoped for.

Usage:
    python3 projects/cthulhuquarium/data/simulate_descent.py [path/to/canon/fish] [--canon-rarity]

--canon-rarity prices and pays each species by its canon `rarity` (the value the
book shows) instead of the highest stat rarity the server uses today, which is
what LOOP.md's coin_value_by_tier numbers were written against.
"""

from __future__ import annotations

import pathlib
import sys

import yaml

ECONOMY_PATH = pathlib.Path(__file__).parent / "economy.yaml"
TIERS = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"]
FLOORS = [(1, 0), (2, 10), (3, 25), (4, 50), (5, 95)]
HOURS = 12


def roster(fish_dir: pathlib.Path, defaults: dict[str, int], canon_rarity: bool = False) -> list[dict]:
    out = []
    for path in sorted(fish_dir.glob("*.yaml")):
        fish = yaml.safe_load(path.read_text())
        stats = dict(fish.get("stats") or {})
        stats["luck"] = fish["rarity"]
        rarity = fish["rarity"] if canon_rarity else max(
            (stats.get(k, "COMMON") for k in ("charm", "empathy", "grace", "luck", "might", "wits")),
            key=TIERS.index)
        evo_only = fish.get("unlock_cost") == 0 and bool(fish.get("evolves_from"))
        cost = defaults[rarity] if evo_only else int(fish.get("unlock_cost") or 0)
        out.append({"slug": fish["slug"], "tier": int(fish["tier"]), "rarity": rarity, "cost": cost})
    return out


def open_floor(known: int) -> int:
    return max(floor for floor, at in FLOORS if known >= at)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    canon_rarity = "--canon-rarity" in sys.argv
    fish_dir = pathlib.Path(args[0]) if args else (
        pathlib.Path(__file__).resolve().parents[4] / "cthulhuquarium" / "fish")
    econ = yaml.safe_load(ECONOMY_PATH.read_text())
    loop = econ["fun_loop"]
    defaults = {t: econ["rarity_tiers"][t]["unlock_cost"] for t in TIERS}
    species = roster(fish_dir, defaults, canon_rarity)
    drop_s = loop["coin_drop_seconds_per_fish"]
    value = loop["coin_value_by_tier"]
    share_cap, max_cps = loop["sim_click_share"], loop["sim_max_clicks_per_second"]
    refund = loop["release_refund_factor_of_unlock_cost"]
    cap = loop["starting_fish_slots"]
    expansions = list(loop["tank_expansions"])

    coins = float(loop["starting_coins"])
    known: set[str] = set()
    tank: list[dict] = []
    events: dict[str, int] = {}

    def buy(sp: dict) -> None:
        nonlocal coins
        coins -= sp["cost"]
        tank.append(sp)
        before = open_floor(len(known))
        known.add(sp["slug"])
        after = open_floor(len(known))
        if after > before:
            events.setdefault(f"floor {after} opens ({len(known)} known)", t)
        for target in (10, 25, 50, 95, len(species)):
            if len(known) >= target:
                events.setdefault(f"{target} species known", t)

    for t in range(1, HOURS * 3600 + 1):
        drops = len(tank) / drop_s
        share = min(share_cap, max_cps / drops) if drops else 0
        coins += sum(share * value[f["rarity"]] / drop_s for f in tank)
        floor = open_floor(len(known))
        candidates = sorted((s for s in species if s["slug"] not in known and s["tier"] <= floor),
                            key=lambda s: s["cost"])
        nxt = candidates[0] if candidates else None
        if nxt and len(tank) < cap and coins >= nxt["cost"]:
            buy(nxt)
        elif len(tank) >= cap and expansions and coins >= expansions[0]["cost"]:
            cap += expansions.pop(0)["slots"]
            events.setdefault(f"expansion to {cap}", t)
        elif nxt and len(tank) >= cap:
            worst = min(tank, key=lambda f: value[f["rarity"]])
            if coins + worst["cost"] * refund >= nxt["cost"] and value[worst["rarity"]] <= value[nxt["rarity"]]:
                tank.remove(worst)
                coins += worst["cost"] * refund
                buy(nxt)
        if len(known) == len(species):
            break

    print(f"{len(species)} species; collector strategy; {HOURS}h cap; "
          f"rarity by {'canon rarity' if canon_rarity else 'highest stat (server today)'}")
    for label, at in sorted(events.items(), key=lambda kv: kv[1]):
        if label.startswith("expansion"):
            continue
        print(f"  {label:<28} {at // 3600:>2}h{(at % 3600) // 60:02d}m")
    print(f"  known at end: {len(known)}  tank: {len(tank)}/{cap}  coins: {round(coins)}")


if __name__ == "__main__":
    main()
