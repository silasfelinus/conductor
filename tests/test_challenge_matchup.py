import json
from pathlib import Path

import pytest

import scripts.challenge_matchup as matchup
import scripts.challenge_submit as challenge_submit


BASE_URL = "https://kind-robots.example"


def test_load_inline_json_and_list_shortcut():
    spec = matchup.load_matchup_spec(
        json.dumps([{"contender": "claude-fable"}, {"contender": "openai-gpt"}])
    )
    assert [entry["contender"] for entry in spec["contenders"]] == [
        "claude-fable",
        "openai-gpt",
    ]


def test_load_yaml_file(tmp_path: Path):
    path = tmp_path / "matchup.yaml"
    path.write_text(
        "contenders:\n  - contender: claude-opus\n    variantKey: detailed\n",
        encoding="utf-8",
    )
    spec = matchup.load_matchup_spec(str(path))
    assert spec["contenders"][0]["variantKey"] == "detailed"


def test_load_spec_rejects_empty_contenders():
    with pytest.raises(matchup.ChallengeMatchupError, match="non-empty contenders"):
        matchup.load_matchup_spec('{"contenders": []}')


def test_build_prompt_and_settings_override():
    prompt = matchup.build_prompt(
        "Base prompt", {"promptPrefix": "Before", "promptSuffix": "After"}
    )
    assert prompt == "Before\n\nBase prompt\n\nAfter"
    assert matchup.merge_settings(
        {"temperature": 0.2, "max_tokens": 100}, {"temperature": 1.0}
    ) == {"temperature": 1.0, "max_tokens": 100}


def test_fetch_contenders(monkeypatch):
    def fake_http(method, url, token="", body=None, timeout=30):
        assert (method, url) == ("GET", f"{BASE_URL}/api/contenders")
        return 200, {
            "success": True,
            "data": [
                {"slug": "claude-fable", "generator": "claude-api"},
                {"slug": "art-sd", "generator": "art-sd"},
            ],
        }

    monkeypatch.setattr(challenge_submit, "http_json", fake_http)
    contenders = matchup.fetch_contenders(BASE_URL)
    assert set(contenders) == {"claude-fable", "art-sd"}


def test_generate_anthropic_uses_contender_model_and_settings(monkeypatch):
    captured = {}

    def fake_request(url, body, headers, timeout=120):
        captured.update(url=url, body=body, headers=headers)
        return {"content": [{"type": "text", "text": "answer"}]}

    monkeypatch.setattr(matchup, "request_json", fake_request)
    answer = matchup.generate_anthropic(
        "Prompt",
        {"model": "claude-opus-test"},
        {"temperature": 0.7, "max_tokens": 333, "system": "Be exact"},
        "anthropic-key",
    )
    assert answer == "answer"
    assert captured["url"] == matchup.ANTHROPIC_URL
    assert captured["body"] == {
        "model": "claude-opus-test",
        "max_tokens": 333,
        "messages": [{"role": "user", "content": "Prompt"}],
        "temperature": 0.7,
        "system": "Be exact",
    }
    assert captured["headers"]["x-api-key"] == "anthropic-key"


def test_generate_openai_uses_configured_model(monkeypatch):
    captured = {}

    def fake_request(url, body, headers, timeout=120):
        captured.update(url=url, body=body, headers=headers)
        return {"choices": [{"message": {"content": "open answer"}}]}

    monkeypatch.setattr(matchup, "request_json", fake_request)
    answer = matchup.generate_openai(
        "Prompt",
        {"model": "gpt-test"},
        {"temperature": 1.0, "maxTokens": 500},
        "openai-key",
    )
    assert answer == "open answer"
    assert captured["url"] == matchup.OPENAI_CHAT_URL
    assert captured["body"]["model"] == "gpt-test"
    assert captured["body"]["max_tokens"] == 500
    assert captured["headers"]["Authorization"] == "Bearer openai-key"


def test_enqueue_art_polls_until_real_art_image(monkeypatch):
    polls = iter(
        [
            {"success": True, "data": {"job": {"status": "PENDING"}}},
            {
                "success": True,
                "data": {"job": {"status": "DONE", "artImageId": 91}},
            },
        ]
    )
    calls = []

    def fake_http(method, url, token="", body=None, timeout=30):
        calls.append((method, url, token, body))
        if method == "POST":
            return 201, {"success": True, "data": {"jobId": 7}}
        return 200, next(polls)

    monkeypatch.setattr(challenge_submit, "http_json", fake_http)
    monkeypatch.setattr(matchup.time, "sleep", lambda seconds: None)
    art_id = matchup.enqueue_art(
        BASE_URL,
        "kr-token",
        "Paint a moon",
        "comfy-flux",
        {"width": 1024, "temperature": 999},
        poll_seconds=0,
        timeout_seconds=20,
    )
    assert art_id == 91
    assert calls[0][3]["engine"] == "flux"
    assert calls[0][3]["width"] == 1024
    assert "temperature" not in calls[0][3]
    assert calls[-1][1] == f"{BASE_URL}/api/art/queue/7"


def test_generate_openai_image_requires_user_id(monkeypatch):
    monkeypatch.delenv("KR_USER_ID", raising=False)
    with pytest.raises(matchup.ChallengeMatchupError, match="KR_USER_ID"):
        matchup.generate_openai_image(BASE_URL, "kr-token", "Paint", {})


def test_generate_openai_image_returns_saved_art_id(monkeypatch):
    captured = {}

    def fake_http(method, url, token="", body=None, timeout=30):
        captured.update(method=method, url=url, token=token, body=body)
        return 201, {"success": True, "data": {"id": 44}}

    monkeypatch.setattr(challenge_submit, "http_json", fake_http)
    art_id = matchup.generate_openai_image(
        BASE_URL,
        "kr-token",
        "Paint",
        {"userId": 10, "size": "1024x1536"},
    )
    assert art_id == 44
    assert captured["body"]["userId"] == 10
    assert captured["body"]["size"] == "1024x1536"
    assert captured["body"]["isPublic"] is False


def test_submit_entry_sends_variant_audit_metadata(monkeypatch):
    captured = {}

    def fake_http(method, url, token="", body=None, timeout=30):
        captured.update(method=method, url=url, token=token, body=body)
        return 201, {"success": True, "data": {"id": 12}}

    monkeypatch.setattr(challenge_submit, "http_json", fake_http)
    result = matchup.submit_entry(
        BASE_URL,
        "kr-token",
        "haiku",
        "claude-fable",
        "random-1",
        "Final prompt",
        {"temperature": 0.4},
        {"animal": "otter"},
        output_text="Otter poem",
    )
    assert result == {"id": 12}
    assert captured["body"] == {
        "contenderSlug": "claude-fable",
        "variantKey": "random-1",
        "promptUsed": "Final prompt",
        "settings": {"temperature": 0.4},
        "randomSelections": {"animal": "otter"},
        "outputText": "Otter poem",
    }


def test_run_text_entry_skips_only_missing_backend_key():
    result = matchup.run_entry(
        BASE_URL,
        "kr-token",
        {"slug": "haiku", "challengeType": "TEXT", "promptText": "Write"},
        {"slug": "claude-opus", "generator": "claude-api", "model": "opus"},
        {"contender": "claude-opus"},
        anthropic_key="",
        openai_key="",
        dry_run=False,
        poll_seconds=0,
        timeout_seconds=10,
    )
    assert result["status"] == "skipped"
    assert result["reason"] == "missing ANTHROPIC_API_KEY"


def test_run_text_entry_generates_and_submits(monkeypatch):
    monkeypatch.setattr(
        matchup,
        "generate_anthropic",
        lambda prompt, contender, settings, key: "Generated answer",
    )
    captured = {}

    def fake_submit(*args, **kwargs):
        captured.update(args=args, kwargs=kwargs)
        return {"id": 88}

    monkeypatch.setattr(matchup, "submit_entry", fake_submit)
    result = matchup.run_entry(
        BASE_URL,
        "kr-token",
        {"slug": "haiku", "challengeType": "TEXT", "promptText": "Write"},
        {
            "slug": "claude-fable",
            "generator": "claude-api",
            "model": "fable",
            "defaultSettings": {"temperature": 0.2},
        },
        {
            "contender": "claude-fable",
            "variantKey": "warm",
            "promptSuffix": "Make it warm",
            "settings": {"temperature": 0.8},
            "randomSelections": {"season": "summer"},
        },
        anthropic_key="key",
        openai_key="",
        dry_run=False,
        poll_seconds=0,
        timeout_seconds=10,
    )
    assert result == {
        "contender": "claude-fable",
        "variant": "warm",
        "generator": "claude-api",
        "status": "submitted",
        "submissionId": 88,
    }
    assert captured["args"][4] == "warm"
    assert captured["args"][5] == "Write\n\nMake it warm"
    assert captured["args"][6] == {"temperature": 0.8}
    assert captured["args"][7] == {"season": "summer"}
    assert captured["kwargs"]["output_text"] == "Generated answer"


def test_run_art_entry_submits_art_image(monkeypatch):
    monkeypatch.setattr(matchup, "enqueue_art", lambda *args, **kwargs: 123)
    monkeypatch.setattr(matchup, "submit_entry", lambda *args, **kwargs: {"id": 9})
    result = matchup.run_entry(
        BASE_URL,
        "kr-token",
        {"slug": "icon", "challengeType": "ART", "promptText": "Draw"},
        {"slug": "art-sd", "generator": "art-sd"},
        {"contender": "art-sd"},
        anthropic_key="",
        openai_key="",
        dry_run=False,
        poll_seconds=0,
        timeout_seconds=10,
    )
    assert result["status"] == "submitted"
    assert result["submissionId"] == 9
    assert result["artImageId"] == 123


def test_main_dry_run_resolves_matrix_without_credentials(monkeypatch, capsys):
    monkeypatch.setattr(
        challenge_submit,
        "fetch_challenge",
        lambda base_url, slug: {
            "slug": slug,
            "challengeType": "TEXT",
            "promptText": "Prompt",
        },
    )
    monkeypatch.setattr(
        matchup,
        "fetch_contenders",
        lambda base_url: {
            "claude-fable": {
                "slug": "claude-fable",
                "generator": "claude-api",
                "model": "fable",
            }
        },
    )
    exit_code = matchup.main(
        [
            "haiku",
            "--spec",
            '{"contenders":[{"contender":"claude-fable"},{"contender":"missing"}]}',
            "--dry-run",
            "--kr-base-url",
            BASE_URL,
        ]
    )
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "1 planned" in output
    assert "1 skipped" in output
    assert "contender not found" in output
