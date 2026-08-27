# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-27T22:49:27Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **794**
- Outcomes: blocked: 16, cancelled: 1, done: 777
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
| cthulhuquarium | 26 | 96% |
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
| software | 778 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 12 |
| transient | 11 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-27 `cthulhuquarium/t-019` — "Retune against real play data" cannot be satisfied by a sandboxed agent session when no telemetry/analytics path exists yet and the session has no way to generate a real multi-session player history itself -- this is an actionable failure (missing access to the core input the task needs), not a quality failure, so it does not burn a pass. A prior session (2026-08-25) had already flagged the milestone-ladder half of this task as needing play data specifically to avoid a naive fix (linear breakpoint extension) that would silently undermine an intentional design constraint (the tank-packing problem) -- worth trusting that prior judgment rather than re-deriving new numbers from design docs alone and asserting they're tuned, when they would actually just be another guess.
- 2026-08-27 `cthulhuquarium/t-051` — A balance-pass task that explicitly allows a no-op exit does not need real play data to close well -- reviewing DECOR_CATALOG's six costs against the existing RARITY_TIERS anchor (already the established convention SET_PIECE_CATALOG uses) surfaced a deliberate taper, not a guess, and was enough to confirm the pricing rather than requiring telemetry this sandbox cannot produce. Worth distinguishing from t-019 in the same session: a task is only genuinely blocked on real data when its own note requires *feel* (does the pacing feel right) rather than *consistency* (does this number follow the pattern the rest of the file already sets).
- 2026-08-27 `cthulhuquarium/t-049` — Adding a purely cosmetic canvas sprite (roaming collector automaton) went fastest by mirroring an existing sibling pattern in the same file -- SWIM_SPEED_SET_KIND's equipped-set-piece read, and the swimmer/mote step+render split -- rather than inventing a new structure. Keeping the change client-rendering-only (no economy/API touch, since settleTick already owns the real roaming_collector income bonus server-side) kept the task genuinely reversible and let the existing aquarium-economy and aquarium-touch test suites stand as sufficient verification without a live browser.
- 2026-08-27 `cthulhuquarium/t-052` — A kaizen task that names the exact fix (add User: { isRestricted: false } to listPublicTanks, matching the leaderboard's already-shipped filter) is a fast, low-risk pickup for a scheduled sweep -- no design judgment needed, just apply the established pattern and verify with the existing aquarium test suites. Worth favoring these small, precisely-scoped kaizen followups when a session needs to pick one task with minimal ambiguity.
- 2026-08-27 `cthulhuquarium/t-018` — A "leave it alone; it is funnier untouched" design note doesn't mean skip the feature -- it means build the plain, understated version and resist adding flourish, foreshadowing, or extra UI weight around it. Read against SYSTEMS.md/DESIGN-BRIEF.md's finale-foreshadowing section before starting confirmed the task's own note (rank by species collected, display names only) was the complete spec, with the "leave it alone" line steering tone (no finale hints near it) rather than scope.
Consent boundaries for public-facing player data aren't one flag: a sibling feature's own opt-in (Aquarium.isPublic, from the dependency this task built on) is the right gate for "will this player's data appear here," not a same-purpose-sounding but different flag from an unrelated feature (the friend-finder directory's listInDirectory). Checking which existing feature the new one actually depends on for consent semantics -- not just grepping for the first consent-shaped flag in the schema -- kept the leaderboard consistent with the browse page it extends.
- 2026-08-27 `cthulhuquarium/t-017` — A genuinely novel feature with no prior in-repo precedent (no decor code, no established real drag-and-drop convention) is worth a research-only Explore pass before writing any implementation code -- confirmed via grep across the whole repo that the only `draggable` attribute anywhere was unwired dead code in stage-manager.vue, which settled the design decision (native Pointer Events over introducing a DnD dependency) before any code was written instead of discovering it mid-implementation.
Extending an existing shared Prisma select (publicAquariumDetailSelect) to carry a new relation is often enough to satisfy a "visible to visitors" style requirement with zero new routes -- check whether the read path already flows through a shared select before assuming a new endpoint is needed.
- 2026-08-27 `cthulhuquarium/t-023` — A task whose deliverable is content (two authored Character/Bot voice pairs) can be fully "done" even when a downstream, standard-rule step (generated portrait art) is stalled by unrelated infra -- don't conflate "the content is complete" with "everything the task mentions has happened." Splitting them (ship the records now, file the infra fault as its own needs-human task, note the exact idempotent retry command in both the roadmap note and the PR) kept the real deliverable from being held hostage by a render-box hardware problem outside this task's control.
Cross-check any ComfyUI failure signature against `GET /api/art/queue/stats` and TALKBACK before assuming it's novel -- this exact `CLIPTextEncode hostbuf_file_reader_read` string was already diagnosed and closed once (ai-art-academy/t-068, disk13 cable) less than 24 hours earlier, so the right move was flagging a likely recurrence with full context, not re-diagnosing from scratch.
- 2026-08-27 `cthulhuquarium/t-016` — A task note's "may pause or redirect income briefly" is a soft option, not a requirement -- reading the HARD CONSTRAINT amendment in full ("no event may take anything away") before designing anything showed that every event kind could be built as a coin bonus or a zero-effect cosmetic beat, sidestepping the real complexity of an actual accounted income pause for a barely-noticeable player-facing difference. Explicit scope-decision comments (in the YAML, the TS, and the PR body) on why the pause was skipped make that a documented choice a reviewer can challenge, not a silent gap they'd have to notice on their own.
Operational note for future sessions: `git reset --hard origin/<branch>` silently discards ANY uncommitted local change in the working tree, not just changes on the branch you're resetting -- including an edit to a file the session made earlier in the SAME repo checkout for unrelated reasons (here: an economy.yaml edit made before claiming the task, lost by a later `git checkout main && git reset --hard origin/main` done purely to refresh state after a different PR's merge). Caught by grepping for the expected content immediately after the reset rather than assuming the working tree still held it; redone from scratch. The safer sequence when a local edit must survive a state refresh: check `git status` for uncommitted changes before any `reset --hard`, or commit/stash first.
- 2026-08-27 `cthulhuquarium/t-014` — A task whose server API already shipped under an earlier task (t-009 built the browse/[username]/[slug] endpoints "frontend/UI wiring is separate scope, not built here") is real remaining work, not a duplicate -- reading that prior task's completion note up front correctly scoped this one to default-visibility + a one-click toggle + the two frontend pages, instead of re-deriving or re-building the already-shipped server side. The layout contract's one-header rule caught both new pages rendering their own <h1> on the first test:layout-contract run; switching to <h2> (matching the existing pages/play/challenges/* convention, since these are plain Nuxt pages with no content-frontmatter shell) fixed it in one pass.
- 2026-08-27 `cthulhuquarium/t-048` — A kaizen task with no depends_on and a well-scoped note (pause two named loops on visibilitychange, resume the same way they started) is often genuinely a single-session, single-file change -- extracting startLoops()/stopLoops() from the existing onMounted/onBeforeUnmount bodies with zero behavior change on mount/unmount, then wiring a visibilitychange listener around them, needed no schema, no new test infra, and no design decisions left open. Verified by type-check + lint + reasoning about the extracted control flow rather than a new automated test, since no test harness for this component's mount lifecycle existed to extend.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-27T22:49:27Z_
