# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-16T00:25:55Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **73**
- Outcomes: blocked: 1, done: 72
- Success rate: **99%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 6 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 12 | 100% |
| coloring-book | 1 | 100% |
| conductor | 11 | 100% |
| digital-storefront | 3 | 100% |
| ecosystem-map | 2 | 100% |
| global-ui | 1 | 100% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 9 | 89% |
| kindrobots-unraid | 1 | 100% |
| mermaids-of-venice | 1 | 100% |
| model-builder | 13 | 100% |
| newsfeed | 1 | 100% |
| packmaker | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 70 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 4 |
| quality | 3 |

## Kaizen targets

- failure category `actionable` — 4 occurrences; look for the shared cause across its records
- failure category `quality` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-16 `mermaids-of-venice/t-012` — Clean first-pass "Polish and upgrade X front-end surface" instance -- the humboldt-scoop/challenge-center established pattern (new top-level ExtraTutorialKey channel, not a nested tutorialChannels.<channel>.sections entry; reuse the already-approved project hero for dashboard-tab/tutorial art when no live image-gen pipeline is available) transferred cleanly. Also found a real, unrelated drift bug while touching adjacent code: conductorCards.ts's project card had stale kind/status (proposal/waiting) years behind the project's actual state (content/ready with a shipped landing page and completed editorial pipeline) -- filed conductor/t-049 to audit the rest of that file rather than assume this was a one-off.

- 2026-07-15 `ai-art-academy/t-016` — Clean first-pass kaizen task: docs-only comment addition, verified against all three real call sites before merge. Second/third instance this week of a Worker PR (kind_robots #302, conductor #579) omitting the handoff template's Stakes/Flags-for-Reviewer/Kaizen-suggestion sections entirely rather than marking them n/a -- not a rejection-worthy issue on its own, but worth a Worker-side habit fix if it keeps recurring.

- 2026-07-15 `kind-robots/t-025` — kind_robots PR #299 merged despite one failing CI check (facet-alias-smoke) after confirming via the GitHub API that the check fails on unmodified main too (a prior migration squash removed prisma/migrations/20260711021500_add_facet_aliases/ without updating the workflow that still references it) -- a red check is only a merge blocker when it's caused by the diff, not when it's independently verified pre-existing breakage. Filed t-026 to fix the workflow itself. Separately: this session's local kind_robots git checkout had desynced from true GitHub main (stale local proxy git mirror), which broke ordinary git push/rebase/cherry-pick with spurious HTTP 413s and bogus unrelated-file conflicts -- verifying file contents against the GitHub API directly and pushing via create_branch+push_files is the workaround when that symptom recurs.

- 2026-07-15 `kind-robots/t-022` — Correction to the same-day t-022 "done" record above: that closure was premature. The pool-limit-fallback fix (kind_robots PR #296) was real and deployed (confirmed limit=10 in post-deploy logs), but production stayed down -- active=0/idle=0 connections at any pool size means the database is unreachable, not undersized. Always verify a production incident fix against POST-DEPLOY live telemetry before marking it done, not just a green CI diff plus pre-merge telemetry. Reverted to needs-human/irreversible -- this remains an unresolved DB/infra reachability issue outside agent access, now spanning 4 hourly cycles.

- 2026-07-15 `kind-robots/t-022` — A production incident's stakes/scope classification can be wrong when it's written at filing time from a theory ("this looks like DB/infra") rather than a confirmed root cause. Three hourly cycles re-confirmed severity via telemetry without re-deriving root cause; the actual bug was an ordinary app-code regression (a hardcoded pool-size fallback in server/utils/prisma.ts, regressed from 10 to 2 -- same as historical fix e2caf03d), fully within normal Worker/Reviewer software-fix authority. On a recurring needs-human incident, re-examine whether the original DB-vs-app-code (or similarly scoped) classification still holds before re-flagging it a third time.

- 2026-07-15 `conductor/t-047` — A CI job's hardcoded file-list whitelist silently rots as new test files get added elsewhere in the same PR cycle (t-007's test_validate_pack_manifest.py landed weeks before this fix and was never actually run in CI). Prefer `pytest tests/` (or a directory glob) over an enumerated file list for any gating job so new tests are covered by default instead of requiring a separate task to notice and wire them in.

- 2026-07-15 `kind-robots/t-020` — All 19 remaining TypeScript errors reduced to two repeatable shapes once grouped by root cause rather than fixed file-by-file: (1) a type imported into a re-exporting module without an explicit re-export breaks any consumer that (wrongly) imports it from the re-exporter instead of the origin -- point consumers at the origin module rather than adding a re-export shim, which can create ambiguous duplicates for a framework's auto-import scanner (confirmed via a Nuxt "Duplicated imports" warning that appeared and was removed); (2) 12 of 19 errors were the same schema-vs-call-site mismatch -- Prisma fields that are String/LongText columns storing serialized JSON text, with call sites casting objects straight to Prisma.InputJsonValue instead of serializing. Diffing prisma/*.prisma against the failing call sites in one pass (rather than trusting the error message's type at face value) confirmed the schema side was correct in every case, so no schema change was needed -- just JSON.stringify/existing normalizeJson-parseStoredJson helpers at each call site. One of those fixes (commit.post.ts's stageStatuses read) was hiding a real behavioral bug behind the type error: a `typeof === 'object'` check that's always false for a string column was silently dropping prior stage statuses on every commit -- a type error is sometimes a symptom of a live correctness bug, not just an annotation to satisfy. Filed kind-robots/t-024 to guard against the InputJsonValue mismatch recurring at new call sites.

- 2026-07-15 `kind-robots/t-018` — A CI wait-step that requires an exact-SHA match is fragile against its own success: the more merges land close together, the more likely a later commit's deploy wins the race and makes an earlier commit's own wait step time out even though nothing broke. Ancestry (is TARGET_SHA reachable from the live commit?) is the right relaxation, not a longer timeout -- a longer timeout still eventually fails if merges never stop arriving, while ancestry succeeds the instant any superseding commit goes live. Kept the common exact-match path fast by only deepening the shallow checkout when the ancestry check is actually needed, and verified the new shell logic against isolated scratch git repos before ever touching live CI, since actions workflow YAML has no local unit-test harness.

- 2026-07-15 `packmaker/t-007` — A schema doc's prose "notes" column can encode a convention that contradicts the project's own worked example (SCHEMA.md said pack id should match filename; example-starter-pack.yaml intentionally doesn't). When writing a validator against a schema doc, cross-check every rule against the doc's own regression fixture before enforcing it -- don't assume prose notes are hard constraints just because they read like one.

- 2026-07-15 `packmaker/t-002` — Resolving an open design question (SPEC.md §7: dream-shaped vs character-shaped pack characters) at the per-item field level (itemShape) instead of a pack-level default kept the schema decision deferred to the actual authors (t-003) without blocking t-002 on an answer from Silas -- a reversible, self-documenting way to carry an open question forward instead of parking the task at needs-human.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-16T00:25:55Z_
