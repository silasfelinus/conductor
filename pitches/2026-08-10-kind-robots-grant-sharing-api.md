# Pitch: Implement the Grant CRUD API and wire it into Project/Resource views

date: 2026-08-10
project-target: kind-robots
status: awaiting-silas

## The idea

`kind-robots/t-058`'s audit (`projects/kind-robots/docs/t-058-m3-m4-gap-audit.md`,
m4) found that m4's own named use cases — project grants, private-but-shared
content — have real, approved design (`SHARING-SPEC.md`, t-008) and real
supporting infrastructure (the `Grant` Prisma model, t-044/t-050; the
`canView()`/`existsActiveGrant()`/`viewablePackIds()` helpers in
`server/utils/contentAccess.ts`) but are entirely unreachable end-to-end: there is
no API route to create, list, or revoke a Grant anywhere (`find server -iname
"*grant*"` returns nothing), no route besides the later PACK/DLC slice actually
calls `existsActiveGrant`/`canView`, and no UI exists to drive any of it.

`SHARING-SPEC.md:138` is explicit that its documented API surface is
"illustrative — routes, not committed contracts," so implementing it is the
backend decision this pitch asks Silas to make, per `BOUNDARY.md`. Proposed scope,
straight from the spec (lines 140-150):

1. `POST /api/grants` — create (owner/admin-only, `source: MANUAL`).
2. `DELETE /api/grants/:id` — revoke (status flip to `REVOKED`, no hard delete —
   an audit trail, same spirit as `ManaTransaction`).
3. `GET /api/grants?subjectType=&subjectId=` — list grants on a subject
   (owner/admin only).
4. `GET /api/grants/mine` — list what's shared with the current user.
5. Migrate `server/api/projects/[id].get.ts` and `server/api/resources/[id].get.ts`
   (+ `.patch.ts`) onto `canView()`/`existsActiveGrant()` — these are
   `SHARING-SPEC.md`'s own named motivating "before" routes, still unmigrated even
   though the helper they'd call already exists.
6. A minimal "Share this project/resource" action and a "Shared with me" list
   surface in the workspace UI — without it the Grant model has no
   end-user-reachable way to ever be populated even once 1-5 land.

No schema change (the `Grant` model, its enums, and the access-check helpers
already exist and are already migration-approved from t-044/t-050) — this pitch
is purely about exposing them through routes and wiring the two real use cases in.

## Why it's worth doing

This closes the loop on infrastructure that already shipped twice (t-044, t-050)
but has never been reachable by an actual user or admin action. It also directly
unblocks the two use cases m4's own title names — private-but-shared content and
project grants — which currently have zero coverage; only the later PACK/DLC
entitlement slice (digital-storefront) uses any of this machinery today.

## Rough effort
medium — four small routes, two existing-route migrations (formula already
implemented in `contentAccess.ts`, so this is call-site wiring, not new logic),
and a minimal UI surface (share action + a list view). No migration risk.

## Suggested first task
If approved: implement the four `/api/grants*` routes first (own task), then a
second task to migrate `projects/[id].get.ts` + `resources/[id].get.ts`/`.patch.ts`
onto `canView()`, then a third for the minimal share/shared-with-me UI — each
depends on the previous, same shape as this pitch's own numbered list.
