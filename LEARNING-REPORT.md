# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-18T03:31:37Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **663**
- Outcomes: blocked: 14, cancelled: 1, done: 648
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 5 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 7 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 12 | 92% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 15 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 24 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 68 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 12 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 647 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 13 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-18 `kapowarr/t-027` — A background agent pushing via the GitHub content API (create_branch/push_files) instead of git, because sandbox isolation blocks git-mutating ops against a shared checkout, works from a point-in-time file snapshot with no non-fast-forward safety net -- if a concurrent PR merges a change to a file it also touches, its push can silently revert that change. Neither isolated-copy tests nor CI caught it here (an import-only removal with no direct test coverage). Reviewing sessions merging such a PR must diff every touched file against live main, not just trust green CI.
- 2026-08-18 `kapowarr/t-026` — A protocol adapter lands cleanly when search query planning, result provenance, and queue preparation are separate seams. Preserve explicit source identity through legacy link-only task contracts rather than reintroducing source-specific branches.
- 2026-08-18 `kapowarr/t-025` — Selective architecture ports are safer than wholesale upstream copies when the fork already has working protocol-specific features; introduce seams around existing behavior, then add new protocols through the seams.
- 2026-08-18 `humboldt-scoop-cms/t-023` — The obvious in-codebase precedent (pet photos, stored as an ordinary WordPress media-library attachment) was the wrong pattern here, and the reason was architectural, not stylistic: the CMS that actually receives the field client's upload runs on a different host from WordPress with no shared filesystem, a fact only stated in a deployment-config comment (cms/ecosystem.config.cjs), not in any doc a feature-scoping read would normally reach first. Worth checking where a write physically lands (which process, which host) before reusing a same-repo pattern that looks superficially identical -- two features can both be 'upload a photo' and still need incompatible storage. Also: caught and fixed a real bug of my own before it shipped by re-deriving a timezone assumption instead of trusting it -- a first draft stamped created_at with site-local time but compared it against a UTC-computed retention cutoff, which would have silently mispurged photos by the site's configured offset on every sweep run; the fix was to pick one clock (GMT) for both the write and the comparison and say why in the code, not to patch the symptom.
- 2026-08-17 `humboldt-scoop-cms/t-030` — An open-ended 'polish' task with no obvious next action is workable by grepping the codebase itself for evidence the code already knows is stale -- two test-file comments in this repo had, weeks earlier, already called a dead theme directory 'retired' and 'a dead duplicate pending deletion', which nobody had acted on. That's a cheap, high-confidence source of scoped work: search for a project's own accumulated in-code annotations of known-stale things before treating a vague polish task as unscopable.
- 2026-08-17 `humboldt-scoop-cms/t-031` — A task note offering '<option A>, and/or <option B>' is not an invitation to build the bigger option by default -- reading the smaller/existing side first (wp-admin's own 'Scoop Solutions' menu already covered every business-management screen the note listed) turned this into a much smaller, lower-risk shared-navigation change instead of a duplicated CMS-side admin surface that would have needed to stay in sync with wp-admin's forever after. Worth checking what already exists before scoping toward the larger reading of an ambiguous task.
- 2026-08-17 `humboldt-scoop-cms/t-032` — A merge tool that only rewrites the FK column an admin-side listing joins on (customer_id) can look complete while staying broken from the customer's own portal, which keys its dashboard history queries on a redundant user_id column carried alongside customer_id on the same rows -- worth checking which column a *customer-facing* read path actually filters on, not just which one an *admin* listing joins on, before assuming one FK rewrite covers both. Also: fixed a pre-existing test (commerce-promises-test.php) that hardcoded a literal SCHEMA_VERSION string instead of version_compare, the exact anti-pattern a sibling test's own comment already named -- this task's legitimate schema bump broke it for real, a good reminder that a hardcoded-version test is a live landmine for the next unrelated schema change, not just a style nit.
- 2026-08-17 `kapowarr/t-011` — For a fork-maintenance doc, live-verifying the documented commands against the real upstream remote (adding Casvt/Kapowarr as `upstream`, fetching, running the actual `git merge-base`) caught nothing wrong here but is worth doing on principle -- a fork-maintenance doc that only describes commands in the abstract, without confirming they resolve cleanly against the actual upstream repo, risks documenting a merge-base or remote-URL assumption that silently doesn't hold. Also: this closed out both remaining m3 tasks and the milestone reconciliation left m2 and m3 with zero open tasks -- flagged in TALKBACK for a human/next-session judgment call on whether kapowarr needs a new milestone or an explicit finish decision, rather than inferring project completion from N/N per the standing caution against that.
- 2026-08-17 `humboldt-scoop-cms/t-021` — A task note that says 'the real gap is X' is a starting hypothesis, not a spec -- tracing the actual write paths (HSS_Notify's own doc comment on why it polls instead of hooking) surfaced that the new scooper-facing write needed the identical wp-cron backstop the existing completion path already has, and designing the SMS extension surfaced a real customer-mismatch bug (HSS_Sms::visit_status()'s get_by_user(0) lookup) that a shallower 'just call the existing function' implementation would have shipped silently. Also: when a schema's status enum gains a new value on one side (WordPress: 'enroute' already existed in HSS_Visits::statuses()), grep the other side's own type/enum definitions (cms/src/schema.ts's VisitStatus, db/rows.ts's VISIT_STATUSES) before assuming they already agree -- they didn't, and a real enroute row would have been silently remapped to 'scheduled' by the CMS's own fallback-on-unrecognized-value logic.
- 2026-08-17 `kapowarr/t-009` — Writing regression coverage for a module that had zero tests surfaced a real production bug that manual reading alone hadn't caught: __load_downloads()'s LinkBroken except-handler referenced a dict key ('source') that doesn't exist on the row it was handling (the actual column is 'source_type') -- on a real sqlite3.Row this raises IndexError, uncaught by the surrounding except clause, silently killing the startup queue-restore loop partway through. The bug was invisible to mypy (dict/Row __getitem__ isn't statically typed) and to every prior manual code read across t-006/t-007/t-008. Lesson for future 'add tests to an untested module' tasks: write the regression test to actually exercise the exception-handling branches (not just the happy path), and verify each new test fails without its corresponding fix before committing -- a passing-on-first-try test for a bug you just 'fixed' is not proof it would have caught the original bug.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-18T03:31:37Z_
