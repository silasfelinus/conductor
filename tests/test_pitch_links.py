import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pitch_links  # noqa: E402

# The same vector is asserted by kind_robots utils/scripts/verifyPitchDecision.test.ts:
# Python signs, TypeScript verifies, so both must agree byte for byte.
VECTOR = "c0900b8ddf3e254c6d3602d3da55ccc183f961781211f94f128bec51f6f66b4d"


def test_signature_matches_the_kind_robots_verifier_vector():
    assert pitch_links.sign("test-secret", "2026-10-01-kind-jigsaw", "approved", 1_900_000_000) == VECTOR


def test_decision_url_carries_slug_vote_expiry_and_signature():
    url = pitch_links.decision_url("test-secret", "2026-10-01-kind-jigsaw", "approved", 1_900_000_000)
    parsed = urlparse(url)
    query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
    assert parsed.path == "/api/conductor/pitch-decision"
    assert query == {"slug": "2026-10-01-kind-jigsaw", "vote": "approved", "exp": "1900000000", "sig": VECTOR}


# kind_robots utils/scripts/verifyPitchDecision.test.ts asserts this inbox vector too.
INBOX_VECTOR = "e7c1d9e2e9608ca15d7a223b49cb2ce082ae079a60ed6bf2c6f86752fff6afaa"


def test_inbox_signature_matches_the_kind_robots_verifier_vector():
    assert pitch_links.sign_inbox("test-secret", 1_900_000_000) == INBOX_VECTOR


def test_inbox_url_signs_only_the_expiry_and_carries_preselections():
    url = pitch_links.inbox_url("test-secret", 1_900_000_000, picks={"2026-10-01-x": "approve-changes"})
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    assert parsed.path == "/api/conductor/pitch-inbox"
    assert query["exp"] == ["1900000000"] and query["sig"] == [INBOX_VECTOR]
    assert query["pick"] == ["2026-10-01-x:approve-changes"]
    # the preselection is a UI default: the same signature serves any pick
    assert parse_qs(urlparse(pitch_links.inbox_url("test-secret", 1_900_000_000)).query)["sig"] == [INBOX_VECTOR]


def test_links_for_needs_a_secret_and_expires_in_fourteen_days(monkeypatch):
    monkeypatch.delenv("PITCH_LINK_SECRET", raising=False)
    assert pitch_links.links_for("2026-10-01-x") is None
    assert pitch_links.inbox_link() is None
    monkeypatch.setenv("PITCH_LINK_SECRET", "test-secret")
    links = pitch_links.links_for("2026-10-01-x", now=1_000_000)
    assert set(links) == {"approve", "changes", "pass"}
    picks = {k: parse_qs(urlparse(v).query) for k, v in links.items()}
    assert picks["approve"]["pick"] == ["2026-10-01-x:approve"]
    assert picks["changes"]["pick"] == ["2026-10-01-x:approve-changes"]
    assert picks["pass"]["pick"] == ["2026-10-01-x:pass"]
    assert picks["approve"]["exp"] == [str(1_000_000 + 14 * 24 * 3600)]
    assert len({q["sig"][0] for q in picks.values()}) == 1  # one signature: the inbox's
