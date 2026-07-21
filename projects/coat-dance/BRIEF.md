# Coat Dance — Production Brief

Task: coat-dance/t-001 · Date: 2026-07-21 · Status: draft for Silas review

One-page brief turning Silas's pitch (`roadmap.yaml` `notes_from_silas`) into a
concrete plan. Nothing here starts production — t-002 through t-009 stay
`blocked`/`waiting` until Silas answers the open questions below.

## Core premise

An experimental avant-garde duet between a performer and a black Goodwill
trench coat, originally performed live around 2006 while Silas was finishing
a dance major at Humboldt State University. The piece mixes physical theater,
object manipulation, juggling vocabulary, spins, pantomime, and deliberate
weirdness — the coat reads as a duet partner, not a prop.

The project turns the original recording into a hybrid AI-assisted music
video: the source footage is the choreographic spine, expanded section by
section with AI animation, perspective shifts, style changes, and remixed
sequences, without flattening the strange intimacy between performer and
coat into generic AI spectacle (per `roadmap.yaml`'s `creative_constraints`).

## Source asset — already in hand

`projects/coat-dance/coat dance_x264.mp4` is already checked into the
project folder (present since 2026-07-17, before this brief). The original
task note assumed Silas still needed to provide it — that assumption is
stale; the file is here. Technical read (via direct MP4 box parsing, no
`ffmpeg` available in this sandbox):

| Property | Value |
|---|---|
| Container | ISO Media / MP4 v2, `isom`/`mp42` brand |
| Video codec | H.264 (x264, per filename) |
| Resolution | 720×480 |
| Duration | ~332.0 s (5 min 32 s) |
| Audio track | present (44.1 kHz timescale) — the recording already has synced audio, not silent |
| File size | 35.5 MB |

Two `mdat` chunks appear before `moov` — consistent with a standard
non-fragmented export, not a streaming/fragmented mp4. No separate still
frames, program notes, or performance memories are in the folder yet.

## Target runtime assumptions

- **Floor:** the full ~5:32 source runtime, if the final cut follows the
  performance beat-for-beat with AI treatment layered on top.
- **Realistic target:** likely shorter for a music-video cut — 2:30–4:00 is
  a common range for a remix that trims dead air/setup and tightens pacing
  to a music track, but this directly depends on Q1 below (companion track
  vs. original audio) and needs Silas's call, not an agent guess.
- Section count (per `assets_needed`/task pipeline: beat map → sections →
  per-section renders → restitch) should follow the actual beat structure
  once t-002/t-003 map it, not a preset number chosen now.

## Required source assets

| Asset | Status |
|---|---|
| Original coat dance video file | ✅ have it (`coat dance_x264.mp4`) |
| Audio from the original performance | ✅ have it — muxed into the same file (see table above); unclear yet whether it's usable music/sound or just room audio (Q2) |
| Desired final music track or mood reference | ❌ not yet — open question (Q1) |
| Still frames / program notes / performance memories | ❌ none in the folder — optional, would help t-005's style-frame prompt pack but isn't blocking |
| Local tool inventory: ComfyUI workflows, LAX/Wan availability, GPU constraints | ❌ not documented yet — needed before t-006 (pipeline prototype), not before this brief |

## Suggested working folders

Proposed layout under `projects/coat-dance/`, created as each stage actually
produces files (not scaffolded speculatively now):

```
projects/coat-dance/
  BRIEF.md              (this file)
  coat dance_x264.mp4    (source, already present)
  source/
    stills/              extracted reference frames (t-005 onward)
    beatmap.md            (or .csv) the t-003 beat-map table
  treatment/
    section-plan.md       t-004's approved section-by-section treatment
  style/
    prompt-packs/          t-005's per-treatment prompt/negative-prompt sets
  pipeline/
    prototype-notes.md     t-006's reproducible pipeline documentation
  renders/
    section-XX/             per-section outputs as t-007/t-008 produce them
  review/
    rough-cut-notes.md      t-008 tracking doc
    final-review-package.md t-009 export/review package
```

Nothing under `source/`, `treatment/`, `style/`, `pipeline/`, `renders/`, or
`review/` is created by this task — folders appear when their first real
file lands, per the milestones' actual `not-started` state.

## Open questions for Silas

1. **Music direction.** Does the final cut use (a) the original performance's
   own audio (verified present, unclear quality/intent), (b) a new/different
   music track chosen for the remix, or (c) a blend (original audio for some
   sections, music for others)? This directly sets the target runtime and
   how t-004's section treatment paces cuts.
2. **Original audio quality/intent.** Is the audio track in the file actual
   performance sound worth preserving (voice, foley, room tone, live music),
   or is it disposable (e.g., a rehearsal room's ambient noise)? Worth a
   quick listen before t-002 starts on beat/shot segmentation.
3. **Tool inventory.** What's actually available in the target render
   environment — ComfyUI workflow set, LAX and Wan availability, GPU/VRAM
   constraints, installed video utilities (this sandbox has neither `ffmpeg`
   nor `cv2` installed; assume the real production environment is separate
   and better equipped, but that should be confirmed, not assumed, before
   t-006's pipeline prototype).
4. **Stills / program notes.** Any surviving photos, programs, or personal
   notes from the original 2006 performance that should inform tone/style
   references beyond the video itself?
5. **Runtime preference.** Full-length beat-for-beat (~5:32) vs. a tightened
   music-video cut (~2:30–4:00) — or no preference yet, decide after seeing
   the beat map?

Ends at `needs-human` per this task's `gate_human: true` — t-002 stays
`blocked` on t-001, so no further coat-dance work proceeds until Silas
answers at least Q1 (music direction) here or in the roadmap task note.
