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
