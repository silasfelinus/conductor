from pathlib import Path

import pytest

import scripts.validate_roadmaps as validate_roadmaps


@pytest.fixture(autouse=True)
def _isolate_root(tmp_path, monkeypatch):
    monkeypatch.setattr(validate_roadmaps, "ROOT", tmp_path)
    return tmp_path


def write_roadmap(root: Path, project: str, text: str) -> None:
    path = root / "projects" / project / "roadmap.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_valid_roadmaps_exit_zero(_isolate_root, capsys):
    write_roadmap(_isolate_root, "demo", "project: demo\ntasks:\n- id: t-001\n  status: ready\n")

    assert validate_roadmaps.main() == 0
    assert "Roadmaps valid" in capsys.readouterr().out


def test_missing_tasks_list_fails(_isolate_root, capsys):
    write_roadmap(_isolate_root, "demo", "project: demo\ntasks: not-a-list\n")

    assert validate_roadmaps.main() == 1
    assert "invalid roadmap" in capsys.readouterr().err


def test_non_mapping_document_fails(_isolate_root, capsys):
    write_roadmap(_isolate_root, "demo", "- just\n- a\n- list\n")

    assert validate_roadmaps.main() == 1
    assert "invalid roadmap" in capsys.readouterr().err


def test_no_roadmaps_is_fine(_isolate_root, capsys):
    (_isolate_root / "projects").mkdir()

    assert validate_roadmaps.main() == 0
    assert "Roadmaps valid" in capsys.readouterr().out
