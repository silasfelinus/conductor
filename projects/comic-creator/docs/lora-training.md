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

## One-time setup on the box (PowerShell)

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
