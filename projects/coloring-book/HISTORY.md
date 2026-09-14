# coloring-book — task history archive

Full `note:` prose for completed coloring-book tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-021 — Install the three-book, 36-pair proposal-ledger production model

<!-- note:begin t-021 -->
DONE 2026-07-17: added PRODUCTION-MODEL.md, ordered set catalog, ledger schema, 36-slot ledgers for Monster Recast / Hollywood Recast / Kind Robots, and scripts/coloring_proposal_status.py. Seeded known Monster Recast approvals honestly, carried the unresolved 27-file inventory snapshot forward, and integrated The Ticking Captain as mr-035. Replaced stale all-or-nothing roadmap gates with the production sequence below.
<!-- note:end t-021 -->

## t-029 — Make coloring_proposal_status.py surface elimination-only inspiration matches

<!-- note:begin t-029 -->
Kaizen from t-022 (PR #697, 2026-07-17): the mr-025 inspiration was matched to its concept "by elimination" (no direct text match), and that distinction currently only lives in a roadmap/proposals.yaml note, not in --check output. Add a --check flag or summary line listing any inspiration entries carrying needs_visual_verification: true (or an equivalent elimination-only marker) so future cycles and Silas see them surfaced automatically instead of having to read prose notes to find them.
Done (burst-mode cycle, 2026-07-17): coloring_proposal_status.py now scans every proposal's inspirations list for entries carrying needs_visual_verification: true and prints a "NEEDS VISUAL VERIFICATION (elimination-only inspiration matches)" section listing slug/proposal-id/path for each, ahead of the STRUCTURAL ERRORS block, in both plain and --strict-finals runs. Verified against the current mr-025 gothic-schoolgirl color/BW pair (both entries now show up automatically instead of needing the prose note read). No other script consumes validate_book()'s return tuple, so extending it with the new needs_verification list was a safe, local change.
<!-- note:end t-029 -->

## t-030 — kind_robots: fix ArtJob seed overflow silently killing coloring-book generation jobs

<!-- note:begin t-030 -->
DONE 2026-07-25 (claude-conductor-agentrun-20260725T140344Z-t030): clamped all 14 fallback seed-generator call sites (`server/api/comfy/**`, `server/utils/artJobRetry.ts`, `server/utils/comfyTestClient.ts`, `server/api/art/queue/[id]/edit.post.ts`) from `Math.floor(Math.random() * 1_000_000_000_000_000)` to `Math.floor(Math.random() * 2_147_483_647)`, plus added a defensive `clampArtImageSeed()` at the single Prisma write site (`server/api/art/save-generated.post.ts`). Verified: prettier/eslint clean on all touched files (pre-existing unrelated warnings on 4 files confirmed present on main too, not introduced here), full-project `vue-tsc --noEmit` (via `npm run test`) 0 errors. kind_robots PR #950, all 7 CI checks green (Contract verifiers, TypeScript, facet-catalog, verify x3, GitGuardian), merged squash `6de92c3`. Also directly reconfirmed the bug live while rechecking ai-art-academy/t-010 lane 3 the same session: job 2276 (queued ~14:08 UTC, before this fix's deploy) carries seed `25204709996469`, itself an out-of-range value that would have failed identically -- confirms the fix lands against a real, still-active failure mode, not a stale one. Impact check deferred to a future cycle (worth re-running `GET /api/art/queue/stats` once this PR's deploy is live to confirm the seed-overflow error class stops recurring project-wide, not just for coloring-book).
Filed 2026-07-25 (ai-art-academy/t-010 lane-2 roadmap-accuracy cycle, session claude-conductor-agentrun-scheduled-t010-lane2) while spot-checking the art-generation relay's health via `GET /api/art/queue/stats`. Found 17+ permanently-failed jobs (attempts: 3, projectSlug: "coloring-book") between 2026-07-25T05:23-11:27 UTC, every one with the identical error: "save-generated failed: HTTP 500 Database operation failed: Invalid prisma.artImage.update() invocation: Value out of range for the type: Out of range value for column 'seed' at row 1". Root cause confirmed via a general-purpose subagent reading kind_robots source directly (not guessed): `prisma/schema.prisma`'s `ArtImage.seed` field is a plain `Int` (32-bit MySQL INT, range +/-2147483647), but the shared fallback seed generator duplicated across the ComfyUI job builders (`server/api/comfy/kontext/utils/workflow.ts`, `server/api/comfy/flux/utils/workflow.ts`, and ~8 other call sites, plus `server/utils/artJobRetry.ts`'s `nextSeed()` at ~line 20, which regenerates the seed on every retry) all use `Math.floor(Math.random() * 1_000_000_000_000_000)` -- six orders of magnitude past the column's max, so almost every seed produced lands out of range. `server/api/art/save-generated.post.ts` (~line 166) passes `requestData.seed ?? -1` straight to the Prisma update with no clamping or validation, so the failure is deterministic: `artJobRetry.ts`'s `refreshConcreteSeeds()` regenerates a fresh (still oversized) seed on each of the 3 retry attempts, explaining why every attempt fails identically instead of eventually succeeding.
Suggested fix: clamp/mod the generated value into the signed 32-bit range at the source (e.g. `Math.floor(Math.random() * 2_147_483_647)`) in every fallback-seed generator listed above, and add a defensive clamp in `save-generated.post.ts` before the Prisma write as a second line of defense against any other future caller passing an oversized seed. Small, scoped, reversible -- not a schema change (widening the column to BigInt is a bigger, separate migration option only worth it if a legitimate use case needs seeds above 2^31, which none of the call sites currently do).
Impact: this silently kills coloring-book art-generation jobs specifically (all 17+ observed failures carried projectSlug "coloring-book") and plausibly affects any other project routing through the same ComfyUI job builders -- worth a broader grep across generated jobs once the fix lands to see if the failure rate drops project-wide, not just for coloring-book. Directly relevant to t-022 (Monster Recast production pass, currently needs-human) since a stuck seed-overflow failure could be silently eating production-pass generation attempts without an obvious surfaced cause.
<!-- note:end t-030 -->

## t-031 — Audit other art-consumption scripts for t-022's unlocked-entry duplicate-submission bug

<!-- note:begin t-031 -->
KAIZEN (from PR #1268, t-022, 2026-07-27): t-022 fixed a real bug in consume_coloring_book_color_art.py where an unlocked entry picks a fresh random seed on every enqueue() call, so a stale wait_for_job() timeout error caused the next run to blindly resubmit a duplicate ArtJob instead of recovering the original (which had often actually completed after the local poll gave up). scripts/consume_art_queue.py and scripts/consume_art_requests.py share the same wait_for_job() timeout-after-Ns-still-queued/running pattern (both call consumer.wait_for_job / a local equivalent) and were not checked for the same risk. Grep each for how it handles a wait_for_job timeout on retry, confirm whether entries are seed-locked or re-randomized on resubmission, and either port recover_timed_out_job()'s pattern if the bug reproduces, or record why it doesn't apply (e.g. already idempotency-keyed) so this doesn't need re-auditing later.


Audited both generic art consumers and added retry-stable seed derivation at their shared queue boundary, while preserving the coloring consumer's specialized timed-out-job recovery and fresh-attempt seed policy.

Completed in Conductor PR #1285, squash e2f2d3c8f59ba4a9fc11e60973e41c6b1a7c7972. Both generic consumers now rebuild retry-stable Comfy payloads after local polling timeouts, while specialized coloring attempts retain their explicit job-id recovery and fresh-seed policy.
<!-- note:end t-031 -->

## t-032 — Execute a live recovery_batch pass against the Monster Recast queue

<!-- note:begin t-032 -->
KAIZEN (from PR #1275, t-022, 2026-07-28): t-022's connector-only session added a bounded recovery_batch / recovery_actionable / recovery_actionable_count output to scripts/coloring_queue_status.py (read-only diagnostic, no ArtJobs touched) plus a --require-recovery-actionable automation guard, but could not exercise it live — this sandbox has no GitHub egress or KR_API_TOKEN in a connector-only run. No workflow or script currently consumes recovery_batch/--require-recovery-actionable yet. Next cycle with real execution access: (1) run `python scripts/coloring_queue_status.py --book monster-recast` and confirm recovery_actionable is true with a non-empty recovery_batch, (2) run the actual recovery pass (consume_coloring_book_color_art.py --live, per t-022's established recover_timed_out_job() pattern) bounded to that batch, verifying no duplicate ArtJob is submitted for an entry whose original job already completed, and (3) if useful going forward, wire `--require-recovery-actionable` into the relevant GitHub Actions workflow as a guard before an automated recovery run.
CHECKED 2026-07-28T07:12:58Z (conductor burst-mode cycle, real shell + KR_API_TOKEN present this session): ran `python scripts/coloring_queue_status.py --book monster-recast` live. Current state: recovery_candidate_count is 0 and recovery_actionable is false — none of the 18 blocked_pending/fresh_submission_blocked entries currently carry a semantic_gate_job_id, so there is no in-flight ArtJob for recover_timed_out_job() to reconcile against right now (the queue looks clean of the specific stale-timeout-behind-a-DONE-job situation t-022 fixed, not populated with fresh failures to recover). Nothing to execute against this cycle — releasing back to `ready` rather than forcing an unrelated fresh-submission `--live` run under this task's scope. Re-check after the next daily monster-recast-art-jobs.yml run (11:00 UTC) submits new entries and any of them time out; that is the next point a non-empty recovery_batch can appear. Step 3 (wiring `--require-recovery-actionable` into the workflow) stays deferred until step 2 is actually proven live, per the original kaizen note.

EXECUTED 2026-07-28T13:19Z (conductor Agent run, session claude-conductor-agentrun-20260728T131919Z-cb-t032, real shell + KR_API_TOKEN present): re-ran `coloring_queue_status.py --book monster-recast` and this time recovery_actionable is true with a 4-entry recovery_batch (mr-016 job 2751, mr-019 job 2754, mr-020 job 2755, mr-021 job 2757, all "timed out after 600s" from the 2026-07-28 10:58-11:37Z window) -- exactly the condition step 1 was waiting for.
Step 2: consume_coloring_book_color_art.py had no way to bound a --live pass to a specific set of queue_ids -- a plain --limit takes the next N pending entries in slot order, and slots 1-21 mix the 4 recoverable entries with 14 other entries already blocked_pending on a *different*, non-recoverable problem (missing ANTHROPIC_API_KEY, no job id in their error text), which the existing code would have treated as fresh submissions via enqueue(). Added `--ids` (comma-separated queue_id filter, limit ignored when set) so the recovery pass could be run bounded to exactly the 4-entry batch without touching those other 14.
Ran `consume_coloring_book_color_art.py --live --book monster-recast --ids mr-016,mr-019,mr-020,mr-021 --timeout 600`. First run surfaced a real, previously-unnoticed bug: this sandbox also has no ANTHROPIC_API_KEY, so validate_candidate() failed the same "ANTHROPIC_API_KEY is required" error recover_timed_out_job() itself doesn't call enqueue() on that path (confirmed: recovery fetched each already-DONE job's existing image via GET /api/art/queue/{id}, no new ArtJob was submitted for any of the 4) -- but the generic except-block handler still overwrote each entry's semantic_gate_error with the API-key message, erasing the "job N timed out" text a *future* recovery pass parses via referenced_job_id(). That would have converted all 4 into ordinary fresh_submission_blocked entries: a later cycle (even one with a real ANTHROPIC_API_KEY) would then see no job to recover and submit a genuine duplicate ArtJob for a render that already completed -- the exact failure mode t-022's original recover_timed_out_job() was built to prevent, reintroduced through this specific credential-missing path. Reverted the accidental mutation (`git checkout -- projects/coloring-book/color-art-jobs.yaml`, removed the 4 stray unverified webp files it produced) before it could be committed.
Fixed in scripts/consume_coloring_book_color_art.py: the per-entry loop now tracks whether the current attempt was a recovery (stuck_job_id) and, when the failure is specifically the missing-semantic-credential RuntimeError, leaves semantic_gate_error/semantic_gate_job_id untouched and logs "RECOVERY UNVERIFIED" instead of calling record_semantic_gate_error -- every other failure path (fresh-submission errors, genuinely failed/cancelled jobs, wrong-concept jobs) is unchanged. Added two regression tests: test_dry_run_with_ids_bounds_pass_to_exactly_those_entries (the --ids filter itself) and test_live_recovery_blocked_by_missing_semantic_credential_preserves_job_reference (asserts enqueue() is never called and semantic_gate_error survives byte-for-byte after a simulated missing-credential failure mid-recovery). Full local pytest suite green (699 passed, 1 skipped) both before and after.
Re-ran the same live recovery pass after the fix: all 4 entries now log "RECOVERY UNVERIFIED ... job N reference left intact ... no duplicate submitted", `git diff` on color-art-jobs.yaml is empty (the job 2751/2754/2755/2757 references are byte-for-byte unchanged), and each already-DONE render was saved and moved to generated/color-proposals-v1/rejected/semantic/unverified/ (the same convention many other mr- entries already use in that folder) pending real semantic verification.
Net result: the recovery mechanism itself is now proven live end-to-end -- no duplicate ArtJob was submitted for any of the 4 already-completed jobs, and the fix closes a real gap that would have caused duplicates on a future cycle. What remains outstanding is downstream of this task's scope: the 4 recovered images still need semantic verification with a real ANTHROPIC_API_KEY (same missing-credential limitation flagged throughout this project's notes, e.g. t-022's 2026-07-27 entry) before they can be accepted or rejected into the book -- that continues under t-022's normal production-pass scope, not this task's. Step 3 of the original kaizen note (wiring --require-recovery-actionable into a workflow) stays deferred, unchanged from the prior check-in.
<!-- note:end t-032 -->

## t-033 — Vendor-neutral print-package readiness manifest and status script

<!-- note:begin t-033 -->
conductor PR #1322 (merged) added projects/coloring-book/print-package.yaml (per-book layout/export fields, all null until Silas picks a printer), scripts/coloring_book_package_status.py (source/layout/exports readiness state machine + ordered interior manifest generation), tests/test_coloring_book_package_status.py, and a main-branch workflow that refreshes print-readiness.yaml on relevant pushes. No trim/bleed/binding/paper/printer decisions are made or assumed; nothing is published. Retroactively logged here — the PR opened from a branch outside the worker/*-claude/* claim flow with no prior roadmap task, so t-025 (Package and register Monster Recast book 1) still gates final packaging on t-022 as before. This task exists only to give the merged infra an audit trail.
<!-- note:end t-033 -->

## t-034 — Wire print-package.yaml layout fields once Silas picks a printer/trim/binding

<!-- note:begin t-034 -->
FOR SILAS: scripts/coloring_book_package_status.py (conductor PR #1322) tracks per-book print layout as explicit null fields in projects/coloring-book/print-package.yaml (trim_width_inches, trim_height_inches, bleed_inches, binding, paper, interior_color_mode, cover_color_mode, printer_template, page_count_includes_blanks, inside_cover_printing, barcode_area_reserved). TO APPROVE: pick a printer/POD vendor and fill in those fields for at least Monster Recast (order 1) — once source assets are also complete (t-022), the status script will report exports-needed with the exact next action. What unblocks: t-025 (package and register Monster Recast book 1) can then generate the ordered interior PDF, cover-wrap PDF, and source archive against real values instead of guessing a trim size.
DECIDED BY SILAS, 2026-09-11 (in session): "When it comes time for printing, we'll use amazons print services, same as I did with my novel, no future decisions about that needed." print-package.yaml's eleven null layout fields are now filled for all three books. The values were NOT invented for this decision -- they are transcribed from this project's own KDP-verified spec in docs/generation-pipeline.md section 4, checked against KDP help topics G201834340 / GVBQ3CMEQW3W2VL6, which settled on 8.5x11 no-bleed interiors long before a printer was chosen. Picking Amazon ratifies that spec rather than reopening it. Filled: 8.5x11 trim, 0 bleed (no-bleed interiors -- coloring art running off the page edge is actively worse for the user, and it avoids looser trim tolerances and the 8.625x11.25 layout), perfect-bound, white paper, bw interiors, color cover, printer_template kdp-paperback-8.5x11, page_count_includes_blanks true (KDP counts every interior page and the count drives spine width, so blanks must be real pages in the file), inside_cover_printing false (KDP does not print paperback inside covers), barcode_area_reserved true (KDP places the ISBN barcode bottom-right on the back cover). Per his 'no future decisions needed', no later task should re-ask any of this; a genuine change of printer would be a new decision, not a reopening of this one. WHAT UNBLOCKS: t-025 can package and register Monster Recast book 1 once t-022's 36 final color/BW pairs are complete.
<!-- note:end t-034 -->

## t-035 — Record a fresh submission's new ArtJob id so a missing-credential semantic-gate failure is recoverable too

<!-- note:begin t-035 -->
KAIZEN (from PR #1327, t-032, 2026-07-28): t-032 fixed consume_coloring_book_color_art.py so a *recovery* attempt (an entry whose semantic_gate_error already names a stuck job id) that fails validate_candidate() solely because ANTHROPIC_API_KEY is missing no longer overwrites that job-id reference -- a future pass with real credentials can still recover the already-completed render instead of submitting a duplicate. The 14 monster-recast entries currently in fresh_submission_blocked (mr-001, mr-005 through mr-015, mr-017, mr-018 as of 2026-07-28) have the identical underlying risk on the *other* branch of the same loop: a fresh submission calls enqueue() and waits for the new ArtJob to complete, but if validate_candidate() then fails on the same missing-credential error, the new job's id is never written into semantic_gate_error (record_semantic_gate_error() just stores str(error), which is "ANTHROPIC_API_KEY is required..." with no job id in it) -- so referenced_job_id() can never find it, and there is no way for any future pass, credentialed or not, to recover that already-rendered image; only a genuinely fresh resubmission is possible for these 14, which duplicates render-backend work for images that likely already completed. Fix: when a fresh enqueue()'s resulting validate_candidate() call fails, include the new ArtJob's id in the recorded semantic_gate_error (matching the "job N timed out" text format referenced_job_id() already parses) so it becomes recoverable via the same recover_timed_out_job() path t-032 just hardened, instead of only degrading to a fresh resubmission. Add regression coverage mirroring t-032's tests.
DONE 2026-07-28: record_semantic_gate_error() now takes an optional job_id and stamps "job N: <message>" onto the stored semantic_gate_error whenever the message doesn't already carry a "job N" reference (so a recovery-path message that already names its job, e.g. the wait_for_job() timeout text, is never double-stamped). main()'s fresh- submission branch tracks the newly enqueued job's id in a submitted_job_id variable (mirroring the existing stuck_job_id tracking for the recovery branch) and passes it through on the record_semantic_gate_error() call in the except handler. enqueue() failing outright (no ArtJob ever created, e.g. mr-018's HTTP 500) leaves submitted_job_id unset, so that case is correctly left unstamped -- only a fresh submission whose ArtJob actually completed and rendered, then failed verification, gets a recoverable reference. Added 3 regression tests: two unit tests on record_semantic_gate_error() (stamps when missing, does not double-stamp when present) and one main()-level integration test mirroring t-032's test_live_recovery_blocked_by_missing_semantic_credential_preserves_job_reference, covering the fresh-submission path instead of the recovery path. Full suite: 705 passed, 1 pre-existing failure (test_committed_ledger_schema_conformance, already tracked as hard needs-human at conductor/t-090, unrelated to this change -- confirmed unaffected with `git stash`), 1 skipped.
Reviewer merge 2026-07-28: PR #1346 merged as b23ce46. CI 24/25 green (only the known conductor/t-090 schema check red, unrelated). t-036 (the PR's kaizen suggestion) is already `ready` in this roadmap, so no new task filed.
<!-- note:end t-035 -->

## t-036 — Add a --require-no-semantic-gate-error flag to coloring_queue_status.py

<!-- note:begin t-036 -->
Added --require-no-semantic-gate-error to scripts/coloring_queue_status.py: a new credential_gate_errors/credential_gate_error_count summary field (matching the ANTHROPIC_API_KEY-is-required message, distinct from recoverable timeout / transient enqueue semantic_gate_error entries) plus the CLI guard flag. Verified against the live projects/coloring-book/color-art-jobs.yaml queue: correctly reports credential_gate_error_count 18 and exits non-zero, matching the 18 Monster Recast slots already flagged stuck on the missing ANTHROPIC_API_KEY GitHub Actions secret (see TALKBACK.md 2026-07-28 security-flag entry -- still unresolved, needs Silas to check the repo secret). Two new regression tests added; full suite green (707 passed, 1 pre-existing skip).
<!-- note:end t-036 -->

## t-037 — Migrate t-022's accumulated RAN/incident note history into a dedicated run-log doc

<!-- note:begin t-037 -->
Kaizen from PR #1416 review (2026-07-29): t-022's `note:` field has grown to
~28k characters of accumulated RAN/incident paragraphs across many recurring
cycles, the same note-bloat pattern already identified and fixed for
ai-art-academy/t-010 (see that project's t-054, filed 2026-07-29): migrate
the accumulated history into a new `projects/coloring-book/t-022-run-log.md`
(or similar), trim the roadmap note down to the current standing instruction
plus a pointer to the log, and add a line to the note telling future cycles
to append new RAN entries to the log doc instead of the roadmap note.

DONE 2026-07-29 (conductor scheduled burst cycle, session
claude-conductor-scheduled-20260729T160500Z-cb-t037): `select_role.py`'s top
`ready_task` (ai-art-academy/t-010) was already claimed by a concurrent session
by the time this cycle fetched `origin/main` fresh. Its next recommendation,
coloring-book/t-022, is itself a live production task with a real, currently
unresolved credential blocker (missing `ANTHROPIC_API_KEY` secret) and a dense
history of concurrent-session collisions on the same canonical batch -- not a
safe pick for a single unattended burst cycle. Picked the next ready,
self-contained, non-colliding task instead: this one, t-037, whose own kaizen
note already scoped exactly what to do. Created
`projects/coloring-book/t-022-run-log.md`
(header + all ~28k characters of accumulated RAN/incident paragraphs, moved
verbatim except for de-indentation -- diffed programmatically against the
removed roadmap note content byte-for-byte before commit, same verification
method t-054 used for the ai-art-academy precedent). Trimmed t-022's roadmap
note to two short paragraphs: the standing CURRENT COLOR-FIRST DIRECTION, and
a CURRENT STATE summary of the real, still-open blocker (18 Monster Recast
slots stuck on the missing `ANTHROPIC_API_KEY` GitHub Actions secret, per the
2026-07-28 TALKBACK security-flag, still unacknowledged by Silas) plus the
preserved recoverable job-id range -- both pulled forward accurately from the
note's own most recent entries, not invented. Added a `run_log:` field
pointing at the new doc, mirroring t-010's `run_log:` field exactly. Did not
touch `recurring:`, `owner:`, `claimed_by:`, or `claimed_at:`.
`python scripts/validate_roadmaps.py` and `python scripts/audit_roadmaps.py`
both clean (0 errors; same 6 pre-existing warnings, none in coloring-book).
Conductor-only change; no kind_robots PR needed.
<!-- note:end t-037 -->

## t-038 — Bake `pip install --user Pillow` into a coloring-book provisioning step so recovery cycles stop rediscovering the sandbox gap

<!-- note:begin t-038 -->
Kaizen from t-022 (conductor PR #2027, 2026-08-10). `consume_coloring_book_color_art.py`'s WebP output needs Pillow, and this sandbox's fresh containers never have it preinstalled -- every recovery-pass cycle that hits a real recovery_batch entry re-derives the same "Pillow is required for WebP output" failure and re-installs it by hand (logged at least 3 times now: 2026-07-27 through 2026-08-10, always resolved correctly by the existing except-block guard with 0 lost job references, but it's pure repeated waste). Add a small provisioning step -- either extend `scripts/provision_kind_robots_deps.sh` with a `pip install --user Pillow`, or add a coloring-book-specific one-liner doc note referencing it -- so a future cycle installs it proactively (e.g. as the first step of any `consume_coloring_book_color_art.py --live` invocation) instead of hitting the failure first. Small, reversible, no live-service impact.


Added idempotent Pillow provisioning to scripts/provision_kind_robots_deps.sh so coloring-book WebP recovery runs stop rediscovering the same missing dependency.

Merged silasfelinus/conductor#2031 as c08a349b6b4ce61a80f1a4e5c59a7463e65af222. scripts/provision_kind_robots_deps.sh now checks for PIL and installs Pillow idempotently with python -m pip install --user Pillow before coloring-book WebP recovery work. Exact PR head passed Process task events #31387694213, Security Audit #31387694254, and Worker PR CI #31387694230.
<!-- note:end t-038 -->

## t-040 — manage_coloring_book_production.py should surface the Pillow-missing fix inline instead of a bare ImportError

<!-- note:begin t-040 -->
Kaizen from t-022's kr-021..kr-030 review pass (2026-09-13, cycle 5): the
sandbox's Pillow install does not persist across sessions, so
`manage_coloring_book_production.py --operation accept-color` has now failed
on a bare "PIL unavailable -- image guard skipped" (or equivalent ImportError)
at least three separate times across three separate sessions (2026-08-11,
2026-09-13 slice 2, 2026-09-13 slice 3/this task), each time fixed the same
way (`pip3 install Pillow`) and each time flagged in TALKBACK with the same
suggested action that nobody has yet implemented: wrap the PIL import in the
script's mechanical image-guard path in a try/except that, on failure, prints
the exact fix (`pip3 install Pillow`, or a pointer to
`scripts/provision_kind_robots_deps.sh` if that's the preferred canonical
path) inline rather than relying on a session having read a TALKBACK entry
first. Scope: this script only -- do not touch the image-guard's actual
validation logic, just make the missing-dependency failure self-diagnosing.
<!-- note:end t-040 -->

## t-041 — Grep the coloring-book pipeline for other unguarded 'from PIL import Image' call sites (kaizen from t-040)

<!-- note:begin t-041 -->
Kaizen from t-040 (2026-09-13, silasfelinus/conductor#4257): that task fixed manage_coloring_book_production.py's two PIL-import call sites (mechanical_check via art_quality.assess_file, and save_image's WebP encode) to surface an actionable "pip3 install Pillow" fix instead of a bare error. Other coloring-book pipeline scripts (consume_art_requests.py, consume_monster_recast_art.py, and any other script that touches image bytes) may have the same unguarded `from PIL import Image` pattern. DO: grep the coloring-book pipeline scripts for other bare PIL imports and apply the same actionable-fix wrapping where found; if none are found, close as done with that finding noted.
Grepped every coloring-book pipeline `from PIL import Image` call site. art_quality.py::load_stats and consume_art_queue_core.py::save_result already degrade gracefully (return None / fall back to PNG with an inline actionable message) -- no fix needed there. consume_coloring_book_color_art.py::save_result and manage_coloring_book_cover.py::save_image both raised a bare RuntimeError with no fix instructions, same bug pattern as t-040 -- fixed both the same way (append pip3 install Pillow / provision_kind_robots_deps.sh guidance), added direct unit tests for each. Full python test suite (1842 passed, 1 skipped) and validate_roadmaps.py both clean.
<!-- note:end t-041 -->

## t-042 — Kaizen: make art_quality.py's load_stats() log once when Pillow is unavailable, instead of silently returning None

<!-- note:begin t-042 -->
Kaizen from t-041 (2026-09-13, silasfelinus/conductor#4264): load_stats() in art_quality.py catches ImportError on `from PIL import Image` and returns None with no side effect, which is the correct optional-dependency pattern for a library function -- but it means a missing-Pillow sandbox is only discoverable downstream, through whatever reason string the caller happens to construct from a None result (e.g. mechanical_check()'s "PIL unavailable" string, which t-040 had to special-case to add the actionable pip3 install Pillow fix). DO: have load_stats() log a single warning (once per process, e.g. via a module- level flag so a batch run doesn't spam it) the first time it hits this ImportError, so a missing-Pillow environment is obvious from the first mechanical-check failure in any coloring-book pipeline script, not just the ones that happen to string-match "PIL unavailable" in their own error handling. Do not change load_stats()'s return contract (still None on ImportError) or add a hard dependency on Pillow.
<!-- note:end t-042 -->

## t-043 — Add a spatial-autocorrelation noise/static detector to art_quality.py's color-variant gate

<!-- note:begin t-043 -->
From t-039's second, independent finding (2026-09-11): `art_quality.assess_file(path, "color")` returned ok=True with reasons=[] on a genuinely corrupted Kontext render (mean_saturation 0.2202, colorful_fraction 0.4868, white_fraction 0.0, luma_std 0.1153) because static is saturated and busy, and every existing check for the "color" variant only enforces the not-blank/not-degenerate floor. The `bw` variant's rejection of that same image was accidental (white_fraction 0.00 fails a line-art check that has nothing to do with noise).
DONE: added `hf_energy_ratio()` -- the ratio of mean squared adjacent-horizontal-pixel luma difference to total luma variance, computed directly from the sampled PIL pixel buffer (row-major, so adjacency is real, not an artifact of flat-list ordering). Real imagery has strong positive spatial autocorrelation (a pixel's luma predicts its neighbor's), so the ratio stays well below 1.0; spatially-independent noise has none, so for iid pixel values the ratio approaches 1.0 (Var(X-Y) == 2*Var(X) when X, Y are independent). `assess()` now takes an optional `hf_ratio` and rejects any variant, not just `bw`, when it clears NOISE_MIN_HF_RATIO (0.55, chosen with wide margin on both sides -- see verification below). `assess_file()`/`load_stats()` wire this through automatically; existing callers (`adopt_coloring_book_asset.py`, `consume_coloring_book_color_art.py`, `manage_coloring_book_cover.py`, `manage_coloring_book_production.py`) are unaffected since `assess_file(path, variant) -> (ok, reasons, info)` keeps its exact signature and return shape (info gains one new `hf_ratio` key). `load_stats()` has no external callers.
Verification: `art_quality.py --selftest` extended with two new pure-math checks (deterministic checkerboard noise correctly rejected, smooth gradient correctly not flagged) -- 11/11 pass. Cross-checked against real Pillow-rendered images: true iid random noise (160x120, seeded) scores hf_ratio 0.98 and is correctly rejected on the color variant; a smooth two-axis gradient scores 0.0001 and a Gaussian-blurred random texture (simulating real painterly grain) scores 0.047, neither flagged as noise. Full existing suite green: `pytest tests/ -q` -- 1851 passed, 1 skipped, 35 subtests passed (no regressions); `test_coloring_book_production.py` green in isolation (its `assess_file` monkeypatching is signature-compatible).
Kaizen for the next slice: this only guards the mechanical gate at ingest/promotion time (`assess_file` callers). It does not retroactively re-scan already-accepted color-proposal or approved/ assets for the same corruption signature -- worth a one-off audit pass across all three coloring-book sets' existing accepted color art if the Kontext corruption (t-039) turns out to have been live for a while before mr-016/mr-020 surfaced it.
<!-- note:end t-043 -->
