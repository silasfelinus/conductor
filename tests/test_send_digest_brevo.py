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
