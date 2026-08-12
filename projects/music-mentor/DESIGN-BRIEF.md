# Music Mentor — Design Brief

## What it is

A page on Kind Robots (`/music-mentor`) where you upload an audio recording of a
sung medley and get back structured, honest feedback on the **singing** and the
**arrangement**. You pick which dimensions of feedback you want; the tool
extracts objective signals from the audio and an LLM reasons over them plus your
setlist.

## Who it serves

Silas first — a songwriter iterating on medleys who wants a fast, private "second
ear" between takes. Secondarily anyone on the site rehearsing vocals or
sequencing songs into a medley who wants concrete, non-hand-wavy pointers.

## The honest boundary (stated up front, in the UI too)

No software judges "good singing" the way a vocal coach does — tone, emotion, and
style are subjective and need a human ear. What Music Mentor *can* do is measure
objective signals and reason about structure:

- **Intonation / pitch** — median pitch, how in-tune (average cents off the
  nearest note), note stability, rough vibrato, estimated key/scale.
- **Timing & rhythm** — tempo estimate and how steady it is (rushing/dragging).
- **Dynamics & expression** — loudness range and contrast across the take.
- **Arrangement & structure** — reasons over the setlist: song-to-song
  transitions, key relationships, pacing, and cohesion of the medley.

The feedback is explicit about only claiming what the numbers support.

## Creative direction

Warm, encouraging coach — specific and actionable, never vague praise or vague
scolding. Leads with what's working, then the highest-leverage fix. Feels like a
friendly rehearsal buddy, not a grading rubric.

## MVP shape (this build)

- **Client-side extraction** (`stores/helpers/audioAnalysisHelper.ts`): decode the file
  with the Web Audio API and compute a compact feature summary. Dependency-free
  (autocorrelation pitch tracking) so it ships today; a heavier pitch model is a
  later accuracy pass (t-007).
- **Endpoint** (`server/api/music-mentor/analyze.post.ts`): reuses the existing
  suggest-provider plumbing (`callSuggestProvider`, `manaGate`) to turn the
  feature summary + setlist + selected dimensions into feedback. No new Prisma
  model.
- **Store** (`stores/musicMentorStore.ts`): runs extraction locally, POSTs the
  summary, exposes status/feedback to the page.
- **Page** (`pages/music-mentor.vue`): audio upload, setlist textarea, four
  dimension toggles, analyze button, feedback panel, and a collapsible
  feature-summary for transparency. Mirrors `pages/video-generator.vue`.

**Ephemeral by design:** the audio is analyzed in the browser and never
uploaded; only the numeric summary and feedback leave the page, and nothing is
stored.

## Future growth

- Frontend placement + project art (t-006).
- Accuracy upgrade to a stronger pitch model behind the same summary shape (t-007).
- Later: optionally persist feedback as a `Chat` record to revisit past analyses;
  per-song breakdown for longer medleys; graduate to a standalone app via
  `scripts/new_app.py`.
