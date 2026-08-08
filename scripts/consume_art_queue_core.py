#!/usr/bin/env python3
"""
consume_art_queue.py — submit approved art-generate.yaml entries to the
kind_robots ArtJob queue and land the results in projects/process/.

Closes the autonomous art loop (art-generator-connect t-012):

  projects/art-generate.yaml (approved batch)
    -> POST {KR}/api/art/queue          (one job per entry)
    -> poll GET {KR}/api/art/queue/{id} (relay renders on the home box)
    -> GET  {KR}/api/art/image/{artImageId}?includeImageData=true
    -> projects/process/{basename}      (distribute_images.py routes from there)
    -> mark the entry status: done in art-generate.yaml (comment-preserving)

Entries self-drain: once an entry has been enqueued as an ArtJob and its render
lands, it is marked status: done and skipped on the next run (failed entries
stay pending for retry). ArtJob is the single source of truth — this script
only turns approved generate entries into jobs and clears them.

Dry-run by default: prints what would be queued and touches nothing. Pass
--live to run for real — Silas has authorized the automatic loop; no separate
per-run approval is required.

Environment:
  KR_API_TOKEN   required for --live (machine auth: user apiKey or admin token)
  KR_BASE_URL    default https://kind-robots.vercel.app

Usage:
  python scripts/consume_art_queue.py                    # dry run
  python scripts/consume_art_queue.py --live             # queue + wait + download
  python scripts/consume_art_queue.py --live --limit 3   # first 3 entries only
  python scripts/consume_art_queue.py --live --no-wait   # enqueue + mark done, don't block

Output files: results are PNG (what the engines emit). If Pillow is
installed they are converted to the .webp filename the entry names;
otherwise they are saved as .png next to that name with a warning, for
manual conversion before distribute_images.py runs.
"""

import argparse
import base64
import json
import os
import random
import re
import sys
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
ART_GENERATE_FILE = ROOT / "projects" / "art-generate.yaml"
PROCESS_DIR = ROOT / "projects" / "process"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

POLL_SECONDS = 5

# Generation quality defaults. Each is overridable per art-generate.yaml entry
# (steps, cfg, sampler, negative_prompt, seed, engine) so a batch can spend
# more on hero key art than on throwaway icons.
#
# Default engine is KREA2 (Krea 2 Turbo) — the fast, VRAM-friendly, extreme-
# creativity path that renders reliably on the home box. A krea2 entry is emitted
# as a COMFY job carrying the full Krea 2 workflow graph below, which the home
# relay's run_comfy drives on ComfyUI. Flux (dev) stays available per-entry
# (`engine: flux`) for anything that genuinely needs it, and Kontext for edits;
# legacy `engine: a1111` entries are migrated to Krea 2 so Conductor never
# creates A1111 work. The shared Kind Robots relay still supports explicitly
# labeled A1111 jobs created by users outside Conductor.
DEFAULT_ENGINE = "krea2"
DEFAULT_STEPS = 30
DEFAULT_CFG = 7

# Flux workflow defaults — mirror kind_robots /api/comfy/flux/generate so the
# queue path renders identically to the interactive endpoint: native 1MP,
# `beta` scheduler, guidance 3.5, GGUF Q8 base. cfg is fixed at 1 (Flux uses
# the guidance embedding, not CFG). Keep these in sync with that endpoint.
FLUX_VARIANT = "dev"
FLUX_SAMPLER = "euler"
FLUX_SCHEDULER = "beta"
FLUX_MODELS = {
    "dev": {"unet": "flux1-dev-Q8_0.gguf", "steps": 30, "guidance": 3.5},
    "schnell": {"unet": "flux1-schnell-Q8_0.gguf", "steps": 8, "guidance": 3.5},
}
# A broad quality/cleanliness negative. The prompts already say "no text, no
# watermark, no collage"; this reinforces that on the sampler side and knocks
# back the usual SD failure modes (bad anatomy, artifacts, borders).
DEFAULT_NEGATIVE_PROMPT = (
    "text, watermark, signature, logo, caption, letters, words, "
    "blurry, low quality, lowres, jpeg artifacts, deformed, disfigured, "
    "extra limbs, bad anatomy, bad hands, cropped, out of frame, "
    "collage, frame, border, ugly, grainy"
)

# ---------------------------------------------------------------------------
# Krea 2 Turbo (default for coloring-book color masters)
# ---------------------------------------------------------------------------
# Krea 2 Turbo is an 8-step distilled DiT tuned for illustration/painting — the
# "extreme creativity" lane the coloring books want, and fast enough to iterate
# on a 12GB card (~sub-minute vs Flux-dev's ~30 min at 36 steps). Its stack is
# Qwen-Image lineage, NOT Flux: a single CLIPLoader with type "krea2" feeding
# the Qwen3-VL text encoder, the Qwen-Image VAE (not Flux's ae.safetensors),
# and a plain KSampler (no FluxGuidance node). Negative conditioning is wired
# correctly but has little effect at cfg 1 (the model is distilled for it).
#
# VERIFY these filenames against your ComfyUI/models folders after download —
# quant/release naming varies. GGUF users: set KREA2_UNET_LOADER to
# "UnetLoaderGGUF" and point KREA2_MODEL at the .gguf (lighter on 12GB VRAM).
KREA2_UNET_LOADER = "UnetLoaderGGUF"  # GGUF quant (lighter on 12GB VRAM)
KREA2_MODEL = "Krea-2-Turbo-Q5_K_S.gguf"  # realrebelai/KREA-2_GGUFs -> models/unet/
KREA2_MODEL_DTYPE = "default"  # UNETLoader weight_dtype; ignored by the GGUF loader
KREA2_CLIP = "qwen3vl_4b_fp8_scaled.safetensors"
KREA2_CLIP_TYPE = "krea2"
KREA2_VAE = "qwen_image_vae.safetensors"
KREA2_STEPS = 8
KREA2_CFG = 1
KREA2_SAMPLER = "euler"
KREA2_SCHEDULER = "simple"

# ---------------------------------------------------------------------------
# Flux.2 Klein 4B (the JSON-structured-prompt option)
# ---------------------------------------------------------------------------
# Klein 4B is Apache-2.0 (clean for storefront/POD), 4-step, <12GB, and takes
# JSON structured prompts that bind compositions ("head": "giant fly", ...) far
# more faithfully than a run-on sentence — the fix for renders that "veer off".
# Pass an entry's `json_prompt:` mapping and it is serialized into the text
# encode; otherwise the plain prompt string is used. Flux.2 uses its OWN text
# encoder and VAE (different from Flux.1).
#
# VERIFY these filenames against the Comfy-Org Flux.2 release you download.
FLUX2_KLEIN_UNET_LOADER = "UnetLoaderGGUF"  # Klein 4B GGUF -> models/unet/
FLUX2_KLEIN_MODEL = "flux-2-klein-4b-Q4_K_M.gguf"
FLUX2_KLEIN_CLIP = "flux2_klein_text_encoder_fp8_scaled.safetensors"
FLUX2_KLEIN_CLIP_TYPE = "flux2"
FLUX2_KLEIN_VAE = "flux2-vae.safetensors"
FLUX2_KLEIN_STEPS = 4
FLUX2_KLEIN_CFG = 1
FLUX2_KLEIN_SAMPLER = "euler"
FLUX2_KLEIN_SCHEDULER = "simple"

# Engine name normalization. Every alias resolves to a canonical engine so a
# queue entry (or a defaults block) can say "krea", "klein", "flux2", etc.
ENGINE_ALIASES = {
    # Conductor is Comfy-only. Preserve old queue/config compatibility by
    # migrating legacy A1111 labels to the default Krea 2 workflow.
    "a1111": "krea2",
    "sd": "krea2",
    "stable-diffusion": "krea2",
    "comfy": "krea2",
    "sdxl": "krea2",
    "krea": "krea2",
    "krea2-turbo": "krea2",
    "krea-2": "krea2",
    "flux2": "flux2-klein",
    "klein": "flux2-klein",
    "flux2-klein-4b": "flux2-klein",
    "flux-2": "flux2-klein",
}

# Engines that emit a full ComfyUI graph (relay engine "COMFY"). Conductor
# normalizes its legacy A1111 labels into this set rather than creating raw
# txt2img jobs.
COMFY_WORKFLOW_ENGINES = ("flux", "krea2", "flux2-klein")

# Per-engine native step counts, used when an entry/defaults block does not
# name an explicit step budget so each model runs at its designed cadence.
ENGINE_DEFAULT_STEPS = {
    "krea2": KREA2_STEPS,
    "flux2-klein": FLUX2_KLEIN_STEPS,
}

# Per-engine guidance. Distilled models are TRAINED at cfg 1 and go out of
# distribution above it: Krea 2 Turbo at DEFAULT_CFG (7) burns contrast, crushes
# colour, and multiplies subjects — the pattern behind the over-cooked,
# face-spammed daily-dream cards on 2026-08-08 (ArtJobs 7953/7954/7961/7966 all
# ran at cfg 7 / 20 steps against krea2's designed 8 / 1). `entry_to_job` used a
# flat DEFAULT_CFG for every engine while resolving steps per-engine, so the
# mismatch only showed up in the rendered image.
ENGINE_DEFAULT_CFG = {
    "krea2": KREA2_CFG,
    "flux2-klein": FLUX2_KLEIN_CFG,
}


def engine_default_cfg(engine):
    """Guidance for `engine`, falling back to the generic SD-style default."""
    return ENGINE_DEFAULT_CFG.get(engine, DEFAULT_CFG)


def normalize_engine(engine):
    name = str(engine or DEFAULT_ENGINE).strip().lower()
    return ENGINE_ALIASES.get(name, name)


def http_json(method, url, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return e.code, payload


def parse_size(size, default=(1024, 1024)):
    """'1280x720' -> (1280, 720); tolerates junk by falling back."""
    m = re.match(r"^\s*(\d+)\s*[xX]\s*(\d+)\s*$", str(size or ""))
    if not m:
        return default
    return int(m.group(1)), int(m.group(2))


SEED_MAX = 2_147_483_647  # MySQL signed INT max; ArtImage.seed is Int in prisma/schema.prisma


def resolve_seed(seed):
    """A concrete, in-range seed. Reuse a caller-supplied non-negative int (clamped
    to fit the ArtImage.seed column, a MySQL signed INT); otherwise pick a random
    one in the same range (matches the KR endpoint's -1 -> random, see randomSeed()
    in kind_robots server/api/art/queue/[id]/edit.post.ts). A prior version picked
    randint(0, 1_000_000_000_000_000) here, far outside INT range -- every render
    using an unset seed landed a value the DB rejected at save time ("Out of range
    value for column 'seed'"), permanently failing the job after retries (18
    consecutive coloring-book ArtJobs, ids 2146-2184, 2026-07-26)."""
    if isinstance(seed, int) and not isinstance(seed, bool) and seed >= 0:
        return min(seed, SEED_MAX)
    return random.randint(0, SEED_MAX)


def build_flux_workflow(prompt, width, height, steps, guidance, seed, unet):
    """Full ComfyUI API-format Flux graph — a Python mirror of buildFluxWorkflow
    in kind_robots server/api/comfy/flux/generate.post.ts. The relay's run_comfy
    POSTs this straight to ComfyUI /prompt. Keep node ids/keys in sync with that
    endpoint so queue art and interactive art render identically."""
    text = prompt or "a beautiful, richly detailed illustration"
    sampler_seed = resolve_seed(seed)
    wildcard_seed = resolve_seed(None)
    return {
        "4": {
            "inputs": {
                "clip_name1": "t5xxl_fp8_e4m3fn_scaled.safetensors",
                "clip_name2": "clip_l.safetensors",
                "type": "flux",
                "device": "default",
            },
            "class_type": "DualCLIPLoader",
            "_meta": {"title": "DualCLIPLoader"},
        },
        "6": {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Empty Latent Image"},
        },
        "7": {
            "inputs": {"samples": ["52", 0], "vae": ["8", 0]},
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"},
        },
        "8": {
            "inputs": {"vae_name": "ae.safetensors"},
            "class_type": "VAELoader",
            "_meta": {"title": "Load VAE"},
        },
        "24": {
            "inputs": {"unet_name": unet},
            "class_type": "UnetLoaderGGUF",
            "_meta": {"title": "Unet Loader (GGUF)"},
        },
        "46": {
            "inputs": {"guidance": guidance, "conditioning": ["59", 2]},
            "class_type": "FluxGuidance",
            "_meta": {"title": "FluxGuidance"},
        },
        "52": {
            "inputs": {
                "seed": sampler_seed,
                "steps": steps,
                "cfg": 1,
                "sampler_name": FLUX_SAMPLER,
                "scheduler": FLUX_SCHEDULER,
                "denoise": 1,
                "model": ["59", 0],
                "positive": ["46", 0],
                "negative": ["46", 0],
                "latent_image": ["6", 0],
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"},
        },
        "57": {
            "inputs": {"filename_prefix": "kindrobots_flux_dev", "images": ["7", 0]},
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"},
        },
        "59": {
            "inputs": {
                "wildcard_text": text,
                "populated_text": text,
                "mode": "populate",
                "Select to add LoRA": "Select the LoRA to add to the text",
                "Select to add Wildcard": "Select the Wildcard to add to the text",
                "seed": wildcard_seed,
                "model": ["24", 0],
                "clip": ["4", 0],
            },
            "class_type": "ImpactWildcardEncode",
            "_meta": {"title": "ImpactWildcardEncode"},
        },
    }


def _lora_from_entry(entry):
    """Optional style-LoRA hook shared by the Comfy engines. Returns
    (lora_name, strength) or (None, _). Use a comic/ink/lineart style LoRA here
    to push the color master toward the bold-contour 'inked illustration' house
    look (the coloring-book target), not a painterly render."""
    lora = entry.get("lora")
    if not lora:
        return None, 0.0
    try:
        strength = float(entry.get("lora_strength", 1.0))
    except (TypeError, ValueError):
        strength = 1.0
    return str(lora), strength


def _build_simple_comfy_workflow(
    *,
    prompt,
    negative,
    width,
    height,
    steps,
    cfg,
    seed,
    sampler,
    scheduler,
    unet_loader,
    unet_name,
    unet_dtype,
    clip_name,
    clip_type,
    vae_name,
    filename_prefix,
    lora=None,
    lora_strength=1.0,
):
    """A generic checkpoint->clip->ksampler->vae ComfyUI graph.

    Krea 2 Turbo and Flux.2 Klein share this exact shape (unlike Flux.1, which
    needs a DualCLIPLoader + FluxGuidance). They differ only in loaders, the
    CLIPLoader `type`, VAE, and sampler settings — all passed in. Negative
    conditioning is wired properly (its own CLIPTextEncode), so 'no text/border'
    negatives are live wherever cfg > 1; at cfg 1 they are simply inert rather
    than silently mis-wired to the positive node (the Flux.1 path's known bug)."""
    text = prompt or "a beautiful, richly detailed illustration"
    sampler_seed = resolve_seed(seed)

    if unet_loader == "UnetLoaderGGUF":
        loader_inputs = {"unet_name": unet_name}
    else:  # UNETLoader (safetensors / fp8)
        loader_inputs = {"unet_name": unet_name, "weight_dtype": unet_dtype}

    model_ref = ["1", 0]
    workflow = {
        "1": {
            "inputs": loader_inputs,
            "class_type": unet_loader,
            "_meta": {"title": "Load Diffusion Model"},
        },
        "2": {
            "inputs": {"clip_name": clip_name, "type": clip_type, "device": "default"},
            "class_type": "CLIPLoader",
            "_meta": {"title": "Load CLIP"},
        },
        "3": {
            "inputs": {"text": text, "clip": ["2", 0]},
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Positive Prompt"},
        },
        "4": {
            "inputs": {"text": negative or "", "clip": ["2", 0]},
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Negative Prompt"},
        },
        "5": {
            "inputs": {"vae_name": vae_name},
            "class_type": "VAELoader",
            "_meta": {"title": "Load VAE"},
        },
        "6": {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Empty Latent Image"},
        },
        "7": {
            "inputs": {
                "seed": sampler_seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": scheduler,
                "denoise": 1,
                "model": model_ref,
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["6", 0],
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"},
        },
        "8": {
            "inputs": {"samples": ["7", 0], "vae": ["5", 0]},
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"},
        },
        "9": {
            "inputs": {"filename_prefix": filename_prefix, "images": ["8", 0]},
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"},
        },
    }

    if lora:
        # Model-only style LoRA: cfg~1 distilled models take the aesthetic from
        # the diffusion model, so wrap only the model path (their text encoders
        # are model-specific and not what these style LoRAs were trained on).
        workflow["10"] = {
            "inputs": {
                "model": ["1", 0],
                "lora_name": lora,
                "strength_model": lora_strength,
            },
            "class_type": "LoraLoaderModelOnly",
            "_meta": {"title": "Style LoRA"},
        }
        workflow["7"]["inputs"]["model"] = ["10", 0]

    return workflow


def build_krea2_workflow(prompt, negative, width, height, steps, seed, entry=None):
    """Krea 2 Turbo (Qwen-lineage) ComfyUI graph. See KREA2_* constants."""
    lora, strength = _lora_from_entry(entry or {})
    return _build_simple_comfy_workflow(
        prompt=prompt,
        negative=negative,
        width=width,
        height=height,
        steps=steps,
        cfg=KREA2_CFG,
        seed=seed,
        sampler=KREA2_SAMPLER,
        scheduler=KREA2_SCHEDULER,
        unet_loader=KREA2_UNET_LOADER,
        unet_name=KREA2_MODEL,
        unet_dtype=KREA2_MODEL_DTYPE,
        clip_name=KREA2_CLIP,
        clip_type=KREA2_CLIP_TYPE,
        vae_name=KREA2_VAE,
        filename_prefix="kindrobots_krea2",
        lora=lora,
        lora_strength=strength,
    )


def build_flux2_klein_workflow(prompt, negative, width, height, steps, seed, entry=None):
    """Flux.2 Klein 4B ComfyUI graph. If the entry carries a `json_prompt`
    mapping, it is serialized to JSON for the text encode (Flux.2's structured
    prompt path). See FLUX2_KLEIN_* constants."""
    entry = entry or {}
    lora, strength = _lora_from_entry(entry)
    json_prompt = entry.get("json_prompt")
    if isinstance(json_prompt, (dict, list)) and json_prompt:
        prompt = json.dumps(json_prompt, ensure_ascii=False)
    return _build_simple_comfy_workflow(
        prompt=prompt,
        negative=negative,
        width=width,
        height=height,
        steps=steps,
        cfg=FLUX2_KLEIN_CFG,
        seed=seed,
        sampler=FLUX2_KLEIN_SAMPLER,
        scheduler=FLUX2_KLEIN_SCHEDULER,
        unet_loader=FLUX2_KLEIN_UNET_LOADER,
        unet_name=FLUX2_KLEIN_MODEL,
        unet_dtype="default",
        clip_name=FLUX2_KLEIN_CLIP,
        clip_type=FLUX2_KLEIN_CLIP_TYPE,
        vae_name=FLUX2_KLEIN_VAE,
        filename_prefix="kindrobots_flux2_klein",
        lora=lora,
        lora_strength=strength,
    )


def entry_to_job(entry):
    """Map an art-generate.yaml entry to an ArtJob enqueue body.

    Default engine is Krea 2 (krea2): the entry becomes a COMFY job whose payload
    carries the full Krea 2 workflow graph (native 8-step cadence, Qwen lineage).
    `engine: flux` selects the Flux graph (native 1MP, beta scheduler, guidance
    3.5) for entries that specifically want it; legacy `engine: a1111` entries
    are migrated to the default Krea 2 COMFY workflow.

    Quality knobs (steps, cfg, negative prompt, sampler, seed) default to the
    module constants and may be overridden per entry. Optional knobs (sampler,
    seed) are only sent when set, so an untouched batch keeps the relay's own
    defaults."""
    engine = normalize_engine(entry.get("engine"))
    if engine not in COMFY_WORKFLOW_ENGINES:
        raise ValueError(
            f"unsupported Conductor art engine {engine!r}; "
            f"expected one of {', '.join(COMFY_WORKFLOW_ENGINES)}"
        )
    width, height = parse_size(entry.get("size"))
    prompt = " ".join(str(entry.get("prompt") or "").split())
    negative = " ".join(
        str(entry.get("negative_prompt") or DEFAULT_NEGATIVE_PROMPT).split()
    )

    variant = None
    if engine == "flux":
        variant = str(entry.get("flux_variant") or FLUX_VARIANT).strip().lower()
        if variant not in FLUX_MODELS:
            variant = FLUX_VARIANT
        steps = int(entry.get("steps") or FLUX_MODELS[variant]["steps"])
    elif engine in ENGINE_DEFAULT_STEPS:
        steps = int(entry.get("steps") or ENGINE_DEFAULT_STEPS[engine])
    else:
        steps = int(entry.get("steps") or DEFAULT_STEPS)

    payload = {
        "promptString": prompt,
        "negativePrompt": negative,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg": entry.get("cfg", engine_default_cfg(engine)),
        # the relay's local fast path files its copy under the project's
        # collection folder; untargeted art falls back to the model-family
        # folder (the engine name), not the frontend name ("comfy")
        "collection": entry.get("project") or engine,
    }

    # Optional per-entry knobs: only send when set, so an untouched batch runs
    # on the relay's proven defaults rather than a possibly-unsupported sampler.
    if entry.get("sampler"):
        payload["sampler"] = str(entry["sampler"])
    if entry.get("seed") is not None:
        payload["seed"] = entry["seed"]

    # `resolvedSeed` is the concrete seed the render actually uses. For the graph
    # engines we resolve it here (random when the entry omits it or passes -1),
    # bake that exact value into the workflow, AND report it on the job so the
    # caller can record "the real seed used" and reproduce an accepted render
    # later. For any non-workflow passthrough path the backend assigns the seed, so
    # we can only echo whatever the entry supplied (may be None).
    resolved_seed = entry.get("seed")

    if engine in COMFY_WORKFLOW_ENGINES:
        resolved_seed = resolve_seed(entry.get("seed"))
        if engine == "flux":
            payload["workflow"] = build_flux_workflow(
                prompt=prompt,
                width=width,
                height=height,
                steps=steps,
                guidance=entry.get("guidance", FLUX_MODELS[variant]["guidance"]),
                seed=resolved_seed,
                unet=FLUX_MODELS[variant]["unet"],
            )
        elif engine == "krea2":
            payload["workflow"] = build_krea2_workflow(
                prompt, negative, width, height, steps, resolved_seed, entry
            )
        else:  # flux2-klein
            payload["workflow"] = build_flux2_klein_workflow(
                prompt, negative, width, height, steps, resolved_seed, entry
            )
        relay_engine = "COMFY"
    else:  # pragma: no cover - guarded above; all Conductor jobs are COMFY
        raise AssertionError(f"missing COMFY workflow builder for {engine}")

    return {
        "engine": relay_engine,
        "projectSlug": entry.get("project") or None,
        "payload": payload,
        "resolvedSeed": resolved_seed,
    }


def load_entries():
    if not ART_GENERATE_FILE.exists():
        return []
    data = yaml.safe_load(ART_GENERATE_FILE.read_text()) or {}
    # Canonical shape is batch.entries. Tolerate a legacy top-level `images:`
    # list too, so a batch written by an older queue_missing_project_art.py
    # (or one already sitting on disk) is still consumed rather than silently
    # skipped.
    entries = (data.get("batch") or {}).get("entries") or data.get("images") or []
    return [
        e
        for e in entries
        if isinstance(e, dict)
        and e.get("prompt")
        and e.get("image_path")
        and _is_pending(e)
    ]


def _is_pending(entry):
    """An entry is still consumable unless it has already been drained
    (status done/complete). This lets the queue self-clear: once an entry has
    been enqueued as an ArtJob and its render landed, it is marked done and
    skipped on the next run."""
    return (
        str(entry.get("status") or "pending").strip().lower()
        not in ("done", "complete", "completed")
    )


ENTRY_START_PAT = re.compile(r"^(\s*)-\s")
IMAGE_PATH_PAT = re.compile(r"^\s*image_path:\s*(.+?)\s*$")
STATUS_PAT = re.compile(r'^(\s*)status:\s*["\']?[A-Za-z0-9_-]+["\']?\s*(#.*)?$')


def set_entry_status(text, image_path, new_status):
    """Flip (or insert) the status line of the batch entry whose image_path
    matches. Surgical, comment-preserving line edit — pyyaml round-trip would
    drop the header and reformat every multi-line prompt. Mirrors
    consume_art_requests.set_request_status."""
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if ENTRY_START_PAT.match(line)]

    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)

        matched = False
        for j in range(start, end):
            m = IMAGE_PATH_PAT.match(lines[j])
            if m and m.group(1).strip().strip("'\"") == image_path:
                matched = True
                break

        if not matched:
            continue

        for j in range(start, end):
            sm = STATUS_PAT.match(lines[j])
            if sm:
                lines[j] = f"{sm.group(1)}status: {new_status}\n"
                return "".join(lines), True

        # No status line on this entry — add one under image_path.
        for j in range(start, end):
            pm = IMAGE_PATH_PAT.match(lines[j])
            if pm:
                indent = re.match(r"^(\s*)", lines[j]).group(1)
                lines.insert(j + 1, f"{indent}status: {new_status}\n")
                return "".join(lines), True

    return text, False


def mark_generate_done(image_paths):
    """Mark each image_path's entry status: done (single read/write).
    Returns the number of entries changed."""
    if not image_paths or not ART_GENERATE_FILE.exists():
        return 0

    text = ART_GENERATE_FILE.read_text()
    changed = 0
    for image_path in image_paths:
        text, did = set_entry_status(text, image_path, "done")
        if did:
            changed += 1

    if changed:
        ART_GENERATE_FILE.write_text(text)
    return changed


def staged_filename(entry):
    """Collision-safe filename for landing an entry's render in projects/process/.

    Plain Path(image_path).name is not always unique across entries: several
    project-art requests can share an identical basename with the
    disambiguating project slug living only in the parent directory (e.g.
    every kind_robots hero request uses image_path
    public/images/projects/{slug}/hero.webp -- basename "hero.webp" for
    every project). Two such entries landing in the same run silently
    overwrite each other in projects/process/, and kind_robots-target files
    are RETAINED there indefinitely (never moved out by distribute_images.py
    -- see its distribute() kind_robots branch), so the collision persists
    across runs too, not just within one batch.

    When an entry carries explicit project_slug/variant metadata (missing-
    image project-art requests, see consume_art_requests.py's
    project_art_sync_payload) and its basename doesn't already encode the
    slug, stage under {slug}-{variant}{suffix} instead -- the same naming
    convention distribute_images.py already uses for every other project
    icon/card/hero file, so no other matching logic needs to change.
    distribute_images.py's build_lookup() must derive this identical key so
    the two stay in sync.
    """
    name = Path(entry["image_path"]).name
    slug = str(entry.get("project_slug") or "").strip()
    variant = str(entry.get("variant") or "").strip().lower()
    if slug and variant and not name.lower().startswith(f"{slug.lower()}-"):
        name = f"{slug}-{variant}{Path(name).suffix}"
    return name


def save_result(entry, image_b64):
    """Write the finished image into projects/process/ under a collision-safe
    staging name (see staged_filename) — converted to webp when Pillow is
    available, else as .png."""
    PROCESS_DIR.mkdir(parents=True, exist_ok=True)
    target_name = staged_filename(entry)
    png_bytes = base64.b64decode(image_b64)

    if target_name.lower().endswith(".webp"):
        try:
            import io

            from PIL import Image  # optional dependency

            img = Image.open(io.BytesIO(png_bytes))
            out = PROCESS_DIR / target_name
            img.save(out, "WEBP", quality=90)
            return out, None
        except ImportError:
            out = PROCESS_DIR / (Path(target_name).stem + ".png")
            out.write_bytes(png_bytes)
            return out, (
                "Pillow not installed - saved PNG; convert to "
                f"{target_name} before running distribute_images.py"
            )

    out = PROCESS_DIR / target_name
    out.write_bytes(png_bytes)
    return out, None


def enqueue(job_body):
    status, resp = http_json("POST", f"{KR_BASE_URL}/api/art/queue", job_body)
    if status not in (200, 201) or not resp or not resp.get("success"):
        raise RuntimeError(f"enqueue failed: HTTP {status} {resp and resp.get('message')}")
    return resp["data"]["job"]["id"]


def wait_for_job(job_id, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        status, resp = http_json("GET", f"{KR_BASE_URL}/api/art/queue/{job_id}")
        if status == 200 and resp and resp.get("success"):
            job = resp["data"]["job"]
            if job["status"] == "DONE":
                return job
            if job["status"] in ("FAILED", "CANCELLED"):
                raise RuntimeError(f"job {job_id} {job['status']}: {job.get('error')}")
        time.sleep(POLL_SECONDS)
    raise RuntimeError(f"job {job_id} timed out after {timeout}s (still queued/running)")


def fetch_image_b64(art_image_id):
    status, resp = http_json(
        "GET",
        f"{KR_BASE_URL}/api/art/image/{art_image_id}?includeImageData=true",
        timeout=180,
    )
    if status != 200 or not resp:
        raise RuntimeError(f"image fetch failed: HTTP {status}")
    record = resp.get("data") or {}
    image_b64 = record.get("imageData")
    if not image_b64:
        raise RuntimeError(f"ArtImage {art_image_id} has no imageData")
    return image_b64


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="actually queue and download")
    parser.add_argument("--limit", type=int, default=0, help="max entries this run (0 = all)")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to wait per job")
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="fire-and-forget: enqueue each entry, mark it done, and exit without "
        "blocking on the render (the relay renders asynchronously; image download "
        "happens separately). Won't freeze when the relay is offline.",
    )
    args = parser.parse_args()

    entries = load_entries()
    if args.limit > 0:
        entries = entries[: args.limit]

    if not entries:
        print("No approved entries in projects/art-generate.yaml - nothing to do.")
        return 0

    print(f"{'LIVE' if args.live else 'DRY RUN'}: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} via {KR_BASE_URL}\n")

    if not args.live:
        for entry in entries:
            job = entry_to_job(entry)
            print(
                f"  would queue {entry['image_path']}"
                f"  [{job['payload']['width']}x{job['payload']['height']}]"
                f"  {job['payload']['steps']}steps"
                f"  \"{job['payload']['promptString'][:60]}\""
            )
        print("\nRe-run with --live to queue for real (requires KR_API_TOKEN).")
        return 0

    if not KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    failures = 0
    done_paths = []
    for entry in entries:
        name = entry["image_path"]
        try:
            job_id = enqueue(entry_to_job(entry))

            if args.no_wait:
                # Fire-and-forget: the entry is now an ArtJob; the relay owns the
                # render. Mark it done and move on — don't block on the render.
                print(f"  queued job {job_id} for {name} - not waiting (relay will render)")
                done_paths.append(name)
                continue

            print(f"  queued job {job_id} for {name} - waiting...")
            job = wait_for_job(job_id, args.timeout)
            image_b64 = fetch_image_b64(job["artImageId"])
            out, warning = save_result(entry, image_b64)
            print(f"  DONE {name} -> {out.relative_to(ROOT)} (ArtImage {job['artImageId']})")
            if warning:
                print(f"    WARNING: {warning}")
            # Enqueued as an ArtJob and rendered — drain it from the queue so it
            # is not re-sent next run. Failed entries stay pending for retry.
            done_paths.append(name)
        except Exception as e:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED {name}: {e}", file=sys.stderr)

    cleared = mark_generate_done(done_paths)

    if args.no_wait:
        print(
            f"\n{len(entries) - failures}/{len(entries)} enqueued"
            f"; {cleared} marked done in {ART_GENERATE_FILE.relative_to(ROOT)}."
            " The relay renders them asynchronously; run distribute_images.py once"
            " the images land (or set the relay's KR_LOCAL_IMAGES_DIR)."
        )
    else:
        print(
            f"\n{len(entries) - failures}/{len(entries)} succeeded"
            f"; {cleared} marked done in {ART_GENERATE_FILE.relative_to(ROOT)}."
            + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
        )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
