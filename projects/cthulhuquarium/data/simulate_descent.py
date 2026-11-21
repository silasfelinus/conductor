#!/usr/bin/env python3
"""
simulate_descent.py -- pace check for the descent (cthulhuquarium/t-102, t-105).

The fun loop (simulate_fun_loop.py) counts fish; the descent counts *species
known*, because that is what opens each floor of the building (10 / 25 / 50 /
95 known, kind_robots utils/cthulhuquariumFloors.ts), together with the floor's
key, which Charlotte sells once the threshold is met (economy.yaml
`floor_keys`, Silas 2026-11-21: "canon rarity + slower floors").

It simulates whole days of play for three kinds of player against the real
roster (the canon fish/*.yaml):

  active  one 60-minute session a day, clicking 80% of coins
  casual  two 10-minute sessions a day
  idle    two 3-minute check-ins a day, clicking a few coins

Each fish is priced and paid by its canon `rarity`, as the server does since
t-105: its own unlock_cost, or -- for a species reached only by evolution,
whose canon price is 0 -- the rarity's default. In a session every fed fish
drops a coin_value_by_tier coin every coin_drop_seconds_per_fish, the player
clicks a share of them, and the tank also settles its passive income
(incomePerTick per minute at the 0.5x rate). Between sessions the tank keeps
settling at 0.5x until its fish go hungry (hunger falls 1 a minute from 100;
income bands 1.0 / 0.5 / 0.2 / 0), so a long absence pays about 70 minutes of
half-rate income, never more than the 8 hour cap.

Strategy (a collector): feed the tank at the start of each session; buy a
floor's key as soon as it is affordable; with room, buy the cheapest species
not yet known on an open floor; with a full tank, buy the next expansion, or
release the least valuable fish to let a new species in.

Usage:
    python3 projects/cthulhuquarium/data/simulate_descent.py [path/to/canon/fish] [--stat-rarity] [--days N]

--stat-rarity reproduces the pre-t-105 server (highest stat rarity) for comparison.
"""

from __future__ import annotations

import pathlib
import sys

import yaml

ECONOMY_PATH = pathlib.Path(__file__).parent / "economy.yaml"
TIERS = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC"]
THRESHOLDS = {1: 0, 2: 10, 3: 25, 4: 50, 5: 95}
INCOME_PER_MIN = {"COMMON": 1, "UNCOMMON": 3, "RARE": 8, "EPIC": 20, "LEGENDARY": 50, "MYTHIC": 120}
PLAYERS = {
    # name: (sessions per day, minutes each, click share, max clicks per second)
    "active": (1, 60, 0.8, 1.5),
    "casual": (2, 10, 0.8, 1.5),
    "idle": (2, 3, 0.3, 0.5),
}


def roster(fish_dir: pathlib.Path, defaults: dict[str, int], stat_rarity: bool) -> list[dict]:
    out = []
    for path in sorted(fish_dir.glob("*.yaml")):
        fish = yaml.safe_load(path.read_text())
        if stat_rarity:
            stats = dict(fish.get("stats") or {})
            stats["luck"] = fish["rarity"]
            rarity = max((stats.get(k, "COMMON") for k in ("charm", "empathy", "grace", "luck", "might", "wits")),
                         key=TIERS.index)
        else:
            rarity = fish["rarity"]
        evo_only = fish.get("unlock_cost") == 0 and bool(fish.get("evolves_from"))
        cost = defaults[rarity] if evo_only else int(fish.get("unlock_cost") or 0)
        out.append({"slug": fish["slug"], "tier": int(fish["tier"]), "rarity": rarity, "cost": cost})
    return out


def offline_minutes(gap_minutes: float) -> float:
    """Full-rate-equivalent minutes a fed tank earns over an absence (hunger bands)."""
    gap = min(gap_minutes, 8 * 60)
    full = min(gap, 50)
    half = min(max(gap - 50, 0), 30)
    fifth = min(max(gap - 80, 0), 19)
    return full + 0.5 * half + 0.2 * fifth


def simulate(species: list[dict], econ: dict, player: str, days: int, keys: dict[int, int]) -> dict:
    loop = econ["fun_loop"]
    drop_s = loop["coin_drop_seconds_per_fish"]
    value = loop["coin_value_by_tier"]
    feed_factor = loop["feed_cost_factor_of_unlock_cost"]
    refund = loop["release_refund_factor_of_unlock_cost"]
    sessions, minutes, share_cap, max_cps = PLAYERS[player]
    cap = loop["starting_fish_slots"]
    expansions = list(loop["tank_expansions"])
    coins = float(loop["starting_coins"])
    known: set[str] = set()
    held = {1}
    tank: list[dict] = []
    events: dict[str, float] = {}
    clock = 0.0  # minutes since the first session
    gap = 24 * 60 / sessions - minutes

    def open_floor() -> int:
        return max(f for f in held if len(known) >= THRESHOLDS[f])

    def note(label: str) -> None:
        events.setdefault(label, clock)

    for day in range(days):
        for s in range(sessions):
            if day or s:
                passive = offline_minutes(gap) * 0.5 * sum(INCOME_PER_MIN[f["rarity"]] for f in tank)
                coins += passive
                clock += gap
            coins -= sum(max(1, round(f["cost"] * feed_factor)) for f in tank)
            for _second in range(minutes * 60):
                clock += 1 / 60
                drops = len(tank) / drop_s
                share = min(share_cap, max_cps / drops) if drops else 0
                coins += sum(share * value[f["rarity"]] / drop_s + 0.5 * INCOME_PER_MIN[f["rarity"]] / 60
                             for f in tank)
                nxt_floor = max(held) + 1
                key_cost = keys.get(nxt_floor, 0)
                if nxt_floor in THRESHOLDS and len(known) >= THRESHOLDS[nxt_floor] and coins >= key_cost:
                    coins -= key_cost
                    held.add(nxt_floor)
                    note(f"floor {nxt_floor} opens")
                    continue
                floor = open_floor()
                candidates = sorted((sp for sp in species if sp["slug"] not in known and sp["tier"] <= floor),
                                    key=lambda sp: sp["cost"])
                nxt = candidates[0] if candidates else None
                saving_for_key = (nxt_floor in THRESHOLDS and len(known) >= THRESHOLDS[nxt_floor])
                if nxt and not saving_for_key and len(tank) < cap and coins >= nxt["cost"]:
                    coins -= nxt["cost"]
                    tank.append(nxt)
                    known.add(nxt["slug"])
                    if len(known) == len(species):
                        note("book complete")
                elif len(tank) >= cap and expansions and coins >= expansions[0]["cost"]:
                    cap += expansions.pop(0)["slots"]
                elif nxt and not saving_for_key and len(tank) >= cap:
                    worst = min(tank, key=lambda f: value[f["rarity"]])
                    if coins + worst["cost"] * refund >= nxt["cost"]:
                        tank.remove(worst)
                        coins += worst["cost"] * refund - nxt["cost"]
                        tank.append(nxt)
                        known.add(nxt["slug"])
                        if len(known) == len(species):
                            note("book complete")
            if len(known) == len(species):
                return {"events": events, "known": len(known)}
    return {"events": events, "known": len(known)}


def when(minutes: float | None) -> str:
    if minutes is None:
        return "not reached"
    days, rest = divmod(minutes, 24 * 60)
    return f"day {int(days) + 1}, {int(rest // 60)}h{int(rest % 60):02d}"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    stat_rarity = "--stat-rarity" in sys.argv
    days = 60
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
        args = [a for a in args if a != str(days)]
    fish_dir = pathlib.Path(args[0]) if args else (
        pathlib.Path(__file__).resolve().parents[4] / "cthulhuquarium" / "fish")
    econ = yaml.safe_load(ECONOMY_PATH.read_text())
    defaults = {t: econ["rarity_tiers"][t]["unlock_cost"] for t in TIERS}
    keys = {int(k): int(v) for k, v in (econ.get("floor_keys") or {}).items()}
    if "--keys" in sys.argv:  # e.g. --keys 2=150,3=2500,4=25000,5=250000 to try prices
        spec = sys.argv[sys.argv.index("--keys") + 1]
        keys = {int(k): int(v) for k, v in (pair.split("=") for pair in spec.split(","))}
        args = [a for a in args if a != spec]
    species = roster(fish_dir, defaults, stat_rarity)
    print(f"{len(species)} species; rarity by {'highest stat' if stat_rarity else 'canon rarity'}; "
          f"floor keys {keys or 'none'}")
    for player in PLAYERS:
        result = simulate(species, econ, player, days, keys)
        ev = result["events"]
        cells = [f"II {when(ev.get('floor 2 opens'))}", f"III {when(ev.get('floor 3 opens'))}",
                 f"IV {when(ev.get('floor 4 opens'))}", f"V {when(ev.get('floor 5 opens'))}",
                 f"book {when(ev.get('book complete'))}"]
        print(f"  {player:<7} " + " | ".join(cells) + f"  (known {result['known']})")


if __name__ == "__main__":
    main()
