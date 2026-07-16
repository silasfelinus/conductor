# Sharing & Access Grants — Design Spec

**Status:** design only — no schema change, no migration, no code in this document.
Per `BOUNDARY.md`'s data-model boundary, any actual Prisma migration in
`silasfelinus/kind_robots` goes through a separate pitch before implementation.
This spec is that pitch's design input.

**Origin:** Silas's 2026-07-05 digital-store-relaunch direction (kind-robots/t-008,
milestone m4). Two related gaps:

1. **Private-but-shared content** — content owned by one user (e.g. a private
   packmaker DLC pack) that specific *other* users, or purchasers, can be
   granted access to. Today's model is roughly public-or-private only.
2. **Project sharing** — a user grants another user viewing or admin rights to
   a project/area they don't own.

Silas has framed the packmaker DLC slice as a deliberate low-stakes security
proving ground for this exact infrastructure (see `projects/packmaker/roadmap.yaml`
and `projects/digital-storefront/roadmap.yaml` t-017, both currently blocked/waiting
on this design).

## Current state (grounding)

All facts below are from `silasfelinus/kind_robots` as of 2026-07-16.

- **No grant/ACL model exists.** `prisma/schema.prisma` has zero `Grant`,
  `Permission`, `Share`, or `ACL` models. Visibility today is a single
  `isPublic Boolean` field, repeated verbatim across ~20 content models:
  `ArtImage`, `ArtCollection`, `Bot`, `Character`, `Chat`, `Code`, `Composition`,
  `Dream`, **`Project`** (line ~482), `Facet`, `NarratorTopic`, `PitchSheet`,
  `Prompt`, **`Resource`** (line ~998), `Reward`, `Scenario`, `Server`,
  `SmartIcon`, `SocialPost`, `Theme`, and even `User` itself (a profile can be
  public/private). This is binary: owner-or-everyone. There is no middle state.
- **Closest existing pattern:** `UserRelation` (schema.prisma ~1462-1481) —
  `userId` / `relatedUserId` / `type` (`RelationType` enum: FRIEND, BLOCK,
  PARENT, CHILD, REFEREE) / `status` (`RelationStatus` enum: PENDING, ACCEPTED,
  DECLINED). It's a friend/family graph, not a resource-access grant, but its
  shape (owner ↔ target, typed relationship, status lifecycle) is exactly the
  shape a grant model should imitate.
- **Ownership/visibility checks are duplicated per-route**, not centralized.
  Example: `server/api/projects/[id].get.ts` (~line 35):
  `if ((!project.isActive || !project.isPublic || project.isMature) && !isAdmin && project.userId !== userId) throw 403`.
  Example: `server/api/resources/[id].patch.ts` (~lines 65-73) recomputes
  `isOwner`/`isAdmin` independently with slightly different logic. Grep shows
  roughly 140 files touching `isPublic`/ownership checks this way. There is no
  shared `canView(...)` helper today.
- **Auth primitives that exist and should NOT be re-implemented:**
  `server/utils/authGuard.ts` (`requireApiUser` / `requireAdminApiUser` /
  `getOptionalApiUser`, supporting JWT bearer / `x-api-key` / beta-admin-token)
  and `server/utils/authUser.ts` (`userIsAdmin()`: `Role === 'ADMIN' || id === 1`).
  `Role` enum: SYSTEM, USER, ASSISTANT, ADMIN, GUEST, BOT, DESIGNER, CHILD, FAMILY.
  Client-side route gating is a separate, coarser system
  (`middleware/navigation-access.global.ts` + `stores/helpers/navigationRouteAccess.ts`,
  string permission tags like `authenticated`/`family`/`mature`/`admin`) — that's
  role-based route access, orthogonal to per-object grants, and out of scope here.
- **No entitlement/purchase-fulfillment model exists.** `ManaTransaction`
  (~line 745) is a spendable-currency ledger (`reason` enum includes
  `PURCHASE`, `SUBSCRIPTION_GRANT`, `ADMIN_REFUND`), not a per-item unlock
  record. `server/api/stripe/checkout.post.ts` / `subscribe.post.ts` create
  real Stripe sessions but there is no webhook fulfillment code found that
  grants anything post-payment. `components/giftshop/credit-purchase.vue` is
  a UI mock (`setTimeout` + `alert()`, no real call). The only "unlock" model
  in the schema, `LifeAchievementUnlock` (~line 1715), is an unrelated
  life-sim game-mechanic record.
- **No Pack/DLC model exists yet.** Confirmed via grep — packmaker's pack
  definitions (`projects/packmaker/packs/*.yaml`) are conductor-side planning
  only; nothing has landed in kind_robots's Prisma schema.
- **`Project` model today** (schema.prisma ~452-506): `userId Int? @default(10)`
  (single owner FK), `isPublic Boolean @default(true)`, `isMature Boolean`,
  `isActive Boolean`, `conductorSlug String? @unique`, `channelKey`/`tabKey`,
  `status`/`priority` enums, `managerBotId`. No collaborator list — exactly
  the single-owner/binary-visibility gap t-008 is about.

## Design

### One generalized `Grant` model, not one per content type

Content grants (DLC/resource unlocks) and project grants (collaborator access)
are the same shape: *someone with authority over a subject lets a specific
other user see or manage it, for a reason, until something ends it.* Modeling
them as one polymorphic table avoids duplicating a near-identical model per
content type (`ProjectGrant`, `ResourceGrant`, `PackGrant`, ...) as new
grantable content types appear — and new ones will (Pack is not the last).

Proposed model (illustrative field names — the actual migration is a separate
pitch):

```
model Grant {
  id            Int           @id @default(autoincrement())
  granterId     Int           // FK User — who granted it (owner or admin)
  granteeId     Int           // FK User — who receives it
  subjectType   GrantSubject  // enum: PROJECT | RESOURCE | PACK | ...
  subjectId     Int           // id within that subject's own table (no FK —
                               // Prisma can't FK across polymorphic types;
                               // enforced/validated in application code, same
                               // pattern already used informally for
                               // Dream/Character/etc. cross-references)
  level         GrantLevel    // enum: VIEW | ADMIN | UNLOCK
  source        GrantSource   // enum: MANUAL | PURCHASE | SUBSCRIPTION | ADMIN
  refId         String?       // e.g. ManaTransaction id or Stripe session id,
                               // when source = PURCHASE/SUBSCRIPTION
  status        GrantStatus   // enum: ACTIVE | REVOKED | EXPIRED
  expiresAt     DateTime?     // null = permanent
  createdAt     DateTime      @default(now())
  updatedAt     DateTime      @updatedAt

  @@index([granteeId, subjectType, subjectId, status])
  @@index([subjectType, subjectId])
}
```

This mirrors `UserRelation`'s owner/target/type/status shape closely enough
that a reviewer familiar with that model should recognize the pattern
immediately — intentional, to keep the new model boring and easy to reason
about rather than novel.

### Visibility check: extend, don't replace, `isPublic`

`isPublic` stays exactly as-is for the common public/private case — no
existing column changes, no data migration on ~20 tables. The check a subject
is visible to a user becomes:

```
canView(subject, user) =
  subject.isPublic
  OR subject.userId === user.id
  OR user.isAdmin
  OR existsActiveGrant(user.id, subject.type, subject.id, level >= VIEW)
```

This should become one shared server-side helper (e.g.
`server/utils/contentAccess.ts`, new file) that the ~140 existing per-route
checks migrate onto incrementally — not a big-bang rewrite. New routes should
be required to use it from day one; that's a Reviewer-checklist item once the
model lands, not something this spec enforces retroactively.

### API surface (illustrative — routes, not committed contracts)

- `POST /api/grants` — create a grant. Caller must be the subject's owner or
  an admin. Body: `granteeId`, `subjectType`, `subjectId`, `level`, optional
  `expiresAt`. `source` defaults to `MANUAL` for this route (see below for
  `PURCHASE`).
- `DELETE /api/grants/:id` — revoke (sets `status = REVOKED`, does not hard
  delete — grants are an audit trail, same spirit as `ManaTransaction` being
  append-only).
- `GET /api/grants?subjectType=&subjectId=` — list grants on a subject
  (owner/admin only).
- `GET /api/grants/mine` — list what's been shared with the current user,
  for a "shared with me" surface in the workspace UI.

### How storefront entitlements plug in

**A purchase IS a grant.** When digital-storefront's Stripe webhook fulfillment
(currently missing — see Current State above) lands, its fulfillment step
should create exactly one `Grant` row: `source = PURCHASE`, `level = UNLOCK`,
`subjectType = PACK` (once packmaker's Pack model exists in kind_robots) or
`RESOURCE`, `refId` = the Stripe session/PaymentIntent id or the
`ManaTransaction` id it produced. No separate "Purchase" or "Entitlement"
table is needed — `Grant` already carries `source`/`refId` for provenance,
and `canView()` already treats an active grant as sufficient. This is also
why the model needs to support content subjects (`RESOURCE`, `PACK`) and not
just `PROJECT` — project sharing and DLC entitlement are two instances of one
mechanism, which was the whole point of generalizing it.

Subscriptions map the same way: `source = SUBSCRIPTION`, and a scheduled job
(not designed here) flips `status = EXPIRED` when the subscription lapses,
rather than deleting the row — same audit-trail rationale as above.

### Non-goals / explicitly out of scope

- **No group/team grants.** `granteeId` is a single user. Group sharing
  (e.g. "everyone in this Discord role") is a plausible future extension via
  a `GrantSubject`-style indirection but isn't needed for the packmaker/DLC
  or project-sharing cases in front of us — don't build it speculatively.
- **No change to `Role`-based route gating.** `navigation-access.global.ts`'s
  tag system stays as-is; it answers "can this class of user reach this
  route at all," which is orthogonal to "can this specific user see this
  specific object."
- **No family/parental-control redesign.** `Role.FAMILY`/`Role.CHILD` and
  `UserRelation`'s `PARENT`/`CHILD` relation types are a separate concern from
  content grants; this spec doesn't touch them, though a future spec could
  reasonably ask whether a `PARENT` `UserRelation` should imply an automatic
  `VIEW` grant over a child's content — flagged here, not designed here.
- **No migration, no new route code, no UI.** All of the above is the shape
  a future pitch should propose; this document is the design input to that
  pitch, per `BOUNDARY.md`.

## Open questions for Silas

1. Does `ADMIN`-level project grants need finer sub-permissions later (e.g.
   "can invite others" vs "can edit but not delete"), or is a flat
   VIEW/ADMIN split enough for the first cut?
2. Should a revoked grant's `refId`-linked purchase trigger anything (refund
   flow), or is revocation always a manual/admin action independent of billing?
3. Packmaker's Pack model doesn't exist yet in kind_robots — should this
   spec's `GrantSubject.PACK` variant be added to the enum now (unused until
   Pack lands) or deferred to whichever pitch adds the Pack model itself?
   Recommendation: defer — adding an enum value used by nothing yet just
   invites drift; the Pack-adding pitch should extend `GrantSubject` in the
   same migration that creates `Pack`.

## Related work

- `projects/packmaker/roadmap.yaml` — DLC pack content (Uncanny Valor, Arcane
  Whimsy) that this design exists to eventually gate.
- `projects/digital-storefront/roadmap.yaml` t-017 — entitlement design task,
  explicitly blocked on this spec landing.
- `UserRelation` (kind_robots `prisma/schema.prisma`) — structural precedent
  this design intentionally mirrors.
