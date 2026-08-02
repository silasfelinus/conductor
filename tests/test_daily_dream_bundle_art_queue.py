"""Integration guard: the six-part proposal produces six distinct art requests."""

import json

import yaml

import scripts.build_dream_records as bdr


PROPOSAL = {
    "title": "Six Art Dream", "slug": "six-art-dream", "idea": "One connected bundle.",
    "vibe": {"title": "Umbrella Vibe", "line": "Everything connects.", "art_direction": "world key art"},
    "locations": [{"title": "One Place", "known_for": "x", "local_rule": "y", "best_scene": "z", "art_direction": "place art"}],
    "characters": [{"name": "One Hero", "role_drive": "keeper", "carries": "keys", "complication": "memory", "look": "bright coat"}],
    "rewards": [
        {"name": "One Item", "reward_type": "ITEM", "rarity": "RARE", "grants": "g", "best_used_when": "w", "catch": "c"},
        {"name": "One Skill", "reward_type": "SKILL", "rarity": "UNCOMMON", "grants": "g", "best_used_when": "w", "catch": "c"},
    ],
    "scenarios": [{"title": "One Scenario", "setup": "Umbrella Vibe at One Place with One Hero."}],
}


class FakeAPI:
    def __init__(self):
        self.next_id = 1000

    def __call__(self, method, url, body=None, timeout=60):
        if method == "DELETE":
            return 200, {"success": True}
        self.next_id += 1
        return 201, {"data": {"id": self.next_id}}


def test_complete_bundle_queues_six_art_requests(tmp_path, monkeypatch):
    backlog = tmp_path / "backlog"
    backlog.mkdir()
    art = tmp_path / "art-prompts.yaml"
    art.write_text(
        "requests:\n"
        "inspirations:\n"
        "- project: reference-project\n"
        "  images:\n"
        "  - image_path: reference.webp\n",
        encoding="utf-8",
    )
    path = backlog / "2020-01-01-six-art-dream.md"
    path.write_text(
        "---\nslug: six-art-dream\ntitle: Six Art Dream\ntype: dream\nstatus: outline\n"
        "narrator: 'no'\nproposal: true\nproposal_date: '2020-01-01'\nbuilt_pr: null\n---\n\n"
        f"<!-- proposal-data\n{json.dumps(PROPOSAL)}\n-->\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(bdr, "BACKLOG", backlog)
    monkeypatch.setattr(bdr, "ART_PROMPTS", art)
    monkeypatch.setattr(bdr, "KR_API_TOKEN", "test-token")
    monkeypatch.setattr(bdr, "http_json", FakeAPI())

    bdr.run_build("2020-01-01", dry_run=False)

    parsed = yaml.safe_load(art.read_text(encoding="utf-8"))
    requests = parsed["requests"]
    assert len(requests) == 6
    assert {request["id"] for request in requests} == {
        "dream-cycle-six-art-dream-six-art-dream",
        "dream-cycle-six-art-dream-one-place",
        "dream-cycle-six-art-dream-one-hero",
        "dream-cycle-six-art-dream-one-item",
        "dream-cycle-six-art-dream-one-skill",
        "dream-cycle-six-art-dream-one-scenario-scenario",
    }
    assert all(request["status"] == "pending" for request in requests)
    assert all(request["target_repo"] == "silasfelinus/kind_robots" for request in requests)
    assert parsed["inspirations"] == [{
        "project": "reference-project",
        "images": [{"image_path": "reference.webp"}],
    }]
