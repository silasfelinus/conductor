import importlib.util
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "drain_failed_art_backlog.py"
)
spec = importlib.util.spec_from_file_location("drain_failed_art_backlog", SCRIPT)
drain = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(drain)


# The exact error strings observed on the 2026-08-25 backlog, trimmed. These are
# the regression cases -- if a rewrite of FAILURE_PATTERNS stops matching one of
# them, a real 400-job backlog silently becomes unretryable "unknown".
WIN_IO_ERROR = (
    "ComfyUI POST /prompt failed at http://127.0.0.1:8188 (ComfyUI /prompt "
    "returned HTTP 400 at http://127.0.0.1:8188: {'1': {'errors': [{'type': "
    "'exception_during_inner_validation', 'details': \"[WinError 1117] The "
    "request could not be performed because of an I/O device error: "
    "'Z:\\\\ai\\\\models\\\\unet'\"}]}}). No accepted prompt for client "
    "Silas-PC-prompt-1787694898990483500 appeared within 120.0s."
)
HOSTBUF_ERROR = (
    "ComfyUI reported a workflow error: node 3 (CLIPTextEncode): "
    "hostbuf_file_reader_read failed"
)
MISSING_MODEL_ERROR = (
    "ComfyUI has no matching file for: "
    "CLIPLoader.clip_name='flux2_klein_text_encoder_fp8_scaled.safetensors'. "
    "Not in the live model list at http://127.0.0.1:8188 (missing, misnamed, or "
    "an ambiguous basename)."
)
STALE_CLAIM_ERROR = "Stale claim reaped: relay stopped responding after 3 attempts."
COMPLETE_500_ERROR = (
    "complete(9004) failed: HTTP 500 Database operation failed: Invalid "
    "`prisma.character.findUnique()` invocation: The column `Character.size` "
    "does not exist in the current database."
)


def test_render_host_io_faults_are_retryable():
    for error in (WIN_IO_ERROR, HOSTBUF_ERROR):
        failure_class = drain.classify_failure({"error": error})
        assert failure_class == "render-host-io", error[:60]
        assert drain.is_retryable(failure_class)


def test_missing_model_is_classified_before_the_render_host_patterns():
    # This error names the ComfyUI URL and would match a looser host pattern.
    # Resubmitting it verbatim fails again every time, so specificity order in
    # FAILURE_PATTERNS is load-bearing, not cosmetic.
    failure_class = drain.classify_failure({"error": MISSING_MODEL_ERROR})
    assert failure_class == "payload-model-missing"
    assert not drain.is_retryable(failure_class)


def test_win_io_error_beats_the_trailing_timeout_phrase():
    # WIN_IO_ERROR ends in "appeared within 120.0s", which relay-stalled also
    # matches. The drive fault is the real cause and must win.
    assert drain.classify_failure({"error": WIN_IO_ERROR}) == "render-host-io"


def test_relay_and_kr_api_faults_are_retryable():
    assert drain.classify_failure({"error": STALE_CLAIM_ERROR}) == "relay-stalled"
    assert drain.classify_failure({"error": COMPLETE_500_ERROR}) == "kr-api-error"
    assert drain.is_retryable("relay-stalled")
    assert drain.is_retryable("kr-api-error")


def test_unrecognized_and_empty_errors_default_to_deny():
    for error in ("something nobody has seen before", "", None):
        failure_class = drain.classify_failure({"error": error})
        assert failure_class == "unknown"
        assert not drain.is_retryable(failure_class)


def test_failure_diagnostic_is_prompt_free_and_bounded():
    diagnostic = drain.failure_diagnostic(
        {
            "id": 9000,
            "engine": "COMFY",
            "projectSlug": "cthulhuquarium",
            "error": "x" * 2000,
            "payload": {"promptString": "SECRET PROMPT SHOULD NOT APPEAR"},
        }
    )
    assert diagnostic.startswith("ArtJob 9000 [cthulhuquarium] engine=COMFY: ")
    assert "SECRET PROMPT" not in diagnostic
    assert diagnostic.endswith("…")
    assert len(diagnostic) < drain.DIAGNOSTIC_ERROR_LIMIT + 100


def test_failure_diagnostic_collapses_whitespace():
    assert drain.failure_diagnostic(
        {"id": 1, "engine": "A1111", "error": "connection\n refused\t now"}
    ) == "ArtJob 1 [-] engine=A1111: connection refused now"


def _stub_requeue(monkeypatch, queued):
    monkeypatch.setattr(drain, "requeue", lambda ids: (list(queued), []))


def test_canary_refuses_to_drain_when_nothing_rendered(monkeypatch):
    # The 2026-08-25 case: the requeue succeeds, the host claims the job, and it
    # fails anyway. The backlog must be left alone.
    _stub_requeue(monkeypatch, [9511])
    monkeypatch.setattr(drain, "job_status", lambda job_id: "FAILED")
    assert drain.run_canary([9511], sleep=lambda _s: None) is False


def test_canary_allows_the_drain_after_one_real_render(monkeypatch):
    _stub_requeue(monkeypatch, [9511, 9512])
    statuses = {9511: "DONE", 9512: "FAILED"}
    monkeypatch.setattr(drain, "job_status", lambda job_id: statuses[job_id])
    assert drain.run_canary([9511, 9512], sleep=lambda _s: None) is True


def test_canary_stops_when_the_requeue_itself_fails(monkeypatch):
    monkeypatch.setattr(drain, "requeue", lambda ids: ([], list(ids)))
    assert drain.run_canary([9511], sleep=lambda _s: None) is False


def test_canary_times_out_rather_than_draining_on_a_stuck_job(monkeypatch):
    _stub_requeue(monkeypatch, [9511])
    monkeypatch.setattr(drain, "job_status", lambda job_id: "RUNNING")
    assert (
        drain.run_canary([9511], timeout_seconds=0, sleep=lambda _s: None) is False
    )


def test_chunks_splits_without_dropping_ids():
    assert list(drain.chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


# 2026-08-25T22:25Z, 30 jobs. Both files are registered in Kind Robots and both
# were used by every job that rendered fine at 07:20Z the same morning. The
# names did not change; the box's answer about which files exist did.
VANISHED_MODEL_ERROR = (
    "ComfyUI has no matching file for: "
    "CLIPLoader.clip_name='qwen3vl_4b_fp8_scaled.safetensors'; "
    "VAELoader.vae_name='qwen_image_vae.safetensors'. Not in the live model "
    "list at http://127.0.0.1:8188 (missing, misnamed, or an ambiguous "
    "basename). Failing fast instead of submitting a prompt ComfyUI would "
    "reject."
)

REGISTERED = {
    "qwen3vl_4b_fp8_scaled.safetensors",
    "qwen_image_vae.safetensors",
    "Krea-2-Turbo-Q5_K_S.gguf",
}


def test_missing_asset_names_reads_every_named_file():
    assert drain.missing_asset_names(VANISHED_MODEL_ERROR) == [
        "qwen3vl_4b_fp8_scaled.safetensors",
        "qwen_image_vae.safetensors",
    ]


def test_missing_asset_names_stops_at_the_live_list_sentence():
    # The trailing prose contains a URL and parentheses; nothing there should be
    # mistaken for a filename.
    assert "8188" not in "".join(drain.missing_asset_names(VANISHED_MODEL_ERROR))


def test_registered_models_that_vanished_are_retryable():
    job = {"id": 9542, "error": VANISHED_MODEL_ERROR}
    failure_class = drain.classify_failure(job, registered=REGISTERED)
    assert failure_class == "render-host-model-vanished"
    assert drain.is_retryable(failure_class)


def test_an_unregistered_model_stays_a_payload_fault():
    # ArtJob 9181: this filename was invented and never existed anywhere.
    job = {"id": 9181, "error": MISSING_MODEL_ERROR}
    failure_class = drain.classify_failure(job, registered=REGISTERED)
    assert failure_class == "payload-model-missing"
    assert not drain.is_retryable(failure_class)


def test_a_partly_registered_rejection_is_held_back():
    error = (
        "ComfyUI has no matching file for: "
        "CLIPLoader.clip_name='qwen3vl_4b_fp8_scaled.safetensors'; "
        "VAELoader.vae_name='never_existed.safetensors'. Not in the live model "
        "list at http://127.0.0.1:8188."
    )
    assert (
        drain.classify_failure({"error": error}, registered=REGISTERED)
        == "payload-model-missing"
    )


def test_an_unreadable_registry_holds_missing_models_back():
    # Can't tell "lost" from "misnamed" without the registry, so don't guess in
    # the direction that resubmits 400 jobs.
    job = {"id": 9542, "error": VANISHED_MODEL_ERROR}
    assert drain.classify_failure(job, registered=None) == "payload-model-missing"
    assert drain.classify_failure(job, registered=set()) == "payload-model-missing"
