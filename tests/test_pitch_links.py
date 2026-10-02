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


def test_links_for_needs_a_secret_and_expires_in_fourteen_days(monkeypatch):
    monkeypatch.delenv("PITCH_LINK_SECRET", raising=False)
    assert pitch_links.links_for("2026-10-01-x") is None
    monkeypatch.setenv("PITCH_LINK_SECRET", "test-secret")
    links = pitch_links.links_for("2026-10-01-x", now=1_000_000)
    assert set(links) == {"approve", "pass"}
    approve = parse_qs(urlparse(links["approve"]).query)
    reject = parse_qs(urlparse(links["pass"]).query)
    assert approve["vote"] == ["approved"] and reject["vote"] == ["rejected"]
    assert approve["exp"] == [str(1_000_000 + 14 * 24 * 3600)]
    assert approve["sig"] != reject["sig"]
