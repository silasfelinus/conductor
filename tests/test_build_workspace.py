from pathlib import Path

import scripts.build_workspace as bw


def test_kind_robots_done_request_stays_pending_while_file_is_staged(tmp_path, monkeypatch):
    """A kind_robots-target request marked status: done is only "complete"
    once its locally staged render is gone -- "done" means generation
    succeeded, not that the home relay actually delivered it (see
    ai-art-academy/t-010, 2026-07-29: the fauvism style-preview request was
    pruned the moment status flipped to done while the render was still
    sitting undelivered in projects/process/, and the file was later swept
    into projects/process/unmatched/ with no yaml entry left to re-match).
    """
    process_dir = tmp_path / "process"
    process_dir.mkdir()
    monkeypatch.setattr(bw, "PROCESS_DIR", process_dir)

    request = {
        "id": "kind-robots-academy-style-preview-fauvism",
        "status": "done",
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/academy/styles/fauvism.webp",
    }

    (process_dir / "fauvism.webp").write_bytes(b"x")
    assert bw.request_is_complete(request) is False

    (process_dir / "fauvism.webp").unlink()
    assert bw.request_is_complete(request) is True


def test_kind_robots_done_request_with_slug_variant_staged_name(tmp_path, monkeypatch):
    """staged_filename() prefixes the slug for project_slug/variant entries
    (see consume_art_queue_core.staged_filename) -- request_is_complete must
    derive the same key or it will always see the file as "gone"."""
    process_dir = tmp_path / "process"
    process_dir.mkdir()
    monkeypatch.setattr(bw, "PROCESS_DIR", process_dir)

    request = {
        "id": "kind-robots-newsfeed-hero",
        "status": "done",
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/projects/newsfeed/hero.webp",
        "project_slug": "newsfeed",
        "variant": "hero",
    }

    (process_dir / "newsfeed-hero.webp").write_bytes(b"x")
    assert bw.request_is_complete(request) is False


def test_non_kind_robots_done_request_still_completes_immediately():
    """Unaffected by this fix: conductor-target (and other) requests never
    go through the RETAIN-in-process/ flow, so status: done stays sufficient."""
    request = {
        "id": "conductor-davinci-card",
        "status": "done",
        "target_repo": "silasfelinus/conductor",
        "image_path": "projects/images/davinci-card.webp",
    }
    assert bw.request_is_complete(request) is True


def test_pending_kind_robots_request_is_not_complete():
    request = {
        "id": "kind-robots-fox-image",
        "status": "pending",
        "target_repo": "silasfelinus/kind_robots",
        "image_path": "public/images/serendipity/a-fox.webp",
    }
    assert bw.request_is_complete(request) is False
