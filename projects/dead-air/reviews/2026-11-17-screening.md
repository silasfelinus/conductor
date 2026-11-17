# Private screening review — 2026-11-17 PT

Reviewer: Conductor daily-creative session (dead-air/t-004). The final was downloaded from
Kind Robots by ArtImage id and its SHA-256 and byte count compared with
`production-state.json`. Frames were inspected at each shot's midpoint and 0.2s either side of
every storyboard cut; loudness was measured per second and with `silencedetect` at −45 dB.
Nothing was published. This is an agent quality review, not Silas's acceptance.

## MusicVideo 22 — Tomorrow Is Calling (ArtImage 274464)

Status: **finished private film, reviewed.** 15.0s, 1280×720 H.264 at 30 fps, mono AAC.
1,581,742 bytes, SHA-256 `4e0f8e1b…55fe62`, both matching the ledger. `is_public: false`
was recorded by the producer's privacy check (dead-air/t-012). The overnight pass started it
at 01:13 PT. This session resumed it at 02:48 PT, after all five stills were done, and it
exported on that resume.

What works:
- This is the most consistent film so far. All five shots share one midcentury cel-noir look:
  ivory, charcoal, cherry-red cords and emerald jewel lights. That is the "five shots, four
  looks" problem from Apology Orchard, and it doesn't happen here.
- s2's switchboard is a wall of red receiver cords in even rows, as authored, and s5's empty
  booth under a rain-lit transmitter tower is a strong closing frame.
- Cuts land on 2.6s, 5.5s, 8.4s and 12.3s, and all five captions are legible and match the
  authored overlays.
- Audio has no run below −45 dB at all: the voiceover carries to about 10s at −16 to −20 dB
  mean, the station bed holds 11–12s at about −32 dB, and the chime sits at 13–15s.

Defects:
- **The reveal is spent in s1.** The yellow single-eyed cuboid is the station's recurring
  mascot and is written into this brief's `visual_style`, so it appears in every still: on
  the desk in s1, on the switchboard in s2, inside the pocket watch in s3 and on the booth
  roof in s5. s4's reversal makes the same machine the reveal ("the voice is the station"),
  so by then it isn't a surprise. This is the Clap Credit jaguar defect again.
- **s4 doesn't show the mirror.** The brief has the woman facing a booth mirror with the
  receiver deep in her reflection. The render shows her and a duplicate side by side with a
  friendly yellow TV set and a yellow payphone. The doubling half-reads as "future self",
  but the uncanny reflection is lost.
- s3's pocket watch holds a tiny yellow cube rather than losing its hands into the receiver
  mouthpiece. The "minutes as payment" image is weaker than authored.
- The authored sound ends with "an abrupt dial tone swallowing the last syllable". The
  station bed and chime are generic, and there is no dial tone, because the provisional mixer
  doesn't use the brief's `sound` field.
- Voiceover peaks reach 0.0 dBFS at 0s and 9s in the final AAC, even though the mix limiter
  is set to 0.93. The AAC re-encode at captioning overshoots. FORMAT.md's acceptance asks that
  "sound/VO does not clip", so this is a minor finding for the next audio pass.
- No GPU motion shot: s4 is authored `motion: clip`, but the ledger records
  `optional_clip_skipped_for_congestion: true` and five kinetic shots.

## Fixed this cycle

- **Upcoming briefs.** 2026-11-18 *Yesterday's Weather* and 2026-11-19 *Opinion Zoo* both make
  the black jaguar their reveal, and both also had it in `visual_style`, so the reveal would
  have rendered in every shot. The jaguar is now named only in their s4 reversal shots. A
  regression test covers future authored briefs.
- **Producer path bug.** `dead_air_produce.py --episode projects/dead-air/...` (a relative
  path) crashed in `record()` with "is not in the subpath". The episode path is now resolved
  first, and a test covers it.

The mascot itself stays a deliberate cross-episode motif. Briefs that make it the reveal
(2026-11-20 *Ghost Exit Interview*, 2026-11-23 *Hold Music Spa*) are flagged here for the
authoring pass, not rewritten: there the station is the reveal, and the mascot is not.
