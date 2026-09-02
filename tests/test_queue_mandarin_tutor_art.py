from pathlib import Path
import urllib.error

import yaml

import scripts.queue_mandarin_tutor_art as queue


def manifest_entry(request_id: str = "mandarin-tutor-v2-abc123") -> dict:
    return {
        "requestId": request_id,
        "imagePath": "public/images/mandarin-tutor/cards/v2/abc123.webp",
        "imageUrl": "/images/mandarin-tutor/cards/v2/abc123.webp",
        "strategy": "illustrate",
        "prompt": "A clear picture-book illustration of a red apple.",
        "artDirectionId": queue.EXPECTED_ART_DIRECTION_ID,
        "simplified": "苹果",
        "pinyin": "píng guǒ",
        "meaning": "apple",
        "engine": "krea2",
        "width": 768,
        "height": 768,
    }


def manifest(*entries: dict) -> dict:
    return {
        "recipeVersion": queue.EXPECTED_RECIPE_VERSION,
        "artDirection": {"id": queue.EXPECTED_ART_DIRECTION_ID},
        "entries": list(entries),
    }


def read_requests(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("requests") or []


class HeadResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_probe_media_state_reads_a_2xx_as_present(monkeypatch):
    monkeypatch.setattr(queue.urllib.request, "urlopen", lambda request, timeout: HeadResponse())
    assert queue.probe_media_state(manifest_entry()) == "present"


def test_probe_media_state_reads_a_404_as_absent(monkeypatch):
    def missing(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 404, "not found", None, None)

    monkeypatch.setattr(queue.urllib.request, "urlopen", missing)
    assert queue.probe_media_state(manifest_entry()) == "absent"


def test_probe_media_state_treats_network_failure_as_unknown(monkeypatch):
    def unavailable(request, timeout):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(queue.urllib.request, "urlopen", unavailable)
    assert queue.probe_media_state(manifest_entry()) == "unknown"


def test_rendered_entry_without_a_yaml_row_is_not_restaged(tmp_path, monkeypatch):
    art_prompts = tmp_path / "art-prompts.yaml"
    art_prompts.write_text("requests:\n", encoding="utf-8")
    monkeypatch.setattr(queue, "ART_PROMPTS", art_prompts)

    summary = queue.queue_batch(
        manifest(manifest_entry()),
        1000,
        probe=lambda entry: "present",
        workers=1,
    )

    assert summary["already_staged"] == 0
    assert summary["already_rendered"] == 1
    assert summary["missing"] == 0
    assert summary["queued"] == 0
    assert read_requests(art_prompts) == []


def test_authoritative_missing_entry_is_staged(tmp_path, monkeypatch):
    art_prompts = tmp_path / "art-prompts.yaml"
    art_prompts.write_text("requests:\n", encoding="utf-8")
    monkeypatch.setattr(queue, "ART_PROMPTS", art_prompts)

    summary = queue.queue_batch(
        manifest(manifest_entry()),
        1000,
        probe=lambda entry: "absent",
        workers=1,
    )

    assert summary["missing"] == 1
    assert summary["queued"] == 1
    assert read_requests(art_prompts)[0]["id"] == "mandarin-tutor-v2-abc123"


def test_unknown_media_state_fails_closed_without_restaging(tmp_path, monkeypatch):
    art_prompts = tmp_path / "art-prompts.yaml"
    art_prompts.write_text("requests:\n", encoding="utf-8")
    monkeypatch.setattr(queue, "ART_PROMPTS", art_prompts)

    summary = queue.queue_batch(
        manifest(manifest_entry()),
        1000,
        probe=lambda entry: "unknown",
        workers=1,
    )

    assert summary["probe_unknown"] == 1
    assert summary["missing"] == 0
    assert summary["queued"] == 0
    assert read_requests(art_prompts) == []


def test_existing_request_row_skips_live_probe(tmp_path, monkeypatch):
    art_prompts = tmp_path / "art-prompts.yaml"
    art_prompts.write_text(
        "requests:\n"
        "- id: mandarin-tutor-v2-abc123\n"
        "  image_path: public/images/mandarin-tutor/cards/v2/abc123.webp\n"
        "  status: done\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(queue, "ART_PROMPTS", art_prompts)

    def unexpected_probe(entry):
        raise AssertionError("an existing request row must not be probed")

    summary = queue.queue_batch(
        manifest(manifest_entry()),
        1000,
        probe=unexpected_probe,
        workers=1,
    )

    assert summary["already_staged"] == 1
    assert summary["queued"] == 0
