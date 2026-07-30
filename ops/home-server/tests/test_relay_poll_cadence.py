from pathlib import Path


def test_kr_relay_pm2_poll_cadence_is_two_seconds():
    config = Path(__file__).parents[1] / 'ecosystem.config.js'
    source = config.read_text(encoding='utf-8')
    assert "POLL_SECONDS: process.env.POLL_SECONDS || '2'" in source
