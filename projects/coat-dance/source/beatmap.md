# Coat Dance — Source-Video Beat Map

Task: coat-dance/t-003 · Template date: 2026-08-12 · Populated: 2026-09-17 ·
Status: first real pass, ready for Silas's review

This is the populated beat map for `coat dance_x264.mp4` (5:32, 720×480,
single continuous take, synced original audio). 38 sections, timestamped
against real detection-tool output, described from actually-extracted
frames — not a guess.

## How this pass was produced

An isolated Python environment in the conductor sandbox (`imageio-ffmpeg`,
`librosa`, `opencv-python-headless`, `scipy`, `Pillow` — none of which were
available in earlier sessions per t-002/the original template note) ran:

1. **Audio extraction** — mono 22.05kHz WAV via `ffmpeg` (bundled through
   `imageio-ffmpeg`, since no system `ffmpeg` binary is installed in this
   sandbox and `apt-get install ffmpeg` failed on unrelated broken mirror
   packages — `pip install imageio-ffmpeg` sidesteps both).
2. **Audio structural segmentation** — `librosa.segment.agglomerative` over
   stacked chroma-CQT + MFCC features, targeting ~28 structurally distinct
   sections. This replaces raw `beat_track`/`onset_detect` output (716 beats
   / 334 onsets at 129 BPM — far too fine-grained for a choreographic beat
   map) with actual phrase/section boundaries.
3. **Motion energy** — frame-to-frame grayscale absolute-difference mean,
   sampled at ~5fps over a 160×107 downscale, smoothed and peak-picked
   (`scipy.signal.find_peaks`, min spacing ~5s). This is a lighter proxy for
   dense optical flow that runs in seconds rather than minutes on this
   sandbox's CPU-only environment, and it's exactly the "no skeleton to key
   on" signal the template calls for — it catches the *coat's* movement
   (throws, flares, drags) as readily as the performer's.
   **MediaPipe Pose was not run** — installing and running full pose
   estimation over ~8,300 frames was judged too costly for this pass
   relative to its marginal value once motion energy already flags every
   high-activity moment; if a future pass wants per-limb keypoints (e.g. for
   precise AI-treatment rigging rather than beat-boundary detection), that's
   a targeted follow-on, not a blocker on this table.
4. **Boundary merge** — audio structural boundaries ∪ motion-energy peaks,
   deduplicated within 4s of each other, snapped to cover the full 0:00–5:32
   runtime with no gaps. 39 boundaries → 38 rows below.
5. **Visual read** — one representative frame extracted at each section's
   midpoint (`ffmpeg -ss <t> -frames:v 1`), assembled into labeled contact
   sheets, and read directly (this is where **Movement/Action**, **Coat
   Behavior**, **Camera/Framing**, and **Emotional Tone** come from — actual
   viewing, not inference from audio/motion numbers alone). The per-segment
   motion-energy mean/max and audio RMS mean (both retained) ground the
   *Emotional Tone* read in a real number, not just a vibe from one frame —
   e.g. row 17 is both the single highest motion-energy segment in the
   piece (mean 13.07, peak 50.97, roughly 4× the piece's own median) and
   among its loudest audio (RMS 0.17), which is why it's read as the
   climactic burst rather than merely "energetic."

**Camera/Framing is not repeated per row** because it doesn't change: the
entire piece is one static wide proscenium shot, camera never pans, cuts, or
reframes. That's recorded once here rather than copy-pasted 38 times: **wide
static shot, full figure to stage floor, fixed camera position throughout —
consistent across all 38 sections; no cuts, pans, zooms, or reframing
anywhere in the source.** Any AI treatment that wants to reframe (closer,
Dutch angle, etc.) is departing from the source camera, not matching it —
worth flagging explicitly for t-004 rather than leaving implicit.

One correction to what a single frame can mislead into: rows 3 and 5 show a
second, blurred humanoid shape crossing the frame. Per `BRIEF.md`, this is a
**solo** piece — "an avant-garde duet between a performer and a coat," not
two dancers — so this is almost certainly **motion blur of the performer
themself** captured mid-movement by the camera's shutter (or conceivably a
lighting/reflection artifact), not a second performer. Described below as
such rather than as a second figure.

**Generation Method is left blank throughout**, per the column definition
and t-006's not-yet-confirmed render-environment tool inventory (BRIEF.md
Q3) — filling it now would mean guessing a tool that may not be installed.
**Candidate AI Treatment** carries first-pass proposals per the column's own
"proposal, not commitment" framing; t-004 owns the approved treatment.

## Column definitions

| Column | What goes here |
|---|---|
| **Timestamp Range** | `MM:SS–MM:SS`, start inclusive / end exclusive, no gaps or overlaps across the full ~5:32 runtime once the table is complete. |
| **Movement/Action** | What the performer is doing — plain description, not interpretation (e.g. "spins twice, coat trailing outward", not "conveys freedom"). |
| **Coat Behavior** | What the coat itself is doing, tracked as its own duet partner per `roadmap.yaml`'s `creative_constraints` — worn, thrown, dragged, held at arm's length, animated by momentum alone, etc. Leave blank only if the coat is genuinely static/off-frame for that beat, not by default. |
| **Emotional Tone** | The beat's felt quality (frantic, tender, absurd, still, menacing, playful...) — grounds t-004's section-by-section treatment in the actual performance rather than generic mood guesses. |
| **Candidate AI Treatment** | A first-pass idea for the AI-assisted expansion of this beat (style shift, perspective change, animated extension, ghosting/duplication, etc.) — proposal, not commitment; t-004 owns the approved treatment. |
| **Generation Method** | Which tool/pipeline the candidate treatment implies, once t-006 has confirmed what's actually available in the render environment (BRIEF.md Q3). Left blank throughout this pass — see above. |
| **Restitch Notes** | Anything this beat needs to cut cleanly against its neighbors after per-section rendering — matching motion/energy at the boundary, audio sync points that must not drift, a held frame to bridge sections, etc. |

*(Camera/Framing dropped as a per-row column this pass since it's constant —
see the note above the table.)*

## Beat map

**Camera/Framing (all rows):** wide static shot, full figure to stage floor,
fixed camera, no cuts/pans/zooms anywhere in the source.

| # | Timestamp Range | Movement/Action | Coat Behavior | Emotional Tone | Candidate AI Treatment | Generation Method | Restitch Notes |
|---|---|---|---|---|---|---|---|
| 1 | 00:00–00:19 | Stands alone center stage, near-motionless, formal poised stance under a single dim spot. Lowest-energy opening (motion mean 1.18, RMS 0.045 — quietest segment in the piece). | Worn, closed, hanging still. | Still, quiet, formal — a held opening breath. | Slow push-in or particle-atmosphere treatment on the negative space around the still figure; let the stillness read as intentional, not dead air. | | Boundary is a hard audio-structure cut into row 2's rose entrance — no motion to match, safe cut point. |
| 2 | 00:19–00:47 | Extends one arm, presents a red rose held out toward the house. Otherwise mostly static. | Worn, closed. | Quiet, presentational, faintly ceremonial. | Subtle color-pop treatment isolating the rose (only saturated object in a desaturated frame) without altering the performer. | | Rose stays in-hand into row 3 — do not let a treatment "lose" the prop across this cut. |
| 3 | 00:47–00:54 | Short, sharp burst — a blurred humanoid shape sweeps across frame (almost certainly the performer's own motion blur from a quick move, not a second dancer — see note above). Motion mean jumps to 4.04, more than 3× row 2. | Likely swings/trails with the movement (blurred, hard to confirm from a single frame). | Sudden, startling, brief. | This is a strong candidate for literal ghosting/duplication treatment — the source footage already reads as a motion-blurred double; an AI pass could make that duplication a deliberate visual device rather than a shutter artifact. | | Very short (7s) — restitch needs to preserve its abruptness, not smooth it into row 4. |
| 4 | 00:54–01:16 | Returns to a held stance, mostly still. Motion back down to 1.33. | Worn, closed. | Settled, quiet again after row 3's jolt. | Match row 1's treatment approach — bookend stillness. | | Long-ish static stretch (22s) — safe for a slower treatment that needs runway. |
| 5 | 01:16–01:22 | Second blurred-figure passage, same motion-blur reading as row 3 (motion mean 4.86, this pass's second-sharpest short burst). | Trailing/swinging with the movement. | Sudden again — the piece is alternating stillness and blur-bursts through the opening minute. | Same ghosting/duplication idea as row 3 — if approved, apply consistently to both so it reads as a motif, not a one-off. | | Pairs with row 3 structurally; keep timing/energy consistent between the two if both get the same treatment. |
| 6 | 01:22–01:29 | Holds the rose again, composed stance. | Worn. | Quiet, returning to presentational mode. | | | |
| 7 | 01:29–01:34 | Stillest single segment in the entire piece (motion mean 0.76, roughly a third of the piece median) — essentially a held freeze. | Worn, motionless. | The piece's stillest breath — near-suspended. | A held-frame/slow-motion treatment would cost nothing here; there's almost no real motion to preserve. | | Ideal bridge point if two rendered sections need a seam — this is the calmest possible splice location in the first two minutes. |
| 8 | 01:34–01:40 | Begins moving again, coat visibly swinging with the motion. | Worn, swinging/trailing. | Building, a shift out of stillness. | | | |
| 9 | 01:40–01:48 | Drops to the floor — performer now down at stage level, white dress shirt visible where the coat was. | Coming off / already removed — first clear coat-off moment in the piece. | A turning point: the "duet partner" is set aside. | This is a structurally important beat — flag clearly for t-004 as the piece's first coat-off transition, likely worth a treatment that marks it as a turn rather than a plain cut. | | Coat state changes here (worn → off) — restitch must not blur this transition; it's a real narrative beat. |
| 10 | 01:48–01:57 | Floor-level work — crouched/seated, physical, motion mean 4.09 (well above median) with the rose visible on the floor nearby. | Off, on or near the floor. | Grounded, physical, searching. | | | |
| 11 | 01:57–02:12 | Crouched, gathering/holding the coat bundled in both arms — object-manipulation focus. Longest segment so far (15s) at moderate energy. | Held, bundled, being handled as an object rather than worn. | Intimate, tactile — treating the coat as the "duet partner" directly. | Good candidate for a treatment that emphasizes the coat-as-character framing (e.g. subtle independent motion/animation on the coat while the performer is otherwise still). | | 15s segment gives runway for a slower object-focused treatment. |
| 12 | 02:12–02:18 | Crouched, reaching gesture toward or with the coat. | Held. | Continues row 11's tactile mode. | | | |
| 13 | 02:18–02:22 | Kneeling, rose held up and visible again, vest visible (coat still off). | Off (vest only). | Tender, presentational from the floor. | | | |
| 14 | 02:22–02:29 | Kneeling, coat now draped back over one shoulder — starting to reclaim it. | Draped, partial re-wear. | Transitional, coat returning. | | | |
| 15 | 02:29–02:40 | Kneeling, rose raised, coat partially worn. Longer segment (11s), moderate energy (motion 3.05). | Partial wear, in motion. | Building back toward the standing, coat-on mode. | | | |
| 16 | 02:40–02:50 | Rises to standing and throws the coat open into a dramatic flared pose, arm raised — a clear flourish. Motion mean jumps to 7.05, peak 28.57 (both well above anything before this point). | Flared open dramatically, functioning like a cape/wing at full extension. | Dramatic, triumphant — the piece's first big physical statement. | Strong candidate for a hero-moment treatment (slow-motion emphasis, particle trail on the coat's edge, or a perspective shift to feature the flare). | | This is the hinge into the projection sequence (row 17 onward) — the flourish and the first projected image should probably land close together if re-timed. |
| 17 | 02:50–02:58 | The rear-projection screen lights up for the first time (a personal photograph, two people close together) and the performer dances in full-body, high-energy movement in front of/against it. **This is the single highest-energy segment in the entire piece** — motion mean 13.07 (peak 50.97, ~4× the piece's own median) and the loudest-but-one audio (RMS 0.17). | In motion, silhouetted against the projection; specific worn/thrown state hard to pin from one frame at this energy level. | Ecstatic, climactic — the piece's dynamic peak. | This is the section to protect most carefully in any edit — a treatment that trims or slows the piece's actual climax would be a real loss. Candidate: amplify rather than replace (motion-reactive visual intensity keyed to the already-high real motion energy). | | Do not let this segment get trimmed for pacing without flagging it — it's the measured energy peak of the whole recording, not just a visually busy frame. |
| 18 | 02:58–03:05 | Continues dancing against a new projected photo (a group/close shot); performer in a dark, closer-fitting layer (coat set aside for this stretch). Motion mean 5.10, still well above median. | Off/aside for this projection stretch. | Sustained high energy, slightly down from row 17's peak. | | | |
| 19 | 03:05–03:10 | Continues against similar photo imagery, motion mean 8.15 — second-highest in the piece. | Off. | Still in the energetic projection-dance mode. | | | |
| 20 | 03:10–03:16 | Another close personal photo on screen; performer now coat-draped again, crouching. Motion 5.15. | Draped, re-entering. | High energy continuing, coat returning to the picture. | | | |
| 21 | 03:16–03:21 | Screen shows an outdoor garden/cafe photo; performer holds a bent, coat-draped pose. Motion drops sharply to 1.68 — but audio RMS hits 0.2047, **the loudest segment in the entire piece**. | Draped, held. | A deliberate freeze against the loudest music in the recording — stillness used as a dynamic contrast, not a lull. | Notable candidate for a "loud silence" visual treatment — the audio doesn't match the motion here, which is a real, intentional-reading contrast worth preserving rather than smoothing over. | | Audio/motion mismatch here is real signal, not noise — don't let an automated cut-detection pass merge this into a neighboring high-motion row just because the audio is loud. |
| 22 | 03:21–03:30 | Blue-tinted portrait photo on screen (figure against blinds/curtain); performer stands, arms raised, in the lighter layer (coat off). Motion 4.14. | Off. | Rising again after row 21's freeze. | | | |
| 23 | 03:30–03:36 | Same blue-portrait photo continues; performer collapsed/lying on the floor. Motion 3.47. | Off, performer grounded. | A physical low point/surrender pose. | | | |
| 24 | 03:36–03:41 | Screen shows an outdoor garden/patio photo; performer crouches low to the ground, coat back on. Motion 4.09, RMS 0.2008 — near the piece's loudest. | Worn/draped, low to the ground. | High-energy, physical, urgent. | | | |
| 25 | 03:41–03:46 | Screen shows a street/tree photo; performer is a small, distant standing figure in the lighter layer. Brief (5s). Motion 3.94, RMS 0.18 — still in the sustained high-energy zone. | Off. | Exposed, small against the image. | | | |
| 26 | 03:46–03:53 | Screen shows two reclining/sleeping figures (a bed scene); performer crouches low near the screen, coat on. Motion mean 3.81 but peak 31.06 — a sharp burst within the segment. | Worn, in motion. | Intimate imagery paired with a sudden physical burst — a striking, specific pairing. | | | |
| 27 | 03:53–04:03 | Same reclining-figures photo continues; performer crouches close to the screen. Longer segment (10s), motion settles to 2.86. | Worn. | Sustained, close, contemplative-but-active. | | | |
| 28 | 04:03–04:11 | Screen changes to an Egyptian pyramid (travel photo); performer crouches near the screen edge, coat on, peak motion 26.13 within the segment. | Worn, in motion — likely another flourish given the peak. | Energetic, travel-imagery section begins. | | | |
| 29 | 04:11–04:18 | Same pyramid photo; performer stands still, coat draped. Motion drops to 1.39 — a brief pause. | Draped, still. | A short breath between travel-image bursts. | | | |
| 30 | 04:18–04:24 | Screen shows Easter Island moai statues; performer crouches, coat-clad, gesturing. Motion 3.16, peak 21.24. | Worn/draped, in motion. | Playful/interpretive engagement with the image. | | | |
| 31 | 04:24–04:34 | Moai-statues photo continues (longest of this run, 10s); performer crouches low, bowed — a pose that visually echoes the statues' posture in the photo behind them. | Worn/draped. | A specific, legible visual rhyme between performer and projected image — worth calling out by name for t-004 rather than treating as generic floor work. | Candidate: a treatment that makes the echo explicit (matched silhouette/outline between performer and the statues) rather than leaving it as a coincidence a viewer might miss. | | This is a deliberate-reading image/body rhyme — protect the framing that makes it legible (performer silhouette against the statue photo) if reframing anywhere nearby. |
| 32 | 04:34–04:40 | Screen changes to Mount Rushmore; performer stands, arm extended pointing toward the screen, coat off (lighter layer). Motion 6.47 — a sharp rise. | Off. | Declarative, pointed — a clear directed gesture at the image. | | | |
| 33 | 04:40–04:46 | Rushmore photo continues; performer crouches low, reaching. Motion 5.80. | Off. | Reaching, physical, sustained energy. | | | |
| 34 | 04:46–04:54 | Screen shows a black-and-white personal portrait (two figures); performer crouches close to the screen, reaching toward the image. Motion 4.71, peak ~20. | On/draped (coat visible in frame). | Emotionally direct — physically reaching toward a photographed memory. | Strong candidate for a treatment that makes the "reaching into the photograph" gesture literal (e.g. the performer's hand appearing to enter the projected image plane). | | The reach-toward-the-screen gesture is the emotional throughline of this whole photo-sequence — worth a consistent treatment vocabulary across rows 26/31/34 rather than treating each in isolation. |
| 35 | 04:54–05:01 | Same portrait photo; performer continues reaching/pushing toward the screen. Motion rises to 6.07. | On/draped, in motion. | Continued, intensifying physical engagement with the image. | | | |
| 36 | 05:01–05:07 | Screen shows a different close-up personal photo; performer in a low lunge/reaching pose, coat on. Motion 6.08 — the last sustained high-energy beat before the wind-down. | Worn, in motion. | Final physical peak before the piece closes. | | | |
| 37 | 05:07–05:19 | Stage goes to blackout/dark — the projection and stage lighting cut. Motion reads low on average (1.54) with one spike (24.87) likely from the lighting change itself registering as a frame difference, not real performer motion. | Not visible in the dark. | A hard tonal drop — silence/darkness after the piece's sustained physical climb. | Treat this as a genuine structural blackout beat, not a detection gap — do not try to "fill in" motion or coat behavior that isn't there; the emptiness is the point. | | This boundary is a real lighting cut, not a detection artifact — safe, deliberate restitch point if the edit needs one. |
| 38 | 05:19–05:32 | Lights return; performer stands center stage facing forward in a final held pose — a closing tableau. Motion low (1.78), audio RMS moderate (0.12, down from the mid-piece loud stretch — music winding down). | Held/carried over one arm rather than worn — the coat is no longer on the body at the very end. | Quiet, settled, conclusive — a deliberate close rather than an abrupt stop. | Bookend treatment with row 1 (both are the piece's calmest moments) — a visual rhyme between opening and closing stillness would reinforce the piece's own structure. | | Final row — no downstream boundary to match; just needs to read as a clean ending, not a fade-out that outstays the actual footage. |

## Structural read (for t-004)

Rows 1–15 (0:00–2:40, coat mostly worn/removed/floor-handled, no
projection): a quiet, presentational, physically restrained opening —
alternating stillness (rows 1, 4, 6, 7) with short sharp motion-blur bursts
(rows 3, 5) and a floor-work stretch treating the coat as an object to be
handled rather than worn (rows 9–15).

Row 16 (2:40–2:50) is the hinge: a dramatic coat-flourish that launches the
piece's second half.

Rows 17–38 (2:50–5:32) run against continuously changing rear-projected
personal/travel photographs, with physical energy in sustained waves rather
than one smooth arc — a true climax at row 17 (2:50–2:58, the measured
motion-energy and audio peak of the entire piece), a loud-but-still freeze
at row 21, a second energetic run through the travel-photo sequence
(rows 24–36) including one legible image/body visual rhyme (row 31, echoing
the moai statues' posture) and a recurring "reaching toward the photograph"
gesture (rows 26, 31, 34–36), then a hard blackout (row 37) and a quiet,
coat-off closing tableau (row 38) that visually rhymes with the opening's
stillness.

## Format note

This file is the canonical version. If a CSV export is ever more convenient
for a script (e.g. t-006's pipeline prototype reading rows programmatically),
regenerate one from this table rather than hand-maintaining two copies —
this Markdown table stays the source of truth for human review.
