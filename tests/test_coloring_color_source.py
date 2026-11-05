"""generate-color-proposals color_source: render from the prompt, or color a chosen file."""

import yaml

from scripts import consume_coloring_book_studio_request as mod
from scripts import process_coloring_art_events as events


def write_set(tmp_path, monkeypatch):
    for rel in ("generated/bw/mr-001-bw.webp", "approved/mr-001-color.webp"):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"RIFF....WEBP")
    monkeypatch.setattr(mod.production, "set_dir", lambda _book: tmp_path)


def test_bw_source_gets_the_colorize_prompt_with_a_scene_hint(tmp_path, monkeypatch):
    write_set(tmp_path, monkeypatch)
    source_rel, data_url = mod.image_source(
        "monster-recast",
        "projects/coloring-book/sets/monster-recast/generated/bw/mr-001-bw.webp",
    )
    entry = {"scene_prompt": "A mummy hosts a beach volleyball game. " * 40}
    mod.attach_image_source(entry, source_rel, data_url)

    assert entry["color_source_path"] == "generated/bw/mr-001-bw.webp"
    assert entry["source_image_data_url"].startswith("data:image/webp;base64,")
    assert entry["image_prompt"].startswith(mod.COLORIZE_PROMPT)
    assert "The scene: A mummy hosts" in entry["image_prompt"]
    assert len(entry["image_prompt"]) <= len(mod.COLORIZE_PROMPT) + 12 + mod.SCENE_HINT_CHARS


def test_color_source_gets_the_recolor_prompt(tmp_path, monkeypatch):
    write_set(tmp_path, monkeypatch)
    entry = {"scene_prompt": ""}
    mod.attach_image_source(entry, *mod.image_source("monster-recast", "approved/mr-001-color.webp"))
    assert entry["image_prompt"] == mod.RECOLOR_PROMPT


def test_missing_source_is_refused(tmp_path, monkeypatch):
    write_set(tmp_path, monkeypatch)
    try:
        mod.image_source("monster-recast", "approved/nope.webp")
    except RuntimeError as error:
        assert "does not exist" in str(error)
    else:
        raise AssertionError("missing source accepted")


def test_run_entries_sends_an_image_source_to_kontext(monkeypatch, tmp_path):
    entry = {
        "id": "mr-001",
        "set": "monster-recast",
        "concept_id": "mr-001",
        "queue_id": "mr-001",
        "image_path": "x.webp",
        "color_source_path": "generated/bw/mr-001-bw.webp",
        "source_image_data_url": "data:image/webp;base64,AAAA",
        "image_prompt": "Color it.",
    }
    posted = []

    def fake_http_json(method, url, body=None):
        posted.append((method, url, body))
        return 201, {"success": True, "data": {"jobId": 77}}

    monkeypatch.setattr(mod.coloring, "ROOT", tmp_path)
    monkeypatch.setattr(mod.queue_consumer, "KR_API_TOKEN", "fake-token")
    monkeypatch.setattr(mod.queue_consumer, "http_json", fake_http_json)
    monkeypatch.setattr(mod.queue_consumer, "wait_for_job", lambda job_id, timeout: {"artImageId": 9})
    monkeypatch.setattr(mod.queue_consumer, "fetch_image_b64", lambda image_id: "AAAA")
    monkeypatch.setattr(mod.coloring, "target_path", lambda e: tmp_path / "missing.webp")
    monkeypatch.setattr(mod.coloring, "referenced_job_id", lambda e: None)
    monkeypatch.setattr(mod.coloring, "enqueue", lambda e: (_ for _ in ()).throw(AssertionError("text path used")))
    monkeypatch.setattr(mod.coloring, "save_result", lambda e, b64: tmp_path / "landed.webp")
    monkeypatch.setattr(mod.coloring, "validate_candidate", lambda e, d: (True, {"score": None}))
    done = []
    monkeypatch.setattr(mod.coloring, "mark_done", lambda completed: done.extend(completed) or len(completed))

    assert mod.run_entries([entry], live=True, timeout=30) == 0
    (_method, url, body), = posted
    assert url.endswith("/api/art/enqueue")
    assert body["engine"] == "kontext"
    assert body["promptString"] == "Color it."
    assert body["sourceImageBase64"] == "data:image/webp;base64,AAAA"
    assert done[0]["engine"] == "kontext"
    assert done[0]["art_image_id"] == 9


def test_mark_done_records_and_clears_the_color_source(tmp_path, monkeypatch):
    queue_file = tmp_path / "color-art-jobs.yaml"
    queue_file.write_text(
        yaml.safe_dump(
            {"books": [{"slug": "monster-recast", "entries": [
                {"id": "mr-001", "status": "pending"},
                {"id": "mr-002", "status": "pending", "color_source": "version", "color_source_path": "old.webp"},
            ]}]}
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod.coloring, "QUEUE_FILE", queue_file)
    base = {"set": "monster-recast", "image_path": "a.webp", "prompt_fingerprint": "f"}
    mod.coloring.mark_done([
        {**base, "queue_id": "mr-001", "color_source_path": "generated/bw/mr-001-bw.webp"},
        {**base, "queue_id": "mr-002"},
    ])
    entries = {e["id"]: e for e in yaml.safe_load(queue_file.read_text())["books"][0]["entries"]}
    assert entries["mr-001"]["color_source"] == "version"
    assert entries["mr-001"]["color_source_path"] == "generated/bw/mr-001-bw.webp"
    assert "color_source" not in entries["mr-002"]
    assert "color_source_path" not in entries["mr-002"]


def test_main_rejects_inconsistent_source_flags(monkeypatch, capsys):
    import pytest

    for extra in (
        ["--color-source", "version"],
        ["--source-path", "approved/a.webp"],
        ["--color-source", "version", "--source-path", "a.webp", "--proposal-id", "mr-002"],
    ):
        monkeypatch.setattr(
            "sys.argv",
            ["x", "--book", "monster-recast", "--proposal-id", "mr-001", *extra],
        )
        with pytest.raises(SystemExit):
            mod.main()


def write_event(tmp_path, **overrides):
    payload = {
        "version": 1,
        "operation": "generate-color-proposals",
        "book": "monster-recast",
        "proposal_ids": ["mr-009"],
        "timeout": 600,
        "force": True,
    }
    payload.update(overrides)
    path = tmp_path / "event.yaml"
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")
    return path


def test_version_event_routes_to_the_studio_consumer_with_the_file(tmp_path):
    event = events.load_event(
        write_event(tmp_path, color_source="version", source_path="generated/bw/mr-009-bw.webp")
    )
    command = event.command(live=False)
    assert "consume_coloring_book_studio_request.py" in command[1]
    assert command[command.index("--color-source") + 1] == "version"
    assert command[command.index("--source-path") + 1] == "generated/bw/mr-009-bw.webp"
    assert "--force" in command


def test_events_without_color_source_keep_the_old_command(tmp_path):
    command = events.load_event(write_event(tmp_path)).command(live=False)
    assert "--color-source" not in command
    assert "--source-path" not in command


def test_invalid_color_source_events_are_refused(tmp_path):
    import pytest

    cases = [
        ({"color_source": "version"}, "requires a source_path"),
        ({"color_source": "sketch"}, "color_source must be one of"),
        ({"source_path": "approved/a.webp"}, "supported only"),
        ({"operation": "generate-bw", "color_source": "prompt"}, "only for generate-color-proposals"),
        ({"color_source": "version", "source_path": "a.webp", "proposal_ids": ["mr-009", "mr-010"]}, "exactly one proposal"),
    ]
    for overrides, message in cases:
        with pytest.raises(ValueError, match=message):
            events.load_event(write_event(tmp_path, **overrides))
