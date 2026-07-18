# Pitch: Pack model + packId FK + GrantSubject.PACK migration for DLC unlocks
date: 2026-07-18
project-target: kind-robots
status: awaiting-silas

## The idea
Add one new Prisma model, `Pack` (`id`, `slug` matching the packmaker manifest's
`id`, `title`, `ownerId`), plus a nullable `packId` FK on the four content
models a packmaker pack can generate items into — `Dream`, `Facet`,
`Character`, `Reward` — defaulting to `null` (zero effect on the ~20 existing
rows/models that never set it). In the same migration, add the deferred
`GrantSubject.PACK` value to the `Grant` model's subject-type enum (currently
`PROJECT | RESOURCE`, per the still-pending `2026-07-17-sharing-grant-model.md`
pitch), exactly as that pitch's design doc (`SHARING-SPEC.md`) recommended:
land `PACK` "in the same migration that creates `Pack`" rather than adding an
unused enum value ahead of time.

This closes the loop packmaker/SPEC.md §4 left open: DLC pack content
(Uncanny Valor, Arcane Whimsy, …) is currently stuck at all-or-nothing
`isPublic: false` because there was no per-item visibility mechanism — every
buyer either sees nothing or a manifest flip would have made it public to
everyone. With `Pack` as a join key, `canView()` (the shared helper
`2026-07-17-sharing-grant-model.md` also adds) extends to:

```
canView(content, viewer) =
  content.isPublic
  OR content.userId === viewer.id
  OR viewer.isAdmin
  OR (content.packId != null
      AND existsActiveGrant(viewer.id, PACK, content.packId, level >= VIEW))
```

Full design detail — the `Entitlement` (proof of purchase) vs. `Grant` (proof
of visibility) split, the fulfillment flow once wired into a Stripe webhook,
the four-model item-shape mapping, and revocation handling — lives in
`projects/digital-storefront/docs/dlc-unlock-design.md`. This pitch is that
design's required next step per `BOUNDARY.md`'s data-model boundary (no
kind_robots schema change without a pitch first) and per kind-robots/t-037's
own instruction to file it here before any schema edit.

## Why it's worth doing
Two projects converge on exactly this gap:
- **packmaker** has two DLC packs designed and generatable
  (packmaker/t-004, already `done` — the admin generator exists and can
  produce pack content today) but every item it creates is forced
  `isPublic: false`/`isMature: false` permanently, because there is no way
  to grant a specific buyer visibility into specific pack content without
  making it public to everyone. That's dead inventory until this lands.
- **digital-storefront** designed `Entitlement` (commerce proof) uniformly
  across every digital good, explicitly deferring the "how do four different
  content tables become visible from one purchase row" problem to whichever
  pitch adds `Pack` — this is that pitch.

Both blockers resolve with one small additive migration plus a `canView()`
extension, not a redesign of either existing system.

## Rough effort
small — one migration (one model, one FK column repeated across four tables,
one enum value) plus a small extension to `canView()`/`existsActiveGrant()`
(already being added by the sibling Grant-model pitch). No data backfill:
every existing row gets `packId: null` and is unaffected. The Stripe webhook
DLC-fulfillment wiring (creating the paired `Entitlement` + `Grant` on
`checkout.session.completed`) is an explicit non-goal here — separate
follow-on task, filed below, once a real DLC `Product` row exists.

## Suggested first task
Additive-only migration, scoped to exactly what the design doc lists and no
more:
- `CREATE TABLE "Pack" (id, slug UNIQUE, title, ownerId, createdAt)`.
- `ALTER TABLE` add nullable `packId` (FK → `Pack.id`) to `Dream`, `Facet`,
  `Character`, `Reward` — no default other than `null`, no backfill.
- Extend the `GrantSubject` enum with `PACK` (this migration is the one
  `SHARING-SPEC.md` and the sibling pitch both said to wait for).
- Extend `canView()`/`existsActiveGrant()` (from the sibling Grant pitch, or
  inline if that pitch hasn't landed first) to check `content.packId` against
  an active `PACK`-subject `Grant`, per the formula above.
- No webhook code, no admin UI changes, no pack publication flow in this
  task — those stay separate (digital-storefront's DLC-fulfillment follow-on,
  filed as a task once a real DLC `Product` row exists).

## Open questions for Silas
1. This pitch depends on `GrantSubject` already existing as an enum, which
   itself is still `awaiting-silas` in `2026-07-17-sharing-grant-model.md`.
   Should these land as one combined migration (`Grant` + `Pack` +
   `GrantSubject.PACK` together), or does the Grant pitch merge first and
   this one follows as a second, smaller migration once it has? Either order
   is additive-only and safe; flagging so the two don't get implemented out
   of the sequence SHARING-SPEC.md assumed.
2. `Pack.ownerId` — should DLC packs be owned by a house/system account (so
   `Grant.granterId` reads as "the store" rather than an individual admin
   user), or by whichever admin's session ran the packmaker generator for
   that pack? No existing pattern in packmaker/SPEC.md picks one.
3. Same revocation question the sibling Grant pitch raised, specific to
   purchases: when an `Entitlement` is marked refunded, should the paired
   `Grant.status → REVOKED` flip be automatic (part of the refund admin
   action) or a manual follow-up step? This pitch assumes automatic
   (one admin action, two rows updated) per the design doc, but it's your
   call.
