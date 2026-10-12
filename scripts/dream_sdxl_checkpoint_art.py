#!/usr/bin/env python3
"""Real ComfyUI SDXL ArtJobs for the Zuzu expansion of the Daily Dream.

The existing original Daily Dream continues through its established Krea lane.
The *additional*, unlinked Zuzu assets can use the two active, documented
Illustrious-series lanes used by Kind Robots' comic rendering. Never turn a
family label into a Krea workflow or blindly accept an unverified model path.
"""
from __future__ import annotations

from typing import Any

# Source of truth: kind_robots/utils/comicLanes.ts DEFAULT_COMIC_LANES.
# Arthemy is an Illustrious-family checkpoint, but has its own tuned settings.
CHECKPOINT_LANES = {
    "arthemy": {
        "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
        "steps": 30, "cfg": 5.0, "sampler": "euler_ancestral",
        "scheduler": "normal",
        "style": "anthropomorphic characters, western comics (style), toon (style), dusty painterly inks",
    },
    "illustrious": {
        "checkpoint": "Illustrious/furrytoonmix_xlV3.safetensors",
        "steps": 20, "cfg": 8.0, "sampler": "dpmpp_2m",
        "scheduler": "karras",
        "style": "expressive anthropomorphic animal folk, illustrated character design, rich color",
    },
}
ENGINE = "sdxl-checkpoint"
SUPPORTED_PROJECTS = ("zuzu-gamebook", "emperor-of-dust")


def resolve_registered_checkpoint(family: str, resource_index: dict) -> str:
    """Resolve exact catalog CHECKPOINT identity; NEVER silently use a default."""
    if family not in CHECKPOINT_LANES:
        raise ValueError(f"unsupported Zuzu checkpoint family: {family!r}")
    expected = CHECKPOINT_LANES[family]["checkpoint"]
    filename = expected.rsplit("/", 1)[-1]
    registered = resource_index.get("CHECKPOINT", {}).get(filename.lower())
    # The catalog uses a ComfyUI-relative path retaining the Illustrious/ folder.
    if not registered or registered.casefold() != expected.casefold():
        raise RuntimeError(
            f"{family} checkpoint {expected!r} is not confirmed in the Kind Robots "
            "CHECKPOINT Resource catalog; refusing a mislabeled ArtJob"
        )
    return registered


def make_checkpoint_job(entry: dict[str, Any], core) -> dict[str, Any]:
    """Build a full ComfyUI workflow compatible with /api/art/queue.

    The queue accepts a COMFY ArtJob containing a workflow graph, NOT
    /api/art/enqueue's browser-only engine='comfy' request shape.
    """
    family = str(entry.get("checkpoint_family") or "").strip().lower()
    project = str(entry.get("project_target") or "").strip()
    if project not in SUPPORTED_PROJECTS:
        raise ValueError("Zuzu checkpoint ArtJobs require a known project_target")
    checkpoint = resolve_registered_checkpoint(family, core._load_resource_index())
    lane = CHECKPOINT_LANES[family]
    width, height = core.parse_size(entry.get("size"))
    prompt = " ".join(str(entry.get("prompt") or "").split())
    if not prompt:
        raise ValueError("checkpoint ArtJob requires a non-empty prompt")
    prompt = f"{lane['style']}, {prompt}"
    negative = " ".join(str(
        entry.get("negative_prompt")
        or "low quality, blurry, bad anatomy, disfigured, writing, text, watermark"
    ).split())
    steps = int(entry.get("steps") or lane["steps"])
    cfg = float(entry.get("cfg") or lane["cfg"])
    if not (1 <= steps <= 100 and 1 <= cfg <= 30):
        raise ValueError("invalid steps/cfg for checkpoint ArtJob")
    seed = core.resolve_seed(entry.get("seed"))
    clip = ["8", 0]
    graph = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint}},
        "8": {"class_type": "CLIPSetLastLayer", "inputs": {
            "clip": ["1", 1], "stop_at_clip_layer": -2,
        }},
        "2": {"class_type": "CLIPTextEncode", "inputs": {
            "text": prompt, "clip": clip,
        }},
        "3": {"class_type": "CLIPTextEncode", "inputs": {
            "text": negative, "clip": clip,
        }},
        "4": {"class_type": "EmptyLatentImage", "inputs": {
            "width": width, "height": height, "batch_size": 1,
        }},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": cfg,
            "sampler_name": lane["sampler"], "scheduler": lane["scheduler"],
            "denoise": 1, "model": ["1", 0], "positive": ["2", 0],
            "negative": ["3", 0], "latent_image": ["4", 0],
        }},
        "6": {"class_type": "VAEDecode", "inputs": {
            "samples": ["5", 0], "vae": ["1", 2],
        }},
        "7": {"class_type": "SaveImage", "inputs": {
            "filename_prefix": f"daily_zuzu_{family}", "images": ["6", 0],
        }},
    }
    return {
        "engine": "COMFY",
        "projectSlug": project,
        "resolvedSeed": seed,
        "payload": {
            "promptString": prompt,
            "negativePrompt": negative,
            "width": width, "height": height,
            "steps": steps, "cfg": cfg,
            "workflow": graph,
            "collection": "dream-cycle",
            "resources": {
                "checkpointName": checkpoint,
                "checkpointFamily": family,
            },
        },
    }
