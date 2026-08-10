# t-058 audit: m3 (slug parity + project creation surfaces) / m4 (sharing & access control) gaps

Read-and-report audit, per t-058's own scope. Findings below are grounded in exact file
paths/lines cited inline; none are invented requirements.

## Framing correction

Both milestones already have many `done` tasks tagged `milestone: m3` / `milestone: m4`
in this project's roadmap.yaml (m3: t-003–t-007, t-011–t-021, t-024, t-025, t-046, t-048,
t-056, t-057; m4: t-008, t-029, t-037, t-044, t-045, t-047, t-049, t-050 — all `status:
done`). The milestone-level `status: not-started` fields are stale/unmaintained, not
literally accurate — t-058's own note clarified "zero tracked tasks" meant zero currently
*open* tasks (the `validate_roadmaps.py` "active project has no open tasks" gate), not
that no work happened. A large amount of real design and implementation already landed
under both milestones. The real question is whether the milestone *scope* is done — it
is not, for either.

## m3 — Slug parity + project creation surfaces: NOT fully covered

**Gap 1 — `conductorSlug` is not immutable, despite being documented as "the stable key".**
`PROJECT-CREATION.md:15`: *"`Project.slug` starts equal to the conductor slug but stays
user-editable on the KR side; `conductorSlug` is the stable key."* But
`server/api/projects/[id].patch.ts:89-91` puts `conductorSlug` in the general mutation
allowlist (`projectMutationFields`, `index.ts:44`) with no immutability guard — any
project owner can silently rewrite the join key that links a kind_robots `Project` to
its `projects/<slug>/roadmap.yaml` directory. The conductor-side bulk sync path
(`server/api/conductor/sync.post.ts:84`: `conductorSlug: existing.conductorSlug ??
project.slug`) already protects it correctly (set-once); the general owner-facing PATCH
route doesn't mirror that pattern.

**Gap 2 — The only general "new project" UI form omits the slug field entirely.**
`PROJECT-CREATION.md` Surface 2 (lines 60, 76) requires the UI to prompt for and let the
user override a derived slug, and (line 150) *"return 409 and prompt for a different
slug. DECIDED."* But `components/pages/conductor-project-gallery-page.vue`'s create form
(`createForm`, ~lines 34-66, submit handler ~605-628) has only `title`/`description`/
`status`/`priority` — no slug field, and a 409 collision just shows the generic backend
"Record already exists." with no re-prompt UX. `conductor-page.vue`'s only
`createProject` call (~line 1775) is an admin-only "sync missing projects"
reconciliation action using pre-known conductor slugs, not a general creation form — it
doesn't fill this gap.

**Gap 3 — At least three undocumented additional live project-creation surfaces.**
Beyond the two "confirmed" surfaces (both via `POST /api/projects`):
1. AppMaker self-serve (`components/pages/appmaker-page.vue`, live nav card in
   `stores/helpers/conductorCards.ts:79`) calls `POST /api/appmaker/scaffold-request`
   and `POST /api/appmaker/github/create-app`
   (`server/api/appmaker/scaffold-request.post.ts:68-83`,
   `server/api/appmaker/github/create-app.post.ts:122-137`) — both create `Project` rows
   via `tx.project.create` directly, bypassing `POST /api/projects`, each with its own
   independently-maintained slug-collision pre-check and `SLUG_RE` regex.
   `appmaker-page.vue:169`'s own comment flags this: *"Mirrors
   `server/api/appmaker/scaffold-request.post.ts`'s `SLUG_RE` — keep in sync."*
2. `server/api/conductor/sync.post.ts` (~line 109) creates Projects directly, a fourth
   path, also outside `POST /api/projects`.
3. `server/api/model-builder/items/[id]/commit.post.ts` (`createRecord`, `'Project'`
   case, lines 541-544; `projectFields()` lines 308-317) creates bare `Project` rows
   with **no `slug`/`conductorSlug` set at all** — private (`isPublic: false, isActive:
   false`) orphan Projects outside slug parity/conductor sync entirely, and absent from
   `PROJECT-CREATION.md`.

**What's confirmed working, no gap:** DB-level uniqueness on both `slug`/`conductorSlug`
(`prisma/schema.prisma:431,438`) and P2002→409 mapping (`server/utils/error.ts:163-168`)
correctly satisfy the "409 on collision" decision for the official route and both
AppMaker routes. The auto-Todo-on-creation flow `PROJECT-CREATION.md` called
"not yet implemented" is now implemented and tested (t-056/t-057) — that part of the doc
is just stale.

## m4 — Sharing & access control: infrastructure built, its named use cases unwired

**What already exists:** `SHARING-SPEC.md` (t-008, approved) is a full design doc. The
Prisma `Grant` model (`prisma/schema.prisma:894-911`, `GrantSubject{PROJECT,RESOURCE,
PACK}`, `GrantLevel{VIEW,ADMIN}`, lines 2578-2604) landed via t-044, extended for PACK
via t-050. `server/utils/contentAccess.ts` implements `canView()`/`existsActiveGrant()`/
`viewablePackIds()` exactly per `SHARING-SPEC.md:171-192`'s formula.

**Gap 1 — No API surface to create/list/revoke a Grant exists anywhere.**
`SHARING-SPEC.md:140-150` specifies `POST /api/grants`, `DELETE /api/grants/:id`,
`GET /api/grants?subjectType=&subjectId=`, `GET /api/grants/mine`. `find server -iname
"*grant*"` returns nothing. The model is schema-only; no user or admin can create a
Grant row anywhere in the live app. **`SHARING-SPEC.md:138` explicitly labels this API
surface "illustrative — routes, not committed contracts,"** so implementing it is a
backend decision that needs its own approval, not a documented gap that's simply
unbuilt yet.

**Gap 2 — The two use cases m4's own title names (project grants, private-but-shared
content) have zero route integration; only the later PACK/DLC use case is wired.**
Every `existsActiveGrant(` call site outside `contentAccess.ts` is `'PACK'`-only
(`server/api/dreams/[id]/facets.get.ts:41`, `server/api/dreams/[id].get.ts:47`,
`server/api/facets/[id].get.ts:43`). A repo-wide grep for `GrantSubject.PROJECT`,
`GrantSubject.RESOURCE`, or `subjectType: 'PROJECT'/'RESOURCE'` outside
`contentAccess.ts`/schema returns zero matches; `canView()` itself is imported by zero
files. `SHARING-SPEC.md`'s own named motivating "before" route,
`server/api/projects/[id].get.ts:36-38`, is unchanged (`isActive`/`isPublic`/`isMature`
+ admin/owner only — no `existsActiveGrant`/`canView`). Same for
`server/api/resources/[id].get.ts` (only imports `effectiveShowMature`, not `canView`).

**Gap 3 — No UI for sharing at all.** `grep -rli grant components/ stores/` finds no
Grant-related UI or store code. No "share with…" affordance, no "shared with me" surface
— `SHARING-SPEC.md:149`'s `GET /api/grants/mine` has nothing to drive.

**Not a gap:** the Pack/DLC entitlement half (t-008→t-029→t-037→t-044→t-050→
digital-storefront's `dlc-unlock-design.md`) is fully designed and wired for that slice.
`Role`-based route gating is explicitly out of scope per `SHARING-SPEC.md:176-179`.
`BOUNDARY.md` has no access-control-specific constraint beyond normal schema-change
gating (the Grant model already exists/migration-approved).

## Disposition (revised after review — see PR #2002)

Neither milestone is closed/retitled — both have real, narrowly-scoped remaining work
traceable to this project's own prior design docs. Milestone status flipped
`not-started` → `in-progress` to reflect that substantial real work already landed
under both (the field was simply never updated as t-003 through t-050 closed).

**Corrected from the rejected first attempt (PR #2002):** every gap above that requires
a change to the shared backend/API goes through `pitches/` per `BOUNDARY.md` and
`SHARING-SPEC.md:138`'s own "illustrative, not committed" label — not straight to a
`ready` implementation task. Only work that is genuinely local/front-end-only, or is
documentation, is filed as a directly-actionable `ready` task:

- **t-059** (`ready`) — document all live Project-creation surfaces in
  `PROJECT-CREATION.md` (Gap 3). Docs-only, no code change.
- **t-060** (`ready`) — add an editable slug field + slug-specific 409 UX to the
  New Project form (Gap 2). Front-end-only, no shared backend contract change.
- **t-061** (`needs-human`, soft, pitch written) — `conductorSlug` immutability
  (Gap 1) and consolidating the three independent slug-collision implementations
  into one shared helper (Gap 3's second half) both touch shared backend route code.
  Pitch: `pitches/2026-08-10-kind-robots-slug-integrity.md`.
- **t-062** (`needs-human`, soft, pitch written) — implement `SHARING-SPEC.md`'s
  illustrative Grant CRUD API and wire `canView()`/`existsActiveGrant()` into the
  `projects`/`resources` view routes, plus a minimal share/shared-with-me UI (m4
  Gaps 1-3, bundled as one capability since t-063/t-064/t-065 only make sense once
  the API exists). Pitch: `pitches/2026-08-10-kind-robots-grant-sharing-api.md`.
