import base64
from pathlib import Path

import scripts.consume_art_queue as consumer


def test_parse_size():
    assert consumer.parse_size("1280x720") == (1280, 720)
    assert consumer.parse_size("512X512") == (512, 512)
    assert consumer.parse_size(None) == (512, 512)
    assert consumer.parse_size("garbage") == (512, 512)


def test_entry_to_job_maps_fields():
    job = consumer.entry_to_job(
        {
            "project": "coat-dance",
            "variant": "hero",
            "image_path": "projects/images/coat-dance-hero.webp",
            "size": "1280x720",
            "prompt": "  a   coat   dancing  ",
        }
    )
    assert job["engine"] == "A1111"
    assert job["projectSlug"] == "coat-dance"
    assert job["payload"]["promptString"] == "a coat dancing"
    assert job["payload"]["width"] == 1280
    assert job["payload"]["height"] == 720
    assert job["payload"]["collection"] == "coat-dance"


def test_load_entries_skips_malformed(tmp_path, monkeypatch):
    art_file = tmp_path / "art-generate.yaml"
    art_file.write_text(
        """
batch:
  entries:
    - image_path: projects/images/alpha-icon.webp
      prompt: alpha icon
    - image_path: projects/images/broken-no-prompt.webp
    - not-a-dict
"""
    )
    monkeypatch.setattr(consumer, "ART_GENERATE_FILE", art_file)
    entries = consumer.load_entries()
    assert len(entries) == 1
    assert entries[0]["image_path"] == "projects/images/alpha-icon.webp"


def test_save_result_falls_back_to_png_without_pillow(tmp_path, monkeypatch):
    monkeypatch.setattr(consumer, "PROCESS_DIR", tmp_path / "process")
    # simulate Pillow being unavailable regardless of the environment
    import builtins

    real_import = builtins.__import__

    def no_pil(name, *args, **kwargs):
        if name == "PIL" or name.startswith("PIL."):
            raise ImportError("no PIL in this test")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_pil)

    entry = {"image_path": "projects/images/alpha-icon.webp"}
    payload = base64.b64encode(b"fake-png-bytes").decode()
    out, warning = consumer.save_result(entry, payload)

    assert out.name == "alpha-icon.png"
    assert out.read_bytes() == b"fake-png-bytes"
    assert warning and "Pillow" in warning


def test_save_result_non_webp_passthrough(tmp_path, monkeypatch):
    monkeypatch.setattr(consumer, "PROCESS_DIR", tmp_path / "process")
    entry = {"image_path": "public/images/comfy/comfy-test.png"}
    payload = base64.b64encode(b"png").decode()
    out, warning = consumer.save_result(entry, payload)
    assert out.name == "comfy-test.png"
    assert warning is None


def test_dry_run_makes_no_network_calls(tmp_path, monkeypatch, capsys):
    art_file = tmp_path / "art-generate.yaml"
    art_file.write_text(
        """
batch:
  entries:
    - image_path: projects/images/alpha-icon.webp
      prompt: alpha icon
      size: 512x512
      project: alpha
"""
    )
    monkeypatch.setattr(consumer, "ART_GENERATE_FILE", art_file)

    def boom(*args, **kwargs):
        raise AssertionError("network touched during dry run")

    monkeypatch.setattr(consumer, "http_json", boom)
    monkeypatch.setattr("sys.argv", ["consume_art_queue.py"])

    assert consumer.main() == 0
    out = capsys.readouterr().out
    assert "would queue projects/images/alpha-icon.webp" in out
    assert "DRY RUN" in out
