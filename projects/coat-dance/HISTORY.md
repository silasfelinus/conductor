# coat-dance — task history archive

Full `note:` prose for completed coat-dance tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Draft production brief and asset checklist

<!-- note:begin t-001 -->
FOR SILAS: Production brief written to projects/coat-dance/BRIEF.md. It covers the core premise, target runtime assumptions, a required-assets checklist, and a suggested (not-yet-created) working-folder layout.

Correction worth flagging: the brief's source note assumed the original video still needed to be provided — it doesn't. `coat dance_x264.mp4` is already in projects/coat-dance/ (has been since 2026-07-17). Read directly from the file (no ffmpeg in this sandbox, so parsed the MP4 box headers by hand): 720x480 H.264, ~5:32 runtime, and it already has a synced audio track (44.1kHz) — not silent, contrary to what "provide the original video" implied.

ANSWERED 2026-07-25: Silas confirmed Q1 (music direction) — "there is very specific audio used in the video, currently no interest in changing it at this point." Original audio only, preserved as-is; no new/replacement track, no blend. Recorded in BRIEF.md's Open Questions section (also resolves Q2 by implication: the audio is intentional, not disposable). Q3-Q5 (tool inventory, surviving stills/notes, target runtime length) remain open but are not blockers for t-002. Unblocking t-002 (video beat-transcription tool research). moves from blocked to ready.
<!-- note:end t-001 -->

## t-002 — Research video beat transcription and shot-slicing tools

<!-- note:begin t-002 -->
Identify practical tools or scripts for segmenting the source dance video by movement beats, shot changes, audio events, and pose/action changes. Compare options such as ffmpeg scene detection, optical-flow/pose analysis, transcript notes, manual beat sheets, and any Comfy/LAX/Wan-friendly preprocessing.
FOR SILAS: Tool-survey draft at projects/coat-dance/RESEARCH-t002-beat-transcription-tools.md (2026-07-29). Contains: (1) a shot/scene-detection pick (ffmpeg scdet as a cheap first pass; PySceneDetect kept in reserve only if the edit later adds cutaways, since the source is one continuous take), (2) an audio beat/onset pick (librosa by default, madmom as a fallback if the 2006 live-performance room audio proves too irregular for librosa's beat tracker), and (3) a movement-detection recommendation to layer MediaPipe Pose (performer) with dense optical flow (the coat itself, which has no skeleton to track) since no single tool covers both duet partners -- plus a suggested t-003 pipeline order for turning these into one merged beat-map table. TO APPROVE: read the doc; if the tool picks look right, set status: ready on t-003 (Create source-video beat map template) yourself, or leave a note here if you want a different tool swapped in first. Also note the doc's caveat: this sandbox has neither ffmpeg nor a Python audio/video stack, so nothing ran against the real file -- it's a selection, not a produced beat map. It re-confirms BRIEF.md's open Q3 (tool inventory in the real render environment) as the actual blocker before t-003's template can be exercised for real, so that's worth resolving alongside/before unblocking t-003. What unblocks: t-003 (currently `blocked` on this task) once you flip it to `ready` -- see BRIEF.md's suggested-folder plan for where its output (source/beatmap.md) should land.


SENT BACK by silasfelinus via Kind Robots For You. I approve the default suggestions, and just need info on how to proceed. if I need to download tools, tell me where to put them.

RESOLVED 2026-08-11: added a "5. Installation -- where to put these tools" section to
RESEARCH-t002-beat-transcription-tools.md answering the direct question -- ffmpeg is a
system package (brew/apt, install wherever the pipeline shell runs), the Python packages
(librosa, madmom, mediapipe, opencv-python, scenedetect) go in a dedicated virtualenv kept
separate from any ComfyUI env (mediapipe/madmom pin numpy/protobuf versions that can
conflict), and none of it needs a GPU except optionally mediapipe/optical-flow (both run
fine on CPU for one 5:32 clip) -- simplest to put it on whatever machine will run t-006's
ComfyUI pipeline so the beat map feeds straight in. Per Silas's own approval above and this
task's own "set status: ready on t-003 yourself" instruction, t-003 is now unblocked to
ready. Closing t-002 done -- deliverable (tool survey + install answer) complete and
approved; nothing further needed from Silas on this task specifically. BRIEF.md's Q3 (tool
inventory actually confirmed present in the real render environment) remains open and is
t-003/t-006's concern, not this task's.
<!-- note:end t-002 -->

## t-003 — Create source-video beat map template

<!-- note:begin t-003 -->
FOR SILAS: the reusable beat-map table format lives at projects/coat-dance/source/beatmap.md. It contains: column definitions (Timestamp Range, Movement/Action, Coat Behavior, Camera/Framing, Emotional Tone, Candidate AI Treatment, Generation Method, Restitch Notes), the suggested fill-in pipeline order from t-002's tool research, and one placeholder row rather than a preset section count (per BRIEF.md, section count should follow the real beat structure once it's produced).
TO APPROVE: read the template's column definitions and pipeline order -- confirm the shape looks right for populating once a render environment with ffmpeg/librosa/mediapipe is available (this sandbox has neither, so no real timestamps were produced), or leave notes if a column should change. Set approved_by_human: true and status: done, or edit the note with what to adjust.
What unblocks: t-004 (section-by-section creative treatment) still needs the table actually filled in with real timestamps first -- that's a separate future task once the render-environment tool inventory (BRIEF.md Q3) is confirmed, not this one.


Silas's 2026-09-07 default-recommendation policy accepts the existing beat-map columns and pipeline order. Do not close this as mere template approval: the remaining deliverable is the real timestamped beat map from the already-present coat dance_x264.mp4. Treat ffmpeg/librosa/MediaPipe availability as agent-owned tooling/setup work; prefer a dedicated isolated analysis environment as t-002 recommended, and produce exact setup/run instructions when execution must occur on a local/render host. Original synced audio remains the soundtrack per Silas's earlier decision.

FOR SILAS: the real, timestamped beat map is done -- projects/coat-dance/source/beatmap.md (38 sections, full 0:00-5:32 runtime, no gaps). It contains: per-section Movement/Action, Coat Behavior, and Emotional Tone read directly from extracted video frames (not guessed), grounded in real audio-structure and motion-energy numbers; a first-pass Candidate AI Treatment idea per section; and a "Structural read" summary of the piece's arc (quiet coat-handling opening -> row 16 flourish hinge -> photo-projection sequence with a measured energy peak at row 17 and a legible image/body rhyme at row 31 -> blackout -> closing tableau).

TO APPROVE: read through the table (or at least the "Structural read" section and a sample of rows) and confirm the beat boundaries and descriptions feel right, or leave notes on what to adjust -- rows 3/5's "blurred figure" read as motion blur of you, not a second performer, is the one interpretive call most worth double-checking against your own memory of the performance. Set approved_by_human: true and status: done, or edit the note with corrections.

What unblocks when you do: t-004 (section-by-section creative treatment) can start for real -- it was blocked on this table existing. Generation Method is deliberately left blank throughout, pending t-006's render-environment tool inventory.

State reconciliation (session sweep): approved_by_human=true was already set (Silas
approved the timestamped beat map per the note's own TO APPROVE instruction) but status
never flipped to done. Reconciling per docs/state-reconciliation.md; t-004 remains
blocked pending its own separate work.
<!-- note:end t-003 -->

## t-010 — Polish and upgrade Coat Dance front-end surface

<!-- note:begin t-010 -->
Re-checked before doing any work (per convention). Step (4) (evolve the interactive slot) remains blocked on t-003 (source-video beat map), still status: needs-human, unresolved -- no source video has landed since the 2026-08-20 cycle. Steps (1)-(3) remain confirmed done. No agent-actionable scope exists on this task until Silas supplies the source video via t-003. Re-armed to ready; will stay a genuine no-op until t-003 clears.
Re-checked before doing any work (per convention). Corrected an inaccurate claim this task's own note had been carrying forward: step (4)'s blocker is NOT 'no source video has landed' -- projects/coat-dance/coat dance_x264.mp4 has been checked in since 2026-07-17 (confirmed present, 35.5MB, per BRIEF.md's own technical read table). The real, still-unresolved blocker is twofold: (a) t-003 (source-video beat map) produced a template scaffold but is still status: needs-human awaiting Silas's read/approval of its column shape and BRIEF.md's open Q1-Q3 (target music track, whether the muxed audio is usable, and the render-environment tool inventory), and (b) filling the template with REAL timestamps needs ffmpeg/librosa/mediapipe, none of which exist in this sandbox (re- confirmed this cycle: 'which ffmpeg' fails, both Python imports fail) -- and per t-003's own note, this is deliberately deferred to whatever real render environment Silas answers BRIEF.md Q3 with, not something to route around by installing these in the conductor sandbox, since that sandbox isn't the actual production/GPU environment this pipeline will run in anyway. Steps (1)-(3) remain confirmed done. No agent-actionable scope exists on this task until Silas answers BRIEF.md's open questions and t-003 clears. Re-armed to ready; will stay a genuine no-op until then.
Re-checked before doing any work (per convention), session-start conductor sweep 2026-09-04 ~20:35 UTC. Nothing has changed since the 2026-09-03 re-check: t-003 (source- video beat map) is still status: needs-human (updated 2026-08-12, no approved_by_human), BRIEF.md's Q1/Q2 (target music track, whether the muxed audio is usable) remain unanswered, and the sandbox still has no ffmpeg/librosa/mediapipe ('which ffmpeg' fails, both Python imports fail). No agent-actionable scope exists on this task until Silas answers BRIEF.md and t-003 clears. Re-armed to ready.
Re-checked before doing any work (per convention), scheduled Conductor Agent sweep 2026-09-23T08:00Z. Corrected a stale claim this task's note had been carrying since 2026-09-04: t-003 (source-video beat map) is NOT still needs-human -- it reached status: done on 2026-09-20 with a real, timestamped beat map (38 sections, full 0:00-5:32 runtime, Silas-approved) at projects/coat-dance/source/beatmap.md. However, that table's Candidate AI Treatment column is explicitly a first-pass idea per section, pending t-004's real section-by-section creative treatment -- t-004 is still status: needs-human (gate_human: true, depends_on t-003, unapproved), so step (4) (evolve the interactive slot with real per-section AI treatment behavior) remains blocked, just on a different, now-correct task than the note previously named. Steps (1)-(3) remain confirmed done. No agent-actionable scope exists on this task until Silas approves t-004's creative treatment. Re-armed to ready; will stay a genuine no-op until t-004 clears.
Re-checked before doing any work (per convention), scheduled Conductor Agent sweep 2026-09-26T16:57Z. Confirmed via this session's own audit_human_gates.py run: coat- dance/t-004 (real section-by-section creative treatment) is still status: needs-human (gate_human: true), unchanged. Steps (1)-(3) remain confirmed done. No agent-actionable scope exists on this task until Silas approves t-004's creative treatment. Re-armed to ready; will stay a genuine no-op until t-004 clears.

Silas explicitly requested a video-generator tab for full-length Coat Dance upload, style selection and resumable background production. This supersedes t-010's old no-op assumption, without approving the separate creative-treatment gate.

Added an admin-only video restyle studio linked from Video Gen, private MP4/MOV/WebM upload with persistent on-disk manifest, segmented motion-preserving render recipe, six styles and independent job history. The actual GPU render worker is explicitly unimplemented; staged jobs do not pretend to run. Kind Robots implementation commit ce062471675df5f652fbdf5f21cef465b8cc7a17. Opening PR and checking CI.

Kind Robots PR #3722 was confirmed merged at 2bb2a79586b60fef535b97c84d856e1a3079dd8b. This closes only the staged frontend/upload milestone; no claim that the motion-conditioned GPU renderer exists. Screenshot follow-up is PR #3723 on t-011.
<!-- note:end t-010 -->

## t-015 — Restyle studio: expanded look library with art-queue preview images

<!-- note:begin t-015 -->
Silas, 2026-10-17, finishing a ChatGPT style-picker thread: add art to the art queue and more style options. Kind Robots PR #3782 grows the /admin/coat-dance Looks pane from 6 to 33 looks. Every look keeps a Wan VACE video prompt and gains a preview clause. Card art is a real Kind Robots ArtJob render (Krea 2, 896x1152) of one shared comparison scene, so the cards compare style rather than subject: a dancer in black, a white coat flung wide, warm hanging lights, a blurred crowd. Admin actions: Generate / Regenerate preview, Generate missing (n). Failed previews requeue in place. Merged at 1f0522ca after 24/24 green checks, live on kindrobots.org (GET /api/video-restyle/previews 200). All 33 previews were queued through the new route as ArtJobs 39767-39799, and all 33 rendered DONE with no failures (verified by downloading each final image). After a visual check, kind_robots#3786 (merged 32fe9980) tightened three preview clauses: the felt, clay and puppet looks had drawn a photoreal dancer. Those were regenerated as ArtJobs 39816-39818: clay and felt now render the dancer in the material; puppet stage is only partly fixed (the crowd are marionettes, but the dancer still reads as human). Open for Silas: a visual pass on the 33 cards, plus Regenerate or edit any look he dislikes.
<!-- note:end t-015 -->

## t-016 — Restyle studio: Grab bag look that rotates styles every motion window

<!-- note:begin t-016 -->
Silas, 2026-10-17: add a Grab bag option that changes look every segment on purpose and loops through the chosen looks, so he can see a version that swaps style deliberately. Kind Robots PR #3820 adds the Grab bag card (4-tile preview collage), lets the gallery pick 2-12 looks in rotation order, and offers "Loop in listed order" and "Shuffle once, then lock". It saves variantStyleIds and variantMode, and a source-time-anchored styleSchedule on each pilot and full pass, so re-renders, retries and the full film never reshuffle. Grab bag ArtJobs are claimable only by a relay that declares supportsVideoRestyleGrabBag. This conductor PR updates ops/home-server (vace_relay.py, relay_agent.py, coat_dance_vace_worker.py): per-window prompts, no chained continuity reference across a look change, and cache signatures unchanged for single-look jobs. Ferngrotto must git pull and restart kr-relay before a Grab bag pilot will be claimed. kind_robots#3820 merged at b0dd5c76 after 27/27 green checks; this conductor PR (#6290) lands the relay/worker side. Merged is not deployed: the Alexandria image and the Ferngrotto relay pull are separate steps. Open for Silas: queue a Grab bag pilot and judge the swaps.
<!-- note:end t-016 -->

## t-017 — Video Restyler overwrite strength and editable project titles

<!-- note:begin t-017 -->
Silas requested control over how strongly rendered video replaces original footage, plus custom editable saved-project titles and no Coat Dance default for uploads. Implement through Kind Robots studio/API and Conductor VACE relay, with source-safe defaults and actual renderer contract tests. No live render, deployment or publishing.

Implemented source-mix overwrite strength through Kind Robots job settings, ArtJob payload and relay capability gate, plus editable titles and filename-based default. VACE worker source blending preserves existing 100 percent behavior and original soundtrack. Implementation PRs are being opened for CI verification.

Merged silasfelinus/conductor#6383 at 8e468a6 after all five workflows passed, including the Python suite. Merged silasfelinus/kind_robots#3884 at 93e6e1a after all 22 workflows passed, including typecheck, video-restyle contract, Prettier and layout checks. A lower overwrite strength blends original source frames into the new look while preserving the original soundtrack; default 100 percent preserves legacy output. New uploads derive title from filename; existing projects and variants can be renamed without re-upload. Both PRs are merged; no live Unraid/Windows deployment or GPU render was performed or verified.
<!-- note:end t-017 -->
