# Ecotone: Weird Humboldt — ready for human tests, 2026-11-18 PT

**Playable route:** https://kindrobots.org/play/ecotone (live after the next Unraid Force Update that includes kind_robots#5320)

**Lifecycle:** `playtest` / `normal` priority (Silas, 2026-11-18 PT: *"Work on wrapping up Ecotone ... get prepared for human playtesting"*). The finite build roadmap is complete. What's left is three owner decisions (below) plus whatever playtesting turns up. New fixes go in as `playtest_iteration: true` tasks. This handoff is **not** publication, promotion or creative-approval sign-off.

## What testers get

- **Three weekend routes:** the Green Ribbon Fair, the Kinetic Grand Championship and the Quiet Way. All three run through six regional chapters, about 180 authored cards, seeded draws, and 2d6 checks with real setbacks.
- **Seven opening lenses**, from Sober to Tripping Balls plus three chemical detours. None of them forces an outcome.
- **Four guides** (Mara, Kit, Juniper, Cedar), with stay/follow crossroads, optional companion time and the chosen-family coda. You can also finish alone or take the Wild Way.
- **84 collectible endings** (6 leads x 7 lenses x hopeful/dark). Each has a dossier with signature, epilogue and picture. **All 84 have painted plates in four art styles** (2026-11-19: Mara's 14 plates and `ecotopia-mdma-dark` re-rendered from a new, non-culturally-coded Mara design, t-076).
- **Twelve once-per-run local mysteries** with Case Files and 36 Real Endings.
- **Main-game standard:**
  - welcome-back title screen
  - settings: text size and speed, art style, motion, contrast, collection reset
  - autosave, undo, three save slots, export/import
  - 18 site achievements
  - a Scrapbook page per finished weekend
  - a Guides tab that remembers who you've met
  - 12 avatars, 6 personalities and 7 origin archetypes

- **Eight new middle encounters** (2026-11-19, t-077): a harbor diner buyout, a Hammond Trail mural, a culvert hearing, a food-share rule, a ridge radio forecast, a shared fire-break survey, a quiet person at a festival gate, and a dam nobody named. They sit two per region in chapters 2-5, each with an earned finale callback. All 48 of their pictures are painted in four styles (three Comic renders were withdrawn on review and fall back to Painted).

## Verification on record

- **100% art coverage** (2026-11-19, t-079): every card (171), choice outcome (680) and ending (84) has its own painted picture in the default style, and `verifyEcotone` now fails if one ever goes missing. This came from 542 rendered-but-unshipped outcomes (kind_robots#5343), 8 missing cards and 194 new outcome pictures (#5346, #5358). Eight off-prompt tag-style renders were withdrawn and fall back to Painted.

- **27 Ecotone CI suites now run on every Ecotone PR** (kind_robots#5320). 19 of them previously ran in no workflow. They cover all 84 endings witnessed by real seeded play, 8,400-campaign and 1,764-journey adversarial audits, sober parity, the 2x2 causal chains, companion continuity, the Cedar invariant, and save round-trips.
- **Mounted browser audit** `npm run audit:ecotone-viewports` runs at nine sizes, 320 to 1920, including short landscape. With engine-played saves, it checks:
  - no document scroll on any tab, the title, the beat screen, the end screen or the dossier
  - an 84/84 ledger that survives reload, with spoiler-safe locked slots
  - a visible keyboard focus ring
  - reduced motion and the missing-art fallback

  Result: see the t-016 note.
- The four companion-time scene pictures (CT-MARA/KIT/JUNIPER/CEDAR-01) had written prompts but were never queued. They're now queued in `art/WRITTEN-BACKLOG-2026-11-19-ECOTONE.yaml` (private, auto_submit) and render without further agent work. The Mara scene shows only her studio, not her. Until the renders land, those four scenes use the code-drawn fallback.
- kind_robots#5321 fixed a production build break (Deepheart) found during this work. Without it, the next deploy would have failed.

## Owner decisions

Decided by Silas, 2026-11-19 PT ("we are expecting all roadmaps before human testing are okayed. do it."):

- **t-076 (done):** the 15 withheld plates were generated from a new Mara design, along with her Guides portrait and the KN-1 pictures (19 pictures x 4 styles).
- **t-075 (done):** The Long Table stays a coda, and following someone new still resets the travel party.
- **t-027 / t-077:** all eight middle-encounter candidates were built as cards (see below).

- **t-007 (cancelled):** "Wider publication and promotion should not be a part of the roadmap. It can be closed." Publication and promotion are decided outside the roadmap, and nothing here authorizes them.

**Nothing is open before human testing.** The only remaining step is the Unraid Force Update that deploys this work. Optional polish such as t-078 (re-rendering three withdrawn Comic pictures) runs as playtest iterations.

## Human playtest checklist

1. **First visit, on a phone.** Read the title and pick a name, avatar and origin. Choose an event. Does the first five minutes explain itself without help?
2. **Play one full weekend** on any route and lens. At the crossroads, follow someone new once. Note any card where the choices felt fake or the outcome didn't follow from the roll.
3. **At the end:** read the ending and epilogue, then check that the Endings tab shows 1/84, the dossier opens, and the Journal's Scrapbook has the page.
4. **Replay** with a different event and lens. On the second run, does the Guides tab remember everyone you've met? Did the run feel different?
5. **Try the Quiet Way alone** and aim for the Wild Way (keep choosing the animals).
6. **Open a Case File** and follow a mystery to a Real Ending.
7. **Settings:** larger text, reduce motion, high contrast. Save to a slot, reload the page, load the slot. Export a save, then import it.
8. **Tone check:** Humboldt felt lived-in, not quirky-for-quirk. Nothing preachy about substances or politics. Dark endings felt earned, not random.

When reporting, include route, lens, guide, ending title, device and width, the exact card and choice, and a screenshot if you can.

**Master issue:** [Kind Robots #4145](https://github.com/silasfelinus/kind_robots/issues/4145). It's renamed to say it's ready for human tests and closed as completed, because agent production is complete. That is not a claim that anyone has played or accepted it.
