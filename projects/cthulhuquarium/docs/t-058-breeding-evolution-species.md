# t-058: author a BREEDING-evolution species pair in the fish bible

## Why this exists

cthulhuquarium/t-055 ("surface breeding as a real player action in the tank
UI") had two parts:

1. Wire the store/UI so a player can actually pick two owned individuals and
   breed them, with a coin-cost confirmation and a reveal of the result.
2. Author at least one species in the fish bible with `evolutionKind:
   BREEDING` + `evolvesToId` set, so the secret-evolution path (schema-ready
   since t-042/t-029, but inert -- no seed data exercises it) has something
   real to reveal end-to-end.

Part 1 shipped: kind_robots PR #2176 (branch `claude/eager-bohr-or1f0n`),
merged into t-055's own close-out. Part 2 is this task.

## Target repository

`silasfelinus/cthulhuquarium` -- the fish bible (`fish/*.yaml`, one file per
species), a **separate GitHub repository** from both `conductor` and
`kind_robots`. `scripts/seed_bestiary.ts` in kind_robots reads it from a
sibling checkout (`../cthulhuquarium/fish`, `~/cthulhuquarium/fish`, or
`/home/user/cthulhuquarium/fish`) and upserts it into the `Monster` table --
the bible is the canonical source, the database is downstream of it.

## Why this session couldn't do it

This session's GitHub access is scoped to exactly four repos: `conductor`,
`kind_robots`, `Kapowarr`, `humboldtscoopsolutions`. `silasfelinus/
cthulhuquarium` is not among them, and none of the three candidate local
paths `seed_bestiary.ts` checks exist in this sandbox either -- the bible
isn't cloned locally. So neither the GitHub MCP connector nor a local git
checkout could read or write it. This is a genuine access gap, not a
decision to skip the work: per AGENTS.md's cross-repo playbook, the fix is a
documented handoff rather than a guess made without ever having read the
bible's actual current content (species roster, existing `evolves_to`
chains, `SCHEMA.md`'s exact field contract).

## What needs to happen (in `silasfelinus/cthulhuquarium`)

1. Read `fish/SCHEMA.md` for the authoritative field contract (this doc's
   `evolution_kind`/`evolves_to` field names come from `scripts/
   seed_bestiary.ts`'s `Species` interface and `toUpsertData()` in
   kind_robots, not from the bible repo itself -- confirm against
   `SCHEMA.md` before editing, in case it documents constraints this doc
   doesn't know about).
2. Pick two existing species already in the bible, same general rarity
   tier, where a "child" species narratively/visually reads as a leveled-up
   or transformed version of a "base" species -- e.g. a common/uncommon
   base fish evolving into a rarer, weirder variant. (This session has no
   read access to the actual roster to name real candidates; whoever does
   this task should browse `fish/*.yaml` for a pair that already makes
   sense thematically, the same editorial judgment `evolves_to` chains
   elsewhere in the bible presumably already use for `growth`/`secret`
   evolutions.)
3. On the **base** species' YAML file, set:
   ```yaml
   evolution_kind: breeding
   evolves_to: <child-species-slug>
   ```
   Leave the child species' own file unchanged (it's the target of the
   edge, not itself evolution-gated).
4. From a kind_robots checkout with the bible cloned beside it, dry-run
   first, then apply:
   ```bash
   npx tsx scripts/seed_bestiary.ts                 # dry run, confirms the edge parses
   npx tsx scripts/seed_bestiary.ts --write          # applies: sets Monster.evolutionKind='BREEDING', evolvesToId=<child's id>
   ```
5. Verify: `aquariumEconomy.ts`'s `qualifiesForBreedingEvolution()` gates on
   the offspring's average rolled stat across all six stats (see that
   function's own threshold constant) -- sanity-check the chosen base
   species' stat tier isn't so low that no roll could plausibly qualify, or
   the payoff `breed()` (kind_robots PR #2176) now supports will never
   actually fire for it in practice.
6. No kind_robots code change is needed for this step -- `breedFishForUser`
   (server/utils/aquarium.ts) and the UI from PR #2176 already handle
   `evolutionKind === 'BREEDING'` generically; they were just waiting on
   real seed data.

## Safety boundaries

- This is content authoring in a bible repo Silas treats as the source of
  truth for the whole bestiary -- not a database mutation. Do not attempt
  to set `Monster.evolutionKind`/`evolvesToId` directly via a database
  script as a substitute: `seed_bestiary.ts --write` unconditionally
  overwrites both columns from the bible's own `evolution_kind`/
  `evolves_to` fields on every run, so a direct DB edit not mirrored in the
  bible would be silently reverted the next time anyone reseeds.
- Nothing here touches pricing, capacity, or ownership logic -- purely
  content (which two species link, and how).

## Status

Filed as cthulhuquarium/t-058, `status: needs-human` (soft -- this is a
repo-access gap a differently-scoped session or Silas himself can clear;
other cthulhuquarium work is unaffected and continues normally).
