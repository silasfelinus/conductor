# Comic Film — Design Brief

date: 2026-10-04
status: active
author: Claude session (Zuzu comic work), from Silas's request

## What it is

Silas, 2026-10-04: *"a regular video project where the story beats for issue 1 are turned into an
animated movie ... this might highlight some gaps in their capabilities, so please upgrade as
needed so this can be manifested."*

Comic Film turns a comic issue from the Kind Robots Comic Studio into a short animated film on our
own ComfyUI backend:

1. **Shot list:** beats become shots, each with a duration, a camera move and, rarely, on-screen text.
2. **Keyframes:** one still per shot, rendered in the comic's house checkpoint or picked from comic attempts Silas already vetted.
3. **Clips:** LTX/WAN image-to-video clips on the shots that earn motion; everything else gets Ken Burns.
4. **Score:** ACE-Step instrumental or an uploaded track. The comic has **no dialogue or narration** (Silas,
   2026-10-04). The only words are diegetic signs and posters, plus a title card.
5. **Delivery:** one MP4 stored as a private ArtImage.

The first film is **Zuzu: Koala Assassin #1**. The tooling is generic, so later issues and other comics reuse it.

## Who it serves

Silas, as director and editor, at an admin page `/admin/comic-film`. Agents also run it headless.
A finished film is a buzz piece for the comic and for Kind Robots once Silas approves it. Publishing
is a separate, publish-gated step.

## Architecture (decided 2026-10-04)

**A film is a `MusicVideo` row with `kind = 'film'`.** The music-video project (active since
2026-10-01) already has almost every part a film needs:

- a timeline document of scenes with start and end times, a still and a motion setting for each, and transitions;
- ArtJob-backed still and clip rendering;
- status sync;
- an MP4 upload route;
- a headless pitch-to-MP4 assembler (`scripts/build_music_video.py`, ffmpeg).

A separate `ComicFilm` model would duplicate the document normaliser, the ArtJob sync, the clip
route, the final upload and the assembler. Kind Robots' AGENTS.md says to audit sibling
implementations and prefer one shared version, so the film extends the music video instead.

- **Kind Robots: one additive column, `MusicVideo.kind` (`music | film`).** Schema-affecting. Film-only document fields:
  - `scene.shot = {beat, camera, caption}`
  - `settings.comicIssueId`
  - `scene.comicSlotId`

  ArtJobs carry `projectSlug: comic-film` through `projectSlugFor(kind)`.
- **Kind Robots: `/admin/comic-film`** reuses the music-video page components (music-video t-027) and adds a shot-list editor.
- **Conductor: `scripts/build_comic_film.py`** imports `build_music_video.py`'s plumbing. It reads `films/<issue>/SHOT-LIST.yaml`. The song is optional (silence if there is none). Captions are burned in from `.ass`.

**Upgrades this depends on in music-video** (filed 2026-10-04; they also serve the Zuzu intro video):

| Task | Upgrade |
|---|---|
| t-013 | song upload |
| t-025 | comic-lane stills, keyframe picker, `bannedTerms` |
| t-026 | crop instead of stretch, aspect-sized clips, last frame |
| t-027 | page controls |
| t-028 | headless script flags |

Conductor's audit does not allow `depends_on` across projects. Waits on those tasks are therefore
written into notes, and each music-video task says what to release here when it merges.

## MVP scope

- **Zuzu #1 shot list, written by an agent:** 2.5 to 4 minutes, about 30 to 45 shots.
- **Clip budget:** at most 12 real LTX clips. They run 30 to 90 minutes each on the single 12 GB card, so they go overnight. The rest use Ken Burns.
- **Keyframes:** character shots come from vetted comic attempts. Other shots are rendered in the house lane, currently furrytoonmix, which the bake-off in comic-creator t-018 may replace.
- **Text:** none spoken or narrated. On-screen text is limited to the title card and inserts of diegetic signs or
  posters (for example the Hollow Bell arch, or a later chapter's missing-child posters). Burned in with the same
  caption machinery, using `kind: title | sign`.
- **Delivery:** a 720p MP4 under the 24 MB upload cap, then parked for Silas's verdict.

## Guardrails

- **Comic canon and the secret:** `projects/comic-creator/issues/zuzu-koala-assassin-01/VIDEO-GUARDRAILS.md`.
  - The buried human-ruins twist never appears in any prompt, caption or title.
  - `settings.bannedTerms` enforces this on the server.
  - The shot list is written by an agent that leaves the secret out on purpose.
- **Mature:** Silas, 2026-10-04: *"I never explicitly said zuzu was teen rated. This is a mature comic with mature themes."* Violence can be on screen. The children are never
  sexualised, and their injuries stay implied (VIDEO-GUARDRAILS.md). Mature renders need the
  Kind Robots maturity flag so galleries filter them.
- **Generation:** ArtJob is the only generation queue. Renders are private. Prompts follow the contract of the engine that renders them.
- **Publishing is a gate:** placing a film anywhere public parks at needs-human (`gate_reason: publish`).

## Open questions (for Silas, non-blocking)

- **Score:** an ACE-Step instrumental (needs music-video t-012 staged on the box) or a track he supplies?
- **Old Komodo:** does his eruption from the sand belong in issue 1's film as the action set piece, or wait for a later issue? The default is to leave him out, because the issue 1 script doesn't have him.
- **Title card wording,** and whether to end on the optional stinger (a third set of sandal prints at the arch).
