#!/usr/bin/env python3
"""Build the curated, immutable launch-hybrid pair list for Hybridizer (hybridizer/t-007).

WHY THIS EXISTS. The Hybridizer launches with 4,000 pre-generated public hybrids so a first
visitor finds a populated specimen browser. The roadmap asks for coverage biased toward
strong, readable animal x animal and oddball combinations WITHOUT the 19,900-pair cross
product. This script picks that subset deterministically from the 200-starter catalogue:

* a short hand-picked showcase first (the pairs a visitor should see on day one);
* fixed per-category quotas (animal x animal dominates, every species/archetype pairing
  is included, fruit and oddity pairs are sprinkled in);
* within each category, pairs are chosen greedily by lowest current ingredient usage with a
  seeded tie-break, so every starter appears a similar number of times;
* the final order interleaves categories so each 50-pair batch shows variety.

The output (projects/hybridizer/LAUNCH-PAIRS.json) is append-only in spirit: pair keys are
canonical (sorted) and the list is regenerated identically from the same catalogue, so the
submitter's ledger keys never drift.

Usage:
    python scripts/hybridizer_launch_pairs.py --catalog ../kind_robots/utils/hybridizer/starterCatalog.json
    python scripts/hybridizer_launch_pairs.py --catalog ... --check   # verify the committed file
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "projects" / "hybridizer" / "LAUNCH-PAIRS.json"
SEED = 20261030
TARGET = 4000
ODDITIES = {"disco-ball", "mushroom", "cupcake"}

# Day-one showcase: instantly readable blends a first visitor should meet.
SHOWCASE = [
    ("banana", "cat"), ("vampire", "bat"), ("octopus", "astronaut"), ("dragon", "axolotl"),
    ("robot", "dog"), ("pineapple", "hedgehog"), ("ghost", "jellyfish"), ("unicorn", "narwhal"),
    ("pirate", "cockatoo"), ("ninja", "red-panda"), ("wizard", "owl"), ("zombie", "flamingo"),
    ("phoenix", "peacock"), ("knight", "armadillo"), ("watermelon", "tortoise"), ("cupcake", "pig"),
    ("disco-ball", "chameleon"), ("mushroom", "tree-frog"), ("werewolf", "giant-panda"), ("alien", "blobfish"),
    ("witch", "cat"), ("cyborg", "rhinoceros"), ("skeleton", "giraffe"), ("strawberry", "pufferfish"),
    ("lemon", "lion"), ("avocado", "sloth"), ("coconut", "lobster"), ("pumpkin", "owl"),
    ("cherry", "gerbil"), ("grapes", "octopus"), ("elephant", "seahorse"), ("penguin", "toucan"),
    ("hammerhead-shark", "horse"), ("capybara", "koala"), ("tiger", "zebra"), ("nautilus", "tortoise"),
]

# Category quotas, summing to TARGET. Small categories take every pair they have.
QUOTAS = [
    ("animal-animal", 2000),
    ("animal-fruit", 700),
    ("animal-species", 500),
    ("animal-archetype", 300),
    ("animal-oddity", 200),
    ("fruit-species", 80),
    ("fruit-archetype", 50),
    ("species-archetype", 66),
    ("species-species", 55),
    ("archetype-archetype", 15),
    ("fruit-fruit", 14),
    ("oddity-other", 20),
]


def group_of(entry: dict) -> str:
    if entry["key"] in ODDITIES:
        return "oddity"
    return {"ANIMAL": "animal", "SPECIES": "species", "ARCHETYPE": "archetype"}.get(
        entry["taxonomy"], "fruit"
    )


def category(a: str, b: str) -> str:
    ga, gb = sorted((a, b))
    if "oddity" in (ga, gb) and "animal" not in (ga, gb):
        return "oddity-other"
    return f"{ga}-{gb}" if f"{ga}-{gb}" in dict(QUOTAS) else f"{gb}-{ga}"


def canonical(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a < b else (b, a)


def build(catalog: dict) -> dict:
    entries = catalog["entries"]
    groups = {e["key"]: group_of(e) for e in entries}
    keys = sorted(groups)
    rng = random.Random(SEED)
    usage = {k: 0 for k in keys}
    chosen: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for a, b in SHOWCASE:
        if a in groups and b in groups:
            pair = canonical(a, b)
            if pair not in seen:
                seen.add(pair)
                chosen.append(pair)
                usage[a] += 1
                usage[b] += 1

    buckets: dict[str, list[tuple[str, str]]] = {name: [] for name, _ in QUOTAS}
    for a, b in itertools.combinations(keys, 2):
        buckets[category(groups[a], groups[b])].append((a, b))

    per_category: dict[str, list[tuple[str, str]]] = {}
    for name, quota in QUOTAS:
        pool = buckets[name]
        rng.shuffle(pool)
        already = sum(1 for p in chosen if category(groups[p[0]], groups[p[1]]) == name)
        picked: list[tuple[str, str]] = []
        remaining = [p for p in pool if p not in seen]
        while remaining and already + len(picked) < quota:
            # Least-used ingredients first; shuffled order breaks ties deterministically.
            remaining.sort(key=lambda p: usage[p[0]] + usage[p[1]])
            pair = remaining.pop(0)
            seen.add(pair)
            picked.append(pair)
            usage[pair[0]] += 1
            usage[pair[1]] += 1
        per_category[name] = picked

    # Interleave categories in proportion to their size so every batch has variety.
    queues = {name: list(pairs) for name, pairs in per_category.items() if pairs}
    total_left = sum(len(q) for q in queues.values())
    credit = {name: 0.0 for name in queues}
    while total_left:
        for name in list(queues):
            credit[name] += len(per_category[name]) / max(1, sum(len(v) for v in per_category.values()))
        name = max(queues, key=lambda n: credit[n])
        chosen.append(queues[name].pop(0))
        credit[name] -= 1
        total_left -= 1
        if not queues[name]:
            del queues[name]

    counts: dict[str, int] = {}
    for a, b in chosen:
        cat = category(groups[a], groups[b])
        counts[cat] = counts.get(cat, 0) + 1
    used = [usage[k] for k in keys]
    return {
        "version": 1,
        "seed": SEED,
        "catalogVersion": catalog.get("version"),
        "total": len(chosen),
        "counts": dict(sorted(counts.items())),
        "ingredientUsage": {"min": min(used), "max": max(used)},
        "pairs": [list(p) for p in chosen],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--catalog",
        type=Path,
        default=ROOT / "projects" / "hybridizer" / "STARTER-CATALOG.json",
        help="starter catalogue; keys and taxonomy must match kind_robots utils/hybridizer/starterCatalog.json",
    )
    parser.add_argument("--check", action="store_true", help="fail if the committed file differs")
    args = parser.parse_args()
    data = build(json.loads(args.catalog.read_text()))
    if data["total"] != TARGET:
        print(f"expected {TARGET} pairs, built {data['total']}", file=sys.stderr)
        return 1
    rendered = json.dumps(data, indent=1) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text() != rendered:
            print(f"{OUT} is stale; rerun without --check", file=sys.stderr)
            return 1
        print(f"{OUT.name} matches ({data['total']} pairs)")
        return 0
    OUT.write_text(rendered)
    print(f"wrote {OUT} ({data['total']} pairs) {data['counts']} usage {data['ingredientUsage']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
