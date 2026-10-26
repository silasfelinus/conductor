import yaml

import scripts.intake as intake
import scripts.new_playbook as new_playbook
from tests.test_intake import _fixture_repo


def test_new_playbook_writes_the_ladder_on_top_of_intake(tmp_path, monkeypatch):
    root, projects = _fixture_repo(tmp_path, monkeypatch)
    assert new_playbook.main([
        "moon-laundry",
        "Moon Laundry: A Spin Cycle",
        "--notes", "Silas: make it about laundry on the moon.\nKeep it small.",
    ]) == 0

    pdir = projects / "moon-laundry"
    roadmap = yaml.safe_load((pdir / "roadmap.yaml").read_text())
    assert roadmap["project"] == "moon-laundry"
    assert roadmap["kind"] == "software"
    assert "Vignette" in roadmap["goal"]
    assert roadmap["notes_from_silas"].startswith("Silas: make it about laundry on the moon.\nKeep it small.")

    tasks = {t["id"]: t for t in roadmap["tasks"]}
    assert [t["id"] for t in roadmap["tasks"]] == [f"t-{n:03d}" for n in range(1, 11)]
    assert {t["milestone"] for t in roadmap["tasks"]} <= {m["id"] for m in roadmap["milestones"]}
    assert sum(m["weight"] for m in roadmap["milestones"]) == 100
    assert tasks["t-001"]["status"] == "ready"
    assert 'npm run playbook:new -- moon-laundry "Moon Laundry: A Spin Cycle"' in tasks["t-001"]["note"]
    for task in roadmap["tasks"]:
        deps = task.get("depends_on")
        if deps is None:
            assert task["status"] == "ready", task["id"]
            continue
        assert task["status"] == "waiting", task["id"]
        for dep in deps if isinstance(deps, list) else [deps]:
            assert dep in tasks, (task["id"], dep)
    assert tasks["t-010"]["gate_human"] is True
    assert tasks["t-010"]["stakes"] == "outward-facing"

    brief = (pdir / "DESIGN-BRIEF.md").read_text()
    assert brief.startswith("# Moon Laundry: A Spin Cycle\n")
    assert "utils/playbookKit/games/moonLaundry.ts" in brief
    assert "__" not in brief
    assert "## 8. Completion gates" in brief

    overrides = yaml.safe_load((root / "project-overrides.yaml").read_text())
    assert any(o["slug"] == "moon-laundry" for o in overrides["overrides"])
    repos = yaml.safe_load((root / "repos.yaml").read_text())
    assert any(r["slug"] == "moon-laundry" and r["repo"] == "silasfelinus/kind_robots" for r in repos["repos"])
    assert "### moon-laundry" in (root / "CONTROL.md").read_text()


def test_templates_have_no_unfilled_placeholders_after_fill():
    values = {"SLUG": "x", "TITLE": "X", "CAMEL": "x", "DATE": "2026-10-26", "GOAL": "g", "NOTES": "n"}
    for name in ("roadmap.template.yaml", "DESIGN-BRIEF.template.md"):
        text = new_playbook.fill((new_playbook.TEMPLATES / name).read_text(), values)
        assert "__" not in text.replace("__init__", ""), name


def test_camel_case_matches_the_kind_robots_scaffold():
    assert new_playbook.camel_case("moon-laundry") == "moonLaundry"
    assert new_playbook.camel_case("lantern-ferry-two") == "lanternFerryTwo"
    assert intake.slugify("Moon Laundry") == "moon-laundry"


FORGE_PITCH = """Moon Laundry: a playbook forged in /admin/playbook-forge.
Socks are portals.

Images: 299 on Illustrious, about 1h 55m of render time
<!-- playbook-blueprint -->
```json
{"slug": "moon-laundry", "title": "Moon Laundry", "idea": "Socks are portals.", "tier": null,
 "placement": "admin", "checkpoint": "illustrious", "artStyles": 1, "creator": "roster",
 "portraits": "per-option", "followers": 8, "partySize": 3, "villains": 3, "villainPerRun": true,
 "factions": 1, "romances": 1, "acts": 2, "encounters": 24, "quests": 6, "reveals": 3,
 "moments": 9, "stats": 2, "checks": "percent", "outcomes": "four-tier", "failForward": true,
 "endings": 4, "finaleBeats": 2, "saveStyle": "snapshot", "unreadable": "hold", "saveSlots": 0,
 "undo": "last-choice"}
```
<!-- /playbook-blueprint -->"""


def test_new_playbook_reads_a_forge_blueprint(tmp_path, monkeypatch):
    root, projects = _fixture_repo(tmp_path, monkeypatch)
    pitch = tmp_path / "pitch.txt"
    pitch.write_text(FORGE_PITCH)
    assert new_playbook.main(["moon-laundry", "Moon Laundry", "--blueprint", str(pitch)]) == 0

    pdir = projects / "moon-laundry"
    saved = yaml.safe_load((pdir / "BLUEPRINT.json").read_text())
    assert saved["endings"] == 4 and saved["checks"] == "percent"
    roadmap = yaml.safe_load((pdir / "roadmap.yaml").read_text())
    assert "24 encounters" in roadmap["goal"] and "4 unique endings" in roadmap["goal"]
    assert roadmap["notes_from_silas"].startswith("Forged in /admin/playbook-forge. Idea: Socks are portals.")
    brief = (pdir / "DESIGN-BRIEF.md").read_text()
    assert "## Blueprint from the Playbook Forge" in brief
    assert "| Outcome tiers | four-tier |" in brief


def test_read_blueprint_accepts_bare_json_and_rejects_other_text():
    assert new_playbook.read_blueprint('{"endings": 3}')["endings"] == 3
    try:
        new_playbook.read_blueprint('{"title": "no endings"}')
    except ValueError:
        pass
    else:
        raise AssertionError("a non-blueprint was accepted")
