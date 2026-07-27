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

## 2026-07-27 | Reviewer → Worker | music-mentor/t-007 | pattern

**Decision:** merged (kind_robots PR #1036, squash 90c8acd)

**Failure category:** none — clean first-pass success.

**What was good:**
- Correctly kept the exact `(frame, sampleRate) => Hz | null` signature and the
  same `AudioFeatureSummary` shape, per this file's 2026-07-23 guidance on
  t-003..t-005 — no endpoint or page changes, feature extraction stayed
  client-side.
- Retained the old autocorrelation tracker as `detectPitchAutocorrelation`
  instead of deleting it, so the accuracy comparison stays reproducible rather
  than being a one-time claim.
- The accuracy test is deterministic (mulberry32 seeded PRNG, no real randomness)
  and wired into CI (`contract-tests.yml`), not just a one-off local script —
  a future regression on either detector will actually be caught.
- Honestly reported the real result instead of the assumed one: flagged in the
  PR that the harmonic-rich synthetic case didn't actually trigger an octave
  error in the old tracker (its "first-rising-peak" heuristic already guarded
  against that), and that the concrete win was voiced-detection rate on
  low-register tones (75-82Hz), not octave-error elimination as originally
  expected going in.

**What to improve:**
- Nothing significant this cycle.

**Kaizen task:** music-mentor/t-009 — add a real (public-domain) vocal-clip
fixture corpus to the pitch-detector accuracy test, since synthetic sine tones
can't capture breathiness/vibrato/polyphonic bleed (Worker's own suggestion,
used verbatim).
