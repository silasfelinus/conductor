import io
import json

import pytest

import scripts.challenge_submit as challenge_submit


BASE_URL = "https://kind-robots.example"


def make_fake_http(routes):
    """routes: {(method, url): (status, body)}"""

    def fake_http_json(method, url, token="", body=None, timeout=30):
        key = (method, url)
        if key not in routes:
            raise AssertionError(f"unexpected request: {method} {url}")
        return routes[key]

    return fake_http_json


def test_fetch_challenge_success(monkeypatch):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown"): (
            200,
            {"success": True, "data": {"slug": "haiku-showdown", "promptText": "Write a haiku."}},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    data = challenge_submit.fetch_challenge(BASE_URL, "haiku-showdown")
    assert data["promptText"] == "Write a haiku."


def test_fetch_challenge_not_found(monkeypatch):
    routes = {("GET", f"{BASE_URL}/api/challenges/missing"): (404, {"success": False, "message": "Challenge not found."})}
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    with pytest.raises(challenge_submit.ChallengeSubmitError, match="not found"):
        challenge_submit.fetch_challenge(BASE_URL, "missing")


def test_submit_challenge_requires_token(monkeypatch):
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http({}))

    with pytest.raises(challenge_submit.ChallengeSubmitError, match="KR_API_TOKEN"):
        challenge_submit.submit_challenge(BASE_URL, "", "haiku-showdown", "conductor-claude", "default", "output")


def test_submit_challenge_duplicate_rejected(monkeypatch):
    routes = {
        ("POST", f"{BASE_URL}/api/challenges/haiku-showdown/submissions"): (
            409,
            {"success": False, "message": "This contender already submitted the same variant for this challenge."},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    with pytest.raises(challenge_submit.ChallengeSubmitError, match="submission rejected"):
        challenge_submit.submit_challenge(BASE_URL, "tok", "haiku-showdown", "conductor-claude", "default", "output")


def test_submit_challenge_success(monkeypatch):
    calls = []

    def fake_http_json(method, url, token="", body=None, timeout=30):
        calls.append((method, url, token, body))
        return 201, {"success": True, "data": {"id": 42}}

    monkeypatch.setattr(challenge_submit, "http_json", fake_http_json)

    result = challenge_submit.submit_challenge(
        BASE_URL, "tok", "haiku-showdown", "conductor-claude", "random-1", "five/seven/five", prompt_used="Write a haiku."
    )

    assert result == {"id": 42}
    method, url, token, body = calls[0]
    assert method == "POST"
    assert url == f"{BASE_URL}/api/challenges/haiku-showdown/submissions"
    assert token == "tok"
    assert body == {
        "contenderSlug": "conductor-claude",
        "variantKey": "random-1",
        "outputText": "five/seven/five",
        "promptUsed": "Write a haiku.",
    }


def test_find_standing_returns_rank_and_entry():
    leaderboard = [
        {"slug": "portos-agent", "score": {"netScore": 5}},
        {"slug": "conductor-claude", "score": {"netScore": 2}},
    ]
    rank, entry = challenge_submit.find_standing(leaderboard, "conductor-claude")
    assert rank == 2
    assert entry["slug"] == "conductor-claude"


def test_find_standing_missing_contender_returns_none():
    assert challenge_submit.find_standing([], "conductor-claude") is None


def test_read_output_from_stdin(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("  agent answer  \n"))
    assert challenge_submit.read_output("-") == "agent answer"


def test_read_output_from_file(tmp_path):
    path = tmp_path / "answer.txt"
    path.write_text("the answer\n")
    assert challenge_submit.read_output(str(path)) == "the answer"


def test_read_output_empty_raises(tmp_path):
    path = tmp_path / "answer.txt"
    path.write_text("   \n")
    with pytest.raises(challenge_submit.ChallengeSubmitError, match="no output text"):
        challenge_submit.read_output(str(path))


def test_main_without_output_prints_prompt_only(monkeypatch, capsys):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown"): (
            200,
            {"success": True, "data": {"slug": "haiku-showdown", "title": "Haiku Showdown", "challengeType": "TEXT", "promptText": "Write a haiku."}},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    exit_code = challenge_submit.main(["haiku-showdown", "--kr-base-url", BASE_URL])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.out == "Write a haiku.\n"
    assert "Haiku Showdown" in captured.err


def test_main_dry_run_does_not_submit(monkeypatch, tmp_path, capsys):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown"): (
            200,
            {"success": True, "data": {"slug": "haiku-showdown", "promptText": "Write a haiku."}},
        )
    }

    def fake_http_json(method, url, token="", body=None, timeout=30):
        key = (method, url)
        if key not in routes:
            raise AssertionError(f"unexpected live request in dry-run: {method} {url}")
        return routes[key]

    monkeypatch.setattr(challenge_submit, "http_json", fake_http_json)

    output_file = tmp_path / "answer.txt"
    output_file.write_text("five/seven/five")

    exit_code = challenge_submit.main(
        ["haiku-showdown", "--output", str(output_file), "--dry-run", "--kr-base-url", BASE_URL]
    )

    assert exit_code == 0
    assert "DRY RUN" in capsys.readouterr().err


def test_main_full_submission_flow_prints_standing(monkeypatch, tmp_path, capsys):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown"): (
            200,
            {"success": True, "data": {"slug": "haiku-showdown", "promptText": "Write a haiku."}},
        ),
        ("POST", f"{BASE_URL}/api/challenges/haiku-showdown/submissions"): (
            201,
            {"success": True, "data": {"id": 7}},
        ),
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown/leaderboard"): (
            200,
            {
                "success": True,
                "data": {
                    "leaderboard": [
                        {"slug": "portos-agent", "score": {"netScore": 5, "votes": 5}},
                        {"slug": "conductor-claude", "score": {"netScore": 0, "votes": 0}},
                    ]
                },
            },
        ),
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))
    monkeypatch.setattr(challenge_submit, "KR_API_TOKEN", "tok")

    output_file = tmp_path / "answer.txt"
    output_file.write_text("five/seven/five")

    exit_code = challenge_submit.main(["haiku-showdown", "--output", str(output_file), "--kr-base-url", BASE_URL])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Submission #7 created for conductor-claude" in out
    assert "#2 of 2" in out


def test_main_reports_missing_token_as_error(monkeypatch, tmp_path, capsys):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown"): (
            200,
            {"success": True, "data": {"slug": "haiku-showdown", "promptText": "Write a haiku."}},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))
    monkeypatch.setattr(challenge_submit, "KR_API_TOKEN", "")

    output_file = tmp_path / "answer.txt"
    output_file.write_text("five/seven/five")

    exit_code = challenge_submit.main(["haiku-showdown", "--output", str(output_file), "--kr-base-url", BASE_URL])

    assert exit_code == 1
    assert "KR_API_TOKEN" in capsys.readouterr().err
