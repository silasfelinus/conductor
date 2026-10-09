# Shifting Lands: source manifest contract (v2)

The **single authored design catalogue** is [WORLD-DECKS.json](WORLD-DECKS.json).
It is an alternate-play game design, not Book One canon, and not a Kind Robots
database export. For authoritative history, read
[the world registry](../../worlds/zuzu/README.md),
[Book One](../comic-creator/issues/zuzu-koala-assassin-01/BOOK-ONE.md) and
[the setting guide](../../worlds/zuzu/WORLD-GUIDE.md).
Spoilers are intentionally present in developer files, as Silas requested.

## Machine-consumable contracts

- `WORLD-DECKS.json`: five ordered lands, exactly three unique encounter
  locations per land, one major challenge each, land-specific species and
  occupation/role pools, seeded-journey contract, source art pointers.
- `world-decks.d.ts`: TypeScript shape for producers/consumers of **version 2**.
- `world-decks.contract.mjs`: dependency-free structural, cross-reference,
  provenance and presentation validator. `toPlayerBoard()` returns an
  explicitly allowlisted player-safe snapshot with gated boss fronts.
- `world-decks.contract.test.mjs`: smoke, graph, cross-Facet, schema migration
  rejection, unknown ID and spoiler-disclosure regression tests.

Run from the Conductor repository root:

```bash
node projects/zuzu-shifting-lands/world-decks.contract.mjs
node --test projects/zuzu-shifting-lands/world-decks.contract.test.mjs
```

## Identity and provenance

**Do not invent runtime resource IDs.** Entries in `scenario_refs` and
`reward_refs` are *design keys*, `status: design-only`, `runtime_id: null`
until the owner-scoped Kind Robots audit in task t-004 and later tagging t-012.
The named Abbess locked **ArtImage 242559** is a sourced selection from
`worlds/zuzu/catalog.json`, not a claim that a Character runtime ID is known.

The first Homestead cards point to four **existing public files** in
`silasfelinus/kind_robots/public/zuzu-gamebook/scenes`. Those paths were
verified as repository entries on 2026-10-09. `repository-file` means exactly
that, not a freshly verified live CDN URL, ArtImage relation, or delivery.
Later chapters have `art_ref: null` until verified illustrations can be
attached through existing asset links. Never fabricate an image or copy media
into this catalogue to quiet a missing-asset check.

The independent SPECIES/ROLE/OCCUPATION pools are deliberately just templates:
species never determines a participant's morality. Named characters remain
stable identities and exceptional faction/condition cases are explicit.

## Spoiler isolation and future integration

This source manifest contains Abbess plot information in `canon_motivation`
and the `world_mysteries` section. **Never send it raw to the browser.**
Only use `toPlayerBoard(manifest, {activeChapter, completedLocationIds})` or
an equally allowlisted server-side DTO. It exposes no developer-only motive,
mystery, disposition, generated Scenario/Reward identifier or source
identification fields. The Abbess's public boss card unlocks only after all
three Homestead locations are resolved, and still doesn't reveal her motives.
Public server APIs must authorize access to game data independently.

The Kind Robots Homestead prototype still uses its existing v2 reducer. The
following engine tasks should consume this typed v2 contract rather than
silently transcribing a second lore database. Add a deliberate import
transform/generator with drift checks when integrating it into the runtime;
Conductor owns this authored game-world content while Kind Robots owns saves
and gameplay state. Do not conflate an updated design manifest with deployed
client code or a completed 5-land game.

**Evolution rule:** changing semantic keys, their identities or state
transition meaning requires a new schema version and migration. Safe additive
teasers/source refs may remain within v2 if the contract and tests pass.
