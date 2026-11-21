# Hybridizer: ready for human tests, 2026-11-21 PT

**Playable route:** https://kindrobots.org/play/hybridizer. It is live now: production `b7a1821c` includes kind_robots #5490 and #5493.

**Lifecycle:** `playtest` / `normal` priority. Silas, 2026-11-21 PT: *"help me get to human playtests and closing the GitHub issue … I'm happy as long as we have the hybridized fully working to react and resubmit bad hybrids in game."* The finite build roadmap is complete. New fixes found in playtesting go in as `playtest_iteration: true` tasks. This handoff is **not** publication or promotion approval: t-010 remains Silas's separate public-release gate.

## What testers get

- **Two-chamber fusion lab.** Pick any two of the 200 illustrated starters (animals, monsters, fruit, oddities) or any earlier hybrid, then fuse. Known pairs show their shared art at once. New pairs render in the background while you keep playing, and a toast appears when your render is ready.
- **4,000 pre-rendered launch hybrids.** All 4,000 are delivered and were reviewed visually. 1,856 that were not real hybrids were re-filed for a better render:
  - 769 showed only one ingredient
  - 567 showed two separate creatures
  - 515 were missing a fruit or object ingredient
  - 5 other

  The re-renders are queued at the lowest priority and replace the old art as they finish. The rejected art stays in each hybrid's version history. Verdicts are in `art/CURATION-ROUND-1.json`.
- **React and fix in game:**
  - Upvote and comment on any public hybrid.
  - Any signed-in player can press **"Not a hybrid? Re-roll"**. This uses a new seed with fused-body guidance. Players cannot add prompt text, the usual mana and limits apply, and earlier versions are kept.
  - The creator of a discovery can **Remix** it (choose the ingredient balance and add direction) and promote any version to primary.
- **Your own ingredients:**
  - **"＋ Add your own ingredient"** uploads a picture with a name, an optional description, and creature or object, after a consent statement.
  - Uploads and every hybrid made from them stay **private** to that account.
  - Image type is checked from the file bytes, then the image is re-encoded with EXIF/GPS stripped. Limits: 10 a day, 30 active.
- **Atlas, favorites and Surprise.** Browse every shared discovery, favorite illustrated ones, and randomize a pair.
- **Sharing.** Public discoveries get a share link. Private ones never do.

## Verification on record

- Production viewports at 390, 768 and 1440: no horizontal overflow and 0 broken images. The reveal measures 326×256, 678×460 and 531×373; before #5490 it was a ~30px thumbnail on phones. Signed-out visitors get no stray ready toasts. Upload endpoints return 401 when signed out, and the signed-out drawer shows the sign-in link.
- Contract suites in CI:
  - `test:hybridizer-art` covers the re-roll and curation rules and the prompt contract.
  - `test:hybridizer-cache` covers pair identity and the upload rules: magic bytes, disguised files, text, dimensions, the owner-only resolver, inherited privacy, consent, re-encode and limits.
  - `test:hybridizer-catalog` checks the starter catalog.
  - Conductor's `tests/test_hybridizer_launch.py` covers the launch ledger, curation idempotence, adopting an already-running re-render, and server-readiness gating.
- Earlier QA slices: #4565 (cross-account privacy) and #4643 (atlas and remix).

## Known, intentional limits

- The illustrator works from an upload's **name and description**. The picture is the ingredient's portrait in the lab, not a render reference.
- About 46% of the launch set needed a second attempt. Re-renders use stronger guidance but are not re-reviewed one by one. Disappointing ones are what the in-game re-roll is for.
- The 398 borderline (WEAK) launch hybrids were left live for players to judge and re-roll.

## Owner decisions (not build work)

- **t-002**: optional creative-direction review of the roster and look. Answer any time.
- **t-010**: authorize promotion from playtest to a public launch.
