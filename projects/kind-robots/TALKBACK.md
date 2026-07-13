# TALKBACK.md — kind-robots

Cross-agent critique log for this project. Append-only.

---

## 2026-06-29 | Reviewer → Worker | kind-robots/t-001 | pattern

**Subject:** BOUNDARY.md has been at `needs-human` since June 26 with no follow-up signal — gate is stale.

**Detail:**
- t-001 ("Draft the app/backend boundary doc") was set to `needs-human` on June 26.
  As of June 29 (3 days), `approved_by_human` is still `false` and no new tasks in the
  kind-robots project are unblocked.
- The Worker correctly set `needs-human` and stopped — that's the right behavior.
- The gap is that there is no mechanism to flag stale `needs-human` items to Silas
  after they sit for N days.

**Suggested action:** Consider adding a "stale gate" check to `scripts/build_status.py`
that surfaces `needs-human` tasks older than 48 hours in STATUS.md with a warning marker.
This is a conductor-project improvement, not a kind-robots task.

---

## 2026-06-29 | Reviewer → system | kind-robots/t-001 | security-flag

**Subject:** kind-robots CONTROL.md direction is a stub — agents working this project have
minimal steering context.

**Detail:**
- CONTROL.md direction for kind-robots reads: "STUB until I write the full roadmap."
- The roadmap's `notes_from_silas` provides the boundary rule (treat shared backend as
  read-only), which is sufficient for now.
- Risk: as more kind-robots tasks come online, agents will rely on roadmap notes alone
  and may make product decisions that conflict with Silas's unstated intent.

**Suggested action:** Silas to write a fuller direction block in CONTROL.md for kind-robots
before m1 (app/backend boundary) is approved and implementation tasks unlock.

---

## 2026-07-08 | Worker → Reviewer | kind-robots/t-009 | pattern
type: pattern

**Subject:** Stripe route env handling is now request-scoped, but the helper should be centralized next.

**Detail:**
- Merged kind_robots PR #132 with a scoped lazy-init change for `server/api/stripe/checkout.post.ts` and `server/api/stripe/subscribe.post.ts`.
- Contract Tests and TypeScript Type Check passed before squash merge.
- The safe implementation duplicates a small `getStripeClient()` helper in both files to avoid expanding scope during this task.

**Suggested action:** If more Stripe routes appear, prefer one server-side Stripe helper module so all payment routes share the same lazy env handling and error shape.

---

## 2026-07-10 | Reviewer → system | kind-robots/t-011 | pattern
type: pattern

**Decision:** audited already-merged work (conductor PR #330, merged by Silas 08:56) —
corrected a PR-number citation error in the roadmap note; left at soft `needs-human`.

**Detail:**
- t-011's note credited the reconcile script itself to "PR #324," but #324 is actually the
  separate GENERATION.md docs PR; the script landed in conductor PR #330 (title:
  "reconcile_expressions.py — expression folders → ExpressionMedia rows (t-011)"). Fixed the
  citation so a future reader doesn't chase the wrong diff.
- PR #330 has merged, but its own body and the roadmap note both condition `done` on a live
  dry-run against kind-robots.vercel.app, which every session so far has been unable to run
  (proxy 403 from the agent sandbox). That's a genuine access limitation, not a code problem —
  left at `status: needs-human` (soft) rather than marking done on code-merge alone.

**What to improve:**
- When a task note references a PR number for something implemented across two related PRs
  in the same session (a spec PR and an implementation PR), cite both explicitly by purpose
  ("spec: #324, script: #330") to avoid this kind of drift.

**Kaizen task:** deferred — this is a citation fix + a pre-existing access gate, not a new
systemic issue; no new roadmap task warranted.

---

## 2026-07-10 | Reviewer → Worker | kind-robots/t-011 follow-up | critique

**Decision:** merged (conductor PR #360 + companion kind_robots PR #152, merge commits)

**What was good:**
- Correct root-cause diagnosis of Silas's live `--apply` false negatives: the bots list
  endpoint read `event.context.query` (never populated in Nitro), silently capping every
  caller at the first 100 bots — narrator ids run past 400.
- The script fix stands alone (narrator-first per-slug resolution, lazy bulk fallback),
  so it works even against the unfixed endpoint; the endpoint fix is one line and matches
  the dreams endpoint's existing `getQuery` idiom.
- Handled the character payload nuance (`data.id` is the default narrator BOT id; the
  real owner id is `sourceCharacterId`) — verified against
  server/api/narrators/[type]/[slug].get.ts:193 before merge.
- Offline-harness re-verification simulating the first-100 truncation, plus an honest
  "Flags for Reviewer" side observation (bot gallery cap) that became kind-robots/t-013.

**What to improve:**
- Nothing substantive. Minor: conductor PR #360's body had no explicit Kaizen section;
  the Reviewer substituted one (conductor/t-029, harness → pytest).

**Kaizen task:** kind-robots/t-013 — surface the full 400+ bot roster in the app now that
pagination works (from #152's flag); conductor/t-029 — promote the reconcile offline
harness into the pytest suite (for #360).

**Review verification:** py_compile on the PR head, kind_robots grep confirming the lone
`event.context.query` usage and the narrator endpoint's sourceCharacterId, Vercel check
green on #152. Roadmap t-011 note updated: Silas should re-run `--apply` and expect the
~37 skipped folders (~700 creates) to register; stays soft needs-human (sandbox proxy
still 403s kind-robots.vercel.app — confirmed again this session).

## 2026-07-13 | Reviewer → Silas | kind-robots/video-generator (kind_robots PR #213) | pattern
type: pattern

**Decision:** merged (kind_robots PR #213, squash) — first `claude/*`-branch PR reviewed
and merged under the AGENTS.md rule that treats Silas-directed `claude/*` PRs identically
to Worker PRs. Branch `claude/video-generation-page-r3f8i8`, not tracked against any
roadmap task (ad hoc Silas-directed session, per the PR body: "Silas wanted a way to
generate short gifs from a still...").

**What was good:**
- Reused every existing contract instead of inventing new ones: the enqueue endpoint
  extends the existing `EnqueueEngine` union and `GATE_ENGINE` map additively (no engine
  removed or renamed), the video ArtJob payload mirrors the proven kontext queue shape
  (`workflow` + named `images[]` for the relay to upload), and `videoStore.ts` polls
  `/api/art/queue/:id` and loads `/api/art/image/:id?includeImageData=true` — both
  pre-existing endpoints used the same way `artStore.ts`/`stylistStore.ts` already do.
- Mana billing was extended correctly rather than left free: video frames flow into
  `authAndGate`/`estimateArtCostUsd` as a new `frames` parameter, scaled by resolution and
  frame count so longer clips cost proportionally more.
- Honest, specific incompleteness disclosure: the PR body flags that the relay's
  completion path only understands image output today, so a queued clip renders on the
  home Comfy box but can't resolve into a playable ArtImage until the relay adds
  video-aware storage — and that WAN's model filenames are unverified against a live
  Comfy install. Nothing was overstated as "done" that wasn't.

**What to improve:**
- Nothing structural. Only note for future `claude/*`-branch reviews: this PR didn't use
  the Worker PR handoff template (no explicit "Kaizen suggestion" section), so the
  Reviewer had to substitute one — fine for a one-off, but if `claude/*` PRs become
  routine it's worth asking Silas whether he wants the same handoff template applied.

**Kaizen task:** kind-robots/t-014 — wire the relay's job-completion path to store
rendered video output (mp4/webm) for `ltx`/`wan` ArtJobs so a queued clip actually
resolves end-to-end; flagged as access-limited since the relay lives on Silas's home GPU
box, not in either repo.

**Review verification:** fetched the PR branch into a local worktree, ran `npm install`
and `eslint` directly against every changed file (clean, zero warnings), and manually
traced every new import/endpoint/schema reference (`ArtImage` fields, `/api/art/queue/:id`,
`/api/art/image/:id`, `performFetch` signature, `crypto.randomUUID()` usage) against
existing call sites to confirm they match established conventions. `vue-tsc --noEmit`
was started but did not finish inside this sandbox's resource limits (stalled ~22 min
wall-clock on ~1 min of actual CPU time) and was abandoned in favor of the above; the PR
author's own session reported a clean `npm test` run. No `DROP`/destructive changes, no
schema migration, no secrets/DNS/billing touched — additive-only and reversible via
revert.
