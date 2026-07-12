# Model Builder — idempotent COMMIT executor (t-013 / t-014 / t-015)

**Repo:** `kind_robots` · **PR:** #190 · **Date:** 2026-07-12
**Directed by:** Silas (full build, merge when CI green)

COMMIT went from preview-only to a real, idempotent canonical write. Completes
milestone **m4**'s core (reference runs t-016–t-018 remain the gated live proof).

## Endpoint — `POST /api/model-builder/items/[id]/commit`

Owner/admin guarded; supports `{ dryRun: true }` to return the plan without writing.

Per action:
- **ASSET_ONLY** → set the source record's `artImageId` to the item's generated
  ArtImage (works across all seven source models).
- **UPDATE** → write the item's pitch into ONE safe text field per model
  (`pitch`/`backstory`/`description`) — not arbitrary field parsing.
- **CREATE** → create a **private/inactive (draft-early)** record of the mapped
  target type (`expand-characters` → Character, etc.) and **link** it to the
  source via the known relation (Dream→Character/Reward/Scenario, Project→Bot,
  Character→Reward, Scenario→Character), all in one `$transaction`.

## Idempotency & recovery

- **Atomic claim:** `updateMany({ where: { id, idempotencyKey: null }, data: {
  idempotencyKey: 'commit:<id>' } })`. `count === 0` ⇒ already committed → return
  the recorded target. Exactly one commit proceeds; a replay never duplicates.
- **Compensating cleanup:** a write failure *after* the claim releases the key so
  a retry can run.
- **No orphans:** CREATE + link share a transaction.
- The item records its result in `targetType`/`targetId` + the COMMIT stage note,
  so it survives resume and the UI shows `→ Type #id`.

## Safety

Reversible: created records are private drafts; promotions/updates touch only the
one field/relation they own. The endpoint writes only on an explicit per-item user
click — nothing runs at deploy time. No schema change.

## Verification

- Pre-merge: whole-project `vue-tsc` validates **every** Prisma field/relation
  name in the executor against the generated client + Vercel preview build. Green.
- **Live proof pending (t-022):** promote a Character hero → confirm `artImageId`;
  run a Dream → 3 Characters expansion → confirm three private linked Characters
  and NO duplicates on commit replay.
