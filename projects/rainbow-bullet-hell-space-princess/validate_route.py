"""Validate rainbowRoute.json: reachability, alt gating, finale on every route, no Act skipped."""
import itertools
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "rainbowRoute.json"
data = json.load(open(path))
nodes = {n["id"]: n for n in data["nodes"]}
paths = data["paths"]
conds = set(data["conditions"])
errors = []

def check(ok, msg):
    if not ok:
        errors.append(msg)

# Schema
starts = [n for n in nodes.values() if n["kind"] == "start"]
finales = [n for n in nodes.values() if n["kind"] == "finale"]
check(len(starts) == 1, "exactly one start node")
check(len(finales) == 1, "exactly one finale node")
check(sum(n["kind"] == "act" for n in nodes.values()) == 8, "eight Act nodes")
check(sum(n["kind"] == "alt" for n in nodes.values()) == 4, "four alt nodes")
check(sorted(n.get("act") for n in nodes.values() if "act" in n) == list(range(1, 10)), "acts 1..9 each once")
for p in paths:
    check(p["from"] in nodes and p["to"] in nodes, f"path {p} names real nodes")
    u = p["unlock"]
    if u is None:
        check(nodes[p["from"]]["kind"] == "start", f"only the start path is always open: {p}")
    else:
        check(u["node"] == p["from"], f"unlock is earned in the stage before: {p}")
        check(u["condition"] in conds, f"condition documented: {u['condition']}")
start = starts[0]["id"]
finale = finales[0]["id"]

def reachable(open_paths):
    seen, todo = {start}, [start]
    while todo:
        here = todo.pop()
        for p in open_paths:
            if p["from"] == here and p["to"] not in seen:
                seen.add(p["to"]); todo.append(p["to"])
    return seen

# 1. Every node reachable when every condition can be met.
everything = reachable(paths)
check(everything == set(nodes), f"unreachable nodes: {set(nodes) - everything}")

# 2. Every alt reachable only via a named (non-'clear', non-null) condition.
for alt in (n for n in nodes.values() if n["kind"] == "alt"):
    incoming = [p for p in paths if p["to"] == alt["id"]]
    check(incoming, f"{alt['id']} has an entry path")
    for p in incoming:
        check(p["unlock"] and p["unlock"]["condition"] != "clear", f"{alt['id']} entered without a condition: {p}")
    check(alt["id"] not in reachable([p for p in paths if p["unlock"] is None or p["unlock"]["condition"] == "clear"]),
          f"{alt['id']} reachable on clears alone")

# 3. Finale reachable by every route: every maximal walk ends at the finale (no dead ends, no cycles),
#    under every combination of branch conditions met / missed, and every route flies all eight Acts.
named = sorted({p["unlock"]["condition"] for p in paths if p["unlock"] and p["unlock"]["condition"] != "clear"})
routes = set()
for combo in itertools.product([False, True], repeat=len(named)):
    met = {c for c, on in zip(named, combo) if on}
    open_paths = [p for p in paths if p["unlock"] is None or p["unlock"]["condition"] in ("clear", *met)]
    check(finale in reachable(open_paths), f"finale unreachable with conditions {met}")
    def walk(here, route):
        if len(route) > len(nodes):
            errors.append(f"cycle on {route}"); return
        nxt = sorted({p["to"] for p in open_paths if p["from"] == here})
        if not nxt:
            check(here == finale, f"dead end at {here} on route {route}")
            routes.add(tuple(route)); return
        for to in nxt:
            walk(to, route + [to])
    walk(start, [start])
acts = {n["id"] for n in nodes.values() if n["kind"] == "act"}
for r in routes:
    check(acts <= set(r), f"route skips an Act: {r}")

# 4. Medals: one per node except the start, ids unique.
medal_nodes = [m["node"] for m in data["medals"]]
check(sorted(medal_nodes) == sorted(n for n in nodes if n != start), "one medal per playable node")
check(len({m["id"] for m in data["medals"]}) == len(data["medals"]), "medal ids unique")

alts = [n for n in nodes if nodes[n]["kind"] == "alt"]
print(f"nodes: {len(nodes)} (8 acts, 4 alts, finale, start); paths: {len(paths)}; medals: {len(data['medals'])}")
print(f"branch conditions: {', '.join(named)}; combinations tested: {2 ** len(named)}")
print(f"distinct routes start -> {finale}: {len(routes)} (2^{len(alts)} detour patterns); all end at {finale}, none skips an Act")
for r in sorted(routes, key=len)[:1] + sorted(routes, key=len)[-1:]:
    print("  e.g. " + " > ".join(r))
if errors:
    print("FAIL"); [print("  - " + e) for e in errors]; sys.exit(1)
print("PASS: every node reachable; every alt gated by a named condition; finale reachable on every route")
