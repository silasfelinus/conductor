#!/usr/bin/env python3
"""Real ComfyUI SDXL ArtJobs for the Zuzu expansion of the Daily Dream.

The existing original Daily Dream continues through its established Krea lane.
The *additional*, unlinked Zuzu assets can use the two active, documented
Illustrious-series lanes used by Kind Robots' comic rendering. Never turn a
family label into a Krea workflow or blindly accept an unverified model path.
"""
from __future__ import annotations

import math
import re
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
    # Shifting Desks uses two distinct treatments of Arthemy, not the
    # rejected furrytoonmix/Dilbert-like or nihilmania visual pitches.
    "corporate-noir": {
        "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
        "steps": 30, "cfg": 5.0, "sampler": "euler_ancestral",
        "scheduler": "normal",
        "style": "masterpiece, best quality, amazing quality, absurdres, very aesthetic, western comics (style), dramatic graphic novel, deep dark ink shadows, expressive body language, strong silhouettes, cinematic color contrast, moody green phosphor glow",
    },
    "western-cartoon": {
        "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
        "steps": 30, "cfg": 5.0, "sampler": "euler_ancestral",
        "scheduler": "normal",
        "style": "masterpiece, best quality, amazing quality, absurdres, very aesthetic, western comics (style), toon (style), premium western animated feature key art, polished expressive character designs, warm orange rim lighting against emerald green office fluorescents, glossy inked shell highlights, strong theatrical gestures, cinematic low angle, rich stylized cel painting, inviting character warmth, playful institutional dread",
    },
}
ENGINE = "sdxl-checkpoint"
SUPPORTED_PROJECTS = ("zuzu-gamebook", "emperor-of-dust", "shifting-desks")
SHIFTING_DESKS_FAMILIES = {"corporate-noir", "western-cartoon"}
ZUZU_PROJECTS = ("zuzu-gamebook", "emperor-of-dust")

# kind_robots utils/comicLanes.ts ILLUSTRIOUS_PREFIX. Illustrious checkpoints
# are tag-trained and expect the quality tags first; the 2026-10-13..17 Zuzu
# jobs shipped without them (Silas, 2026-10-18).
ILLUSTRIOUS_PREFIX = "masterpiece, best quality, amazing quality, absurdres, very aesthetic"

# Canon Zuzu, from kind_robots utils/musicVideoSpecs.ts ZUZU (VIDEO-GUARDRAILS.md
# "Canon in every prompt"). The checkpoint has never heard of "Zuzu": a prompt
# that names him without these tags draws a random animal.
ZUZU_CANON_TAGS = (
    "Zuzu, anthro, koala, male, adult, (short:1.2), (stocky:1.2), standing upright, "
    "short legs, small stature, slight paunch, grey fur, round fluffy ears, broad black nose, "
    "serious, squinting, rust-brown poncho, orange zigzag trim, dark tunic, orange sash, "
    "dark brown cloth trousers, (katana on back:1.3), hilt over right shoulder, "
    "conical straw kasa, wide brim shading the eyes, (fully clothed:1.3)"
)
ZUZU_CANON_NEGATIVE = (
    "tall, lanky, long legs, slender, straw boater, cowboy hat, cloak, cape, "
    "feather duster, chibi"
)
ZUZU_NEGATIVE = (
    "(nude:1.4), (naked:1.3), nsfw, suggestive, lowres, worst quality, bad anatomy, "
    "bad hands, extra limbs, deformed, blurry, jpeg artifacts, human, text, english lettering, "
    "watermark, signature, logo"
)
DEFAULT_NEGATIVE = "low quality, blurry, bad anatomy, disfigured, writing, text, watermark"

# VIDEO-GUARDRAILS.md: words the house checkpoint draws literally, and the
# bannedTerms list (every character is an animal). Applied to Zuzu-world
# prompts at submission so already-queued requests re-render correctly too.
LITERAL_WORD_SUBSTITUTIONS = (
    (r"\b(grey|gray|white|silver)-muzzled\b", r"\1-snouted"),
    (r"\bmuzzles?\b(?!-)", "snout"),
    (r"\bdusters?\b", "long riding coat"),
    (r"\bpost-human\b", "forgotten"),
    (r"\b(humans|humanity|mankind)\b", "animal-folk"),
    (r"\bhuman\b", "animal-folk"),
    (r"\bpeople\b", "townsfolk"),
)
ZUZU_MENTION = re.compile(r"\b(zuzu|koala)\b", re.IGNORECASE)
# A koala in the authored art direction is Zuzu; his canon hat is a kasa and
# he wears a poncho, never a straw boater or cloak (VIDEO-GUARDRAILS.md).
ZUZU_COSTUME_SUBSTITUTIONS = (
    (r"\bstraw hat\b", "conical straw kasa"),
    (r"\b(travel |travelling |traveling )?(cloak|cape)\b", "poncho"),
)

# SDXL is trained near one megapixel; the 512x768 card size is an SD1.5 size
# and renders mushy, duplicated anatomy. Same buckets as kind_robots
# utils/comicLanes.ts COMIC_RENDER_SIZES.
SDXL_BUCKETS = (
    (1024, 1024), (1152, 896), (896, 1152), (1216, 832), (832, 1216),
    (1344, 768), (768, 1344), (1536, 640),
)
SDXL_MIN_PIXELS = 896 * 896


def sdxl_render_size(width: int, height: int) -> tuple[int, int]:
    """Native SDXL bucket closest in aspect to a requested size below ~0.8MP."""
    if width * height >= SDXL_MIN_PIXELS:
        return width, height
    aspect = width / height
    return min(SDXL_BUCKETS, key=lambda wh: abs(math.log((wh[0] / wh[1]) / aspect)))


def compose_checkpoint_prompt(prompt: str, family: str, project: str) -> tuple[str, str]:
    """Positive and default negative prompt for one checkpoint ArtJob.

    The dream-cycle builder ends every prompt with the lane style; this used to
    prepend it a second time. Strip it from the body and lead with quality tags
    and style once, then canon tags when Zuzu is in the frame.
    """
    lane = CHECKPOINT_LANES[family]
    style = lane["style"]
    body = " ".join(str(prompt or "").split())
    body = body.replace(f", {style}", "").replace(style, "").strip(" ,")
    negative = DEFAULT_NEGATIVE
    canon = ""
    if project in ZUZU_PROJECTS:
        for pattern, replacement in LITERAL_WORD_SUBSTITUTIONS:
            body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)
        negative = ZUZU_NEGATIVE
        if project == "zuzu-gamebook" and ZUZU_MENTION.search(body):
            for pattern, replacement in ZUZU_COSTUME_SUBSTITUTIONS:
                body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)
            canon = ZUZU_CANON_TAGS
            negative = f"{ZUZU_NEGATIVE}, {ZUZU_CANON_NEGATIVE}"
    prefix = "" if style.startswith(ILLUSTRIOUS_PREFIX) else ILLUSTRIOUS_PREFIX
    positive = ", ".join(part for part in (prefix, style, canon, body) if part)
    return positive, negative


def resolve_registered_checkpoint(family: str, resource_index: dict) -> str:
    """Resolve exact catalog CHECKPOINT identity; NEVER silently use a default."""
    if family not in CHECKPOINT_LANES:
        raise ValueError(f"unsupported checkpoint family: {family!r}")
    expected = CHECKPOINT_LANES[family]["checkpoint"]
    filename = expected.rsplit("/", 1)[-1]
    registered = resource_index.get("CHECKPOINT", {}).get(filename.lower())
    # The catalog uses a ComfyUI-relative path retaining the Illustrious/ folder.
    if registered:
        if registered.casefold() != expected.casefold():
            raise RuntimeError(
                f"{family} checkpoint {expected!r} conflicts with Resource registry "
                f"entry {registered!r}; refusing a mislabeled ArtJob"
            )
        return registered

    # /api/resources is a *visibility-filtered gallery*, not a complete model
    # inventory. Private/mature CHECKPOINT rows are omitted for the worker JWT
    # even though the house Comic Studio has rendered against this exact Arthemy
    # path (kind_robots utils/comicLanes.ts, Zuzu's approved Arthemy keyframes).
    # For the two Shifting Desks lanes ONLY, fall back to that one audited,
    # exact pinned path; the render box will still check actual file existence.
    # Never do this for arbitrary names, mismatched active catalog entries or
    # Daily Dream's independently guarded checkpoint lanes.
    if family in SHIFTING_DESKS_FAMILIES and expected == (
        "Illustrious/arthemyWesternArt_v30.safetensors"
    ):
        return expected

    raise RuntimeError(
        f"{family} checkpoint {expected!r} is not confirmed in the Kind Robots "
        "CHECKPOINT Resource catalog; refusing a mislabeled ArtJob"
    )


def make_checkpoint_job(entry: dict[str, Any], core) -> dict[str, Any]:
    """Build a full ComfyUI workflow compatible with /api/art/queue.

    The queue accepts a COMFY ArtJob containing a workflow graph, NOT
    /api/art/enqueue's browser-only engine='comfy' request shape.
    """
    family = str(entry.get("checkpoint_family") or "").strip().lower()
    project = str(entry.get("project_target") or "").strip()
    if project not in SUPPORTED_PROJECTS:
        raise ValueError("checkpoint ArtJobs require a known project_target")
    if (project == "shifting-desks") != (family in SHIFTING_DESKS_FAMILIES):
        raise ValueError("checkpoint family is reserved for its own project")
    checkpoint = resolve_registered_checkpoint(family, core._load_resource_index())
    lane = CHECKPOINT_LANES[family]
    width, height = sdxl_render_size(*core.parse_size(entry.get("size")))
    if not str(entry.get("prompt") or "").strip():
        raise ValueError("checkpoint ArtJob requires a non-empty prompt")
    prompt, default_negative = compose_checkpoint_prompt(entry.get("prompt"), family, project)
    negative = " ".join(str(entry.get("negative_prompt") or default_negative).split())
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
            "filename_prefix": f"{project.replace('-', '_')}_{family}", "images": ["6", 0],
        }},
    }
    job = {
        "engine": "COMFY",
        "projectSlug": project,
        "resolvedSeed": seed,
        "payload": {
            "promptString": prompt,
            "negativePrompt": negative,
            "width": width, "height": height,
            "steps": steps, "cfg": cfg,
            "workflow": graph,
            "collection": project if project == "shifting-desks" else "dream-cycle",
            "resources": {
                "checkpointName": checkpoint,
                "checkpointFamily": family,
            },
        },
    }

    # Keep non-Dream checkpoint jobs in the ordinary ArtJob priority lane,
    # ahead of no one else's Daily Dream submissions.
    if project == "shifting-desks" and entry.get("priority") is not None:
        job["priority"] = int(entry["priority"])
    return job
