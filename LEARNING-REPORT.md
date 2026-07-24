# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-24T00:57:29Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **334**
- Outcomes: blocked: 12, cancelled: 1, done: 321
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 36 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 8 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 47 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 30 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 29 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 319 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 7 |
| quality | 6 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 7 occurrences; look for the shared cause across its records
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-22 `ai-art-academy/t-010` — When widening an async-race token guard to cover a new code path, checking only the 'obviously stale' write is not enough -- every write inside the guarded block needs its own safety check. Fixing art-styler.vue's selectStarterEntry() to skip its selectedSourceImage write on a stale sourceSelectionToken almost shipped with the adjacent isLoadingStarterImage reset also gated on the same token, which would have permanently disabled every starter thumbnail (template binds :disabled to that flag) after any stale race, since no other code path resets it. Caught by reading the template's actual bindings for every ref touched in the guarded function, not just tracing the store/script logic -- a token guard is only correct once you've confirmed which of the block's several writes are actually invalidated by staleness and which need to run unconditionally regardless of which async call won.
- 2026-07-22 `sketchy/t-007` — The 'polish front-end' task template's channelKey wording can be wrong for a project without anyone noticing, because ProjectFrontConfig.channelKey (tutorialChannels.ts, e.g. 'wonder'/'builder'/'scenario') and dashboardHelper.ts's dashboardKey (e.g. 'academy') are two independent namespaces that sometimes share a value and sometimes don't -- sketchy's task note and its own -page.vue both said 'academy' for the tutorial-channel field, copying the (correct, but different-system) dashboardKey value, and the mistake was invisible until checked against TutorialChannelKey's actual union. Before writing a tutorialChannels.<key>.sections entry from a roadmap note, verify <key> actually exists in stores/helpers/tutorialCards.ts rather than trusting the note's channel name -- cross-check the project's physical content/channels/<x>/*.md siblings (which tutorialChannels key do they use?) when in doubt.
- 2026-07-22 `conductor/t-079` — audit_roadmaps.py's yaml.safe_load could not see duplicate keys within a single task mapping, so a stale trailing owner/claimed_by/updated value could silently override the real one under YAML's last-key-wins semantics (root cause of the ai-art-academy/t-010 stale-claim incident). Fixed by adding a SafeLoader subclass that collects (not raises on) every duplicate key per mapping, wired into audit_roadmaps.py as a DUPLICATE_YAML_KEY finding, then fixing all 11 pre-existing instances across conductor/global-ui/kind-robots/packmaker after reading context to determine which duplicate value was actually correct rather than mechanically keeping first-or-last. Bundled all 4 projects' fixes into one PR instead of 4 separate claimed tasks (as the original note suggested) since a solo session showed no concurrent-edit risk and splitting would have left the audit tool reporting stale findings against 3 files between PRs -- judgment call, documented in the task note and TALKBACK for later audit.
- 2026-07-21 `animation-studio/t-001` — A hand-rolled ready-task scan (used to pick a rotation target instead of next_ready_task.py's priority-order pick) computed the active-project set from project-overrides.yaml but never filtered the priority.yaml walk by it, so a retired project (animation-studio, superseded by animation-manager) surfaced a claimable ready task. Caught before any PR opened, via audit_roadmaps.py's project-inventory table showing the retired status -- run that check (or grep the specific project's status: line) as the last step immediately before claim_task.py, not just earlier in a broad sweep. claim_task.py itself has no active/retired guard.
- 2026-07-21 `superkate-services-calculator/t-037` — dart:io real filesystem work (temp-dir creation, real file writes) inside a testWidgets body can hang indefinitely under flutter_test's FakeAsync zone -- wrap it in tester.runAsync() (with a bounded tester.pump() poll loop for the async completion signal) rather than assuming a widget test's async gaps are always safely fake-clock-driven. A test that genuinely needs real I/O will hang to CI's timeout, not fail fast, so a hang in a shared multi-app CI job can look like it's blocking an unrelated app's PR.
- 2026-07-21 `conductor/t-077` — This session's designated git-push transport (http://127.0.0.1:41729 relay) 413'd on every plain `git push` to its own session branch -- even a brand-new throwaway branch with a 1-byte diff and a ~59KB pack -- while pushing directly to `main` via claim_task.py's git-plumbing helper worked fine. This doesn't match either of CLAUDE.md's two documented HTTP-413 causes (new-ref full-pack, post-rebase force-push). Workaround that eventually worked: retry the SAME single-file git-plumbing commit approach (scratch index + commit-tree + `git push <sha>:<ref>`) against the session branch itself, not just main -- it succeeded where a bulkier `git push -u origin <branch>` failed, before falling back to the heavier push_files MCP tool. Separately: when relaying a large file's full content through push_files (no diff/patch mode exists), ALWAYS diff the pushed remote content byte-for-byte against the local working tree immediately after (e.g. `git show origin/<branch>:<path> | diff - <local-path>`) before trusting it -- a transcription slip during one such relay silently dropped a clause from one note field, and a later slip (pasting an incomplete draft) briefly truncated the entire 2198-line roadmap.yaml to just its 22-line header, discovered only because this verification step is now habitual. Both were caught and fixed before the PR was even opened, with zero cost to Silas -- but only because verification happened immediately, not after moving on.
- 2026-07-21 `sketchy/t-008` — A project's milestones can show every spec task as done while nothing has actually been built against those specs -- check milestone status against real code state (does the app scaffold still show generated boilerplate?), not just task-list completion, before assuming a project has no available work. Also: app-ci.yml tests every app in apps/ within one shared job whenever its changed-app diff detection doesn't isolate to a single app, so an unrelated app's flaky/hung test can make an otherwise-clean PR's CI look broken -- read the full job log for which app actually failed before assuming your own diff caused it; a test that passes cleanly in the first few seconds of a job that then hangs for 10 more minutes on a different app's test file is not your regression.
- 2026-07-21 `davinci/t-014` — set_task_field.py edits whatever is on the caller's local working tree, unlike claim_task.py which fetches origin/main fresh and pushes via git plumbing -- calling set_task_field.py right after claim_task.py in the same session without an intervening fetch+ff-only can silently reapply a stale claimed_by/claimed_at (or any other field) on top of the real claim. Always fetch and fast-forward the local branch before any set_task_field.py call that follows a claim_task.py call. Separately: hand-appending a new paragraph to a folded (>) YAML note: field needs a blank line between paragraphs, not just a newline -- YAML's folded-scalar rule collapses adjacent non-blank lines into one line with a space, so a missing blank line silently merges the new paragraph into the previous one on next parse. Verify by re-parsing the note and diffing paragraph-boundary bytes, not by eyeballing the raw text diff.
- 2026-07-21 `ai-art-academy/t-036` — A recurring rotation task (t-010) can strand a green, unmerged kind_robots PR at session end if the completion checklist only names the terminal-state requirement generically instead of listing 'poll CI and merge (or explicitly park) before the cycle ends' as its own explicit bullet -- this had already happened twice (PR #942, PR #814) under slightly different framings before it was made an explicit, lane-agnostic checklist item. When a recurring task's own history shows the same failure shape twice, generalize the fix beyond the specific lane/step where it was first noticed, since the underlying gap (an implicit 'PR opened' being mistaken for 'cycle done') can recur on any lane that opens a PR.
- 2026-07-21 `conductor-app/t-012` — Before assuming a feature needs new backend endpoints, check what the existing API already returns/accepts -- GET /api/dreams/:id already embedded up to 12 linked ArtCollections with up to 12 ArtImages each, and POST /api/conductor/art-request already existed pre-built and admin-gated, so the whole task (ArtCollection browsing + admin art-request form) was pure Flutter client work with zero kind_robots changes needed. Also: a sandboxed toolchain pinned to a fixed version can silently drift stale against CI's unpinned 'stable' channel and produce false-positive analyze errors (including on files never touched this cycle) -- when a fresh error appears on pre-existing code, suspect the toolchain version before the diff, and verify against the actual current stable before trusting the result.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-24T00:57:29Z_
