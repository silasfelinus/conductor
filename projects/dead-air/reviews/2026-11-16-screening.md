# Private screening review — 2026-11-16 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). Each final was downloaded from
Kind Robots by ArtImage id and its SHA-256 and byte count compared with
`production-state.json`. Frames were inspected once per second and on both sides of every
storyboard cut; loudness was measured per second. This session published nothing, but see
"The films are public, not private" below. This is an agent quality review, not Silas's
acceptance.

## MusicVideo 20 — CLAP CREDIT: Borrow an Audience (ArtImage 273075)

Status: **finished film, reviewed.** 15.0s, 1280×720 H.264 at 30 fps, mono AAC.
1,557,302 bytes, SHA-256 `cb31c6c7…cf08b0`, both matching the ledger. Completed 2026-11-15 PT.

What works:
- Five readable beats in storyboard order: the guitarist before a motionless crowd, the
  teal-suited lender and brass applause meter, the bought ovation, the collector's chrome
  vacuum with the jaguar shadow seated in the stalls, and the empty stage with the ON AIR lamp.
- Every cut lands on its storyboard time. Frames at 2.6/3.0s, 8.3/8.7s and 12.2/12.6s sit on
  the correct sides of the 2.8s, 8.5s and 12.4s cuts.
- All five captions are legible and match the authored overlays.
- **The 2026-11-14 audio fix holds.** Voiceover runs to about 9s at −18 dB mean; the station
  bed carries 9–12s at about −32 dB; the sign-off chime sits at 12–14s (−26 dB mean, −12 dB
  peak). The only run below −45 dB is the final 0.86s, which is the authored
  `silent_tail_seconds: 1.0` "dead-silent last beat", not dead air.
- The ON AIR lamp lettering in s5 rendered correctly, with no pseudo-lettering elsewhere.

Defects:
- **The reveal is spent early.** The jaguar is authored as the s4 reveal (a shadow that stays
  seated when the applause is repossessed). A literal black big cat already sits at the left
  edge of s2 and fills the right foreground of s3, blue cheek streaks included. Cause: the
  jaguar is described in the episode-wide `visual_style`, which is appended to every still
  prompt. Authoring fix for future briefs: keep reveal-only motifs out of `visual_style` and
  name them only in the shot that reveals them.
- **No GPU motion shot.** s4 is authored `motion: clip`, but the ledger records
  `gpu_animated_shots: 0` and five kinetic shots. See "Scheduled passes arrive hours late".
- s4 and s5 shift from the retro cel look of s1–s3 to a flatter graphic style. It reads as a
  deliberate hard cut here because the story turns at s4, but it was not authored.
- s5 keeps three lit audience heads in the foreground although the brief says everyone has
  left. Minor: the stage itself is empty and the shadow gag still reads.

## MusicVideo 21 — The Apology Orchard (ArtImage 273690)

Status: **finished film, reviewed.** 15.0s, 1280×720 H.264 at 30 fps, mono AAC. 1,960,755
bytes, SHA-256 `0ab37fbf…910bc7`, both matching the ledger. Completed 2026-11-16 03:21 PT by
workflow run 43856792294, which this session dispatched by hand (see "Scheduled passes arrive
hours late").

What works:
- s4 is the strongest frame of the week: a whole folk-art orchard of worried face-fruit, the
  gardener small at the roots and the yellow receiver beside them.
- s3's fruit with a calm painted face in a felt-sleeved hand sells the premise in one image.
- Cuts land on 2.6s, 5.5s, 8.4s and 12.3s as authored, and all five captions are legible.
- Audio is clean: voiceover to about 12s at −18 dB mean, bed at 12s, chime at 13–15s, and no
  run below −45 dB longer than 0.6s.

Defects:
- **The punchline is missing.** s5 is authored as a fruit "with the gardener's face hanging
  nearest the lens", the visual answer to "it may be growing you next". The render shows a
  plain peach with no face, so the film ends on a basket and a fruit, not on the reveal.
- **s2 lost its surreal detail.** The fruit were authored as small ceramic ears; the render
  shows ordinary apples and plums, in a semi-photoreal style.
- **Five shots, four looks.** s1 is felt cut-paper, s2 semi-photoreal, s3 a photoreal macro,
  s4 painted folk art and s5 clay-like 3D. Only s1 and s4 match the authored "cut-paper and
  hand-painted garden television".
- s1 put the gardener on a vintage television screen among the trees instead of standing in
  the orchard beside a camera tripod. It reads well as public access, but it was not authored.
- No GPU motion shot: s4 is authored `motion: clip` and exported kinetic, as with Clap Credit.

The dropped face in s5 and the dropped ears in s2 are the same class of still-versus-prompt
drift that dead-air/t-010 already tracks; this review is added evidence for its proposed
check before export.

## The films are public, not private

**Every Dead Air film so far has been publicly listed and playable on kindrobots.org.**
Checked without credentials on 2026-11-16 at about 03:35 PT:

- `GET /api/music-video` (the visitor gallery feed) listed MusicVideos 18, 19, 20 and 21 with
  `isPublic: true` and `isOwner: false`.
- `GET /api/music-video/21/video` returned HTTP 200, `video/mp4`, 1,960,755 bytes: the whole
  final cut. `GET /api/music-video/21` returned the full record.
- The underlying ArtImage file is private (`/api/art/images/273690/file` returned 403), but
  the music-video endpoint serves it for any record whose `isPublic` is true.

Cause: Kind Robots creates a MusicVideo with `isPublic` true unless told otherwise, and
`dead_air_produce.py` "never publishes or changes isPublic", so each film has been public
from the moment it exported. That contradicts the project README ("New films remain private
drafts until Silas explicitly approves publication") and the dead-air/t-007 release gate.
The 2026-11-14 review's "Nothing was published" was therefore wrong for MusicVideos 18 and 19.

This session attempted to set the four records to `isPublic: false`; the session's permission
guard refused the change to live site data, so **they are still public**. The decision and
the fix are filed as dead-air/t-012 (needs-human) with a security flag in
`projects/dead-air/TALKBACK.md`.

## Scheduled passes arrive hours late

The workflow's four overnight passes are scheduled for 01:00, 01:45, 02:30 and 03:15 PT.
The render-progress commits show when passes actually ran:

| PT date | Passes that saved progress (UTC) | Roughly, in PT |
| --- | --- | --- |
| 2026-11-13 | 17:06, 17:23, 18:00 | 09:06–10:00 |
| 2026-11-14 | 15:43, 16:06, 16:42 | 07:43–08:42 |
| 2026-11-15 | 08:59 (push-triggered), then 16:14 | 00:59, then 08:14 |
| 2026-11-16 | 09:01 (push-triggered); none of the 09:45 or 10:30 UTC passes had run by 11:20 UTC | 01:01 only |

Two consequences:
- Films finish around 08:00–10:00 PT instead of by 03:15 PT, which misses the morning
  screening deadline.
- The optional GPU clip can only be requested inside the first 90 minutes of the two-hour
  budget, and only after the stills exist. With no second pass inside that window the clip is
  never requested, so every film falls back to an all-kinetic cut.

On 2026-11-16 this session dispatched the workflow by hand at 03:20 PT once all five Apology
Orchard stills were DONE. A durable fix (follow-up passes that do not depend on GitHub's
schedule queue) is filed as a separate ready task rather than widened into this cycle.
