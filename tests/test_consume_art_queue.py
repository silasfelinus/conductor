import base64
from pathlib import Path

import scripts.consume_art_queue as consumer


def test_parse_size():
    assert consumer.parse_size("1280x720") == (1280, 720)
    assert consumer.parse_size("512X512") == (512, 512)
    assert consumer.parse_size(None) == (1024, 1024)
    assert consumer.parse_size("garbage") == (1024, 1024)


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
    # default engine is Flux, emitted as a COMFY job carrying the workflow graph
    assert job["engine"] == "COMFY"
    assert job["projectSlug"] == "coat-dance"
    assert job["payload"]["promptString"] == "a coat dancing"
    assert job["payload"]["width"] == 1280
    assert job["payload"]["height"] == 720
    assert job["payload"]["collection"] == "coat-dance"
    # quality defaults applied when the entry says nothing
    assert job["payload"]["steps"] == consumer.FLUX_MODELS["dev"]["steps"]
    assert job["payload"]["negativePrompt"] == consumer.DEFAULT_NEGATIVE_PROMPT
    # optional knobs stay off so the relay's own defaults apply
    assert "sampler" not in job["payload"]
    assert "seed" not in job["payload"]
    # the Flux graph is present and carries the quality settings
    wf = job["payload"]["workflow"]
    assert wf["6"]["inputs"]["width"] == 1280
    assert wf["52"]["inputs"]["scheduler"] == "beta"
    assert wf["52"]["inputs"]["cfg"] == 1
    assert wf["46"]["inputs"]["guidance"] == 3.5
    assert wf["24"]["inputs"]["unet_name"] == "flux1-dev-Q8_0.gguf"


def test_entry_to_job_flux_untargeted_lands_in_flux_folder():
    job = consumer.entry_to_job(
        {"image_path": "public/images/x.webp", "prompt": "a fox"}
    )
    assert job["engine"] == "COMFY"
    assert job["payload"]["collection"] == "flux"
    assert "workflow" in job["payload"]


def test_entry_to_job_a1111_override_emits_raw_keys():
    job = consumer.entry_to_job(
        {
            "project": "alpha",
            "image_path": "projects/images/alpha-hero.webp",
            "size": "1024x1024",
            "prompt": "a hero shot",
            "engine": "a1111",
        }
    )
    assert job["engine"] == "A1111"
    # A1111 path stays txt2img — no ComfyUI workflow graph
    assert "workflow" not in job["payload"]
    assert job["payload"]["steps"] == consumer.DEFAULT_STEPS
    assert job["payload"]["cfg"] == consumer.DEFAULT_CFG


def test_entry_to_job_flux_schnell_variant():
    job = consumer.entry_to_job(
        {
            "image_path": "public/images/x.webp",
            "prompt": "quick sketch",
            "flux_variant": "schnell",
        }
    )
    assert job["payload"]["steps"] == 8
    assert (
        job["payload"]["workflow"]["24"]["inputs"]["unet_name"]
        == "flux1-schnell-Q8_0.gguf"
    )


def test_entry_to_job_honors_per_entry_quality_overrides():
    job = consumer.entry_to_job(
        {
            "project": "alpha",
            "image_path": "projects/images/alpha-hero.webp",
            "size": "1280x720",
            "prompt": "a hero shot",
            "engine": "comfy",
            "steps": 45,
            "cfg": 5,
            "sampler": "DPM++ 2M Karras",
            "seed": 12345,
            "negative_prompt": "text, blur",
        }
    )
    assert job["engine"] == "COMFY"
    assert job["payload"]["steps"] == 45
    assert job["payload"]["cfg"] == 5
    assert job["payload"]["sampler"] == "DPM++ 2M Karras"
    assert job["payload"]["seed"] == 12345
    assert job["payload"]["negativePrompt"] == "text, blur"


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


def test_load_entries_reads_legacy_images_shape(tmp_path, monkeypatch):
    # A batch written by an older queue_missing_project_art.py used a
    # top-level images: list instead of batch.entries. The consumer must
    # still read it (the file may already be on disk).
    art_file = tmp_path / "art-generate.yaml"
    art_file.write_text(
        """
generated_by: scripts/queue_missing_project_art.py
mode: dry-run
images:
  - image_path: projects/images/alpha-icon.webp
    prompt: alpha icon
    size: 256x256
    project: alpha
"""
    )
    monkeypatch.setattr(consumer, "ART_GENERATE_FILE", art_file)
    entries = consumer.load_entries()
    assert len(entries) == 1
    assert entries[0]["project"] == "alpha"


def test_builder_output_is_consumable(tmp_path, monkeypatch):
    # End-to-end shape contract: what queue_missing_project_art.write_queue
    # emits must be exactly what consume_art_queue.load_entries reads.
    import scripts.queue_missing_project_art as builder

    entries = [
        {
            "project": "alpha",
            "variant": "icon",
            "target_repo": "silasfelinus/conductor",
            "image_path": "projects/images/alpha-icon.webp",
            "size": "256x256",
            "status": "pending",
            "prompt": "bright alpha icon",
        }
    ]
    art_file = tmp_path / "art-generate.yaml"
    builder.write_queue(entries, art_file)

    monkeypatch.setattr(consumer, "ART_GENERATE_FILE", art_file)
    loaded = consumer.load_entries()
    assert len(loaded) == 1
    job = consumer.entry_to_job(loaded[0])
    assert job["payload"]["width"] == 256
    assert job["projectSlug"] == "alpha"


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
