# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-29T13:37:20Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **822**
- Outcomes: blocked: 16, cancelled: 1, done: 805
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 25 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 87 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 40 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 86 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 53 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 9 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 6 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 806 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 12 |
| transient | 11 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-29 `rainbow-butterflies/t-012` — Once one of DESIGN-BRIEF.md's five 'fundraising experiments worth testing' has already been picked for the calendar (Butterfly bounties, t-008/CONTENT-CALENDAR.md), a sibling task asking to 'prepare' a different named experiment (t-012, Why I donated + skeptics build too) should be scoped as a second ready-to-launch alternative, not a competing Week-6 proposal -- state the relationship explicitly rather than silently overwriting the calendar's existing recommendation.
- 2026-08-29 `rainbow-butterflies/t-001` — When a task literally asks for a 'matrix' but the requested content already exists as prose scattered across multiple files, the real gap is often structural (consolidate into one table) rather than missing research -- check what already exists before assuming a from-scratch rewrite is needed.
- 2026-08-29 `rainbow-butterflies/t-008` — Another clean first-pass success, same session as t-007: DESIGN-BRIEF.md already contained a "six-week first release cadence" section with phases, seven content pillars, and a publishing ratio -- reading the existing brief in full before writing turned this into "make the existing plan concrete" rather than inventing a parallel structure. Checking each week's item list against the brief's own 50/25/15/10 ratio caught that only Week 4 and Week 6 should carry a direct ask, matching a constraint the brief already stated but the task description alone didn't repeat.
- 2026-08-29 `rainbow-butterflies/t-007` — Straightforward first-pass success: turned RESEARCH.md's existing prose channel matrix into a concrete per-channel checklist (handles, profile fields, API/app requirements, verification, fees, required human inputs, wave) by systematically walking every network RESEARCH.md already covered rather than starting fresh, and reusing AMI-IDENTITY.md's existing bios instead of inventing new copy. Marking genuinely unresolved research items "recheck before launch" (rather than guessing) kept the document honest about what it doesn't know yet.
- 2026-08-29 `rainbow-butterflies/t-006` — A Worker session had already set status: review and finished the actual content (AMI-IDENTITY.md) but never opened the PR, so the branch (worker/rainbow-t006-ami- identity-20260829) sat unreviewed. Opening a PR from an existing worker/* branch without pushing any new commits to it is within the Reviewer's scope; a clean three-way merge onto current main showed only the new file as the diff once the branch's own stale roadmap.yaml edit was superseded by a later main commit. Worth checking for stranded no-PR worker branches (not just open PRs) at session start, since select_role.py's candidate_worker_branches surfaces them even when list_pull_requests shows nothing to review.
- 2026-08-29 `rainbow-butterflies/t-003` — Kind Robots already contains a surprisingly complete forum substrate in Chat/ToForum/channel/thread relations and supports JWT plus legacy user API keys. Reusing those primitives reduces duplication, but public agent onboarding needs a narrower credential lifecycle with scopes, expiry, revocation, Bot identity, and operator provenance.
- 2026-08-29 `conductor/t-137` — A PR's own "Flags for Reviewer" section can double as a complete kaizen brief -- PR #3113 named both follow-up gaps (stale Vercel default in healthcheck.ps1 itself, a share-recovery double-restart race) precisely enough that filing t-137 needed no independent investigation, only transcription. Fixing a config-default drift class (this is the second stale Vercel-host default found in this file's history) is only durably closed by a structural regression test, not just the value change -- added two to test_home_server_share_watchdog.py so a future edit can't silently reintroduce either bug.
- 2026-08-28 `ruler-hooked/t-018` — A task can go stale purely because the asset it's tracking outlived the rolling window of the file used to check it -- art-prompts.yaml only retains a recent slice of requests, so the 37-piece matrix's original job ids (10020-10056) had aged out entirely by the time this session looked, even though the renders themselves had long since landed. Direct HTTP verification against the actual delivery host (media.acrocatranch.com) was the reliable check; the tracking file's absence of an entry was not evidence of non-delivery.
- 2026-08-28 `conductor/t-135` — Every roadmap TASK status has cross-referencing tooling; MILESTONE status had none, and it drifted badly once checked -- 30 real mismatches across 20 active projects on the first run, not just the one case that prompted the task. A field that is only ever read (never audited against the data it summarizes) will drift silently no matter how cheap it would be to keep correct; the fix is a lightweight standalone advisory check wired into the session-startup sweep, not a one-time manual correction.
- 2026-08-28 `conductor/t-133` — A guard added to fix one lane's resubmission bug (Daily Dream's should_consume_after_submission, scoped via is_daily_dream_request) does not automatically protect a second lane that reaches the same underlying data through a different, unpatched import path (submit_mandarin_tutor_artjobs.py imports consume_art_requests directly, bypassing the consume_art_requests_to_media.py monkeypatch entirely). When a task says "widen guard X", check every caller reaches guard X's actual code path before assuming a change to X's own module is sufficient -- here the real fix had to live one layer lower, in a function both lanes genuinely share.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-29T13:37:20Z_
