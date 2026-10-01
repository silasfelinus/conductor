# Music Video — Design Brief

date: 2026-10-01
status: draft (Silas-directed session; scope confirmation t-002 is a soft checkpoint and blocks nothing)
author: claude

## What it is

A Suno-inspired music video creator, built on our ComfyUI. An admin gives a **pitch** plus optional **length, genre, BPM and mood**. The tool writes **structured lyrics**, generates the **song** on Comfy, lets the admin **edit the lyrics**, **set where scenes change** on a beat grid, **generate or upload an image for each scene**, and **compiles everything into one MP4** with the song.

Silas's pitch, 2026-10-01, verbatim: *"a music video creator. similar to and inspired by suno. we should be able to give it a pitch, optional settings like length of time, genre, beats, and have it create lyrics, also edit lyrics, set when to change scenes, add or upload images for each scene beat, and compile everything. this should use our comfy as the backend."*

Decided with Silas in session: **the song is generated on Comfy from day one**, and the **first release is admin-only** (like Scene Animator).

## Who it serves

Silas first: he writes medleys and songs and wants to turn an idea into a watchable video without leaving Kind Robots. Later (t-019, after acceptance) signed-in Kind Robots users, metered by mana.

## The flow

1. **Pitch and settings.** Free-text pitch; optional duration, genre, BPM, mood, vocal type, language, a shared style bible for the visuals, aspect ratio.
2. **Lyrics.** Structured sections (verse, chorus, bridge), editable line by line, regenerate per section, lock sections.
3. **Song.** Generated on Comfy (ACE-Step) from the style tags and lyrics, or uploaded (Suno exports, own recordings) as a fallback lane.
4. **Timeline.** Waveform plus beat grid. Place scene markers that snap to beats or bars. Lyric lines are assigned to scenes.
5. **Scenes.** One image per scene: written by an LLM from the lyric span and style bible, or uploaded, or picked from the gallery. Regenerate any one. Optional per-scene motion clip.
6. **Compile.** In the browser: stills (and clips) with Ken Burns and crossfades, the song as audio, exported as MP4.

## What already exists, and what does not (verified in code, 2026-10-01)

| Stage | Status | Evidence |
|---|---|---|
| Lyrics (LLM) | Ready | `POST /api/generate/text` in kind_robots: provider-agnostic, mana-metered |
| Still per scene | Ready | `POST /api/art/enqueue` engines `krea2`, `flux2`, `flux`, `zimage`, `kontext`; LoRAs via `loraResourceIds` |
| Scene clip (optional) | Ready but slow | `/api/video/generate` runs ltx or wan; 3 to 4 second clips; up to about an hour each on the single 12 GB card |
| Pick image from gallery | Ready | ArtImage gallery |
| Upload image | Image-only | `server/api/art/upload.post.ts`: PNG, JPEG, WebP, 15 MB cap, any signed-in user |
| Song generation | **Missing** | No audio workflow or engine; no ACE-Step model provisioned; the LTX endpoint has audio switched off |
| Audio through the relay | **Missing** | The live relay is `ops/home-server/relay_media_agent.py` (overrides `relay.run_comfy` and recomputes `want_video`); `find_output_file` in `relay_agent.py` knows only video or image; `save-generated` has no audio file types, so a `.flac` would be silently stored as `png` |
| Beat grid | Derive from BPM | `audioAnalysisHelper` is tuned for monophonic vocals and exports no onset times |
| Compile to MP4 | **Missing** | No ffmpeg in the kind_robots container; Comfy `CreateVideo` takes images, fps and optional audio but is per-frame |

Cloud sessions cannot reach ComfyUI (`projects/art-generator-connect/docs/pipeline-architecture.md`). It runs on Silas's Windows render box under pm2 with one 12 GB GPU, reached through the pull-based relay.

## Architecture

```
/admin/music-video  (Nuxt page, art-first stage UI; Pinia musicVideoStore owns ALL API calls)
  lyrics      -> POST /api/generate/text                                         (existing)
  song        -> /api/art/enqueue engine "acestep" (jobEngine COMFY, payload.media "audio")
                 -> ArtJob -> kr-relay -> ComfyUI ACE-Step -> ArtImage(fileType mp3, isPublic false)
  scene still -> /api/art/enqueue (krea2 default) | admin image upload | pick from gallery
  scene clip  -> /api/video/generate (ltx or wan)            [opt-in per scene]
  document    -> MusicVideo model (one additive migration; timeline and scenes as JSON)
  compile     -> in-browser canvas compositor + WebCodecs and a muxer -> MP4 download
```

Decisions and why:

1. **Home is kind_robots**, admin-only at `/admin/music-video`. Conductor holds the roadmap and this brief. Same pattern as music-mentor, scene-animator and cthulhuquarium. `projects/kind-robots/BOUNDARY.md` scopes to the kind-robots app project only; sibling projects ship Prisma changes in kind_robots under AGENTS.md's additive-migration rule, so it does not apply here.
2. **No new queue or renderer.** Every GPU job is an ArtJob carrying a `musicVideo: {videoId, sceneId}` provenance block and a dedupe key modeled on scene-animator's. Scene status is derived from ArtJobs and never stored. (Scene Animator's own rule: *ArtJobs are the ledger.*)
3. **Audio rides ArtImage**, which already stores mp4 and webm through `fileType`: no schema change for audio. The engine needs no migration either; video already uses `jobEngine: 'COMFY'` plus `payload.media`. Do not add audio to the verbatim-offload set: offload writes to the public media origin and would defeat `isPublic: false`.
4. **Song output is MP3** (`SaveAudioMP3`), not FLAC: a 4-minute FLAC is about 47 MB of base64 inside the `/complete` transaction.
5. **Song model is ACE-Step.** v1 has documented native Comfy nodes (`TextEncodeAceStepAudio`, `SaveAudio`). v1.5 reportedly does up to 10 minutes on 12 GB-class cards, but its native-Comfy support is unconfirmed, so t-003 is a spike that picks the variant. The model files must be staged on the Alexandria share first, because `sync-comfy-models.sh` only copies share to local disk.
6. **Prompt provenance for audio needs a change.** `enrichArtJobPayload` (`artJobProvenance.ts`, called from `claim.post.ts`) requires the top-level `promptString` to equal a workflow string whose key matches `(^|_)(prompt|text)($|_)`. `TextEncodeAceStepAudio` uses `tags` and `lyrics`, so every job would be rejected. t-010 extends the pattern and sets `promptString` to exactly the tags string. Lyrics stay out of `promptString` because `assertQueuedArtPromptContract` would reject lyric text.
7. **A capability gate, not a hidden flag.** The relay advertises `supportsAudio` (like `supportsInputImages`); the claim endpoint leaves audio jobs PENDING until an audio-capable relay exists. An unpatched relay otherwise reports success and stores audio as a png.
8. **Compile in the browser** (recommended; Silas can redirect). Zero infrastructure, the same canvas renderer drives scrub-preview and export, and it does not compete with the single GPU for queue time. Chromium-first (WebCodecs) is fine for admin-only. A relay-side ffmpeg compile job is the documented later upgrade for unattended export.
9. **Stills first.** Default motion is client-side Ken Burns plus crossfade. ltx or wan clips are an opt-in per scene with a runtime hint, because they are slow on this hardware.
10. **Scene prompts obey the Krea 2 contract** in `ART-PROMPTS.md`: concrete nouns first, no negations, no art-direction jargon, no conditionals. A validator rejects bad prompts before enqueue. A shared style bible (plus an optional LoRA and a fixed-seed policy) is appended to every scene prompt for visual coherence.
11. **Lyric timing is approximate.** Lines are spread across sections by section length and are user-adjustable. Forced alignment (Whisper) is out of scope for v1.
12. **An audio upload fallback exists** (a new admin-only route, since the existing upload is image-only) so lyrics, timeline, images and compile can be built and tested before the Comfy audio lane is deployed.
13. **Mana.** An acestep job gated as `comfy` bills like a 1024 square still, acceptable while admin-only. t-019 needs duration-based billing.

### Timeline document (the contract between lanes; JSON on `MusicVideo`)

```ts
type MusicVideoDoc = {
  version: 1
  pitch: string
  settings: { durationSec: number; genre?: string; bpm?: number; mood?: string
              vocal?: 'female' | 'male' | 'duet' | 'instrumental'; language?: string
              styleBible: string; loraResourceIds?: number[]; aspect: '16:9' | '9:16' | '1:1' }
  lyrics: { sections: { id: string; kind: 'intro'|'verse'|'pre-chorus'|'chorus'|'bridge'|'outro'
                        lines: string[]; locked: boolean }[] }
  song:   { source: 'comfy-acestep' | 'upload'; artImageId?: number; jobId?: number
            durationSec?: number; bpm?: number; seed?: number; tags?: string }
  timeline: { beatGrid: { bpm: number; offsetSec: number; beatsPerBar: number }
              markers: { id: string; atSec: number; snap: 'beat'|'bar'|'free' }[] }
  scenes: { id: string; startSec: number; endSec: number
            lyricRefs: { sectionId: string; lineIdx: number }[]
            prompt: string; promptSource: 'llm' | 'user'
            image:  { source: 'generated'|'upload'|'gallery'; artImageId?: number; jobId?: number }
            motion: { kind: 'kenburns'|'clip'; preset?: string; clipArtImageId?: number; jobId?: number }
            transition: 'cut' | 'crossfade'; transitionSec: number }[]
}
```

The compositor consumes only `song`, `timeline` and `scenes`, so it can be built against fixtures before any lane that fills them exists. Timeline math is pure code in `utils/`; the compositor lives in `stores/helpers/` (kind_robots has no root `composables/`, and components never call APIs).

## MVP scope

Four lanes, parallel across sessions (one claim per session at a time):

- **Studio core, no GPU:** t-004 model and API, t-005 lyrics, t-006 page and store, t-007 timeline editor, t-013 audio upload fallback.
- **Scenes:** t-008 prompts, validator and per-scene images, t-009 motion options.
- **Audio on Comfy (the gated lane):** t-003 spike, t-020 ArtImage audio support, t-010 workflow and engine, t-011 relay, t-012 stage models and deploy (a hard gate: Silas's render box).
- **Compile:** t-014 browser compositor and exporter, then t-015 acceptance of a roughly 60 second real video.

Then m3: responsive and art-first polish (t-016), project art (t-017), docs (t-018), and opening it to users (t-019).

## Out of scope / guardrails

- No second queue or renderer. ArtJob only.
- No publishing, no public route, no payments, no secrets or DNS changes. Everything is admin-only until t-019, which parks at `needs-human`.
- Cloud sessions never deploy to the render box. The relay and model staging (t-012) is Silas's hands-on gate; sessions stage the commands and stop.
- No forced lyric alignment, no server-side ffmpeg, no save-to-server of the final MP4 in v1.
- No `prisma migrate reset`, ever; the one migration is additive (CREATE TABLE).
- Do not mirror `liveUrl`, `channelKey` or `tabKey` into `project-overrides.yaml` (kind_robots AGENTS.md forbids it); placement lives in kind_robots `utils/projectPlacements.ts`.

## Open questions (none block development)

1. **ACE-Step v1 or v1.5 on Comfy** (t-003 decides; v1.5 native-Comfy support is unconfirmed).
2. **Compile location.** Browser is the pick; revisit a relay ffmpeg job if admin-side export proves unreliable or unattended export is wanted.
3. **Safari and Firefox export** when this opens to users (t-019).
4. **Priority slot.** Placed just behind the top-10 band; Silas can promote it.
5. **Render capacity.** The last logged backlog was about 1,464 pending jobs, oldest about 39 hours; a 30-scene video is about 30 stills at roughly 400 seconds each.

## Related projects

- **coat-dance** (active, content): wants "per-section renders, restitch, music alignment" for one specific 2006 video. This project's exporter is the reusable engine it will want at t-008; nothing in coat-dance changes now.
- **scene-animator** (the architectural precedent) and **art-generator-connect** (the generation backend and relay docs).
- **music-mentor** (client-side Web Audio analysis; reusable pieces, though not tuned for beat onsets) and **text-generation** (the lyric path).

## Sources

- Repo evidence: `projects/art-generator-connect/docs/pipeline-architecture.md`, `ops/home-server/relay_media_agent.py`, `ops/home-server/relay_agent.py`, `tests/test_relay_agent_video.py`; kind_robots `server/api/art/enqueue.post.ts`, `save-generated.post.ts`, `claim.post.ts`, `server/utils/artJobProvenance.ts`, `server/api/generate/text.post.ts`, `docs/scene-animator.md`, `utils/videoPresets.ts`.
- External, to be re-verified by t-003 rather than trusted: [ACE-Step in ComfyUI (Comfy docs)](https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1.md), [ComfyUI Wiki ACE-Step guide](https://comfyui-wiki.com/en/tutorial/advanced/audio/ace-step/ace-step-v1), [Comfy CreateVideo node](https://docs.comfy.org/built-in-nodes/CreateVideo.md), [ACE-Step 1.5 README](https://cdn.jsdelivr.net/gh/ace-step/ace-step-1.5@main/README.md).
