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
            "engine": "flux",
        }
    )
    # Flux is emitted as a COMFY job carrying the full workflow graph
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


def test_entry_to_job_untargeted_lands_in_default_engine_folder():
    # An untargeted entry (no project, no engine) falls back to the default
    # engine's model-family folder -- krea2 since it became the default.
    job = consumer.entry_to_job(
        {"image_path": "public/images/x.webp", "prompt": "a fox"}
    )
    assert job["engine"] == "COMFY"
    assert job["payload"]["collection"] == "krea2"
    assert job["payload"]["collection"] == consumer.DEFAULT_ENGINE
    assert "workflow" in job["payload"]


def test_entry_to_job_legacy_a1111_override_migrates_to_comfy():
    job = consumer.entry_to_job(
        {
            "project": "alpha",
            "image_path": "projects/images/alpha-hero.webp",
            "size": "1024x1024",
            "prompt": "a hero shot",
            "engine": "a1111",
        }
    )
    assert job["engine"] == "COMFY"
    assert job["payload"]["collection"] == "alpha"
    assert job["payload"]["steps"] == consumer.KREA2_STEPS
    assert job["payload"]["workflow"]["1"]["inputs"]["unet_name"] == consumer.KREA2_MODEL
    assert consumer.normalize_engine("a1111") == consumer.DEFAULT_ENGINE


def test_legacy_comfy_and_sdxl_labels_migrate_to_krea2():
    assert consumer.normalize_engine("comfy") == consumer.DEFAULT_ENGINE
    assert consumer.normalize_engine("sdxl") == consumer.DEFAULT_ENGINE


def test_unknown_conductor_engine_is_rejected():
    import pytest

    with pytest.raises(ValueError, match="unsupported Conductor art engine"):
        consumer.entry_to_job(
            {"image_path": "public/images/x.webp", "prompt": "a fox", "engine": "mystery"}
        )


def test_entry_to_job_flux_schnell_variant():
    job = consumer.entry_to_job(
        {
            "image_path": "public/images/x.webp",
            "prompt": "quick sketch",
            "engine": "flux",
            "flux_variant": "schnell",
        }
    )
    assert job["payload"]["steps"] == 8
    assert (
        job["payload"]["workflow"]["24"]["inputs"]["unet_name"]
        == "flux1-schnell-Q8_0.gguf"
    )


def test_entry_to_job_krea2_builds_qwen_lineage_graph():
    job = consumer.entry_to_job(
        {
            "image_path": "public/images/x.webp",
            "prompt": "a haunted doll, inked comic style",
            "engine": "krea2",
        }
    )
    assert job["engine"] == "COMFY"
    wf = job["payload"]["workflow"]
    # Krea 2 stack: single CLIPLoader (type krea2), Qwen VAE, plain KSampler
    assert wf["2"]["class_type"] == "CLIPLoader"
    assert wf["2"]["inputs"]["type"] == consumer.KREA2_CLIP_TYPE
    assert wf["5"]["inputs"]["vae_name"] == consumer.KREA2_VAE
    assert wf["7"]["class_type"] == "KSampler"
    # native 8-step cadence applied when the entry names no steps
    assert job["payload"]["steps"] == consumer.KREA2_STEPS
    assert wf["7"]["inputs"]["steps"] == consumer.KREA2_STEPS
    # negative is wired to its OWN encode node (not the positive), unlike the
    # broken flux path — live wherever cfg > 1, inert (not mis-wired) at cfg 1
    assert wf["7"]["inputs"]["negative"] == ["4", 0]
    assert wf["7"]["inputs"]["positive"] == ["3", 0]
    # a concrete seed is resolved and reported so the caller can record it
    assert isinstance(job["resolvedSeed"], int)
    assert wf["7"]["inputs"]["seed"] == job["resolvedSeed"]


def test_entry_to_job_flux2_klein_alias_and_json_prompt():
    job = consumer.entry_to_job(
        {
            "image_path": "public/images/x.webp",
            "prompt": "fallback text",
            "engine": "flux2",  # alias -> flux2-klein
            "json_prompt": {"subject": "curvy pinup", "head": "giant fly"},
        }
    )
    assert job["engine"] == "COMFY"
    wf = job["payload"]["workflow"]
    assert wf["1"]["inputs"]["unet_name"] == consumer.FLUX2_KLEIN_MODEL
    assert wf["2"]["inputs"]["type"] == consumer.FLUX2_KLEIN_CLIP_TYPE
    assert job["payload"]["steps"] == consumer.FLUX2_KLEIN_STEPS
    # JSON structured prompt is serialized into the positive text encode
    encoded = wf["3"]["inputs"]["text"]
    assert '"head": "giant fly"' in encoded


def test_entry_to_job_style_lora_wraps_model_only():
    job = consumer.entry_to_job(
        {
            "image_path": "public/images/x.webp",
            "prompt": "inked slasher at the lake",
            "engine": "krea2",
            "lora": "comic_inks_v2.safetensors",
            "lora_strength": 0.8,
        }
    )
    wf = job["payload"]["workflow"]
    assert wf["10"]["class_type"] == "LoraLoaderModelOnly"
    assert wf["10"]["inputs"]["lora_name"] == "comic_inks_v2.safetensors"
    assert wf["10"]["inputs"]["strength_model"] == 0.8
    # sampler now pulls the model through the LoRA, clip stays on the encoder
    assert wf["7"]["inputs"]["model"] == ["10", 0]


def test_entry_to_job_random_seed_when_unset_is_reported():
    job = consumer.entry_to_job(
        {"image_path": "public/images/x.webp", "prompt": "a fox", "engine": "krea2"}
    )
    # no seed on the entry -> a concrete random seed is resolved and reported,
    # and it is NOT surfaced as a fixed payload["seed"] (relay/graph own it)
    assert isinstance(job["resolvedSeed"], int)
    assert job["resolvedSeed"] >= 0
    # ArtImage.seed is a MySQL signed INT (prisma/schema.prisma) -- a resolved
    # seed outside this range fails the save with "Out of range value for
    # column 'seed'" after the render already completed (18 consecutive
    # coloring-book ArtJobs, ids 2146-2184, 2026-07-26).
    assert job["resolvedSeed"] <= consumer.SEED_MAX
    assert "seed" not in job["payload"]


def test_resolve_seed_clamps_out_of_range_and_random_values():
    assert consumer.resolve_seed(None) <= consumer.SEED_MAX
    assert consumer.resolve_seed(-1) <= consumer.SEED_MAX
    assert consumer.resolve_seed(5) == 5
    assert consumer.resolve_seed(consumer.SEED_MAX + 1_000_000_000_000) == consumer.SEED_MAX


def test_entry_to_job_honors_per_entry_quality_overrides():
    # "comfy" aliases to krea2, so steps/cfg are held to what that engine is
    # distilled for (12 / 1). This case used to assert steps 45 / cfg 5 passed
    # through verbatim — the server rejects both, which is how 35 jobs ended up
    # queued at 20 steps and failing at claim. Every other knob is untouched.
    job = consumer.entry_to_job(
        {
            "project": "alpha",
            "image_path": "projects/images/alpha-hero.webp",
            "size": "1280x720",
            "prompt": "a hero shot",
            "engine": "comfy",
            "steps": 10,
            "cfg": 1,
            "sampler": "DPM++ 2M Karras",
            "seed": 12345,
            "negative_prompt": "text, blur",
        }
    )
    assert job["engine"] == "COMFY"
    assert job["payload"]["steps"] == 10
    assert job["payload"]["cfg"] == 1
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


def test_staged_filename_disambiguates_shared_basename_via_project_slug():
    # Every kind_robots hero request uses the identical basename "hero.webp"
    # with the slug living only in the parent directory -- staged_filename
    # must fold project_slug/variant into the name so two projects' renders
    # never collide in projects/process/ (conductor TALKBACK 2026-07-29:
    # voice-lab's and humboldt-scoop's first hero renders were lost this way).
    a = {
        "image_path": "public/images/projects/ruler-hooked/hero.webp",
        "project_slug": "ruler-hooked",
        "variant": "hero",
    }
    b = {
        "image_path": "public/images/projects/newsfeed/hero.webp",
        "project_slug": "newsfeed",
        "variant": "hero",
    }
    name_a = consumer.staged_filename(a)
    name_b = consumer.staged_filename(b)
    assert name_a != name_b
    assert name_a == "ruler-hooked-hero.webp"
    assert name_b == "newsfeed-hero.webp"


def test_staged_filename_noop_without_project_metadata():
    # No project_slug/variant on the entry (or a basename that already
    # encodes the slug) -- behave exactly like the old Path(image_path).name.
    assert (
        consumer.staged_filename({"image_path": "projects/images/alpha-icon.webp"})
        == "alpha-icon.webp"
    )
    assert (
        consumer.staged_filename(
            {
                "image_path": "projects/images/coat-dance-hero.webp",
                "project_slug": "coat-dance",
                "variant": "hero",
            }
        )
        == "coat-dance-hero.webp"
    )


def test_save_result_uses_staged_filename_for_collision_prone_entries(tmp_path, monkeypatch):
    # Pillow's webp encoder needs real image bytes; sidestep that by simulating
    # Pillow being unavailable (same trick as test_save_result_falls_back_to_png_without_pillow)
    # -- this test is about the staging filename, not image encoding.
    import builtins

    real_import = builtins.__import__

    def no_pil(name, *args, **kwargs):
        if name == "PIL" or name.startswith("PIL."):
            raise ImportError("no PIL in this test")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_pil)
    monkeypatch.setattr(consumer, "PROCESS_DIR", tmp_path / "process")
    entry_a = {
        "image_path": "public/images/projects/ruler-hooked/hero.webp",
        "project_slug": "ruler-hooked",
        "variant": "hero",
    }
    entry_b = {
        "image_path": "public/images/projects/newsfeed/hero.webp",
        "project_slug": "newsfeed",
        "variant": "hero",
    }
    payload = base64.b64encode(b"fake-png-bytes").decode()
    out_a, _ = consumer.save_result(entry_a, payload)
    out_b, _ = consumer.save_result(entry_b, payload)
    assert out_a != out_b
    assert out_a.name == "ruler-hooked-hero.png"
    assert out_b.name == "newsfeed-hero.png"
    assert out_a.exists() and out_b.exists()


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


def test_explicit_steps_are_clamped_to_the_engine_ceiling():
    """A stale `steps: 20` in a queue entry must not reach the server.

    kind_robots rejects krea2 above 12 steps (artPromptContract.ts). Resolving
    per-engine DEFAULTS was not enough on its own: an explicit `steps:` used to
    override the default untouched, and 35 krea2 jobs reached the queue at 20
    steps that way — 8 died at claim on 2026-08-09, 27 more were queued behind
    them. Clamp the caller's number too, in the payload AND in the graph the
    sampler actually executes.
    """
    job = consumer.entry_to_job(
        {
            "project": "coat-dance",
            "prompt": "a coat dancing",
            "engine": "krea2",
            "steps": 20,
            "cfg": 7,
        }
    )
    ceiling = consumer.ENGINE_MAX_STEPS["krea2"]
    assert job["payload"]["steps"] == ceiling
    assert job["payload"]["cfg"] == consumer.ENGINE_MAX_CFG["krea2"]
    sampler = next(
        node
        for node in job["payload"]["workflow"].values()
        if node.get("class_type") == "KSampler"
    )
    assert sampler["inputs"]["steps"] == ceiling


def test_explicit_steps_below_the_ceiling_are_respected():
    """The clamp is a ceiling, not a rewrite — a deliberate low budget stands."""
    job = consumer.entry_to_job(
        {
            "project": "coat-dance",
            "prompt": "a coat dancing",
            "engine": "krea2",
            "steps": 6,
        }
    )
    assert job["payload"]["steps"] == 6


def test_flux_cfg_metadata_matches_the_graph():
    """Flux steers with FluxGuidance and samples at cfg 1.

    The payload's top-level cfg used to read DEFAULT_CFG (7), describing a job
    that was never going to run that way — and kind_robots' contract falls back
    to that field when a graph has no KSampler.
    """
    job = consumer.entry_to_job(
        {"project": "coat-dance", "prompt": "a coat dancing", "engine": "flux"}
    )
    assert job["payload"]["cfg"] == 1
    assert job["payload"]["workflow"]["52"]["inputs"]["cfg"] == 1
