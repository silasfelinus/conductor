# Shifting Desks / SDXL img2img pilot / actual visual verdict (2026-11-15 PT)

## Evidence and scope

- Workflow: [Shifting Desks art visual review, run 43783086752](https://github.com/silasfelinus/conductor/actions/runs/43783086752)
- Actual authenticated image bytes and source-provenance manifest: [artifact 14189401216](https://github.com/silasfelinus/conductor/actions/runs/43783086752/artifacts/14189401216), under `pilot-v3/previews/` and `pilot-v3/contact-01.jpg`.
- Input ledger: [SDXL-IMG2IMG-CORRECTION-PILOT-1.yaml](SDXL-IMG2IMG-CORRECTION-PILOT-1.yaml).
- Source rejected V2 ArtImages: 271721, 271722, 271723; produced private ArtJobs 69431, 69432, 69433 and new ArtImages 273305, 273306, 273307.
- These are *not* the production Classic image paths. No player-visible image was overwritten.

## Pixel-level verdicts

| Subject | ArtJob | ArtImage | Verdict | Objective failure |
| --- | ---: | ---: | --- | --- |
| Extra eyes in the back of a bob | 69431 | 273305 | **REDO** | Hair has no embedded eyes at all. Photographic rather than the game's painted aesthetic. |
| Three living organic doorframes | 69432 | 273306 | **REDO** | Ordinary rectangular doors and a blank central wall; no thick padded ribs or organic doorway. |
| Three-armed worker inside one tank | 69433 | 273307 | **REDO** | Only two arms. No torso-grown third hand, no orange pen held by it; waterline at lap. |

All three were inspected individually at full size and together at thumbnail size. **0 KEEP / 3 REDO**. The ledger now records these individual editorial decisions and the exact evidence artifact ID. `DONE` means the ArtJob produced an ArtImage; it never implies that the requested visual beat is there.

## Decision and next production step

The subject-only V2 pilot already failed all three relational details; the high-denoise, eight-step SDXL img2img attempt also failed all three. **Do not submit more identical prompt-only or global img2img retries.** These simple focal gags require targeted layer/mask compositing or tightly bounded inpaint regions rather than hoping a full-frame denoiser discovers extra anatomy. For each subject, prepare a credible painted base scene and the specific missing layer or isolated mask (two anatomical rear eyes; three padded living doorway throats; one independently drawn third arm holding a pen). Re-run an explicit full-scene and thumbnail KEEP/REDO check before attaching it to the production Classic target.

Remaining original task t-032: correct all 14 Classic REDO scenes or supply independent, scene-faithful alternatives, then link only KEEP via `encounters/link_art.py --write --probe` and pass the strict required Classic art gate. Keep suspended optional Western art separate. Playtest handoff and GitHub master issue #4150 remain blocked pending art and deployed-browser QA.
