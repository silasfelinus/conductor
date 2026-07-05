# Da Vinci ↔ Storymaker Boundary Comparison

**Task:** davinci/t-007 — revisit the project boundary now that the Da Vinci
endpoint engine exists.

**Recommendation up front:** keep them separate projects with separate data
models through Da Vinci's play-loop MVP and Storymaker's first schema
milestone. Share through the existing Kind Robots models (Bot, Chat,
Character, Dream, Scenario, ArtCollection, Milestone) and, later, through
small extracted utilities — never through merged tables or a shared session
row. Revisit after BOTH of those milestones land, not before.

## Where each project stands (2026-07-05)

| | Da Vinci | Storymaker |
|---|---|---|
| Schema | **Live in kind_robots** (LifeRun, LifeChoice, LifeStat, LifeEnding, LifeAchievement, LifeAchievementUnlock, LifeRunArt + 4 enums, PR #87) | Spec only (session data model approved, no tables) |
| Engine | **Working + verified**: 1024 seeded endings, importer (PR #89), resolution/award API (PR #92), regression suite (PR #93) | Spec only (turn lifecycle, collaboration rules, artifact mapping, UX flow) |
| Players | Single player per run | Multi-player, async-first, turn custody rules |
| Outcome space | Closed and deterministic: 10-bit outcomeKey → exactly 1024 endings | Open-ended: stories end where players stop; value is the artifacts and the log |
| Progression | Pass/fail stat thresholds → milestone + achievement awards | Artifact lifecycle: ephemeral → candidate → unlocked → reusable |
| Source of truth | App-owned outcome math; AI narrates but never decides results | Server-held session state; player text is a contribution request, not authority |

## Why they feel similar

Both are "AI narrates, app owns state" story games sitting on the same Kind
Robots anchors: a Bot narrator, Chat as the narration surface, Characters and
Dreams as seeds, generated art collected along the way, and unlockable
records at the end. Both reject freeform AI as the source of truth. That
shared philosophy is why the merge question keeps recurring.

## Why they should not merge yet

1. **Opposite outcome geometry.** Da Vinci's whole identity is a closed,
   deterministic endpoint space — every run resolves to one of 1024
   pre-seeded endings, and the achievement economy depends on that being
   stable. Storymaker's identity is the opposite: bounded-visibility
   surprise and open-ended collaboration. A shared "session" abstraction
   would have to carry both a deterministic resolver and a freeform
   turn-custody engine, and would serve both badly.

2. **Custody models differ in kind, not degree.** LifeRun has one owner;
   ownership checks are a single userId comparison (already implemented and
   tested). Storymaker turns require actor validation, turn order, and
   visibility windows. Merging tables means every Da Vinci query inherits
   multi-actor complexity it never uses.

3. **Maturity asymmetry.** Da Vinci's engine is merged, seeded, and
   regression-checked. Storymaker has no schema. Coupling a working system
   to an unbuilt one means every Storymaker schema decision becomes a
   potential Da Vinci migration — the cheapest possible way to destabilize
   the thing that currently works.

4. **The milestone economies shouldn't blur.** Da Vinci endings are
   one-per-user global unlocks with an API-layer duplicate guard shaped by
   MySQL NULL semantics. Storymaker rewards are curated artifact copies into
   profile inventory. Same word ("unlock"), different invariants.

## What they genuinely could share — later

Ranked by likelihood that duplication actually hurts:

1. **Narration prompt assembly** — both build a bounded prompt from
   (narrator Bot config + seed objects + state snapshot + recent history).
   When Da Vinci's play loop lands, this is the first real duplication risk.
   Extract as a utility function contract, not a table.
2. **Art-scene hooks** — both generate scene art into an ArtCollection with
   a scene-type tag. LifeRunArt's sceneType enum is a reasonable prototype
   for a shared pattern (pattern, not shared table).
3. **Session resume UX** — "whose turn / where was I" card state. Shareable
   as a frontend component once both exist.
4. **Choice interpretation** — mapping structured options + freeform input
   to validated effects. Same shape at the API layer even though effects
   differ (LifeStat deltas vs story mutations).

What should NOT be shared even then: run/session tables, outcome resolution,
unlock/award records, turn custody. These are the identity of each game.

## Concrete boundary rules (proposed as standing guidance)

- Da Vinci code lives under `server/api/davinci/` + `server/utils/davinci.ts`
  in kind_robots; Storymaker gets its own namespaces when built. No shared
  `story/` namespace until a real utility is extracted from working code on
  both sides.
- Neither project's roadmap may add columns to the other's tables.
- Shared behavior enters through the existing Kind Robots models or through
  a pure-function utility with tests — merged storage is out of bounds
  without a Silas-approved schema pitch.
- The merge question is closed until: Da Vinci play-loop MVP is merged AND
  Storymaker m1 (session schema) is merged. Then re-open t-007-style review
  with actual duplication evidence in hand.

## Decision requested from Silas (soft — nothing blocked)

This doc recommends "separate projects, shared primitives later, revisit
after both MVPs." If that matches your intent, no action needed — t-002's
open scope confirmation can absorb this. If you want a different shape
(e.g., Da Vinci as a Storymaker mode from day one), say so before the
Da Vinci play-loop task gets scoped, because that's the fork in the road.
