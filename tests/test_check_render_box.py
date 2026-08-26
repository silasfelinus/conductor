"""The pre-drain gate must notice a box that answers HTTP but cannot render.

2026-08-25: the render box's SMB model share stopped authenticating, so ComfyUI
could not read a single model file for ~15 hours. media.acrocatranch.com kept
answering HTTP 404 at its root the whole time, so this gate kept reporting UP and
auto-art-generate kept enqueuing -- the FAILED backlog grew from 420 to 448
during the incident review itself.

2026-08-26: `render_throughput_verdict` short-circuited on `if done: return True`
-- any completion inside the window was treated as proof of health, no matter
how long ago it happened. During the ruler-hooked art batch, 40 ArtJobs were
submitted into a queue that had been genuinely empty; the first job claimed and
then sat RUNNING with no movement for 35+ minutes while nothing else started.
The gate kept reporting UP on the strength of completions that all predated the
batch. Fixed by checking `staleRunningCount`/`queueDepth.PENDING` (already in
the same stats payload) before the "any completion is healthy" shortcut.
"""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_render_box.py"
spec = importlib.util.spec_from_file_location("check_render_box", SCRIPT)
check = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(check)


def test_failures_with_nothing_completing_is_a_down_box():
    healthy, reason = check.render_throughput_verdict(
        {"windowThroughput": {"DONE": 0, "FAILED": 262}}
    )
    assert healthy is False
    assert "262" in reason


def test_any_completed_render_is_healthy_even_alongside_failures():
    # A box that is producing images is working; some jobs fail for their own
    # reasons and that must not stop the queue.
    healthy, _reason = check.render_throughput_verdict(
        {"windowThroughput": {"DONE": 73, "FAILED": 262}}
    )
    assert healthy is True


def test_an_idle_queue_is_not_a_broken_box():
    for throughput in ({}, {"DONE": 0, "FAILED": 0}, {"DONE": 0, "FAILED": 1}):
        healthy, _reason = check.render_throughput_verdict({"windowThroughput": throughput})
        assert healthy is None, throughput


def test_a_couple_of_failures_is_not_yet_sustained():
    healthy, _reason = check.render_throughput_verdict(
        {"windowThroughput": {"DONE": 0, "FAILED": check.SUSTAINED_FAILURE_COUNT - 1}}
    )
    assert healthy is None


def test_unreadable_stats_yield_no_opinion():
    for data in (None, "nope", [], 7):
        healthy, _reason = check.render_throughput_verdict(data)
        assert healthy is None, data


def test_missing_queue_depth_and_stale_count_default_to_zero():
    # A stats payload that omits the new fields entirely (older server, or a
    # partial response) must not crash and must not be treated as stalled.
    healthy, _reason = check.render_throughput_verdict(
        {"windowThroughput": {"DONE": 73, "FAILED": 0}}
    )
    assert healthy is True


def test_stale_running_claim_with_pending_backlog_is_down_even_with_past_completions():
    # The exact 2026-08-26 shape: completions earlier in the window, but a
    # claim has gone stale and pending work is stacking up behind it right now.
    healthy, reason = check.render_throughput_verdict(
        {
            "windowThroughput": {"DONE": 42, "FAILED": 0},
            "staleRunningCount": 1,
            "queueDepth": {"PENDING": 39, "RUNNING": 1, "DONE": 5376},
        }
    )
    assert healthy is False
    assert "stale" in reason
    assert "39" in reason


def test_stale_running_claim_without_pending_backlog_is_not_flagged():
    # A stale claim with nothing waiting behind it isn't blocking any work --
    # stay conservative and don't call it down on that signal alone.
    healthy, _reason = check.render_throughput_verdict(
        {
            "windowThroughput": {"DONE": 0, "FAILED": 0},
            "staleRunningCount": 1,
            "queueDepth": {"PENDING": 0, "RUNNING": 1},
        }
    )
    assert healthy is None


def test_pending_backlog_without_a_stale_claim_is_not_flagged():
    # Pending work with a healthy (non-stale) claim in flight is just a normal
    # working queue, not evidence of a stall.
    healthy, _reason = check.render_throughput_verdict(
        {
            "windowThroughput": {"DONE": 0, "FAILED": 0},
            "staleRunningCount": 0,
            "queueDepth": {"PENDING": 10, "RUNNING": 1},
        }
    )
    assert healthy is None


def test_gate_fails_when_reachable_but_not_rendering(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(
        check, "fetch_queue_stats", lambda: {"windowThroughput": {"DONE": 0, "FAILED": 262}}
    )
    assert check.main() == 1


def test_gate_fails_on_a_stalled_queue_despite_past_completions(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(
        check,
        "fetch_queue_stats",
        lambda: {
            "windowThroughput": {"DONE": 42, "FAILED": 0},
            "staleRunningCount": 1,
            "queueDepth": {"PENDING": 39},
        },
    )
    assert check.main() == 1


def test_gate_passes_when_reachable_and_rendering(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(
        check, "fetch_queue_stats", lambda: {"windowThroughput": {"DONE": 73, "FAILED": 0}}
    )
    assert check.main() == 0


def test_gate_passes_on_an_idle_queue(monkeypatch):
    # No throughput signal must never turn a reachable box into a blocked one.
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(check, "fetch_queue_stats", lambda: None)
    assert check.main() == 0


def test_unreachable_origin_still_fails_first(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (False, "refused"))
    monkeypatch.setattr(
        check, "fetch_queue_stats", lambda: (_ for _ in ()).throw(AssertionError)
    )
    assert check.main() == 1
