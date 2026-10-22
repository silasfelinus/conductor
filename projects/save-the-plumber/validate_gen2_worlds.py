"""Validate gen2Worlds.json (Save the Plumber Gen-2 overworld graphs).

Usage: python3 -I validate_gen2_worlds.py [path/to/gen2Worlds.json]
Exit 0 when every hard check passes; 1 otherwise. Prints a summary either way.

Hard checks
  - ids unique campaign-wide, lowercase kebab; kinds from the allowed set
  - every path endpoint and unlock node exists; unlock.node is the path's `from`
    (a path is revealed from the node that earns it); unlock exit is normal|secret
  - unlocks only come from course nodes (level/fortress/house/castle/special/chapel)
  - secretExit nodes <-> secret-unlock paths match both ways
  - each campaign world: one start, one castle, >=1 fortress, >=1 house,
    >=1 bonus or shop, 6-9 non-start nodes, >=1 secret exit
  - castle N has a normal-exit warp path to wN+1-start (worlds 1-7)
  - progression sim from w1-start (clearing what is reachable, both exits where
    a node has a secret) reaches every node
  - normal-exits-only sim reaches every castle (secrets are never required)
  - every Gen-1 code 1-1..8-4 is used exactly once as a node `stage`
"""
import json
import re
import sys
from pathlib import Path

KINDS = {"start", "level", "fortress", "house", "bonus", "shop", "chapel", "castle", "special"}
COURSE = {"level", "fortress", "house", "castle", "special", "chapel"}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("gen2Worlds.json")
worlds = json.loads(path.read_text())
errors: list[str] = []
err = errors.append

if not isinstance(worlds, list):
    sys.exit("top level must be an array of worlds")

nodes: dict[str, dict] = {}
node_world: dict[str, int] = {}
paths: list[dict] = []
for w in worlds:
    for n in w["nodes"]:
        if n["id"] in nodes:
            err(f"duplicate id {n['id']}")
        if not KEBAB.match(n["id"]):
            err(f"id not lowercase kebab: {n['id']}")
        if n["kind"] not in KINDS:
            err(f"{n['id']}: bad kind {n['kind']}")
        nodes[n["id"]] = n
        node_world[n["id"]] = w["world"]
    for p in w["paths"]:
        paths.append(p)

# Path integrity
for p in paths:
    for end in ("from", "to"):
        if p[end] not in nodes:
            err(f"path {p['from']}->{p['to']}: dangling {end} id {p[end]}")
    u = p["unlock"]
    if u is not None:
        if u["node"] not in nodes:
            err(f"path {p['from']}->{p['to']}: dangling unlock node {u['node']}")
        elif nodes[u["node"]]["kind"] not in COURSE:
            err(f"path {p['from']}->{p['to']}: unlocked by non-course {u['node']}")
        if u["exit"] not in ("normal", "secret"):
            err(f"path {p['from']}->{p['to']}: bad exit {u['exit']}")
        if u["node"] != p["from"]:
            err(f"path {p['from']}->{p['to']}: unlock node {u['node']} is not its origin")
    if "warp" in p and p["warp"] not in ("up", "down", "left", "right"):
        err(f"path {p['from']}->{p['to']}: bad warp {p['warp']}")
    if p["from"] in nodes and p["to"] in nodes and node_world[p["from"]] != node_world[p["to"]] and "warp" not in p:
        err(f"path {p['from']}->{p['to']}: crosses worlds without a warp")

# Secret exits both ways
secret_paths = {p["unlock"]["node"] for p in paths if p["unlock"] and p["unlock"]["exit"] == "secret"}
flagged = {i for i, n in nodes.items() if n.get("secretExit")}
for i in sorted(flagged - secret_paths):
    err(f"{i}: secretExit opens nothing")
for i in sorted(secret_paths - flagged):
    err(f"{i}: has a secret path but no secretExit flag")

# Per-world shape
for w in worlds:
    if w.get("special"):
        continue
    kinds = [n["kind"] for n in w["nodes"]]
    wn = w["world"]
    if kinds.count("start") != 1:
        err(f"world {wn}: needs exactly one start")
    if kinds.count("castle") != 1:
        err(f"world {wn}: needs exactly one castle")
    for need in ("fortress", "house"):
        if need not in kinds:
            err(f"world {wn}: no {need}")
    if "bonus" not in kinds and "shop" not in kinds:
        err(f"world {wn}: no bonus or shop")
    playable = len(kinds) - kinds.count("start")
    if not 6 <= playable <= 9:
        err(f"world {wn}: {playable} non-start nodes (want 6-9)")
    if not any(n.get("secretExit") for n in w["nodes"]):
        err(f"world {wn}: no secret exit")
    if f"w{wn}-start" not in nodes:
        err(f"world {wn}: start id must be w{wn}-start (engine startId)")

campaign = [w for w in worlds if not w.get("special")]
last = max(w["world"] for w in campaign)
for w in campaign:
    if w["world"] == last:
        continue
    castle = next(n["id"] for n in w["nodes"] if n["kind"] == "castle")
    nxt = f"w{w['world'] + 1}-start"
    ok = any(
        p["from"] == castle and p["to"] == nxt and p["unlock"] == {"node": castle, "exit": "normal"}
        and p.get("warp") == "right"
        for p in paths
    )
    if not ok:
        err(f"world {w['world']}: castle {castle} has no normal warp-right path to {nxt}")


def simulate(allow_secret: bool) -> set[str]:
    """Fixed point: a node is reached when an open path touches a reached node;
    clearing a reached course node earns its normal exit (and secret if allowed)."""
    reached = {"w1-start"}
    while True:
        earned = set()
        for i in reached:
            if nodes[i]["kind"] in COURSE:
                earned.add((i, "normal"))
                if allow_secret and nodes[i].get("secretExit"):
                    earned.add((i, "secret"))
        grew = False
        for p in paths:
            if p["from"] not in nodes or p["to"] not in nodes:
                continue  # dangling: already reported above
            u = p["unlock"]
            open_ =u is None or (u["node"], u["exit"]) in earned
            if open_ and (p["from"] in reached) != (p["to"] in reached):
                reached |= {p["from"], p["to"]}
                grew = True
        if not grew:
            return reached


full = simulate(True)
for i in sorted(set(nodes) - full):
    err(f"{i}: unreachable from w1-start")
normal = simulate(False)
for w in campaign:
    castle = next(n["id"] for n in w["nodes"] if n["kind"] == "castle")
    if castle not in normal:
        err(f"{castle}: needs a secret exit to reach (main route must not)")
hidden_only = sorted(set(nodes) - normal)

# Gen-1 reuse
gen1 = [f"{a}-{b}" for a in range(1, 9) for b in range(1, 5)]
used: dict[str, list[str]] = {}
for i, n in nodes.items():
    if n.get("stage"):
        used.setdefault(n["stage"], []).append(i)
for code in gen1:
    if len(used.get(code, [])) != 1:
        err(f"Gen-1 {code}: used {len(used.get(code, []))} times (want 1)")
for code in used:
    if code not in gen1:
        err(f"unknown Gen-1 code {code}")

# Report
courses = [i for i, n in nodes.items() if n["kind"] in COURSE - {"chapel"}]
print(f"file: {path}")
print(f"worlds: {len(campaign)} + {len(worlds) - len(campaign)} special zone")
print(f"nodes: {len(nodes)}  paths: {len(paths)}  courses: {len(courses)}  chapels: "
      f"{sum(n['kind'] == 'chapel' for n in nodes.values())}  secret exits: {len(flagged)}")
for w in worlds:
    ks = [n["kind"] for n in w["nodes"]]
    print(f"  W{w['world']} {w['name']}: {len(ks) - ks.count('start')} nodes, "
          f"{sum(n.get('secretExit', False) for n in w['nodes'])} secret exit(s)")
print(f"reachable (all exits): {len(full)}/{len(nodes)}")
print(f"reachable (normal exits only): {len(normal)}/{len(nodes)}; secret-only: {', '.join(hidden_only)}")
print("Gen-1 -> node: " + ", ".join(f"{c}->{used[c][0]}" for c in gen1 if c in used))
if errors:
    print(f"\nFAIL: {len(errors)} problem(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("\nPASS: all hard checks")
