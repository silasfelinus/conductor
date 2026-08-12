# Coat Dance — Source-Video Beat Map Template

Task: coat-dance/t-003 · Date: 2026-08-12 · Status: template, not yet populated

This is the reusable table format t-003 asked for — the shape every future
beat-map pass fills in, not a produced beat map itself. Per t-002's research
(`RESEARCH-t002-beat-transcription-tools.md`) and its own caveat, this
sandbox has neither `ffmpeg` nor a Python audio/video stack, so nothing here
has run against `coat dance_x264.mp4` yet. Populating the rows below is
real, separate work — either a future task with that tooling available, or
a manual pass — not something this template does for you.

## How this gets filled in

Follow RESEARCH-t002-beat-transcription-tools.md §4's suggested pipeline
order:

1. Extract the audio track (`ffmpeg`).
2. Run `librosa.beat.beat_track` + `onset_detect` on the audio → candidate
   beat/onset timestamps (fall back to `madmom`'s DBN tracker if the beat
   grid comes out unstable on this specific 2006 live-room recording).
3. Run MediaPipe Pose over the video → per-frame keypoints → performer
   movement-peak timestamps.
4. Run dense optical flow (OpenCV Farneback, or a ComfyUI optical-flow
   node) over the video → frame-to-frame motion magnitude → flags spikes
   pose tracking alone would miss, which is how the *coat's* movement gets
   captured (it has no skeleton to key on).
5. Merge the candidate timestamps from (2)+(3)+(4) into rows below, one row
   per beat/section. Boundaries don't have to land on a single tool's
   output — a beat can be "where 2+ signals agree" as much as "where any
   one signal fires."
6. A human pass (Silas, or a later task) reviews and annotates before
   t-004 treats each section — the tool outputs above populate the first
   five columns; **Candidate AI Treatment**, **Generation Method**, and
   **Restitch Notes** are creative/production calls, not something the
   detection tools produce on their own.

Only reach for shot/scene-change detection (ffmpeg `scdet` / PySceneDetect)
if the eventual edit introduces actual cutaways — the source is a single
continuous take, so this table doesn't reserve a column for shot changes by
default.

## Column definitions

| Column | What goes here |
|---|---|
| **Timestamp Range** | `MM:SS–MM:SS` (or `HH:MM:SS` if ever needed), start inclusive / end exclusive, no gaps or overlaps across the full ~5:32 runtime once the table is complete. |
| **Movement/Action** | What the performer is doing — plain description, not interpretation (e.g. "spins twice, coat trailing outward", not "conveys freedom"). |
| **Coat Behavior** | What the coat itself is doing, tracked as its own duet partner per `roadmap.yaml`'s `creative_constraints` — worn, thrown, dragged, held at arm's length, animated by momentum alone, etc. Leave blank only if the coat is genuinely static/off-frame for that beat, not by default. |
| **Camera/Framing** | Shot scale and camera behavior as recorded in the source (wide/medium/close, static/handheld/pan) — this is about the *original 2006 footage*, informing how much an AI treatment can plausibly reframe vs. must respect. |
| **Emotional Tone** | The beat's felt quality (frantic, tender, absurd, still, menacing, playful...) — grounds t-004's section-by-section treatment in the actual performance rather than generic mood guesses. |
| **Candidate AI Treatment** | A first-pass idea for the AI-assisted expansion of this beat (style shift, perspective change, animated extension, ghosting/duplication, etc.) — proposal, not commitment; t-004 owns the approved treatment. |
| **Generation Method** | Which tool/pipeline the candidate treatment implies (ComfyUI workflow name, LAX, Wan, vid2vid, optical-flow-guided interpolation, etc.), once t-006 has confirmed what's actually available in the render environment (BRIEF.md Q3). Leave blank until that's resolved rather than guessing a tool that may not be installed. |
| **Restitch Notes** | Anything this beat needs to cut cleanly against its neighbors after per-section rendering — matching motion/energy at the boundary, audio sync points that must not drift, a held frame to bridge sections, etc. |

## Beat map

| # | Timestamp Range | Movement/Action | Coat Behavior | Camera/Framing | Emotional Tone | Candidate AI Treatment | Generation Method | Restitch Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 00:00–?? | _pending tool run_ | | | | | | |

Rows are added/split as the detection pipeline (or a manual scrub) actually
produces timestamps — this template intentionally ships with one open
placeholder row rather than a preset section count, per BRIEF.md's note
that section count should follow the real beat structure, not a guess made
now.

## Format note

This file is the canonical version. If a CSV export is ever more convenient
for a script (e.g. t-006's pipeline prototype reading rows programmatically),
regenerate one from this table rather than hand-maintaining two copies —
this Markdown table stays the source of truth for human review.
