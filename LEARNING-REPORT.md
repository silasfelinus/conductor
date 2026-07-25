# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-25T23:04:09Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **340**
- Outcomes: blocked: 12, cancelled: 1, done: 327
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 36 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 10 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 14 | 100% |
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
| kind-robots | 31 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 31 | 100% |
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
| software | 325 | 99% |

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

- 2026-07-25 `model-builder/t-022` — The model-builder COMMIT executor's CREATE/ASSET_ONLY/idempotency paths (PR #190) had zero non-CI coverage (no test file, no live smoke) despite already backing gated reference runs t-016/t-017/t-018 -- a live prod round-trip (throwaway private/inactive Dream + Characters, cleaned up via DELETE after verification) was the only way to prove the idempotencyKey claim-then-write pattern and the isPublic/isActive=false override actually hold outside a type-checker. Also: GET /api/characters ignores a `?id=` query string and silently returns the unfiltered list -- the working per-id lookup is the path-param route GET /api/characters/{id}; worth knowing before the next live-smoke task on this surface.
- 2026-07-25 `animation-manager/t-014` — Existing invariant-verifier scripts need explicit CI wiring or real regressions can remain invisible until a developer happens to run them locally.
- 2026-07-25 `kind-robots/t-033` — A monitoring/recheck task with no recurring: true flag and no defined stopping criterion will keep surfacing as the highest-priority ready task in its project every time rotation lands there, even after the finding has been negative for a week straight (seven consecutive clean rechecks, 07-18 through 07-25, for kind-robots/t-033's Prisma cast-bypass sweep) -- each cycle burns a full rotation slot re-confirming the same zero-evidence result instead of doing new work. When a task's own note pattern is wait-for-new-evidence-recheck-meanwhile with no cadence limit, either mark it recurring: true (if the check itself is the ongoing value) or close it once repeated evidence makes the standing caution well-established, documenting that a genuine new instance should get a fresh task rather than reopening the closed one. Do not leave an indefinite-monitoring task at bare status: ready.
- 2026-07-25 `coloring-book/t-030` — A shared fallback value duplicated across many call sites (here: 14 ComfyUI job-builder seed generators all independently writing Math.floor(Math.random() * 1_000_000_000_000_000)) is a latent multi-site bug waiting for one schema constraint to expose it -- the seed column was a 32-bit Int the whole time, but nothing failed until real traffic hit it. When fixing this class of bug, grep for the literal/pattern across the whole repo before assuming a single call site is the only offender; a fix at one site while 13 siblings keep the same defect just delays the next incident.
- 2026-07-25 `animation-manager/t-007` — Local-only verification scripts (npm run test:animation-catalog, invoked from SPEC.md's shipping checklist but never referenced by any GitHub Actions workflow) can silently regress for days with zero signal, because nothing ever runs them except a session that happens to remember to. Caught this cycle only because building a new animation required running the script locally to verify the new catalog entry -- DEFAULT_PREFERENCES.startupEffect's 'random' sentinel had been failing verifyAnimationCatalog.ts's literal-catalog-id assertion since 2026-07-22 with no CI check ever red for it. Before trusting a 'ship only after X' checklist item, confirm X is actually wired into CI (grep the workflow YAML for the exact npm script name) rather than assuming a script's existence in package.json means it runs automatically.
- 2026-07-25 `model-builder/t-029` — Never hand-generate a base64 (or any binary-safe) encoding of file content as text output when pushing via a GitHub-file-write MCP tool -- an LLM cannot reliably reproduce an exact byte-for-byte encoding of a multi-KB file by 'typing' it, and a single wrong byte (here: a multi-byte × character mis-encoded, plus dropped indentation whitespace) silently corrupts the pushed file without any tool-level error. create_or_update_file's `content` parameter takes plain text directly and the server encodes it -- there is no need to hand-encode at all. Whenever a file-write tool's schema is ambiguous about raw-text-vs-pre-encoded, or after any push whose content you generated as long text rather than copied verbatim from a Read, fetch the pushed content back and diff it against the verified-correct source before treating the push as done, not after opening the PR.
- 2026-07-22 `ai-art-academy/t-010` — When widening an async-race token guard to cover a new code path, checking only the 'obviously stale' write is not enough -- every write inside the guarded block needs its own safety check. Fixing art-styler.vue's selectStarterEntry() to skip its selectedSourceImage write on a stale sourceSelectionToken almost shipped with the adjacent isLoadingStarterImage reset also gated on the same token, which would have permanently disabled every starter thumbnail (template binds :disabled to that flag) after any stale race, since no other code path resets it. Caught by reading the template's actual bindings for every ref touched in the guarded function, not just tracing the store/script logic -- a token guard is only correct once you've confirmed which of the block's several writes are actually invalidated by staleness and which need to run unconditionally regardless of which async call won.
- 2026-07-22 `sketchy/t-007` — The 'polish front-end' task template's channelKey wording can be wrong for a project without anyone noticing, because ProjectFrontConfig.channelKey (tutorialChannels.ts, e.g. 'wonder'/'builder'/'scenario') and dashboardHelper.ts's dashboardKey (e.g. 'academy') are two independent namespaces that sometimes share a value and sometimes don't -- sketchy's task note and its own -page.vue both said 'academy' for the tutorial-channel field, copying the (correct, but different-system) dashboardKey value, and the mistake was invisible until checked against TutorialChannelKey's actual union. Before writing a tutorialChannels.<key>.sections entry from a roadmap note, verify <key> actually exists in stores/helpers/tutorialCards.ts rather than trusting the note's channel name -- cross-check the project's physical content/channels/<x>/*.md siblings (which tutorialChannels key do they use?) when in doubt.
- 2026-07-22 `conductor/t-079` — audit_roadmaps.py's yaml.safe_load could not see duplicate keys within a single task mapping, so a stale trailing owner/claimed_by/updated value could silently override the real one under YAML's last-key-wins semantics (root cause of the ai-art-academy/t-010 stale-claim incident). Fixed by adding a SafeLoader subclass that collects (not raises on) every duplicate key per mapping, wired into audit_roadmaps.py as a DUPLICATE_YAML_KEY finding, then fixing all 11 pre-existing instances across conductor/global-ui/kind-robots/packmaker after reading context to determine which duplicate value was actually correct rather than mechanically keeping first-or-last. Bundled all 4 projects' fixes into one PR instead of 4 separate claimed tasks (as the original note suggested) since a solo session showed no concurrent-edit risk and splitting would have left the audit tool reporting stale findings against 3 files between PRs -- judgment call, documented in the task note and TALKBACK for later audit.
- 2026-07-21 `animation-studio/t-001` — A hand-rolled ready-task scan (used to pick a rotation target instead of next_ready_task.py's priority-order pick) computed the active-project set from project-overrides.yaml but never filtered the priority.yaml walk by it, so a retired project (animation-studio, superseded by animation-manager) surfaced a claimable ready task. Caught before any PR opened, via audit_roadmaps.py's project-inventory table showing the retired status -- run that check (or grep the specific project's status: line) as the last step immediately before claim_task.py, not just earlier in a broad sweep. claim_task.py itself has no active/retired guard.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-25T23:04:09Z_
