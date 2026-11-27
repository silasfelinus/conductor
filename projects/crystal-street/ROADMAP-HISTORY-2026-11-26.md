# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not live direction. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `8667ecb20e3faecd993ab58468b991a1eeaa67bf`.

## goal

<!-- raw:begin goal -->
goal: >-
  A full single-screen, console-style horror-comedy card adventure at /admin/crystal-street
  (later /play/crystal-street). A week of seven Days and Nights on Crystal Street against one
  of twenty or more nightmares, each with a backstory, central issue, three leads, three
  signature nights, a fight/trick/heart Halloween finale and four endings (one Best per
  nightmare). Days visit ten locations and a traveling pawnshop for daylight beats, leads,
  training, gear and companions; nights deal signature scenes and tag-deck pulls with
  teleports. Twenty or more companions (ten active) with perks, six emotions, portrait and
  poster art. Every choice has two or more options whose success and failure outcomes are
  illustrated. Every run is recorded in a scrapbook. Queer-positive, PG-13, deterministic and
  seeded, no LLM at play time. Finished only after painted art is delivered for key art,
  cast and scenes, a balance pass, phone/tablet/desktop review, and Silas's acceptance.
<!-- raw:end goal -->

## t-004

<!-- raw:begin t-004 -->
    note: >-
      About 270 scene prompts already live in the JSON (`art` on each encounter). Build a
      ledger from them (generated art is pre-approved), batch it behind round 1, and deliver to
      /crystal-street/scenes/<encounter-id>.webp.

      2026-11-02 PT: Round 2 ledger built and opted into auto_submit: projects/crystal-
      street/art/ROUND-2-SCENES.yaml, 466 encounter scene plates (all scenes/<id> prompts from
      kind_robots allArtPrompts() not yet delivered or in another ledger; 33 already
      delivered). All 466 pass the live prompt contract. Queued is not delivered: next owner
      runs --status, curates keepers with export_crystal_street_art.py --sheet, exports to
      public/crystal-street/scenes/<id>.webp and PRs kind_robots. Released to ready while it
      renders (~8-9h at current box throughput).

      2026-11-02 PT rolling curation, batch 1: first 60 round-2 scenes judged against their
      prompts; 26 keep (exported to kind_robots public/crystal-street/scenes), 34 redo
      (verdict on each subject; main failures readable text, dropped signature props like the
      shear glove and wrist chains, extra background kids). Next 60 pending scenes moved to
      priority 620. A redo ledger follows once every scene has rendered.

      2026-11-02 PT rolling curation, batch 2: next 60 round-2 scenes reviewed; 33 keep
      (exported), 27 redo (readable mall neon and signage in 13; missing smoke-demon hints,
      Bog Baby shape, head-count misses). Running total 59 keep / 61 redo of 120 rendered;
      next 60 pending moved to priority 620.

      2026-11-02 PT rolling curation, batch 3: 60 more round-2 scenes reviewed; 37 keep
      (exported), 23 redo (missing monster beats for Brightwaters, Bobo and Sugarlings;
      readable signs; head-count misses). Running total 96 keep / 84 redo of 180 rendered;
      next 60 pending moved to priority 620.
<!-- raw:end t-004 -->

## t-016

<!-- raw:begin t-016 -->
    note: >-
      Silas: "then we work on the first playable slice". Proposed scope to confirm when we get there: one
      nightmare played end to end at full polish (Counselor Jess, the cover star), with scene and outcome
      art for her leads, nights, finale and endings; the daylight beats and decks she can deal; an
      onboarding first day; sound effects and the theme; and a balance and narrative pass on that path.

      Progress 2026-10-25 PT: onboarding shipped in kind_robots #4168 (merged 21f752c): nine
      first-week coach tips (utils/crystalStreet/tips.ts, unit tested), in-flow banner, Tips
      setting and Replay the tips. Slice art queued: art/JESS-1.yaml, 113 renders (ArtJobs
      45413-45525) covering Jess's 13 scene plates, 76 outcome plates, 4 tier endings and the
      slasher/paranormal deck scenes. Remaining: export the Jess art, sound effects, and the
      balance/narrative pass on her path.

      Progress 2026-10-25 PT: sound effects shipped (kind_robots #4169). Slice art: 106 Jess
      plates in kind_robots #4175, covering scenes, outcomes, tier endings and the
      slasher/paranormal deck scenes, every image reviewed at full size. 23 rejects across
      three rounds had their prompts fixed at the source; 7 more are re-rolling in art/JESS-
      REROLL-3.yaml and ship in a follow-up. Continuity pass on all content landed in #4173.
      Remaining for the slice: the 7 re-rolls and a balance read on Jess's path (73% Best,
      inside the band).
<!-- raw:end t-016 -->
