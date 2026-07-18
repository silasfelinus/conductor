# DLC Unlock Design — packmaker packs as store items

**Status:** design only — no schema change, no migration, no code in this
document. Per `BOUNDARY.md`'s data-model boundary, any actual Prisma
migration in `silasfelinus/kind_robots` goes through a separate pitch before
implementation.

**Origin:** digital-storefront/t-017 (milestone m5, "DLC website unlocks —
packmaker packs purchasable"). Was blocked on two cross-project, note-level
dependencies (not visible to `resolve_deps.py`, per CONTROL.md's 2026-07-17
cross-project-collision note): packmaker/t-003 (draft the two launch packs)
and kind-robots/t-008 (`SHARING-SPEC.md`, the general grant model). Both are
now `status: done` — this doc is the reconciliation those two unblocked.

## What already exists (don't re-invent)

Two designs already solve half of this problem each, written before either
depended on the other landing:

1. **`Entitlement`** (`digital-storefront/SPEC.md` §3-4, packmaker/SPEC.md
   §5) — answers *"did this user buy this `Product`?"* One row per purchase:
   `{ userId, productId, orderItemId, grantedAt, revokedAt }`. Already
   designed to cover a DLC `Product.type` uniformly with every other
   digital good (Mermaids PDF, mana top-ups, etc.) — "one model, no
   product-type-specific entitlement tables." This is a **commerce record**:
   it proves payment, nothing about content visibility.
2. **`Grant`** (`kind-robots/SHARING-SPEC.md`) — answers *"can this specific
   user see this specific content row?"* Polymorphic:
   `{ granterId, granteeId, subjectType, subjectId, level, source, refId,
   status, expiresAt }`. Explicitly designed with purchases in mind
   ("a purchase IS a grant") but left `GrantSubject.PACK` unadded, on the
   recommendation that whichever pitch adds the `Pack` model should extend
   the enum in the same migration — that pitch is what this design points
   at (see "Follow-on work" below).

packmaker/SPEC.md §4 called this out directly: DLC packs were stuck at
all-or-nothing `isPublic: false` "conservative but safe" placeholder
visibility specifically because t-008 hadn't landed yet. It has now. This
doc is the missing middle layer connecting `Entitlement` (proof of purchase)
to `Grant` (proof of per-item visibility) so that placeholder can retire.

## Design: Entitlement proves purchase, Grant proves visibility, Pack links them

A DLC pack (Uncanny Valor, Arcane Whimsy, …) contains a mixed bag of content
across **four different models** — locations (`Dream`, `dreamType: LOCATION`),
genres (`Facet`, `kind: GENRE`), characters (`Character` or `Dream` with
`dreamType: CHARACTER` — see "Character item shape" below), and rewards
(`Reward`) — per packmaker's `SCHEMA.md` item-shape mapping. A single
`Entitlement` row (scoped to one `Product`) can't directly answer "is *this*
`Character` row visible" across four unrelated tables without a join key.
`Grant`'s `subjectType`/`subjectId` polymorphism is built for exactly that
join; `Entitlement` was never meant to be walked backwards into four content
tables per view.

**The missing join key is a `Pack` model.** This resolves packmaker
SPEC.md §7's second open question ("is a YAML manifest sufficient
indefinitely, or does pack creation eventually need a real `Pack` Prisma
model") — yes, once a pack is purchasable, not before. A manifest stays the
authoring format (`projects/packmaker/packs/*.yaml`); a `Pack` row is created
when a manifest is promoted from `visibility: draft` to purchasable, one row
per pack (`id`, `slug` matching the manifest's `id`, `title`, `ownerId`).
Each content row generated from that pack's items gets a nullable `packId`
FK pointing at it (default `null` for all non-pack content — zero effect on
the ~20 existing `isPublic`-gated models that never set it).

Fulfillment flow, once wired into the Stripe webhook (`digital-storefront/t-022`
and its DLC-product follow-on, see below):

```
checkout.session.completed (Product.type = DLC, metadata.packSlug = "uncanny-valor")
  → create Order + OrderItem                              (existing SPEC.md §3 shape)
  → create Entitlement { userId, productId, orderItemId }  (existing SPEC.md §4 shape — proves purchase)
  → create Grant {                                          (new — proves visibility)
      granterId:  pack.ownerId,
      granteeId:  buyer.id,
      subjectType: PACK,
      subjectId:  pack.id,
      level:      UNLOCK,
      source:     PURCHASE,
      refId:      entitlement.id,
      status:     ACTIVE,
    }
```

Content visibility check (extends `canView()` from SHARING-SPEC.md, applied
identically across `Dream`/`Facet`/`Character`/`Reward`):

```
canView(content, viewer) =
  content.isPublic
  OR content.userId === viewer.id
  OR viewer.isAdmin
  OR (content.packId != null
      AND existsActiveGrant(viewer.id, PACK, content.packId, level >= VIEW))
```

DLC-pack content is created with `isPublic: false` permanently (never
flips true — unlike a `free`/`one-time` pack per packmaker SCHEMA.md's
existing `visibility: released` switch, which is unaffected by this design
and keeps working exactly as documented for non-DLC packs). The `Grant` row
is the only path to visibility for a `dlc`-hook pack's content, which is the
actual point of it being paid content.

Revocation/refunds mirror the existing `Entitlement.revokedAt` pattern
(SPEC.md §8's "mark refunded" admin action): when that action sets
`Entitlement.revokedAt = now()`, it should also set the paired `Grant.status
= REVOKED` (not delete — same audit-trail rationale SHARING-SPEC.md already
gives for `Grant`, and the pattern `ManaTransaction` already uses). One
admin action, two rows updated; no new admin surface needed.

## Character item shape (packmaker SPEC.md §7, resolved pragmatically)

Doesn't block this design either way: `Grant.subjectType` can point at
either `CHARACTER` or `DREAM` (`dreamType: CHARACTER`) — the visibility
mechanism is identical regardless of which shape a given pack's manifest
declares per packmaker SCHEMA.md's `itemShape` field. Packmaker's own
recommendation (full `Character` model for stat-block-bearing packs like
Uncanny Valor/Arcane Whimsy) stands; this doc doesn't need to arbitrate it.

## Non-goals / explicitly out of scope for this doc

- **No `Pack` Prisma model migration.** Field names above (`id`, `slug`,
  `ownerId`) are illustrative, same caveat SHARING-SPEC.md already applies
  to `Grant`.
- **No `GrantSubject.PACK` enum edit, no `packId` column addition.** Per
  SHARING-SPEC.md's own recommendation, these land together in the migration
  that creates `Pack` — a separate pitch, not this design doc.
- **No webhook code.** `digital-storefront/t-022` (Mermaids PDF fulfillment)
  stays scoped to the PDF product only; DLC fulfillment is a distinct
  follow-on task (filed below) once a `Product` row for a real pack exists,
  which itself waits on Silas approving pack contents for generation
  (packmaker/t-004, still ahead of this in the build order).
- **No live Stripe configuration or pack publication.** Same hard rules as
  every other digital-storefront doc: test mode only, nothing sold until
  Silas explicitly flips that switch.

## Follow-on work (filed as new roadmap tasks, not implemented here)

- kind-robots: add the `Pack` model + `packId` FK (on `Dream`/`Facet`/
  `Character`/`Reward`) + `GrantSubject.PACK` enum value in one migration,
  and extend the shared `canView()`/content-access helper to check it —
  the actual schema pitch SHARING-SPEC.md deferred.
- digital-storefront: extend the Stripe webhook fulfillment path to handle
  `Product.type = DLC` (create the paired `Entitlement` + `Grant`), once a
  real DLC `Product` row exists for an approved pack.

## Related work

- `projects/digital-storefront/SPEC.md` §3-4, §9 — `Product`/`Order`/
  `Entitlement` shape this design builds on unchanged.
- `projects/kind-robots/SHARING-SPEC.md` — `Grant` model and `canView()`
  this design builds on unchanged.
- `projects/packmaker/SPEC.md` §4-5, §7 and `projects/packmaker/packs/SCHEMA.md`
  — the interim all-or-nothing visibility rule this design retires for
  `dlc`-hook packs, and the item-shape mapping this design's visibility
  check must span.
