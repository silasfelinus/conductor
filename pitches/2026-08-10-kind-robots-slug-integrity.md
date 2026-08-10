# Pitch: Make `conductorSlug` immutable and consolidate Project-creation slug-collision logic

date: 2026-08-10
project-target: kind-robots
status: awaiting-silas

## The idea

Two small, related backend fixes found by `kind-robots/t-058`'s audit
(`projects/kind-robots/docs/t-058-m3-m4-gap-audit.md`, m3 Gaps 1 and 3):

1. **`conductorSlug` immutability.** `PROJECT-CREATION.md:15` documents it as "the
   stable key" linking a kind_robots `Project` to its
   `projects/<slug>/roadmap.yaml` directory in this repo, but
   `server/api/projects/[id].patch.ts` puts it in the general owner-facing mutation
   allowlist (`projectMutationFields`, `index.ts:44`) with no immutability guard —
   any project owner can silently rewrite it today. `server/api/conductor/sync.post.ts:84`
   already has the correct pattern for its own write path
   (`conductorSlug: existing.conductorSlug ?? project.slug` — set once, never
   overwritten). Copy that shape into the general PATCH route: once `conductorSlug`
   is non-null, reject or silently ignore any attempt to change it.

2. **One shared slug-collision helper instead of three.** At least three live
   code paths create `Project` rows outside `POST /api/projects`, each with its
   own independently-maintained slug-normalize/collision-check logic:
   `server/api/appmaker/scaffold-request.post.ts`,
   `server/api/appmaker/github/create-app.post.ts` (both flagged by
   `appmaker-page.vue:169`'s own "keep in sync" comment), and
   `server/api/conductor/sync.post.ts`. Extract one shared helper (slug
   normalization + `SLUG_RE` + the P2002→409 collision pattern `index.ts` already
   uses) and have all creation paths call it, instead of three copies that can
   silently drift apart. `server/api/model-builder/items/[id]/commit.post.ts`'s
   `createRecord('Project')` case creates orphan Projects with no slug at all —
   this pitch does not resolve whether that's intentional (a "draft idea" state
   exempt from slug parity) or a bug; flagging it for Silas to decide in "Suggested
   first task" below rather than guessing.

Both are shared-backend route changes per `BOUNDARY.md`'s data-model boundary
("must not add production Prisma models, alter shared migrations... create a
proposal describing the desired backend change" — no schema change here, but the
PATCH-route guard and the cross-route refactor both touch shared backend contracts,
so this project's own boundary rule routes them through a pitch first rather than
a direct roadmap `ready` task).

## Why it's worth doing

`conductorSlug` is the single join key between this repo's `roadmap.yaml` files and
the live kind_robots `Project` row — if it silently drifts, conductor and the app
disagree about which project a row belongs to with no error anywhere. The
slug-collision triplication is lower-severity but a real maintenance hazard: the
AppMaker routes' `SLUG_RE` has already needed a manual "keep in sync" comment
because there is no single source of truth.

## Rough effort
small — two narrowly-scoped route changes, no schema/migration involved.

## Suggested first task
If approved: one task to add the immutability guard to
`server/api/projects/[id].patch.ts` (mirroring `sync.post.ts`'s pattern) plus a
regression test asserting a PATCH with a changed `conductorSlug` on an
already-set project is rejected/ignored. A second task to extract the shared
slug helper and point all three non-canonical creation paths at it, plus Silas's
call on the model-builder orphan-Project slug question above.
