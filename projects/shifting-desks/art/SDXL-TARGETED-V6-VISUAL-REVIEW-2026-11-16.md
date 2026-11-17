# Shifting Desks / V6 targeted SDXL private art review / 2026-11-16 PT

## Authenticated actual-image evidence

- Generation: [Auto Art Generate 44004142755](https://github.com/silasfelinus/conductor/actions/runs/44004142755), completed success. ArtJob **69681** delivered private ArtImage **274183** (832×1248).
- Full-size pixel review: [workflow 44006541795](https://github.com/silasfelinus/conductor/actions/runs/44006541795), [evidence ZIP 14293774749](https://github.com/silasfelinus/conductor/actions/runs/44006541795/artifacts/14293774749). The actual authenticated rendered image is `pilot-v6/previews/001-three-arm-tank--sdxl-targeted-local.jpg`; the full prompt, source and region metadata live in `pilot-v6/manifest.json`.
- Baseline: private V5 source ArtImage **273631** (ArtJob **69458**), in the same evidence ZIP at `pilot-v5/previews/003-three-arm-tank--kontext-localized.jpg`.
- Edit region: normalized box **[0.36, 0.58, 0.70, 0.80]**, bleed 16 px, feather 10 px, DreamShaper XL Turbo, 8 steps, CFG 2, denoise 0.72.

## V6 verdict: REDO

The resulting image still has **exactly two** visible, shoulder-attached arms: the left is raised with the orange pen, the right rests across the tank floor. **No independently connected third arm, elbow, wrist, or third hand appears.** It fails the ledger's explicit acceptance contract.

Side-by-side native-size JPG review of baseline and result (both 832×1248) showed essentially the same composition. The mean per-channel absolute difference between the two saved previews is **1.29 on a 0–255 scale**, and just **0.0055%** of pixels differ by over 15 on any channel; the very small changes may simply be a consequence of JPEG re-encoding. This does **not** establish the exact underlying ComfyUI failure mode. It *does* establish that the attempted anatomical edit did not happen visually.

**Decision:** keep ArtImage 274183 **private/REDO**. Do not map it to a public Classic target, run `link_art.py` for it, or resubmit an identical SDXL request. Investigate the mask/latent/compositing result and verify the output actually diverges in the permitted edit footprint before another candidate is considered. An explicit illustrated third-arm compositing layer may be more reliable than repeating this generative prompt.

V5's unrelated **rear-eyes** (273629) and **living-doors** (273630) remain independently accepted **KEEP** privately. Public delivery and the other Classic REDO gaps remain unfinished. The roadmap task **t-032** and [master #4150](https://github.com/silasfelinus/kind_robots/issues/4150) stay open; Shifting Desks is **not** flagged ready for human playtests.
