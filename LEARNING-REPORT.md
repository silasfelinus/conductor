# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-20T04:44:38Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **700**
- Outcomes: blocked: 15, cancelled: 1, done: 684
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 17 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 77 | 100% |
| conductor-app | 4 | 100% |
| davinci | 5 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 36 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 70 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 14 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 684 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-20 `conductor/t-119` — The status:review transition (AGENTS.md step 7) was left ambiguous between claim_task.py's sanctioned direct-to-main exception and close_task.py's branch+PR pattern -- resolved by routing it through close_task.py (which already supports arbitrary target statuses, review included) rather than inventing a new script or a new hard-rule-1 exception. model-builder/t-029 cycle 21's STATUS.md merge conflict, doing this transition by hand with set_task_field.py + a manually-managed branch, was a symptom of not using the existing fetch-fresh git plumbing, not evidence that branch+PR is the wrong shape for this transition.

- 2026-08-19 `storybook/t-010` — Cycle 20 of the recurring storybook/t-010 bug-hunt: Dream rows without a first-class Prisma model of their own (Location is just dreamType === 'LOCATION' on the generic Dream table) are easy to under-serve relative to Character/Reward/Scenario/Facet, which each have both a dedicated model and a dedicated detail component with its own "start a story" deep-link CTA. The generic dream-narration.vue detail surface had no such CTA for any Dream type, so seedFromQuery()'s ?location= query key had been dead code with no sender anywhere in the repo since it was added. Worth checking, for any future object type added to Storybook's seed-query set, whether it actually has a first-class detail component or only the generic Dream surface -- the generic surface is the one that silently misses new CTAs.

- 2026-08-19 `brainstorm/t-021` — Adding real behavioral test coverage for Pinia store logic in this repo hits a real environmental wall: a store file that imports another store transitively (brainstormStore.ts -> serverStore -> userStore -> achievementStore) can be unimportable from a plain tsx process even though none of the actual logic under test needs Pinia, because some unrelated store in the chain calls a Vite-only API (import.meta.glob) at module load time. The fix already has a name in this codebase -- brainstormSourceAdapterKit.ts/brainstormSourceContextKit.ts already split pure logic out for exactly this reason -- but it's not written down as a general rule anywhere, so it's worth re-deriving the "does this file transitively import a store with a Vite-only top-level call" question explicitly before assuming a store's exports are tsx-testable. Second lesson: a CI job that installs with `npm ci --ignore-scripts` (for speed) skips the `nuxi prepare` postinstall that generates the '@/' path-alias tsconfig -- any new tsx-run script under such a job must use relative imports, not '@/', or verify locally with `.nuxt` removed before trusting it'll pass in CI.

- 2026-08-19 `brainstorm/t-024` — The task's own "scope check first" step is what caught this: before building any UI, re-verified whether bot-gallery.vue was actually unmounted as the t-018 kaizen note claimed, and found the claim already false on current main -- content/bots.md -> bot-manager.vue -> bot-interact.vue -> bot-gallery.vue is a complete, CI-verified (test:route-gallery-contract) mount chain reachable via the play channel's normal nav, not just a direct URL. Closed with no code change and no kind_robots PR. Worth generalizing: a kaizen-sourced task's premise can go stale between when it was written and when it is picked up, especially for reachability/mounting claims in a codebase with this much concurrent agent activity -- re-verify the premise against live main before writing any diff, not just before merging one.

- 2026-08-19 `kind-economy/t-016` — The two failure modes the task named -- under-remitting (promise broken) and double-remitting (money gone twice) -- turned out not to need any new schema or per-period tracking: because a remittance is meant to bring the running outstanding = accrued - remitted balance back to exactly zero, both collapse onto the sign of outstandingCents immediately after a remittance is logged (positive = under-remitted, negative = over-remitted/ likely duplicate, zero = reconciled). Read the existing t-010 accrual dashboard code first rather than assuming a new bucketing mechanism was needed -- the simplest correct design was already implied by the ledger shape that existed. Also caught mid-session: resolve_deps.py only edits the local working tree, it does not commit/push -- its output needs an explicit commit+PR+merge before claim_task.py will see the unblocked task on origin/main (worth remembering for any future session running it).

- 2026-08-19 `davinci/t-021` — Slice 9 fixed a real focus-loss bug (chapter-swap v-if/v-else-if unmounting the clicked button with nothing restoring focus), verified against a real, named precedent (model-builder-manager.vue's identical fix) rather than inventing a pattern from scratch. Separately, this cycle demonstrated the documented "in-flight git workaround" recovery path working as intended at a new scale: a first background agent pushed the implementation commit then died mid-run (API connection lost) before opening the PR. Rather than trusting an unseen report or re-doing the work blind, the foreground session checked live GitHub state directly (list_branches/list_commits) to confirm exactly one clean commit existed on the stranded branch, then dispatched a second worktree-isolated agent with explicit instructions to independently re-verify the diff's claims (not just trust the first agent's commit message) before finishing the PR+merge. Worth generalizing: when a background agent dies mid-task after a git-mutating step already landed, the recovery move is "verify live state, then dispatch a fresh agent to independently confirm and complete" -- not "assume it succeeded" and not "discard and redo from scratch."

- 2026-08-19 `kind-economy/t-009` — A new dashboard page's content/*.md frontmatter can declare background* art routes that verifyPageBackdrop.ts requires a matching PageSeed entry in stores/seeds/pageBackdropArtPrompts.ts for -- easy to miss in a sandbox with no live DB/browser to catch the 404 directly, but caught reliably by CI's contract check. Worth adding "does this page need a backdrop seed entry" to the standard pre-PR checklist for any task creating a new page.

- 2026-08-19 `kind-economy/t-008` — Clean first-pass Worker output on a genuinely ambiguous accounting task: the roadmap note left two real judgment calls open (a documented rounding rule for the 3-way split, and how to treat a per-transaction payment-processing fee when tokens are purchased in batches but spent fungibly later) and the Worker resolved both with a named constant, an inline rationale, and a 20,000-iteration property test proving the sum-to-gross invariant holds exactly including negative-margin rows -- rather than picking a plausible number and moving on. It also independently re-verified the task note's own claim ("costUsd is never reconciled against real billing") by grepping every gate.commit() call site itself instead of taking the note at face value, and surfaced it as a flagged follow-up rather than baking a false assumption into the schema doc comments. Reviewed the migration.sql line-by-line (additive CREATE TABLE + one FK only) before merging, per this repo's financial-ledger convention -- the Worker's own PR body correctly left the PR unmerged for exactly that reason instead of assuming a non-gate_human task meant no review was needed.

- 2026-08-19 `kind-economy/t-007` — Clean first-pass Worker output: additive-only migration (ADD COLUMN IF NOT EXISTS / CREATE INDEX matching the repo's established convention), a resolver that never throws (a lookup failure degrades to "no attribution" rather than failing the charge), and both open policy questions (mission-share fallback on unresolved creatorUserId, self-attribution recorded but not decided) handled exactly as the task note specified rather than guessed at. Reviewed the actual diff (schema, migration.sql, manaAttribution.ts, manaGate.ts wiring) rather than trusting the PR description alone.

- 2026-08-19 `kind-economy/t-005` — A flat "donate a third" plan does not net to zero for tax purposes by default -- gross receipts and a charitable deduction are separate line items whose offset depends entirely on entity type and itemization, and for a sole prop/LLC taking the standard deduction the offset is worth nothing. The fix has to be structural (keep the mission third out of gross receipts entirely via a direct customer-to-charity donation) rather than a bigger deduction. Also: when researching a compliance question, the framing in the task note ("check these N states") can undersell the real exposure -- a broader, newer category of law (California's charitable-fundraising-platform registration, which reads broadly enough to plausibly cover an embedded donate-at-checkout flow) was more directly on point than the originally-flagged commercial-co-venture states, and surfaced a concrete design lever (redirect to the donation platform's own hosted page vs. embedding it) worth flagging even though this task's scope was research-only.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-20T04:44:38Z_
