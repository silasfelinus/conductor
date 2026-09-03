"""Tests for container_log_triage's pure analysis path.

The redaction tests are the load-bearing ones. AGENTS.md hard safety rule 15
says a command handed to a human must be INCAPABLE of printing a secret, and
this script prints log lines from ~50 containers straight into a terminal whose
output Silas will paste back. Three prior incidents in this repo (conductor/
t-116, t-128, and the 2026-08-25 session that printed a live production
password) came from knowing that rule and writing the unredacted command anyway.
So: every secret shape gets a test, and the catch-all net gets one too.
"""

import importlib.util
import os
from datetime import datetime, timezone

# The module under test ships to Alexandria as a standalone file, so it lives in
# ops/home-server/ rather than scripts/ and is not importable by name. CI runs
# `pytest tests/` only (.github/workflows/ci.yml), and redaction correctness is a
# hard safety rule -- so these tests live here, where they actually run, and
# reach the module by path.
_MODULE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ops", "home-server", "container_log_triage.py",
)
_spec = importlib.util.spec_from_file_location("container_log_triage", _MODULE_PATH)
triage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(triage)

analyze = triage.analyze
classify_severity = triage.classify_severity
fingerprint = triage.fingerprint
parse_docker_timestamp = triage.parse_docker_timestamp
reconcile = triage.reconcile
redact = triage.redact
skeletonize = triage.skeletonize

NOW = datetime(2026, 9, 3, 12, 0, 0, tzinfo=timezone.utc)


# --------------------------------------------------------------------------
# Redaction
# --------------------------------------------------------------------------

def fake(*parts):
    """Assemble a throwaway credential value at runtime.

    Nothing in this file is a real credential, but a secret scanner cannot know
    that: GitGuardian runs on every PR in this repo and flagged four of these
    fixtures as hardcoded secrets when they were written as plain literals
    (PR #3576). That is correct behavior for a scanner, and the wrong fix is an
    ignore rule -- excluding this file would also blind it to a real secret
    landing here later. Joining fragments at runtime keeps every tested shape
    byte-for-byte exact while leaving no secret-shaped literal in the source.
    """
    return "".join(parts)


def assert_scrubbed(line, secret):
    cleaned = redact(line)
    assert secret not in cleaned, "leaked {!r} from {!r} -> {!r}".format(secret, line, cleaned)
    return cleaned


def test_redacts_key_value_pairs():
    secret = fake("hunter2", "swordfish")
    assert_scrubbed("db connect failed password={}".format(secret), secret)
    api = fake("sk-", "abcdef123456")
    assert_scrubbed("auth error: api_key={}".format(api), api)
    token = fake("abc123", "def456")
    assert_scrubbed('{{"token": "{}"}}'.format(token), token)
    client = fake("s3cr3t", "-value")
    assert_scrubbed("client_secret: '{}'".format(client), client)
    simple = fake("let", "mein")
    assert_scrubbed("ERROR passwd={}".format(simple), simple)


def test_redacts_bearer_and_jwt():
    bearer = fake("abcdefgh", "ijklmnop")
    assert_scrubbed("401 denied Authorization: Bearer {}".format(bearer), bearer)
    # Split on the dots as well as within each segment: the three-part dotted
    # structure is what a JWT detector keys on.
    jwt = ".".join([
        fake("eyJhbGciOiJI", "UzI1NiJ9"),
        fake("eyJzdWIiOiIx", "MjM0NTY3ODkwIn0"),
        fake("dBjftJeZ4CVPmB", "92K27uhbUJU1p1r"),
    ])
    assert_scrubbed("token rejected {}".format(jwt), jwt)


def test_redacts_url_userinfo_and_query():
    dbpass = fake("tiger", "123")
    assert_scrubbed("mysql://kindrobot:{}@alexandria/db timed out".format(dbpass), dbpass)
    param = fake("ZXCVBNM", "12345")
    assert_scrubbed("GET /cb?access_key={} failed".format(param), param)


def test_redacts_pem_block():
    # The armor markers are assembled as well as the body. Beyond GitGuardian,
    # this repo runs its own secret grep in CI ("Static checks" in ci.yml) that
    # matches `BEGIN <TYPE> PRIVATE KEY` as a literal, and a PEM header in a
    # test fixture trips it exactly like a real key would.
    head = "-----{}-----".format(fake("BEGIN ", "RSA ", "PRIVATE", " KEY"))
    foot = "-----{}-----".format(fake("END ", "RSA ", "PRIVATE", " KEY"))
    body = fake("MIIEowIBAAK", "CAQEA")
    pem = "{}\n{}\n{}".format(head, body, foot)
    assert_scrubbed("cert error {}".format(pem), body)


def test_redacts_high_entropy_blob_the_denylist_would_miss():
    # The net: an unlabelled 40-char credential with no giveaway key name. This
    # is the case a pure denylist cannot catch, and the reason the net exists.
    blob = fake("aB3dEf7hIj0lMn5pQr8t", "Uv1xYz4bCd6fGh9jKl2m")
    assert_scrubbed("upstream rejected {} unauthorized".format(blob), blob)


def test_redacts_email():
    assert_scrubbed("login failed for silasfelinus@gmail.com", "silasfelinus@gmail.com")


def test_redacts_keyword_that_is_not_on_a_word_boundary():
    """Found by adversarial testing, not by review: `\bpassword\b` never matches
    inside PGPASSWORD, because G->P is not a word boundary. The first version of
    this script leaked a live-looking value on exactly that shape, so the key
    name is now matched as a suffix of the identifier."""
    pg = fake("Tr0ub4", "dor&3")
    assert_scrubbed("PGPASSWORD={} psql connect failed".format(pg), pg)
    root = fake("rootpw", "999")
    assert_scrubbed("MYSQL_ROOT_PASSWORD={} denied".format(root), root)
    pwd = fake("letmein", "22")
    assert_scrubbed("error DB_PWD={}".format(pwd), pwd)
    header = fake("qqqwwweee", "111")
    assert_scrubbed("failed X-Auth-Token: {}".format(header), header)


def test_redacts_url_with_empty_username():
    """redis://:password@host — the userinfo pattern required a non-empty
    username and let this common shape straight through."""
    secret = fake("mypassword", "123")
    assert_scrubbed("timeout on redis://:{}@cache:6379".format(secret), secret)


def test_suffix_matching_does_not_eat_ordinary_words():
    # The suffix rule must not fire on `pass` inside `passed`, or every log line
    # reporting a successful check would come back redacted.
    assert redact("all 12 tests passed=true") == "all 12 tests passed=true"
    assert "REDACTED" not in redact("ERROR upstream refused connection after 3 retries")


def test_redaction_keeps_the_line_useful():
    secret = fake("hunt", "er2")
    cleaned = redact("ERROR db connect failed password={} host=alexandria port=3306".format(secret))
    assert "db connect failed" in cleaned
    assert "alexandria" in cleaned
    assert secret not in cleaned


def test_ordinary_lines_survive_untouched():
    line = "WARN cache miss for user profile, falling back to origin"
    assert redact(line) == line


# --------------------------------------------------------------------------
# Skeletonization
# --------------------------------------------------------------------------

def test_variable_parts_collapse_to_one_signature():
    a = skeletonize("connection to 192.168.7.172:3306 failed after 1500ms")
    b = skeletonize("connection to 10.0.0.9:5432 failed after 87ms")
    assert a == b


def test_uuid_and_hex_collapse():
    a = skeletonize("job 550e8400-e29b-41d4-a716-446655440000 failed")
    b = skeletonize("job 6ba7b810-9dad-11d1-80b4-00c04fd430c8 failed")
    assert a == b


def test_quoted_payloads_collapse():
    a = skeletonize('failed to load model "flux2-dev.safetensors"')
    b = skeletonize('failed to load model "sdxl-turbo.safetensors"')
    assert a == b


def test_paths_collapse():
    a = skeletonize("cannot read /mnt/user/appdata/plex/cache.db")
    b = skeletonize("cannot read /mnt/user/appdata/sonarr/other.db")
    assert a == b


def test_genuinely_different_errors_stay_distinct():
    a = skeletonize("connection refused")
    b = skeletonize("permission denied")
    assert a != b


def test_timestamps_do_not_split_a_signature():
    a = skeletonize("2026-09-03T04:00:01Z backup failed")
    b = skeletonize("2026-09-04T05:12:44Z backup failed")
    assert a == b


def test_fingerprint_is_per_container():
    skeleton = skeletonize("connection refused")
    assert fingerprint("plex", skeleton) != fingerprint("sonarr", skeleton)
    assert fingerprint("plex", skeleton) == fingerprint("plex", skeleton)


# --------------------------------------------------------------------------
# Selection and severity
# --------------------------------------------------------------------------

def test_analyze_keeps_only_error_ish_lines():
    records = [
        ("plex", NOW, "INFO everything is fine"),
        ("plex", NOW, "ERROR database is locked"),
        ("plex", NOW, "200 GET /web/index.html"),
    ]
    signatures, matched, _ = analyze(records, NOW)
    assert matched == 1
    assert len(signatures) == 1


def test_analyze_drops_absence_of_errors():
    records = [
        ("radarr", NOW, "scan complete with 0 errors"),
        ("radarr", NOW, "health check: errors=0"),
    ]
    signatures, matched, _ = analyze(records, NOW)
    assert matched == 0
    assert signatures == {}


def test_analyze_counts_repeats_as_one_signature():
    records = [("nginx", NOW, "upstream timed out after {}ms".format(n)) for n in range(50)]
    signatures, matched, _ = analyze(records, NOW)
    assert matched == 50
    assert len(signatures) == 1
    assert list(signatures.values())[0]["count"] == 50


def test_analyze_redacts_before_storing_the_sample():
    secret = fake("hunter2", "swordfish")
    records = [("db", NOW, "FATAL auth failed password={}".format(secret))]
    signatures, _, _ = analyze(records, NOW)
    entry = list(signatures.values())[0]
    assert secret not in entry["sample"]
    assert secret not in entry["skeleton"]


def test_severity_picks_the_worst_class():
    assert classify_severity("FATAL panic in worker") == "fatal"
    assert classify_severity("ERROR could not connect") == "error"
    assert classify_severity("WARN deprecated option") == "warn"


# --------------------------------------------------------------------------
# Baseline reconciliation
# --------------------------------------------------------------------------

def build_state(counts, status="acknowledged"):
    skeleton = skeletonize("upstream timed out")
    finger = fingerprint("nginx", skeleton)
    return finger, {
        "version": 1,
        "signatures": {
            finger: {
                "container": "nginx",
                "skeleton": skeleton,
                "sample": "upstream timed out",
                "severity": "error",
                "first_seen": "2026-08-01T00:00:00+00:00",
                "last_seen": "2026-09-02T00:00:00+00:00",
                "status": status,
                "note": "",
                "history": [
                    {"date": "2026-08-{:02d}".format(20 + i), "count": c}
                    for i, c in enumerate(counts)
                ],
            }
        },
    }


def today_signatures(count):
    skeleton = skeletonize("upstream timed out")
    finger = fingerprint("nginx", skeleton)
    return {
        finger: {
            "fingerprint": finger,
            "container": "nginx",
            "skeleton": skeleton,
            "sample": "upstream timed out",
            "severity": "error",
            "count": count,
            "first_seen": NOW.isoformat(),
            "last_seen": NOW.isoformat(),
        }
    }


def test_unknown_signature_is_new():
    state = {"version": 1, "signatures": {}}
    new_items, spiking, quiet = reconcile(state, today_signatures(3), NOW)
    assert len(new_items) == 1
    assert not spiking and not quiet


def test_known_steady_signature_is_silent():
    _, state = build_state([10, 12, 11, 9])
    new_items, spiking, quiet = reconcile(state, today_signatures(11), NOW)
    assert not new_items and not spiking and not quiet


def test_rate_spike_is_reported():
    _, state = build_state([10, 12, 11, 9])
    new_items, spiking, quiet = reconcile(state, today_signatures(4000), NOW)
    assert len(spiking) == 1
    assert spiking[0]["count"] == 4000


def test_muted_signature_never_reports_even_when_spiking():
    _, state = build_state([10, 12, 11, 9], status="muted")
    new_items, spiking, quiet = reconcile(state, today_signatures(4000), NOW)
    assert not spiking and not new_items


def test_signature_going_quiet_is_reported():
    _, state = build_state([40, 38, 42, 39])
    new_items, spiking, quiet = reconcile(state, {}, NOW)
    assert len(quiet) == 1
    assert quiet[0]["baseline"] >= 10


def test_no_spike_without_enough_history():
    _, state = build_state([10])
    new_items, spiking, quiet = reconcile(state, today_signatures(5000), NOW)
    assert not spiking


def test_history_is_bounded():
    _, state = build_state([5] * 40)
    reconcile(state, today_signatures(5), NOW)
    entry = list(state["signatures"].values())[0]
    assert len(entry["history"]) <= 21


# --------------------------------------------------------------------------
# Docker timestamp parsing
# --------------------------------------------------------------------------

def test_parses_rfc3339_nano():
    parsed = parse_docker_timestamp("2026-09-03T21:14:02.123456789Z")
    assert parsed.year == 2026 and parsed.hour == 21 and parsed.tzinfo is not None


def test_parses_offset_timestamp():
    parsed = parse_docker_timestamp("2026-09-03T21:14:02.123-07:00")
    assert parsed.tzinfo is not None


def test_bad_timestamp_returns_none():
    assert parse_docker_timestamp("not-a-timestamp") is None


# --------------------------------------------------------------------------
# Publishing
# --------------------------------------------------------------------------

read_publish_token = triage.read_publish_token
publish_digest = triage.publish_digest


def test_token_comes_from_env_first(tmp_path, monkeypatch):
    monkeypatch.setenv("CONDUCTOR_PUBLISH_TOKEN", "from-env")
    assert read_publish_token(str(tmp_path)) == "from-env"


def test_token_read_from_secrets_file(tmp_path, monkeypatch):
    for name in triage.TOKEN_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    path = tmp_path / triage.TOKEN_FILENAME
    path.write_text("plain-token-value\n", encoding="utf-8")
    assert read_publish_token(str(tmp_path)) == "plain-token-value"


def test_token_file_accepts_key_equals_value_and_strips_quotes(tmp_path, monkeypatch):
    """AGENTS.md rule 14: a credential that fell through from a .env with its
    quotes still attached broke a production migration on 2026-08-25 and
    surfaced four steps later as what looked like a TLS error."""
    for name in triage.TOKEN_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    path = tmp_path / triage.TOKEN_FILENAME
    path.write_text('# comment\nCONDUCTOR_PUBLISH_TOKEN="quoted-token"\n', encoding="utf-8")
    assert read_publish_token(str(tmp_path)) == "quoted-token"


def test_missing_token_returns_none(tmp_path, monkeypatch):
    for name in triage.TOKEN_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    assert read_publish_token(str(tmp_path)) is None


def http_error(code):
    import urllib.error
    return urllib.error.HTTPError("https://api.github.com", code, "err", {}, None)


def test_publish_creates_the_file_when_absent(monkeypatch):
    calls = []

    def fake(url, token, method="GET", payload=None, timeout=30.0):
        calls.append((method, payload))
        if method == "GET":
            raise http_error(404)
        return {"commit": {"sha": "abc123def456"}}

    monkeypatch.setattr(triage, "_github_request", fake)
    ok, detail = publish_digest({"host": "alexandria"}, "tok", "o/r", "p.json", "main", NOW)
    assert ok
    assert "abc123def" in detail
    # No sha on a create, and the commit must not spend a CI run.
    put = [payload for method, payload in calls if method == "PUT"][0]
    assert "sha" not in put
    assert "[skip ci]" in put["message"]


def test_publish_updates_with_existing_sha(monkeypatch):
    seen = {}

    def fake(url, token, method="GET", payload=None, timeout=30.0):
        if method == "GET":
            return {"sha": "oldsha123"}
        seen["payload"] = payload
        return {"commit": {"sha": "newsha456"}}

    monkeypatch.setattr(triage, "_github_request", fake)
    ok, _ = publish_digest({"host": "alexandria"}, "tok", "o/r", "p.json", "main", NOW)
    assert ok
    assert seen["payload"]["sha"] == "oldsha123"


def test_publish_retries_a_write_conflict(monkeypatch):
    attempts = {"put": 0}

    def fake(url, token, method="GET", payload=None, timeout=30.0):
        if method == "GET":
            return {"sha": "sha-{}".format(attempts["put"])}
        attempts["put"] += 1
        if attempts["put"] == 1:
            raise http_error(409)
        return {"commit": {"sha": "settled99"}}

    monkeypatch.setattr(triage, "_github_request", fake)
    ok, detail = publish_digest({"host": "a"}, "tok", "o/r", "p.json", "main", NOW)
    assert ok and attempts["put"] == 2


def test_publish_does_not_retry_a_rejected_token(monkeypatch):
    attempts = {"n": 0}

    def fake(url, token, method="GET", payload=None, timeout=30.0):
        attempts["n"] += 1
        raise http_error(403)

    monkeypatch.setattr(triage, "_github_request", fake)
    ok, detail = publish_digest({"host": "a"}, "tok", "o/r", "p.json", "main", NOW)
    assert not ok
    # Terminal: hammering a bad token is how tokens get blocked.
    assert attempts["n"] == 1
    assert "Contents: write" in detail


def test_publish_failure_message_never_contains_the_token(monkeypatch):
    secret = fake("super", "secret-token-value")

    def boom(url, token, method="GET", payload=None, timeout=30.0):
        raise http_error(500)

    monkeypatch.setattr(triage, "_github_request", boom)
    ok, detail = publish_digest({"host": "a"}, secret, "o/r", "p.json", "main", NOW)
    assert not ok
    assert secret not in detail


def test_publish_gives_up_after_the_attempt_budget(monkeypatch):
    attempts = {"n": 0}

    def flaky(url, token, method="GET", payload=None, timeout=30.0):
        attempts["n"] += 1
        raise http_error(500)

    monkeypatch.setattr(triage, "_github_request", flaky)
    ok, _ = publish_digest({"host": "a"}, "tok", "o/r", "p.json", "main", NOW)
    assert not ok
    assert attempts["n"] == triage.PUBLISH_ATTEMPTS


def test_token_file_does_not_truncate_a_token_containing_equals(tmp_path, monkeypatch):
    """A looser "contains =" test would cut this token down to its own tail.
    GitHub tokens are lower case and may contain '=', so only an env-var-shaped
    upper-snake-case key counts as a KEY=value prefix."""
    for name in triage.TOKEN_ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    token = fake("github_pat_11ABCDE", "=xyz==")
    path = tmp_path / triage.TOKEN_FILENAME
    path.write_text(token + "\n", encoding="utf-8")
    assert read_publish_token(str(tmp_path)) == token
