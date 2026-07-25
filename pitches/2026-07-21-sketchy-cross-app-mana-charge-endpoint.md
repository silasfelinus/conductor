# Pitch: Trusted-caller mana-charge endpoint for external apps (Sketchy critique/assignment)

date: 2026-07-21
project-target: kind-robots
status: approved

## The idea

Add one small authenticated API route, e.g. `POST /api/economy/mana/charge`, that lets a **trusted
external app** (Sketchy today; potentially other satellite apps later) charge a Kind Robots user's mana
for an action that app performed on its own infrastructure. Body: `{ krUserId, kind: 'text', estCostUsd,
refId, reason }`. The route does nothing new internally — it authenticates the caller via the existing
`requireMachineUser` pattern (`server/utils/comfyGate.ts:47` already combines this with `manaGate` for
Comfy image routes), then runs the existing `manaGate()` → `gate.commit()` sequence
(`server/utils/manaGate.ts`) exactly as every in-process kind_robots route already does, and returns the
new balance or a 402.

No new mana math, no new ledger, no new `ManaReason` (`GENERATION_TEXT` already covers both critique and
assignment generation from mana's point of view). The only genuinely new surface is that this specific
sequence currently only runs **in-process**, from a kind_robots route calling its own `withArtMana`/
`withTextMana` helper directly — there is no existing endpoint an external service can call to trigger the
same charge for work it did itself.

## Why it's worth doing

Filed as a direct follow-on to sketchy/t-004 (`projects/sketchy/TOKEN-TIERS.md`), which specs Sketchy's
free/paid tiers on top of the *real* mana system rather than a placeholder. Sketchy is architected as a
separate app with its own DB (`projects/sketchy/PRODUCT-SPEC.md` "App-Owned Schema") that "consumes Kind
Robots via API" — it was never going to be able to call `withTextMana` in-process the way
`server/api/art/enqueue.post.ts:163-170` calls `authAndGate` in-process, because Sketchy's request never
runs inside the kind_robots Nuxt process at all. Every other mana-gated action in the codebase gates a
route that also *performs* the AI action; this is the first case of "the action already happened
somewhere else, now go debit the ledger for it."

Without this, Sketchy either (a) has to duplicate mana-debit logic against the shared `User`/
`ManaTransaction` tables directly from a separate codebase — exactly the kind of shared-schema write
PRODUCT-SPEC.md and BOUNDARY.md already forbid without a pitch — or (b) skips real mana accounting
entirely and only enforces its own daily-count ceilings, which would silently let Sketchy usage go
un-costed against the shared economy Silas explicitly wants it to plug into
("The token/background economy should align with Kind Robots rather than creating a separate economy" —
`projects/sketchy/roadmap.yaml` `notes_from_silas`).

## Rough effort

small — one route, reusing `manaGate`/`applyMana`/`requireMachineUser` verbatim; no schema change, no new
enum value, no migration.

## Suggested first task

1. Add `server/api/economy/mana/charge.post.ts`: `requireMachineUser` (scoped to a new trusted-caller
   credential issued to Sketchy specifically, not the general Comfy machine-user role) → `manaGate({kind:
   'text', estCostUsd, userId: krUserId})` → on success, `gate.commit(refId, estCostUsd)` → return
   `{ ok: true, balance }`; on insufficient mana, return the existing 402 shape unchanged.
2. Add a contract test mirroring the existing Comfy-gate tests: valid trusted-caller token + sufficient
   mana → charged and balance decremented; insufficient mana → 402, no debit; wrong/missing caller
   credential → 401/403, no debit.
3. Issue Sketchy a scoped machine credential (out of band, not part of this migration) and document the
   two call sites in `projects/sketchy/TOKEN-TIERS.md` that will use it once built (critique: 8 mana;
   assignment generation: 1 mana — both already specced there).

## Open questions for Silas

1. Should the trusted-caller credential be a new `Role` value, a scoped API key distinct from the
   existing Comfy machine-user mechanism, or is reusing the exact same machine-user role (just called from
   a different service) acceptable? No existing pattern distinguishes "which external service" a
   machine-user request came from.
2. Rate-limiting/abuse: should this endpoint cap how much mana a single external caller can charge in a
   given window (defense against a compromised or buggy external app over-charging users), separate from
   the per-user mana balance check that already exists?
