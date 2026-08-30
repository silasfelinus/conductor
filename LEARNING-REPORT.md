# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-30T08:47:46Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **831**
- Outcomes: blocked: 16, cancelled: 1, done: 814
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
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 87 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 41 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 92 | 100% |
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
| rainbow-butterflies | 7 | 100% |
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
| software | 815 | 99% |

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

- 2026-08-30 `rainbow-butterflies/t-020` — forum-thread.vue had drifted entirely off the canonical /api/v1/forum/* endpoints onto a legacy chatStore path with a hardcoded, wrong channel list and an unimplemented reply handler -- the backend (server/utils/forumApi.ts) was already built and unused by any client. Worth checking, before starting a "build X" task, whether the backend already exists and only the frontend wiring is missing; the task note's own framing ("let humans and agents post through the same API") was the tell that a real API already existed to point at. Also: not every authorship kind a task note names has to be invented in the same slice -- HUMAN_AI and SYSTEM had no schema/backend concept behind them, so they were flagged as a follow-up needing a product decision rather than guessed at.
- 2026-08-30 `interface-vision/t-104` — Slice 63 (kind_robots#2220) was a clean, exact-match kr-panel substitution on project-front-page.vue's two raised-surface sections, following the same override convention prior slices established (kr-panel + trailing rounded-3xl/p-5 overrides for values that differ from kr-panel's rounded-2xl/p-6 defaults). Verified the CSS definition (assets/css/tailwind.css .kr-panel) before merging to confirm the override convention actually produces the same computed classes, rather than trusting the PR description's claim alone.
- 2026-08-30 `interface-vision/t-104` — Slice 62: the kr-note family (border-{status}/N + bg-{status}/M + text-{status}) is a much bigger candidate pool (~150+ raw grep hits) than any prior mechanical sweep, but padding/opacity/text-size/font-weight vary too widely across it to convert blindly -- unlike kr-container/kr-surface/kr-panel-flat, where near-total instances matched the canonical shape exactly. Scoping the slice to only instances where every differing attribute was explicit in the original class list (never inferring an ambient/inherited text-size or font-weight) kept the substitution provably byte-for-visual-identical at the cost of converting only 7 of ~150 instances this slice. Also worth noting: a family of otherwise-identical pills/badges sharing one non-kr-note color (stage-manager.vue's primary/success/warning trio) should be skipped as a set rather than partially converted, since fixing two of three fragments what was a visually consistent group.

- 2026-08-30 `interface-vision/t-104` — Slice 57: opened a third mechanical pool (kr-panel-flat) alongside kr-container and kr-surface, both reported near-exhausted. A repo-wide grep for the hand-rolled dashed empty-state shape ('rounded-2xl border border-dashed border-base-300 bg-base-100') turned up 13 exact matches plus one non-dashed variant, none previously swept. Key discipline: excluded near-miss translucent variants (bg-base-100/50, /60, /70) as a genuinely different, not-byte-exact shape rather than folding them in -- confirmed via a baseline prettier/eslint check per file (git stash + rerun) which was itself pre-existing drift on main, not something this slice introduced. When a class-string edit shortens a line enough to change its wrap point, run prettier --check on main at the same file BEFORE editing to know whether a resulting --write is a real fix (file was clean) or would trigger an unrelated full-file reformat (file was already dirty) -- doing this blind cost one wasted 2700-line reformat-and-revert cycle on art-test.vue this slice.

- 2026-08-30 `interface-vision/t-104` — Slice 56: swept the kr-surface pool slice 55 flagged. The highest-leverage single conversion was components/manager/kr-manager.vue itself -- the shared shell every primary-model dashboard (bot/character/reward/facet/scenario/giftshop managers) delegates its root to via <kr-manager>, so fixing its one root class reaches all of them transitively instead of needing per-manager edits. 6 more standalone managers (art-manager, artjob-queue-browser, art-studio, stylist-relay-status, animation-manager, giftshop-manager) shared the identical hand-rolled root and converted the same way. A useful check before assuming a *-manager.vue hit needs its own edit: verify whether its root actually delegates to <kr-manager> first -- most do, and editing the shell once is strictly better than editing each call site.
- 2026-08-30 `interface-vision/t-104` — Slice 55: the kr-surface root-wrapper pool (hand-rolled 'flex h-full min-h-0 ... overflow-hidden') is a parallel-but-unswept sibling of the kr-container mx-auto/max-w- pool -- most *-manager.vue hits are false positives (root is <kr-manager>), but user-manager.vue's root was a genuine byte-exact-apart-from-gap-override match. Worth a dedicated future slice checking the kr-surface pool specifically, the way max-w-N overrides already work for kr-container.
- 2026-08-30 `cthulhuquarium/t-064` — Milestone status drift can also hide behind non-extreme values (in-progress/planned) with 100% task completion underneath, not just the not-started/done extremes check_milestone_status_drift.py originally checked -- conductor/t-138 (merged same day) widens that check so this class of drift surfaces automatically going forward.
- 2026-08-29 `interface-vision/t-104` — A recurring mechanical-sweep task's 'exhausted against main@<SHA>' note goes stale the moment main moves, even by unrelated commits -- several same-day sessions treated the note as still valid without re-running the actual grep, and a fresh full-repo search turned up six real unconverted candidates. Re-verify against the exact current SHA before trusting a same-day exhaustion claim, don't just check whether the SHA moved.
- 2026-08-29 `brainstorm/t-025` — Reusing ART_ENGINE_PROFILES keeps prompt-only engine availability centralized and naturally excludes source-image-only engines from Brainstorm's fresh text-to-image flow.
- 2026-08-29 `rainbow-butterflies/t-012` — Once one of DESIGN-BRIEF.md's five 'fundraising experiments worth testing' has already been picked for the calendar (Butterfly bounties, t-008/CONTENT-CALENDAR.md), a sibling task asking to 'prepare' a different named experiment (t-012, Why I donated + skeptics build too) should be scoped as a second ready-to-launch alternative, not a competing Week-6 proposal -- state the relationship explicitly rather than silently overwriting the calendar's existing recommendation.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-30T08:47:46Z_
