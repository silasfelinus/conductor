# Da Vinci ↔ Storybook: one storymaker

> **This document used to argue for keeping Da Vinci and Storybook apart. That
> recommendation is dead.** Silas merged the two on 2026-09-09 and asked that
> every reference telling us to separate them be killed. This file keeps its
> original path so that nothing linking to it lands on a dead page — the
> filename is a URL, not a claim. What follows is what is actually true now.
>
> Shipped in kind_robots PR #2549. Superseded: davinci/t-007 (2026-07-05).

## The decision

Silas, 2026-09-09, verbatim:

> merge the projects, and kill any reference that says we should separate them.
> we care about having a solid *single* interface that is a stylish and
> effective storymaker with many endings. Whatever has been done should be
> merged.

There is one product: **Storybook**, at `/storybook`. One route, one setup
screen, one story library. `/play/davinci` is a permanent 301 to it.

## How the two engines coexist

The storymaker's setup screen asks for a **shape** alongside the narrator
voice. Four shapes; the fourth is the endings engine:

| Shape | Engine | Ends when |
|---|---|---|
| Short story | client-side beat loop | the arc closes |
| Chaptered tale | client-side beat loop | the reader finishes it |
| Episodic serial | client-side beat loop | the reader stops |
| **A whole life** | **server-side `LifeRun`** | **ten dimensions resolve to one of 1,024 seeded `LifeEnding`s** |

Both shapes are seeded from the same ingredients — cast, primary setting,
Facets, Rewards, a premise. The life shape maps them onto the FK columns
`LifeRun` has carried since it was built (`characterId`, `dreamId`, `botId`,
`artCollectionId`), which is why the merge needed **no migration**.

## The `Life*` models stay, and that is not a boundary

`LifeRun`, `LifeChoice`, `LifeStat`, `LifeEnding`, `LifeAchievement`,
`LifeAchievementUnlock` and `LifeRunArt` keep their own tables because they
encode something the beat loop has no equivalent of: a closed, deterministic
outcome space (a 10-bit `outcomeKey` → exactly one of 1,024 pre-seeded endings)
with a live achievement economy on top of it. That is a statement about what
those rows hold, not a wall between two products. There is no rule here that
forbids a future shared table, a shared session row, or a column added to a
`Life*` model — if a change to the merged storymaker wants one, the only
question is whether it is a good change.

The one invariant worth keeping from the old doc, because it was never about
project separation: **the narrator proposes, the app disposes.** Narration
never owns durable state. A narration response that invents an eleventh
dimension or swings a stat by 40 is a schema violation, not a new rule. That
lives in `server/utils/davinciNarration.ts`'s own header comment and holds for
every shape.

## What is still worth unifying

Real duplication, now that the two live in one product — none of it blocking,
all of it worth doing when a session has room:

1. **Narration prompt assembly.** Both shapes build a bounded prompt from
   (narrator config + seed objects + state snapshot + recent history), in two
   places: `stores/storybookStore.ts` and `server/utils/davinciNarration.ts`.
   The beat loop builds it client-side and the life engine server-side, which
   is the actual obstacle to sharing it — worth resolving deliberately.
2. **The `/api/davinci/*` namespace and the `davinci-*` localStorage keys.**
   Kept at the merge, deliberately: renaming a live API and orphaning every
   in-flight run buys nothing Silas asked for. Worth renaming later, behind a
   plan that migrates running games rather than stranding them.
3. **Session resume UX.** "Where was I" is answered twice, in
   `storybook-life-run.vue` and `storybookLibraryHelper.ts`.
4. **Choice interpretation.** Structured options plus freeform input mapping to
   validated effects — the same shape either side of the split, even though
   the effects differ (`LifeStat` deltas vs. story mutations).

## History

The 2026-07-05 version of this file recommended separation on four grounds:
opposite outcome geometry, differing turn-custody models, maturity asymmetry,
and distinct unlock economies. It set its own expiry — revisit once Da Vinci's
play-loop MVP and Storybook's first schema milestone both landed. Both landed.
The maturity argument expired with them, and Silas answered the rest: a single
stylish interface with many endings is worth more than the tidiness of two
separate products. The engines were never the problem; two front doors were.
