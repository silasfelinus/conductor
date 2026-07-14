import pytest

import scripts.challenge_runner as challenge_runner
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


def test_fetch_open_challenges_success(monkeypatch):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges?status=OPEN"): (
            200,
            {"success": True, "data": [{"slug": "haiku-showdown", "challengeType": "TEXT"}]},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    challenges = challenge_runner.fetch_open_challenges(BASE_URL)
    assert challenges == [{"slug": "haiku-showdown", "challengeType": "TEXT"}]


def test_fetch_open_challenges_error(monkeypatch):
    routes = {("GET", f"{BASE_URL}/api/challenges?status=OPEN"): (500, {"success": False, "message": "boom"})}
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    with pytest.raises(challenge_runner.ChallengeRunnerError, match="boom"):
        challenge_runner.fetch_open_challenges(BASE_URL)


def test_already_submitted_true(monkeypatch):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown/leaderboard"): (
            200,
            {"success": True, "data": {"leaderboard": [{"slug": "conductor-claude", "score": {}}]}},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    assert challenge_runner.already_submitted(BASE_URL, "haiku-showdown", "conductor-claude") is True


def test_already_submitted_false(monkeypatch):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown/leaderboard"): (
            200,
            {"success": True, "data": {"leaderboard": []}},
        )
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    assert challenge_runner.already_submitted(BASE_URL, "haiku-showdown", "conductor-claude") is False


def test_run_challenge_skips_unhandled_type(monkeypatch):
    challenge = {"slug": "icon-duel", "challengeType": "ART", "promptText": "Draw an icon."}

    outcome = challenge_runner.run_challenge(BASE_URL, challenge, "conductor-claude", "default", "key", dry_run=False)

    assert outcome == "skipped-type"


def test_run_challenge_skips_duplicate(monkeypatch):
    challenge = {"slug": "haiku-showdown", "challengeType": "TEXT", "promptText": "Write a haiku."}
    monkeypatch.setattr(challenge_runner, "already_submitted", lambda base_url, slug, contender: True)

    outcome = challenge_runner.run_challenge(BASE_URL, challenge, "conductor-claude", "default", "key", dry_run=False)

    assert outcome == "skipped-duplicate"


def test_run_challenge_dry_run_skips_generation_and_submission(monkeypatch):
    challenge = {"slug": "haiku-showdown", "challengeType": "TEXT", "promptText": "Write a haiku."}
    monkeypatch.setattr(challenge_runner, "already_submitted", lambda base_url, slug, contender: False)

    def boom(*args, **kwargs):
        raise AssertionError("should not be called in dry-run")

    monkeypatch.setattr(challenge_runner, "generate_answer", boom)
    monkeypatch.setattr(challenge_submit, "submit_challenge", boom)

    outcome = challenge_runner.run_challenge(BASE_URL, challenge, "conductor-claude", "default", "key", dry_run=True)

    assert outcome == "dry-run"


def test_run_challenge_submits_generated_answer(monkeypatch):
    challenge = {"slug": "haiku-showdown", "challengeType": "TEXT", "promptText": "Write a haiku."}
    monkeypatch.setattr(challenge_runner, "already_submitted", lambda base_url, slug, contender: False)
    monkeypatch.setattr(challenge_runner, "generate_answer", lambda prompt_text, api_key: "five/seven/five")

    calls = []

    def fake_submit(base_url, token, slug, contender_slug, variant_key, output_text, prompt_used=None):
        calls.append((base_url, token, slug, contender_slug, variant_key, output_text, prompt_used))
        return {"id": 7}

    monkeypatch.setattr(challenge_submit, "submit_challenge", fake_submit)

    outcome = challenge_runner.run_challenge(BASE_URL, challenge, "conductor-claude", "default", "key", dry_run=False)

    assert outcome == "submitted"
    assert calls == [(BASE_URL, challenge_submit.KR_API_TOKEN, "haiku-showdown", "conductor-claude", "default", "five/seven/five", "Write a haiku.")]


def test_generate_answer_success(monkeypatch):
    captured = {}

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b'{"content": [{"type": "text", "text": "five/seven/five"}]}'

    def fake_urlopen(req, timeout=120):
        captured["req"] = req
        return FakeResp()

    monkeypatch.setattr(challenge_runner.urllib.request, "urlopen", fake_urlopen)

    answer = challenge_runner.generate_answer("Write a haiku.", "sk-test")

    assert answer == "five/seven/five"
    assert captured["req"].get_header("X-api-key") == "sk-test"


def test_generate_answer_empty_text_raises(monkeypatch):
    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b'{"content": []}'

    monkeypatch.setattr(challenge_runner.urllib.request, "urlopen", lambda req, timeout=120: FakeResp())

    with pytest.raises(challenge_runner.ChallengeRunnerError, match="no text content"):
        challenge_runner.generate_answer("Write a haiku.", "sk-test")


def test_main_requires_api_key_without_dry_run(monkeypatch, capsys):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    exit_code = challenge_runner.main(["--all", "--kr-base-url", BASE_URL])

    assert exit_code == 1
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


def test_main_requires_kr_token_without_dry_run(monkeypatch, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setattr(challenge_submit, "KR_API_TOKEN", "")

    exit_code = challenge_runner.main(["--all", "--kr-base-url", BASE_URL])

    assert exit_code == 1
    assert "KR_API_TOKEN" in capsys.readouterr().err


def test_main_dry_run_no_open_challenges(monkeypatch, capsys):
    routes = {("GET", f"{BASE_URL}/api/challenges?status=OPEN"): (200, {"success": True, "data": []})}
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    exit_code = challenge_runner.main(["--all", "--dry-run", "--kr-base-url", BASE_URL])

    assert exit_code == 0
    assert "No open challenges found." in capsys.readouterr().out


def test_main_dry_run_summarizes_mixed_outcomes(monkeypatch, capsys):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges?status=OPEN"): (
            200,
            {
                "success": True,
                "data": [
                    {"slug": "haiku-showdown", "challengeType": "TEXT", "promptText": "Write a haiku."},
                    {"slug": "icon-duel", "challengeType": "ART", "promptText": "Draw an icon."},
                ],
            },
        ),
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown/leaderboard"): (
            200,
            {"success": True, "data": {"leaderboard": []}},
        ),
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    exit_code = challenge_runner.main(["--all", "--dry-run", "--kr-base-url", BASE_URL])

    out = capsys.readouterr().out
    assert exit_code == 0
    assert "2 attempted" in out
    assert "1 dry-run" in out
    assert "1 skipped" in out


def test_main_single_challenge_flag_fetches_directly(monkeypatch, capsys):
    routes = {
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown"): (
            200,
            {"success": True, "data": {"slug": "haiku-showdown", "challengeType": "TEXT", "promptText": "Write a haiku."}},
        ),
        ("GET", f"{BASE_URL}/api/challenges/haiku-showdown/leaderboard"): (
            200,
            {"success": True, "data": {"leaderboard": [{"slug": "conductor-claude", "score": {}}]}},
        ),
    }
    monkeypatch.setattr(challenge_submit, "http_json", make_fake_http(routes))

    exit_code = challenge_runner.main(["--challenge", "haiku-showdown", "--dry-run", "--kr-base-url", BASE_URL])

    out = capsys.readouterr().out
    assert exit_code == 0
    assert "1 attempted" in out
    assert "1 skipped" in out
