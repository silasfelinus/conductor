# Character LoRAs for Zuzu, Koala Assassin (t-016)

Silas, 2026-10-07: *"go ahead with the LoRA sets"*. The trainer is **kohya sd-scripts**, run on the render box (Ferngrotto,
12 GB card). Neither Conductor nor Kind Robots trains LoRAs. `lora-ingestion` only registers finished `.safetensors`
files, and `model-builder` is a record builder. So agents build the datasets and Silas runs the training.

## What an agent builds

```
python scripts/build_lora_dataset.py projects/comic-creator/issues/zuzu-koala-assassin-01/LORA-SETS.yaml --out <dir>
```

This produces one folder and one zip per character. The triggers are `zuzukoala`, `zkasister`, `zkatoddler`, `zkacoyote`
and `zkaabbess`. Each folder holds:

- `img/10_<trigger> <class>/`: the images, each with a `.txt` caption that starts with the trigger word;
- `dataset.toml`: buckets on, resolution 1024;
- `train.ps1`: an SDXL LoRA run sized for 12 GB. It trains the U-Net only, caches latents and text-encoder outputs, and
  uses gradient checkpointing, AdamW8bit, dim 16 / alpha 8, learning rate 1e-4 and 10 epochs, saving every 2.

Each set is about 17 images, or 19 for the coyote:

- the 8 locked angles from CAST-PICKS.md, where a negative id means the image is mirrored;
- 3 upper-body crops of the front views;
- 6 expressions from LORA-EXPRESSIONS.yaml;
- for the coyote only, both stump states, tagged `missing right hand`, so a prompt can choose the hand or the stump.

Base model: Arthemy Western Art v3 (`Illustrious/arthemyWesternArt_v30.safetensors`), the house lane.

## The short way: one paste, overnight

Silas, 2026-10-08: *"am i needed to run a lora training?"* Yes, once. No agent can reach a trainer: the box agents only
run ComfyUI jobs and register finished LoRAs. The build also writes `train_all.ps1`, which cuts his part to one paste.

1. Copy the five zips and `train_all.ps1` into `D:\ai\lora-sets\`.
2. Run `powershell -ExecutionPolicy Bypass -File D:\ai\lora-sets\train_all.ps1`.

The script:
- installs sd-scripts the first time (the setup below, done for you);
- pauses the art relay (`pm2 stop kr-relay`), waits for ComfyUI to finish its current job and frees its VRAM;
- unzips and trains each set in turn, stopping on the first failure;
- always restarts the relay at the end, even after a failure.

Expect 6–10 hours for all five. A set whose `<trigger>_v1.safetensors` is already in the import folder is skipped, so
running it again resumes where it stopped. `-Only zkacoyote` trains a single set. The log is `train-all.log` next to it.

### If training stops on "No module named 'torchvision'" or "no CUDA torch"

First run on Ferngrotto, 2026-10-09: `requirements.txt` installs torch from PyPI, which on Windows is the CPU-only build
without torchvision. `train_all.ps1` now replaces it with ComfyUI's own CUDA build during setup. To repair a venv
created before that change, copy ComfyUI's build into it:

```powershell
$tv, $vv = (& D:\comfy\comfy-fast\venv\Scripts\python.exe -c "import torch, torchvision; print(torch.__version__, torchvision.__version__)").Split(" ")
D:\ai\sd-scripts\venv\Scripts\python.exe -m pip install --force-reinstall --no-deps "torch==$tv" "torchvision==$vv" --index-url "https://download.pytorch.org/whl/$($tv.Split('+')[1])"
D:\ai\sd-scripts\venv\Scripts\python.exe -c "import torch, torchvision; print(torch.__version__, torch.cuda.is_available())"
```

The last line must print `True`. Then run `train_all.ps1` again.

### If every set logs "No data found" in a few seconds

Also from 2026-10-09. kohya resolves `image_dir` against its working directory (the sd-scripts checkout), not the
folder `dataset.toml` sits in, so the relative `img/...` path found nothing. kohya exits 0 when this happens.
`train.ps1` now writes `dataset.abs.toml` with the full path, and fails when no `.safetensors` was written. To fix
sets unzipped before that change, rewrite each `dataset.toml` in place:

```powershell
Get-ChildItem D:\ai\lora-sets -Directory | ForEach-Object {
  $toml = Join-Path $_.FullName 'dataset.toml'
  $abs  = ($_.FullName -replace '\\','/') + '/img/'
  (Get-Content $toml) -replace "image_dir = 'img/", "image_dir = '$abs" | Set-Content $toml
}
```

### If the log says `accelerator device: cpu`

From 2026-10-10. `accelerate config default` had run while the venv still had CPU torch, so it saved a config with
`use_cpu: true`, and it never overwrites that file. Training then crawled on the CPU: 8 hours for 1 of 17 latents.
`train_all.ps1` now regenerates a CPU-pinned config before training. To fix it by hand:

```powershell
Remove-Item "$env:USERPROFILE\.cache\huggingface\accelerate\default_config.yaml"
D:\ai\sd-scripts\venv\Scripts\accelerate.exe config default --mixed_precision fp16
```

A healthy run logs `accelerator device: cuda` and caches all latents in under a minute.

## One-time setup on the box (PowerShell)

`train_all.ps1` does this itself; it is here for a manual install.

```powershell
cd D:\ai
git clone https://github.com/kohya-ss/sd-scripts.git
cd sd-scripts
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
pip install bitsandbytes
accelerate config   # this machine, no distributed training, fp16
```

## Training one character

1. Unzip `<trigger>.zip` anywhere, for example `D:\ai\lora-sets\`.
2. Run `powershell -ExecutionPolicy Bypass -File D:\ai\lora-sets\<trigger>\train.ps1`.
   - It defaults to `-SdScripts D:\ai\sd-scripts`.
   - It writes `<trigger>_v1.safetensors` to `D:\comfy\comfy-fast\models\Lora\import`, where the import agent
     (`ops/home-server/lora_import_agent.py`) sorts it and registers it in Kind Robots.
3. Run one character at a time while the art queue is quiet, because training takes the whole card.
   - Each set is about 170 steps per epoch, so about 1,700 steps in all.
   - Expect roughly 1–2 hours per character on 12 GB.

## Testing

Prompt the house lane with the trigger word and the identity tags at LoRA weight 0.7–0.9. Then compare against
the locked sheet (the facing convention, the eyepatch and holster on the coyote's right side, Zuzu's single
katana). If the character comes out too stiff, try an earlier epoch file (`-000006`, `-000008`).

## Results (2026-10-11)

All five trained on Ferngrotto: about 1 hour each on the 12 GB card, at 2.1 s/step. All are registered as private
Kind Robots resources. The final epoch is the pick for every character, and four of the five hold their locked
design. The coyote's LoRA ignores his stump: only 2 of his 19 images had it. Ids, verdicts and the stump workaround
are in `issues/zuzu-koala-assassin-01/CAST-PICKS.md`. Test renders are in `LORA-TEST.yaml`.

To use one in an art ledger, add `loras: [{resource_id: 4593, strength: 0.8}]` to a lane or subject, and put the
trigger word in the prompt. `/api/art/enqueue` resolves the file.

## The default for Zuzu art (2026-10-11)

Silas: the character LoRAs are the default for every project that uses the series' art: the comic, the music videos
(intro and trailer), the comic-film, the gamebook and Shifting Lands. Not the pinball, the fighting game or the 2D
game, which have their own stylized looks.

| Path | Projects | Where the list lives |
| --- | --- | --- |
| Kind Robots comic lanes | Comic Studio, music videos, comic-film | `castLoras` on the Zuzu series' Arthemy lane (kind_robots `utils/comicLanes.ts`) |
| Conductor art ledgers | comic issue ledgers, gamebook, Shifting Lands | `projects/comic-creator/cast-loras/zuzu-koala-assassin.yaml`, read by `scripts/enqueue_art_requests.py` for any ledger with `series: zuzu-koala-assassin` |

A LoRA rides only on renders whose own prompt names its character, by trigger or match word. One character gets
0.8; two or more get 0.6 each, except that Zuzu and the abbess are `stacks: false`. The gamebook's ROUND-12 test
(2026-10-11) found that Zuzu fuses with any second LoRA (two koalas, his hat on the fennec) and that the abbess gets a
human face beside anyone. A render naming either of them with another character therefore gets no default LoRAs; give
it an explicit list, or keep the frame to one figure. A ledger opts out with `cast_loras: false`, and an explicit `loras:` wins. When a LoRA
is retrained, update both lists.
