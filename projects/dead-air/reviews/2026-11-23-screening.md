# Private screening review — 2026-11-23 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). I downloaded the final from Kind
Robots by ArtImage ID. Its SHA-256 and byte count match `production-state.json`, and the API
reports MusicVideo 28 as `isPublic: false`, status `EXPORTED`. I checked frames at each shot's
midpoint, found cuts with FFmpeg scene detection, and checked audio with `silencedetect`
(−45 dB, 0.1s) and `volumedetect`. Nothing was published. This is an agent quality review, not
Silas's acceptance.

## MusicVideo 28 — Rerun Laundromat (ArtImage 279777)

Status: **finished private film, reviewed.** The 00:55 PT pass started it. All five stills
(ArtJobs 76821–76825) sat PENDING for 43,966s (12.2h) and were first seen done at 13:08 PT, when
the film was exported. 15.0s, 1280×720 H.264, AAC; 1,700,829 bytes, SHA-256 `8e23fb0f…3fee6c0`.
Cuts land at 2.8 / 5.8 / 8.8 / 12.4s, exactly as authored. No silence run below −45 dB. Mean
−19.6 dB, **peak −1.8 dBFS**, so the 2026-11-18 limiter fix still holds.

What works:
- **The yellow-television reveal held for s4 again (second film in a row).** One small yellow
  set sits on the back-room shelf in s4 and isn't in s1–s3. In s5 it shows a grainy rerun of
  the customer's party. This is the first film where the tag's TV shows the premise payoff
  rather than a blank screen.
- **Every premise beat reads.** s1: a basket of faded snapshots at the door. s2: the teal-polo
  owner and portholes full of tumbling photos. s3: folding at the table. s4: the station
  worker with a sack stamped with the broadcast tower.
- **The state row is honest.** `optional_clip_skip_reason: deadline` matches the 12.2h still
  wait. This is the first unattended use of the 2026-11-22 fix.

Defects:
- **Garbled fake neon words in four of five shots.** "LAY NIGHT BIATNIGHT" (s1), "BIP" and
  "ORIGINAL BIETHDKS" (s2/s3), "ORIGINAL NIGH-HIFT" (s4) and "BAGTOO PROCINS" (s5). The brief's
  `visual_style` asked for "a teal and pink neon window sign". It is appended to every still
  prompt, so every shot got a sign, and Krea filled each one with letters taken from the prompt
  itself ("Original…", "night-shift", "birthday"). This is the worst lettering regression since
  MV18.
- **s3 memories rendered as rainbow beach towels.** "Neatly stacked like fresh towels" became
  literal towels, so the birthday cake and beach afternoon were lost. This is the same simile
  literalism as MV26's "like snow" and MV27's candles.
- **Photoreal people.** The s2 owner and s3 customer read as photographs, not as a 1990s
  commercial painting.
- **s4 lint-trap frames missing.** The worker is loading a dryer, but no glowing film frames
  show, so "the missing seconds" become a sack of laundry.
- **No hero clip, the seventh film in a row.** The 12.2h still queue ran past the two-hour
  deadline (t-011).

Fixed this session:
- `dead_air_produce.lettering_surface_problems` flags phrases that give the painter a surface to
  fill with words: signs, marquees, billboards, banners, labels, stickers, sandwich boards,
  "lettered", and quoted or ALL-CAPS "reading …" text.
- `tests/test_dead_air.py::test_unrendered_briefs_give_the_painter_no_lettering_surface` runs
  it over every unrendered brief (dated 2026-11-23 onward). It fails on the briefs as they stood
  this morning and passes after this rewrite.
- Rewrote the offending lines in five unrendered briefs, keeping each beat as a picture or
  symbol:
  - 11-24 Leftover Hour: twist-tied foil, not "SUNDAY NAP" labels.
  - 11-26 Way Back Express: a bulb-lit movie palace, not a marquee.
  - 11-27 Rain Check Doorbuster: bunting instead of hand-lettered banners, and pen sketches in
    place of the quoted rain-check text.
  - 11-28 Second Copy Keys: a painted key-and-clock window and tower-stamped key tags.
  - 11-29 Dish Return Depot: tower-stamped lids.

  The words still reach the viewer through the compositor's overlay and the voiceover.

Carried forward (not fixed here): the 12h still queue (t-011) is still why the hero clip never
lands. Literal similes ("like towels/snow") need a brief-writing rule, not a regex. Most briefs
still open their style line with "Original", and MV28 painted that word into its signs. With no
sign surface it should have nowhere to go, but watch MV29+.
