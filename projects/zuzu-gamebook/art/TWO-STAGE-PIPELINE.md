# Krea 2 composition → Arthemy house-style pipeline (Zuzu book)

## Why this exists
The Round 16 Arthemy txt2img jobs all delivered real images but none pictured its prose.
The new two-stage pipeline separates scene truth (Krea 2) from western-comic finish (Arthemy).
Only the first stage auto-submits. The second is **prohibited until the real Krea pixels are reviewed**.

## Stage 1: active compositions
`ROUND-18-KREA-COMPOSITION.yaml` has `auto_submit: true` and nine private Krea 2 jobs:
three for `a2-bell-view` (foreground bell, overlook, distant tower, tiny tracks);
three for `a2-gift` (full hanging waterskin, one nail, wooden post, tiny scratched mask mark);
three for `a4-bloom` (dense yellow/white/violet wildflowers in damp desert soil).
The normal `auto-art-generate.yml` sweep queues cells with durable `jobs.krea-composition` IDs,
then records `art.krea-composition.status` and `art_image_id`. Do not mistake a queued
job for a completed image.

Krea 2 supports the `engine: krea2`, `prompt: prose` path of `enqueue_art_requests.py`.
That code does **not** forward a negativePrompt for Krea 2; subject framing must therefore be
clear in the *positive* prose, not depend upon negative terms.

## Review composition results
The `Zuzu Two-Stage Art Delivery Checks` workflow validates completed private ArtImages
and uploads **metadata receipts only**. Its private contact sheet lives on the
ephemeral runner and is **never published as a downloadable public GitHub artifact**.
Inspect the rendered ArtImage IDs from the ledger in the authenticated Kind Robots gallery.
Use the verified hashes from the metadata receipt to fill `ROUND-18-SELECTIONS.yaml`.

Each scene requires 0–2 scoring on: scene truth, composition, required objects, emphasis.
Total must be at least **7/8** AND every critical item must be `true`; a missing bell,
nail, carved mark, track line, or flower carpet vetoes promotion, regardless of aesthetics.
Record an image-specific observation in `notes`, not the template instructions.
If no Krea candidate passes, leave selection empty and reroll **only that composition**.
Never invent a passing assessment to unlock Arthemy.

## Stage 2: gated Arthemy img2img
`ROUND-19-ARTHEMY-STYLEPASS.yaml` starts with `auto_submit: false` and no subjects.
After **all three scenes** have passing Krea choices, run:

```bash
python scripts/activate_zuzu_gamebook_stylepass.py \
  --receipt /secure/path/krea-receipt.json
```

The activator confirms:
- each selected key exists in Round 18 and its ArtJob is DONE with a real ArtImage;
- the receipt lists that exact job, image ID, seed, and SHA-256 from authenticated delivery;
- the scoring is ≥7/8 and every scene-specific veto passes;
- Stage 19 is still empty/dormant, preventing accidental duplicate submissions.

The output is the existing Stage 19 YAML now containing **six** separate jobs, two per
chosen Krea source: **0.28 denoise** safe and **0.43** bolder. Engine is
`sdxl-img2img`, checkpoint `Illustrious/arthemyWesternArt_v30.safetensors`,
steps 30, CFG 5. The internal API fetches private source images by `source_image_id`
using `KR_API_TOKEN` and sends their bytes as `sourceImageBase64`.
Open a scoped PR for the activated ledger; merge only after checks pass.
Conductor's auto-submit sweep will enqueue the six new cells exactly once.

## Final gate
Verify all six ArtJob IDs and private rendered images. Compare safe/bold candidates to
Krea originals, *reject* any losing the bell, waterskin, scratched mark, or flowers.
Only then export accepted WebPs into `kind_robots/public/zuzu-gamebook/scenes`,
update section plate manifests and Zuzu media registry, test, and replace temporary SVGs
and the erroneous raccoon-head art. Keep task `zuzu-gamebook/t-006` ready until delivery.
Public-facing publication requires its normal human gate.
