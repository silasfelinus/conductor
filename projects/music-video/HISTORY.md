# music-video — task history archive

Full `note:` prose for completed music-video tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-003 — ACE-Step spike: pick the model variant and write the Comfy workflow spec

<!-- note:begin t-003 -->
Write projects/music-video/docs/ace-step-spike.md. Decide ACE-Step v1 (documented native Comfy nodes TextEncodeAceStepAudio, EmptyAceStepLatentAudio, SaveAudio and SaveAudioMP3) versus v1.5 (reportedly up to 10 minutes on 12 GB-class cards, but native-Comfy support is unconfirmed; it may need a custom node or a newer ComfyUI). Include for the chosen variant (a) the API-format workflow graph as JSON with node ids, (b) how pitch settings map to tags and lyrics and to the duration and seed inputs, (c) the output node (prefer SaveAudioMP3; a 4-minute FLAC is about 47 MB of base64 inside the /complete transaction), (d) every model file with size and the folder it must live in, (e) expected VRAM and runtime on the 12 GB card, (f) the licence, and (g) the minimum ComfyUI version. Cite sources. Cloud sessions cannot reach Comfy or reliably reach huggingface (EGRESS-BLOCKERS.md), so this is research and a spec; the live proof is t-012. Verify node names against the docs rather than memory.
2026-10-01: spec landed at projects/music-video/docs/ace-step-spike.md (ACE-Step 1.5 turbo chosen; UNVERIFIED items handed to t-012).
<!-- note:end t-003 -->

## t-004 — MusicVideo model, admin API and timeline-document schema (kind_robots)

<!-- note:begin t-004 -->
In silasfelinus/kind_robots add a MusicVideo Prisma model (id, userId, title, status, doc LongText holding the MusicVideoDoc JSON from DESIGN-BRIEF.md, timestamps, optional finalArtImageId) with ONE additive migration (CREATE TABLE only; the Reviewer may merge it after a line-by-line audit). Add admin-only CRUD under server/api/music-video/ using requireAdminApiUser, and the TypeScript types plus a DB-free validator for the document in utils/ (timeline math stays pure and in utils/). Tests are tsx utils/scripts/verify*.test.ts with a package.json test script and a step in contract-tests.yml; kind_robots has no vitest. Never run prisma migrate reset. Use scripts/provision_kind_robots_deps.sh to verify.
2026-10-02: kind_robots#3179 opened (MusicVideo model + additive migration, MusicVideoDoc normalizer, admin CRUD under /api/music-video, contract test). Local: vue- tsc 0 errors, 404/404 contract scripts, generated-client parity OK.
2026-10-02: kind_robots#3179 merged (794397b) after 36/36 checks green incl. Replay migrations on MariaDB. Schema-affecting: MusicVideo table applies on the next Alexandria deploy-unraid.sh run.
<!-- note:end t-004 -->

## t-005 — Lyrics: pitch and settings to structured, editable lyrics

<!-- note:begin t-005 -->
Server route under server/api/music-video/ that wraps POST /api/generate/text (provider agnostic and mana metered; do not hand-roll a provider call). Input is the pitch plus optional duration, genre, BPM, mood, vocal and language; output is MusicVideoDoc.lyrics sections tagged verse, chorus, bridge and so on, with the section count derived from duration and BPM. Support per-section regenerate, inline line editing and a per-section lock so regenerate never overwrites locked text. Lyric text must never go into an ArtJob promptString. DB-free tests cover the section-count math and the response parser.
2026-10-02: kind_robots#3183 merged (00d8b0e) after 33/33 checks. First CI run caught an unguarded capture-group index (verifyCaptureGroupGuards); fixed in bc8fc39. POST /api/music-video/[id]/lyrics plus utils/musicVideoLyrics.ts (incl. toAceStepLyrics for t-010).
<!-- note:end t-005 -->

## t-006 — Admin page, musicVideoStore and placement

<!-- note:begin t-006 -->
Add /admin/music-video (pages/admin/) and a Pinia musicVideoStore that owns every API call (components never call $fetch or localStorage). Follow kind_robots' art-first standard: an image-led stage with the pitch, lyrics, song, timeline and scenes on one visual surface instead of a wizard. Add the placement entry to utils/projectPlacements.ts (channelKey admin, tabKey music-video, route /admin/music-video, like scene-animator) and the channel document content/channels/admin/music-video.md with requiredRole ADMIN; verifyChannelContent.ts and verifyNoHiddenRoutes.ts reject an unplaced route. Do NOT add liveUrl, channelKey or tabKey to conductor's project-overrides.yaml (kind_robots AGENTS.md forbids it). Read docs/agents/frontend-verification.md before verifying.
PR https://github.com/silasfelinus/kind_robots/pull/3210: /admin/music-video page, musicVideoStore, placement and channel doc. Checked: vue-tsc, eslint, prettier, channel- content, no-hidden-routes, layout-contract, page-backdrop. Not browser-verified.
MERGED kind_robots#3210 (64e9074). Admin page, store, placement, channel doc landed. Ladder rung: worker pickup via select_role (branch-medic finding was PR #3195, open and security-sensitive, left to its reviewer).
<!-- note:end t-006 -->

## t-007 — Timeline editor: waveform, beat grid and scene markers

<!-- note:begin t-007 -->
Waveform of the song, a beat grid built from the requested BPM plus an offset and beats per bar (audioAnalysisHelper is tuned for monophonic vocals and exports no onset times, so detection is a later upgrade), section bands from the lyrics, scene markers that snap to beat or bar or move freely, and lyric-line assignment to scenes. Lines are spread across sections by section length and are user-adjustable; forced alignment is out of scope. Timeline math is pure code in utils/ with tsx verify tests; the audio is fetched as a blob because private rows need a Bearer header.
2026-10-06: merged kind_robots#3240. utils/musicVideoTimeline.ts (beat grid, snap, waveform peaks, section bands, markers, scene split/merge, lyric assignment) with test:music-video-timeline in CI, plus components/music-video/music-video-timeline- editor.vue wired into the admin page. Note: Nuxt pathPrefix is off, so component file names must be globally unique. Phone/tablet/desktop visual check is not done here; it belongs to t-016.
<!-- note:end t-007 -->

## t-008 — Scene prompts, validator and per-scene image generation

<!-- note:begin t-008 -->
An LLM scene-prompt writer (via POST /api/generate/text) that turns a scene's lyric span plus the shared style bible into one Krea 2 prompt, and a validator that rejects negations, art-direction jargon and conditionals before enqueue (patterns: utils/kreaSemanticPrompt.ts in kind_robots; the negation guard in scripts/build_cthulhuquarium_art_queue.py here). Enqueue each scene through POST /api/art/enqueue (krea2 default, optional loraResourceIds) with a musicVideo provenance block and a dedupe key modeled on scene-animator's. Scene status is derived from ArtJobs, never stored. Per scene: regenerate, upload an image (the existing upload route is image-only and open to any signed-in user, so use or add an admin-gated path), or pick from the gallery. Enqueue at the default priority; scene jobs are about 400 s each on the single 12 GB card.
Reviewed and merged kind_robots#3188 (all checks green, reversible admin-gated routes).
<!-- note:end t-008 -->

## t-009 — Per-scene motion: Ken Burns presets and optional ltx or wan clip

<!-- note:begin t-009 -->
Default motion is client-side Ken Burns plus crossfade. A per-scene opt-in requests an ltx or wan image-to-video clip through /api/video/generate with the scene still as the first frame, showing the runtime hint from utils/videoPresets.ts (3 to 4 second clips, timeouts up to 5400 s). Clips are silent; the song is the only audio. The clip is an ArtImage referenced by scene.motion.clipArtImageId.
Canonical Ken Burns presets (utils/musicVideoMotion.ts, mirrored in conductor scripts/build_music_video.py), presets on planned scenes, POST /api/music- video/[id]/scenes/clips (ltx/wan via /api/video/generate, mp4, scene still as first frame), clip status sync; headless pipeline waits for clips and falls back to Ken Burns (conductor#5513).
<!-- note:end t-009 -->

## t-010 — acestep workflow builder, enqueue engine and song endpoint (kind_robots)

<!-- note:begin t-010 -->
Build server/api/comfy/acestep/utils/workflow.ts from the t-003 spec and add engine acestep to POST /api/art/enqueue with jobEngine COMFY and payload.media audio (no migration, as video does): EnqueueEngine, normalizeEngine and GATE_ENGINE in enqueue.post.ts, a buildJobPayload branch, and ComfyEngine in comfyGate.ts. Provenance: enrichArtJobPayload (artJobProvenance.ts lines 47 and 261-270) requires top-level promptString to equal a workflow string whose key matches (^|_)(prompt|text)($|_), but TextEncodeAceStepAudio uses tags and lyrics, so every job would 400; extend the pattern with the artjob-provenance-contract tests and set promptString to exactly the tags string. Keep lyrics out of promptString because assertQueuedArtPromptContract (claim.post.ts) would reject lyric text. Set timeoutSeconds in the payload. Add POST /api/music-video/song (tags, lyrics, duration, BPM, seed). Mana gates an acestep job as comfy, which bills like a 1024 square still; fine while admin-only. Verify structurally with fixtures; Comfy is unreachable from cloud sessions.
ACE-Step 1.5 song graph, acestep enqueue engine (tags as promptString, lyrics separate), provenance tags candidate, audio skips claim-time image contract, POST/GET /api/music- video/[id]/song. Live run is t-012.
<!-- note:end t-010 -->

## t-011 — Relay audio support (conductor ops/home-server)

<!-- note:begin t-011 -->
The live relay entry point is ops/home-server/relay_media_agent.py, which overrides relay.run_comfy and recomputes want_video itself, so patch it AND relay_agent.py. Add media audio handling with audio extensions and a want_audio path through find_output_file, extract_comfy_output and run_comfy; fix write_local_copy (it would write mp3 bytes as .png); send isPublic false at upload_result (it currently sends no isPublic, so the row is public until /complete flips it); and advertise supportsAudio so the t-020 claim gate releases audio jobs. An unpatched relay does not fail loudly; it stores audio as a png. Add tests/test_relay_agent_audio.py following tests/test_relay_agent_video.py. This is a conductor-side PR; the kind_robots t-020 PR merges first. Do not deploy anything (that is t-012).
2026-10-02: conductor#5506 merged (relay supportsAudio, mp3 outputs; CI green). Reviewer-approved.
<!-- note:end t-011 -->

## t-012 — Stage ACE-Step on the share, deploy the relay, run a 30 second song

<!-- note:begin t-012 -->
Agent part: add an audio tier to scripts/sync-comfy-models.sh and .ps1 in kind_robots (the script only copies from the Alexandria share to local disk, so the ACE-Step files must be on the share first), and write the runbook. Human part, which only Silas can do and which is a production deploy to his render box (never deployed from a session): stage the model files, update the relay checkout and restart it under pm2, then run one 30 second song through /api/music-video/song and confirm the ArtImage plays. Write the FOR SILAS block as self-contained commands that start with cd and git pull, per kind_robots AGENTS.md. Park the task at needs-human with the commands and stop; this is the first real render of the audio lane.
Agent part done: audio tier in kind_robots sync-comfy-models (#3198) and projects/music- video/docs/t-012-runbook.md. FOR SILAS: follow the runbook at Ferngrotto: (1) curl the four ACE-Step files onto Z:\ai\models\{unet,clip,vae}; (2) cd D:\code\kind_robots; git pull --ff-only; .\scripts\sync-comfy-models.ps1 -Tier audio -Yes; (3) cd D:\comfy\comfy-fast; git pull; pm2 restart comfyui, then /object_info/TextEncodeAceStepAudio1.5 must be 200; (4) cd D:\code\conductor; git pull --ff-only; pm2 restart kr-relay; (5) cd D:\code\conductor; python scripts\build_music_video.py --duration 30 ... and confirm the song ArtImage plays. Record peak VRAM, wall-clock, mp3 size and whether SaveAudioAdvanced accepted the encoding, then set done + approved_by_human: true (unblocks t-015).
2026-10-06: Silas asked why the models go through Alexandria when ComfyUI runs from local disk anyway. The runbook now has steps (1) and (2) curl the four files straight into D:\comfy\comfy-fast\models\{unet,clip,vae}. Archiving them on the share is now an optional robocopy step. Steps (3)-(5) are unchanged.
2026-10-06 DONE (Silas confirmed the song plays). First real render of the audio lane: ArtJob 34086, ACE-Step 1.5 turbo, 30 s song generated in 0:40 on Ferngrotto (warm-ish; first job after the ComfyUI restart), mp3 930 KB. SaveAudioAdvanced accepted the format/quality encoding as sent, so the SaveAudioMP3 fallback is not needed. Peak VRAM not measured (nvidia-smi -l does not keep a peak). Models were downloaded straight to D:\comfy\comfy-fast\models, not via Alexandria. Setup snags, now in the runbook: ComfyUI was a detached checkout at v0.35.1 so git pull failed (moved to tag v0.39.0); a plain pm2 restart orphaned the old ComfyUI on 8188 and the new one crash-looped (fixed with pm2 stop, kill the port owner, pm2 start); 'python' on PATH is the Store stub (use C:\Python312\python.exe). UI follow-ups shipped: song playback on the ArtJob card (kind_robots#3242) and the art card, which also now loads private renders through the queue's loader (kind_robots#3243).
<!-- note:end t-012 -->

## t-013 — Audio upload fallback (admin-only route)

<!-- note:begin t-013 -->
The existing server/api/art/upload.post.ts is image-only (PNG, JPEG and WebP, a 15 MB cap) and open to any signed-in user, so add a new admin-only audio route: MP3 and WAV, a sensible size cap, stored as a private audio ArtImage through the t-020 path, returning the artImageId for MusicVideoDoc.song with source upload. This is for Suno exports and Silas's own medleys, and it lets lyrics, timeline, images and compile be built and tested before t-012.
Song upload merged (kind_robots#3216): POST /api/music-video/[id]/song-upload, MP3/WAV, private audio ArtImage, video length follows the song.
<!-- note:end t-013 -->

## t-014 — Browser compositor and MP4 exporter

<!-- note:begin t-014 -->
A canvas stage renderer that composites scene stills and clips with Ken Burns and crossfades, driven by song, timeline and scenes only, so it can be built against fixtures. The same renderer powers scrub-preview and export. Export encodes with WebCodecs and a muxer library (mp4-muxer or mediabunny; record the dependency choice in the PR) with the song as the audio track, and downloads the MP4. The compositor lives in stores/helpers/, not a root composables/ directory. Chromium-first is acceptable while admin-only. Tests: pure frame and timing math as tsx verify tests, plus a Cypress or Playwright smoke for the WebCodecs path. Save-to-server and a relay ffmpeg job are later upgrades, not this task.
Implementation: silasfelinus/kind_robots#3241 (compositor + mediabunny exporter + admin button; contract test in CI). Smoke in headless Chromium produced a valid MP4 via the VP9 fallback; H.264/AAC path and visual check on a real doc still need Silas's browser.
RECONCILED 2026-10-06: implementing PR kind_robots#3241 merged 2026-10-06T02:08:47Z; closed by drift check (check_pr_merged_drift).
<!-- note:end t-014 -->

## t-020 — ArtImage audio support in kind_robots (storage, serving, consumer audit, claim gate)

<!-- note:begin t-020 -->
Audio rides ArtImage, which already stores mp4 and webm through fileType, so this needs no schema change. In kind_robots: add mp3, wav, ogg and flac to ALLOWED_FILE_TYPES in server/api/art/save-generated.post.ts (today a .flac is silently stored as png); add audio content types to the file serving route (it serves unknown types as octet-stream with nosniff); add an audio kind to ArtMediaKind in utils/artImageSource.ts (line 44 currently classifies ogg as video); make private audio rows playable (private rows need a Bearer header, which an audio element cannot send, so the store fetches a blob); audit every ArtImage consumer for fileType assumptions (admin /api/art/image and owner collection lists include private rows; public rails filter isPublic true and are safe; the offload in complete.post.ts throws on audio, which is caught, so keep audio out of the verbatim-offload set because offload writes to the public media origin); and add a claim-side supportsAudio gate like supportsInputImages (claim.post.ts) so audio jobs stay PENDING until an audio-capable relay exists. Merge this before t-011 (companion PRs, kind_robots first).
2026-10-02: kind_robots#3181 opened (audio ArtImage support, supportsAudio claim gate, private + no collection/offload for audio, audio media kind, admin queue views). Local: vue-tsc 0 errors, 406/406 contract scripts, prettier/lint ratchets hold.
2026-10-02: kind_robots#3181 merged (2de2d0b) after 38/38 checks green. No schema change. Audio jobs stay PENDING until a relay advertises supportsAudio (t-011).
<!-- note:end t-020 -->

## t-021 — Agent-run pipeline: pitch to finished MP4 with no human in the loop

<!-- note:begin t-021 -->
The browser exporter (t-014) needs someone at a screen, so the first-run trailer (t-015) needs a headless path. Write scripts/build_music_video.py in conductor. It drives the Kind Robots API with KR_API_TOKEN (presence checks only, never print it): create a MusicVideo, write lyrics, enqueue the song, plan scenes on the beat grid, enqueue scene stills and optional clips, and poll the ArtJobs. It then downloads the finished assets and assembles the MP4 locally with ffmpeg (present in cloud sessions), following the same timeline semantics as the browser compositor (scene start and end, Ken Burns or clip, cut or crossfade, the song as the audio track), and attaches the result via PATCH finalArtImageId once there is an upload path. It must resume a half-finished run from the MusicVideo doc and its ArtJobs instead of re-enqueueing, since renders take hours on the single 12 GB card. Unit-test the timeline-to-ffmpeg filter graph with fixtures, and add a dry-run mode that prints the plan without enqueueing anything.
scripts/build_music_video.py: resumable pitch-to-MP4 pipeline over the music-video API plus ffmpeg (Ken Burns zoompan, concat cuts, xfade crossfades, song audio); --dry-run and --wait. MP4 is written locally until an upload route exists (needed before t-022).
<!-- note:end t-021 -->

## t-023 — Upload route for a finished music video MP4 (kind_robots)

<!-- note:begin t-023 -->
scripts/build_music_video.py (t-021) assembles the MP4 but can only write it to local disk: nothing in kind_robots accepts a finished video file for a MusicVideo. Add an admin-only upload (e.g. POST /api/music-video/[id]/final) that stores the MP4 as a private video ArtImage (fileType mp4, never in a public collection, size-capped), sets the row's finalArtImageId, and serves it through the existing ArtImage file route; then teach the script to call it after assembly (with --no-upload to skip). Publishing stays t-022.
POST /api/music-video/[id]/final stores the MP4 as a private mp4 ArtImage (MUSIC_VIDEO_MAX_UPLOAD_MB, default 24) and sets finalArtImageId/EXPORTED; art file route now serves video/audio content types. Pipeline uploads after a CRF-ladder encode (conductor#5516).
<!-- note:end t-023 -->

## t-024 — Zuzu: Koala Assassin intro: creative brief and settings (comic-creator request)

<!-- note:begin t-024 -->
Silas, 2026-10-04: "submit requests that Zuzu Koala Assassin get an intro video as a music video project". Write projects/music-video/docs/zuzu-intro.md: pitch, 45-60 s at 16:9, genre and mood (a samurai-western title theme; instrumental or sparse chant), ACE-Step tags, style bible, the Kind Robots ComicSeries slug (zuzu-koala-assassin) and lane. STYLE: the comic's house lane wins over Krea 2 for this video (Illustrious furrytoonmix plus lane prefix/suffix and series negatives, tag prompts; t-025). Source of truth is comic-creator's BRAINSTORM-ROUND-3.md (Zuzu always serious, fennec siblings, action over exposition, a mature comic, violence allowed; the children never sexualised). settings.bannedTerms must cover comic-creator's secret list (comic-creator t-019); never write the secret itself in any prompt or doc. Name the vetted comic attempts to use as keyframes for character shots; cap real clips at 6 (Ken Burns elsewhere).
Merged conductor#5619: projects/music-video/docs/zuzu-intro.md (55 s brief, ACE-Step settings, bannedTerms, keyframes, shot list). t-028 must confirm comicLaneKey.
<!-- note:end t-024 -->

## t-025 — Comic-lane scene stills, comic keyframe picker and banned terms (kind_robots)

<!-- note:begin t-025 -->
settings.comicSeriesId / comicLaneKey route scene stills through the series' house lane (buildComicLaneEnqueueBody) instead of the krea2 constant in server/utils/musicVideoScenes.ts; prompt checks and the dedupe key become engine-aware. POST /api/music-video/[id]/scenes/keyframes maps ComicAttempt picks (selected, then liked) to image.source gallery, checked against the series. settings.bannedTerms is enforced for every engine (also usable for t-015's franchise guardrail). No schema change. On merge, check comic-film t-004/t-005 notes for anything waiting on this.
Merged (kind_robots#3218): settings.comicSeriesId/comicLaneKey route stills through the comic house lane; bannedTerms enforced on stills, LLM prompts and clip prompts; POST scenes/keyframes assigns vetted comic attempts. Picker UI rides t-027.
<!-- note:end t-025 -->

## t-026 — Aspect-correct clips: crop instead of stretch, aspect-sized frames, optional last frame (kind_robots)

<!-- note:begin t-026 -->
Clips take their size from the preset, so a 9:16 or 1:1 video still gets 1280x720 clips, and LTX resizes with crop disabled, stretching 2:3 comic art. Add an opt-in imageFit crop on /api/art/enqueue video jobs (LTX ImageScale crop center; WAN an explicit centre-crop ImageScale). Default stays stretch, so Scene Animator and the Video Generator are unchanged. clipFrameSize(preset, aspect) in multiples of 32; scene.motionPrompt (falls back to prompt) and motion.lastFrame next-scene. Verify WAN on the box when t-012 runs.
Merged (kind_robots#3217): opt-in imageFit crop on video jobs (default stretch unchanged), clipFrameSize per aspect, motionPrompt, motion.lastFrame next-scene.
<!-- note:end t-026 -->

## t-027 — Admin page controls: settings, song (generate or upload) and pipeline steps (kind_robots)

<!-- note:begin t-027 -->
/admin/music-video is a shell: every pipeline step is API-only and a new video gets the defaults (120 s, 16:9). Extract components/music-video/* (settings panel, song panel, pipeline bar, scene grid with keyframe picker) so comic-film's admin page can reuse them. The store owns every call; auto-fit grids, no viewport breakpoints in shared components.
t-013 and t-025 merged; ready.
2026-10-06 DONE: kind_robots#3247. /admin/music-video now drives the pipeline: musicVideoStore gained writeLyrics/generateSong/planScenes/writeScenePrompts/renderScene s/animateScenes/setSceneImage/uploadSceneImage/syncStatus (opening a video syncs finished renders into the doc; polls every 20 s while a render is queued). Extracted components/music-video/* pipeline bar, song panel (player + upload), scene grid (status, re-render, Replace image, hero-shot ticks, Animate N hero shots with preset picker) and settings panel; auto-fit grids, no viewport breakpoints. New POST /api/music- video/[id]/scenes/image. server/utils/artImageBytes reads offloaded stills, fixing clips.post.ts which read imageData only and failed every offloaded still with 'The scene still has no image data'. Same session: kind_robots#3245 (admin tab dropped by a YAML colon), #3246 (exporter/waveform song via the file route; the browser export had been silent). Not yet exercised live from the page; Silas to try it on MusicVideo 1.
<!-- note:end t-027 -->

## t-028 — Headless pipeline: song file, comic lane, clip requests, banned terms (conductor)

<!-- note:begin t-028 -->
scripts/build_music_video.py gains --song-file (upload through t-013's route, ffprobe for duration), --comic-series / --comic-lane / --banned-terms carried into settings, and a request_clips action (--clips, --clip-preset, at most 8 per call). Extend tests/test_build_music_video.py. comic-film's builder imports this plumbing.
t-013, t-025 and t-026 merged; ready.
Reviewed and squash-merged PR #5643 (CI green on latest attempt; 38 tests). Live-API path unverified (needs admin KR_API_TOKEN).
<!-- note:end t-028 -->

## t-030 — Scene cards, lyrics editor, animation presets and clips in the browser export (kind_robots)

<!-- note:begin t-030 -->
Silas, 2026-10-06, after trying t-027: the animate control belongs on each scene, with changing or uploading the image, animated or pan-and-zoom, the pan direction, and "a preset section to create/edit an animation prompt"; also "create and edit the song lyrics and then get it to generate from that same interface". Shipped in kind_robots#3249: a card per scene (image prompt, render, upload, Use art by ArtImage id, pan and zoom with direction or animated clip with its own prompt, preset picker, end on the next scene, Animate now, transition in, clip preview), a lyrics editor (sections, lock, reorder, rewrite one section or all unlocked, generate the song from them), named animation presets in settings.motionPresets, and clip playback in the browser exporter (it drew stills only, so hero shots never reached a front-end export).
<!-- note:end t-030 -->

## t-031 — Produce: pitch to attached final cut from the admin page (kind_robots)

<!-- note:begin t-031 -->
Silas, 2026-10-06: "a perfect setup would take a pitch, length, style suggestions, etc, and then an llm could fill in those elements and submit the art prompts immediately ... it should happen automatically when directed from the front end when all the images are created." kind_robots#3250: a Produce button drives brief, lyrics, song, scenes, prompts, stills, hero clips, then exports in the browser and attaches the final cut, resuming after a reload. Adds POST /brief (the LLM fills only blank settings and never replaces a full style bible), settings.heroShots, and the comic series and lane in the settings panel. It runs while the page is open; a server-side runner for a closed tab is the follow-up.
2026-10-06: kind_robots#3250 merged (with the settings panel's comic series and lane). Done; a live Produce run is Silas's to try.
<!-- note:end t-031 -->

## t-032 — Music video page: half-width stage, inline lyrics, checkpoint and LoRA picks (kind_robots)

<!-- note:begin t-032 -->
Silas, 2026-10-06, after trying t-030/t-031: "on a large screen, this should take up half of the space", the name and pitch whitespace and the broken final-cut still waste room, "lyrics should be editable in line, underneath the image that they represent", "settings should be on top with the name and pitch", "select the checkpoint we use for generation, and optionally add a lora to a specific image, or globally", hero selection should reveal the animation prompt, and "replace image should give us a choice from uploading or selecting from recent artjobs". kind_robots#3252 (merged): one Brief panel (title, pitch, settings, Checkpoint lane, global LoRAs); video picker and New video in one row; stage and scenes half and half on xl; scene cards with inline lyric lines, a Hero toggle that reveals the animation prompt, Replace image (upload, recent art jobs, ArtImage id) and a per-scene checkpoint and LoRAs; doc fields settings.imageLaneKey, scene.image.laneKey and scene.image.loraResourceIds.
<!-- note:end t-032 -->

## t-033 — Create the theme-song and Zuzu videos from prepared specs via the API (kind_robots)

<!-- note:begin t-033 -->
Silas, 2026-10-06: "I should [not] need to paste fields, you should be able to create the entire setup for our prompts, desired hero shots, lyrics, pitch, etc from api for both new projects." kind_robots#3254: POST /api/music-video/import ({ specKey } or a full { spec }) and a Create from spec picker on the page, with two bundled specs (Kind Robots theme for t-015, Zuzu intro for t-029) that a contract test checks against the doc normalizer, the banned terms and the prompt rules the render route enforces. A session holding an admin KR_API_TOKEN can POST the same body; without one, the page button is the one-click path.
<!-- note:end t-033 -->

## t-035 — Contract test pinning build_music_video.MAX_CLIPS_PER_CALL to the kind_robots clips route

<!-- note:begin t-035 -->
Kaizen from t-028 review: the constant mirrors kind_robots server/api/music-video/[id]/scenes/clips.post.ts MAX_CLIPS_PER_CALL by comment only. Add a test (skipped when no kind_robots checkout is present) that reads the route source and asserts the values match.

PR could not be opened; recover worker/music-video-t-035-clip-limit-contract-20261010-7c91e.

RAN 2026-10-11: tests/test_music_video_clip_batch_contract.py already on main (#5904);
kind_robots checkout absent here so it skips by design. Closed by reconciliation.
<!-- note:end t-035 -->
