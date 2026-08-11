# Coat Dance — Beat Transcription & Shot-Slicing Tool Research (t-002)

Task: coat-dance/t-002 · Date: 2026-07-29 · Status: draft for Silas review

Per `BRIEF.md`: the source is `coat dance_x264.mp4` (720×480, ~5:32, H.264,
with synced original performance audio confirmed load-bearing per Q1/Q2 —
no replacement track). This task surveys practical tools for segmenting
that footage by movement beats, shot changes, audio events, and
pose/action changes, to feed t-003's actual beat map.

Sandbox caveat: neither `ffmpeg` nor `cv2` is installed in this conductor
sandbox (confirmed in `BRIEF.md`), so nothing below was run against the
real file — this is tool selection, not a produced beat map. Confirm the
target render environment has (or can install) the picks below before
t-003/t-006.

## 1. Shot / scene-change detection (visual cuts)

The source is a single continuous performance take, so hard "shot changes"
are unlikely — this category matters more if the AI-treatment edit later
splices in cutaways or alternate angles. Still worth having in the toolkit
for t-006's pipeline.

| Tool | Approach | Notes |
|---|---|---|
| **PySceneDetect** (0.7, released 2026-05-03) | Content-aware (frame-difference) + adaptive detectors, Python API + CLI | The practical default: one-command `detect-content`/`detect-adaptive`, splits directly to per-scene clips, has a stable Python API to call from a pipeline script rather than shelling out. Known limitation: frame-difference approach struggles with gradual transitions/fades — unlikely to matter for a single continuous take. |
| **ffmpeg `scdet`/`select` filters** | Metadata-based scene-score threshold (`scdet`) or manual `select='gt(scene,0.4)'` | Already assumed available in the real render environment (BRIEF.md Q3). Lower-level than PySceneDetect but combines scene detection with transcoding/frame extraction in one pass — good for a lightweight first grep before reaching for PySceneDetect's fuller pipeline. |
| **ffmpeg `blackdetect`** | Flags black frames | Useful narrowly if the source has any black-frame slates/leaders at start/end (worth a quick manual scrub instead of tooling, given only one file). |

**Recommendation:** ffmpeg `scdet` as a cheap first pass (likely near-empty
result on a single continuous take, which itself is a useful confirmation);
keep PySceneDetect in the toolkit for if/when the treatment introduces
cut-in material.

## 2. Audio beat/onset detection (music/beat structure)

This is the core of t-003's beat map, since Silas confirmed the original
performance audio is load-bearing and stays as-is.

| Tool | Approach | Notes |
|---|---|---|
| **librosa** | `librosa.beat.beat_track` (dynamic-programming beat tracker) + `onset.onset_detect` | Best starting point: mature, well-documented, pure-Python-friendly install, general-purpose feature extraction (tempo, chroma, onset envelope) beyond just beats — useful if the "very specific audio" turns out to be non-metronomic (spoken word, foley, sparse percussion) rather than a clean 4/4 track, since librosa's onset-envelope tools work even when a beat-tracker's periodicity assumption doesn't hold. |
| **madmom** | Neural-network + HMM-based beat/downbeat tracking (`DBNBeatTrackingProcessor`, `RNNDownBeatProcessor`) | State-of-the-art accuracy for tempo/downbeat tracking on musical audio, but heavier dependency footprint and geared to offline batch processing (fits this use case fine — this is an offline edit, not live performance). Worth reaching for if librosa's beat track is noisy on this specific recording (plausible, given it's 2006 live-performance room audio, not a studio mix). |
| **BeatNet** | Real-time joint beat/downbeat/meter tracking | Optimized for live use; no advantage here over madmom for an offline single-file job — lower priority than the two above. |

**Recommendation:** run `librosa.beat.beat_track` + `onset_detect` first
(fast, good default); fall back to `madmom`'s DBN beat tracker if the
source audio is irregular enough (spoken cues, sparse hits, tempo drift
across a 5:32 live take) that librosa's periodicity assumption produces an
unstable beat grid. Both are Python, so either slots into the same t-006
pipeline-prototype step without a language/runtime mismatch.

## 3. Movement / pose / action-change detection

This is the most distinctive need for Coat Dance specifically — the
"duet" is a performer *and* a coat (an inanimate object being manipulated,
thrown, worn as a second body), so movement segmentation can't rely purely
on human-pose keypoints; the coat itself carries as much
choreographic information as the performer's joints.

| Tool | Approach | Notes |
|---|---|---|
| **MediaPipe Pose** | 33-landmark single-person pose estimation, real-time-capable | Simplest to stand up, good single-performer accuracy. Confirmed limitation: unreliable multi-person tracking — irrelevant here (one performer), but it also only tracks the *human* body, not the coat, so it captures half the duet. Good first pass for performer-only beat/pose keyframes. |
| **OpenPose** | 18-keypoint multi-person, Part Affinity Fields | Heavier to deploy than MediaPipe for a single-performer job; multi-person capability is unused here. Lower priority than MediaPipe unless the real environment already has it running. |
| **AlphaPose** | 136-landmark whole-body (body+face+hands+feet) multi-person, with tracking | The hand/foot detail could matter for a piece built on object manipulation and juggling vocabulary (BRIEF.md) — hand keypoints are exactly what distinguishes "holding/throwing the coat" from generic arm movement. Worth the heavier setup if hand-level detail turns out to matter for t-004's section-by-section treatment. |
| **Optical flow (ComfyUI optical-flow nodes / raw OpenCV `calcOpticalFlowFarneback`)** | Dense pixel-motion field, not skeletal | This is the piece most suited to tracking the *coat itself*, since it has no skeleton to key on — optical-flow magnitude spikes/direction changes are a language-agnostic way to flag "something moved sharply" (a spin, a throw, a catch) regardless of whether it's the performer's body or the coat. Also the natural bridge into t-006's pipeline, since ComfyUI's optical-flow nodes are the same family used for vid2vid frame-consistency later in the pipeline — reusing the same motion-field data for both beat-mapping and render consistency avoids computing it twice. |

**Recommendation:** don't pick one — layer two signals, since the coat has
no skeleton: (a) MediaPipe Pose for the performer's own movement beats
(cheap, fast, good single-person accuracy), and (b) dense optical flow
(OpenCV Farneback or a ComfyUI optical-flow node, matching whatever t-006
already needs for render consistency) for coat motion and overall
scene-energy spikes that pose tracking alone would miss. AlphaPose's
hand/foot detail is a reasonable upgrade path if t-004's treatment planning
finds MediaPipe too coarse for the object-manipulation sections
specifically — flag as a fallback, not a default.

## 4. Suggested t-003 pipeline shape (for the beat map itself)

Not prescribing exact code (that's t-006), but the tool choices above
suggest a practical order of operations for producing the actual beat-map
table:

1. Extract audio track from the mp4 (ffmpeg, already assumed available).
2. Run librosa beat/onset detection on the extracted audio → candidate
   beat/onset timestamps.
3. Run MediaPipe Pose over the video → per-frame keypoints → derive
   movement-peak timestamps (e.g. joint-velocity local maxima).
4. Run dense optical flow over the video → frame-to-frame motion
   magnitude → flag motion spikes independent of pose (catches the coat).
5. Merge (2)+(3)+(4) into one beat-map table (timestamp, source signal(s)
   that fired, rough description) for a human pass — Silas or a later
   task reviews and annotates before t-004 treats each section.
6. Only reach for ffmpeg `scdet`/PySceneDetect if/when the edit introduces
   actual shot changes (cutaways, alternate angles) rather than treating
   the continuous single-take source.

## 5. Installation — where to put these tools

Silas approved the picks above and asked directly where to install them.
Answer: on whichever machine actually runs the beat-detection scripts (the
"target render environment" from `BRIEF.md`'s open Q3) — not in this
conductor sandbox, which deliberately has none of this stack and never
runs production tooling.

- **ffmpeg** is a system binary, not a Python package: `brew install ffmpeg`
  (macOS), `apt install ffmpeg` (Linux, including the kindrobots-unraid
  box if that ends up being the render machine), or an official static
  build for Windows. Install it wherever the shell that runs the pipeline
  scripts lives.
- **Python packages** (`librosa`, `madmom`, `mediapipe`, `opencv-python`,
  `scenedetect`) go in a dedicated virtualenv for this project, kept
  separate from any ComfyUI Python environment:
  ```
  python3 -m venv coat-dance-env
  source coat-dance-env/bin/activate
  pip install librosa madmom mediapipe opencv-python scenedetect
  ```
  Isolating the env matters here specifically because `mediapipe`/`madmom`
  pin `numpy`/`protobuf` versions that can conflict with ComfyUI's own
  dependency set — installing straight into a shared ComfyUI env risks
  breaking it.
- **Which machine:** beat detection itself is CPU-bound (`librosa`,
  `madmom`, `scenedetect` don't touch the GPU; `mediapipe` and optical
  flow can use one but run fine on CPU for a single 5:32 clip), so it
  doesn't need to live on the GPU/render box specifically — any machine
  convenient for running scripts works. It's still simplest to put it on
  the same machine that will run t-006's ComfyUI pipeline, so beat-map
  output feeds straight in without moving files across machines.
- **Where in this repo:** nothing to create yet — once t-006 stands up the
  actual pipeline, installation/setup notes belong in
  `projects/coat-dance/pipeline/` per `BRIEF.md`'s suggested folder layout.

## Open items / not resolved by this task

- No tool here was run against the actual file (sandbox has neither
  `ffmpeg` nor `cv2`/Python audio-video stack) — this is a selection, not
  a produced beat map. t-003 needs an environment with these installed.
- Whether AlphaPose's extra hand/foot detail is worth its heavier setup
  is a call to make once t-004's treatment planning is underway, not now.
- Confirms BRIEF.md's open Q3 (tool inventory in the real render
  environment) remains the actual blocker for running any of this for
  real — this task only narrows *which* tools to install/confirm there.

## Sources

- [Scene Detection & Automated Editing in FFmpeg – Complete Guide](http://www.ffmpeglab.com/articles/ffmpeg-scene-detection-automated-editing.html)
- [FFmpeg Scene Detection - Find Cuts Automatically](https://ffmpeg-cookbook.com/en/articles/scene-detect/)
- [Building a shot-detection worker for an upload pipeline with PySceneDetect 0.7 - DEV Community](https://dev.to/masonwritescode/building-a-shot-detection-worker-for-an-upload-pipeline-with-pyscenedetect-07-21n6)
- [GitHub - albanie/shot-detection-benchmarks](https://github.com/albanie/shot-detection-benchmarks)
- [PySceneDetect : Infrastructure for AI for Science | SciencePedia](https://www.bohrium.com/en/sciencepedia/agent-tools/Breakthrough_PySceneDetect)
- [Automated Dance Movement Analysis](https://www.emergentmind.com/topics/automated-dance-movement-analysis)
- [AfroBeats Dance Movement Analysis Using Computer Vision (YOLO + SAM)](https://arxiv.org/pdf/2512.03509)
- [Intelligent Dance Motion Evaluation: Keyframe Acquisition via Musical Beat Features](https://pmc.ncbi.nlm.nih.gov/articles/PMC11478525/)
- [PosePipe: Open-Source Human Pose Estimation Pipeline](https://arxiv.org/pdf/2203.08792)
- [madmom: A New Python Audio and Music Signal Processing Library (paper)](https://www.cp.jku.at/research/papers/Boeck_etal_ACMMM_2016.pdf)
- [Learn Audio Beat Tracking for Music Information Retrieval (Analytics Vidhya)](https://www.analyticsvidhya.com/blog/2018/02/audio-beat-tracking-for-music-information-retrieval/)
- [Open-Source Beat Detection Models Compared (madmom, BeatNet & More)](https://biff.ai/a-rundown-of-open-source-beat-detection-models/)
- [ComfyUI Optical Flow detailed guide](https://www.runcomfy.com/comfyui-nodes/comfyui-optical-flow)
- [GitHub - seanlynch/comfyui-optical-flow](https://github.com/seanlynch/comfyui-optical-flow)
