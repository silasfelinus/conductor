import io

from scripts.check_pr_handoff_template import (
    REQUIRED_SECTIONS,
    github_error_annotation,
    main,
    missing_sections,
)


def complete_body() -> str:
    return "\n\n".join(f"{heading}\ncontent" for heading in REQUIRED_SECTIONS)


def test_complete_handoff_has_no_missing_sections():
    assert missing_sections(complete_body()) == []


def test_missing_stakes_is_reported():
    body = complete_body().replace("### Stakes\ncontent\n\n", "")
    assert missing_sections(body) == ["### Stakes"]


def test_github_annotation_names_missing_heading():
    assert github_error_annotation("### Stakes") == (
        "::error title=Worker PR handoff incomplete::Missing required heading: ### Stakes"
    )


def test_flags_for_reviewer_is_not_required_when_empty():
    assert "### Flags for Reviewer" not in REQUIRED_SECTIONS


def test_main_non_worker_branch_skips_without_reading_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["check_pr_handoff_template.py", "--head-ref", "claude/foo"])
    monkeypatch.setattr("sys.stdin", io.StringIO(""))

    exit_code = main()

    assert exit_code == 0
    assert "SKIP" in capsys.readouterr().out


def test_main_complete_body_exits_zero(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["check_pr_handoff_template.py", "--head-ref", "worker/demo-t-001"])
    monkeypatch.setattr("sys.stdin", io.StringIO(complete_body()))

    exit_code = main()

    assert exit_code == 0
    assert "OK" in capsys.readouterr().out


def test_main_missing_stakes_exits_one_and_annotates_stderr(monkeypatch, capsys):
    body = complete_body().replace("### Stakes\ncontent\n\n", "")
    monkeypatch.setattr("sys.argv", ["check_pr_handoff_template.py", "--head-ref", "worker/demo-t-001"])
    monkeypatch.setattr("sys.stdin", io.StringIO(body))

    exit_code = main()

    assert exit_code == 1
    err = capsys.readouterr().err
    assert github_error_annotation("### Stakes") in err
    assert "### Stakes" in err
