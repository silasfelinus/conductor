#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_dream_records.py"
TESTS = ROOT / "tests" / "test_build_dream_records.py"
WORKFLOW = ROOT / ".github" / "workflows" / "_patch-daily-dream-vibe-links.yml"
SELF = Path(__file__)

text = BUILDER.read_text(encoding="utf-8")
text = text.replace(
    "each linked to the\n    world Dream via dreamIds. NO shadow Dreams of those types.",
    "each linked to both the\n    world Dream and its GENRE vibe via dreamIds. NO shadow Dreams of those types.",
)
text = text.replace(
    "scenario cohesion comes from the dreamIds link to the world Dream.",
    "scenario cohesion comes from dreamIds links to both the world and GENRE vibe.",
)
old_links = "link_ids = [world_id] if world_id else []"
if text.count(old_links) != 3:
    raise SystemExit(f"expected 3 world-only link assignments, found {text.count(old_links)}")
text = text.replace(
    old_links,
    "link_ids = [i for i in (world_id, genre_id) if i]",
)
text = text.replace(
    "# 7. Scenarios (real Scenario rows, linked to the world + locations)",
    "# 7. Scenarios (real Scenario rows, linked to the world, vibe + locations)",
)
old_scenario = "scenario_links = [i for i in [world_id, *location_ids] if i]"
if text.count(old_scenario) != 1:
    raise SystemExit("expected one world/location Scenario link assignment")
text = text.replace(
    old_scenario,
    "scenario_links = [i for i in [world_id, genre_id, *location_ids] if i]",
)
BUILDER.write_text(text, encoding="utf-8")

tests = TESTS.read_text(encoding="utf-8")
tests = tests.replace(
    "        self.posts = []\n",
    "        self.posts = []\n        self.created = []\n",
)
tests = tests.replace(
    "        self.next_id += 1\n        return 201, {\"data\": {\"id\": self.next_id}}\n",
    "        self.next_id += 1\n        self.created.append((url, body, self.next_id))\n        return 201, {\"data\": {\"id\": self.next_id}}\n",
)
new_test = '''\n\ndef test_real_entities_link_to_world_and_genre_vibe(env, monkeypatch):\n    backlog, _ = env\n    write_proposal_file(backlog)\n    fake = FakeAPI(fail_after=None)\n    monkeypatch.setattr(bdr, "http_json", fake)\n\n    bdr.run_build("2020-01-01", dry_run=False)\n\n    world_id = next(\n        row_id for url, body, row_id in fake.created\n        if url.endswith("/api/dreams") and body.get("dreamType") == "PITCH"\n    )\n    vibe_id = next(\n        row_id for url, body, row_id in fake.created\n        if url.endswith("/api/dreams") and body.get("dreamType") == "GENRE"\n    )\n    linked_paths = ("/api/characters", "/api/bots", "/api/rewards", "/api/scenarios")\n    linked_bodies = [\n        body for url, body, _ in fake.created\n        if any(url.endswith(path) for path in linked_paths)\n    ]\n\n    assert linked_bodies\n    for body in linked_bodies:\n        assert world_id in body["dreamIds"]\n        assert vibe_id in body["dreamIds"]\n'''
if "def test_real_entities_link_to_world_and_genre_vibe" not in tests:
    tests = tests.rstrip() + new_test + "\n"
TESTS.write_text(tests, encoding="utf-8")

for path in (WORKFLOW, SELF):
    if path.exists():
        path.unlink()
