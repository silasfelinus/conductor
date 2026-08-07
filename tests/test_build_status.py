from pathlib import Path

import scripts.build_status as build_status


def test_status_counts_real_lifecycle_states(tmp_path: Path, monkeypatch) -> None:
    projects = tmp_path / "projects"
    projects.mkdir()
    (tmp_path / "pitches").mkdir()
    (tmp_path / "project-overrides.yaml").write_text(
        "overrides:\n"
        "  - slug: finite\n    status: active\n"
        "  - slug: forever\n    status: continuous\n"
        "  - slug: shipped\n    status: finished\n",
        encoding="utf-8",
    )
    for slug in ("finite", "forever", "shipped"):
        path = projects / slug
        path.mkdir()
        (path / "roadmap.yaml").write_text(
            f"project: {slug}\nkind: software\ntasks:\n- id: t-001\n  status: {'done' if slug == 'shipped' else 'ready'}\n",
            encoding="utf-8",
        )
    monkeypatch.setattr(build_status, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_status, "PROJECTS_DIR", projects)
    monkeypatch.setattr(build_status, "PITCHES_DIR", tmp_path / "pitches")
    monkeypatch.setattr(build_status, "STATUS_FILE", tmp_path / "STATUS.md")
    monkeypatch.setattr(build_status, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    build_status.build_status()
    text = (tmp_path / "STATUS.md").read_text(encoding="utf-8")
    assert "| Active projects | 1 |" in text
    assert "| Continuous projects | 1 |" in text
    assert "| Finished projects | 1 |" in text
    assert "| forever | continuous | software |" in text
