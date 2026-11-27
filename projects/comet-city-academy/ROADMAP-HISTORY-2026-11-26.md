# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not live directions. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `d1b74635d2fedd1a53ceed2e1d90f457a4f76a92`. Existing archive files remain untouched.

## goal

<!-- raw:begin goal -->
goal: >-
  Deliver Prom of Doom, a Capes & Tassels series game: a thirty-day, day/night, single-screen
  superhero graduation RPG. Two geographically consistent campus/town maps,
  weekly gated authored and seeded encounters, hero/villain/rogue patrol cases,
  1-3-follower dispatch, romances and sidekick bonds including at least two
  fully consensual throuple routes, injuries and infirmary recovery, one of
  eight city-destruction villains per run, powers with unique mission solutions,
  Hero, Followers, Scrapbook and Settings pages, real save/load/card backs and
  twelve consequential endings. High-priority art-first Play experience with
  verified branching art, adversarial seeded tests and final human design review.
<!-- raw:end goal -->

## t-016

<!-- raw:begin t-016 -->
    note: |-
      Preserve the existing 48 signature/save identities, version and migrate old saves, extend the choice taxonomy to explicit element plus focus, reconcile Animal + Technical Training and the Zuzu example with existing canon, and implement persistent person/role/relationship history. Build the first six fully playable six-viewpoint/form character arcs, meaningful partner and optional romance choices, distinct hero/villain tactics, at least four seeded foreshadowed betrayal candidates with a guaranteed real NPC heel turn per run, redemption/prevention logic that doesn't counterfeit player choice, and at least two independent evil accomplices per early mastermind. See IDENTITY-SYSTEM.md.
      2026-11-04 PT (round 6, patch on origin/main 239b6022): Built a playable slice. A hero/villain/rogue alignment track for the player and every roster classmate now moves only with night choices (led calls, district walks, the contracts you hand your crew) and shows on the Hero screen, the crew cards and a debrief strip; it is saved as optional alignmentLog. Two state-driven classmate arcs play as authored debrief beats. "The Other Side of the Radio" is a three-beat heel turn for a classmate pushed three steps against your side: reach/tail/leave, then promise/expose/release, then a turn that a kept promise or changed work prevents. It has a mirror notebook/testimony version for villain players. "Partners in Crime" is a three-beat accomplice job against the seeded mastermind's warehouse; the deal you offered and what you did with the haul decide loyalty, sellout or double agent. Payoffs: roster loss, accomplice +1 on villain/rogue calls, recruiter evidence, morning lines and finale lines with a small support modifier. The seeded day-20 betrayal, the 48 identities and the romance/triad rules are untouched. Hero-only play fires neither arc, and saves are validated and backward-compatible. Pinned by the new verifyCometAlignmentArcs.test.ts (wired into test:comet-city-academy). Remaining for t-016: the 4+ seeded betrayal-candidate pool with a guaranteed per-run NPC turn reconciled with day 20, redemption beats after a turn, six full character arcs and partner/romance evolution, 390/768/1440 screenshots of the new debrief card, and art for the beats. Merged as kind_robots#4842 (2026-11-06); task stays ready for the remaining slices.

      2026-11-25 PT intent-audit reconciliation: the task's own note says the merged increment is partial and the task returns to ready after merge (kind_robots#4842 merged 2026-11-06; claim since 2026-11-21). No open matching PR or worker/comet-city-academy-t-016-* branch in kind_robots. Scope unchanged; remaining work as listed in the note.
<!-- raw:end t-016 -->

## t-002

<!-- raw:begin t-002 -->
    note: |-
      Detail a thirty-day five-band story, six power families with week-specific unique approaches, sixteen recruits and eight romanceable adults across body and gender diversity, two mutually negotiated throuple arcs, twenty-four geographically consistent campus and city sites, eight villains and twelve endings. Reconcile the six existing prototype student IDs.
      Completed a scoped first creative writing/art round in conductor PR #6648, merged at 9eba77b54023a31279b4b0d931add1fd9ac17bd1. Authored three distinct thirty-day campaign encounters with nine methods, eighteen materially different success/failure consequences, and three candidate ending epilogues. The paired auto_submit Krea 2 ledger contains 21 literal illustration requests and a static source/ledger parity test. No runtime integration or rendered images yet; art generation must submit and assign ArtJob ids before claiming queue success. The full cast/power/map/finale bible is still unfinished, so t-002 returns ready rather than done.
      Merged canonical real Prom of Doom writing, art and requirements in Conductor PR #6649 at abcb341b2054199449e61fa02a0bfc5a3e4726bf after all 22 checks passed (one skipped). Authored mandatory day-29 guest-list setup and day-30 real catastrophic ballroom prom with seven choices and fourteen outcome versions, three distinct physical antagonist plan adapters, four potential endings, three cinematic beats and 21 literal Krea 2 automatic-submission entries. Canon document and tests enforce that a rehearsal cannot replace the real prom. The 30-day runtime, five additional antagonist adaptations, rendered ArtJobs, fully verified end-to-end traces and complete cast bible remain unfinished. Return t-002 ready for continuing work; do not label final game complete.
      Authored 48 distinct student, hero and villain identity triads in the Kind Robots runtime with protagonist, antagonist and partner hooks; integrated first-week identity preview and simulated foreshadowing. Added canonical 30-day six-track identity design, guaranteed NPC heel turn, accomplices and final-gate roadmap tasks. Full quest engine, 288 authored tracks and artwork remain unfinished.
      Merged Conductor PR #6668 (68319fa) and Kind Robots PR #4204 (994cb888), all 21 latest Kind Robots check runs passed. Authored 48 distinct three-form identity entries with protag/antag/partner hooks, console previews, safe first-week nonbinding finale projection, and the IDENTITY-SYSTEM.md canon. [...]
      [Earlier history (4,392 chars) archived verbatim to projects/comet-city-academy/T002-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
      Submitted scoped lore and product increment: 48 original power-origin start level blueprints, 48 villain-specific lair phases with tactical secrets, 48 powered independent number-two lieutenant bosses with counters and motives. Kind Robots JSON and typed lookup are backed by a full 48-signature parity test and an interactive catalogue inside the existing internal tactical hero dossier. Conductor design briefs and Prom/tactical roadmaps define the 96 playable stage implementation + 48 lieutenant AI follow-ons. This is an authored/inspectable catalogue, not 96 implemented battles or delivered original art. The complete 30-day bible task remains open.
      Triage 2026-10-30: review with no open PR, returned to ready as partial. Merged increments are #6648/#6649/#6668/#6791 and kind_robots #4455. Still missing: 8 romanceable adults (3 exist), the two negotiated throuple arcs (no triad code on main), and the 16-recruit bible. This is the cheapest real content gap and also feeds t-005 and t-013.
      2026-10-30 romance/recruit slice. MERGED Kind Robots #4489 (b93d33b2) and #4492 (95e960cf), with all 22 check runs green on each, plus Conductor #6820 (86200d83), which adds RECRUIT-AND-ROMANCE-BIBLE.md and links it from DESIGN-BRIEF section 4. Romanceable adults: 8/8 in runtime (Mina, Imani, Nix, Mara Fen, DRIFT-9, Tessel Mire, Jo Mercer, Lark Sato; 3 she/her, 3 they/them, 2 he/him). Bodies include plus-size, sturdy, broad- shouldered, slender, lab-grown and alien. Faculty are never romanceable. Each has a distinct voice, consent-first listen/help/invite/date scenes, a bedside scene, two or three compatibility rules (closed/wary/kindred by form, vow, power and danger) and save- validated state. Negotiated throuple arcs: 2/2 in runtime. The Listening Accord (Imani + Nix) is player-initiated; The Night Shift (Jo + Lark) is partner-initiated. Each has 5 beats, every beat has a pause or decline exit, every adult consents separately, there is no cheating option, and the arcs have different terms, a standing or trust consequence, a +1 team bonus and prom epilogues. Saves are replay-validated and old saves load. Recruit bible: 16/16 authored, of which 12 are runtime recruits and 4 are authored only (Vesna Duarte, Bram Kowalczyk, Femi Ilunga, Cyrus Adeyemi; not recruitable and no art). STILL OPEN for t-002: bring the 4 authored recruits into runtime (adding STUDENTS changes openingNightFriend and legacy knownContacts, so it needs a migration), the full 30-day five-band story bible, six power-family week-specific approaches, eight villain plans and twelve endings bible, and relationship art. Returned to ready, not done.

      Scoped follow-on to the authored recruit bible: four previously non-playable recruits Vesna Duarte, Bram Kowalczyk, Femi Ilunga and Cyrus Adeyemi integrated into runtime roster and game social cards, with distinct site introductions, sidekick eligibility, dispatch reactions, four team bonus paths, original cast visual descriptions and save/replay regressions. Existing six night-three friends and twelve implicitly known legacy-save contacts are unchanged. Code branch worker/comet-city-academy-t-002-recruit-onboarding-20261121 at e2b40c8dd6b502da655023b4a9bdcf5d7b528057. Tests committed, CI not yet verified. No new ArtJobs or rendered follower art. The full thirty-day bible and art remain unfinished; return to ready after merge.

      2026-11-25 PT intent-audit reconciliation: the task's own note says the merged increment is partial and the task returns to ready after merge (kind_robots#4492 merged 2026-10-30; claim since 2026-11-21). No open matching PR or worker/comet-city-academy-t-002-* branch in kind_robots. Scope unchanged; remaining work as listed in the note.
<!-- raw:end t-002 -->

## t-004

<!-- raw:begin t-004 -->
    note: |-
      Create thirty-six distinct training, heroic, villainous and rogue/shared cases across five calendar bands; write meaningful success/mixed/failure/decline, roster conflicts, injuries, unique-power approaches and delayed faction callbacks. Clearly distinguish training simulation from real danger.

      Added five authored next-school-morning consequence callbacks for each of the twelve original real night cases, preserved all twenty-four expanded cases, wired original rescue/refusal outcomes into nextSchoolDay, and added seeded callback verification. Scoped PR pending CI; the broader delayed faction callback and injured-roster work remains.

      Merged Kind Robots PR #4567 (squash 48bc9735ecd267349188f2facdb2ed7739474c9c) after all 19 checks completed green. Added 60 distinct next-morning outcomes across 12 original patrol cases, preserving the 24 expanded cases and patrol narrative priority. Tests cover 36 total case families, all five results per original case, and next-day routing. Remaining for t-004: delayed faction effects, injury-driven roster conflicts, and wider unique-power callbacks in the 24 expanded cases.

      Added saved case history and five-night district trust effects to deterministic dispatch odds, separating unanswered emergencies from failed rescues. Earlier runs preserve compatibility; 36-case and corrupted-save verification added. CI pending.

      Merged Kind Robots PR #4569 as c412e3ae3da41bdd4ae5e72e1ff9039f1ec400f2 after all 19 check runs completed successfully. Thirty-day runs now retain unique case outcomes and unanswered calls in a validated campaign history, with bounded five-night district trust effects on the player-chosen investigation path. Seeded 30-day rescue endings remain stable, old saves load, and new case-memory tests passed. Remaining t-004 scope includes character-specific social and injury callbacks, richer faction branches, and art-verified encounter choices.

      2026-11-05 PT game sprint: Fixed a contradiction a playtester would see. The 12 late
      expanded night cases each had one morning callback used for every grade, so refusals and
      failed rescues were followed by success prose; the 12 first-wave expanded cases had none
      at all. All 24 now have distinct honors/pass/partial/failed/refused mornings (120
      lines), so all 36 case families answer every result. Dispatch cards gained a DISTRICT
      MEMORY line driven by the saved caseHistory. It names the last call in the same district
      within five nights, voiced through 4x5 authored witness lines. It also states the exact
      district-trust odds a personal investigation receives, shown only on cases that can be
      investigated. The morning after an unanswered call now says "unanswered" instead of
      "failed". Odds, seeds, saves and endings are unchanged; verifyCometMorningCallbacks
      covers the change. The kind_robots patch against origin/main 050b23e went to the
      coordinator to push and PR (scratchpad comet-city-academy-t-004.patch), because the
      sandbox blocked kind_robots pushes from this agent. Remaining for t-004: injury-driven
      roster conflicts and wider unique-power callbacks in the 24 expanded cases.

      2026-11-04 PT: five-way morning callbacks for all 36 night cases plus district memory
      merged as kind_robots #4772 (squash c5e8e55). Back to ready for injury-driven roster
      conflicts and unique-power callbacks in the 24 expanded cases.

      2026-11-04 PT round 2: Injury now shapes the night roster. A follower rushed back
      through the infirmary that morning won't work a call without a healthy partner. A
      healthy teammate or the player leading the call covers them at no cost. Sent alone, they
      go anyway at -1 to the roll, shown on the dispatch card (RECOVERING line, hand-card
      state, odds) and in the night report. Rested followers and the existing next-
      day/infirmary rules are unchanged, and visual-novel nights send healthy contacts to solo
      calls first. Each of the 24 expanded cases gained two authored power callbacks (the
      needed field plus one other relevant field, 8 per field, 48 lines). They show when the
      player leads, with the exact +2/+1 the roll already applies, and are flavor only: odds
      are unchanged. New verifyCometNightCallbacks.test.ts covers it and is wired into
      test:comet-city-academy and CI. A 60-seed greedy 30-day comparison against base gives
      identical endings. Patch built against kind_robots f074838 and verified on a13933a
      (scratchpad comet-city-academy-t-004-r2.patch). Remaining for t-004: delayed faction
      effects, injury conflicts for neighborhood patrol-story teammates, and art-verified
      encounter choices.  Merged as kind_robots #4788. Back to ready for the remaining scope.

      Scoped delayed faction aftermath authored for all four districts and five outcome grades; exposed in saved district memory. Awaiting PR checks; broader patrol art and story scope remains.

      2026-11-19 PT review recovery: Original patrol-faction PR silasfelinus/kind_robots#5370 failed the seeded morning callback contract because faction prose appeared after the district-trust odds suffix. Superseding rescue PR #5385 preserves the 4-district by 5-grade delayed faction responses, places them ahead of the trusted odds line, and merged to main as fee5f93 after all eight latest-head checks passed. Mark #5370 obsolete; never merge it. The scoped contribution is done, but the 36-case umbrella remains open for patrol art, additional identity-specific consequences and full from-new-game acceptance QA.

      Added a regression fix for faction responses hidden by newer district witness reports. Scoped Kind Robots PR to follow; remaining patrol art and identity QA stay open.

      Reopen the remaining Patrol consequences scope for independent production. No open matching implementation PR was found; preserve previously merged contributions and all acceptance requirements. Do not count partial implementation as done.

      Scoped patrol injury debrief and next-morning recovery notices on Kind Robots worker/comet-city-academy-t-004-injury-debrief-c4d9 at 2e18ec470fa55456ef464782edea0ee72e6da49f. Existing deterministic injuries and save schema unchanged; named report consequences and infirmary availability, including graduation cutoff. Extracted actual notice function passed 27 calendar cases, and 120-seed integration regression extended for injury, restoration and recovery; full repository CI pending. Umbrella remains partial.

      Verified PR #5820 merged at 5d79dbbd9e2892be71dfd6816f69d18af016c68e after eight successful corrected-head workflows and successful branch janitor. Injury and recovery notices are merged; wider patrol scope remains open.
<!-- raw:end t-004 -->
