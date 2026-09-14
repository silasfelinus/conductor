import yaml

from scripts import consume_coloring_book_studio_request as mod


def make_queue(entries):
    return {
        "books": [
            {
                "slug": "monster-recast",
                "entries": entries,
            }
        ]
    }


def write_queue_file(tmp_path, entries, monkeypatch):
    queue_file = tmp_path / "color-art-jobs.yaml"
    queue_file.write_text(yaml.safe_dump(make_queue(entries)), encoding="utf-8")
    monkeypatch.setattr(mod.coloring, "QUEUE_FILE", queue_file)
    return queue_file


def test_prepare_requested_entries_skips_already_done_ids_without_force(tmp_path, monkeypatch):
    entries = [
        {"id": "mr-001", "status": "pending"},
        {"id": "mr-009", "status": "done", "art_image_id": 13144},
        {"id": "mr-016", "status": "done", "art_image_id": 13164},
    ]
    queue_file = write_queue_file(tmp_path, entries, monkeypatch)

    already_resolved, would_force = mod.prepare_requested_entries(
        "monster-recast", ["mr-001", "mr-009", "mr-016"], force=False
    )

    assert already_resolved == [("mr-009", "done"), ("mr-016", "done")]
    assert would_force == []
    # Nothing was mutated: the already-done entries keep their status and data.
    reloaded = yaml.safe_load(queue_file.read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in reloaded["books"][0]["entries"]}
    assert by_id["mr-009"]["status"] == "done"
    assert by_id["mr-009"]["art_image_id"] == 13144
    assert by_id["mr-016"]["status"] == "done"


def test_prepare_requested_entries_all_already_resolved_returns_full_list(tmp_path, monkeypatch):
    entries = [
        {"id": "mr-009", "status": "done"},
        {"id": "mr-016", "status": "approved"},
    ]
    write_queue_file(tmp_path, entries, monkeypatch)

    already_resolved, would_force = mod.prepare_requested_entries(
        "monster-recast", ["mr-009", "mr-016"], force=False
    )

    assert set(already_resolved) == {("mr-009", "done"), ("mr-016", "approved")}
    assert would_force == []


def test_prepare_requested_entries_force_live_resets_non_pending_entries(tmp_path, monkeypatch):
    entries = [
        {
            "id": "mr-009",
            "status": "done",
            "art_image_id": 13144,
            "rendered_path": "some/path.webp",
            "image_path": "some/path.webp",
        },
    ]
    write_queue_file(tmp_path, entries, monkeypatch)

    already_resolved, would_force = mod.prepare_requested_entries(
        "monster-recast", ["mr-009"], force=True, live=True
    )

    assert already_resolved == []
    assert would_force == []
    reloaded_file = mod.coloring.QUEUE_FILE
    reloaded = yaml.safe_load(reloaded_file.read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in reloaded["books"][0]["entries"]}
    assert by_id["mr-009"]["status"] == "pending"
    assert "art_image_id" not in by_id["mr-009"]


def test_prepare_requested_entries_force_without_live_does_not_mutate_state(tmp_path, monkeypatch):
    """`--force` alone (no `--live`) must be a pure dry-run preview: it must
    never archive the existing candidate file or rewrite the queue's
    persisted status -- that mutation is real state a genuine dry run must
    not touch. Regression test for a live incident (coloring-book/t-022,
    2026-09-14): a `--force` probe without `--live` archived a real
    accepted-review candidate image and reset its queue status before the
    mistake was caught and manually reverted.
    """
    entries = [
        {
            "id": "mr-009",
            "status": "done",
            "art_image_id": 13144,
            "rendered_path": "some/path.webp",
            "image_path": "some/path.webp",
        },
    ]
    queue_file = write_queue_file(tmp_path, entries, monkeypatch)
    before = queue_file.read_text(encoding="utf-8")

    already_resolved, would_force = mod.prepare_requested_entries(
        "monster-recast", ["mr-009"], force=True, live=False
    )

    assert already_resolved == []
    assert would_force == ["mr-009"]
    # Nothing was mutated on disk: byte-identical to before the call.
    assert queue_file.read_text(encoding="utf-8") == before


def test_main_skips_stale_done_ids_and_processes_remaining_pending(tmp_path, monkeypatch, capsys):
    entries = [
        {"id": "mr-001", "status": "pending", "set": "monster-recast", "concept_id": "mr-001"},
        {"id": "mr-009", "status": "done"},
    ]
    write_queue_file(tmp_path, entries, monkeypatch)

    def fake_selected_entries(book_slug, proposal_ids):
        assert proposal_ids == ["mr-001"]
        return [{"set": "monster-recast", "concept_id": "mr-001"}]

    def fake_run_entries(entries, *, live, timeout):
        assert len(entries) == 1
        return 0

    monkeypatch.setattr(mod, "selected_entries", fake_selected_entries)
    monkeypatch.setattr(mod, "run_entries", fake_run_entries)
    monkeypatch.setattr(
        "sys.argv",
        [
            "consume_coloring_book_studio_request.py",
            "--book",
            "monster-recast",
            "--proposal-id",
            "mr-001",
            "--proposal-id",
            "mr-009",
        ],
    )

    exit_code = mod.main()

    assert exit_code == 0
    err = capsys.readouterr().err
    assert "Skipping already-resolved proposal(s)" in err
    assert "mr-009 (done)" in err


def test_main_returns_zero_when_every_requested_id_is_already_resolved(tmp_path, monkeypatch, capsys):
    entries = [{"id": "mr-009", "status": "done"}]
    write_queue_file(tmp_path, entries, monkeypatch)

    def fail_if_called(*args, **kwargs):
        raise AssertionError("run_entries must not be called with nothing left to do")

    monkeypatch.setattr(mod, "run_entries", fail_if_called)
    monkeypatch.setattr(
        "sys.argv",
        [
            "consume_coloring_book_studio_request.py",
            "--book",
            "monster-recast",
            "--proposal-id",
            "mr-009",
        ],
    )

    exit_code = mod.main()

    assert exit_code == 0
    assert "nothing to do" in capsys.readouterr().out


def test_run_entries_live_failure_records_render_gate_error(monkeypatch, tmp_path):
    """Regression test (coloring-book/t-022, 2026-09-14 live incident): the
    exception handler in run_entries() called a nonexistent
    `coloring.record_semantic_gate_error`, so ANY failure during a --live
    studio request (a fresh enqueue error, a timeout, a validation crash)
    raised AttributeError and aborted the whole batch instead of being
    recorded as a retryable failure and moving on to the next proposal id.
    Hit for real requesting fresh renders for mr-001/mr-013/mr-023: mr-001's
    fresh submission failed and the AttributeError killed the run before
    mr-013 or mr-023 were even attempted.
    """
    entry = {
        "id": "mr-001",
        "set": "monster-recast",
        "concept_id": "mr-001",
        "queue_id": "mr-001",
        "image_path": "does/not/exist.webp",
    }

    monkeypatch.setattr(mod.queue_consumer, "KR_API_TOKEN", "fake-token")
    monkeypatch.setattr(mod.coloring, "target_path", lambda e: tmp_path / "missing.webp")
    monkeypatch.setattr(mod.coloring, "referenced_job_id", lambda e: None)
    monkeypatch.setattr(mod.coloring, "enqueue", lambda e: (_ for _ in ()).throw(RuntimeError("boom")))

    calls = []

    def fake_record_render_gate_error(entry, error, job_id=None):
        calls.append((entry["id"], str(error), job_id))

    monkeypatch.setattr(mod.coloring, "record_render_gate_error", fake_record_render_gate_error)
    # Guarantee the old, nonexistent name really is gone -- if the bug ever
    # comes back (the call site reverted to it), this makes the failure loud
    # (AttributeError) instead of quietly matching a stray attribute.
    monkeypatch.delattr(mod.coloring, "record_semantic_gate_error", raising=False)

    exit_code = mod.run_entries([entry], live=True, timeout=30)

    assert exit_code == 1
    assert calls == [("mr-001", "boom", None)]


def test_run_entries_live_recovery_ambiguous_failure_preserves_job_reference(monkeypatch, tmp_path, capsys):
    """Same regression class as above, but for the recovery path: an ambiguous
    failure while checking a previously-stuck job (network error, missing
    local dependency, ...) does NOT positively prove the job is dead -- it may
    still be a perfectly good, completed render. Mirrors
    consume_coloring_book_color_art.py's batch-consumer handling: leave the
    entry's existing render_gate_error (still naming the stuck job) untouched
    rather than overwriting it, so a future pass can still recover it instead
    of losing the reference and submitting a genuine duplicate ArtJob.
    """
    entry = {
        "id": "mr-001",
        "set": "monster-recast",
        "concept_id": "mr-001",
        "queue_id": "mr-001",
        "image_path": "does/not/exist.webp",
    }

    monkeypatch.setattr(mod.queue_consumer, "KR_API_TOKEN", "fake-token")
    monkeypatch.setattr(mod.coloring, "target_path", lambda e: tmp_path / "missing.webp")
    monkeypatch.setattr(mod.coloring, "referenced_job_id", lambda e: 9999)

    def fake_recover(entry, stuck_job_id):
        raise RuntimeError("still broken")

    monkeypatch.setattr(mod.coloring, "recover_timed_out_job", fake_recover)

    calls = []

    def fake_record_render_gate_error(entry, error, job_id=None, drop_reference=False):
        calls.append((entry["id"], str(error), job_id, drop_reference))

    monkeypatch.setattr(mod.coloring, "record_render_gate_error", fake_record_render_gate_error)

    exit_code = mod.run_entries([entry], live=True, timeout=30)

    assert exit_code == 1
    # The ambiguous failure must NOT touch render_gate_error at all -- the
    # existing "job 9999 ..." reference stays exactly as it was.
    assert calls == []
    stderr = capsys.readouterr().err
    assert "RECOVERY UNVERIFIED" in stderr
    assert "job 9999 reference left intact" in stderr


def test_run_entries_live_recovery_abandoned_drops_job_reference(monkeypatch, tmp_path, capsys):
    """The flip side: when recover_timed_out_job() positively determines the
    referenced job failed/was cancelled (RecoveryAbandoned), the reference
    MUST be dropped so the next pass submits a fresh render instead of
    re-checking the same dead job forever. This is the exact bug found live
    running coloring-book/t-022 on 2026-09-14: the render box came back up
    after an outage, but re-requesting mr-001/mr-013/mr-023 just re-confirmed
    their original hostbuf failures (job 22003/22004/22005) instead of firing
    fresh renders, because this call site used to fall through to the generic
    except and preserve the dead job's id via `job_id=job_id`.
    """
    entry = {
        "id": "mr-001",
        "set": "monster-recast",
        "concept_id": "mr-001",
        "queue_id": "mr-001",
        "image_path": "does/not/exist.webp",
    }

    monkeypatch.setattr(mod.queue_consumer, "KR_API_TOKEN", "fake-token")
    monkeypatch.setattr(mod.coloring, "target_path", lambda e: tmp_path / "missing.webp")
    monkeypatch.setattr(mod.coloring, "referenced_job_id", lambda e: 22003)

    def fake_recover(entry, stuck_job_id):
        raise mod.coloring.RecoveryAbandoned(f"job {stuck_job_id} FAILED: hostbuf_file_reader_read failed")

    monkeypatch.setattr(mod.coloring, "recover_timed_out_job", fake_recover)

    calls = []

    def fake_record_render_gate_error(entry, error, job_id=None, drop_reference=False):
        calls.append((entry["id"], str(error), job_id, drop_reference))

    monkeypatch.setattr(mod.coloring, "record_render_gate_error", fake_record_render_gate_error)

    exit_code = mod.run_entries([entry], live=True, timeout=30)

    assert exit_code == 1
    assert calls == [
        ("mr-001", "job 22003 FAILED: hostbuf_file_reader_read failed", None, True)
    ]
    stderr = capsys.readouterr().err
    assert "RECOVERY UNVERIFIED" not in stderr
    assert "FAILED monster-recast/mr-001" in stderr


def test_run_entries_live_gate_rejection_records_render_rejection(monkeypatch, tmp_path, capsys):
    """Regression test (coloring-book/t-022, 2026-09-14 live incident): the
    SEMANTIC-REJECT branch called a nonexistent `coloring.record_semantic_rejection`,
    so ANY mechanical-gate rejection during a --live studio request (e.g. mr-025's
    render failing art_quality.py's color-variant gate) raised AttributeError instead
    of recording the rejection and rotating the queue entry to its next state. Hit for
    real recovering mr-025's job 22165 after fixing its prompt-contract blocker: the
    render was fetched fine, but the rejection bookkeeping crashed before landing any
    reasons or advancing render_attempts, leaving the entry's job reference stranded.
    validate_candidate()/recover_timed_out_job() only ever return the *mechanical* gate
    result here (see consume_coloring_book_color_art.py's own docstring), so the correct
    call is the same `record_render_rejection` the plain batch consumer already uses.
    """
    entry = {
        "id": "mr-025",
        "set": "monster-recast",
        "concept_id": "mr-025",
        "queue_id": "mr-025",
        "image_path": "does/not/exist.webp",
    }

    monkeypatch.setattr(mod.queue_consumer, "KR_API_TOKEN", "fake-token")
    monkeypatch.setattr(mod.coloring, "ROOT", tmp_path)
    monkeypatch.setattr(mod.coloring, "target_path", lambda e: tmp_path / "missing.webp")
    monkeypatch.setattr(mod.coloring, "referenced_job_id", lambda e: 22165)

    gate_result = {"gate": "mechanical", "reasons": ["single-hue tint wash"], "stats": {}}
    monkeypatch.setattr(mod.coloring, "recover_timed_out_job", lambda entry, job_id: (False, gate_result))
    monkeypatch.setattr(
        mod.coloring, "rejection_destination", lambda destination, entry, category: tmp_path / "rejected.webp"
    )

    calls = []

    def fake_record_render_rejection(entry, mechanical, rejected):
        calls.append((entry["id"], mechanical, rejected))
        return "pending"

    monkeypatch.setattr(mod.coloring, "record_render_rejection", fake_record_render_rejection)
    # Guarantee the old, nonexistent name really is gone -- if the bug ever
    # comes back (the call site reverted to it), this makes the failure loud
    # (AttributeError) instead of quietly matching a stray attribute.
    monkeypatch.delattr(mod.coloring, "record_semantic_rejection", raising=False)

    exit_code = mod.run_entries([entry], live=True, timeout=30)

    assert exit_code == 1
    assert calls == [("mr-025", gate_result, tmp_path / "rejected.webp")]
    stderr = capsys.readouterr().err
    assert "SEMANTIC-REJECT monster-recast/mr-025" in stderr
    assert "single-hue tint wash" in stderr
    assert "(pending)" in stderr
