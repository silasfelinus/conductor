import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "projects/shifting-desks"
packs = [json.loads(p.read_text()) for p in (ROOT / "encounters").glob("*-12.json")]
cards = {c["id"]: (p["department"]["order"], c) for p in packs for c in p["encounters"]}


def test_clue_chains_preserve_prerequisites():
    clues = json.loads((ROOT / "CLUE-CHAINS.json").read_text())["clues"]
    receipts = json.loads((ROOT / "CLUE-RECEIPTS.json").read_text())["receipts"]
    assert len(clues) == len(receipts) == 9
    assert len({r["flag"] for r in receipts}) == 9
    for link in clues:
        order, card = cards[link["card"]]
        source = next(c for c in card["choices"] if c["id"] == link["choice"])
        target_card, target_choice = link["target"].split("/")
        target_order, target = cards[target_card]
        target_action = next(c for c in target["choices"] if c["id"] == target_choice)
        assert target_order >= order
        assert source["requires"] is None
        assert target_action["requires"]["flag"] == link["grants"]
        assert target_action["success"]["add_flags"][0] in {r["flag"] for r in receipts}
        assert link["message"] and link["hint"]
        effects = {k: source["cost"].get(k, 0) + source["success"]["effects"].get(k, 0)
                   for k in ("composure", "clearance", "suspicion", "successors", "forms")}
        assert effects["suspicion"] > 0 or any(effects[k] < 0 for k in
            ("composure", "clearance", "successors", "forms"))
