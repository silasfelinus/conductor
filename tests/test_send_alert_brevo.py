import pytest

import scripts.send_alert_brevo as alert


def _clear_env(monkeypatch):
    for name in (
        "BREVO_API_KEY",
        "ALERT_TO",
        "DIGEST_TO",
        "ALERT_FROM",
        "DIGEST_FROM",
        "ALERT_TO_NAME",
        "DIGEST_TO_NAME",
        "ALERT_FROM_NAME",
        "DIGEST_FROM_NAME",
    ):
        monkeypatch.delenv(name, raising=False)


def test_build_payload_uses_digest_env(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("BREVO_API_KEY", "key123")
    monkeypatch.setenv("DIGEST_TO", "silas@example.com")
    monkeypatch.setenv("DIGEST_FROM", "ops@example.com")

    api_key, payload = alert.build_payload("Subj", "Body text")

    assert api_key == "key123"
    assert payload["subject"] == "Subj"
    assert payload["textContent"] == "Body text"
    assert payload["sender"]["email"] == "ops@example.com"
    assert payload["to"] == [{"email": "silas@example.com", "name": "Silas"}]


def test_alert_env_overrides_digest(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("BREVO_API_KEY", "k")
    monkeypatch.setenv("DIGEST_TO", "digest@example.com")
    monkeypatch.setenv("ALERT_TO", "alert@example.com")
    monkeypatch.setenv("DIGEST_FROM", "digest-from@example.com")
    monkeypatch.setenv("ALERT_FROM", "alert-from@example.com")

    _, payload = alert.build_payload("s", "b")

    assert payload["to"][0]["email"] == "alert@example.com"
    assert payload["sender"]["email"] == "alert-from@example.com"


def test_missing_config_raises(monkeypatch):
    _clear_env(monkeypatch)
    monkeypatch.setenv("BREVO_API_KEY", "k")  # no TO/FROM
    with pytest.raises(SystemExit) as exc:
        alert.build_payload("s", "b")
    assert "ALERT_TO/DIGEST_TO" in str(exc.value)


def test_dry_run_does_not_send(monkeypatch, capsys):
    _clear_env(monkeypatch)
    monkeypatch.setenv("BREVO_API_KEY", "k")
    monkeypatch.setenv("DIGEST_TO", "t@example.com")
    monkeypatch.setenv("DIGEST_FROM", "f@example.com")

    rc = alert.send_alert("Render box down", "unreachable", dry_run=True)

    assert rc == 0
    out = capsys.readouterr().out
    assert "Render box down" in out
    assert "unreachable" in out
