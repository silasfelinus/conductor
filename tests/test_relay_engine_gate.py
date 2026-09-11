"""The engine gate: don't claim jobs when there is no ComfyUI to render them.

2026-09-02 — ComfyUI crash-looped under pm2 for hours. comfyui-mnemic-nodes
printed a "\N{HIGH VOLTAGE SIGN}" from its __init__, stdout was cp1252 (pm2
gives it a pipe, and the comfyui app had no PYTHONIOENCODING while kr-relay and
kr-download both did), and the resulting UnicodeEncodeError escaped
init_extra_nodes to kill main.py — before the Prompt Server ever bound 8188.
So the engine was not slow or wedged, it was absent, ~26s at a time, forever.

The model share stayed perfectly readable throughout, so the 2026-08-26 share
gate stayed open and the relay kept claiming into nothing: each job sat out
COMFY_RECOVERY_SECONDS at POST /prompt and then burned an attempt. The relay
had been posting COMFY ok:false on every heartbeat the whole time and never
consulted its own signal before claiming.

These lock the gate's behaviour and, most importantly, its wiring — a gate that
main() never calls is exactly the bug this replaces.
"""
import contextlib
import http.server
import importlib
import os
import socket
import sys
import threading
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
HOME_SERVER = REPO / "ops" / "home-server"


def load_relay(**env):
    """Import relay_agent fresh with `env` applied, and capture its log lines."""
    saved = dict(os.environ)
    os.environ.update({k: v for k, v in env.items() if v is not None})
    for key, value in env.items():
        if value is None:
            os.environ.pop(key, None)
    sys.path.insert(0, str(HOME_SERVER))
    try:
        sys.modules.pop("relay_agent", None)
        relay = importlib.import_module("relay_agent")
    finally:
        sys.path.remove(str(HOME_SERVER))
        os.environ.clear()
        os.environ.update(saved)

    lines = []
    relay.log = lambda message: lines.append(str(message))
    relay.logged = lines
    return relay


def closed_port_url():
    """A URL nothing is listening on — the crash-loop shape, refused instantly."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return f"http://127.0.0.1:{port}"


@contextlib.contextmanager
def stalled_engine():
    """A bound socket that accepts connections and never answers.

    This is what ComfyUI looks like while it stages a 9.4 GB unet into VRAM:
    the listener is up (so nothing is refused) and the event loop is not
    running (so nothing is served). A plain listening socket with no accept
    loop reproduces it exactly, and it is the case the probe used to call
    "down".
    """
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(8)
    try:
        yield f"http://127.0.0.1:{listener.getsockname()[1]}"
    finally:
        listener.close()


@contextlib.contextmanager
def fake_engine(status=200):
    """A localhost HTTP server standing in for ComfyUI's /system_stats."""

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"system":{}}')

        def log_message(self, *args):  # keep the test output clean
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class EngineProbeTests(unittest.TestCase):
    def test_probe_succeeds_against_a_live_engine(self):
        with fake_engine() as url:
            relay = load_relay(COMFY_URL=url)
            ok, detail = relay.probe_engine()
        self.assertTrue(ok)
        self.assertEqual(detail, "")

    def test_probe_reports_a_refused_connection(self):
        """Nothing listening is the crash-loop signature; name it, don't hide it."""
        url = closed_port_url()
        relay = load_relay(COMFY_URL=url)
        ok, detail = relay.probe_engine()
        self.assertFalse(ok)
        self.assertTrue(detail)
        self.assertIn("Error", detail)

    def test_probe_reports_a_non_200_as_down(self):
        """A process that answers 500 cannot render either."""
        with fake_engine(status=503) as url:
            relay = load_relay(COMFY_URL=url)
            ok, detail = relay.probe_engine()
        self.assertFalse(ok)
        self.assertTrue(detail)

    def test_probe_uses_system_stats(self):
        relay = load_relay()
        self.assertEqual(relay.ENGINE_PROBE_PATH, "/system_stats")


class BusyEngineTests(unittest.TestCase):
    """A render box mid-model-load is busy, not down.

    2026-09-11 — Silas: "comfy is listed as down, even though it just made that
    image." ComfyUI serves /system_stats from the process that also loads
    models, and staging wan2.2_ti2v_5B_fp16 (9.4 GB) holds its event loop for
    minutes. The probe's 10s timeout expired against a perfectly healthy engine
    and every failure was classified the same way, so the dashboard and the
    claim gate both called it dead. comfyui.err.log carries the other side of
    it: a burst of `ConnectionResetError: [WinError 10054]` at 15:30:34 — the
    probe hanging up — 33 seconds before `Model WanVAE prepared`.

    A refused connection still means down immediately; that is the 2026-09-02
    crash-loop the gate above exists for, and nothing about it is slow.
    """

    SHORT_TIMEOUT = "0.25"

    def test_a_timeout_is_classified_busy_not_down(self):
        with stalled_engine() as url:
            relay = load_relay(
                COMFY_URL=url, KR_ENGINE_PROBE_TIMEOUT=self.SHORT_TIMEOUT
            )
            status, detail, latency = relay.probe_engine_status()
        self.assertEqual(status, relay.ENGINE_BUSY, detail)
        self.assertIsNone(latency)

    def test_a_refused_connection_is_still_down_immediately(self):
        relay = load_relay(COMFY_URL=closed_port_url())
        status, _, _ = relay.probe_engine_status()
        self.assertEqual(status, relay.ENGINE_DOWN)

    def test_a_non_2xx_is_still_down_immediately(self):
        """Answering 503 is not being busy — it answered, and cannot render."""
        with fake_engine(status=503) as url:
            relay = load_relay(COMFY_URL=url)
            status, _, _ = relay.probe_engine_status()
        self.assertEqual(status, relay.ENGINE_DOWN)

    def test_busy_engine_keeps_claiming_inside_the_grace(self):
        with stalled_engine() as url:
            relay = load_relay(
                COMFY_URL=url,
                KR_ENGINE_PROBE_TIMEOUT=self.SHORT_TIMEOUT,
                KR_ENGINE_PROBE_SECONDS="0",
                KR_ENGINE_BUSY_GRACE_SECONDS="300",
            )
            self.assertTrue(relay.engine_available(now=1000.0))
            self.assertTrue(relay.engine_available(now=1200.0))

    def test_busy_engine_is_reported_down_once_the_grace_expires(self):
        """A genuine wedge must not hide behind the grace forever."""
        with stalled_engine() as url:
            relay = load_relay(
                COMFY_URL=url,
                KR_ENGINE_PROBE_TIMEOUT=self.SHORT_TIMEOUT,
                KR_ENGINE_PROBE_SECONDS="0",
                KR_ENGINE_BUSY_GRACE_SECONDS="300",
            )
            self.assertTrue(relay.engine_available(now=1000.0))
            self.assertFalse(relay.engine_available(now=1301.0))
        self.assertTrue(
            any("NOT claiming" in line for line in relay.logged), relay.logged
        )

    def test_busy_is_announced_once_not_every_poll(self):
        with stalled_engine() as url:
            relay = load_relay(
                COMFY_URL=url,
                KR_ENGINE_PROBE_TIMEOUT=self.SHORT_TIMEOUT,
                KR_ENGINE_PROBE_SECONDS="0",
                KR_ENGINE_BUSY_GRACE_SECONDS="300",
            )
            for tick in range(0, 200, 20):
                relay.engine_available(now=1000.0 + tick)
        busy_lines = [line for line in relay.logged if "BUSY" in line]
        self.assertEqual(len(busy_lines), 1, relay.logged)

    def test_recovery_clears_the_busy_window(self):
        """Two separate stalls must not add up into a false wedge."""
        relay = load_relay(
            KR_ENGINE_PROBE_TIMEOUT=self.SHORT_TIMEOUT,
            KR_ENGINE_PROBE_SECONDS="0",
            KR_ENGINE_BUSY_GRACE_SECONDS="300",
        )
        with stalled_engine() as stalled:
            relay.COMFY_URL = stalled
            self.assertTrue(relay.engine_available(now=1000.0))
        with fake_engine() as live:
            relay.COMFY_URL = live
            self.assertTrue(relay.engine_available(now=1200.0))
        with stalled_engine() as stalled:
            relay.COMFY_URL = stalled
            # 400s after the FIRST stall, but only 1s into this one.
            self.assertTrue(relay.engine_available(now=1400.0))

    def test_heartbeat_reports_a_busy_engine_as_up(self):
        """This is the line Silas actually reads on the dashboard."""
        with stalled_engine() as url:
            relay = load_relay(
                COMFY_URL=url, KR_ENGINE_PROBE_TIMEOUT=self.SHORT_TIMEOUT
            )
            posted = []
            relay.post_heartbeat = lambda *args, **kwargs: posted.append(
                (args, kwargs)
            )
            relay.resolve_seconds = lambda _url: 0.0
            relay.send_heartbeats()

        self.assertEqual(len(posted), 1)
        (engine, ok, _latency), kwargs = posted[0]
        self.assertEqual(engine, "COMFY")
        self.assertTrue(ok, "a busy engine must not be heartbeat as down")
        self.assertIn("busy", (kwargs.get("note") or "").lower())

    def test_heartbeat_still_reports_a_refused_engine_as_down(self):
        relay = load_relay(COMFY_URL=closed_port_url())
        posted = []
        relay.post_heartbeat = lambda *args, **kwargs: posted.append(
            (args, kwargs)
        )
        relay.resolve_seconds = lambda _url: 0.0
        relay.send_heartbeats()

        (_engine, ok, _latency), _kwargs = posted[0]
        self.assertFalse(ok)

    def test_heartbeat_reports_a_live_engine_as_up_with_no_note(self):
        with fake_engine() as url:
            relay = load_relay(COMFY_URL=url)
            posted = []
            relay.post_heartbeat = lambda *args, **kwargs: posted.append(
                (args, kwargs)
            )
            relay.resolve_seconds = lambda _url: 0.0
            relay.send_heartbeats()

        (_engine, ok, latency), kwargs = posted[0]
        self.assertTrue(ok)
        self.assertIsInstance(latency, int)
        self.assertIsNone(kwargs.get("note"))


class EngineGateTests(unittest.TestCase):
    def test_gate_is_on_by_default(self):
        relay = load_relay(KR_ENGINE_GATE=None)
        self.assertTrue(relay.KR_ENGINE_GATE)

    def test_gate_can_be_disabled(self):
        """KR_ENGINE_GATE=0 -> previous always-claim behaviour, silently."""
        relay = load_relay(KR_ENGINE_GATE="0", COMFY_URL=closed_port_url())
        self.assertFalse(relay.KR_ENGINE_GATE)
        self.assertTrue(relay.engine_available())
        self.assertEqual(relay.logged, [])

    def test_live_engine_permits_claiming(self):
        with fake_engine() as url:
            relay = load_relay(COMFY_URL=url)
            self.assertTrue(relay.engine_available(now=1000.0))

    def test_dead_engine_blocks_claiming(self):
        relay = load_relay(COMFY_URL=closed_port_url())
        self.assertFalse(relay.engine_available(now=1000.0))

    def test_block_is_logged_once_not_every_poll(self):
        """A 2s poll loop must not emit a line every 2s while pm2 restarts it."""
        relay = load_relay(
            COMFY_URL=closed_port_url(), KR_ENGINE_PROBE_SECONDS="15"
        )
        for tick in range(0, 300, 15):
            relay.engine_available(now=1000.0 + tick)
        self.assertEqual(len(relay.logged), 1, relay.logged)
        self.assertIn("NOT claiming", relay.logged[0])

    def test_a_healthy_first_probe_says_nothing(self):
        """Don't announce a recovery from an outage that never happened."""
        with fake_engine() as url:
            relay = load_relay(COMFY_URL=url)
            self.assertTrue(relay.engine_available(now=1000.0))
        self.assertEqual(relay.logged, [])

    def test_a_failing_first_probe_still_warns(self):
        relay = load_relay(COMFY_URL=closed_port_url())
        self.assertFalse(relay.engine_available(now=1000.0))
        self.assertEqual(len(relay.logged), 1, relay.logged)
        self.assertIn("NOT claiming", relay.logged[0])

    def test_recovery_is_logged(self):
        relay = load_relay(
            COMFY_URL=closed_port_url(), KR_ENGINE_PROBE_SECONDS="0"
        )
        self.assertFalse(relay.engine_available(now=1000.0))
        with fake_engine() as url:
            relay.COMFY_URL = url
            self.assertTrue(relay.engine_available(now=1001.0))
        self.assertEqual(len(relay.logged), 2, relay.logged)
        self.assertIn("answering again", relay.logged[1])

    def test_result_is_cached_between_probes(self):
        with fake_engine() as url:
            relay = load_relay(COMFY_URL=url, KR_ENGINE_PROBE_SECONDS="15")
            calls = []
            real = relay.probe_engine_status
            relay.probe_engine_status = lambda *a, **k: (calls.append(1), real())[1]

            relay.engine_available(now=1000.0)
            relay.engine_available(now=1005.0)
            relay.engine_available(now=1014.0)
            self.assertEqual(len(calls), 1, calls)

            relay.engine_available(now=1016.0)
            self.assertEqual(len(calls), 2, calls)

    def test_blocked_message_points_at_the_engine_not_the_queue(self):
        url = closed_port_url()
        relay = load_relay(COMFY_URL=url)
        relay.engine_available(now=1000.0)
        message = relay.logged[0]
        self.assertIn(url, message)
        self.assertIn("pm2", message)
        self.assertIn("retry budget", message)


class MainLoopWiringTests(unittest.TestCase):
    """A gate main() never calls is the bug, not the fix."""

    def drive_one_pass(self, relay):
        """Run main()'s poll loop for exactly one pass, then break out.

        main() swallows Exception on purpose (the relay must survive a failed
        job) but re-raises KeyboardInterrupt, so that is the only sentinel that
        can stop it from the inside.
        """
        relay.log_build_identity = lambda: None
        relay.install_shutdown_handler = lambda: None
        relay.warm_object_info_async = lambda: None
        relay.send_heartbeats = lambda: None
        relay.HEARTBEAT_SECONDS = 0
        relay.POLL_SECONDS = 0

        claims = []
        relay.claim_job = lambda: claims.append(1)

        def stop(_seconds):
            raise KeyboardInterrupt

        with mock.patch.object(relay.time, "sleep", stop):
            with self.assertRaises(KeyboardInterrupt):
                relay.main()
        return claims

    def test_main_does_not_claim_while_the_engine_is_down(self):
        relay = load_relay(
            KR_RELAY_TOKEN="test-token",
            KR_RELAY_USER_ID="1",
            KR_SHARE_PROBE_PATH=None,
            COMFY_URL=closed_port_url(),
        )
        relay.share_available = lambda *a, **k: True
        claims = self.drive_one_pass(relay)
        self.assertEqual(claims, [], "claimed a job with no engine to render it")

    def test_main_claims_when_the_engine_is_up(self):
        """The gate must not wedge the relay shut on a healthy box."""
        with fake_engine() as url:
            relay = load_relay(
                KR_RELAY_TOKEN="test-token",
                KR_RELAY_USER_ID="1",
                KR_SHARE_PROBE_PATH=None,
                COMFY_URL=url,
            )
            relay.share_available = lambda *a, **k: True
            claims = self.drive_one_pass(relay)
        self.assertEqual(claims, [1])


    def test_kr_relay_actually_runs_this_loop(self):
        """The pm2 app is relay_media_agent.py, not relay_agent.py.

        It overrides run_comfy and process but delegates the poll loop itself
        to relay.main() — which is the only reason a gate added in relay_agent
        protects the process that does the claiming. If that ever changes, this
        gate silently stops applying to the only relay in production.
        """
        source = (HOME_SERVER / "relay_media_agent.py").read_text(encoding="utf-8")
        self.assertIn("relay.main()", source)
        self.assertNotIn("def main(", source)


class EcosystemConfigTests(unittest.TestCase):
    """The root cause: pm2's comfyui app had no PYTHONIOENCODING."""

    def test_every_python_app_forces_utf8_stdout(self):
        config = (HOME_SERVER / "ecosystem.config.js").read_text(encoding="utf-8")
        # Crude but honest: one env block per app, and all three are Python.
        # kr-relay and kr-download carried this since 2026-08-13; comfyui,
        # which loads the third-party custom nodes whose banners we do not
        # control, did not -- and it is the one that died of it.
        self.assertEqual(
            config.count("PYTHONIOENCODING: 'utf-8'"),
            3,
            "every pm2 Python app needs PYTHONIOENCODING; comfyui is the one "
            "that crash-looped without it (2026-09-02)",
        )


if __name__ == "__main__":
    unittest.main()
