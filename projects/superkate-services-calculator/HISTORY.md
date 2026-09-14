# superkate-services-calculator — task history archive

Full `note:` prose for completed superkate-services-calculator tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-003 — Build the appointment and customer data model with persistence

<!-- note:begin t-003 -->
Implemented in apps/superkate-services-calculator/ (Silas-directed session 2026-07-07). The prior handoff wrongly parked this as "cannot locate the app repository" — the Flutter app is in-repo at apps/superkate-services-calculator/, so the domain + persistence layer was built directly there against the SPEC.md data model: domain money/validation/ids, customer and appointment models, PersistenceService, in-memory persistence, and unit tests for totals, product-cost defaults, recomputation, validation, customer-delete snapshots, and search filters. Money is cents, time is minutes, totals are always recalculated, customer delete detaches rather than cascades. Verification gap from that run was later cleared by t-014.
<!-- note:end t-003 -->

## t-004 — Build calculator form with live totals

<!-- note:begin t-004 -->
DONE (2026-07-07, Silas-directed session): built lib/ui/new_appointment_form.dart — client name, appointment date picker, hourly rate, time spent with steppers and preset chips, optional product cost defaulting to $0, live appointment total recomputed through the t-003 domain layer, save through PersistenceService, user-safe errors, main.dart wiring, widget tests, and money parser tests. Verification gap from that run was later cleared by t-014.
<!-- note:end t-004 -->

## t-005 — Add client/date appointment search

<!-- note:begin t-005 -->
DONE (2026-07-08, Reviewer-merged conductor PR #290). Implemented a History tab in apps/superkate-services-calculator/ with client-name search, date-range filter controls, newest-first appointment results, and cards showing client, date, and appointment total. Uses the existing PersistenceService.listAppointments(AppointmentFilter) contract unchanged. Added widget coverage for saved appointments appearing in history and client-name filtering.
<!-- note:end t-005 -->

## t-006 — Add warm receipt email composer

<!-- note:begin t-006 -->
DONE (2026-07-08, PR #295): added a local, user-reviewed receipt email composer for saved appointments. History cards now expose Prepare receipt, which builds a mailto draft with saved customer email when available, client name, appointment date, hourly rate, time spent, product cost, total price, the formula line, and "Superkate loves you!". The implementation uses Android/iOS platform mail composer handoff plus a local copyable fallback dialog; it does not send backend email, add analytics, or call external customer-data services.
<!-- note:end t-006 -->

## t-007 — Polish the dark purple/teal salon UI

<!-- note:begin t-007 -->
DONE (2026-07-08): polished the Superkate Flutter UI with a richer dark purple/teal theme, gradient app shell, centered mobile/tablet-friendly content width, salon-styled cards for the appointment form, clearer touch targets, more professional history result cards with rate/time/product details, and a cleaner receipt fallback dialog. No persistence, analytics, backend email sending, or customer-data flow changed.
<!-- note:end t-007 -->

## t-008 — Prepare handoff checklist without store submission

<!-- note:begin t-008 -->
Silas approved the handoff gate in-session on 2026-07-08 and supplied the current release decisions: first app target is Android, receipt/contact schedule link is https://hairbysuperkate.glossgenius.com/, reply-to contact is hairbysuperkate@gmail.com, and cloud sync ownership is now a dedicated Hair by Superkate backend. The checklist remains the safety reference: do not use real customer records until durable persistence lands, and do not submit to stores, publish, bill, deploy, or send backend email without explicit concrete approval.
<!-- note:end t-008 -->

## t-014 — Run flutter create to complete platform scaffolding and run the test suite

<!-- note:begin t-014 -->
DONE (2026-07-08): PR #293 scaffolded apps/superkate-services-calculator with .metadata, android/, and ios/ after running Flutter locally on Windows. The merged PR reported successful verification with D:\dev\flutter\bin\flutter.bat pub get, D:\dev\flutter\bin\flutter.bat analyze --fatal-infos, and D:\dev\flutter\bin\flutter.bat test. Main now includes the platform metadata and generated Android/iOS project files, so the toolchain/scaffolding blocker is cleared.
<!-- note:end t-014 -->

## t-015 — Add a CI workflow that runs flutter analyze/test for superkate on push

<!-- note:begin t-015 -->
DONE (2026-07-08, PR #298): added .github/workflows/superkate-flutter-ci.yml, scoped to pull_request and push events that touch apps/superkate-services-calculator/** or the workflow file itself. The workflow installs stable Flutter with cache, runs flutter pub get, flutter analyze --fatal-infos, and flutter test from apps/superkate-services-calculator/. Merged to main with no deploy, secrets, publishing, customer data, DNS, billing, or app-store behavior touched.
<!-- note:end t-015 -->

## t-016 — Add rainbow, queer-alt Superkate visual styling pass

<!-- note:begin t-016 -->
DONE (2026-07-08, PR #300): merged the style-only Flutter pass inspired by Silas's direction that Superkate is a queer/genderqueer alternative barber focused on rainbow hair, gender-affirming cuts, wild designs, and spunk. The pass adds shared rainbow style tokens, updates the app shell, appointment form, history cards, and fallback receipt dialog with stronger rainbow gradients/glow/copy while preserving tested labels and customer-data behavior. No persistence, sync, analytics, backend email, billing, deploy, or app-store behavior is touched.
<!-- note:end t-016 -->

## t-017 — Add desktop Flutter target CI coverage

<!-- note:begin t-017 -->
DONE (2026-07-08, PR #303): merged Windows and Linux debug desktop build checks into the Superkate Flutter CI and documented local desktop build commands in the app README. This treats desktop scaffolding as first-class install coverage while keeping the normal analyze/test job intact. The change was scoped to CI/docs plus an analyzer-friendly Flutter alpha API update; it did not change persistence, sync, customer-data behavior, backend email, deploy, billing, secrets, DNS, app-store behavior, or analytics.
<!-- note:end t-017 -->

## t-018 — Add durable local SQLite persistence adapter

<!-- note:begin t-018 -->
DONE (2026-07-08, PR #306): merged a local SQLite-backed PersistenceService adapter in apps/superkate-services-calculator, wired production startup to open the durable local database by default, and added app-level persistence injection so widget tests do not hit platform SQLite startup. Superkate Flutter analyze/test and Linux desktop build passed in CI; Windows desktop build reached a successful build step before post-action cleanup. No cloud sync, analytics, backend email, app-store, billing, deploy, secrets, or live customer-data service was added.
<!-- note:end t-018 -->

## t-019 — Add customer profile edit and delete UI

<!-- note:begin t-019 -->
DONE (2026-07-09, Reviewer-merged conductor PR #314, squash). Adds a "Manage customers" AppBar sheet (lib/ui/customer_profiles.dart) for add/edit/delete of local customer profiles, reusing the validated upsertCustomer/deleteCustomer contract from t-018 unchanged; delete detaches appointments rather than cascading, per spec. CI (Flutter analyze/test, Linux/Windows desktop builds, security scans) all green. Reviewer fixed up this roadmap entry and the claim bookkeeping after merge: the Worker branch (worker/superkate-management-flows) never ran the claim step, never touched this roadmap file, and used a non-task-scoped branch name instead of worker/superkate-services-calculator-t-019. No widget tests were added for the new add/edit/delete flow itself — see TALKBACK for the coverage gap and t-031 kaizen task.
<!-- note:end t-019 -->

## t-022 — Add app/device lock onboarding and settings toggle

<!-- note:begin t-022 -->
Done 2026-07-10 (hourly Worker, PR from claude/hourly-conductor-worker-wcv547): optional PIN app lock — onboarding step (switch + PIN confirm), startup lock screen, and an app-bar settings sheet (turn on/off, change PIN; current PIN required to disable or change). PIN stored as salted SHA-256 only, never plaintext; local-only. Placeholder warm copy is editable. Verified: flutter analyze clean, 71 tests pass including 7 new lock widget tests and file/in-memory service tests.
<!-- note:end t-022 -->

## t-023 — Draft cloud sync ownership and self-hosted backend decision note

<!-- note:begin t-023 -->
DONE (2026-07-08, PR #307, later amended by Silas decision): added projects/superkate-services-calculator/docs/cloud-sync-ownership-decision.md and recorded the final direction that cloud sync/auth should be owned by a dedicated Hair by Superkate backend. Immediate Android beta remains local-only until durable persistence, export, app-lock, and fake-data backend sync are safe. No production sync, secrets, deploy, DNS, billing, analytics, backend email, or app-store behavior was implemented.
<!-- note:end t-023 -->

## t-024 — Add Android-first beta install notes

<!-- note:begin t-024 -->
DONE (2026-07-08, PR #310): added projects/superkate-services-calculator/docs/android-first-beta-install.md and linked it from the app README. The doc covers Android debug build/install commands, USB device install flow, fake-data-only beta warnings, a local device smoke test checklist, and explicit blockers before wider beta/store distribution. No release signing, app-store listing, production backend, real customer data, DNS, secrets, billing, analytics, or backend email sending was added.
<!-- note:end t-024 -->

## t-026 — Add independent background pattern selector

<!-- note:begin t-026 -->
DONE (2026-07-09, PR #312): added an independent background selector with Circles, Hearts, Grid, and None options. Theme changes no longer force the decorative background pattern, and background changes do not alter the theme. Added widget coverage for theme/background independence. Security Audit, Worker PR CI, app-ci, and Superkate Flutter CI all passed before squash merge. No persistence, customer-data schema, backend sync, live endpoint, direct-send email, analytics, production deploy, secrets, DNS, billing, or app-store behavior changed.
<!-- note:end t-026 -->

## t-027 — Define dedicated Hair by Superkate backend API and schema contract

<!-- note:begin t-027 -->
DONE (2026-07-08, PR #308): added projects/superkate-services-calculator/docs/backend-api-schema-contract.md defining the dedicated Hair by Superkate backend contract: customer and appointment schema, owner/business scoping, local-to-server ID mapping, sync tombstones, validation rules for money/time/dates, fake-data endpoints, and t-028 scaffold guidance. No secrets, DNS, deploy settings, production database connections, direct-send email, analytics, billing, app-store behavior, or public admin surfaces were created.
<!-- note:end t-027 -->

## t-028 — Scaffold dedicated Hair by Superkate backend locally without deploy or secrets

<!-- note:begin t-028 -->
DONE (2026-07-08, PR #309): merged the fake/local-only Hair by Superkate backend scaffold in apps/hairbysuperkate-backend/ with health, bootstrap, push, pull, reset-test-data, fake auth, in-memory store, validation, models, and unittest coverage. The same PR also fixed the repo Security Audit workflow so pull requests scan changed lockfiles/files while scheduled/manual runs retain repo-wide coverage. No secrets, DNS, deploy settings, production DB connections, real customer sync, analytics, billing, backend email sending, or app-store behavior was added.
<!-- note:end t-028 -->

## t-030 — Plan dedicated backend deployment, secrets, and backup gates

<!-- note:begin t-030 -->
DECIDED 2026-07-26 (Silas): no dedicated Hair by Superkate backend for now — the app keeps using the existing kind_robots infra/fake-local backend scaffold as-is. Only Superkate herself uses this app; a dedicated deployment, secrets, and backup plan isn't worth building until usage grows beyond her. Revisit this gate if/when someone besides Superkate starts using it. No production sync, secrets, DNS, or real customer data handling is authorized by this decision — that still needs its own future gate if this ever gets revisited.
<!-- note:end t-030 -->

## t-032 — Write the SyncEngine design note (dirty tracking, local tombstones, push/pull loop)

<!-- note:begin t-032 -->
Kaizen from t-029 (PR #344): the sync client interfaces and fake exist, but nothing defines how the app tracks dirty records, when local deletions become tombstone records, or how the push/pull loop drives SyncStatus for the UI. Write docs/sync-engine-design.md mapping PersistenceService records to the wire records in lib/sync/, including offline behavior and retry policy. Design note only — still no live endpoint or production sync.
<!-- note:end t-032 -->

## t-033 — Share-sheet handoff for exported CSVs (share_plus) pending dependency approval

<!-- note:begin t-033 -->
Done via PR #352 (Reviewer-merged 2026-07-10): share_plus ^11.0.0 added and production exports open the platform share sheet after both CSV writes; the injected-directory test path stays share-free. FOR SILAS: the new dependency is share_plus (standard Flutter Community Plus package, local share sheet only, nothing uploads) — veto by reverting PR #352 if unwanted. The Worker did not flip this status in the PR; Reviewer reconciled it here.
<!-- note:end t-033 -->

## t-034 — SyncEngine step 1: schema v2 migration (server_id/synced_at columns) + deletion outbox writes

<!-- note:begin t-034 -->
Kaizen from t-032 (PR #349), implementing step 1 of docs/sync-engine-design.md: bump sqlite userVersion to 2 adding customers.synced_at, customers.server_id, appointments.server_id, the sync_outbox table, and the one-row sync_state table; write outbox rows inside the existing deleteCustomer/deleteAppointment transactions. Pure local storage work, no network, tested against the existing sqlite test setup (migration from a v1 database included).
<!-- note:end t-034 -->

## t-036 — Fix Flutter 3.44 ListTile-in-DecoratedBox assert breaking 5 onboarding widget tests

<!-- note:begin t-036 -->
CI's stable Flutter channel moved to 3.44.6 (2026-07-08), which added a framework assert: a ListTile inside a color-decorated box without its own Material paints its ink under the decoration. The onboarding app lock card (SwitchListTile in a decorated Container in superkate_onboarding.dart) tripped it, failing 5 widget tests on main since ~13:00 UTC 2026-07-10 — unrelated to the PRs that surfaced it. Fixed by wrapping the card body in Material(type: transparency). Completed in this session's conductor PR.
<!-- note:end t-036 -->

## t-037 — test/csv_export_widget_test.dart: "export flow shares exactly the two written CSV paths" hangs until the 10-minute test timeout in CI

<!-- note:begin t-037 -->
Found 2026-07-21 (conductor burst-mode session working sketchy/t-008, conductor PR #994): app-ci.yml's "Analyze and test each app" step runs every app in apps/ in one shared job (falls back to `ls apps` whenever the changed-app diff detection doesn't isolate to a single app -- this run touched only apps/sketchy but still executed the full apps/ list, superkate-services-calculator included). This test ("export flow shares exactly the two written CSV paths", added by t-035/PR #365) hung with `TimeoutException after 0:10:00.000000: Test timed out after 10 minutes` at `dart:isolate _RawReceivePort._handleMessage`, failing the shared job and blocking an otherwise fully green, unrelated PR (sketchy/t-008 -- see run https://github.com/silasfelinus/conductor/actions/runs/29865852390/job/88753749403). The other two tests in the same file (the InMemoryCsvExportService-backed flow and the cancel-dialog flow) passed fine; only the FileCsvExportService + real temp-directory + InMemoryCsvShareGateway variant hangs. Likely culprit: something in FileCsvExportService's real file-write path (or a timer/animation it triggers) never settles, so `tester.pumpAndSettle()` (or an awaited Future) blocks forever instead of throwing promptly -- worth checking whether FileCsvExportService's share step touches a real plugin channel despite the injected fake gateway, or whether a SnackBar/ animation controller from the confirm dialog is the one not settling. Reproduce locally with `flutter test test/csv_export_widget_test.dart` (fast on a real machine if it's CI-environment-specific hardware/headless timing, but likely reproduces anywhere if it's a genuine unsettled Future/Timer). Separately worth a conductor-side follow-up: app-ci.yml testing every app in one job means one hung/flaky test in any single app can block PRs for every other unrelated app -- consider per-app job matrix (isolated failure blast radius) or at minimum a per-app timeout shorter than the shared job's overall runtime budget so one hang doesn't silently eat ~10 minutes of CI on someone else's PR.

FIXED 2026-07-21 (conductor burst-mode session, ~21:07 UTC): reproduced locally by provisioning Flutter fresh and running `flutter test test/csv_export_widget_test.dart` -- hangs indefinitely, same as CI. Bisected with a minimal standalone widget test: a bare `await Directory.systemTemp.createTemp(...)` inside a `testWidgets` body hangs forever in this environment when called directly, but succeeds immediately when wrapped in `tester.runAsync()`. Root cause: testWidgets bodies run inside flutter_test's FakeAsync zone (for animation/timer control), and in this environment genuine dart:io async completions (temp-dir creation, file writes) never get drained by that zone's pump()/pumpAndSettle() -- they need the real zone tester.runAsync() provides. It is not merely a timing race: an unwrapped real dart:io call hangs 100% of the time, not intermittently. Fix applied to csv_export_widget_test.dart: (1) create the temp `Directory` inside `tester.runAsync()` instead of a bare `await`; (2) drive the confirm-export tap itself (whose onPressed chain triggers FileCsvExportService's real file writes) from inside a `runAsync` block too, polling `tester.pump()` + a short real delay until `shareGateway.shareCount` increments (capped at 500 x 10ms attempts so a future regression fails the assertion instead of reintroducing a silent hang); (3) the `addTearDown` directory cleanup also now runs through `runAsync`. Verified: `flutter test test/csv_export_widget_test.dart` (3/3 passing, ~2s), full `flutter test` for the app (98/98 passing), `flutter analyze --fatal-infos` (0 issues), `dart format` (already formatted). The separate shared-CI-job blast-radius question from the note above is left as a conductor-side follow-up, not part of this fix.
<!-- note:end t-037 -->
