# Private screening review — 2026-11-18 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). The final was downloaded from
Kind Robots by ArtImage ID, and its SHA-256 and byte count were compared with
`production-state.json`. Frames were checked at each shot's midpoint and 0.2s either side of
every storyboard cut. Loudness was measured per audio window, and with `silencedetect` at
−45 dB (0.1s minimum) and `volumedetect`. Nothing was published. This is an agent quality
review, not Silas's acceptance.

## MusicVideo 23 — The Empty Square (ArtImage 275278)

Status: **finished private film, reviewed.** It runs 15.0s at 1280×720, H.264 at 30 fps,
with mono AAC audio. The file is 1,771,082 bytes with SHA-256 `521eea23…20b0d9`, and both
match the ledger. The live MusicVideo record reads `isPublic: false`. The overnight pass
started it at 00:56 PT, and this session's 02:45 PT `--resume` found all five stills done
(ArtImages 275262–275266) and exported it.

What works:
- **The reveal survives.** The yellow one-eyed receiver appears only in s4, peering out of
  one apartment in a grid of television-frame rooms. That fixes the MV22 defect, where the
  mascot appeared in every shot. The brief's `visual_style` still names a "single yellow
  television eye", but the stills don't paint it in. Through s1–s3 the only yellow is a lit
  arched doorway (s2) and a tea table (s3).
- **One consistent look across all five shots:** salmon arches, cyan windows, brass elevator
  doors and cobalt checkerboard floors.
- **s5's recursive tag works.** The television shows the same room containing a smaller
  television, so "YOU ALREADY LIVE HERE" lands visually.
- **The cuts land on the storyboard:** 2.6s, 5.5s, 8.4s and 12.3s. All five captions are
  legible and match the authored overlays.
- **Audio has no run below −45 dB, not even a 0.1s one.** The voiceover carries at about
  −16 to −21 dB RMS and the station bed holds about −31 dB after it. The last half-second
  (the chime decay) is at −32 dB mean.

Defects:
- **Photoreal people, not airbrush.** In s1 and s3 the people are glossy stock photography
  over painted sets. The brief asks for "original retro painted advertisement" and "retro
  airbrush". The sets read as 1980s, but the people read as 2020s.
- **The film-strip idea is missing in s2 and s3.** s2 shows ordinary pastel apartment towers
  rather than models "suspended between glowing strips of analog television film". s3 is a
  normal room whose window is black, not a home inside a filmstrip square. The premise (a
  home inside deleted broadcast frames) only becomes visible in s4.
- **Brief identity cues didn't carry through.** The brief describes a nonbinary realtor and
  an older queer couple. The renders fell back to generic defaults. The prompts need more
  concrete visual direction there, not adjectives the model drops.
- **The sound brief is unused.** It calls for a synth fanfare, an elevator bell, a key jingle
  and a tape-splice click, but the provisional mixer still ignores `sound` (as noted for
  MV22).
- **No GPU motion.** s4 is authored `motion: clip`, but the ledger again records
  `optional_clip_skipped_for_congestion: true` and five kinetic shots.
- **Audio peaks at −0.2 dBFS.** The mean is −19.4 dB. Fixed this cycle (below).

## Fixed this cycle

- **Root cause of the near-0 dBFS peaks (MV22 0.0, MV23 −0.2).** The mix used
  `alimiter=limit=0.93` with FFmpeg's default `level=1`. That auto-level adds make-up gain
  equal to 1/limit, so every limited peak went back to full scale. The mix now uses
  `alimiter=limit=0.8:level=0`, about −1.9 dBFS. A worst-case loud synthetic voice, run
  through the MP3 mix and then AAC, now peaks at −1.1 dBFS (0.0 before). A regression test
  covers it.

## Next

- Storyboard authors: put the medium into the subject itself ("airbrushed illustration of a
  …") rather than only into the trailing style phrase, so faces stop rendering as
  photographs.
- Use concrete visual details where an identity matters, and treat the s2/s3 filmstrip
  framing as the premise, not decoration.
- The congestion clip skip and the unused `sound` field remain open (t-011 and the earlier
  audio note).
