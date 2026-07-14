from __future__ import annotations

import scripts.ci_janitor as janitor


def test_existing_markers_find_completed_and_open_incidents():
    todos = [
        {
            "status": "DONE",
            "description": "ci-janitor:owner/repo:cypress.yml:41\nFinished",
        },
        {
            "status": "OPEN",
            "description": "Context\nci-janitor:owner/repo:typecheck.yml:42",
        },
        {"status": "OPEN", "description": None},
    ]

    assert janitor.existing_markers(todos) == {
        "ci-janitor:owner/repo:cypress.yml:41",
        "ci-janitor:owner/repo:typecheck.yml:42",
    }


def test_main_stays_silent_when_latest_run_is_green(monkeypatch, capsys):
    monkeypatch.setenv("KR_API_TOKEN", "test-token")
    monkeypatch.setattr(janitor, "fetch_todos", lambda _token: [])
    monkeypatch.setattr(
        janitor,
        "latest_completed_run",
        lambda _check, _token: {
            "id": 101,
            "conclusion": "success",
            "html_url": "https://example.test/runs/101",
        },
    )

    assert janitor.main() == 0
    output = capsys.readouterr().out
    assert "red=0" in output
    assert "created=0" in output


def test_main_creates_one_high_priority_todo_for_new_red_run(monkeypatch):
    monkeypatch.setenv("KR_API_TOKEN", "test-token")
    monkeypatch.setattr(janitor, "fetch_todos", lambda _token: [])
    monkeypatch.setattr(
        janitor,
        "latest_completed_run",
        lambda _check, _token: {
            "id": 202,
            "conclusion": "failure",
            "html_url": "https://example.test/runs/202",
            "head_sha": "abc123",
        },
    )

    calls = []

    def fake_create(check, run, token):
        calls.append((check, run, token))
        return {"success": True, "data": {"id": 77}}

    monkeypatch.setattr(janitor, "create_incident_todo", fake_create)

    assert janitor.main() == 0
    assert len(calls) == 1
    assert calls[0][1]["id"] == 202
    assert calls[0][2] == "test-token"


def test_main_does_not_duplicate_a_known_run(monkeypatch):
    check = janitor.DEFAULT_CHECKS[0]
    marker = janitor.todo_marker(check, 303)
    monkeypatch.setenv("KR_API_TOKEN", "test-token")
    monkeypatch.setattr(
        janitor,
        "fetch_todos",
        lambda _token: [{"status": "DONE", "description": marker}],
    )
    monkeypatch.setattr(
        janitor,
        "latest_completed_run",
        lambda _check, _token: {
            "id": 303,
            "conclusion": "timed_out",
            "html_url": "https://example.test/runs/303",
        },
    )
    monkeypatch.setattr(
        janitor,
        "create_incident_todo",
        lambda *_args: (_ for _ in ()).throw(AssertionError("duplicate Todo created")),
    )

    assert janitor.main() == 0
