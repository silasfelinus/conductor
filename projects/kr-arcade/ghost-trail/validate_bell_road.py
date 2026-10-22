#!/usr/bin/env python3
"""Validate bellRoad.json (Zuzu: Ghost Trail Gen-2 overworld, conductor kr-arcade t-158).

Checks: no dangling ids; every node reachable from the start (exits earned by fixpoint, seals
honoured); every declared secret exit opens something and every unlock names a declared exit;
each region's boss leads on to the next region (the last one ends the game); per-region quota
(level, fortress, house, boss, a secret exit); the shrine is reachable only by secret paths;
20-28 nodes; relic ids unique; every Gen-1 act and relic in kind_robots is mapped exactly once
(read-only scan of utils/arcade/ghostTrail/acts); and a worst-case three-slot save fits the
arcade store's 8 KB per-game limit.

Usage: python3 validate_bell_road.py [bellRoad.json] [kind_robots root]
Exit 0 when every check passes, 1 otherwise.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "bellRoad.json"
kr_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/home/user/kind_robots")
D = json.loads(data_path.read_text())

errors: list[str] = []
notes: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


nodes = {n["id"]: n for n in D["nodes"]}
regions = {r["id"]: r for r in D["regions"]}
maps = {m["id"] for m in D["maps"]}
kinds = set(D["nodeKinds"])
exits_ok = set(D["exits"])

# --- ids and shape --------------------------------------------------------------------------
dupes = [i for i, c in Counter(n["id"] for n in D["nodes"]).items() if c > 1]
if dupes:
    err(f"duplicate node ids: {dupes}")
if D["start"] not in nodes or nodes[D["start"]]["kind"] != "start":
    err("start is not a start node")
for n in D["nodes"]:
    if n["kind"] not in kinds:
        err(f"{n['id']}: unknown kind {n['kind']}")
    if n["region"] not in regions:
        err(f"{n['id']}: dangling region {n['region']}")
    if not (0 <= n["x"] <= D["screen"][0] and 0 <= n["y"] <= D["screen"][1]):
        err(f"{n['id']}: off-screen ({n['x']},{n['y']})")
    for e in n.get("exits", []):
        if e not in exits_ok:
            err(f"{n['id']}: unknown exit {e}")
    if n["kind"] != "start" and "normal" not in n.get("exits", []):
        err(f"{n['id']}: playable node without a normal exit")
    for b in n.get("seal", {}).get("bossClears", []):
        if b not in nodes or nodes[b]["kind"] != "boss":
            err(f"{n['id']}: seal names {b}, not a boss node")
for r in D["regions"]:
    if r["map"] not in maps:
        err(f"region {r['id']}: dangling map {r['map']}")
    for k in ("entry", "boss"):
        if r[k] is not None and r[k] not in nodes:
            err(f"region {r['id']}: dangling {k} {r[k]}")
seen_paths = set()
for p in D["paths"]:
    for k in ("from", "to"):
        if p[k] not in nodes:
            err(f"path {p['from']}->{p['to']}: dangling {k}")
    key = frozenset((p["from"], p["to"]))
    if key in seen_paths:
        err(f"duplicate path {p['from']}<->{p['to']}")
    seen_paths.add(key)
    u = p["unlock"]
    if u is not None:
        if u["node"] not in nodes:
            err(f"path {p['from']}->{p['to']}: unlock names missing node {u['node']}")
        elif u["exit"] not in nodes[u["node"]].get("exits", []):
            err(f"path {p['from']}->{p['to']}: {u['node']} has no {u['exit']} exit")
        if u["node"] not in (p["from"], p["to"]):
            notes.append(f"path {p['from']}->{p['to']} is opened remotely by {u['node']}")
    crosses = p["from"] in nodes and p["to"] in nodes and (
        regions[nodes[p["from"]]["region"]]["map"] != regions[nodes[p["to"]]["region"]]["map"]
        or regions[nodes[p["from"]]["region"]].get("mapLayer") != regions[nodes[p["to"]]["region"]].get("mapLayer")
    )
    if crosses and "warp" not in p:
        err(f"path {p['from']}->{p['to']} changes map without a warp")
for s in D.get("switches", []):
    sb = s["setBy"]
    if sb["node"] not in nodes or sb["exit"] not in nodes[sb["node"]]["exits"]:
        err(f"switch {s['id']}: dangling setBy")
    for lv in s.get("levelsWithPlanks", []):
        if lv not in nodes:
            err(f"switch {s['id']}: dangling level {lv}")
for w in D.get("subweapons", []):
    if w["from"] != "start" and w["from"] not in nodes:
        err(f"subweapon {w['id']}: dangling source {w['from']}")
if D["ending"]["node"] not in nodes:
    err("ending node missing")

if errors:  # dangling ids make the graph walk meaningless: report them alone
    print("FAIL (ids):")
    for e in errors:
        print("  -", e)
    sys.exit(1)

# --- reachability (fixpoint over earned exits; paths walk both ways; seals gate entry) -------
def reach(honour_seals: bool):
    reached = {D["start"]}
    earned = set()  # (node, exit)
    changed = True
    while changed:
        changed = False
        for nid in list(reached):
            for e in nodes[nid].get("exits", []):
                if (nid, e) not in earned:
                    earned.add((nid, e))
                    changed = True
        bosses_down = {n for (n, e) in earned if e == "normal" and nodes[n]["kind"] == "boss"}
        for p in D["paths"]:
            u = p["unlock"]
            if u is not None and (u["node"], u["exit"]) not in earned:
                continue
            for a, b in ((p["from"], p["to"]), (p["to"], p["from"])):
                if a in reached and b not in reached:
                    seal = nodes[b].get("seal")
                    if honour_seals and seal and not set(seal["bossClears"]) <= bosses_down:
                        continue
                    reached.add(b)
                    changed = True
    return reached, earned


reached, earned = reach(True)
missing = sorted(set(nodes) - reached)
if missing:
    err(f"unreachable nodes: {missing}")

# Main path only (normal exits): what a player who never finds a secret can reach.
def reach_normal():
    reached = {D["start"]}
    changed = True
    while changed:
        changed = False
        done = {n for n in reached if nodes[n]["kind"] != "start"}
        bosses = {n for n in done if nodes[n]["kind"] == "boss"}
        for p in D["paths"]:
            u = p["unlock"]
            if u is not None and (u["exit"] != "normal" or u["node"] not in done):
                continue
            for a, b in ((p["from"], p["to"]), (p["to"], p["from"])):
                seal = nodes[b].get("seal")
                if a in reached and b not in reached and not (seal and not set(seal["bossClears"]) <= bosses):
                    reached.add(b)
                    changed = True
    return reached


main_path = reach_normal()
if D["ending"]["node"] not in main_path:
    err("the ending is not reachable by normal exits alone")
notes.append(
    f"normal-exit-only player reaches {len(main_path) - 1} of {len(nodes) - 1} playable nodes; "
    f"secret-only nodes: {sorted(set(nodes) - main_path)}"
)

# --- secret exits ----------------------------------------------------------------------------
openers = {(p["unlock"]["node"], p["unlock"]["exit"]) for p in D["paths"] if p["unlock"]}
openers |= {(s["setBy"]["node"], s["setBy"]["exit"]) for s in D.get("switches", [])}
hidden_exits = [(n["id"], "secret") for n in D["nodes"] if "secret" in n.get("exits", [])]
for se in hidden_exits:
    if se not in openers:
        err(f"secret exit of {se[0]} opens nothing")
for n in D["nodes"]:
    if n["kind"] in ("start",) or n["id"] == D["ending"]["node"]:
        continue
    if (n["id"], "normal") not in openers:
        err(f"normal exit of {n['id']} opens nothing (dead end)")

# --- bosses lead on ---------------------------------------------------------------------------
ordered = sorted((r for r in D["regions"] if r["n"] > 0), key=lambda r: r["n"])
for i, r in enumerate(ordered):
    b = r["boss"]
    if nodes[b]["kind"] != "boss" or nodes[b]["region"] != r["id"]:
        err(f"region {r['id']}: boss {b} is not its boss node")
    if i == len(ordered) - 1:
        if D["ending"] != {**D["ending"], "node": b, "exit": "normal"}:
            err(f"last region boss {b} does not end the game")
        continue
    nxt = ordered[i + 1]
    leads = [p for p in D["paths"] if p["unlock"] == {"node": b, "exit": "normal"}
             and p["from"] == b and p["to"] == nxt["entry"]]
    if not leads:
        err(f"region {r['id']}: boss {b} does not lead on to {nxt['entry']}")

# --- per-region quota -------------------------------------------------------------------------
for r in ordered:
    ns = [n for n in D["nodes"] if n["region"] == r["id"]]
    k = Counter(n["kind"] for n in ns)
    for need in ("level", "fortress", "house", "boss"):
        if k[need] < 1:
            err(f"region {r['id']}: no {need}")
    if k["boss"] != 1:
        err(f"region {r['id']}: {k['boss']} boss nodes")
    if not any("secret" in n.get("exits", []) for n in ns):
        err(f"region {r['id']}: no secret exit")
shrines = [n for n in D["nodes"] if n["kind"] == "shrine"]
if len(shrines) != 1:
    err(f"{len(shrines)} shrine nodes")
else:
    sid = shrines[0]["id"]
    ins = [p for p in D["paths"] if sid in (p["from"], p["to"])]
    entries = [p for p in ins if p["unlock"] and p["unlock"]["node"] != sid]
    if not entries or any(p["unlock"]["exit"] != "secret" for p in entries):
        err("the shrine is reachable by something other than a secret exit")
    notes.append(f"shrine entries: {[p['unlock']['node'] for p in entries]}")
total = len(D["nodes"])
if not 20 <= total <= 28:
    err(f"{total} nodes (want 20-28)")

# --- relics, notes and Gen-1 mapping ----------------------------------------------------------
relics = [x for n in D["nodes"] for x in n.get("relics", [])]
if len(relics) != len(set(relics)):
    err(f"duplicate relic ids: {[x for x, c in Counter(relics).items() if c > 1]}")
bell_notes = [n["note"] for n in D["nodes"] if n["kind"] != "start"]
if len(bell_notes) != total - 1 or len(set(bell_notes)) != len(bell_notes):
    err("every playable node needs one unique bell note")
for n in D["nodes"]:
    if n["kind"] != "start" and not n.get("relics"):
        err(f"{n['id']}: no relic")
acts_dir = kr_root / "utils/arcade/ghostTrail/acts"
if acts_dir.is_dir():
    src = "\n".join(p.read_text() for p in sorted(acts_dir.glob("*.ts")))
    code_acts = set(re.findall(r"^  id: '(s\d[a-z0-9]+)'", src, re.M))
    code_relics = set(re.findall(r"id: '(s\d[a-z0-9]+-[a-z0-9-]+)',\s*\n?\s*x:", src))
    code_relics |= set(re.findall(r"\{ id: '(s\d[a-z0-9]+-[a-z0-9-]+)', x:", src))
    captives = set(re.findall(r"captive: \{\s*id: '([^']+)'", src))
    code_relics -= captives
    mapped_acts = Counter(n["gen1Act"] for n in D["nodes"] if n["gen1Act"])
    if set(mapped_acts) != code_acts or any(c > 1 for c in mapped_acts.values()):
        err(f"Gen-1 act mapping mismatch: code-only {sorted(code_acts - set(mapped_acts))}, "
            f"json-only {sorted(set(mapped_acts) - code_acts)}")
    if not code_relics <= set(relics):
        err(f"Gen-1 relics not placed: {sorted(code_relics - set(relics))}")
    for n in D["nodes"]:
        if n.get("gen1Act"):
            for x in n.get("relics", []):
                if x.startswith("s") and x.split("-")[0] != n["gen1Act"]:
                    err(f"{n['id']}: relic {x} belongs to another act")
    cap_json = {n["captive"] for n in D["nodes"] if n.get("captive")}
    if cap_json != captives:
        err(f"captive mismatch: code {captives}, json {cap_json}")
    notes.append(f"Gen-1 source: {len(code_acts)} acts, {len(code_relics)} relics, captives {sorted(captives)} all mapped")
else:
    notes.append(f"kind_robots acts not found at {acts_dir}; Gen-1 cross-check skipped")
notes.append(f"relics: {len(relics)} total ({len(relics) - 21} new), bell notes: {len(bell_notes)}")

# --- save budget: worst-case three-slot file (GEN2-BELL-ROAD.md 'Save slots') -----------------
playable = [n["id"] for n in D["nodes"] if n["kind"] != "start"]
# The design stores per-node marks as one bitmask (1 normal, 2 secret, 4 bell note, 8/16 relic 0/1,
# 32 rescue) instead of id lists; ids are recovered from the catalog. Measure both forms.
run = {"level": "s6a2", "checkpoint": 6620, "down": [f"squad-member-{i:02d}" for i in range(24)],
       "opened": list(range(16))}
common = {"node": "s6a2", "subweapons": [w["id"] for w in D["subweapons"]], "weapon": "katana",
          "reserve": "poncho", "poncho": True, "switches": ["shrine-bell"], "score": 99_999_999,
          "lives": 99, "deaths": 999_999, "time": 99_999_999, "best": {k: 99_999 for k in playable},
          "run": run}
naive = {**common, "done": playable, "secrets": [s[0] for s in hidden_exits],
         "relics": relics + ["s6a1-novice"], "notes": bell_notes}
compact = {**common, "marks": {k: 63 for k in playable}}
sizes = {}
for name, slot in (("id-list", naive), ("bitmask", compact)):
    f = {"v": 2, "active": 2, "tier": 5, "slots": [slot, slot, slot]}
    sizes[name] = len(json.dumps(f, separators=(",", ":")))
if sizes["bitmask"] > 6144:
    err(f"worst-case bitmask save file is {sizes['bitmask']} bytes (> 6144, 75% of the 8 KB store)")
if sizes["id-list"] > 8192:
    notes.append("id-list save form would overflow 8 KB; use the bitmask form")
notes.append(f"worst-case 3-slot save: bitmask {sizes['bitmask']} B, id-list {sizes['id-list']} B, of 8192")

# --- report -----------------------------------------------------------------------------------
k = Counter(n["kind"] for n in D["nodes"])
print(f"bellRoad.json: {total} nodes {dict(k)}, {len(D['paths'])} paths, "
      f"{len(hidden_exits)} secret exits, {len(ordered)} regions + shrine")
for n in notes:
    print("  note:", n)
if errors:
    print(f"FAIL ({len(errors)}):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("PASS: all reachable, every secret exit opens something, each boss leads on, no dangling ids")
