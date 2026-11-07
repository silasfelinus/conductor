"""Contract checks for the e12 Hoshimori finale writer packet (not runtime integration)."""
import itertools
import json
import unittest
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1] / "projects/memory-dungeon/story/HOSHIMORI-FINALE-CROSSINGS.json"


def apply_choice(state, scene, choice_id, visited=True, earned_entry=True):
    """Pure reference reducer: reject forged choices, never double-award fragments."""
    if not visited or not earned_entry:
        return state
    choice = next((c for c in scene["choices"] if c["id"] == choice_id), None)
    if choice is None:
        return state
    if scene["id"] in state["decisions"]:
        return state
    return {
        "decisions": {**state["decisions"], scene["id"]: choice_id},
        "effects": sorted(set(state["effects"]) | {choice["effect"]}),
        "fragments": sorted(set(state["fragments"]) | {scene["id"]}),
    }


class FinaleCrossingContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(PACKET.read_text(encoding="utf-8"))

    def test_scope_and_unique_content(self):
        p = self.packet
        self.assertEqual((p["world"], p["lead"], p["canonical_world_count"]), ("e12", "Vesper", 12))
        self.assertEqual(len(p["scenes"]), 2)
        ids = [s["id"] for s in p["scenes"]]
        self.assertEqual(len(set(ids)), 2)
        effects = [c["effect"] for s in p["scenes"] for c in s["choices"]]
        self.assertEqual(len(effects), len(set(effects)))
        for scene in p["scenes"]:
            self.assertEqual(len(scene["choices"]), 3)
            for c in scene["choices"]:
                for key in ("label", "cost", "outcome", "effect", "callback"):
                    self.assertTrue(c[key].strip(), (scene["id"], key))
            self.assertTrue(scene["fallback"])
        self.assertEqual(p["art"]["job_ids"], [])
        self.assertEqual(p["art"]["status"], "NOT_SUBMITTED")

    def test_all_nine_routes_and_replays(self):
        a, b = self.packet["scenes"]
        for first, second in itertools.product(a["choices"], b["choices"]):
            state = {"decisions": {}, "effects": [], "fragments": []}
            state = apply_choice(state, a, first["id"])
            state = apply_choice(state, b, second["id"])
            self.assertEqual(len(state["decisions"]), 2)
            self.assertEqual(len(state["fragments"]), 2)
            self.assertEqual(len(state["effects"]), 2)
            restored = json.loads(json.dumps(state))
            self.assertEqual(apply_choice(restored, a, first["id"]), restored)
            self.assertEqual(apply_choice(restored, a, a["choices"][-1]["id"]), restored)
            self.assertEqual(apply_choice(restored, b, second["id"]), restored)

    def test_forged_and_unearned_choices_do_not_mutate(self):
        state = {"decisions": {}, "effects": [], "fragments": []}
        for scene in self.packet["scenes"]:
            valid = scene["choices"][0]["id"]
            for choice, visited, earned in [
                ("forged-choice", True, True),
                (valid, False, True),
                (valid, True, False),
            ]:
                self.assertIs(apply_choice(state, scene, choice, visited, earned), state)


if __name__ == "__main__":
    unittest.main()
