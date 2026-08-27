# Shared bestiary handshake with Ruler is Hooked (t-022)

Date: 2026-08-27
Task: cthulhuquarium/t-022 — "Shared bestiary handshake with Ruler is Hooked"

---

## TL;DR

The **contract documentation** half of this task is already done, merged directly to
`silasfelinus/cthulhuquarium` (PR #14, `worker/ruler-hooked-shared-fish-20260826`,
2026-08-26 14:43 PT) — `fish/SCHEMA.md` and the new `fish/CROSS-GAME-SHARING.md` both
state the contract in the exact terms this task asked for. This session confirmed that
via a read-only clone (this session's GitHub grant does not include
`silasfelinus/cthulhuquarium`, but anonymous `git clone` over HTTPS works read-only —
same finding t-015's TALKBACK entry already recorded).

The **seed-freshness half is not confirmed, and is likely stale**: the bible's 18
ruler-hooked-tagged species (below) were tagged in the 14:43 PT PR, but `t-008`'s own
closing note timestamps the last production seed run at **01:45 PT the same day** —
about 13 hours *before* the tagging PR merged. No later reseed is recorded anywhere in
`projects/cthulhuquarium/TALKBACK.md` or the roadmap. Unless Silas ran
`npm run seed:bestiary:write` by hand sometime since, the live `Monster.games` column
for these 18 rows almost certainly still reads `[cthulhuquarium]` only, not
`[cthulhuquarium, ruler-hooked]`. This session could not verify the live DB value
directly (see "Why this session couldn't just check" below) or fix it (same DB
unreachability t-008 hit: DNS resolves, TCP to the port times out, from this sandbox).

**FOR SILAS / next session with DB reach:** run `npm run seed:bestiary` (dry run) in
kind_robots, confirm it reports 18 rows changing `games`, then `npm run seed:bestiary:write`
— exactly the same two-step Silas already ran once for t-008 from his WSL checkout at
`/mnt/d/code/kind_robots` (that's the machine that could reach the DB; this sandbox
cannot). This is idempotent and safe to run even if a reseed already happened — it will
just report 0 changes.

## The 18 ruler-hooked-tagged species

Every fish below has `games: [cthulhuquarium, ruler-hooked]` in its bible YAML
(`silasfelinus/cthulhuquarium`, `fish/<slug>.yaml`) as of PR #14:

| slug | name | rarity |
|---|---|---|
| bailiff-eel | Bailiff Eel | RARE |
| chandelier-lion | Chandelier Lion | RARE |
| choirfish | Choirfish | RARE |
| drowned-carp | Drowned Carp | COMMON |
| errand-guppy | Errand Guppy | COMMON |
| gutter-minnow | Gutter Minnow | COMMON |
| lamplight-angler | Lamplight Angler | UNCOMMON |
| ledger-crab | Ledger Crab | UNCOMMON |
| moebius-crab | Moebius Crab | EPIC |
| parlour-rustfish | Parlour Rustfish | COMMON |
| sea-camel | Sea Camel | UNCOMMON |
| sump-blob | Sump Blob | COMMON |
| the-hold | The Hold | EPIC |
| the-long-patience | The Long Patience | LEGENDARY |
| the-pleasant-island | The Pleasant Island | LEGENDARY |
| the-sexton | The Sexton | UNCOMMON |
| the-understone | The Understone | RARE |
| tithe-shoal | Tithe Shoal | UNCOMMON |

This is a superset of the two species `CROSS-GAME-SHARING.md`'s own prose calls out by
name as examples (`parlour-rustfish`, `drowned-carp`) — the doc's examples were not the
full list, this table is. Sharing is per-species, not per-evolution-line: check each
stage's own `games` list in the bible rather than assuming a whole line shares status
just because one stage does.

## What ruler-hooked's dark-ecosystem branch should do

Straight from `fish/SCHEMA.md` (`silasfelinus/cthulhuquarium`), already authoritative,
repeated here only so the reopening session doesn't have to go find it:

- **Query:** `Monster` rows where `games` contains `ruler-hooked` — once seeded, that
  is the 18 slugs above (`SELECT ... WHERE games LIKE '%ruler-hooked%'` or the Prisma
  equivalent against the `games String? @db.VarChar(764)` column; check
  `scripts/seed_bestiary.ts` in kind_robots for the exact list-to-string encoding it
  writes, since `games` is a delimited string column, not a native array type).
- **Never mutate:** a shared `Monster` row is not either game's property. Neither game
  writes to the shared identity fields (`slug`, `name`, `species`, `class`, `tier`,
  `fieldNote`, canonical art, the six `Rarity` stats). Ruler is Hooked's own
  caught/discovered state, habitat/lure availability, catch weighting, specimen
  records, Fishopedia state, and kingdom-unlock conditions all belong in Ruler is
  Hooked's own tables, keyed on the shared `slug`, never as new columns on `Monster`.
- **Never DELETE:** if a species is later dropped from the bible, the seed script sets
  `isActive: false` on the row. A dark-ecosystem query should filter `isActive: true`
  the same way the aquarium side does.
- **Rarity stays canonical:** if a shared fish needs to be harder or easier to catch in
  Ruler is Hooked specifically, change local unlock/weight/habitat/gear conditions —
  never relabel `Monster.tier`.
- **Art may vary by presentation** (bestiary plate vs. catch card vs. lake illustration)
  as long as it's keyed to the same `slug` as a variant, not treated as a different
  creature.
- **Ecology affinity is a Ruler-side field, not `alignment`:** the bible's free-text
  `alignment` is not the same thing as Ruler is Hooked's `GOOD | NEUTRAL | EVIL`
  ecosystem classification — that field belongs in Ruler is Hooked's own schema, not
  on `Monster`.

Full source: `silasfelinus/cthulhuquarium` `fish/SCHEMA.md` (`## The games field is the
whole sharing mechanism`) and `fish/CROSS-GAME-SHARING.md` (the complete rules doc) —
read those directly rather than this summary if anything here seems to conflict.

## Why this session couldn't just check the live DB

- No public, unauthenticated kind_robots API lists `Monster` rows by `games` value.
  `GET /api/monsters/[id]` (id or slug) exists but its select (`monsterArtSelect` in
  `server/api/monsters/lookup.ts`) is art-linking-only and does not include `games`.
  `GET /api/aquarium/catalog` does include species data but requires an authenticated
  user session (`requireApiUser`).
- Direct DB access is unreachable from this sandbox — same finding as t-008's own
  closing note: DNS resolves, TCP to the database port times out.
- This session's GitHub grant does not include `silasfelinus/cthulhuquarium` for API/
  MCP purposes (read-only anonymous `git clone` over HTTPS still works, which is how
  the species table above and the schema quotes were confirmed).

## What would close this task for real

1. Confirm (or perform) a `seed:bestiary` reseed from a machine that can reach the DB,
   and confirm via `npm run seed:bestiary` (dry run) that it reports 0 pending changes
   for the 18 slugs above afterward.
2. Optionally, once confirmed, add a one-line pointer in this doc or the roadmap note
   recording the reseed date/run, so a future session doesn't have to re-derive this
   timeline gap again.
3. The documentation contract itself needs no further work — `fish/SCHEMA.md` and
   `fish/CROSS-GAME-SHARING.md` in `silasfelinus/cthulhuquarium` already say everything
   t-022's original note asked for.
