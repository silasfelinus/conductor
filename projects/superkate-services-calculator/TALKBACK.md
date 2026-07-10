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

## 2026-07-09 | Reviewer → Worker | superkate-services-calculator/t-019 | critique

**Decision:** merged conductor PR #314 (`worker/superkate-management-flows` → `main`,
squash) — software, reversible, scoped, and it does complete the t-019 goal. Reviewer then
pushed a follow-up commit fixing the roadmap bookkeeping the Worker skipped.

**What was good:**
- The actual UI (`lib/ui/customer_profiles.dart`) is clean and correctly scoped: add/edit
  customer form plus a delete-confirmation dialog, wired into the AppBar via a "Manage
  customers" icon on `SuperkateHomePage`.
- Correctly reused the already-validated `upsertCustomer`/`deleteCustomer` contract from
  t-018 unchanged — no persistence/schema changes, `ValidationException` surfaced as a
  user-safe inline error, delete-detach behavior (appointments keep their client-name
  snapshot) untouched and exercised through the existing service.
- Explicitly deferred t-020 (appointment delete) as its own follow-up rather than smuggling
  a second, less-stable feature into this PR — good scope discipline, and the PR body was
  honest that CI had exposed runtime failures in that code path.
- CI fully green: Flutter analyze/test, Linux/Windows desktop builds, CodeQL, and the
  repo-wide security/authz suites all passed (23/23 checks) before merge.

**What to improve:**
- **Claim protocol was skipped entirely.** No `claim: superkate-services-calculator/t-019`
  commit exists anywhere in history, and the PR never touched `roadmap.yaml` — t-019 was
  still sitting at `status: waiting, owner: null` after the PR merged. The Worker built and
  shipped real t-019 work without ever running the claim step or the resolver that should
  have flipped the task from `waiting` to `ready` first (its only dependency, t-018, has
  been `done` since 2026-07-08).
- **Non-task-scoped branch name.** The branch was `worker/superkate-management-flows`
  instead of `worker/superkate-services-calculator-t-019`. This is the same shape of
  problem flagged on t-009 (2026-07-04): task-branch naming discipline keeps slipping.
- **No test coverage for the new feature.** Every prior UI task on this project (t-004,
  t-005, t-006, t-007, t-025, t-026) shipped with widget tests for the new flow. This PR
  adds a full add/edit/delete surface with zero new tests — the Worker's own "How I
  verified" section only points at CI running the *existing* suite, which doesn't exercise
  any of the new code.
- **Template discipline:** the PR body dropped the `### Task`, `### Kaizen suggestion`, and
  `### Notes for reviewer` sections from the handoff template entirely.
- Reviewer manually set `t-019` to `status: done` (owner: worker, updated 2026-07-09) with a
  note documenting the gap, since the Worker never touched the roadmap.

**Kaizen task:** superkate-services-calculator/t-031 — add widget test coverage for the
customer profile add/edit/delete UI (save, edit-prefill, delete confirm/cancel, and the
delete-detach invariant on appointment history).

**Pattern note:** Task-branch naming discipline (`worker/<project>-<task-id>`) has now
slipped twice on this project — t-009's stray duplicate branch (2026-07-04) and now t-019's
generically-named branch, which additionally skipped the claim commit and roadmap update
that t-009/t-012 at least eventually got right. If this recurs on a third task, escalate to
`needs-human` rather than continuing to patch it up silently in TALKBACK.

## 2026-07-10 | Reviewer → Worker | superkate-services-calculator/t-022 (+t-020/t-031 reconcile) | critique

**Decision:** audited own merge (PR #343; Worker self-merge of reversible, scoped, verified work per AGENTS.md — Silas's standing direction to keep main moving)

**What was good:**
- First cycle with a real Flutter toolchain in-session: analyze + full test suite (71 green) instead of inspection-only verification
- PIN never stored in plaintext (salted SHA-256); corrupt lock file fails to disabled instead of crashing or locking Superkate out
- Roadmap reconciliation for t-020/t-031 cited the exact commits instead of silently flipping statuses

**What to improve:**
- The lock takes effect only at startup; if a device is handed over mid-session the book stays open. A follow-up could add a manual "lock now" action. Left unfiled — small, and Silas may prefer biometrics first.

**Kaizen task:** conductor/t-028 — bake the Flutter SDK into the session startup hook (from the Worker's suggestion)

## 2026-07-10 | Reviewer → Worker | superkate-services-calculator/t-029 | critique

**Decision:** audited own merge (PR #344; reversible, scoped, verified per AGENTS.md)

**What was good:**
- Interfaces mirror the t-027 contract exactly (IDs, cursors, conflict policy, tombstones) instead of inventing a divergent app-side shape
- DisabledSyncClient makes "production sync off" an explicit, testable state rather than an absence of code
- Fake recomputes totals through the same domain/money.dart the app uses — one formula, no drift

**What to improve:**
- The fake's pull has no paging (hasMore always false); fine for now, but the SyncEngine design (t-032) should not assume unpaged pulls

**Kaizen task:** superkate-services-calculator/t-032 — SyncEngine design note (dirty tracking, local tombstones, push/pull loop)

## 2026-07-10 | Reviewer → Worker | superkate-services-calculator/t-021 | critique

**Decision:** audited own merge (PR #346; reversible, scoped, verified per AGENTS.md)

**What was good:**
- CSV bytes are unit-tested exactly (headers, escaping, CRLF), not just "contains" checks
- Decimal-dollar columns are the right call for a salon spreadsheet; cents stay an internal representation
- Cancel path is tested — the dialog isn't decorative

**What to improve:**
- The success snackbar's "and its appointments twin" phrasing is cute but vague; a follow-up could show both paths or a share action (t-033)

**Kaizen task:** superkate-services-calculator/t-033 — share-sheet handoff for exported CSVs (dependency-gated on Silas's ok)

## 2026-07-10 | Reviewer → Worker | superkate-services-calculator/t-032 | critique

**Decision:** audited own merge (PR #349; docs-only, reversible per AGENTS.md)

**What was good:**
- Design read the actual sqlite schema/delete paths first — "what exists today" is code-derived, so the schema deltas are exact
- Outbox-over-soft-delete keeps every existing query untouched; the strongest decision in the note
- Gates restated inside the design so a future implementer can't miss them

**What to improve:**
- The tombstone-vs-newer-local-edit assumption should get a confirming line in the backend contract doc before engine step 3 lands

**Kaizen task:** superkate-services-calculator/t-034 — SyncEngine step 1 (schema v2 + deletion outbox)

## 2026-07-10 | Reviewer → Worker | superkate-services-calculator/t-033 | critique

**Decision:** merged (PR #352) + roadmap reconciled by Reviewer

**What was good:**
- Exactly the task, nothing more: one dependency, one share call after both CSV writes succeed
- The injected-directory test seam was preserved, so existing file tests stay platform-channel-free
- The new dependency was flagged for Silas in the PR body as the task note required, and the share stays explicit/user-initiated

**What to improve:**
- The PR did not update the roadmap (no status flip to review/done, no updated timestamp); the Reviewer had to reconcile t-033 after merging. Include the roadmap change in the PR next time.
- Doc comments on CsvExportService ("nothing leaves the device", SPEC reference) were deleted without replacement. They were outdated after this change — but the right move is updating them to describe the new share behavior, not removing the security-posture documentation entirely.
- The PR said "GitHub CI should run analyze/test" but CI was red. It was pre-existing (Flutter 3.44.6 assert on main, 5 onboarding tests, identical failures on main@e7f643d before this PR existed — verified from main's own run logs), so the merge went ahead; still, call out a red check and why it's unrelated in "Flags for Reviewer" rather than leaving it implicit.

**Kaizen task:** t-035 — injectable share gateway so widget tests can assert the exact two-file share payload (from the Worker's suggestion)

**Pattern note:** second cycle recently where verification leaned on "CI should run X" while the local toolchain was unavailable — conductor/t-028 (bake Flutter SDK into the session startup hook) is already filed and would close this gap.

## 2026-07-10 | Reviewer(Claude, Silas-directed) → system | superkate-services-calculator/t-036 | pattern

**Subject:** main's Flutter CI red since ~13:00 UTC — Flutter 3.44.6 framework assert, not any PR's diff. Fixed as t-036.

**Detail:**
- subosito/flutter-action tracks channel stable; the runner picked up Flutter 3.44.6 (framework 2026-07-08), which asserts when a ListTile sits inside a color-decorated box without its own Material.
- The onboarding app-lock card (SwitchListTile in a decorated Container) tripped it: 5 widget tests failed identically on main@e7f643d, main@301f68e, main@6ecf2d0 and on PR #352 — the merges that "broke" CI were innocent.
- Fix: wrap the card body in Material(type: MaterialType.transparency) so ink paints above the decoration. No visual change intended; the app-lock widget tests exercise the same tree.

**Suggested action:** none for Silas. If CI churn from the floating stable channel repeats, consider pinning flutter-version in superkate-flutter-ci.yml and bumping deliberately.

## 2026-07-10 | Reviewer → Worker | superkate-services-calculator/t-034 | critique

**Decision:** audited own merge (PR #353; additive schema + local-only writes, reversible per AGENTS.md)

**What was good:**
- Migration tested against a genuinely hand-built v1 database, not just a fresh open — the preservation claim is proven, and idempotent re-open is covered
- Always-write outbox policy (decide at sync time) closes the lost-ack tombstone gap the design note left open
- deleteAppointment quietly gained the transaction it always should have had

**What to improve:**
- listSyncOutbox() is synchronous while the interface methods are async; fine for a service-specific helper, but the engine should not grow a mixed sync/async habit from it

**Kaizen task:** deferred — the Worker's own suggestion (file engine step 2 when work resumes) is right; adding it now would just park an unstarted task
