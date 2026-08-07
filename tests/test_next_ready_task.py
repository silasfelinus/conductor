from pathlib import Path

import scripts.next_ready_task as selector


def write_yaml(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def configure_repo(tmp_path: Path, monkeypatch) -> Path:
    projects_dir = tmp_path / "projects"
    monkeypatch.setattr(selector, "ROOT", tmp_path)
    monkeypatch.setattr(selector, "PROJECTS_DIR", projects_dir)
    monkeypatch.setattr(selector, "PRIORITY_FILE", projects_dir / "priority.yaml")
    monkeypatch.setattr(selector, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    return projects_dir


def write_project(projects_dir: Path, slug: str, tasks: str, kind: str = "software") -> None:
    write_yaml(
        projects_dir / slug / "roadmap.yaml",
        f"""project: {slug}
kind: {kind}
tasks:
{tasks}
""",
    )


def test_first_ready_task_honors_priority_order(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - beta\n  - alpha\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: alpha\n    status: active\n  - slug: beta\n    status: active\n",
    )
    write_project(
        projects_dir,
        "alpha",
        """- id: t-001
  title: Alpha task
  status: ready
  stakes: reversible
""",
    )
    write_project(
        projects_dir,
        "beta",
        """- id: t-002
  title: Beta task
  status: ready
  stakes: reversible
""",
    )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["project"] == "beta"
    assert result["task_id"] == "t-002"


def test_paused_and_retired_projects_are_skipped(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - paused\n  - retired\n  - active\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: paused\n    status: paused\n  - slug: retired\n    status: retired\n  - slug: active\n    status: active\n",
    )
    for slug in ("paused", "retired", "active"):
        write_project(
            projects_dir,
            slug,
            f"""- id: t-001
  title: {slug} task
  status: ready
  stakes: reversible
""",
        )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["project"] == "active"


def test_dependency_chain_must_be_done(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - blocked\n  - unblocked\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: blocked\n    status: active\n  - slug: unblocked\n    status: active\n",
    )
    write_project(
        projects_dir,
        "blocked",
        """- id: t-001
  title: Upstream task
  status: review
  stakes: reversible
- id: t-002
  title: Dependent task
  status: ready
  depends_on: t-001
  stakes: reversible
""",
    )
    write_project(
        projects_dir,
        "unblocked",
        """- id: t-003
  title: Independent task
  status: ready
  stakes: reversible
""",
    )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["project"] == "unblocked"
    assert result["task_id"] == "t-003"


def test_gate_human_dependency_requires_approval(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - gated\n  - fallback\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: gated\n    status: active\n  - slug: fallback\n    status: active\n",
    )
    write_project(
        projects_dir,
        "gated",
        """- id: t-001
  title: Human gate
  status: done
  gate_human: true
  approved_by_human: false
  stakes: reversible
- id: t-002
  title: Waiting on human gate
  status: ready
  depends_on: t-001
  stakes: reversible
""",
    )
    write_project(
        projects_dir,
        "fallback",
        """- id: t-003
  title: Fallback task
  status: ready
  stakes: reversible
""",
    )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["project"] == "fallback"


def test_gate_human_dependency_allows_approved_done_task(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - gated\n")
    write_yaml(tmp_path / "project-overrides.yaml", "overrides:\n  - slug: gated\n    status: active\n")
    write_project(
        projects_dir,
        "gated",
        """- id: t-001
  title: Human gate
  status: done
  gate_human: true
  approved_by_human: true
  stakes: reversible
- id: t-002
  title: Ready after approval
  status: ready
  depends_on: t-001
  stakes: reversible
""",
    )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["project"] == "gated"
    assert result["task_id"] == "t-002"


def test_umbrella_task_skipped_while_delegate_is_open(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - interface-vision\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: interface-vision\n    status: active\n",
    )
    write_project(
        projects_dir,
        "interface-vision",
        """- id: t-017
  title: Umbrella sweep
  status: ready
  stakes: reversible
  remaining_scope_task: t-058
- id: t-058
  title: Dedicated follow-on
  status: ready
  stakes: reversible
""",
    )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["task_id"] == "t-058"


def test_umbrella_task_claimable_again_once_delegate_done(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - interface-vision\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: interface-vision\n    status: active\n",
    )
    write_project(
        projects_dir,
        "interface-vision",
        """- id: t-017
  title: Umbrella sweep
  status: ready
  stakes: reversible
  remaining_scope_task: t-058
- id: t-058
  title: Dedicated follow-on
  status: done
  stakes: reversible
""",
    )

    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())

    assert result is not None
    assert result["task_id"] == "t-017"


def test_continuous_project_waits_behind_any_active_ready_work(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - forever\n  - finite\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: forever\n    status: continuous\n  - slug: finite\n    status: active\n",
    )
    write_project(projects_dir, "forever", "- id: t-001\n  title: Continuous task\n  status: ready\n  stakes: reversible\n")
    write_project(projects_dir, "finite", "- id: t-001\n  title: Finite task\n  status: ready\n  stakes: reversible\n")
    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())
    assert result is not None
    assert result["project"] == "finite"


def test_continuous_project_runs_when_active_queue_is_empty(tmp_path: Path, monkeypatch) -> None:
    projects_dir = configure_repo(tmp_path, monkeypatch)
    write_yaml(projects_dir / "priority.yaml", "order:\n  - forever\n  - finite\n")
    write_yaml(
        tmp_path / "project-overrides.yaml",
        "overrides:\n  - slug: forever\n    status: continuous\n  - slug: finite\n    status: active\n",
    )
    write_project(projects_dir, "forever", "- id: t-001\n  title: Continuous task\n  status: ready\n  stakes: reversible\n")
    write_project(projects_dir, "finite", "- id: t-001\n  title: Finite task\n  status: done\n  stakes: reversible\n")
    result = selector.first_ready_task(selector.load_priority_order(), selector.load_workable_overrides())
    assert result is not None
    assert result["project"] == "forever"
