# Shifting Desks | Krea 2 Turbo V4 img2img | actual visual review (2026-11-16 PT)

## Actual evidence, not ArtJob status alone

- GitHub workflow: [Shifting Desks art visual review run 43834548491](https://github.com/silasfelinus/conductor/actions/runs/43834548491).
- Authentic captured full-size `pilot-v4/previews/`, `pilot-v4/contact-01.jpg` and provenance `pilot-v4/manifest.json`: [review artifact 14210147265](https://github.com/silasfelinus/conductor/actions/runs/43834548491/artifacts/14210147265).
- Summary reports **3/3 ArtImages captured**, 0 missing or unreadable, all `DONE`. Individual originals were viewed at full native resolutions (832×1216 or 1216×832), and the contact sheet was inspected.
- The source images were rejected private V2 ArtImages 271721–271723. The V4 output remains private; no public Classic target or active game image was changed.

| Subject | ArtJob | ArtImage | Result | Visible evidence and failure |
| --- | ---: | ---: | --- | --- |
| Eyes in back of bob | 69448 | 273605 | **REDO** | Smooth black back of hair, **zero anatomical rear eyes**, no sclera, iris or lids. |
| Living hallway doors | 69449 | 273606 | **REDO** | Three ordinary doorways with thin smooth pink frames, **zero swollen ribbed organic throats**. |
| Extra arm in tank | 69450 | 273607 | **REDO** | Green-filled glass tank and orange pen are present, but the employee has **only two arms**. The raised natural arm holds the pen; there is no additional torso-grown limb. |

**Score: 0 KEEP / 3 REDO.** The painted mid-century aesthetic and basic framing are considerably closer to target than the SDXL attempt, but appearance is not the objective acceptance criterion. The unique impossible action/detail has still not appeared.

## Next editing procedure

Do not repeat whole-frame Krea 2 or SDXL img2img with only a longer prompt. The two global approaches have now both failed all three cases, even when the base compositions were retained.

Use **localized mask-guided inpainting or authored compositing** to lock the good pixels and force the missing visual beats:

1. **Rear eyes:** define two clear oval mask regions in the mid-back bob hair, preserving the surrounding hair and silhouette; insert two complete forward-looking eyes with sclera, iris, pupil, and upper/lower lids.
2. **Living doors:** individually mask the three doorframe boundaries without repainting walls and floor; replace smooth thin trims with thick overlapping raised rose-colored padded throat ribs.
3. **Third arm:** preserve both existing natural arms and the tank; mask a distinct torso-to-hand region to create a third full limb, ensuring the extra hand itself holds the orange pen. The current natural-hand pen must not be misread as the requested extra-hand pen.

Any edited render requires a new private ArtJob/ArtImage provenance record, a full-size + thumbnail KEEP/REDO check, and an explicit decision before `encounters/link_art.py --write --probe` or any production target changes. Do not invent a KEEP from a `DONE` status.

The separate eleven-scene [source-referenced correction draft](KREA-IMG2IMG-CORRECTION-PILOT-2.yaml) also stays `auto_submit: false`, now explicitly staged for localized rather than global editing. All fourteen original Round 19 Classic REDOs remain outstanding, and browser human-trial QA remains unverified. Master roadmap [#4150](https://github.com/silasfelinus/kind_robots/issues/4150) stays open, lifecycle active/high.
