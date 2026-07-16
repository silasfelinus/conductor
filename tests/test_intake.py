import yaml

import scripts.intake as intake


def _fixture_repo(tmp_path, monkeypatch, *, with_control=True):
    """Build a minimal repo tree and point intake's module globals at it."""
    projects = tmp_path / "projects"
    (projects / "_template").mkdir(parents=True)
    (projects / "_template" / "roadmap.yaml").write_text(
        "project: REPLACE-ME\n"
        "kind: software        # software | content | proposal\n\n"
        "milestones:\n  - id: m1\n    title: SHAPE\n    weight: 25\n    status: not-started\n"
        "tasks:\n  - id: t-001\n    milestone: m1\n    title: First\n    status: ready\n"
        "    owner: null\n    passes: 0\n    stakes: reversible\n"
    )
    (projects / "priority.yaml").write_text("order:\n  - brainstorm\n")
    (tmp_path / "project-overrides.yaml").write_text("overrides: []\n")
    (projects / "art-prompts.yaml").write_text("images: []\nrequests: []\n")
    (tmp_path / "repos.yaml").write_text("repos: []\n")
    if with_control:
        (tmp_path / "CONTROL.md").write_text(
            "# CONTROL.md\n\n## Global overview\n\nsome global steering.\n\n"
            "## Per-project direction\n\n### existing-proj  (software)\n"
            "**Direction:** already here.\n**Notes:**\n- (your notes)\n"
        )

    monkeypatch.setattr(intake, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(intake, "PROJECTS_DIR", projects)
    monkeypatch.setattr(intake, "TEMPLATE_DIR", projects / "_template")
    monkeypatch.setattr(intake, "PRIORITY_FILE", projects / "priority.yaml")
    monkeypatch.setattr(intake, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(intake, "ART_PROMPTS_FILE", projects / "art-prompts.yaml")
    monkeypatch.setattr(intake, "REPOS_FILE", tmp_path / "repos.yaml")
    monkeypatch.setattr(intake, "CONTROL_FILE", tmp_path / "CONTROL.md")
    return tmp_path, projects


def test_scaffold_touches_every_surface(tmp_path, monkeypatch):
    root, projects = _fixture_repo(tmp_path, monkeypatch)
    intake.main(["cosmic-loom", "--kind", "content", "--title", "Cosmic Loom",
                 "--goal", "Weave star maps into wearable art."])

    pdir = projects / "cosmic-loom"
    # project files
    assert (pdir / "roadmap.yaml").exists()
    assert (pdir / "DESIGN-BRIEF.md").exists()
    assert (pdir / "CHANGELOG.md").exists()
    # roadmap slug/kind substituted
    rm = yaml.safe_load((pdir / "roadmap.yaml").read_text())
    assert rm["project"] == "cosmic-loom" and rm["kind"] == "content"
    # priority: inserted before brainstorm
    order = yaml.safe_load((projects / "priority.yaml").read_text())["order"]
    assert "cosmic-loom" in order and order.index("cosmic-loom") < order.index("brainstorm")
    # overrides: registered active/content
    ov = yaml.safe_load((root / "project-overrides.yaml").read_text())["overrides"]
    entry = next(e for e in ov if e["slug"] == "cosmic-loom")
    assert entry["status"] == "active" and entry["kind"] == "content"
    # art-prompts: icon/card/hero queued
    art = yaml.safe_load((projects / "art-prompts.yaml").read_text())["images"]
    assert any(e["project"] == "cosmic-loom" and {"icon", "card", "hero"} <= e.keys() for e in art)
    # repos registered
    repos = yaml.safe_load((root / "repos.yaml").read_text())["repos"]
    assert any(r["slug"] == "cosmic-loom" for r in repos)
    # CONTROL.md block appended, preserving the existing one
    control = (root / "CONTROL.md").read_text()
    assert "### cosmic-loom  (content)" in control
    assert "### existing-proj  (software)" in control


def test_design_brief_uses_title_and_goal(tmp_path, monkeypatch):
    _, projects = _fixture_repo(tmp_path, monkeypatch)
    intake.main(["star-forge", "--title", "Star Forge", "--goal", "Mint constellations on demand."])
    brief = (projects / "star-forge" / "DESIGN-BRIEF.md").read_text()
    assert brief.startswith("# Star Forge — Design Brief")
    assert "Mint constellations on demand." in brief
    assert "## MVP scope" in brief and "## Out of scope / guardrails" in brief


def test_title_and_goal_default_from_slug_and_desc(tmp_path, monkeypatch):
    _, projects = _fixture_repo(tmp_path, monkeypatch)
    intake.main(["tide-pool", "--desc", "A pool of tides."])
    brief = (projects / "tide-pool" / "DESIGN-BRIEF.md").read_text()
    assert brief.startswith("# Tide Pool — Design Brief")   # titleized slug
    assert "A pool of tides." in brief                       # goal fell back to desc


def test_control_block_goes_inside_per_project_section(tmp_path, monkeypatch):
    root, _ = _fixture_repo(tmp_path, monkeypatch)
    intake.main(["moon-mill", "--kind", "software", "--goal", "Grind moonlight into flour."])
    control = (root / "CONTROL.md").read_text()
    # new block appears after the section header, not before it
    assert control.index("## Per-project direction") < control.index("### moon-mill  (software)")
    assert "**Direction:** Grind moonlight into flour." in control


def test_control_block_appends_section_when_missing(tmp_path, monkeypatch):
    root, _ = _fixture_repo(tmp_path, monkeypatch, with_control=True)
    (root / "CONTROL.md").write_text("# CONTROL.md\n\n## Global overview\n\nno per-project section yet.\n")
    intake.main(["salt-glass"])
    control = (root / "CONTROL.md").read_text()
    assert "## Per-project direction" in control
    assert "### salt-glass  (software)" in control


def test_register_control_block_is_idempotent(tmp_path, monkeypatch):
    root, _ = _fixture_repo(tmp_path, monkeypatch)
    intake.register_control_block("dup-proj", "software", "once")
    intake.register_control_block("dup-proj", "software", "twice")
    assert (root / "CONTROL.md").read_text().count("### dup-proj  (software)") == 1


def test_existing_project_dir_aborts(tmp_path, monkeypatch):
    _, projects = _fixture_repo(tmp_path, monkeypatch)
    (projects / "taken").mkdir()
    try:
        intake.main(["taken"])
        assert False, "expected SystemExit"
    except SystemExit as e:
        assert e.code == 1
