#!/usr/bin/env python3
"""Build kohya sd-scripts LoRA datasets from locked Comic Studio cast renders (comic-creator t-016).

A spec YAML names each character's trigger word, class word, identity tags and images (Kind Robots
ArtImage ids). For every character this writes, under ``--out``:

    <trigger>/img/<repeats>_<trigger> <class>/NNN.png   the training images
    <trigger>/img/<repeats>_<trigger> <class>/NNN.txt   one caption per image, trigger word first
    <trigger>/dataset.toml                               kohya dataset config (buckets, captions)
    <trigger>/train.ps1                                  SDXL LoRA run for a 12 GB card
    <trigger>.zip                                        the folder above, ready to copy to the box

Spec images:
  - ``id: 242395`` uses the render as it is; a negative id (``-242193``) mirrors it, the same
    convention as the cast tables in import_comic_studio.py.
  - ``crop: [l, t, r, b]`` (fractions) cuts a close-up, for headshots.
  - ``tags`` are the per-image caption tags (view, expression, framing).
  - ``ledger: LEDGER.yaml`` + ``ledger_key`` take the id from an art ledger subject's
    ``art.<lane>.art_image_id`` once ``enqueue_art_requests.py --status`` has filled it.

Training is not run here: no trainer is installed anywhere in Conductor or Kind Robots. Silas runs
train.ps1 on the render box. Finished .safetensors go to the LoRA import inbox, where
ops/home-server/lora_import_agent.py registers them as Kind Robots LoRA resources.

Usage:
    python scripts/build_lora_dataset.py SPEC.yaml --out DIR [--only zuzu] [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

TRIGGER_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def caption(trigger, identity, tags):
    """The caption for one image: trigger word first, then identity tags, then the image's own tags."""
    parts = [trigger, *identity, *tags]
    seen, out = set(), []
    for part in (p.strip() for p in parts):
        if part and part.lower() not in seen:
            seen.add(part.lower())
            out.append(part)
    return ", ".join(out)


def subset_dir(character):
    return f"{int(character.get('repeats', 10))}_{character['trigger']} {character['class']}"


def resolve_image_id(image, spec_dir, ledgers=None):
    """The signed ArtImage id for a spec image: ``id`` directly, or looked up in an art ledger."""
    if "id" in image:
        return int(image["id"])
    ledgers = ledgers if ledgers is not None else {}
    path = spec_dir / image["ledger"]
    if path not in ledgers:
        ledgers[path] = yaml.safe_load(path.read_text())
    for subject in ledgers[path].get("subjects") or []:
        if subject.get("key") == image["ledger_key"]:
            for cell in (subject.get("art") or {}).values():
                if isinstance(cell, dict) and cell.get("art_image_id"):
                    return int(cell["art_image_id"])
            raise ValueError(f"{image['ledger_key']}: no art_image_id yet (run --status on {image['ledger']})")
    raise ValueError(f"{image['ledger_key']}: not in {image['ledger']}")


def validate(spec):
    problems = []
    for character in spec.get("characters") or []:
        trigger = str(character.get("trigger", ""))
        if not TRIGGER_RE.match(trigger):
            problems.append(f"{character.get('key')}: trigger {trigger!r} must match {TRIGGER_RE.pattern}")
        if not character.get("class"):
            problems.append(f"{character.get('key')}: class word is required")
        if len(character.get("images") or []) < 10:
            problems.append(f"{character.get('key')}: {len(character.get('images') or [])} images; a LoRA set needs at least 10")
    return problems


def dataset_toml(character, resolution=1024):
    return (
        "[general]\n"
        "enable_bucket = true\n"
        "min_bucket_reso = 512\n"
        "max_bucket_reso = 1536\n"
        'caption_extension = ".txt"\n'
        "\n"
        "[[datasets]]\n"
        f"resolution = {resolution}\n"
        "batch_size = 1\n"
        "\n"
        "  [[datasets.subsets]]\n"
        f"  image_dir = 'img/{subset_dir(character)}'\n"
        f"  num_repeats = {int(character.get('repeats', 10))}\n"
    )


def train_ps1(character, base_model, output_dir, epochs=10):
    name = f"{character['trigger']}_v1"
    return f"""# Train the {character['name']} LoRA ({character['trigger']}) with kohya sd-scripts on a 12 GB card.
# Run from this folder: powershell -ExecutionPolicy Bypass -File .\\train.ps1 [-SdScripts D:\\ai\\sd-scripts]
# Settings for 12 GB: U-Net only, cached latents and text-encoder outputs, gradient checkpointing, AdamW8bit.
param(
  [string]$SdScripts = "D:\\ai\\sd-scripts",
  [string]$Model = "{base_model}",
  [string]$Out = "{output_dir}"
)
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
if (-not (Test-Path $Model)) {{ throw "Base model not found: $Model" }}
New-Item -ItemType Directory -Force -Path $Out | Out-Null
Set-Location $SdScripts
& .\\venv\\Scripts\\accelerate.exe launch --num_cpu_threads_per_process 1 sdxl_train_network.py `
  --pretrained_model_name_or_path "$Model" `
  --dataset_config "$here\\dataset.toml" `
  --output_dir "$Out" --output_name "{name}" --save_model_as safetensors `
  --network_module networks.lora --network_dim 16 --network_alpha 8 `
  --network_train_unet_only --cache_text_encoder_outputs `
  --learning_rate 1e-4 --optimizer_type AdamW8bit `
  --lr_scheduler cosine --lr_warmup_steps 50 `
  --max_train_epochs {epochs} --save_every_n_epochs 2 --train_batch_size 1 `
  --mixed_precision fp16 --save_precision fp16 `
  --gradient_checkpointing --cache_latents --cache_latents_to_disk --sdpa `
  --max_data_loader_n_workers 1 --seed 42
Write-Host "Done: $Out\\{name}.safetensors (every 2 epochs also saved as {name}-0000NN)"
"""


def render(image, data, crop):
    """Mirror and crop one fetched render (PIL Image)."""
    from PIL import ImageOps

    if image < 0:
        data = ImageOps.mirror(data)
    if crop:
        left, top, right, bottom = (float(v) for v in crop)
        if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
            raise ValueError(f"crop {crop} must be fractions with left < right and top < bottom")
        w, h = data.size
        data = data.crop((round(left * w), round(top * h), round(right * w), round(bottom * h)))
    return data


def build(spec, spec_dir, out, only=None, fetch=None, dry_run=False):
    import enqueue_art_requests as enq

    fetch = fetch or (lambda image_id: enq._decode_data_url(enq.fetch_source_image(image_id)).convert("RGB"))
    ledgers, written = {}, {}
    for character in spec["characters"]:
        if only and character["key"] not in only:
            continue
        root = out / character["trigger"]
        sub = root / "img" / subset_dir(character)
        rows = []
        for n, image in enumerate(character["images"], start=1):
            try:
                image_id = resolve_image_id(image, spec_dir, ledgers)
            except ValueError:
                if not dry_run:
                    raise
                image_id = None  # a dry run reports a render that has not landed yet
            text = caption(character["trigger"], character.get("identity") or [], image.get("tags") or [])
            rows.append((n, image_id, image.get("crop"), text))
        written[character["key"]] = rows
        if dry_run:
            continue
        sub.mkdir(parents=True, exist_ok=True)
        cache = {}
        for n, image_id, crop, text in rows:
            if abs(image_id) not in cache:
                cache[abs(image_id)] = fetch(abs(image_id))
            render(image_id, cache[abs(image_id)], crop).save(sub / f"{n:03d}.png")
            (sub / f"{n:03d}.txt").write_text(text + "\n")
        (root / "dataset.toml").write_text(dataset_toml(character))
        (root / "train.ps1").write_text(train_ps1(character, spec["base_model"], spec["output_dir"]), newline="\r\n")
        with zipfile.ZipFile(out / f"{character['trigger']}.zip", "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    bundle.write(path, path.relative_to(out))
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec")
    parser.add_argument("--out", required=True)
    parser.add_argument("--only", action="append", help="character key; repeatable")
    parser.add_argument("--dry-run", action="store_true", help="print captions; fetch and write nothing")
    args = parser.parse_args(argv)
    spec_path = Path(args.spec)
    spec = yaml.safe_load(spec_path.read_text())
    problems = validate(spec)
    if problems:
        for problem in problems:
            print("ERROR:", problem)
        return 1
    rows = build(spec, spec_path.parent, Path(args.out), args.only, dry_run=args.dry_run)
    for key, items in rows.items():
        print(f"{key}: {len(items)} images")
        if args.dry_run:
            for n, image_id, crop, text in items:
                if image_id is None:
                    print(f"  {n:03d} PENDING render: {text}")
                    continue
                flag = (" mirrored" if image_id < 0 else "") + (f" crop {crop}" if crop else "")
                print(f"  {n:03d} ArtImage {abs(image_id)}{flag}: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
