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
