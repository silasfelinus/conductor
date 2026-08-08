import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HOURLY = ROOT / ".github" / "workflows" / "hourly-conductor.yml"
DIGEST = ROOT / ".github" / "workflows" / "daily-digest.yml"
RETRY = ROOT / ".github" / "workflows" / "daily-digest-retry.yml"
CRON_RE = re.compile(r"cron:\s*[\"']([^\"']+)[\"']")


def cron_schedules(path: Path) -> list[str]:
    return CRON_RE.findall(path.read_text(encoding="utf-8"))


def daily_minutes(cron: str) -> int:
    minute, hour, day, month, weekday = cron.split()
    assert (day, month, weekday) == ("*", "*", "*")
    return int(hour) * 60 + int(minute)


def test_daily_digest_runs_after_same_hour_builder():
    hourly = cron_schedules(HOURLY)
    digest = cron_schedules(DIGEST)

    assert "0 * * * *" in hourly
    assert len(digest) == 1

    minute, hour, *_ = digest[0].split()
    assert int(hour) == 15
    assert int(minute) >= 30


def test_digest_retry_watchdog_keeps_expected_offsets():
    digest = cron_schedules(DIGEST)
    retry = cron_schedules(RETRY)

    assert len(digest) == 1
    assert len(retry) == 2

    primary = daily_minutes(digest[0])
    fallbacks = [daily_minutes(schedule) for schedule in retry]
    assert fallbacks == [primary + 60, primary + 180]
