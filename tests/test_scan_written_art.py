import yaml

import scripts.scan_written_art as scan

DUMPED = {
    "playbooks": [
        {
            "game": "ruler-hooked",
            "title": "Ruler Hooked",
            "artProject": "ruler-hooked",
            "artStyle": "storybook gouache",
            "artNegative": None,
            "nodes": [
                {"key": "opening:1", "kind": "opening", "title": "Castle", "needsArt": True, "artUrl": None,
                 "artPath": "/images/ruler-hooked/castle.webp", "art": None,
                 "prompt": "A small tidy grey stone castle with two short round towers on a green lawn."},
                {"key": "opening:2", "kind": "opening", "title": "Shore", "needsArt": True, "artUrl": None,
                 "artPath": None, "art": None, "prompt": None},
                {"key": "f:1", "kind": "follower", "title": "Pim", "needsArt": True, "artUrl": None,
                 "artPath": None, "art": None, "prompt": "A small rusty lantern-headed robot on a ferry deck at night."},
                {"key": "done", "kind": "spine", "title": "Done", "needsArt": False, "artUrl": "/x.webp",
                 "artPath": None, "art": None, "prompt": "Already painted, never a candidate."},
            ],
        },
        {"game": "broken", "error": "boom"},
    ],
    "extras": [
        {"project": "crystal-street", "publicDir": "public/crystal-street", "suffix": "Airbrushed gouache.",
         "prompts": [
             {"key": "outcomes/lock-in--sing-success", "prompt": "Teens in sleeping bags singing in a circle."},
             {"key": "items/walkman", "prompt": "A yellow tape player on a carpet."},
             {"key": "endings/blank", "prompt": "   "},
         ]},
    ],
}


def test_candidates_keep_only_written_unpainted_art(tmp_path):
    (tmp_path / "public/crystal-street/items").mkdir(parents=True)
    (tmp_path / "public/crystal-street/items/walkman.webp").write_bytes(b"x")
    cells = scan.candidates(DUMPED, tmp_path)
    keys = {c["key"] for c in cells}
    assert keys == {"opening:1", "f:1", "outcomes/lock-in--sing-success"}
    by_key = {c["key"]: c for c in cells}
    assert by_key["opening:1"]["asset"] == "ruler-hooked/castle"
    assert by_key["f:1"]["asset"] == "playbook/ruler-hooked/f:1"
    assert by_key["f:1"]["size"] == "832x1216"
    assert by_key["outcomes/lock-in--sing-success"]["size"] == "1216x832"


def test_ledgered_cells_are_dropped_by_prompt_or_asset(tmp_path):
    cells = scan.candidates(DUMPED, tmp_path)
    prompts = {scan.norm("A small tidy grey stone castle with two short round towers on a green lawn.")}
    assets = {"outcomes/lock-in--sing-success"}
    left = [c["key"] for c in cells if not scan.already_ledgered(c, prompts, assets)]
    assert left == ["f:1", "items/walkman"]


def test_written_ledgers_are_auto_submit_low_priority_and_split(tmp_path, monkeypatch):
    monkeypatch.setattr(scan, "ROOT", tmp_path)
    cells = scan.candidates(DUMPED, tmp_path)
    paths = scan.write_ledgers(cells, part_size=1, today="2026-11-02")
    assert len(paths) == 4
    crystal = [p for p in paths if "crystal-street" in str(p)]
    data = yaml.safe_load(crystal[0].read_text())
    assert data["auto_submit"] is True and data["priority"] == 1 and data["is_public"] is False
    assert data["lanes"][0]["suffix"] == "Airbrushed gouache."
    subject = data["subjects"][0]
    assert subject["asset"].startswith(("outcomes/", "items/"))
    ruler = sorted(p.name for p in paths if "ruler-hooked" in str(p))
    assert ruler == ["WRITTEN-BACKLOG-2026-11-02-PART-1.yaml", "WRITTEN-BACKLOG-2026-11-02-PART-2.yaml"]
