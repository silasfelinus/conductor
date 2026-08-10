# Weekly Site Audit — 2026-08-09

This run follows `projects/global-ui/SITE-AUDIT-AGENT.md`, with the current session directive narrowing the audit to one meaningful site area: **route/navigation reachability and stale surface registration**. The previous report was `AUDIT-REPORT-2026-08-02.md`, so the weekly audit was due.

## Scope and method

Read-only cross-checks were performed against current `silasfelinus/kind_robots` `main` using the connected GitHub source/index tools. No live URLs were called, no npm/pnpm build was run, and no production data was touched.

The slice checked:

- the Memory Dungeon route and its Play-channel registration;
- the canonical project-placement table and its channel-content contract;
- the ArtJob trainer's previously reported `curate-request` disappearance;
- stale worker branches that could falsely resemble missing/live surface work.

## Findings

### 1. Memory Dungeon is currently reachable and registered — no gap

The game implementation still exists at `components/pages/memory-dungeon.vue`, with its store at `stores/memoryStore.ts`. Its page content is `content/play/memory.md`, which declares `channelKey: play`, `tabKey: experiments`, `dashboardKey: wonder`, and `dashboardTab: memory-dungeon`.

The corresponding navigation document, `content/channels/play/experiments.md`, labels the tab **Memory Dungeon** and routes it to `/play/memory` with `requiredRole: GUEST`. The code search also finds the dedicated public-navigation verification and responsive-audit references. This is not an orphaned or unreachable surface on current `main`.

**Action:** none. Do not create a duplicate restoration task.

### 2. The missing `curate-request` endpoint remains intentional cleanup — no regression

The 2026-08-02 audit filed `kind-robots/t-051` because `server/api/conductor/curate-request.post.ts` had disappeared. That task is now `done` with the removing history identified: Kind Robots PR #1244 deliberately retired the vision-model curator pass and removed the endpoint, helper, store actions, and front-end request button together.

Current `stores/artJobStore.ts` confirms the replacement behavior: every completed render with an `artImageId` is eligible for trainer review, and human feedback is posted directly to `/api/art/queue/:id/feedback`. There is no dangling `curate-request` caller to 404.

**Action:** none. The previous finding is resolved and should not be re-filed.

### 3. Project-placement navigation has an active structural guard

`utils/projectPlacements.ts` remains the canonical slug → channel/tab/route map. `utils/scripts/verifyChannelContent.ts` explicitly validates every placement's channel and tab against the Nuxt Content channel documents, validates parent-channel/default-tab relationships, and also checks page placement references and navigation component mounts.

For the inspected Coloring Book example, the placement (`plan/coloring`, `/coloring`) matches `content/channels/plan/coloring.md`; this is internally consistent even though older Conductor bootstrap placement fields use historical values. Per `docs/github-connector-worker.md`, those override presentation fields are temporary bootstrap fallbacks and are not a second source of truth.

**Action:** none from this audit slice. No contradictory live registration was found.

## Branch-medic cross-check

Two old Kind Robots worker branches initially looked like stranded work but are superseded:

- `worker/guest-achievement-records-safe-get`: its achievement-record route is byte-for-byte identical to current `main`; the work was already rescued and merged via PR #1700.
- `worker/digital-storefront-t-004-20260808-a83f`: its useful DLC/Pack-Grant slices are represented by merged PRs #1630 and #1643. Its remaining Character/Reward visibility work is isolated in open PR #1668, which is intentionally human-gated under `digital-storefront/t-005`.

No code from either stale branch should be re-opened or re-implemented.

## Follow-up tasks

**None.** This slice found no new actionable route/navigation defect. Creating a task merely to make the audit look productive would duplicate already-landed work or manufacture a bug.

## Outcome

The inspected navigation/reachability area is coherent on current `main`: Memory Dungeon is registered, ArtJob trainer curation has no dead caller, and project placements are covered by a structural content contract. The only unresolved related item is the already-known human-gated security PR #1668, which this audit does not alter.
