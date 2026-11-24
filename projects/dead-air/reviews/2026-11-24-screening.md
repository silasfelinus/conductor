# Private screening review — 2026-11-24 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). I downloaded the final from Kind
Robots by ArtImage ID. Its SHA-256 and byte count match `production-state.json`, and the API
reports MusicVideo 29 as `isPublic: false`, status `EXPORTED`. I checked frames at each shot's
midpoint, found cuts with FFmpeg scene detection, and checked audio with `silencedetect`
(−45 dB, 0.1s) and `volumedetect`. Nothing was published. This is an agent quality review, not
Silas's acceptance.

## MusicVideo 29 — Hold Music Day Spa (ArtImage 280005)

Status: **finished private film, reviewed.** The 00:14 PT pass started it. All five stills
(ArtJobs 77027–77031) sat PENDING for 19,916s (5.5h). This session's `--daily` resume first saw
them done at 05:46 PT and exported the film. 15.0s, 1280×720 H.264, AAC; 1,761,992 bytes,
SHA-256 `af5b9b6f…e78d6330`. Cuts land at 2.8 / 5.8 / 8.8 / 12.4s, exactly as authored. No
silence run below −45 dB. Mean −19.7 dB, **peak −1.8 dBFS**, so the limiter fix still holds.

What works:
- **No garbled painted words in any background.** The 2026-11-23 lettering-surface rewrite held:
  the film has no sign, marquee or label, where MV28 had fake neon words in four of five shots.
- **The yellow-television reveal held for s4 (third film in a row).** It sits on top of a
  switchboard whose panels carry tower symbols, with curly cords running in from the lounge. In
  s5 it glows on the reception table over the guests, who are still on hold.
- **The late-1980s pastel look holds in every shot.** Peach and seafoam walls, wicker, ferns and
  seashell headphones show in each one, and the s3 cucumber-eyes gag reads at a glance.

Defects:
- **Style-bible set dressing bled into the contrast shots.** `visual_style` listed "peach and
  seafoam pastel walls, wicker chairs, potted ferns, beige corded telephones on every armrest,
  seashell-shaped headphones". It is appended to every still prompt, so:
  - The s1 "harsh fluorescent" office hook is painted as a spa: peach walls, ferns, wicker
    chairs, and the worker already wears the shell headphones. The before/after contrast that
    sells the offer is lost.
  - The s4 back room is not the "vast dim" switchboard the brief asked for. It has a peach
    wall, ferns and wicker chairs, which softens the reversal.
- **s3 character continuity broke.** "The once-frazzled worker" in s1 is a dark-haired man in a
  blazer. In s3 he is a white-haired older man, because the still model has no memory of s1.
- **The s5 television screen shows "DAY-SPA" text**, not a single eye, and its face is lost for
  the second time (after MV27).
- **Photoreal people again** in s2 and s5.
- **No hero clip, the eighth film in a row.** `optional_clip_skip_reason: deadline` is accurate:
  the 5.5h still wait ran past the two-hour deadline (t-011).

Fixed this session:
- `dead_air_produce.style_bible_set_dressing_problems` flags location, prop and wardrobe nouns
  in a `visual_style`: walls, windows, kitchens, chairs, counters, telephones, coats, clocks and
  similar.
- `tests/test_dead_air.py::test_unrendered_style_bibles_carry_look_not_set_dressing` runs it
  over every unrendered brief dated 2026-11-24 onward. It failed on all seven briefs as they
  stood and passes after the rewrite.
- Rewrote `visual_style` in the 11-24 through 11-30 briefs so it names only era, medium,
  palette, light and film texture. Each shot's `image_prompt` already describes its own place
  and props, so no beat was lost. Dropped: kitchen, refrigerator and foil packets (11-24);
  dining rooms, wall clocks, turkey and tinsel (11-25); cornfields, bus-depot interiors and
  coats (11-26); sidewalks, display windows, scarves and vests (11-27); shop window and walls of
  keys and clocks (11-28); garage window, floor and shelves (11-29); strip-mall window and CRT
  glow (11-30).

Carried forward (not fixed here): recurring characters need a full description in every shot
that shows them, because "the same", "now" and "once-" phrasing gives the painter nothing to
match. That is a brief-writing rule, and a lint could flag those back-references. The still
queue (t-011) still decides whether the hero clip lands.
