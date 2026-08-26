"""The pre-drain gate must notice a box that answers HTTP but cannot render.

2026-08-25: the render box's SMB model share stopped authenticating, so ComfyUI
could not read a single model file for ~15 hours. media.acrocatranch.com kept
answering HTTP 404 at its root the whole time, so this gate kept reporting UP and
auto-art-generate kept enqueuing -- the FAILED backlog grew from 420 to 448
during the incident review itself.
"""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_render_box.py"
spec = importlib.util.spec_from_file_location("check_render_box", SCRIPT)
check = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(check)


def test_failures_with_nothing_completing_is_a_down_box():
    healthy, reason = check.render_throughput_verdict({"DONE": 0, "FAILED": 262})
    assert healthy is False
    assert "262" in reason


def test_any_completed_render_is_healthy_even_alongside_failures():
    # A box that is producing images is working; some jobs fail for their own
    # reasons and that must not stop the queue.
    healthy, _reason = check.render_throughput_verdict({"DONE": 73, "FAILED": 262})
    assert healthy is True


def test_an_idle_queue_is_not_a_broken_box():
    for throughput in ({}, {"DONE": 0, "FAILED": 0}, {"DONE": 0, "FAILED": 1}):
        healthy, _reason = check.render_throughput_verdict(throughput)
        assert healthy is None, throughput


def test_a_couple_of_failures_is_not_yet_sustained():
    healthy, _reason = check.render_throughput_verdict(
        {"DONE": 0, "FAILED": check.SUSTAINED_FAILURE_COUNT - 1}
    )
    assert healthy is None


def test_unreadable_stats_yield_no_opinion():
    for throughput in (None, "nope", [], 7):
        healthy, _reason = check.render_throughput_verdict(throughput)
        assert healthy is None, throughput


def test_gate_fails_when_reachable_but_not_rendering(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(check, "fetch_throughput", lambda: {"DONE": 0, "FAILED": 262})
    assert check.main() == 1


def test_gate_passes_when_reachable_and_rendering(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(check, "fetch_throughput", lambda: {"DONE": 73, "FAILED": 0})
    assert check.main() == 0


def test_gate_passes_on_an_idle_queue(monkeypatch):
    # No throughput signal must never turn a reachable box into a blocked one.
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (True, 404))
    monkeypatch.setattr(check, "fetch_throughput", lambda: None)
    assert check.main() == 0


def test_unreachable_origin_still_fails_first(monkeypatch):
    monkeypatch.setattr(check, "render_box_reachable", lambda *a, **k: (False, "refused"))
    monkeypatch.setattr(
        check, "fetch_throughput", lambda: (_ for _ in ()).throw(AssertionError)
    )
    assert check.main() == 1
