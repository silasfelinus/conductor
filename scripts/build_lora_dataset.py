#!/usr/bin/env python3
"""Build kohya sd-scripts LoRA datasets from locked Comic Studio cast renders (comic-creator t-016).

A spec YAML names each character's trigger word, class word, identity tags and images (Kind Robots
ArtImage ids). For every character this writes, under ``--out``:

    <trigger>/img/<repeats>_<trigger> <class>/NNN.png   the training images
    <trigger>/img/<repeats>_<trigger> <class>/NNN.txt   one caption per image, trigger word first
    <trigger>/dataset.toml                               kohya dataset config (buckets, captions)
    <trigger>/train.ps1                                  SDXL LoRA run for a 12 GB card
    <trigger>.zip                                        the folder above, ready to copy to the box
    train_all.ps1                                        one paste on the box: setup + every set, overnight

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
# image_dir in dataset.toml is relative to this folder, but kohya resolves it against the working directory (the
# sd-scripts checkout). Write a copy with the absolute path (2026-10-09: the relative one found no images).
$abs = ($here -replace "\\\\", "/") + "/img/"
(Get-Content "$here\\dataset.toml") -replace "image_dir = 'img/", "image_dir = '$abs" | Set-Content "$here\\dataset.abs.toml"
Set-Location $SdScripts
& .\\venv\\Scripts\\accelerate.exe launch --num_cpu_threads_per_process 1 sdxl_train_network.py `
  --pretrained_model_name_or_path "$Model" `
  --dataset_config "$here\\dataset.abs.toml" `
  --output_dir "$Out" --output_name "{name}" --save_model_as safetensors `
  --network_module networks.lora --network_dim 16 --network_alpha 8 `
  --network_train_unet_only --cache_text_encoder_outputs `
  --learning_rate 1e-4 --optimizer_type AdamW8bit `
  --lr_scheduler cosine --lr_warmup_steps 50 `
  --max_train_epochs {epochs} --save_every_n_epochs 2 --train_batch_size 1 `
  --mixed_precision fp16 --save_precision fp16 `
  --gradient_checkpointing --cache_latents --cache_latents_to_disk --sdpa `
  --max_data_loader_n_workers 1 --seed 42
if ($LASTEXITCODE) {{ exit $LASTEXITCODE }}
# kohya exits 0 on "No data found", so a run that wrote no LoRA is a failure too.
if (-not (Test-Path "$Out\\{name}.safetensors")) {{ Write-Host "No {name}.safetensors was written; see the log above"; exit 2 }}
Write-Host "Done: $Out\\{name}.safetensors (every 2 epochs also saved as {name}-0000NN)"
"""


def train_all_ps1(triggers):
    """One script that trains every set in turn, so Silas's part is a single overnight paste.

    It sets sd-scripts up the first time, pauses the art relay and empties ComfyUI's VRAM so training has the
    card, unzips and trains each set, and always restarts the relay at the end, even after a failure.
    """
    names = ", ".join(f'"{t}"' for t in triggers)
    return f"""# Train every Zuzu character LoRA in one go (comic-creator t-016). Put this file next to the zips, then:
#   powershell -ExecutionPolicy Bypass -File D:\\ai\\lora-sets\\train_all.ps1
# First run installs kohya sd-scripts into -SdScripts. The art relay (pm2 kr-relay) is paused while training holds
# the card and restarted at the end, even on failure. A set whose .safetensors already exists in the import folder is
# skipped, so a re-run picks up where a stopped one left off. Log: train-all.log next to this file.
param(
  [string]$SdScripts = "D:\\ai\\sd-scripts",
  [string]$Comfy = "http://127.0.0.1:8188",
  [string]$ComfyDir = "D:\\comfy\\comfy-fast",
  [string]$Out = "D:\\comfy\\comfy-fast\\models\\Lora\\import",
  [string[]]$Only = @(),
  # The base Python ComfyUI runs on (ops/home-server/ecosystem.config.js COMFY_BASE_PYTHON). A bare "python" on this
  # box is a broken Store alias, so it is only the fallback.
  [string]$Python = "$env:LOCALAPPDATA\\Programs\\Python\\Python310\\python.exe"
)
$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$AccelerateConfig = "$env:USERPROFILE\\.cache\\huggingface\\accelerate\\default_config.yaml"
$triggers = @({names})
if ($Only.Count) {{ $triggers = $triggers | Where-Object {{ $Only -contains $_ }} }}
Start-Transcript -Path "$here\\train-all.log" -Append | Out-Null

if (-not (Test-Path "$SdScripts\\venv\\Scripts\\accelerate.exe")) {{
  Write-Host "Setting up kohya sd-scripts in $SdScripts (one time, ~10 min)"
  if (-not (Test-Path $SdScripts)) {{ git clone https://github.com/kohya-ss/sd-scripts.git $SdScripts }}
  Push-Location $SdScripts
  if (-not (Test-Path $Python)) {{ $Python = "python" }}
  & $Python -m venv venv
  if ($LASTEXITCODE) {{ throw "venv creation failed" }}
  & .\\venv\\Scripts\\python.exe -m pip install -r requirements.txt bitsandbytes
  if ($LASTEXITCODE) {{ throw "pip install -r requirements.txt failed" }}
  # requirements.txt pulls torch from PyPI, which on Windows is CPU-only. Replace it with the exact CUDA build
  # ComfyUI already runs on this card (2026-10-09: the cu124 index alone failed on typing_extensions, and the CPU
  # torch then crashed on a missing torchvision).
  $tv, $vv = (& "$ComfyDir\\venv\\Scripts\\python.exe" -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)").Split(" ")
  $cu = $tv.Split("+")[1]
  & .\\venv\\Scripts\\python.exe -m pip install --force-reinstall --no-deps "torch==$tv" "torchvision==$vv" --index-url "https://download.pytorch.org/whl/$cu"
  if ($LASTEXITCODE) {{ throw "CUDA torch $tv install failed" }}
  Remove-Item $AccelerateConfig -ErrorAction SilentlyContinue  # "config default" never overwrites an old one
  & .\\venv\\Scripts\\accelerate.exe config default --mixed_precision fp16
  Pop-Location
}}
& "$SdScripts\\venv\\Scripts\\python.exe" -c "import torch, torchvision, sys; sys.exit(0 if torch.cuda.is_available() else 1)"
if ($LASTEXITCODE) {{ throw "sd-scripts venv has no CUDA torch/torchvision; see docs/lora-training.md" }}
# A config written while torch was CPU-only pins accelerate to the CPU (2026-10-10: 8 hours for 1 of 17 latents).
if ((Test-Path $AccelerateConfig) -and (Select-String -Path $AccelerateConfig -Pattern "use_cpu: true" -Quiet)) {{
  Write-Host "accelerate config pins the CPU; regenerating it for the GPU"
  Remove-Item $AccelerateConfig
  & "$SdScripts\\venv\\Scripts\\accelerate.exe" config default --mixed_precision fp16
}}

pm2 stop kr-relay | Out-Null
try {{
  $waited = 0
  while ($true) {{
    try {{ $q = Invoke-RestMethod "$Comfy/queue" -TimeoutSec 10 }} catch {{ break }}
    if (($q.queue_running.Count + $q.queue_pending.Count) -eq 0) {{ break }}
    if ($waited -eq 0) {{ Write-Host "ComfyUI is finishing a job; waiting before taking the card" }}
    Start-Sleep -Seconds 30; $waited += 30
  }}
  try {{ Invoke-RestMethod "$Comfy/free" -Method Post -ContentType "application/json" `
      -Body '{{"unload_models": true, "free_memory": true}}' -TimeoutSec 30 | Out-Null }} catch {{ }}
  foreach ($t in $triggers) {{
    if (Test-Path "$Out\\$($t)_v1.safetensors") {{ Write-Host "$t already trained; skipping"; continue }}
    if (-not (Test-Path "$here\\$t\\train.ps1")) {{ Expand-Archive -Path "$here\\$t.zip" -DestinationPath $here -Force }}
    Write-Host "=== $t  $(Get-Date -Format s)"
    & "$here\\$t\\train.ps1" -SdScripts $SdScripts -Out $Out
    if ($LASTEXITCODE) {{ throw "$t training failed (exit $LASTEXITCODE); see train-all.log" }}
  }}
  Write-Host "All done $(Get-Date -Format s). The LoRA import agent registers the files in Kind Robots."
}} finally {{
  pm2 start kr-relay | Out-Null
  Stop-Transcript | Out-Null
}}
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
    ledgers, written, triggers = {}, {}, []
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
        triggers.append(character["trigger"])
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
    if triggers and not dry_run:
        (out / "train_all.ps1").write_text(train_all_ps1(triggers), newline="\r\n")
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
