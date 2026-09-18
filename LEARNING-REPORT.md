# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-18T04:39:30Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1010**
- Outcomes: blocked: 16, cancelled: 1, done: 993
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 3 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 120 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 24 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 136 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 64 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 14 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 29 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 993 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 28 |
| transient | 16 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 28 occurrences; look for the shared cause across its records
- failure category `transient` — 16 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-18 `art-archive/t-005` — Clean first-pass success following t-004's rejection lesson: the Worker correctly treated raw-metadata retention as a hard invariant (preserved verbatim in extractedMetadata for every format) while still scoping per-column generation-field extraction to PNG only, matching what t-006/ t-008 actually need next. A contract verifier regex-checking the privacy/ maturity/idempotency invariants directly against source shipped alongside the feature, not as an afterthought -- worth treating as the default shape for any importer/reconciler task in this project going forward.
- 2026-09-18 `art-archive/t-004` — A reviewer caught a real scope gap on the first pass: the task's own note said "extract available ... EXIF/text metadata" but the implementation returned supported:false for every JPEG/WebP unconditionally, reasoning (in the PR body) that PNG was "the format that actually carries this data in practice" -- true for AI-tool defaults, but the roadmap language was about what's AVAILABLE, not just the common case, and JPEG/WebP EXIF/XMP/COM can carry real provenance. Re-read a task's exact wording against the diff before calling something out of scope, especially when the shortcut is also the path of least implementation effort. Separately: Silas intervened directly on the implementation branch mid-cycle to correct an invented ART_ARCHIVE_ROOT env var to the already-existing PRIVATE_PATH convention -- when a human pushes directly to a branch you're working on, rebase your next commit on top of it rather than force-pushing over it; a plain rebase merged cleanly here since the files didn't overlap.
- 2026-09-18 `art-archive/t-003` — First implementation cycle on a brand-new project (art-archive, scaffolded the same day). Following an existing sibling model's own loose-reference convention (ModelBuildItem.artImageId has no formal Prisma @relation) let this migration add a whole new ledger table without touching ArtImage/ArtCollection at all, keeping the Reviewer's additive-migration audit trivial. CI's "Replay migrations on MariaDB" job is the real backstop for a hand-authored migration.sql in a sandbox with no MIGRATION_DATABASE_URL -- it caught nothing here, but it is the check that would.
- 2026-09-18 `storybook/t-010` — Same connectivity gap recurred immediately (select_role.py's urllib probe 403'd against cthulhuquarium again, producing reviewer-uncertain), but a direct GitHub MCP check on kind_robots again found the real open PR (#2813) the script's own failed calls weren't even probing. This is now the second session in a row hitting the identical pattern -- worth checking whether select_role.py's underlying_role fallback should itself try the GitHub MCP transport before giving up, rather than relying on every session to remember to cross-check by hand.
- 2026-09-18 `storybook/t-010` — select_role.py's raw urllib GitHub probe 403'd in this sandbox as usual, but the underlying worker-branch PR (kind_robots#2811) was real and reviewable via the GitHub MCP tools -- cross-checking select_role.py's uncertain verdict against a working transport before falling back to its "worker" recommendation caught a genuine PR that a literal reading of the tool's own output would have missed. Reviewed, confirmed all 47 checks green and mergeable_state clean with a diff scoped to exactly the intended files, then squash-merged and re-armed the task to ready per the established recurring-polish precedent.
- 2026-09-17 `dream-cycle/t-027` — check_live_facet_coverage.py now walks creation-burst bundles too (built.facets in projects/kind-robots/bursts/*.yaml), not only daily-dream backlog records -- any future live-coverage-style check over agent-recorded built-state should default to covering every bundle shape that records it, not just the first one that prompted the check.
- 2026-09-17 `appmaker/t-014` — A "FOR SILAS: decide X or Y" task can sit fully implementable long after the decision lands if nobody revisits it -- Silas answered this one on 2026-09-07 (approved_by_human: true, keep /appmaker admin-only and fix the copy) but the actual one-file copy fix wasn't picked up until this cycle. Worth a quick pass over ready tasks with approved_by_human: true and no implementation_pr to catch this class earlier next time.
- 2026-09-17 `appmaker/t-010` — A task blocked for weeks on open design questions can turn fully actionable the moment a human decision resolves them -- the roadmap note already carried Silas's 2026-09-07 answers to all three open questions (squash graduation, admin-only, existing-granted-repo-only), so the real work was reading that note carefully rather than re-deriving the design. Splitting the landable, reversible half (a Todo-filing request endpoint) from the genuinely irreversible half (the squash-push executor that writes to a real external repo) kept this PR safely mergeable without a human gate, while filing the executor as its own gate_human task (t-015) rather than either building it unreviewed or leaving the remaining scope implicit in t-010's note.
- 2026-09-17 `ruler-hooked/t-026` — Redesigning a discrete-action minigame (button REEL/SLACK/WAIT) into a continuous timing-bar input without breaking replay determinism was made tractable by keeping the animation purely client-side display and only ever sending the recorded stop position into a pure reducer -- the same "framework-free, never elapsed milliseconds" contract the rest of the engine already kept. Adding a `quality` parameter defaulting to 1 and proving byte-for-byte equivalence to the old formulas at quality=1 (self-test #8) gave a cheap, concrete regression guard for a refactor that touched core resolution math. Also confirmed prettier is not CI-enforced in kind_robots (no workflow runs `lint:prettier`/`npm run lint`) -- running it blind reformats unrelated code the task never touched; check for an enforcing workflow before applying a formatter repo-wide, and prefer reverting to the original eslint-clean formatting when it isn't enforced.
- 2026-09-17 `storybook/t-052` — The task note offered two options (client migration vs. export) but the export mechanism (buildExport/downloadStory) was already fully built at ?legacy=1 -- the actual gap was discovery, not implementation. Read the existing code before assuming a roadmap task's two listed options are both still open; often one is already done and the task is really about surfacing it. Filed t-054 (waiting on t-037) so the banner does not become permanent dead code once the beat loop it points at is deleted.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-18T04:39:30Z_
