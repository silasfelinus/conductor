# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-29T09:41:39Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **818**
- Outcomes: blocked: 16, cancelled: 1, done: 801
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
| rainbow-butterflies | 2 | 100% |
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
| software | 802 | 99% |

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

- 2026-08-29 `rainbow-butterflies/t-006` — A Worker session had already set status: review and finished the actual content (AMI-IDENTITY.md) but never opened the PR, so the branch (worker/rainbow-t006-ami- identity-20260829) sat unreviewed. Opening a PR from an existing worker/* branch without pushing any new commits to it is within the Reviewer's scope; a clean three-way merge onto current main showed only the new file as the diff once the branch's own stale roadmap.yaml edit was superseded by a later main commit. Worth checking for stranded no-PR worker branches (not just open PRs) at session start, since select_role.py's candidate_worker_branches surfaces them even when list_pull_requests shows nothing to review.
- 2026-08-29 `rainbow-butterflies/t-003` — Kind Robots already contains a surprisingly complete forum substrate in Chat/ToForum/channel/thread relations and supports JWT plus legacy user API keys. Reusing those primitives reduces duplication, but public agent onboarding needs a narrower credential lifecycle with scopes, expiry, revocation, Bot identity, and operator provenance.
- 2026-08-29 `conductor/t-137` — A PR's own "Flags for Reviewer" section can double as a complete kaizen brief -- PR #3113 named both follow-up gaps (stale Vercel default in healthcheck.ps1 itself, a share-recovery double-restart race) precisely enough that filing t-137 needed no independent investigation, only transcription. Fixing a config-default drift class (this is the second stale Vercel-host default found in this file's history) is only durably closed by a structural regression test, not just the value change -- added two to test_home_server_share_watchdog.py so a future edit can't silently reintroduce either bug.
- 2026-08-28 `ruler-hooked/t-018` — A task can go stale purely because the asset it's tracking outlived the rolling window of the file used to check it -- art-prompts.yaml only retains a recent slice of requests, so the 37-piece matrix's original job ids (10020-10056) had aged out entirely by the time this session looked, even though the renders themselves had long since landed. Direct HTTP verification against the actual delivery host (media.acrocatranch.com) was the reliable check; the tracking file's absence of an entry was not evidence of non-delivery.
- 2026-08-28 `conductor/t-135` — Every roadmap TASK status has cross-referencing tooling; MILESTONE status had none, and it drifted badly once checked -- 30 real mismatches across 20 active projects on the first run, not just the one case that prompted the task. A field that is only ever read (never audited against the data it summarizes) will drift silently no matter how cheap it would be to keep correct; the fix is a lightweight standalone advisory check wired into the session-startup sweep, not a one-time manual correction.
- 2026-08-28 `conductor/t-133` — A guard added to fix one lane's resubmission bug (Daily Dream's should_consume_after_submission, scoped via is_daily_dream_request) does not automatically protect a second lane that reaches the same underlying data through a different, unpatched import path (submit_mandarin_tutor_artjobs.py imports consume_art_requests directly, bypassing the consume_art_requests_to_media.py monkeypatch entirely). When a task says "widen guard X", check every caller reaches guard X's actual code path before assuming a change to X's own module is sufficient -- here the real fix had to live one layer lower, in a function both lanes genuinely share.
- 2026-08-28 `conductor/t-134` — A directory-listing-only share probe ("can I read one entry") is not a test for a partially-populated share -- it needs to check the specific files a render actually depends on, opened and read, not just scandir'd or stat'd (a stale SMB handle can satisfy a stat too). Generalized as KR_SHARE_REQUIRED_FILES, opt-in and unset by default so the existing directory-only behavior is unchanged unless configured.
- 2026-08-28 `cthulhuquarium/t-063` — A kaizen note's framing of "what's still open" (t-062's note named only t-058) was itself stale by the time this audit ran -- it undercounted by four tasks (t-019, t-021, t-022, t-041 were also open needs-human items). A planning/audit task should always re-derive the open set directly from live roadmap state (grep every task's own status) rather than trusting the prior task's kaizen prose about what remains, even when that prose sounds authoritative. Also caught a genuinely stale milestone `status` field (m3 sat at `not-started` despite 25/31 tasks done) -- milestone status isn't auto-derived from task counts anywhere in this repo's tooling, so it silently drifts unless an audit like this one checks it by hand.
- 2026-08-28 `cthulhuquarium/t-062` — Show-the-price-before-clicking (kind_robots#2182) had a nearby precedent in the same function (breedCost, added by t-055) that looked like a template but wasn't quite one: breedCost is a fixed per-species number nested under Monster, while sellPrice depends on the individual's own rolled stats and belongs as a top-level ClientStock field instead. Copying the precedent's TYPE SHAPE without checking whether its reasoning (per-species vs. per-individual) still applies would have produced a field that was technically present but structurally misleading. Checking why a precedent is shaped the way it is, not just that one exists, is what caught this before it shipped.
- 2026-08-28 `cthulhuquarium/t-061` — A "read-and-report audit" task (kind_robots#2181) turned out to have exactly one applicable shape once grepped precisely: of 17 files matching `meta:` under server/, only three (browse/catalog/leaderboard) return an actual API-response meta object -- everything else was ComfyUI workflow node `_meta`, a same-named but unrelated shape. Narrowing from a broad text match to the specific contract (an API route's response envelope, not any object literal keyed `meta`) before concluding "N call sites found" avoided both over-counting false positives and under-counting by assuming the grep result was already the answer. The two real hand-cast call sites (browse/leaderboard pages) already read the server's meta.total correctly -- the audit's fix was purely routing through performFetch's typed second generic instead of a manual ApiResponse<T> & {meta?: {...}} cast, so "no behavior change" was verifiable, not just claimed.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-29T09:41:39Z_
