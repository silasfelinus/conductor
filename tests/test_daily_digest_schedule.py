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


def test_daily_digest_has_one_morning_cycle_and_hourly_is_report_only():
    hourly_text = HOURLY.read_text(encoding="utf-8")
    digest = cron_schedules(DIGEST)

    assert "0 * * * *" in cron_schedules(HOURLY)
    assert "build_conductor_summary_report_only.py" in hourly_text
    assert "build_dream_records.py" not in hourly_text
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


def test_daily_dream_sidecars_warn_without_manufacturing_a_failed_digest_run():
    workflow = DIGEST.read_text(encoding="utf-8")

    assert "::warning::Daily Dream object build failed" in workflow
    assert "::warning::Daily Dream live composed-field verification found drift" in workflow
    assert "Fail after digest if Daily Dream cycle failed" not in workflow
    assert 'exit "$failed"' not in workflow

    email_block = workflow.split("- name: Email via Brevo", 1)[1]
    email_block = email_block.split("\n  creative-revision:", 1)[0]
    assert "continue-on-error" not in email_block


def test_delayed_schedule_cannot_resend_after_watchdog_replacement_succeeds():
    workflow = DIGEST.read_text(encoding="utf-8")

    assert "delivery-guard:" in workflow
    assert "Suppress a delayed duplicate delivery" in workflow
    assert "GITHUB_RUN_ID" in workflow
    assert '.actor.login == "github-actions[bot]"' in workflow
    assert '.conclusion == "success"' in workflow
    assert "needs: delivery-guard" in workflow
    assert "needs.delivery-guard.outputs.should_run == 'true'" in workflow
    assert "Human workflow_dispatch is explicit" in workflow


def test_digest_gives_priority_art_a_bounded_same_cycle_window():
    workflow = DIGEST.read_text(encoding="utf-8")

    assert "submit_daily_dream_art.py --wait-timeout 300" in workflow
    assert "continue-on-error: true" in workflow
