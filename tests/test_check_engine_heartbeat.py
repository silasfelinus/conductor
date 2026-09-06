"""The dead-man's switch: alarm when NOTHING is happening.

2026-09-02 — ComfyUI crash-looped under pm2 for ~24 hours and not one of the
four existing checks said a word. The decisive fact, from healthcheck.log:

    2026-08-31  288 ticks
    2026-09-01   30 ticks, last at 02:26:07
    2026-09-02   (nothing)

The on-box watchdog stopped running ~37 hours before Silas noticed, while the
box was still healthy. Everything downstream of it was edge-triggered or
work-conditional, so a drained queue read as "idle" and therefore fine.

These tests pin the two alarms that do not depend on queue depth, and the
sustained-outage case specifically: ~1,440 consecutive ok:false beats must read
as DOWN, never as "down for 0 minutes" because the newest failing beat is
seconds old.
"""
import importlib.util
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_engine_heartbeat", REPO / "scripts" / "check_engine_heartbeat.py"
)
heartbeat = importlib.util.module_from_spec(SPEC)
sys.modules["check_engine_heartbeat"] = heartbeat
SPEC.loader.exec_module(heartbeat)

NOW = datetime(2026, 9, 2, 15, 30, 0, tzinfo=timezone.utc)


def beat(minutes_ago, ok=True):
    when = NOW - timedelta(minutes=minutes_ago)
    return {
        "checkedAt": when.isoformat().replace("+00:00", "Z"),
        "ok": ok,
        "status": "ok" if ok else "down",
        "latencyMs": 12 if ok else None,
        "source": "relay",
    }


def server(samples, is_active=True, title="comfy-fast"):
    """A uptime-endpoint server report. `samples` is chronological, as the API sends it."""
    return {
        "serverId": 1,
        "title": title,
        "serverType": "COMFY",
        "isActive": is_active,
        "lastStatus": "ok" if (samples and samples[-1]["ok"]) else "down",
        "lastCheckedAt": samples[-1]["checkedAt"] if samples else None,
        "samples": samples,
    }


def healthy_series(minutes=360, step=1):
    return [beat(m, ok=True) for m in range(minutes, 0, -step)]


class TimestampTests(unittest.TestCase):
    def test_parses_the_z_suffix_prisma_sends(self):
        parsed = heartbeat.parse_timestamp("2026-09-02T15:20:37.123Z")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.tzinfo, timezone.utc)

    def test_parses_an_explicit_offset(self):
        parsed = heartbeat.parse_timestamp("2026-09-02T08:20:37-07:00")
        self.assertEqual(parsed.hour, 15)

    def test_naive_timestamps_are_treated_as_utc(self):
        self.assertEqual(
            heartbeat.parse_timestamp("2026-09-02T15:20:37").tzinfo, timezone.utc
        )

    def test_junk_is_none_not_an_exception(self):
        for junk in (None, "", "   ", "not a date", 42, {}):
            self.assertIsNone(heartbeat.parse_timestamp(junk))


class LatestBeatTests(unittest.TestCase):
    def test_newest_sample_is_the_last_one_not_the_first(self):
        """The endpoint reverses a desc query, so samples arrive chronological.

        Reading samples[0] would pin every verdict to the OLDEST beat in the
        window -- a six-hour-old success reported as current health, which is
        the same stale-completion bug check_render_box.py had to fix.
        """
        when, ok = heartbeat.latest_beat(server([beat(300, ok=True), beat(1, ok=False)]))
        self.assertFalse(ok)
        self.assertLess(heartbeat.minutes_since(when, NOW), 2)

    def test_falls_back_to_last_checked_at_without_samples(self):
        record = server([beat(3, ok=True)])
        record["samples"] = []
        when, ok = heartbeat.latest_beat(record)
        self.assertTrue(ok)
        self.assertIsNotNone(when)

    def test_no_history_at_all(self):
        self.assertEqual(heartbeat.latest_beat({"samples": []}), (None, None))


class AssessServerTests(unittest.TestCase):
    def assess(self, record, **kw):
        return heartbeat.assess_server(record, NOW, **kw)

    def test_healthy_engine_is_ok(self):
        state, reason = self.assess(server(healthy_series()))
        self.assertEqual(state, heartbeat.OK)
        self.assertIn("healthy", reason)

    def test_silent_relay_is_caught(self):
        """The case the on-box watchdog can never report: it dies with the box."""
        state, reason = self.assess(server([beat(m) for m in range(360, 40, -1)]))
        self.assertEqual(state, heartbeat.SILENT)
        self.assertIn("not reporting", reason)

    def test_no_heartbeat_on_record_is_silent(self):
        state, reason = self.assess(server([]))
        self.assertEqual(state, heartbeat.SILENT)
        self.assertIn("no heartbeat", reason)

    def test_the_2026_09_02_outage_shape_is_down(self):
        """~24h of consecutive ok:false, still arriving every 60s.

        The regression that matters most: the newest failing beat is seconds
        old, so dating the outage from it yields "down for 0 minutes" and a
        healthy verdict. There is no healthy beat anywhere in the window, so
        the outage must be dated from the OLDEST beat instead.
        """
        state, reason = self.assess(server([beat(m, ok=False) for m in range(360, 0, -1)]))
        self.assertEqual(state, heartbeat.DOWN)
        self.assertIn("no healthy beat", reason)

    def test_engine_down_after_a_healthy_period_is_down(self):
        samples = [beat(m, ok=True) for m in range(360, 90, -1)]
        samples += [beat(m, ok=False) for m in range(90, 0, -1)]
        state, reason = self.assess(server(samples))
        self.assertEqual(state, heartbeat.DOWN)
        self.assertIn("ok:false", reason)

    def test_a_brief_blip_is_not_an_alarm(self):
        """A restart reports ok:false for a few beats. Don't page for that."""
        samples = [beat(m, ok=True) for m in range(360, 4, -1)]
        samples += [beat(m, ok=False) for m in range(4, 0, -1)]
        state, _ = self.assess(server(samples), down_minutes=10)
        self.assertEqual(state, heartbeat.OK)

    def test_a_blip_that_outlasts_the_limit_becomes_down(self):
        samples = [beat(m, ok=True) for m in range(360, 25, -1)]
        samples += [beat(m, ok=False) for m in range(25, 0, -1)]
        state, _ = self.assess(server(samples), down_minutes=10)
        self.assertEqual(state, heartbeat.DOWN)

    def test_silence_wins_over_staleness_thresholds_being_generous(self):
        state, _ = self.assess(server([beat(20, ok=True)]), stale_minutes=15)
        self.assertEqual(state, heartbeat.SILENT)
        state, _ = self.assess(server([beat(20, ok=True)]), stale_minutes=30)
        self.assertEqual(state, heartbeat.OK)


class AssessTests(unittest.TestCase):
    def assess(self, data, **kw):
        return heartbeat.assess(data, NOW, **kw)

    def test_healthy_fleet(self):
        state, _ = self.assess({"servers": [server(healthy_series())]})
        self.assertEqual(state, heartbeat.OK)

    def test_no_servers_is_unresolved_not_healthy(self):
        """A missing server row is a config problem, not a green light."""
        state, _ = self.assess({"servers": []})
        self.assertEqual(state, heartbeat.UNRESOLVED)

    def test_inactive_servers_are_skipped(self):
        """Deactivating a server is deliberate; paging about it trains you to ignore alerts."""
        state, reason = self.assess(
            {"servers": [server([beat(m, ok=False) for m in range(360, 0, -1)], is_active=False)]}
        )
        self.assertEqual(state, heartbeat.UNRESOLVED)
        self.assertIn("inactive", reason)

    def test_worst_state_wins_across_servers(self):
        state, _ = self.assess(
            {
                "servers": [
                    server(healthy_series(), title="comfy-a"),
                    server([beat(m, ok=False) for m in range(360, 0, -1)], title="comfy-b"),
                ]
            }
        )
        self.assertEqual(state, heartbeat.DOWN)

    def test_silent_outranks_down(self):
        """A box we cannot hear from at all is the more urgent of the two."""
        state, _ = self.assess(
            {
                "servers": [
                    server([beat(m, ok=False) for m in range(360, 0, -1)], title="comfy-a"),
                    server([beat(120, ok=True)], title="comfy-b"),
                ]
            }
        )
        self.assertEqual(state, heartbeat.SILENT)


def live_beat(minutes_ago, ok=True):
    """A beat relative to the REAL clock.

    main() reads datetime.now() rather than a fixture, deliberately -- these
    tests would pass against a frozen clock while the deployed script silently
    scored every real run as SILENT. So the end-to-end tests use real time.
    """
    when = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
    return {
        "checkedAt": when.isoformat().replace("+00:00", "Z"),
        "ok": ok,
        "status": "ok" if ok else "down",
        "latencyMs": 12 if ok else None,
        "source": "relay",
    }


def live_server(samples):
    return {
        "serverId": 1,
        "title": "comfy-fast",
        "serverType": "COMFY",
        "isActive": True,
        "lastStatus": "ok" if (samples and samples[-1]["ok"]) else "down",
        "lastCheckedAt": samples[-1]["checkedAt"] if samples else None,
        "samples": samples,
    }


class ExitCodeTests(unittest.TestCase):
    """A broken credential must never look like a broken render box."""

    def run_main(self, argv, fetch):
        original = heartbeat.fetch_uptime
        heartbeat.fetch_uptime = fetch
        try:
            return heartbeat.main(argv)
        finally:
            heartbeat.fetch_uptime = original

    def test_healthy_exits_zero(self):
        healthy = [live_beat(m, ok=True) for m in range(360, 0, -1)]
        code = self.run_main([], lambda *a, **k: {"servers": [live_server(healthy)]})
        self.assertEqual(code, heartbeat.EXIT_HEALTHY)

    def test_outage_exits_one(self):
        outage = [live_beat(m, ok=False) for m in range(360, 0, -1)]
        code = self.run_main([], lambda *a, **k: {"servers": [live_server(outage)]})
        self.assertEqual(code, heartbeat.EXIT_PROBLEM)

    def test_missing_token_exits_two_not_one(self):
        def boom(*a, **k):
            raise RuntimeError("KR_API_TOKEN is required to read the engine heartbeat.")

        self.assertEqual(self.run_main([], boom), heartbeat.EXIT_UNRESOLVED)

    def test_unreachable_api_exits_two_not_one(self):
        def boom(*a, **k):
            raise RuntimeError("uptime unreachable: [Errno -2] Name or service not known")

        self.assertEqual(self.run_main([], boom), heartbeat.EXIT_UNRESOLVED)


if __name__ == "__main__":
    unittest.main()


class AlertStateTests(unittest.TestCase):
    """Fix #4: re-alert while it stays broken, don't email once and go quiet.

    auto-art-generate's render-box email fires only on the transition
    (`NOW=down && PREV!=down`), so a box down for a week emails on day one and
    then nothing. Silence has to mean one thing, not both.
    """

    def decide(self, previous, state, minutes_later=0, realert_hours=6.0):
        now = NOW + timedelta(minutes=minutes_later)
        return heartbeat.decide_alert(previous, state, now, realert_hours)

    def test_first_bad_run_alerts(self):
        alert, record = self.decide(None, heartbeat.DOWN)
        self.assertEqual(alert, heartbeat.ALERT_DOWN)
        self.assertEqual(record["state"], heartbeat.DOWN)

    def test_an_outage_already_underway_at_first_run_still_alerts(self):
        """Deploying mid-outage must page, not adopt the outage as normal."""
        alert, _ = self.decide({}, heartbeat.SILENT)
        self.assertEqual(alert, heartbeat.ALERT_DOWN)

    def test_first_healthy_run_is_quiet(self):
        alert, record = self.decide(None, heartbeat.OK)
        self.assertEqual(alert, heartbeat.ALERT_NONE)
        self.assertEqual(record["state"], heartbeat.OK)

    def test_still_down_inside_the_window_is_quiet(self):
        _, first = self.decide(None, heartbeat.DOWN)
        alert, _ = self.decide(first, heartbeat.DOWN, minutes_later=90)
        self.assertEqual(alert, heartbeat.ALERT_NONE)

    def test_still_down_past_the_window_reminds(self):
        _, first = self.decide(None, heartbeat.DOWN)
        alert, record = self.decide(first, heartbeat.DOWN, minutes_later=361)
        self.assertEqual(alert, heartbeat.ALERT_REMINDER)
        self.assertEqual(record["since"], first["since"], "outage start must not reset")

    def test_reminders_repeat_on_cadence_not_once(self):
        record = None
        alerts = []
        for tick in range(0, 24 * 60, 30):  # a full day at the 30-minute cron
            alert, record = self.decide(record, heartbeat.DOWN, minutes_later=tick)
            alerts.append(alert)
        reminders = alerts.count(heartbeat.ALERT_REMINDER)
        self.assertEqual(alerts[0], heartbeat.ALERT_DOWN)
        self.assertEqual(reminders, 3, f"expected 6-hourly reminders, got {alerts}")
        self.assertLess(reminders, 10, "must not spam every run")

    def test_recovery_alerts_once_then_settles(self):
        _, down = self.decide(None, heartbeat.DOWN)
        alert, recovered = self.decide(down, heartbeat.OK, minutes_later=60)
        self.assertEqual(alert, heartbeat.ALERT_RECOVERED)
        alert, _ = self.decide(recovered, heartbeat.OK, minutes_later=90)
        self.assertEqual(alert, heartbeat.ALERT_NONE)

    def test_unresolved_never_manufactures_a_recovery(self):
        """An expired token must not report the engine fixed."""
        _, down = self.decide(None, heartbeat.DOWN)
        alert, record = self.decide(down, heartbeat.UNRESOLVED, minutes_later=30)
        self.assertEqual(alert, heartbeat.ALERT_NONE)
        self.assertEqual(record, down, "state must survive an unreadable run untouched")

    def test_unresolved_does_not_reset_the_reminder_clock(self):
        """Otherwise a flapping token silences every reminder forever."""
        record = None
        alert, record = self.decide(record, heartbeat.DOWN)
        self.assertEqual(alert, heartbeat.ALERT_DOWN)
        for tick in range(30, 361, 30):
            _, record = self.decide(record, heartbeat.UNRESOLVED, minutes_later=tick)
        alert, _ = self.decide(record, heartbeat.DOWN, minutes_later=361)
        self.assertEqual(alert, heartbeat.ALERT_REMINDER)

    def test_corrupt_state_file_is_treated_as_absent(self):
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write("{not json at all")
            path = handle.name
        self.assertIsNone(heartbeat.load_state(path))
        Path(path).unlink()

    def test_state_round_trips_through_disk(self):
        import tempfile

        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "state.json")
            _, record = self.decide(None, heartbeat.DOWN)
            heartbeat.save_state(path, record)
            self.assertEqual(heartbeat.load_state(path), record)


class DozingTests(unittest.TestCase):
    """A box that suspends and resumes looks perfectly healthy beat-by-beat.

    2026-09-06 — the COMFY series carried one beat every ~7 minutes for 2h20m,
    either side of blackouts of 143 and 200 minutes. Every beat it did send was
    fresh and ok:true, so SILENT (nothing within 15 minutes) and DOWN (ok:false
    for 10 minutes) both stayed quiet while the machine spent most of the hour
    frozen. The relay's heartbeat thread sleeps 60s and blocks at most 85s, so
    the SPACING is evidence about the box that its content cannot carry.
    """

    def dozing_series(self, gap_minutes=7, span_minutes=60):
        return [beat(m, ok=True) for m in range(span_minutes, 0, -gap_minutes)]

    def test_beats_spaced_far_wider_than_the_relay_can_manage_are_dozing(self):
        state, reason = heartbeat.assess_server(server(self.dozing_series()), NOW)
        self.assertEqual(state, heartbeat.DOZING)
        self.assertIn("kr-relay", reason)

    def test_the_verdict_names_no_cause_it_has_not_established(self):
        """The first guess on 2026-09-06 was sleep, and powercfg refuted it.

        Standby and hibernate were both 0 on AC and the newest Kernel-Power
        42/107 pair predated the gaps by two months. A reason line that had
        asserted sleep would have sent every future reader down that same dead
        end. State the measurement; leave the cause to the two log greps.
        """
        _, reason = heartbeat.assess_server(server(self.dozing_series()), NOW)
        for unproven in ("suspend", "sleep", "powercfg", "CUDA"):
            self.assertNotIn(unproven, reason.lower())

    def test_a_healthy_one_minute_cadence_is_not_dozing(self):
        state, _ = heartbeat.assess_server(server(healthy_series()), NOW)
        self.assertEqual(state, heartbeat.OK)

    def test_one_isolated_gap_is_a_restart_not_a_dozing_box(self):
        samples = [beat(m, ok=True) for m in range(60, 40, -1)]
        samples += [beat(m, ok=True) for m in range(30, 0, -1)]
        state, _ = heartbeat.assess_server(server(samples), NOW)
        self.assertEqual(state, heartbeat.OK)

    def test_a_capped_series_never_scores_dozing(self):
        """The endpoint downsamples to 500 and invents gaps doing it.

        Confirmed by asking for samples=5000 and getting 500 back. Scoring a
        24-hour window would otherwise report SLEEP on a box that never slept.
        """
        samples = [
            beat(m, ok=True)
            for m in range(heartbeat.SAMPLE_CAP * 7, 0, -7)
        ][-heartbeat.SAMPLE_CAP :]
        self.assertGreaterEqual(len(samples), heartbeat.SAMPLE_CAP)
        dozing, detail = heartbeat.detect_dozing(server(samples), NOW)
        self.assertFalse(dozing)
        self.assertIsNone(detail)

    def test_zero_min_gaps_disables_the_check_rather_than_dividing_by_nothing(self):
        dozing, detail = heartbeat.detect_dozing(
            server(self.dozing_series()), NOW, min_gaps=0
        )
        self.assertFalse(dozing)
        self.assertIsNone(detail)

    def test_a_down_engine_outranks_a_dozing_box(self):
        """Both true at once: report the one that is failing renders right now."""
        samples = [beat(m, ok=False) for m in range(60, 0, -7)]
        state, _ = heartbeat.assess_server(server(samples), NOW)
        self.assertEqual(state, heartbeat.DOWN)

    def test_dozing_alerts_and_re_alerts_like_any_other_bad_state(self):
        alert, record = heartbeat.decide_alert({}, heartbeat.DOZING, NOW)
        self.assertEqual(alert, heartbeat.ALERT_DOWN)
        self.assertEqual(record["state"], heartbeat.DOZING)

        recovered, record = heartbeat.decide_alert(record, heartbeat.OK, NOW)
        self.assertEqual(recovered, heartbeat.ALERT_RECOVERED)

    def test_gaps_outside_the_lookback_do_not_leak_into_the_verdict(self):
        """The window is bounded at both ends, including against future beats.

        A beat newer than `now` would otherwise pull a gap from outside the
        lookback into a reason line that claims to describe only the last hour.
        """
        samples = [beat(m, ok=True) for m in range(50, 0, -7)]
        samples.append(beat(-200, ok=True))  # 200 minutes in the future
        dozing, detail = heartbeat.detect_dozing(server(samples), NOW)
        self.assertTrue(dozing)
        self.assertNotIn("200 min", detail)
