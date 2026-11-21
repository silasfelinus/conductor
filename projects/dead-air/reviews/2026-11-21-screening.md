# Private screening review — 2026-11-21 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). The final was downloaded from Kind
Robots by ArtImage ID. Its SHA-256 and byte count match `production-state.json`, and the
producer recorded `is_public: false`. Frames were checked at each shot's midpoint, cuts with FFmpeg
scene detection, and audio with `silencedetect` (−45 dB, 0.1s) and `volumedetect`. Nothing was
published. This is an agent quality review, not Silas's acceptance.

## MusicVideo 26 — The Ghost Exit Interview (ArtImage 277935)

Status: **finished private film, reviewed.** Started by the 00:56 PT pass. This session's 02:51 PT
`--daily --resume` found all five stills (ArtJobs 76346–76350) done and exported the film. 15.0s,
1280×720 H.264, AAC; 1,731,922 bytes, SHA-256 `b5376a4e…977be`. Cuts land at 2.6 / 5.5 / 8.4 /
12.3s. No silence run below −45 dB. Mean −19.6 dB, **peak −1.8 dBFS**, so the 2026-11-18 limiter
fix still holds.

What works:
- **The 1990s training-cartoon look carries all five shots.** Lavender cubicles, teal rolling
  chairs, mint fluorescent panels, fax machines, and translucent pearl-gray ghosts with
  expressive faces. All are painted cartoon; none are photoreal.
- **s1 sets up the premise clearly**: a weary HR manager in turquoise glasses holds a survey
  across from a ghost.
- **s4 and s5 read as a reversal and a tag.** In s4 the TV's eyes glow over an office of teal
  chairs. In s5 a lone manager faces the one-eyed receiver.

Defects:
- **The reveal was spent in s2, and the cause is authoring, not rendering.** The brief's s2
  `image_prompt` itself placed "a yellow one-eyed square television" on the reception desk, so
  the station appears with a full face two shots before "WHO INTERVIEWS THE STATION?". This is
  the same lesson as MV22/MV24, reached by a different route: the visual_style guard can't
  catch a reveal written into an early shot.
- **s3 roles swapped.** The "elderly ghost gardener" rendered as a living man in gardening
  gloves, and the "skeptical manager" rendered as the ghost. When an adjective like "ghost"
  sits on one of two people, the model can attach it to the wrong one. Future briefs should
  state the translucency on the figure itself ("a translucent pearl-gray elderly gardener").
- **s5 turned a simile into literal weather.** "White forms scattered like snow" became snow
  caps on chairs and ghosts. Ghosts also remain in s5, although s4 says every ghost departs.
- **s4 motion lost again.** It was authored `motion: clip`, but the clip was skipped for
  congestion: five kinetic shots, no GPU clip.

Fixed this session:
- `tests/test_dead_air.py::test_yellow_television_reveal_waits_for_the_reversal_shot` fails if
  any unrendered brief (dated 2026-11-21 on) paints the yellow television before its reversal
  shot. It fails on the MV26 brief and passes on the whole 7-day runway.
