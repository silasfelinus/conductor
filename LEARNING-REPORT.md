# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-27T18:44:49Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **788**
- Outcomes: blocked: 15, cancelled: 1, done: 772
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
| conductor | 83 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 20 | 100% |
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
| kind-robots | 52 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 7 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 10 | 100% |
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
| software | 772 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 11 |
| transient | 11 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 11 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-27 `cthulhuquarium/t-023` — A task whose deliverable is content (two authored Character/Bot voice pairs) can be fully "done" even when a downstream, standard-rule step (generated portrait art) is stalled by unrelated infra -- don't conflate "the content is complete" with "everything the task mentions has happened." Splitting them (ship the records now, file the infra fault as its own needs-human task, note the exact idempotent retry command in both the roadmap note and the PR) kept the real deliverable from being held hostage by a render-box hardware problem outside this task's control.
Cross-check any ComfyUI failure signature against `GET /api/art/queue/stats` and TALKBACK before assuming it's novel -- this exact `CLIPTextEncode hostbuf_file_reader_read` string was already diagnosed and closed once (ai-art-academy/t-068, disk13 cable) less than 24 hours earlier, so the right move was flagging a likely recurrence with full context, not re-diagnosing from scratch.
- 2026-08-27 `cthulhuquarium/t-016` — A task note's "may pause or redirect income briefly" is a soft option, not a requirement -- reading the HARD CONSTRAINT amendment in full ("no event may take anything away") before designing anything showed that every event kind could be built as a coin bonus or a zero-effect cosmetic beat, sidestepping the real complexity of an actual accounted income pause for a barely-noticeable player-facing difference. Explicit scope-decision comments (in the YAML, the TS, and the PR body) on why the pause was skipped make that a documented choice a reviewer can challenge, not a silent gap they'd have to notice on their own.
Operational note for future sessions: `git reset --hard origin/<branch>` silently discards ANY uncommitted local change in the working tree, not just changes on the branch you're resetting -- including an edit to a file the session made earlier in the SAME repo checkout for unrelated reasons (here: an economy.yaml edit made before claiming the task, lost by a later `git checkout main && git reset --hard origin/main` done purely to refresh state after a different PR's merge). Caught by grepping for the expected content immediately after the reset rather than assuming the working tree still held it; redone from scratch. The safer sequence when a local edit must survive a state refresh: check `git status` for uncommitted changes before any `reset --hard`, or commit/stash first.
- 2026-08-27 `cthulhuquarium/t-014` — A task whose server API already shipped under an earlier task (t-009 built the browse/[username]/[slug] endpoints "frontend/UI wiring is separate scope, not built here") is real remaining work, not a duplicate -- reading that prior task's completion note up front correctly scoped this one to default-visibility + a one-click toggle + the two frontend pages, instead of re-deriving or re-building the already-shipped server side. The layout contract's one-header rule caught both new pages rendering their own <h1> on the first test:layout-contract run; switching to <h2> (matching the existing pages/play/challenges/* convention, since these are plain Nuxt pages with no content-frontmatter shell) fixed it in one pass.
- 2026-08-27 `cthulhuquarium/t-048` — A kaizen task with no depends_on and a well-scoped note (pause two named loops on visibilitychange, resume the same way they started) is often genuinely a single-session, single-file change -- extracting startLoops()/stopLoops() from the existing onMounted/onBeforeUnmount bodies with zero behavior change on mount/unmount, then wiring a visibilitychange listener around them, needed no schema, no new test infra, and no design decisions left open. Verified by type-check + lint + reasoning about the extracted control flow rather than a new automated test, since no test harness for this component's mount lifecycle existed to extend.
- 2026-08-27 `cthulhuquarium/t-031` — A record's schema and its consumers can land in different tasks without a gap: t-032 already added AquariumCodexEntry.bestStat* columns and t-024 already built the collected/fieldNote codex view, so t-031 was "wire the already-decided record's remaining two features into the existing view" rather than a new screen. Both new features (best-individual-stats, re-order) are provable no-ops today because their upstream dependencies (t-029 genetics, t-030 sell-back) haven't landed -- writing unit tests for the pure merge function (mergeBestStats) that assert the both-null case explicitly, rather than skipping coverage for "nothing to test yet," is what makes that correctly-inert-for-now claim verifiable instead of just asserted.
- 2026-08-27 `cthulhuquarium/t-026` — A task's own economy.yaml section can already contain the full balance spec before any code exists -- set_pieces (all seven kinds, exact effect values) was fully authored in a prior session's economy.yaml edit, so this task was really "wire an already-decided spec into code" rather than "design set pieces from scratch." Reading the data file's own comments (no_stack_idle_effects, the debris_skimmer/click_clears sync note) surfaced constraints that would otherwise have needed a second pass to discover. The one real design gap economy.yaml left open was equip pricing, which it explicitly named as this task's job to fill in -- anchoring those to RARITY_TIERS rather than inventing unrelated numbers kept the new values traceable the same way every other price in the file already is.
- 2026-08-27 `cthulhuquarium/t-013` — An "offline income" task can be mostly already shipped by an earlier task with a different name -- t-009/t-011 had already built the full server-authoritative settleTick/lastTickAt settlement (8h cap, 0.5x multiplier, coins only ever server-incremented) before this task was ever picked up. Reading the existing store/component flow end-to-end before writing anything found the real remaining gap was narrower and different from what the title suggests: the "welcome back" moment was an easy-to-miss inline banner instead of "one clear panel," and the Clean button (a different task's, t-027's, active-play channel) fired one write per click with no batching. Claimed the conductor task before starting the cross-repo kind_robots implementation this time, per the lesson recorded in this same day's ruler-hooked/t-021 collision.
- 2026-08-27 `cthulhuquarium/t-012` — Before implementing a "wire the shop" task, read what the prior task already shipped -- t-011 had already wired buy-food and species-unlock end-to-end (including auto-placement), so the real remaining gap was a design-intent violation already visible in the diff (the field note was rendered pre-unlock, contradicting the task's own "reveals on first unlock, not before" note), not a missing feature. Checking sibling tasks' depends_on graph (t-026 depends_on t-012, status: waiting) also confirmed "buy upgrades" from this task's note was intentionally deferred, not a gap in this task.
- 2026-08-27 `ruler-hooked/t-021` — A heavier cross-repo implementation task (kind_robots code, ~800 lines, three distinct pieces) was claimed and implemented start-to-finish before ever touching the conductor roadmap, since the code work itself needed no roadmap edit until close-out. A different concurrent session claimed the same task in the roadmap mid-implementation with no way to see this session was already deep into it. No work was lost -- this session's implementation was complete and merged first, so the close-out simply documented the collision and pointed the other session at main -- but the gap was real: claiming the conductor task BEFORE starting the cross-repo code (not only recording it after), even though the roadmap edit itself isn't needed until later, would have surfaced the collision to the other session immediately instead of after both sides had sunk effort in.

- 2026-08-27 `interface-vision/t-121` — A trivial, verified-clean 2-file markup diff took 6 attempts and ~50 minutes of retries for kind_robots' required Contract verifiers check to actually complete, stalling at a different step nearly every time (install, several individual per-file contracts, and 3 of 6 times specifically at the full-repo ESLint ratchet step) despite the exact same script finishing in seconds locally against the identical diff -- pure CI-infra flakiness, not a code problem. Confirming the script itself is clean locally before assuming a hung required check reflects a real diff issue saved real time; filed conductor/t-132 to track the pattern (esp. the ESLint-ratchet-specific recurrence) for future diagnosis rather than re-deriving it next time.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-27T18:44:49Z_
