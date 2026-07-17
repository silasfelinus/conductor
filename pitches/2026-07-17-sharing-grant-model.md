# Pitch: Add a generalized Grant model for private-but-shared content and project sharing
date: 2026-07-17
project-target: kind-robots
status: awaiting-silas

## The idea
Add one new Prisma model, `Grant`, to `silasfelinus/kind_robots`, replacing the
implicit "you'd need a new table per content type" path with a single polymorphic
table that answers *does this user have access to this specific object*. A grant
row records who granted access (`granterId`), who received it (`granteeId`), what
kind of thing it's on (`subjectType`: `PROJECT | RESOURCE | PACK`), which row of
that type (`subjectId`, unenforced by FK — same informal cross-reference pattern
already used for Dream/Character/etc.), an access level (`VIEW | ADMIN | UNLOCK`),
where it came from (`source`: `MANUAL | PURCHASE | SUBSCRIPTION | ADMIN`, with an
optional `refId` back to the `ManaTransaction` or Stripe session that produced it),
and a lifecycle (`status`: `ACTIVE | REVOKED | EXPIRED`, plus optional `expiresAt`
— revocation flips status rather than deleting the row, an audit trail in the same
spirit as `ManaTransaction` being append-only).

This is purely additive: no existing column changes, no data migration on any of
the ~20 tables that currently carry `isPublic`. The migration creates `Grant` plus
its three enums (`GrantSubject`, `GrantLevel`, `GrantSource`; `GrantStatus` can
reuse an existing pattern or be its own small enum) and nothing else. A new shared
helper, `server/utils/contentAccess.ts`, exposes `canView(subject, user)` as
`subject.isPublic OR subject.userId === user.id OR user.isAdmin OR
existsActiveGrant(...)` — existing per-route checks migrate onto it incrementally,
not in this task.

Full design detail, current-state grounding (grep counts, existing model shapes,
auth primitives to reuse), and the storefront-entitlement mapping already live in
`projects/kind-robots/SHARING-SPEC.md` — this pitch is that spec's required
next step per `BOUNDARY.md`'s data-model boundary (no kind_robots schema change
without a pitch first).

## Why it's worth doing
Two independent efforts are blocked waiting on exactly this:
- **digital-storefront/t-017** (entitlement design) can't proceed — there is
  currently no way to record "user X bought pack Y" anywhere except a
  `ManaTransaction` row, which is a currency ledger, not an unlock record.
  `Grant` with `source: PURCHASE` is the entitlement itself; no separate
  Purchase/Entitlement table is needed.
- **packmaker's DLC packs** (Uncanny Valor, Arcane Whimsy) are explicitly framed
  by Silas as a deliberate low-stakes security proving ground for private-but-
  shared content — there's no mechanism to gate them today.

Beyond unblocking those two, it also gives project collaboration (a second
gap SHARING-SPEC.md covers) a real mechanism instead of the current
single-owner-only `Project.userId`, and replaces ~140 duplicated,
independently-drifting `isPublic`/ownership checks with one helper new routes
can be required to use from day one.

## Rough effort
medium — one migration (small: one model, a few enums, no data backfill) plus
one new shared helper file. The larger effort is incremental: migrating the
~140 existing per-route checks onto `canView()` is explicitly NOT part of this
task (see Suggested first task) and should happen opportunistically as routes
are touched, not as a big-bang follow-up.

## Suggested first task
Additive-only migration scoped to exactly what SHARING-SPEC.md designs and no
more, per its own recommendation on open question 3 below:
- `CREATE TABLE "Grant" (...)` with the fields/indexes SHARING-SPEC.md lists
  (`@@index([granteeId, subjectType, subjectId, status])`,
  `@@index([subjectType, subjectId])`).
- New enums: `GrantSubject { PROJECT RESOURCE }` (see open question 3 —
  `PACK` deferred), `GrantLevel { VIEW ADMIN UNLOCK }`,
  `GrantSource { MANUAL PURCHASE SUBSCRIPTION ADMIN }`,
  `GrantStatus { ACTIVE REVOKED EXPIRED }`.
- `server/utils/contentAccess.ts`: `canView(subject, user)` and
  `existsActiveGrant(userId, subjectType, subjectId, minLevel)` — new file,
  no existing route rewired yet.
- No new API routes (`POST /api/grants` etc.) in this first task — those are
  a natural follow-up once the model exists, scoped separately so this PR
  stays small and reviewable as a pure schema + helper change.

## Open questions for Silas (carried from SHARING-SPEC.md, unresolved — need your call before implementation)
1. Does `ADMIN`-level project grants need finer sub-permissions later (e.g.
   "can invite others" vs "can edit but not delete"), or is a flat
   VIEW/ADMIN split enough for the first cut?
2. Should a revoked grant's `refId`-linked purchase trigger anything (refund
   flow), or is revocation always a manual/admin action independent of
   billing?
3. Packmaker's Pack model doesn't exist yet in kind_robots. SHARING-SPEC.md
   recommends deferring `GrantSubject.PACK` until the Pack-adding pitch lands
   in the same migration that creates `Pack`, rather than adding an unused
   enum value now. This pitch follows that recommendation — flagging here in
   case you'd rather add it preemptively.
