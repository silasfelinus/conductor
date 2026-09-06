"""The on-box watchdog must be able to say "crash loop".

2026-09-02, from ops/home-server/logs/healthcheck.log:

    2026-08-31   288 ticks
    2026-09-01    30 ticks, last at 02:26:07
    2026-09-02    (nothing)

The watchdog stopped running ~37 hours before the outage was noticed, so the
primary net is now off-box (see check_engine_heartbeat.py + the Render Box
Watchdog workflow). But the on-box gate had a real hole too, and it is the one
that would have caught this in five minutes if the task had been alive:

    if ($status.status -ne 'online') { ... continue }

That branch exists so a deliberate `pm2 stop` is not fought. It cannot tell a
stop from a crash loop. ComfyUI died ~26s into every start, so at any given
tick pm2 reported 'online' most of the time and 'waiting restart' the rest --
and after max_restarts (50) it parks in 'errored', which the same branch also
waved through, silently and permanently.

Note the log records ZERO "pm2 status is" lines, so this hole did not actually
fire during that outage; the watchdog was simply not running. It is fixed here
because it is real, not because it was the cause.

PowerShell cannot run in CI, so these lock the structure the fix depends on.
"""
import json
import subprocess
import unittest
from pathlib import Path

HOME_SERVER = Path(__file__).resolve().parents[1] / "ops" / "home-server"
SCRIPT = HOME_SERVER / "healthcheck.ps1"
SNAPSHOT = HOME_SERVER / "pm2-jlist-snapshot.js"


class SnapshotTests(unittest.TestCase):
    """The projection must carry the crash-loop signal without re-introducing
    the case-collision bug it exists to avoid."""

    def project(self, jlist):
        result = subprocess.run(
            ["node", str(SNAPSHOT)],
            input=json.dumps(jlist),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_restart_counters_survive_the_projection(self):
        out = self.project(
            [{"name": "comfyui", "pm2_env": {"status": "online", "restart_time": 47}}]
        )
        self.assertEqual(out[0]["pm2_env"]["restart_time"], 47)

    def test_username_collision_is_still_stripped(self):
        """PowerShell 5.1's ConvertFrom-Json is case-insensitive and throws on
        an env carrying both `username` and `USERNAME`. That is why this helper
        exists at all -- adding fields must not start passing the env through."""
        out = self.project(
            [
                {
                    "name": "comfyui",
                    "pm2_env": {
                        "status": "online",
                        "restart_time": 1,
                        "username": "a",
                        "USERNAME": "b",
                        "env": {"PATH": "..."},
                    },
                }
            ]
        )
        self.assertEqual(
            set(out[0]["pm2_env"]),
            {"status", "restart_time", "unstable_restarts", "pm_uptime"},
        )

    def test_missing_counters_become_null_not_a_crash(self):
        out = self.project([{"name": "kr-relay", "pm2_env": {"status": "errored"}}])
        self.assertIsNone(out[0]["pm2_env"]["restart_time"])

    def test_a_non_numeric_counter_is_rejected(self):
        out = self.project(
            [{"name": "x", "pm2_env": {"status": "online", "restart_time": "47"}}]
        )
        self.assertIsNone(out[0]["pm2_env"]["restart_time"])


class HealthcheckScriptTests(unittest.TestCase):
    def setUp(self):
        self.source = SCRIPT.read_text(encoding="utf-8")

    def test_stays_ascii_only(self):
        """PowerShell 5.1 reads a no-BOM script as the system ANSI codepage, so
        one smart quote or em-dash in a string literal corrupts parsing. The
        file says so at the top; this enforces it."""
        offenders = [
            (n, line)
            for n, line in enumerate(self.source.splitlines(), 1)
            if not line.isascii()
        ]
        self.assertEqual(offenders, [], f"non-ASCII content: {offenders}")

    def test_errored_is_an_alarm_not_a_shrug(self):
        """pm2 giving up is the most silent state a backend can be in."""
        self.assertIn("$status.status -eq 'errored'", self.source)
        self.assertIn("ERRORED: $($t.Name) on $hostName", self.source)

    def test_only_a_deliberate_stop_is_waved_through_silently(self):
        self.assertIn("$status.status -eq 'stopped'", self.source)
        self.assertIn("deliberate, leaving it alone", self.source)
        self.assertNotIn("- leaving it alone\"\n        continue", self.source)

    def test_crash_loop_is_detected_by_the_restart_counter(self):
        """Status cannot express a crash loop; the climbing counter can."""
        self.assertIn("$crashLoopRestarts", self.source)
        self.assertIn("restart_time", self.source)
        self.assertIn("CRASH LOOP:", self.source)

    def test_crash_loop_alert_says_not_to_just_restart_it(self):
        self.assertIn("Restarting it again will not help", self.source)

    def test_crash_loop_alert_warns_that_silence_is_not_recovery(self):
        """pm2 parks it at max_restarts and the alerts stop. Say so, or the
        absence of email reads as 'fixed itself'."""
        self.assertIn("do not read silence as recovery", self.source)

    def test_the_threshold_clears_an_ordinary_single_restart(self):
        """A deploy or a watchdog restart moves the counter by 1."""
        self.assertIn("$crashLoopRestarts = 3", self.source)

    def test_it_logs_before_anything_that_can_block(self):
        """A run that hangs must leave a trace.

        2026-09-01: the log stopped at 02:26:07 and stayed empty for 37+ hours
        while Task Scheduler reported the task running every 5 minutes with
        LastTaskResult 0x40010004 ("terminated"). The 'tick' heartbeat could not
        show that, because it sits after the pm2 block -- a run that hung in
        pm2 wrote nothing, which reads exactly like a run that never happened.
        """
        start = self.source.index('Write-Log "run starting')
        pm2 = self.source.index("--- pm2 visibility")
        tick = self.source.index('Write-Log "tick as')
        self.assertLess(start, pm2, "the first log line must precede the pm2 block")
        self.assertLess(pm2, tick, "the tick line still reports the app list")

    def test_pm2_jlist_cannot_hang_forever(self):
        """An unbounded jlist wedges the whole watchdog for every future run."""
        self.assertIn("$pm2TimeoutSeconds", self.source)
        self.assertIn("Wait-Job $pm2Job -Timeout $pm2TimeoutSeconds", self.source)
        self.assertIn("did not respond within", self.source)
        self.assertNotIn("(& $pm2Command.Source jlist 2>&1 | Out-String)", self.source)

    def test_the_jlist_timeout_stays_under_the_task_interval(self):
        """A timeout longer than the 5-minute schedule reintroduces the overlap
        that had Task Scheduler killing each run with the next."""
        self.assertIn("$pm2TimeoutSeconds = 60", self.source)

    def test_a_timed_out_job_is_stopped_and_reaped(self):
        """Otherwise every 5-minute run leaks a PowerShell job."""
        self.assertIn("Stop-Job $pm2Job", self.source)
        self.assertIn("Remove-Job $pm2Job -Force", self.source)

    def test_transitional_states_still_skip_the_probe(self):
        """Probing a process mid-launch produces a false hang and a pointless
        restart -- the double-restart observed 2026-08-28."""
        self.assertIn("in transition, probing next tick", self.source)


if __name__ == "__main__":
    unittest.main()
