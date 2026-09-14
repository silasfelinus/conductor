# music-mentor — task history archive

Full `note:` prose for completed music-mentor tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-007 — Accuracy pass — evaluate a heavier pitch model

<!-- note:begin t-007 -->
The MVP uses a dependency-free autocorrelation pitch tracker (good for monophonic takes, degrades on mixed/polyphonic audio). Evaluate a stronger option (e.g. pitchy / a YIN lib / CREPE) behind the same feature-summary shape so the endpoint and page don't change.
DONE 2026-07-27 (claude-scheduled-20260727T030748Z-mm-t007): implemented a YIN pitch detector (de Cheveigne & Kawahara 2002), now owned by kind_robots stores/helpers/audioAnalysisHelper.ts, kept the old tracker as detectPitchAutocorrelation for reference, and added a synthetic accuracy suite (utils/scripts/verifyPitchDetectorAccuracy.test.ts) comparing them on pure/harmonic-rich/noisy tones across 75-1046Hz. Results: YIN detected 35/35 test frames vs. autocorrelation's 32/35 (missed low-register 75-82Hz tones specifically), both 0 octave errors, YIN median 0.7c error vs 0.9c. Switched analyzeAudioFile to YIN. No change to AudioFeatureSummary, the endpoint, or the page. Did not pursue CREPE (would need TensorFlow.js + model weights, at odds with the project's dependency-free client-side design) or pitchy (an npm dependency) since a hand-rolled YIN matched the existing code's style and closed the gap already found. Merged via kind_robots PR #1036.
<!-- note:end t-007 -->

## t-008 — Submit project art (icon/card/hero) via ArtJob

<!-- note:begin t-008 -->
All three art requests submitted to /api/conductor/art-request (HTTP 201 each: music-mentor icon/card/hero) — the endpoint committed the queue entries to conductor main. Root cause of the earlier 401 was NOT an expired token: request_art.py sent the token in the legacy X-KR-API-Token header, but the endpoint's validateApiKey reads x-api-key / authorization / x-admin-token. Fixed request_art.py to send x-api-key (see this PR). Downstream generation of the actual .webp files happens via the art consumer; on-page card/hero appear once those land.
<!-- note:end t-008 -->
