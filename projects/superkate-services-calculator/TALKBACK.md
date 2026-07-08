# TALKBACK — superkate-services-calculator

Append-only critique log. Never edit or delete entries. Format per AGENTS.md.

## 2026-07-04 | Reviewer → Worker | superkate-services-calculator/t-009 | response

**Decision:** audited already-merged work — conductor PR #176
(`worker/superkate-services-calculator-t-009-security` → `main`), self-merged by the
Worker under its reversible/scoped software authority before this review ran.

**What was good:**
- Diff is scoped exactly to the task: added a "Customer data security baseline" section to
  `SPEC.md` (data minimization, local-first storage, no analytics/telemetry, no plaintext
  secrets, receipt composer safety, deletion/export expectations, paid-app release gates)
  and nothing else — no code, no live behavior, no credentials.
- Correctly wired the new requirement into the rest of the roadmap instead of leaving it
  inert: `t-003` now `depends_on` both `t-002` and `t-009`, and `t-008`'s handoff note now
  calls out a customer data security review before app-store readiness.
- Verification claim matches reality: only `SPEC.md` and `roadmap.yaml` changed, and the
  PR body's "compared against main" check was accurate.
- Task marked `done` on the correct branch and merged cleanly — confirmed content now
  present in `main` HEAD (`SPEC.md` "Customer data security baseline" section,
  `roadmap.yaml` t-009 `status: done`).

**What to improve:** a duplicate branch, `worker/superkate-services-calculator-t-009`
(without the `-security` suffix), was pushed with the same claim commit and near-identical
diff but never turned into a PR — it's now stale/superseded dead weight sitting in the
remote. Worth deleting or at least not reusing; two branches racing the same task-id is a
process smell worth avoiding on future tasks (stick to one branch name per task-id, ideally
exactly `worker/<project>-<task-id>`).

**Kaizen task:** superkate-services-calculator/t-010 — write a pre-implementation
architecture note selecting the local storage target and app-lock approach once Superkate
approves the MVP spec (`waiting` on `t-002`; Worker's own suggestion, adopted as-is).

## 2026-07-05 | Reviewer → Worker | superkate-services-calculator/t-012 | critique

**Decision:** opened conductor PR #194 (`worker/superkate-services-calculator-t-012` →
`main`) myself, then squash-merged it — t-012 was `claimed` on `main` (per the atomic
claim-commit protocol) and its branch held the finished SPEC.md work, but no PR had ever
been opened for it. Found during a Reviewer sweep after `list_pull_requests` returned zero
open PRs in both repos.

**What was good:**
- The branch's content itself was clean and scoped: resolves the "Remaining open questions
  for Superkate" section in `SPEC.md` (receipt contact block, app-lock onboarding, paid-v1
  data lifecycle, backend direct-send deferred to future roadmap) with nothing else touched.
- Note text on `main`'s `t-002` task already correctly previewed these decisions, so the
  claim commit's task metadata was accurate — only the PR-opening step was missing.

**What to improve:**
- This is the same shape of process gap flagged on `t-009` (2026-07-04): a claimed task's
  branch sits pushed but un-PR'd. There it was a stray duplicate branch; here it's the
  canonical branch for the claimed task simply never getting a PR. Two occurrences on one
  project is a pattern, not a one-off — see kaizen task below.

**Kaizen task:** superkate-services-calculator/t-013 — open the PR in the same cycle a task
branch is pushed, before ending the Worker session, so claimed work never sits stranded
waiting for a Reviewer sweep to notice it.

**Pattern note:** Recurring across this project — `t-009`'s duplicate unopened branch
(2026-07-04) and now `t-012`'s canonical branch (2026-07-05) both reached `main` only
because a Reviewer sweep found and PR'd them, not because the Worker cycle opened the PR
itself.

## 2026-07-08 | Reviewer → Worker | superkate-services-calculator/t-005 | response

**Decision:** merged conductor PR #290 (`worker/superkate-services-calculator-t-005` → `main`,
squash) — software, reversible, scoped, completes the task.

**What was good:**
- Diff is scoped exactly to t-005: adds a `History` tab (`lib/ui/appointment_history.dart`)
  with client-name search, date-range filters (auto-clamping `from`/`to` so they can't cross),
  newest-first ordering, and result cards showing client/date/total — nothing else touched.
- Correctly reused the existing `PersistenceService.listAppointments(AppointmentFilter)`
  contract from t-003 rather than inventing a new query path; `AppointmentFilter`'s
  documented case-insensitive substring match on `clientNameSnapshot` lines up with the
  widget test that types `'kat'` and expects only `'Kate'` to match.
  in `main.dart` wired to a `DefaultTabController`/`TabBarView`, refreshing history via an
  incrementing token on save rather than a fragile manual re-fetch call — a clean pattern.
- Added widget tests for both the "saved appointment shows up in history" and "filters by
  client name" paths, plus incidentally cleaned a few stale test comments.
- Honest, well-labeled verification gap: no Flutter toolchain in the connector environment,
  which I independently confirmed is also true on the Reviewer side (`flutter` not installed
  here either) — so this isn't a Worker shortcut, it's a real environment limitation already
  tracked by t-014.

**What to improve:**
- Nothing new this cycle — template discipline, scoping, and verification-gap honesty were
  all solid.

**Kaizen task:** superkate-services-calculator/t-015 — add a CI workflow that runs
`flutter analyze`/`flutter test` for the superkate app on push, so the recurring
no-toolchain verification gap gets closed by CI instead of repeating every session (Worker's
own suggestion, adopted as-is).

**Pattern note:** The "no Flutter toolchain here" gap has now appeared on t-003, t-004, and
t-005 — always honestly disclosed, never causing an unsafe merge, but consistently unresolved.
t-015 exists specifically to break this pattern instead of letting it recur into t-006/t-007.
