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
    write_roadmap(_isolate_root, "demo", "project: demo\nkind: software\ntasks:\n- id: t-001\n  status: ready\n  stakes: reversible\n")

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


def test_duplicate_task_id_fails(_isolate_root, capsys):
    write_roadmap(
        _isolate_root,
        "demo",
        "project: demo\ntasks:\n"
        "- id: t-001\n  status: ready\n"
        "- id: t-002\n  status: ready\n"
        "- id: t-001\n  status: needs-human\n",
    )

    assert validate_roadmaps.main() == 1
    err = capsys.readouterr().err
    assert "duplicate task id(s)" in err
    assert "t-001" in err
    assert "t-002" not in err


def test_duplicate_task_id_reports_all_projects(_isolate_root, capsys):
    write_roadmap(
        _isolate_root,
        "demo-a",
        "project: demo-a\ntasks:\n- id: t-001\n  status: ready\n- id: t-001\n  status: ready\n",
    )
    write_roadmap(
        _isolate_root,
        "demo-b",
        "project: demo-b\ntasks:\n- id: t-001\n  status: ready\n",
    )

    assert validate_roadmaps.main() == 1
    err = capsys.readouterr().err
    assert "demo-a" in err
    assert "demo-b" not in err


def test_duplicate_task_ids_function_directly():
    tasks = [{"id": "t-001"}, {"id": "t-002"}, {"id": "t-001"}, {"id": "t-003"}, {"id": "t-003"}]
    assert validate_roadmaps.duplicate_task_ids(tasks) == ["t-001", "t-003"]


def test_active_project_with_no_open_tasks_fails_lifecycle_reconciliation(_isolate_root, capsys):
    (_isolate_root / "project-overrides.yaml").write_text(
        "overrides:\n  - slug: demo\n    status: active\n", encoding="utf-8"
    )
    write_roadmap(_isolate_root, "demo", "project: demo\ntasks:\n- id: t-001\n  status: done\n")
    assert validate_roadmaps.main() == 1
    assert "active project has no open tasks" in capsys.readouterr().err


def test_continuous_project_may_have_only_recurring_done_history(_isolate_root, capsys):
    (_isolate_root / "project-overrides.yaml").write_text(
        "overrides:\n  - slug: demo\n    status: continuous\n", encoding="utf-8"
    )
    write_roadmap(_isolate_root, "demo", "project: demo\ntasks:\n- id: t-001\n  status: done\n")
    assert validate_roadmaps.main() == 0


def test_unknown_project_lifecycle_fails(_isolate_root, capsys):
    (_isolate_root / "project-overrides.yaml").write_text(
        "overrides:\n  - slug: demo\n    status: immortal\n", encoding="utf-8"
    )
    write_roadmap(_isolate_root, "demo", "project: demo\ntasks:\n- id: t-001\n  status: ready\n")
    assert validate_roadmaps.main() == 1
    assert "invalid project lifecycle status" in capsys.readouterr().err


def test_invalid_task_stakes_fails_even_for_done_task(_isolate_root, capsys):
    write_roadmap(
        _isolate_root,
        "demo",
        "project: demo\nkind: software\ntasks:\n- id: t-001\n  status: done\n  stakes: high\n",
    )

    assert validate_roadmaps.main() == 1
    err = capsys.readouterr().err
    assert "invalid task stakes" in err
    assert "t-001" in err
    assert "'high'" in err


def test_supported_task_stakes_are_valid(_isolate_root, capsys):
    write_roadmap(
        _isolate_root,
        "demo",
        "project: demo\nkind: software\ntasks:\n"
        "- id: t-001\n  status: ready\n  stakes: reversible\n"
        "- id: t-002\n  status: ready\n  stakes: outward-facing\n"
        "- id: t-003\n  status: ready\n  stakes: irreversible\n",
    )

    assert validate_roadmaps.main() == 0
    assert "Roadmaps valid" in capsys.readouterr().out


def test_invalid_effective_project_kind_fails(_isolate_root, capsys):
    write_roadmap(
        _isolate_root,
        "demo",
        "project: demo\nkind: infrastructure\ntasks:\n- id: t-001\n  status: ready\n  stakes: reversible\n",
    )

    assert validate_roadmaps.main() == 1
    err = capsys.readouterr().err
    assert "invalid project kind" in err
    assert "infrastructure" in err


def test_override_kind_is_authoritative(_isolate_root, capsys):
    (_isolate_root / "project-overrides.yaml").write_text(
        "overrides:\n  - slug: demo\n    status: active\n    kind: software\n", encoding="utf-8"
    )
    write_roadmap(
        _isolate_root,
        "demo",
        "project: demo\nkind: infrastructure\ntasks:\n- id: t-001\n  status: ready\n  stakes: reversible\n",
    )

    assert validate_roadmaps.main() == 0
    assert "Roadmaps valid" in capsys.readouterr().out
