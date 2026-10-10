# Comic Film — Design Brief

> **Zuzu-specific source index:** [worlds/zuzu](../../worlds/zuzu/README.md) contains the shared canon, character designs and art/model pointers for the first film. Comic Film's reusable engine remains production-agnostic.


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

**Update, 2026-10-04: an experience, not the whole story.** Silas: *"an animation doesn't need to tell this full story, but just needs to give an experience"* The source
is now Book One (`projects/comic-creator/issues/zuzu-koala-assassin-01/BOOK-ONE.md`), one continuous
arc from the massacre to the three of them on the road. The film picks the moments that carry its
feeling; it does not adapt every chapter. Old Komodo is not in Book One. Book One's signature frames
(the eye strip, silhouettes on the road, the lone survivor) are the natural anchors for those moments.

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

## Decisions (Silas, 2026-10-10)

Scope confirmed (t-002). The three open questions are answered:

- **Score:** an ACE-Step instrumental rendered on our own box. No supplied track.
- **Old Komodo:** not in issue 1.
- **Title card:** a generated art asset (a rendered still, not just burned-in text). Silas left the wording
  to us: *"not sure what i can say"*. The stinger is not required.

## Issue 1 beats (Silas, 2026-10-10)

This is the authoritative beat order for the issue 1 film and supersedes the "massacre to the road" framing
above. The apple tree moment is cut. Each beat is a shot or a short run of shots in `SHOT-LIST.yaml`.

1. Zuzu and the vagrant (the coyote) meet at the water.
2. The croc appears.
3. The croc bites off the vagrant's hand.
4. They kill the croc together.
5. Zuzu bandages the hand.
6. They part, walking away back to back.
7. Zuzu finds the village massacre.
8. He discovers the children; they follow him.
9. He gives them an apple (the apple tree scene itself is cut).
10. They follow him to the convent; he leaves them with the abbess.
11. At the convent the boy eats while the abbess eats the apple.
12. Zuzu reaches the next town and sees the walls of posters of missing children.
13. He runs back.
14. The abbess has tied up the children while the other nuns chant.
15. Zuzu appears and cuts the children free.
16. The abbess attacks; Zuzu is caught by the tentacle thing.
17. The abbess approaches the trapped Zuzu.
18. The abbess dies: reveal the sister holding the knife, which she drops.
19. Zuzu struggles; she picks the knife back up and hands it to him.
20. He throws it and kills the last chanting nun.
21. The tentacle thing is caught half in the portal and dies, segmented.
22. The three of them walk away together.

Silas's words, verbatim: *"zuzu and vagrant meet at the water, croc appears, croc bites off vagrants hand,
they kill croc together, zuzu bandages hand, they leave back to back, zuzu finds village massacre, discovers
children, they follow him, he gives them apple (we are going to cut the apple tree moment), they follow him to
convent, he leaves them with abbess, the boy eats while she eats apple, he gets to next town and sees all the
posters of children, he runs back, the abbess has tied up the children, other nuns are chanting, he appears and
cuts them free, abbess attacks, zuzu gets caught by tentable thing. abbess approaches while zuzu is trapped,
abbess dies and we see the daughter holding knife which she drops. zuzu struggles, she picks it back up and
hands to him, he throws it and kills the last chanting nun, the tentacle thing is caught half in portal and dies
segmented, the three walk together leaving."*

The VIDEO-GUARDRAILS.md rules still apply: the children's injuries stay implied and the buried-ruins secret
never appears. Beats 1-5 overlap the music-video intro (music-video t-029), so its vetted keyframes can be reused
once Silas's fidelity notes on that video are fixed.
