# kr-arcade/t-155 — full note history archive

This file is the archaeology index for kr-arcade/t-155 ("Turn on ACE arcade soundtrack generation, ingest the first approved track, and listen to it in a cabinet"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-155 -->
Silas, 2026-10-19, verbatim: "generating better audio should absolutely not require human approval, fyi". The money gate is lifted: agents queue ACE-Step renders themselves through /api/art/enqueue (enqueueArcadeSoundtrack.ts, enqueueRainbowScore.ts; Rainbow's 21 score cues went in as ArtJobs #40796-#40816 the same day while the render box's queue was idle). Remaining agent work: drop the per-cue approval and ARCADE_AUDIO_JOBS_ENABLED gates from POST /api/arcade/audio-jobs (or retire it for the direct path), then ingest renders as below. A production env var still only Silas sets; nothing here needs one any more.
Remainder of silasfelinus/kind_robots#3606 that needs Silas. Human steps: confirm the kr-relay build advertises supportsAudio with the ACE-Step model installed (GET /api/arcade/audio-jobs then reports the relay ready), and set ARCADE_AUDIO_JOBS_ENABLED=true on production. After that an agent can: approve one test cue (gloom-invaders/level), confirm the worker returns a readable file, and ingest it: check duration and format, set the loop point, trim cue renders from 10s, transcode, record the SHA-256, ArtJob id and approval/verified dates, publish under /images/arcade/audio/<game|shared>/<cue>.<ext>, confirm it fetches from production, and add it to VERIFIED_ARCADE_AUDIO_ASSETS. Then approve the remaining priority-cabinet cues. Done when someone has heard at least one ACE recording in a cabinet, including the crossfade, ducking and oscillator fallback.

Removed the obsolete per-cue approval, environment flag and relay-readiness gates from the admin audio enqueue route. The PR retains job deduplication and uses the existing ACE-Step ArtJob pipeline. Render ingestion and audible verification remain open.

Reviewer (scheduled, 2026-11-23 PT): kind_robots#5663 merged on all-green CI (989b6f37).
The admin audio enqueue now submits deduplicated ACE-Step jobs without the retired
approval, env-flag and relay gates, and it stays admin-guarded. Ingesting renders, an
audible cabinet check and cue activation remain, so t-155 goes back to ready. The new
path only works on production after a Force Update.
<!-- note:end t-155 -->
