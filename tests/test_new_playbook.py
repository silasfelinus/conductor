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
