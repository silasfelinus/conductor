import importlib.util
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "worker_merge_pr.py"


def load_module():
    spec = importlib.util.spec_from_file_location("worker_merge_pr", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_merge_helper_marks_done_immediately_after_merge(monkeypatch):
    module = load_module()
    calls = []

    def fake_gh(repo, path, token, *, method="GET", body=None):
        calls.append(("gh", repo, path, method, body))
        assert path == "pulls/123/merge"
        assert method == "PUT"
        assert body == {"merge_method": "squash"}
        return {"merged": True, "sha": "abc123"}

    def fake_run(command, cwd=None, text=False, capture_output=False):
        calls.append(("subprocess", command, cwd, text, capture_output))
        return subprocess.CompletedProcess(command, 0, "", "")

    def fake_git(*args):
        calls.append(("git", args))
        return ""

    monkeypatch.setattr(module, "_gh", fake_gh)
    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(module, "run_git", fake_git)

    result = module.main(["123", "conductor", "t-021", "--token", "token"])

    assert result == 0
    merge_index = next(i for i, call in enumerate(calls) if call[0] == "gh")
    status_index = next(
        i
        for i, call in enumerate(calls)
        if call[0] == "subprocess" and "worker_task_status.py" in str(call[1])
    )
    assert merge_index < status_index
    status_command = calls[status_index][1]
    assert status_command[-5:] == ["done", "conductor", "t-021", "--note", "Completed in PR #123."]
    assert ("git", ("commit", "-m", "done: conductor/t-021 [skip ci]")) in calls
    assert ("git", ("push", "origin", "main")) in calls


def test_dry_run_does_not_call_github_or_git(monkeypatch, capsys):
    module = load_module()

    monkeypatch.setattr(module, "_gh", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no gh")))
    monkeypatch.setattr(module, "run_git", lambda *args: (_ for _ in ()).throw(AssertionError("no git")))

    result = module.main(["123", "conductor", "t-021", "--dry-run"])

    assert result == 0
    output = capsys.readouterr().out
    assert "would squash-merge silasfelinus/conductor PR #123" in output
    assert "would mark conductor/t-021 done" in output
