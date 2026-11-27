# Main-game quality standard

Silas, 2026-11-11 PT, in session:

> Our games should all have a base standard of quality: a settings menu, save/load,
> achievements, some sort of scrapbook, multiple endings, in most cases, customizable
> characters (with exception for early zuzu gamebooks), and multiple hooks to get the user
> to keep replaying: unlockables, persistent save states, branching pathways, etc.
> Three achievements was the standard for arcade games, those are smaller scale. We want our
> main games to have 12 plus achievements. There's no reasonable limit, some games may have
> them tied to each ending, but let's not go overboard.

**Current direction (2026-11-26 PT):** fully develop the intended game before handing it to humans for playtesting. This is an agent-owned evidence standard, not another subjective approval gate. Publication and final human acceptance remain separate.

**Owner direction (2026-11-26 PT):** Completed generated art is presumed present for roadmap acceptance. Do not retain subjective human approval, manual art inspection or human playtesting as finite build tasks or graduation prerequisites, including older project-specific acceptance wording (e.g. Deepheart t-012 and t-016–018). Finish integration and agent-owned automated QA, then graduate; record unavailable manual art checks as handoff observations rather than requiring a human to perform them. Known concrete failures still require repair. Independent release/publication and security-sensitive approvals remain separate and unchanged.

## Which games

**Main games** are the full-length, story or campaign games:

- Slime City
- Ecotone: Weird Humboldt
- Zuzu Gamebook
- Zuzu: Shifting Lands
- Emperor of Dust
- Rainbow Bullet Hell Space Princess
- Save the Plumber
- Shifting Desks
- Memory Dungeon
- Terrors on Crystal Street
- The Ruler Is Hooked
- Cthulhuquarium
- Prom of Doom (`comet-city-academy`)
- Space Couch (`game-of-captains`)
- Every Villain Tactics
- MONSTRIQUE (`monstress-convention`)
- Deepheart (`deepheart`)

A new full-length game joins this list when it's created. Paused or finished main games
(Zuzu's Lair, Zuzu Showdown) meet the standard if they're reopened.

**Arcade cabinets** (`kr-arcade`) and small toys keep the smaller arcade standard: three
achievements. They still need complete gameplay, generated art and icons, art-first single-screen presentation, front page, settings, sound/music, account progress and an appropriate collection/history. Full-length Arcade campaigns use 12+ achievements.

## The standard

1. **Title screen.** It offers New Game, Continue, Settings, Scrapbook and Achievements. The
   MONSTRIQUE console (kind_robots#4848) is the reference.
2. **Settings menu.** Reachable from the title screen and during play. At minimum:
   - music and sound volume
   - text size and reading speed
   - reduced motion and high contrast
   - reset progress, with a confirmation step

   Settings persist between visits.
3. **Save and load.**
   - Progress autosaves, and Continue picks up exactly where the player left off.
   - A page reload never loses progress.
   - Run-based games keep their unlocks permanently, separate from any single run.
   - Signed-in players get persistent global account-backed saves and unlocks across devices using the existing shared save service or verified equivalent. Local/guest storage is the offline fallback, not a substitute. Test reload, cross-device restore, account isolation and reset.
   - Saves are versioned, so updates never wipe them.
4. **Achievements: 12 or more.**
   - Each is a live Achievement record created through the site's achievements API, with a
     unique `triggerCode` prefixed by the game slug.
   - Each is awarded in game and shown with `components/achievements/game-achievement-strip.vue`.
   - Mix story, skill, discovery and completion achievements. Tying some to endings is fine,
     but don't overboard: usually 12–30.
   - Verify actual award, deduplication, persistence and displayed generated original badge/icon art. Obtain account evidence on the authorized deployed build; no automatic deployment.
5. **Scrapbook.** A persistent collection of what the player has found:
   - endings earned
   - characters met
   - art unlocked
   - a page for each finished run (choices, losses, outcome)

   Unfound entries show as locked silhouettes with an "X of N found" count. It survives new
   runs, rewinds and reloads.
6. **Multiple endings.** Several earned endings, each with its own text and **its own painted
   plate** queued through a conductor art ledger. One generic "THE END" doesn't count.
7. **Customizable characters**, in most cases. Choose or design the player character (name,
   look or portrait, and stats where the genre has them), and the story adapts to who the
   player is.
8. **Replay hooks: at least three.** Pick from:
   - unlockables that carry into the next run
   - persistent saves or new game plus
   - branching paths
   - seeded or randomized content
   - difficulty modes
   - collectibles
   - alternate starting characters

9. **Art-first single-screen console.** One composed primary screen, with substantial art and controls/choices immediately adjacent. No scroll-dependent primary gameplay, document-like pages, modal maze, placeholder skeleton or admin chrome. Test phone, tablet portrait/landscape, desktop and short-wide layouts. Internal accessible collection panes may scroll.
10. **Original generated artwork AND icons.** All player-facing illustrations, portraits, backgrounds, items, sprites, effects, cards, title/ending plates, collection art, achievement badges and thematic UI icons use original generated art. No SVG art or SVG icon sets, emoji stand-ins, stock substitutes, programmer-drawn placeholders or CSS shapes masquerading as illustrations. Functional layout, meters, focus outlines, hitboxes and semantic text remain functional UI. Reuse suitable original generated assets. Verify successful render receipts with concrete ArtImage IDs (or committed generated files), expected asset coverage and runtime bindings. Queued, running or failed jobs are not acceptance. Assume successful renders with concrete asset IDs are delivered unless there is affirmative evidence of a missing or broken asset; authenticated URL checks and visual curation are helpful when available, not blockers for finite roadmap closure. Preserve licensing, mature/privacy and security gates.
11. **Sound and music.** Original or approved rights-safe soundtrack, gameplay and UI cues, working volume/mute controls, looping/transitions, browser gesture unlock and persistent settings. Verify audible playback and controls on the accessible build. Existing completed Prom/Tactics audio is sufficient until human testing; do not reopen merely for subjective taste.
12. **Complete gameplay and adversarial testing.** All promised stages, enemies/bosses, encounters, routes, choices and endings are playable. Test from New Game through real conclusions, alternate/adverse decisions, losses, retry/reload, resource extremes, device input and accessibility. Record reproducible seeds, screenshots and defects. Fix critical/high failures and material art/UX gaps, rerun tests. A prototype, single vertical slice, green CI, metadata count or drained art queue is not full readiness.

## Character exceptions and decisions (Silas, 2026-11-11 PT)

- **Zuzu Gamebook keeps its fixed protagonist, Zuzu.** No character customization. Every other
  item in the standard still applies.
- **Zuzu: Shifting Lands gets a character creator with adjustable stats.** This is what sets it
  apart from the gamebook.
  - Playable characters include **Zuzu** and **Jeffery Mittens** (the young raccoon looter
    from Book One).
  - Encounters adapt to who is playing. For example, a player can't play a fennec sibling and
    then meet the siblings as strangers.

Any other exception to item 7 is Silas's call. Record it here when he makes one.

## How agents apply it

Audit each applicable row once against actual main/runtime evidence: Met, Partial or Missing, exact evidence, responsible existing task ID and next finite action. Keep the table in the existing audit/spec or linked acceptance document, not every task note. Use existing standard, art, build and QA tasks; add a finite task only for an uncovered requirement. Keep original art ledgers and auto-submit; never duplicate jobs.

Handoff requires all applicable rows verified, finite original build/art/content/QA resolved, no missing required render receipts or runtime bindings, or known critical/high defects, and inspectable actual run/device evidence. Then use the existing playtest/normal and master-issue procedure. Do not require a human verdict first. Do not deploy/publish automatically. Preserve explicit prior owner waivers; no new exceptions without owner approval. Do not automatically reopen projects already in playtest.

## Active project acceptance ownership

Existing scopes to reconcile, not another task ledger. Live roadmaps own task state, dependencies and claims.

| Project | Existing completion scopes |
| --- | --- |
| Rainbow Bullet Hell Space Princess | t-044 standard, t-012 story/audio, t-022/030 art, t-013 full local co-op QA, t-042 reconciliation; t-014 human release |
| Save the Plumber | t-028 standard, t-005 traversal, t-021–023 worlds, t-012/024–026 art/audio, t-027 Maker, t-013 QA; t-014 release |
| Kind Robots Arcade | Finite cabinet depth slices and existing display/audio/device tasks; 3 achievements per small cabinet; t-009 recurring factory not a finite blocker |
| Memory Dungeon | t-068 standard, t-025–028/047/077 maps/dungeons, t-075/076 art, t-079 opening, t-078 endings, t-080 delivery/device readiness, existing balance tests |
| Prom of Doom | t-034 standard, t-002/004–006/016–017/021–027 campaign/identity, t-007/008/031/033/046/051 art, t-009/010/018 QA, t-032 reconciliation; t-049 audio done; t-011 human gate |
| Terrors on Crystal Street | t-024 standard, t-004/005 art, t-016 Jess slice plus complete-game coverage, t-011 human gate |
| Every Villain Tactics | t-025 standard, t-009–011/018/020–024 routes/AI/editor/identity, t-012 art, t-013 QA; t-029 audio done, t-014/015 human gates |
| MONSTRIQUE | t-015 standard, t-003–010 story/rooms/art/endings, t-014 art, t-011 security, t-012 QA; t-013 human gate |
| Tarot Studio | Non-game production tool: t-004/005 decks, t-006 print exports, t-009 accessible workflow; generated visuals/icons, global private deck state/settings. t-007/008 commerce gated |
| The Ruler Is Hooked | t-067 standard, t-047/057/058 art, t-048 fairness/economy, t-050/061 device QA, t-051 readiness; t-032 human gate |
| Playbook Kit | Shared infrastructure: t-003–007 adoptions, t-008/013 adapter, t-009/017 art, t-026 review. Provide standard through shared components, preserve engines/saves. No revived daily challenge |
| Rebel Button | Small game: t-001 brief, t-003/004 foundation, t-005 finale/full 100-press loop; 3 achievements, global progress, generated icons, front/settings, audio and discovery/history equivalent. t-002 soft gate |
| Deep Heart | t-012 delivery audit, t-016–018 bestiary/environments/relationships, t-013 adversarial/device QA, t-014 graduation. Recheck all standard rows against existing build tasks |

Non-game tools use equivalent full-workflow, generated visuals/icons, accessible art-led design, persistent account state, settings and adversarial functional QA. Don't invent RPG features, achievements or endings for an admin production tool.
