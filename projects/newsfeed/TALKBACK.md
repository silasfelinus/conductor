# newsfeed — TALKBACK

Append-only. Never edit or delete a prior entry.

## 2026-07-18 | Worker → Reviewer | newsfeed/t-003 | pattern

**Decision:** merged (kind_robots PR #391, self-merged same session per AGENTS.md's
Worker self-merge rule for reversible/scoped/verified software work)

**Failure category:** n/a — clean first pass, no rejection.

**What was good:**
- Scope stayed tight to exactly what t-003 asked for: relocate settings off the
  homepage, don't build the real feed (that's t-006, still `waiting` on t-005).
- Found and reused the existing `/dashboard` route + `user-picture.vue` header
  link instead of inventing a new settings entry point — `content/dashboard.md`
  already rendered the identical `:user-manager` component, so zero risk of
  losing functionality.
- Caught and fixed a second-order issue the task note didn't mention: the "Home"
  channel's Dashboard nav-tab metadata (`content/channels/home/dashboard.md`,
  route `/`) still carried `dashboardKey: user` / `dashboardTab: dashboard`,
  which would have left `pageStore`'s dashboard-tab state stale/wrong once `/`
  stopped rendering that tab's content. Dropped the two fields.
- Verified with `vue-tsc --noEmit`, `eslint`, and `prettier --check` before
  opening the PR; all clean.

**What to improve:**
- Could not get a working local `nuxt dev` preview in this sandbox — both `/`
  and `/dashboard` served the stock Nuxt welcome page regardless of branch
  content (no real DB/session available here). Flagged explicitly in the PR
  rather than claiming a visual check that didn't happen. A future session with
  a real preview-deploy connector should do the visual pass CLAUDE.md asks for.

**Kaizen task:** newsfeed/t-014 — "Preview-deploy visual check of the / and
/dashboard swap from t-003" (stakes: reversible).

**Pattern note:** n/a (first task closed on this project).
