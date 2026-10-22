"""Risk should earn authored receipts without bypassing Shifting Desks' no-clean-wins contract."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "projects" / "shifting-desks" / "encounters"


def test_risky_paperwork_rewards_are_real_authored_routes():
    reward_file = PACKS / "RISK-PAYOFFS.json"
    doc = json.loads(reward_file.read_text(encoding="utf-8"))
    assert doc["schema_version"] == 1
    assert doc["project"] == "shifting-desks"
    assert len(doc["payoffs"]) >= 4
    by_dept = {}
    for path in PACKS.glob("*.json"):
        if path.name in {"DECKS.json", "ENDINGS.json", "FLAG-MAP.json", "RISK-PAYOFFS.json"}:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("department", {}).get("id"):
            by_dept[data["department"]["id"]] = data

    seen = set()
    for payoff in doc["payoffs"]:
        department_id = payoff["department"]
        card_id = payoff["card"]
        choice_id = payoff["choice"]
        key = (department_id, card_id, choice_id)
        assert key not in seen, f"duplicate reward: {key}"
        seen.add(key)
        department = by_dept[department_id]
        card = next(card for card in department["encounters"] if card["id"] == card_id)
        choice = next(choice for choice in card["choices"] if choice["id"] == choice_id)
        assert choice["roll"], f"{key}: rewards must require a risky check"
        assert choice["requires"] is None, f"{key}: advertised rewards must be ungated"
        assert payoff["effects"] == {"forms": 1}, f"{key}: limited to one earned Form"
        assert len(payoff["message"]) >= 40, f"{key}: narrative payoff is not optional"
        combined = {
            meter: (choice["cost"].get(meter, 0) + choice["success"]["effects"].get(meter, 0))
            for meter in ("composure", "clearance", "suspicion", "successors", "forms")
        }
        assert any(
            combined[meter] < 0 for meter in ("composure", "clearance", "successors", "forms")
        ) or combined["suspicion"] > 0, f"{key}: even success must have a cost"
