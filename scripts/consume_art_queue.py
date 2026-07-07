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

Dry-run by default: prints what would be queued and touches nothing.
The first live run is human-gated (Silas approves; see roadmap t-012).

Environment:
  KR_API_TOKEN   required for --live (machine auth: user apiKey or admin token)
  KR_BASE_URL    default https://kind-robots.vercel.app

Usage:
  python scripts/consume_art_queue.py                    # dry run
  python scripts/consume_art_queue.py --live             # queue + wait + download
  python scripts/consume_art_queue.py --live --limit 3   # first 3 entries only

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
# Default engine is FLUX (dev) — the beautiful-by-default path. A flux entry is
# emitted as a COMFY job carrying the full Flux workflow graph below, which the
# home relay's run_comfy drives on ComfyUI. Set `engine: a1111` on an entry to
# fall back to the A1111 txt2img path (raw KR-style keys the relay consumes
# directly) — useful when ComfyUI is down or for quick SD-only tests.
DEFAULT_ENGINE = "flux"
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


def resolve_seed(seed):
    """A concrete, in-range seed. Reuse a caller-supplied non-negative int;
    otherwise pick a random one (matches the KR endpoint's -1 -> random)."""
    if isinstance(seed, int) and not isinstance(seed, bool) and seed >= 0:
        return seed
    return random.randint(0, 1_000_000_000_000_000)


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
                "clip_name1": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
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


def entry_to_job(entry):
    """Map an art-generate.yaml entry to an ArtJob enqueue body.

    Default engine is Flux: the entry becomes a COMFY job whose payload carries
    the full Flux workflow graph (native 1MP, beta scheduler, guidance 3.5).
    `engine: a1111` on an entry instead emits KR-style txt2img keys the relay's
    run_a1111 consumes directly.

    Quality knobs (steps, cfg, negative prompt, sampler, seed) default to the
    module constants and may be overridden per entry. Optional knobs (sampler,
    seed) are only sent when set, so an untouched batch keeps the relay's own
    defaults."""
    engine = str(entry.get("engine") or DEFAULT_ENGINE).strip().lower()
    width, height = parse_size(entry.get("size"))
    prompt = " ".join(str(entry.get("prompt") or "").split())
    negative = " ".join(
        str(entry.get("negative_prompt") or DEFAULT_NEGATIVE_PROMPT).split()
    )

    if engine == "flux":
        variant = str(entry.get("flux_variant") or FLUX_VARIANT).strip().lower()
        if variant not in FLUX_MODELS:
            variant = FLUX_VARIANT
        steps = int(entry.get("steps") or FLUX_MODELS[variant]["steps"])
    else:
        steps = int(entry.get("steps") or DEFAULT_STEPS)

    payload = {
        "promptString": prompt,
        "negativePrompt": negative,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg": entry.get("cfg", DEFAULT_CFG),
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

    if engine == "flux":
        # Emit a COMFY job carrying the Flux graph; the relay drives ComfyUI.
        payload["workflow"] = build_flux_workflow(
            prompt=prompt,
            width=width,
            height=height,
            steps=steps,
            guidance=entry.get("guidance", FLUX_MODELS[variant]["guidance"]),
            seed=entry.get("seed"),
            unet=FLUX_MODELS[variant]["unet"],
        )
        relay_engine = "COMFY"
    else:
        relay_engine = engine.upper()

    return {
        "engine": relay_engine,
        "projectSlug": entry.get("project") or None,
        "payload": payload,
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
        if isinstance(e, dict) and e.get("prompt") and e.get("image_path")
    ]


def save_result(entry, image_b64):
    """Write the finished image into projects/process/ under the entry's
    basename — converted to webp when Pillow is available, else as .png."""
    PROCESS_DIR.mkdir(parents=True, exist_ok=True)
    target_name = Path(entry["image_path"]).name
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
    if status != 201 or not resp or not resp.get("success"):
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
    for entry in entries:
        name = entry["image_path"]
        try:
            job_id = enqueue(entry_to_job(entry))
            print(f"  queued job {job_id} for {name} - waiting...")
            job = wait_for_job(job_id, args.timeout)
            image_b64 = fetch_image_b64(job["artImageId"])
            out, warning = save_result(entry, image_b64)
            print(f"  DONE {name} -> {out.relative_to(ROOT)} (ArtImage {job['artImageId']})")
            if warning:
                print(f"    WARNING: {warning}")
        except Exception as e:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED {name}: {e}", file=sys.stderr)

    print(
        f"\n{len(entries) - failures}/{len(entries)} succeeded."
        + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
