# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-13T15:50:04Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **945**
- Outcomes: blocked: 16, cancelled: 1, done: 928
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 27 | 100% |
| conductor | 99 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 134 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 83 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 20 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 21 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 928 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 21 |
| transient | 15 |
| actionable | 14 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 21 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 14 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-13 `coloring-book/t-041` — Kaizen from t-040: grepping the rest of the coloring-book pipeline for the same bare 'from PIL import Image' pattern found two more genuine hits (consume_coloring_book_color_art.py, manage_coloring_book_cover.py) and two false leads that already degrade gracefully (art_quality.py's load_stats returns None; consume_art_queue_core.py's save_result falls back to PNG with its own actionable message). A kaizen framed as 'grep for the same pattern elsewhere' is worth doing literally and completely in one pass rather than fixing only the first hit found -- distinguishing already-graceful call sites from genuinely bare ones is the actual work, not the grep itself.
- 2026-09-13 `coloring-book/t-040` — A recurring TALKBACK-flagged papercut (bare 'PIL unavailable' error on a non-persistent sandbox Pillow install, rediscovered fix-and-forgotten across three separate sessions on 2026-08-11 and 2026-09-13) had its actual fix fully specified in the task note before this session ever claimed it -- the work was pure implementation, no design decision needed. When a TALKBACK entry proposes the exact same concrete fix three times running, the next session to touch that area should file the roadmap task itself rather than re-suggesting it a fourth time; this task existed only because a prior session finally did that.
- 2026-09-13 `kindrobots-unraid/t-019` — An alarming-looking MCE decoded to a benign one. Status bea0000000000108 sets PCC (processor context corrupt), which reads as the urgent case, but TSC 0 is the decisive field: a real machine-check exception captures a timestamp, so zero means machine_check_poll() read stale bank status -- and the boot-time poll of all banks runs without MCP_TIMESTAMP, so it always logs TSC 0. EDAC initialising 45s later confirmed the line landed ~1 min into a boot. Decode the status bits before escalating on the headline; also decode IPID (HWID 0xB0 / McaType 0x5 = SMCA_EX) rather than assuming a bank number means memory. The correlation check the task was filed to run came back NEGATIVE and was still worth the round trip: dmesg covered the whole current boot including t-018's window with no MCE, which is a clean negative on hardware for that incident, and the same output exposed three real blind spots (RAM-only syslog, non-ECC memory so no EDAC detector at all, 4x16GB DDR4-3600 above JEDEC on a Matisse IMC) now tracked at t-020. A diagnostic that disproves your hypothesis but hands you the actual lead is a success, not a wasted pass.
- 2026-09-13 `interface-vision/t-104` — Slice 260: a fresh full-repo class-frequency survey scoped to component-styling token families (badge/btn/input/select/checkbox/textarea/text-/icon/loading/etc.) rather than raw flex-layout utility combos (flex gap-2 items-center and similar score far higher by count but are structural, not the visual/design-token surfaces this umbrella targets) found a clean new three-size family (kr-loading-primary-xs/-sm/-md) at 17 exact-match occurrences across 13 files. Reinforces slice 249/253's precedent of bundling sibling sizes/colors of the same shape into one slice with separate per-primitive codemods, and that vue-tsc/eslint/verifyKrClassCoverage.ts/verifyLayoutContract.ts run locally via provision_kind_robots_deps.sh catch what CI would catch, before ever opening the PR.
- 2026-09-13 `kindrobots-unraid/t-018` — Fourth occurrence of the 502/503 outage class (t-014, t-015, t-017, t-018), again caught only because a scheduled sweep happened to notice rather than any alerting. Closed on objective recovery evidence alone (8 consecutive healthy curls against / and /api/health/database over ~20s, schemaCurrent: true) per docs/state-reconciliation.md -- no Unraid/Alexandria access was needed or used, since the sandbox's unrestricted HTTPS egress to kindrobots.org is sufficient to confirm the task's own stated close-out criterion. approved_by_human stays false per the t-014/t-015/t-017 precedent. kindrobots-unraid/t-016 (external health probe/alert) is still ready/unclaimed after four occurrences -- this is the actual fix for the detection gap, not another manual sweep catching it by luck.
- 2026-09-13 `interface-vision/t-136` — Kaizen from t-135 closed the gap outright: verifyKrClassCoverage.ts (kind_robots#2696) asserts every static kr-* class token used in a components/+pages/ template has a matching .kr-* rule, no ratchet/baseline since an undefined kr-* reference is never intentional. The PR's own comment-migration-contract check was red at review time from an unrelated live kindrobots.org 502 (kindrobots-unraid/t-018, confirmed via direct curl and one re-run reproducing the identical error) -- correctly triaged as not-this-PR's failure and merged anyway once every check touching the actual diff was green.
- 2026-09-13 `interface-vision/t-135` — Four consecutive t-104 badge-migration slices (#2691-#2694, three different sessions) introduced and reused a CSS class name (kr-badge-accent-sm) that was never defined, because every check that passed on those PRs (TypeScript, eslint, layout-contract, the full Storybook/Narrative contract suite) type-checks templates and structure but never asserts that a referenced kr-* @apply target actually exists in tailwind.css -- so four real visual regressions (unstyled plain text instead of a badge) shipped to production invisibly. Caught only because a Reviewer pass grepped the CSS file directly instead of trusting green CI. Kaizen filed on the fix PR: add a cheap repo-wide check asserting every kr-* class token used in a class="..." attribute has a matching rule in tailwind.css, so the next missing-primitive slice fails fast in CI.
- 2026-09-13 `kindrobots-unraid/t-017` — A recovered production incident should be closed on objective evidence (health endpoint + SSR check + the actual fix commit on kind_robots main) rather than left needs-human pending root-cause paperwork once the root cause is already known from a merged fix -- docs/state-reconciliation.md's 'Closing human gates safely' section and CLAUDE.md's session-end rule both say so explicitly. approved_by_human stays false per the t-014/t-015 precedent for this exact outage class; only Silas sets that field. Third occurrence of this outage class with kindrobots-unraid/t-016 (external health probe) still unclaimed -- worth prioritizing so a lucky scheduled sweep isn't the detection mechanism again.
- 2026-09-12 `conductor/t-155` — Reused project_lifecycle.ordered_workable_slugs (the same helper check_priority_queue_starvation.py and next_ready_task.py already use) to sort audit_human_gates.py's report by priority-queue rank instead of writing new roadmap-walking logic -- confirms t-149's lesson generalizes: grep for the existing shared module before writing a new roadmap-ordering tool, and a report can be re-ordered by reusing pickup-order logic without touching what it detects.
- 2026-09-12 `conductor/t-149` — check_priority_queue_starvation.py was straightforward to build correctly on the first pass by reusing the exact shared modules (roadmap_claims, roadmap_deps, daily_gate, project_lifecycle) next_ready_task.py already uses, rather than reimplementing claim/staleness/dependency logic -- the two scripts structurally cannot disagree about what counts as claimable ready work. Worth defaulting to this pattern (grep for the existing shared module before writing new roadmap-walking logic) for any future roadmap-reading tool.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-13T15:50:04Z_
