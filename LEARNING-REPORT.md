# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-23T12:10:47Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1133**
- Outcomes: blocked: 18, cancelled: 2, done: 1113
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 17 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 133 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 27 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-robots | 68 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 14 | 93% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 22 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 40 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1116 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 41 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 41 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-23 `ruler-hooked/t-038` — build_ruler_hooked_art_queue.py's card lane had been silently staging every request at the wrong image_path (public/images/ruler-hooked/cards/<id>.webp with a cards/ subdirectory and no card- prefix) against cardArtPath()'s actual contract (public/images/ruler-hooked/card-<id>.webp, no subdirectory) since the lane was written -- caught only by reading the consuming component (cardArt.ts) directly rather than trusting the producing script's own naming. A staging script and its consumer having independently-plausible-looking but silently mismatched path conventions is a class of bug that unit tests over the staging script alone would never catch, since it never reads the consumer; worth checking both ends of any asset-path contract when adding a new art-queue lane, not just validating the producer's own output shape.
- 2026-09-23 `animation-manager/t-020` — Pass 1's only defect was test isolation, not the feature: adding find_due_daily_commitments() to select_role.py changed live selection outcomes for the same roadmap data test_github_api_unreachable_surfaced_when_real_requests_fail asserted against, and that test didn't mock run_worker.load_roadmaps or the new finder the way its sibling test_remote_refresh_failure_does_not_crash_selection already did. Any new selection signal that reads load_roadmaps() needs every existing test exercising select_role() end-to-end re-checked for the same missing mock, not just the tests written for the new feature itself. Separately: this session's own PR-body edits tripped scripts/check_pr_handoff_template.py's required-heading check twice (dropped Kaizen suggestion, then dropped Notes for reviewer) while iterating the body by hand -- worth diffing a PR-body edit against the full AGENTS.md handoff heading list before pushing it, not just eyeballing the new content.
- 2026-09-23 `kind-robots/t-117` — Its own unit tests caught a real bug in the first pass of a route-matching regex before it shipped: a trailing-boundary check used a negative lookahead against word/slash/hyphen characters, which let quantifier backtracking land on the harmless-looking '}' that closes a template-literal interpolation and falsely accept a call to a longer, different route. A positive whitelist of real string/call terminators (excluding template-syntax characters) fixed it. Worth remembering generally: a negative-lookahead boundary check on a backtracking character class is exploitable by the regex engine's own backtracking, not just by adversarial input -- a positive whitelist of real terminators is safer whenever the preceding token is a backtracking quantifier.
- 2026-09-23 `art-archive/t-043` — Read both PRs before assuming a kaizen'd reconciliation task still needs code: kind_robots#3006 (the second of the two independent signed-capability schemes this task was filed to reconcile) already extracted the shared server/utils/signedMediaCapability.ts primitive and removed the duplicate attacher module itself, with its own added contract test (verifyArtArchiveSignedMedia.test.ts) enforcing 'one implementation, two key domains, one attacher' as part of its own green CI. The task only needed verification against live main (file listing + a code search for the removed duplicate's name) and a close-out, not a new PR -- closing tasks unread risks either duplicating work already done or missing that it's done at all.
- 2026-09-23 `animation-manager/t-019` — Creative cadence needs machine-readable release provenance at ship time: once Animation Manager dates and exact preview links were exposed in both the app and digest, a two-week build gap became immediately visible instead of hiding in prose history.
- 2026-09-23 `kind-economy/t-028` — A gap in check_project_scaffold_drift.py's sibling-check idea: nothing watches whether a server/api file that isn't reachable from any Vue page still makes sense to exist. Silas's own PR #2669 (2026-09-12) retired the mission-accrual admin page but left its backend (two API routes, a utils file, a regression test) live and orphaned for 11 days until the weekly site-audit gap-analysis pass caught it. Fix was straightforward once found: remove the four dead files, keep the Prisma model/migration in place (a destructive drop is out of scope for a reversible cleanup, AGENTS.md hard rule 10) with a schema comment explaining why. Separately: touching a schema comment still requires `prisma generate` -- the committed generated client is checked for parity against the schema, and forgetting the regen step fails CI on a diff that looks unrelated to the actual code change (verifyGeneratedClientParity flagged 4 stale files); the fix is mechanical (run prisma generate, commit the regenerated files) but easy to miss when the only edit is a comment.
- 2026-09-23 `art-archive/t-042` — A repository-wide contract verifier (verifyContentVisibilityCoverage.ts) that reads only a query's own where clause has no way to recognize authorization that happens earlier, at capability-mint time, in a different file -- the new archive media route was correctly gated by a signed capability (verifyGalleryArchiveMedia(), itself downstream of buildArtImageWhere()) but still read as unguarded. The fix was naming the specific function in the scanner's recognized-checks list, not allowlisting the route -- allowlisting would have silently exempted the whole file from future scrutiny, while naming the function keeps the scanner honest about WHY it trusts this shape. Added a regression test against the scanner's own classifier (with synthetic source, not real files) so a plain unguarded read and an unrecognized check name both still fail -- otherwise the exception itself becomes the next silent gap. Also hit the Prettier ratchet on the same PR for unrelated pre-existing formatting drift in touched files; `npx prettier --write` on the flagged files was sufficient once `npm ci`/provision_kind_robots_deps.sh was actually run locally (a stale/incomplete local node_modules previously made a bare `npx prettier` resolve a different version than CI's pinned one and produced misleading extra violations).
- 2026-09-23 `lora-ingestion/t-017` — When a helper return shape grows, update both new-path coverage and pre-existing exact-dict assertions for unchanged/no-op paths in the same patch.
- 2026-09-23 `lora-ingestion/t-016` — resync_vendored_scanner.py's --from-parity-report mode closes the last manual step in the parity-check-then-fix loop; the PR itself was correct and every code check passed on the first push. The one thing that blocked merge was the PR body using a non-AGENTS.md section layout, caught by check_pr_handoff_template.py -- editing the PR body in place (no re-implementation needed) was the right-sized fix, not a full retry cycle.
- 2026-09-23 `lora-ingestion/t-015` — Closing the last manual step t-014 left: scripts/resync_vendored_scanner.py --file <name> now does the fix half of the drift-repair loop (fetch the kind_robots original, write it over the vendored copy, append a dated PROVENANCE.md note) that check_vendored_scanner_parity.py only detects. A detector alone still leaves a human/agent to hand-run cp + hand-edit a note every time it fires -- pairing a parity checker with a one-command fixer is what actually removes the toil, not just the risk of silent drift.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-23T12:10:47Z_
