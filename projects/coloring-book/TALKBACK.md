# coloring-book — Project TALKBACK

Append-only. Never edit or delete a prior entry.

## 2026-07-14 | Reviewer → Worker | coloring-book/t-019 | pattern

**Decision:** audited already-merged work (self-executed as Worker in a solo burst-mode session; kind_robots PR #260 merged)

**Failure category:** null (clean first pass on the scoped portion)

**What was good:**
- Read the actual kind_robots implementation before touching anything, which caught that the task description's "placeholder scaffold" framing was stale — the coloring engine (coloringStore.ts, coloring-canvas.vue, coloring-book-manager.vue) is functionally complete, not a placeholder.
- Kept the diff to exactly what was specified and verifiable: one tutorial-card entry, shaped identically to its five siblings.
- Didn't fabricate or skip the missing art assets — queued both via the established `projects/art-prompts.yaml` `requests:` mechanism instead of leaving them undocumented or inventing placeholder files.

**What to improve:**
- Could not run `eslint`/`vue-tsc` in kind_robots locally (`.nuxt/eslint.config.mjs` missing pre-`nuxt prepare`) — verification leaned on shape-parity review instead of tooling. Low risk given the change (single object-literal addition, no new imports/types), but a future session touching this file should run `nuxt prepare` first if time allows.

**Kaizen task:** t-020 — thicken coloring-book-page.vue's Generate/Proposals/Prompts tabs and add a second page set to coloring-book-manager.vue's SET_SLUGS, once t-006 lands.

**Pattern note:** Second instance this cycle (see conductor/t-012 pattern) of a roadmap task's note describing "scaffold"/"placeholder" state that had already moved past that description by the time it was picked up. Worth a standing reminder: read the target repo's current state before trusting a task's framing, especially on tasks that have sat `ready` for several days while related work merged elsewhere.

## 2026-07-17 | Reviewer → Worker | coloring-book/t-022 | pattern (autonomous conductor cycle)

**Decision:** merged conductor PR #697 (inventory reconciliation for Monster Recast book 1).
Recurring task flipped back to `status: ready` per convention; kaizen task t-029 filed.

**Failure category:** n/a (clean pass, recurring task in progress, not closed).

**What was good:**
- Reconciled all 18 represented_concept_ids without renaming or guessing files; the one
  ambiguous match (gothic-schoolgirl → mr-025) was explicitly flagged
  `needs_visual_verification: true` with a transparent "by elimination, not by text match"
  note rather than silently promoted to a confident match.
- Kept `accepted` fields untouched — respected the manifest's "confirmed approvals only from
  Silas" policy even though the task's own note allows "record accepted working files" later
  in the cycle.
- Verification was concrete and checkable: existence-checked every new inspiration path,
  reran both status scripts, confirmed the audit_roadmaps.py warning count was unchanged
  (pre-existing, unrelated).

**What to improve:**
- The elimination-only match is currently discoverable only by reading roadmap/proposals.yaml
  prose — nothing in `coloring_proposal_status.py --check` output flags it. Filed as t-029.

**Kaizen task:** t-029 — surface `needs_visual_verification`/elimination-only inspiration
matches directly in `coloring_proposal_status.py --check` output instead of leaving them to
prose notes.

## 2026-07-17 | Worker → Reviewer | coloring-book/t-022 | pattern (infra concurrency collision)

**Decision:** fixed a real infra bug found while checking on the recurring color-production
pass; no code claim beyond a one-line workflow config change. Task stayed `recurring: true`,
flipped back to `status: ready`.

**Detail:**
- `Process coloring art events` (process-color-art-events.yml, added earlier this same task's
  cycle as the connector-safe event bridge) had its first-ever run fail: 0/18 ArtJobs
  succeeded (2 immediate ComfyUI connection-refused, 16 timeouts after 300s).
- Cross-checked GitHub Actions run history: `Coloring Book Color ArtJobs`
  (monster-recast-art-jobs.yml) ran 18:37:54-21:10:53Z (success) while the event-bridge run
  went 20:34:48-22:00:43Z (failure) — a ~36-minute overlap. Both workflows call
  `consume_coloring_book_color_art.py --live` against the exact same `color-art-jobs.yaml`
  queue and the same single-worker render backend, but carried *different*
  `concurrency.group` values, so GitHub Actions ran them fully in parallel instead of
  serializing. The failed run's reported ArtJob ids (228, 229, 231, 233, 234, 236, 237,
  239-249) skip ids that the concurrently-running successful workflow was almost certainly
  consuming at the same moments — consistent with two workflows racing the same backend.
- This is exactly the "a second event would risk duplicate generation" risk this task's own
  note already flagged from an earlier cycle, just triggered by the *pre-existing*
  daily/push-triggered workflow rather than a second manually-dropped event file.
- Fix: unified `process-color-art-events.yml`'s concurrency group to
  `coloring-book-color-artjobs` (matching `monster-recast-art-jobs.yml`) so the two workflows
  now queue behind each other instead of hitting the render backend simultaneously. No other
  workflow touches either script, so no third group needed updating.
- The preserved event file (`color-art-events/20260717T203500Z-monster-recast-batch-01.yaml`)
  needs no manual edit — it self-retries on the next hourly cron and should now succeed since
  it won't race the other workflow.

**Suggested action:** when adding any new automation that shares a mutable resource (a queue
file, an external render backend, a rate-limited API) with an existing workflow, always check
whether an existing `concurrency.group` already covers that resource and reuse it — a new,
uniquely-named group only prevents self-collision, not collision with siblings touching the
same backend.

## 2026-07-25 | Reviewer (scheduled agent run) | coloring-book/t-030 | pattern

**Decision:** merged kind_robots PR #950.

**Failure category:** null — real production bug, found and fixed first-pass clean.

**Subject:** t-030 was filed the same day by an ai-art-academy/t-010 roadmap-accuracy
cycle after it spot-checked `GET /api/art/queue/stats` and found 17+ permanently-failed
coloring-book ArtJobs, all failing identically on a seed-out-of-range Prisma error. This
session picked up the filed task directly rather than re-deriving the root cause.

**Detail:**
- Root cause (already correctly diagnosed by the filing cycle): `ArtImage.seed` is a
  32-bit MySQL `Int`, but 14 separate fallback seed generators across
  `server/api/comfy/**`, `server/utils/artJobRetry.ts`, `server/utils/comfyTestClient.ts`,
  and `server/api/art/queue/[id]/edit.post.ts` all produced values up to `10^15` — six
  orders of magnitude past the column's range.
- Fixed all 14 call sites (mechanical `grep -rl` + `sed`, then manually diffed each hunk)
  from `Math.floor(Math.random() * 1_000_000_000_000_000)` to
  `Math.floor(Math.random() * 2_147_483_647)`, plus added a defensive clamp
  (`clampArtImageSeed()`) at the one Prisma write site (`save-generated.post.ts`) as a
  second line of defense.
- While rechecking ai-art-academy/t-010's lane 3 (home-relay health) in the same session,
  incidentally queued job 2276 and found its seed was `25204709996469` — itself an
  out-of-range value generated by the pre-fix code still live on `main` at that moment.
  Good independent confirmation the bug was real and still active, not stale.
- Verified: prettier + eslint clean on all 15 touched files (a handful of pre-existing
  unrelated warnings/errors on 4 files confirmed present on `main` before this change too,
  not introduced by it); full-project `vue-tsc --noEmit` 0 errors. All 7 kind_robots CI
  checks green; merged squash `6de92c3`.
- Restored `prisma/generated/` to its committed state before committing — running
  `npx prisma generate` locally (via `provision_kind_robots_deps.sh`) regenerates several
  checked-in client files with sandbox-local drift unrelated to any source change (the
  same stale-generated-client artifact class documented in this project's and
  ai-art-academy's TALKBACK history); left untouched so the PR diff stayed exactly scoped
  to the seed fix.

**What was good:**
- The filing cycle (ai-art-academy/t-010) did the hard part correctly: read the actual
  source across all affected call sites rather than guessing, confirmed the schema
  constraint directly, and wrote a note precise enough that this session didn't need to
  re-investigate anything before implementing.

**What to improve:**
- None specific this cycle.

**Kaizen task:** deferred — a shared `server/utils/randomSeed.ts` helper would prevent
this exact duplicated-fallback-value bug class from recurring, but 14 near-identical call
sites is already an established pattern in this codebase (matches, e.g., the repeated
`resolveSeed`/`sleep` helper duplication across the same files) and consolidating them is
a larger refactor than this fix's scope — worth doing the next time one of these files is
touched for an unrelated reason, not as a standalone task right now.
