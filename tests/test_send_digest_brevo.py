import base64
import io
import json
import urllib.error

import scripts.send_digest_brevo as digest_sender


class FakeResponse:
    def __init__(self, body=b'{"messageId":"digest-123"}'):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.body


def http_error(code, body, headers=None):
    return urllib.error.HTTPError(
        digest_sender.BREVO_URL,
        code,
        "test failure",
        headers or {},
        io.BytesIO(body.encode("utf-8")),
    )


def base_payload():
    return {
        "subject": "Conductor digest 2026-08-06",
        "htmlContent": "<p>Daily digest</p>",
        "sender": {"email": "from@example.com", "name": "Conductor"},
        "to": [{"email": "silas@example.com", "name": "Silas"}],
    }


def test_configure_payload_adds_provider_independent_direct_links_backup(monkeypatch):
    monkeypatch.setenv("DIGEST_FROM", "conductor@example.com")
    monkeypatch.setenv("DIGEST_FROM_NAME", "Conductor")
    monkeypatch.setenv("DIGEST_TO", "silas@example.com")
    monkeypatch.setenv("DIGEST_TO_NAME", "Silas")

    direct = (
        "https://kindrobots.org/api/conductor/pitch-inbox?"
        "exp=1792348892&sig=deadbeef"
    )
    payload = {
        "subject": "Daily Dream",
        "htmlContent": (
            f'<a href="{direct.replace("&", "&amp;")}">Decide all 5</a>'
            '<a href="https://kindrobots.org/build/animation-manager?effect=test&preview=1">'
            "Try animation</a>"
        ),
    }

    configured = digest_sender.configure_payload(payload)

    assert configured["to"] == [
        {
            "email": "silas@example.com",
            "name": "Silas",
            "contactPixelTrackingConsent": False,
        }
    ]
    assert "X-Mailin-Track-Click" not in configured.get("headers", {})
    assert "X-Mailin-Track-Open" not in configured.get("headers", {})
    assert digest_sender.DIRECT_LINKS_NOTICE_MARKER in configured["htmlContent"]

    attachment = next(
        item
        for item in configured["attachment"]
        if item["name"] == digest_sender.DIRECT_LINKS_ATTACHMENT
    )
    backup_html = base64.b64decode(attachment["content"]).decode("utf-8")
    assert direct.replace("&", "&amp;") in backup_html
    assert "https://kindrobots.org/build/animation-manager?effect=test&amp;preview=1" in backup_html
    assert "sendibt2.com" not in backup_html


def test_direct_links_backup_is_idempotent(monkeypatch):
    monkeypatch.setenv("DIGEST_FROM", "conductor@example.com")
    monkeypatch.setenv("DIGEST_TO", "silas@example.com")

    payload = {
        "subject": "Daily Dream",
        "htmlContent": '<a href="https://kindrobots.org">Kind Robots</a>',
    }

    digest_sender.configure_payload(payload)
    digest_sender.configure_payload(payload)

    backups = [
        item
        for item in payload["attachment"]
        if item["name"] == digest_sender.DIRECT_LINKS_ATTACHMENT
    ]
    assert len(backups) == 1
    assert payload["htmlContent"].count(digest_sender.DIRECT_LINKS_NOTICE_MARKER) == 1


def test_transient_http_failure_retries_with_same_idempotency_key():
    requests = []
    sleeps = []

    def urlopen(request, timeout):
        requests.append(json.loads(request.data.decode("utf-8")))
        if len(requests) == 1:
            raise http_error(503, '{"code":"unavailable","message":"try again"}')
        return FakeResponse()

    rc = digest_sender.send_payload(
        base_payload(),
        "secret",
        max_attempts=2,
        retry_delays=(0,),
        urlopen=urlopen,
        sleep=sleeps.append,
    )

    assert rc == 0
    assert len(requests) == 2
    first_key = requests[0]["headers"]["Idempotency-Key"]
    assert first_key.startswith("conductor-digest-")
    assert requests[1]["headers"]["Idempotency-Key"] == first_key
    assert sleeps == [0]


def test_non_retryable_http_failure_stops_immediately():
    attempts = 0

    def urlopen(request, timeout):
        nonlocal attempts
        attempts += 1
        raise http_error(400, '{"code":"invalid_parameter","message":"bad recipient"}')

    rc = digest_sender.send_payload(
        base_payload(),
        "secret",
        max_attempts=3,
        retry_delays=(0, 0),
        urlopen=urlopen,
        sleep=lambda _: None,
    )

    assert rc == 1
    assert attempts == 1


def test_duplicate_idempotency_response_counts_as_success_after_network_retry():
    attempts = 0

    def urlopen(request, timeout):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise urllib.error.URLError("connection reset after submit")
        raise http_error(
            400,
            '{"code":"duplicate_parameter","message":"idempotencyKey already used"}',
        )

    rc = digest_sender.send_payload(
        base_payload(),
        "secret",
        max_attempts=2,
        retry_delays=(0,),
        urlopen=urlopen,
        sleep=lambda _: None,
    )

    assert rc == 0
    assert attempts == 2


def test_idempotency_key_is_stable_for_identical_payloads():
    first = base_payload()
    second = base_payload()

    assert digest_sender.ensure_idempotency_key(first) == digest_sender.ensure_idempotency_key(second)


class FakeSMTP:
    instances = []

    def __init__(self, host, port, timeout=None):
        self.host, self.port = host, port
        self.sent = []
        FakeSMTP.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def login(self, user, password):
        self.login_args = (user, password)

    def send_message(self, message):
        self.sent.append(message)


def smtp_env(monkeypatch):
    monkeypatch.setenv("DIGEST_SMTP_USER", "sender@example.com")
    monkeypatch.setenv("DIGEST_SMTP_PASSWORD", "app-password")
    monkeypatch.setenv("DIGEST_TO", "silas@example.com")
    monkeypatch.setenv("DIGEST_FROM", "conductor@example.com")


def test_smtp_send_keeps_hrefs_byte_for_byte(monkeypatch):
    import scripts.send_digest_smtp as smtp_sender

    smtp_env(monkeypatch)
    FakeSMTP.instances = []
    direct = "https://kindrobots.org/api/conductor/pitch-inbox?exp=1792348892&amp;sig=deadbeef"
    payload = {"subject": "Daily Dream", "htmlContent": f'<a href="{direct}">Decide all 5</a>'}

    assert smtp_sender.send_payload(payload, smtp_factory=FakeSMTP) == 0

    message = FakeSMTP.instances[0].sent[0]
    assert message["To"] == "Silas <silas@example.com>"
    assert message["From"] == "Conductor <sender@example.com>"
    body = message.get_body(("html",)).get_content()
    assert direct in body
    assert "sendibt" not in body
    assert "Direct-link backup" not in body
    assert not list(message.iter_attachments())


def test_smtp_drops_brevo_only_backup_but_keeps_real_attachments(monkeypatch):
    import scripts.send_digest_smtp as smtp_sender

    smtp_env(monkeypatch)
    payload = {
        "subject": "Daily Dream",
        "htmlContent": "<p>hi</p>",
        "attachment": [
            {"name": "conductor-direct-links.html", "content": base64.b64encode(b"x").decode()},
            {"name": "notes.txt", "content": base64.b64encode(b"keep me").decode()},
        ],
    }
    names = [part.get_filename() for part in smtp_sender.build_message(payload).iter_attachments()]
    assert names == ["notes.txt"]


def test_main_prefers_smtp_and_skips_brevo(monkeypatch, tmp_path):
    smtp_env(monkeypatch)
    monkeypatch.setenv("BREVO_API_KEY", "brevo-key")
    payload_path = tmp_path / "digest-email.json"
    payload_path.write_text(json.dumps(base_payload()), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["send_digest_brevo.py", str(payload_path)])
    monkeypatch.setattr(digest_sender.send_digest_smtp, "send_payload", lambda payload: 0)

    def brevo_must_not_send(*args, **kwargs):
        raise AssertionError("Brevo was called although SMTP succeeded")

    monkeypatch.setattr(digest_sender, "send_payload", brevo_must_not_send)
    assert digest_sender.main() == 0


def test_main_falls_back_to_brevo_when_smtp_fails(monkeypatch, tmp_path):
    smtp_env(monkeypatch)
    monkeypatch.setenv("BREVO_API_KEY", "brevo-key")
    payload_path = tmp_path / "digest-email.json"
    payload_path.write_text(json.dumps(base_payload()), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["send_digest_brevo.py", str(payload_path)])
    monkeypatch.setattr(digest_sender.send_digest_smtp, "send_payload", lambda payload: 1)
    calls = []
    monkeypatch.setattr(digest_sender, "send_payload", lambda payload, key: calls.append(key) or 0)

    assert digest_sender.main() == 0
    assert calls == ["brevo-key"]


def test_main_uses_brevo_when_smtp_unconfigured(monkeypatch, tmp_path):
    monkeypatch.delenv("DIGEST_SMTP_USER", raising=False)
    monkeypatch.delenv("DIGEST_SMTP_PASSWORD", raising=False)
    monkeypatch.setenv("BREVO_API_KEY", "brevo-key")
    monkeypatch.setenv("DIGEST_TO", "silas@example.com")
    monkeypatch.setenv("DIGEST_FROM", "conductor@example.com")
    payload_path = tmp_path / "digest-email.json"
    payload_path.write_text(json.dumps(base_payload()), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["send_digest_brevo.py", str(payload_path)])
    calls = []
    monkeypatch.setattr(digest_sender, "send_payload", lambda payload, key: calls.append(key) or 0)

    assert digest_sender.main() == 0
    assert calls == ["brevo-key"]


def test_direct_links_notice_goes_inside_body_of_full_document():
    payload = {
        "htmlContent": (
            '<!doctype html><html><head></head><body style="margin:0">'
            '<a href="https://kindrobots.org/x">x</a></body></html>'
        )
    }
    digest_sender.attach_direct_links_backup(payload)
    html_content = payload["htmlContent"]
    assert html_content.startswith("<!doctype html>")
    assert html_content.index('<body style="margin:0">') < html_content.index(
        digest_sender.DIRECT_LINKS_NOTICE_MARKER
    )
