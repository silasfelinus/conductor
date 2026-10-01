# ACE-Step spike: model variant and Comfy workflow spec (music-video t-003)

Researched 2026-10-01 from a cloud session that could reach docs.comfy.org, huggingface.co and
raw.githubusercontent.com (the EGRESS-BLOCKERS.md caveat did not bite today). Nothing here was run:
the live proof is t-012. Items marked **UNVERIFIED** must be confirmed there.

## Decision

**Use ACE-Step 1.5 turbo (split files), not v1.** 1.5 has native ComfyUI nodes (so the "may need a
custom node" worry is closed), plans song structure with an LM, runs 8 steps at cfg 1, and handles
long songs. v1 stays as the fallback if the 12 GB card cannot hold the 1.5 stack (see e).

| | v1 (3.5B) | 1.5 turbo (**chosen**) |
|---|---|---|
| Native Comfy nodes | `TextEncodeAceStepAudio`, `EmptyAceStepLatentAudio` | `TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio` |
| Sampling | 50 steps, cfg 5, euler/simple | 8 steps, cfg 1, euler/simple |
| Length | seconds 1-1000 (node limit) | seconds 1-1000 node limit; model advertises up to ~10 min |
| License | Apache-2.0 | MIT |
| Template | `audio_ace_step_1_t2a_song` | `audio_ace_step_1_5_split` / `..._checkpoint` |

Both nodes sets exist in current ComfyUI `comfy_extras/nodes_ace.py`, which also defines
`ReferenceTimbreAudio` (reference-voice conditioning, not needed for the spike).

## (a) API-format workflow graph (1.5 turbo, split files)

Built from the official `audio_ace_step_1_5_split.json` template (same links: UNETLoader ->
ModelSamplingAuraFlow -> KSampler; DualCLIPLoader -> TextEncodeAceStepAudio1.5 -> positive and,
via ConditioningZeroOut, negative; EmptyAceStep1.5LatentAudio -> latent; VAEDecodeAudio -> save).
The template ships `SaveAudioMP3`; that node is now marked DEPRECATED in ComfyUI source, so the
graph below uses `SaveAudioAdvanced`. **UNVERIFIED**: how the API prompt encodes the
DynamicCombo (`format` plus `format.quality` below is the expected flattening); if the server
rejects it, export the real API JSON from the Comfy UI ("Save (API Format)") and paste it here.
`SaveAudioMP3` is a working fallback while it still exists (inputs: audio, filename_prefix, quality).

```json
{
  "1": {
    "class_type": "UNETLoader",
    "inputs": {
      "unet_name": "acestep_v1.5_turbo.safetensors",
      "weight_dtype": "default"
    }
  },
  "2": {
    "class_type": "DualCLIPLoader",
    "inputs": {
      "clip_name1": "qwen_0.6b_ace15.safetensors",
      "clip_name2": "qwen_1.7b_ace15.safetensors",
      "type": "ace",
      "device": "default"
    }
  },
  "3": {
    "class_type": "VAELoader",
    "inputs": {
      "vae_name": "ace_1.5_vae.safetensors"
    }
  },
  "4": {
    "class_type": "ModelSamplingAuraFlow",
    "inputs": {
      "model": [
        "1",
        0
      ],
      "shift": 3
    }
  },
  "5": {
    "class_type": "TextEncodeAceStepAudio1.5",
    "inputs": {
      "clip": [
        "2",
        0
      ],
      "tags": "<TAGS>",
      "lyrics": "<LYRICS>",
      "seed": 31,
      "bpm": 120,
      "duration": 120.0,
      "timesignature": "4",
      "language": "en",
      "keyscale": "E minor",
      "generate_audio_codes": true,
      "cfg_scale": 2.0,
      "temperature": 0.85,
      "top_p": 0.9,
      "top_k": 0,
      "min_p": 0.0
    }
  },
  "6": {
    "class_type": "ConditioningZeroOut",
    "inputs": {
      "conditioning": [
        "5",
        0
      ]
    }
  },
  "7": {
    "class_type": "EmptyAceStep1.5LatentAudio",
    "inputs": {
      "seconds": 120.0,
      "batch_size": 1
    }
  },
  "8": {
    "class_type": "KSampler",
    "inputs": {
      "model": [
        "4",
        0
      ],
      "positive": [
        "5",
        0
      ],
      "negative": [
        "6",
        0
      ],
      "latent_image": [
        "7",
        0
      ],
      "seed": 31,
      "steps": 8,
      "cfg": 1,
      "sampler_name": "euler",
      "scheduler": "simple",
      "denoise": 1
    }
  },
  "9": {
    "class_type": "VAEDecodeAudio",
    "inputs": {
      "samples": [
        "8",
        0
      ],
      "vae": [
        "3",
        0
      ]
    }
  },
  "10": {
    "class_type": "SaveAudioAdvanced",
    "inputs": {
      "audio": [
        "9",
        0
      ],
      "filename_prefix": "audio/musicvideo",
      "format": "mp3",
      "format.quality": "V0"
    }
  }
}
```

## (b) Pitch settings -> inputs

All on node 5 unless noted. Template defaults in brackets.

| Pitch setting | Input | Notes |
|---|---|---|
| Style / genre / mood / instruments | `tags` | Comma-separated or short prose; the template uses a prose paragraph beginning with the genre. |
| Lyrics | `lyrics` | Section tags in square brackets: `[Intro]`, `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`. Instrumental: use `[Instrumental]` or an empty string (**UNVERIFIED** which behaves better). |
| Duration (seconds) | `duration` on node 5 **and** `seconds` on node 7 | Must be set to the same value; the template drives both from one primitive (120). |
| Seed | `seed` on node 5 **and** `seed` on node 8 | The template links one primitive to both; set both. |
| Tempo | `bpm` [120] (10-300) | |
| Time signature | `timesignature` ["4"] | One of "2","3","4","6" (string). |
| Language | `language` ["en"] | Codes include en, zh, ja, ko, es, fr, de, ... plus "unknown". |
| Key | `keyscale` ["E minor"] | "<root> major\|minor", roots C..B including sharps and flats. |
| Quality knobs | `generate_audio_codes` [true], `cfg_scale` [2.0], `temperature` [0.85], `top_p` [0.9], `top_k` [0], `min_p` [0] | Leave defaults. Turn `generate_audio_codes` off only when feeding a reference audio. |

The server should render lyrics/tags into the two string inputs and set duration and seed in both
places, so a `Pitch` row needs: tags, lyrics, durationSeconds, seed, and optionally bpm, key,
time signature, language.

v1 mapping, if the fallback is used: `tags`, `lyrics` and `lyrics_strength` (0.99 in the
template) on `TextEncodeAceStepAudio`; `seconds` on `EmptyAceStepLatentAudio`; `seed` on KSampler;
v1 also needs `ModelSamplingSD3` (shift 5), `LatentApplyOperationCFG` with
`LatentOperationTonemapReinhard` (multiplier ~1.0; higher makes vocals more prominent) and a
`ConditioningZeroOut` negative. Non-English v1 lyrics must be romanised by hand with a `[zh]`/`[ja]`/`[ko]`
prefix per line (Comfy does not do the conversion).

## (c) Output node

Use `SaveAudioAdvanced` with `format: mp3`, quality `V0` (or `128k` to cap size). Per the brief, a
4-minute FLAC is about 47 MB of base64 inside the /complete transaction; MP3 V0 is (estimate) roughly a
quarter to a third of that, 128k about 3.8 MB (4 min x 128 kbit/s). FLAC remains available as
`format: flac` if lossless is wanted later. The audio is written under
`ComfyUI/output/audio/` and reported in the history response's `outputs[node].audio[]` (filename,
subfolder, type), fetched via `/view`.

## (d) Model files (from Comfy-Org/ace_step_1.5_ComfyUI_files)

| File | Folder under `ComfyUI/models/` | Size |
|---|---|---|
| `split_files/diffusion_models/acestep_v1.5_turbo.safetensors` | `diffusion_models/` | 4,787,825,604 B (4.46 GiB) |
| `split_files/text_encoders/qwen_0.6b_ace15.safetensors` | `text_encoders/` | 1,191,588,248 B (1.11 GiB) |
| `split_files/text_encoders/qwen_1.7b_ace15.safetensors` | `text_encoders/` | 3,708,523,360 B (3.45 GiB) |
| `split_files/vae/ace_1.5_vae.safetensors` | `vae/` | 337,431,732 B (321.8 MiB) |

Total about 9.5 GiB on disk. Alternative single file: `checkpoints/ace_step_1.5_turbo_aio.safetensors`
(10,025,478,736 B, 9.34 GiB) loaded with `CheckpointLoaderSimple` (its CLIP and VAE outputs feed
nodes 5 and 9). The repo also holds `acestep_v1.5_base`, three `xl` (about 10 GB each, bf16) diffusion
variants and a `qwen_4b_ace15` encoder (8.4 GB); **ignore them for the 12 GB card**.
v1 fallback: `Comfy-Org/ACE-Step_ComfyUI_repackaged`, `all_in_one/ace_step_v1_3.5b.safetensors` into
`checkpoints/`.

## (e) VRAM and runtime on the 12 GB card

- No measured figure was found for ComfyUI on a 12 GB card. Sources: ACE-Step 1.5 README says "less than 4GB of VRAM" (that is
  the project's own runtime with offloading, not Comfy); Comfy docs claim a 4-minute song in under 10 s on an RTX 3090
  (24 GB) and about 1 s on an RTX 5090.
- Expectation: the 4.5 GiB DiT + 3.5 GiB 1.7B encoder + 0.6 GiB encoder + VAE fit within 12 GB, and ComfyUI offloads the
  text encoders after encoding. Runtime for 3-4 minutes should be seconds to low tens of seconds once models are warm,
  plus a 30-90 s cold load. **UNVERIFIED**: t-012 must record peak VRAM and wall-clock for 60 s and 240 s.
- Risk: the LM's audio-code generation (`generate_audio_codes: true`) is the slow part; if it is too slow or OOMs,
  set it false and accept lower quality.
- Do not use the XL (10 GB bf16) variants on 12 GB.

## (f) Licence

ACE-Step v1: Apache-2.0 (HF model tag; Comfy docs say free for commercial use). ACE-Step 1.5: MIT
(HF model tag and README). The 1.5 README lists "professionally licensed music tracks" among its training data; read its data section before any commercial release. Qwen text encoders: confirm their licence (Qwen3 is Apache-2.0 upstream; the
repackaged `qwen_*_ace15` files are **UNVERIFIED**).

## (g) Minimum ComfyUI version

The nodes `TextEncodeAceStepAudio1.5`, `EmptyAceStep1.5LatentAudio` and `SaveAudioAdvanced` are in current
ComfyUI master (`comfy_extras/nodes_ace.py`, `nodes_audio.py`); master pins `comfyui-workflow-templates==0.11.73`
and a 1.53.x frontend. The 1.5 split template was authored against frontend 1.37.11. The exact first
release tag with the 1.5 nodes was not determinable (GitHub API for the ComfyUI repo is not reachable from this
sandbox). **Rule: use current master/nightly or the latest stable, then gate on
`GET /object_info/TextEncodeAceStepAudio1.5` returning 200.** Docs note stable/Desktop/Cloud lag nightly.

## Sources

- https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1-5 and .../ace-step-v1
- https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_ace.py and nodes_audio.py
- https://github.com/Comfy-Org/workflow_templates/tree/main/templates (audio_ace_step_1_5_split.json, audio_ace_step_1_5_checkpoint.json, audio_ace_step_1_t2a_song.json)
- https://huggingface.co/Comfy-Org/ace_step_1.5_ComfyUI_files (file tree, sizes)
- https://huggingface.co/ACE-Step/Ace-Step1.5 and https://huggingface.co/ACE-Step/ACE-Step-v1-3.5B (licence tags, file sizes)

## Handoff to t-012

1. Update ComfyUI; confirm the three node classes via `/object_info`.
2. Download the four split files; load the graph above (or the template) and run 60 s and 240 s.
3. Record peak VRAM, cold and warm wall-clock, output size, and whether the `SaveAudioAdvanced` API encoding above is accepted.
4. Replace every **UNVERIFIED** here with the measured value.
