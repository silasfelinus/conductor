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

    already_resolved = mod.prepare_requested_entries(
        "monster-recast", ["mr-001", "mr-009", "mr-016"], force=False
    )

    assert already_resolved == [("mr-009", "done"), ("mr-016", "done")]
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

    already_resolved = mod.prepare_requested_entries(
        "monster-recast", ["mr-009", "mr-016"], force=False
    )

    assert set(already_resolved) == {("mr-009", "done"), ("mr-016", "approved")}


def test_prepare_requested_entries_force_still_resets_non_pending_entries(tmp_path, monkeypatch):
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

    already_resolved = mod.prepare_requested_entries("monster-recast", ["mr-009"], force=True)

    assert already_resolved == []
    reloaded_file = mod.coloring.QUEUE_FILE
    reloaded = yaml.safe_load(reloaded_file.read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in reloaded["books"][0]["entries"]}
    assert by_id["mr-009"]["status"] == "pending"
    assert "art_image_id" not in by_id["mr-009"]


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
