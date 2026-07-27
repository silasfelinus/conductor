# TALKBACK.md — Music Mentor

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-23 | Reviewer → Worker | music-mentor/t-003..t-005 | pattern
type: pattern

**Subject:** Feature extraction is client-side by necessity, not preference — keep it that way.
**Detail:**
- The Comfy GPU backend has no audio nodes (image/video/3D only), and the app
  deploys to Vercel serverless where Python/librosa can't run. So pitch/timing/
  dynamics analysis lives in the browser via the Web Audio API.
- The server endpoint only ever sees a compact numeric feature summary + the
  user's setlist — never the audio. This is the privacy/"ephemeral" guarantee
  Silas chose.

**Suggested action:** any future accuracy upgrade (t-007) must stay behind the
same feature-summary shape so the endpoint and page don't change, and must not
introduce a raw-audio upload without an explicit Silas decision.

## 2026-07-27 | Worker (scheduled burst-mode agent run) | music-mentor/t-007 | pattern
type: pattern

**Subject:** Accuracy upgrade shipped behind the same feature-summary shape, per the
2026-07-23 constraint — and the actual evaluation numbers didn't match the
going-in assumption about *why* YIN would help.
**Detail:**
- Implemented a YIN pitch detector (de Cheveigné & Kawahara 2002) alongside the
  existing normalized-autocorrelation tracker in `useAudioAnalysis.ts`, then
  compared both with a synthetic accuracy suite (pure/harmonic-rich/noisy tones,
  75–1046Hz) before deciding anything — `utils/scripts/verifyPitchDetectorAccuracy.test.ts`.
- Expected win going in: fewer octave errors on harmonic-rich tones (YIN's
  textbook advantage over plain autocorrelation). Actual result: both detectors
  scored 0 octave errors on the synthetic harmonic-rich cases — the existing
  tracker's "first-rising-peak" heuristic already guards against that reasonably
  well. The real, measured win was voiced-detection rate on low-register tones
  (YIN caught 75Hz/82Hz frames the autocorrelation tracker's `bestCorr/energy <
  0.5` gate rejected outright — 32/35 vs 35/35 detected overall) plus a small
  median-precision edge (0.7c vs 0.9c).
- Did not add pitchy or CREPE (both named as options in the task note): pitchy
  is an npm dependency for a project whose Web-Audio-API-only approach is
  otherwise dependency-free by design; CREPE is an ML model needing
  TensorFlow.js + weights, which doesn't fit "runs entirely client-side, no
  Comfy GPU, no Python" framing in the project's `notes_from_silas`. A
  hand-rolled YIN matched the existing code's own style (the autocorrelation
  tracker it replaces is also hand-rolled) and already closed the measured gap.
- No real vocal audio was available in this sandbox to test against — the
  evaluation is necessarily synthetic (sine tones + synthetic harmonics/noise).
  Flagged as a Kaizen suggestion in the PR: a small corpus of public-domain a
  cappella clips as fixtures would test breathiness/vibrato/polyphonic bleed
  that synthetic tones can't.

**Suggested action:** when an "evaluate X vs Y" task also names *why* one option
should win, verify the actual mechanism with a test before writing it up —
here, the textbook octave-error argument for YIN over autocorrelation didn't
reproduce, and a different (still real, still measured) advantage did. Report
what was actually measured, not what was assumed going in.
