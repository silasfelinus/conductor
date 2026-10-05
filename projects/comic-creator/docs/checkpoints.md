# Checkpoints for Zuzu, Koala Assassin

Silas, 2026-10-03: *"Illustrious/furrytoonmix_xlV3.safetensors is hands down the best model for
this project ... I love it for its cartoon expressiveness, attention to detail, and overall
emotion and character. It also just hits that good mature cartoon style that I'm wanting."*
He asked for its updates and about five lookalikes to download and compare. *"Work done finding
the right checkpoint should pay off dividends down the road."*

This page records what we found (2026-10-03, from Civitai's public API and Hugging Face) so the
search does not have to be repeated. The Kind Robots Comic Studio's **house checkpoint** setting
(Notes tab → House checkpoint) is where the winner goes. Round 4 (`issues/zuzu-koala-assassin-01/ART-ROUND-4.yaml`,
task t-018) is the bake-off.

## Decision: Arthemy Western Art v3.0 is the house checkpoint

Silas, 2026-10-04, after the round-4 bake-off: "arthemy is the winner." Round 4 compared seven Illustrious checkpoints on the same six
prompts (tier list and sheets in t-018's notes). Arthemy had the best tone, a naturally stocky Zuzu and
no frames withheld. Its author's settings are Euler a, 25 to 50 steps, CFG 3.5 to 7, and the tags
`toon (style)` and `western comics (style)`; round 4 used the Illustrious family profile instead.
FurryToonMix V3 stays available as a lane.

Silas, 2026-10-05: "Yes on house settings." The house lane now runs the author's settings (Euler a,
30 steps, CFG 5, plus the two style tags). Seven of his nine round-5 design picks came from them.

## The previous house checkpoint: FurryToonMix

- Page: https://civitai.com/models/97479 by Epitaph. Illustrious (SDXL), eps prediction. The license
  is permissive: selling images and merges is allowed.
- It merges cutefurrymix V2/V3, yiffmix, Furry Ametrine and ToonYou.
- Versions:
  - **XL-V3** (2026-05-20, ours): https://civitai.com/api/download/models/2961728
  - **XL-V3B** (2026-08-08, latest): https://civitai.com/api/download/models/3209518. Same style
    and faces as V3. The only change is slimmer, more natural female body proportions, so for a
    koala and fennec cast it is a sidegrade. It's in round 4 as a second control.
  - Older: XL-illustrious-V2 is 2178201, XL-Illustrious is 1323509.
- The author's sample settings: euler_ancestral, 40 steps, CFG 5, clip skip 2, 832×1216, then a
  1.5× hires fix with 4x-AnimeSharp. The gallery runs CFG 4–7 and 24–40 steps.
- Kind Robots renders it with the Illustrious family profile instead (`utils/checkpointProfiles.ts`:
  dpmpp_2m/karras, 20 steps, CFG 8, clip skip 2). Those are the renders Silas loves, so the house
  lane keeps the profile. Round 4's second pass tests the author settings.

## Round 4 candidates (all Illustrious/NoobAI eps: same profile, no workflow change)

| Lane | Checkpoint | Why it might match | Download | Author settings |
|---|---|---|---|---|
| nova-furry-b | Nova Furry XL v18.0 B (Crody), 2026-05-13 | The most-used furry Illustrious model (287k downloads). Very detailed fur; "B" is tuned for more expressive posing. A DARE merge of NoobAI eps 1.1, Illustrious v2.0 and ChenkinNoob | https://civitai.com/api/download/models/2943191 (civitai.com/models/503815) | Euler a, 20–50 steps, CFG 3–5 |
| nova-comic | Nova Comic XL v2.0 (Crody), 2025-11-22 | Gritty western-comic inking. Tag `western_comics_(style)` | https://civitai.com/api/download/models/2431039 (civitai.com/models/1969383) | Euler a, 20–30 steps, CFG 4–6, clip skip 1–2 |
| arthemy-western | Arthemy Western Art v3.0 | Graphic-novel and western-cartoon style, dramatic camera angles. Tags `toon (style)` and `western comics (style)` | https://civitai.com/api/download/models/2715424 (civitai.com/models/2241572) | Euler a, 25–50 steps, CFG 3.5–7, ~1024×1344 |
| anthroblend | AnthroBlend – Indigo Genesis v3.0, 2026-06-04 | Cel-shaded anthro with expressive characters and clear outlines (a merge of Indigo Furry Mix, Indigo Void, REED and Kage). Tags `flat color`, `outline` | https://civitai.com/api/download/models/3004444 (civitai.com/models/2432781) | Not stated |
| molkeun | Mol_Keun Mix DeepCobalt V2, 2026-04-24 | Anthro with strong faces and painterly, moody lighting. Leans slightly Asian in style | https://civitai.com/api/download/models/2884581 (civitai.com/models/135477) | Euler a, 20–28 steps, CFG 3–4, clip skip 2 |

File each one under ComfyUI `models/checkpoints/Illustrious/` with the names in ART-ROUND-4.yaml.
NoobAI models also go in `Illustrious/`. Kind Robots now also maps a `NoobAI/` folder to the
Illustrious profile, but keeping one folder keeps lane paths predictable.

## Alternates

- **CuteFurryMix XL v1.0**: same author as furrytoonmix, but cuter. Could suit the fennec kids.
  Download id 2771835; page civitai.com/models/51467.
- **Arthemy Toons v3.0**: id 2450328 (v4.0, 2550685, is more expressive but less consistent).
  Page civitai.com/models/1906150.
- **Nova Cartoon XL v6.0**: a general western toon look; add `furry, anthro` to the prompt.
  Id 2329740; page civitai.com/models/1570391.
- **ChrisMix Toon v1**: 2D Disney/Pixar-style toon. Id 1884639 (v2, 2424392, leans 3D).
- **Dixar 4**: a Pixar-style 3D animated-feature look. Id 2598560.
- **REED_FURRY_MiX v2.6NAi**: NoobAI, updated 2026-09-25. Id 3358722.
- **YetAnotherToonyMerge**: a **NoobAI v-pred** merge built to pull toward a western furry-toon
  look. Id 2902590 (fp8). Kind Robots' SDXL workflow has no v-pred sampling yet
  (`ModelSamplingDiscrete v_prediction`), so it needs workflow work before it can be a lane.

## Ruled out

- **Indigo Furry Mix (original), EasyFluff, Fluffyrock**: SD 1.5.
- **SeaArt Furry XL**: plain SDXL, last updated 2024.
- **Animagine XL 4**: anime, not furry.
- **DreamShaper XL**: general purpose, last updated 2024.
- **PonyRealism and any realism model**: realism drew this cast as human bodies in round 3
  (realismIllustriousBy).
- **WAI-illustrious**: anime-first, and its license forbids selling and merging.
- **BB95 Furry Mix**: not found.

Newer architectures (Anima / Cosmos-Predict2-based "Nova Furry AM" and "Indigo Furry Mix Anima",
and Chroma) are not SDXL. They need separate text encoders and VAEs and can't use SDXL LoRAs, so
they're out of scope until a LoRA plan exists.

## Caveats

- Nearly every furry and toon checkpoint's Civitai gallery is mostly NSFW, furrytoonmix's
  siblings included. Comic Studio renders are private by default, and the series negative
  carries `nsfw, nude, suggestive`. Round 4 is private.
- Civitai downloads may need an API token: append `?token=<key>` to the URL.
