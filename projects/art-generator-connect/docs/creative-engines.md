# Creative engines: Krea 2 Turbo, Flux.2 Klein, and the coloring-book upgrade

date: 2026-07-22
status: active

## Why this exists

The coloring-book **color masters** were rendering on `flux1-dev-Q8_0.gguf` at 36
steps — ~30 min/image on a 12GB card, and Flux-dev fights the house style
(soft/painterly, a "cosmic poster" attractor, and it will not hold the bold
clean ink linework these books are traced from). Three separate problems were
compounding, and only one of them was the base model:

1. **Model + speed.** Flux-dev is slow to iterate and drifts painterly. It is
   also **non-commercially licensed** — a blocker for POD/storefront output.
2. **Inert negatives + a fixed seed.** On the Flux path the KSampler `negative`
   input is wired to the same node as `positive` at cfg 1, so every "no border,
   no text" negative did nothing; and the coloring queue reused one fixed seed
   per concept, so repeated renders came back byte-identical.
3. **No coloring-specific handling.** The intended line-art converter was never
   wired in; the color-master and line-art intents were collapsed into one
   muddy prompt.

The target house style (confirmed from reference art Silas loves) is **inked
comic art**: bold clean black ink outlines with flat cel-shaded comic color, in
the tradition of European bande dessinée. The color master is the same drawing
the black-and-white coloring page is traced from.

## New engine lineup

Engine is now **selectable per job**, not hardcoded. All are wired in both the
conductor consumer (`scripts/consume_art_queue.py`) and the kind_robots enqueue
endpoint (`server/api/art/enqueue.post.ts`).

| Engine (`engine:`) | Model | Steps | License | Best for |
|---|---|---|---|---|
| `krea2` **(coloring default)** | Krea 2 Turbo (Qwen-lineage DiT) | 8 | Community (<50 seats, needs content filter) | Extreme-creativity illustration, non-photoreal |
| `flux2` / `flux2-klein` | Flux.2 Klein 4B | 4 | **Apache-2.0** | JSON structured prompts, compositional binding, cleanest commercial |
| `flux` | Flux.1 dev/schnell GGUF | 30/8 | Non-commercial (dev) | Existing project icon/card/hero lane |
| `comfy` / `sdxl` / `a1111` | SDXL + LoRAs | ~20 | Permissive | Fast exploration, biggest comic/ink LoRA ecosystem |

**Two-tier flow** falls out for free: explore cheaply on SDXL/Klein (many seeds,
seconds each), then re-render the accepted composition on Krea 2 Turbo for the
finished color master.

### Model files to download (home ComfyUI box)

Krea 2 Turbo (diffusion model is GGUF; encoder + VAE are the Comfy-Org fp8
safetensors — they load independently of the diffusion quant):
- `Krea-2-Turbo-Q5_K_S.gguf` (realrebelai/KREA-2_GGUFs) → `models/unet/`
- `qwen3vl_4b_fp8_scaled.safetensors` (Comfy-Org/Krea-2) → `models/text_encoders/`
- `qwen_image_vae.safetensors` (Comfy-Org/Krea-2) → `models/vae/`

Flux.2 Klein 4B:
- `flux-2-klein-4b-Q4_K_M.gguf` → `models/unet/`
- Flux.2 Klein text encoder (Comfy-Org Flux.2 release) → `models/text_encoders/`
- `flux2-vae.safetensors` → `models/vae/`

Comic/ink style LoRAs (for the inked look) → `models/loras/`. Use an
aesthetic/ink LoRA on the **color** stage (`lora:` on the job), and a line-art
LoRA only on the later BW-conversion stage.

> The exact filenames + CLIP `type` string are configurable constants at the top
> of each engine module. **Verify them against your download** — Krea uses
> `CLIPLoader` type `krea2`, Klein uses type `flux2`; quant/release naming
> varies. GGUF users flip the loader constant to `UnetLoaderGGUF`.

## Seed policy (the fix for identical iterations)

- **Explore:** seeds randomize every attempt. Repeated renders of a concept now
  actually differ. `-1`/unset → a concrete random seed is resolved, baked into
  the graph, and **recorded** (`render_seed` on the queue entry; `ArtImage.seed`
  is backfilled at completion from the real workflow seed).
- **Reproduce:** set `lock_seed: true` on a concept (with its recorded
  `render_seed`) once its color master is accepted, so the BW coloring page is
  traced from the exact same composition.

## Per-job knobs (conductor `color-art-jobs.yaml` / `art-generate.yaml`)

```yaml
engine: krea2            # krea2 | flux2-klein | flux | sdxl | a1111
lora: comic_inks.safetensors
lora_strength: 0.8
json_prompt:            # flux2-klein only — structured compositional prompt
  subject: curvy 1950s pinup, high-waisted swimsuit
  head: giant fly with compound eyes
  style: bold ink lineart, flat comic color
lock_seed: true         # reproduce an accepted composition
steps: 8                # optional; defaults to each engine's native cadence
```

## Re-queue with different settings (kind_robots ArtJobs UI)

The "Try again" menu now has **Adjust settings & retry** — override steps,
checkpoint/model, seed, cfg, sampler, scheduler, or negative prompt before
re-running, instead of blindly re-running the frozen payload. A blank seed uses
a fresh random seed; a filled seed reproduces an exact render.
