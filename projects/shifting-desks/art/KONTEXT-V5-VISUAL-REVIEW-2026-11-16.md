# Shifting Desks / V5 private localized edit review / 2026-11-16 PT

## Evidence and actual acceptance

Workflow: [Shifting Desks visual review run 43842537777](https://github.com/silasfelinus/conductor/actions/runs/43842537777). Full-size source images and manifest: [artifact 14213687064](https://github.com/silasfelinus/conductor/actions/runs/43842537777/artifacts/14213687064).

| Scene | ArtJob | ArtImage | Pixel verdict | Why |
| --- | ---: | ---: | --- | --- |
| Rear eyes in bob | 69456 | 273629 | **KEEP** | Two fully open teal eyes with whites, irises, pupils and lids emerge from back of dark bob. |
| Living corridor doors | 69457 | 273630 | **KEEP** | All three archways have large swollen overlapping ribbed pink organic frames. |
| Three-arm employee in tank | 69458 | 273631 | **REDO** | Only two arms are visible. The ordinary raised hand holds the pen; third torso-grown limb is absent. |

**Verdict: 2 KEEP / 1 REDO.** Actual delivered pixel quality was checked at native resolution, independently of ArtJob `DONE` status. The upstream global Krea V4 attempt failed all three; localized Kontext V5 materially fixed two.

**Acceptance is private, not public game integration.** These are private ArtImages. Existing public Classic art target paths have NOT been updated or HEAD-verified as replaced. Do not change `ROUND-19.yaml` or the encounter packs to pretend the older public images match the new accepted pixels. The public transfer and `link_art.py --write --probe` remain real work.

## Last failure, exact SDXL-targeted plan

Target only the clerk's chest and proposed third arm. The native V5 image has its face above y=0.58 and natural right hand below y=0.80; preserving both avoids redrawing existing anatomy. Target using private ArtImage 273631 as base, with rectangle [0.36, 0.58, 0.70, 0.80], bleed 16 source pixels and inward feather 10 pixels. The new generic Kind Robots `POST /api/art/inpaint-targets` queues SDXL with a hard latent mask **and a final pixel composite** against the original, preserving source pixels outside the permitted footprint. One request only, 8 steps/CFG2 on DreamShaper Turbo. Stage in `SDXL-TARGETED-CORRECTION-PILOT-1.yaml`; `auto_submit: false` until the endpoint is merged and **deployed on Alexandria**. After rendering, inspect complete image and count three separate whole arms and hands; never accept a detached extra hand or a pen in an existing hand.

Game remains `active/high`; task t-032 and master [#4150](https://github.com/silasfelinus/kind_robots/issues/4150) remain open. Eleven additional source-referenced drafts still require targeted corrections, and only 2/14 originally rejected Classic scenes have newly accepted private candidate images.
