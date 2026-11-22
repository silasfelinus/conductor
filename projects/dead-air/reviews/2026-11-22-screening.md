# Private screening review — 2026-11-22 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). I downloaded the final from Kind
Robots by ArtImage ID. Its SHA-256 and byte count match `production-state.json`, and the
producer recorded `is_public: false`. I checked frames at each shot's midpoint, found cuts with
FFmpeg scene detection, and checked audio with `silencedetect` (−45 dB, 0.1s) and `volumedetect`.
Nothing was published. This is an agent quality review, not Silas's acceptance.

## MusicVideo 27 — Silence by Mail (ArtImage 278942)

Status: **finished private film, reviewed.** The 01:30 PT pass started it. All five stills
(ArtJobs 76608–76612) sat PENDING for 27,095s (7.5h) and were first seen done at 09:02 PT, when
the film was exported. 15.0s, 1280×720 H.264, AAC; 1,712,526 bytes, SHA-256 `530fb089…752b3`.
Cuts land at 2.8 / 5.8 / 8.8 / 12.4s, exactly as authored. No silence run below −45 dB. Mean
−19.9 dB, **peak −1.8 dBFS**, so the 2026-11-18 limiter fix still holds.

What works:
- **This is the first film to keep the yellow-television reveal for the reversal shot from
  brief to render.** The guard added after MV26 (`test_yellow_television_reveal_waits_for_the_reversal_shot`)
  kept the station out of s1–s3. It first appears in the s4 control room and comes back in the s5 tag.
- **The 1970s mail-order look carries all five shots.** Harvest gold cabinets, burnt orange
  wallpaper, avocado shag and amber cork-stopper jars are all painted, not photoreal.
- **Every premise beat reads without the voiceover.** s1 has both noise sources, the lawnmower
  through the window and the child's tuba at the table. s2 shows the powder-blue carrier with
  the crate. s3 has mist rolling over the shag and the tuba parked in the corner. s4 has the
  headphoned engineer filling a glowing jar among shelves of filled ones.
- **No fake lettering in the pictures.** The only text is the authored caption overlay.

Defects:
- **s4 motion lost again, and this time the state hid it.** s4 was authored `motion: clip`, but
  the stills took 7.5h, so the two-hour deadline had passed and no clip was requested. The state
  row still said `optional_clip_skipped_for_congestion: false`, so it read as though nothing had
  been skipped. Five kinetic shots, no GPU clip: the sixth film running without its hero clip.
- **The jar glow rendered as tea-light candles.** "Each jar holding a soft pale glow" became a
  flame inside every jar in s2 and s4. The prompt made the light literal, as "like snow" did in
  MV26. Future briefs should name the light as mist or haze ("pale luminous mist inside").
- **s4 has two yellow televisions.** One is the single-eyed station. The other is an ordinary
  yellow set with rabbit ears, which weakens the "one watching eye" image.
- **s5's television shows a blank screen, not an eye.** At kitchen scale the station's face is
  lost, so the closing "watching eye" has to be read from s4.

Fixed this session:
- `dead_air_produce.optional_clip_skip_reason` records why an authored clip was not requested
  (`deadline` or `congestion`) as `optional_clip_skip_reason` on the state row.
  `tests/test_dead_air.py::test_clip_skip_reason_names_the_deadline_not_just_congestion` covers it.
  MV27's row is backfilled to `deadline` from the 27,095s still wait. The old boolean is kept
  for compatibility.

Carried forward (not fixed here): scheduled-pass lateness and long still queues (t-011) are the
real reason the hero clip keeps being dropped. A recording fix makes this visible but doesn't
speed up the queue.
