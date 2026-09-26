# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-26T14:02:07Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1153**
- Outcomes: blocked: 19, cancelled: 2, done: 1132
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 20 | 95% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 137 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 29 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-robots | 73 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 11 | 100% |
| mandarin-tutor | 14 | 93% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 23 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 44 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |
| tzaddik-gallery | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1136 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 42 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 42 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-26 `dream-cycle/t-034` — build_dream_proposal.py --from-json only ran validate_proposal (schema/invention/ title-shape/structural-repetition) -- it never called dream_prose_quality.complaints() or check_dream_creative_contract.py's entropy-version/premise-vocabulary-overlap/ name-diversity checks, so a proposal could pass a clean local --dry-run and only fail CI's check_dream_creative_contract.py --all-open job after being pushed (the 2026-09-29-gillstack kaizen this task came from). Fixed by adding creative_contract_complaints() to build_dream_proposal_core.py, mirroring check_dream_creative_contract.validate_path's checks exactly, and wiring it into --from-json: a real write is refused outright on failure (no partial write, matching CI's hard failure) while --dry-run still renders for inspection but reports the failure and returns non-zero. Scoped to --from-json only, not write_proposal/--sample generally, to avoid touching unrelated call sites the task didn't ask about. Needed lazy imports of author_dream_proposal/dream_prose_quality inside the new function (not at module top) because author_dream_proposal imports build_dream_proposal back (as `dreams`) -- a top-level import would have been circular at exec time, since build_dream_proposal_core.py's source is exec'd inside build_dream_proposal_impl.py's namespace before that namespace is fully populated.
- 2026-09-26 `tzaddik-gallery/t-002` — components/conductor/project-front-page.vue is a reusable page shell that already owns its own kr-surface root and kr-scroll region internally. Wrapping it inside a NEW pages/*.vue file's own template without giving that page file its own root-surface class and scroll region passes eslint/vue-tsc but fails utils/scripts/verifyLayoutContract.ts's root-surface/zero-scroll rules, because the checker scans each page-classified file's own template independently rather than resolving through child components -- and forcing it to pass by adding a second kr-scroll class at the page level would create a genuine nested-scroll region in the rendered DOM, not just satisfy the linter. A brand-new top-level route composing project-front-page needs either its own self-contained scroll wrapper (the music-mentor.vue shape, used here instead) or a documented exception; there is no existing precedent in this codebase of a real routed page reusing that shell as-is.
- 2026-09-26 `conductor/t-197` — A roadmap task block can carry a duplicate same-indent field key (found live in coloring-book/t-022: two `updated:` keys, one before `note:`, one after) that PyYAML silently resolves via last-key-wins, but set_task_field.py's field locator stopped at the first match and edited the wrong (shadowed) occurrence -- confirmed reproducing via this session's own claim_task.py/close_task.py calls against the live task. Neither validate_roadmaps.py nor verify_result() catches this class of drift, since both only check that a field is present somewhere, not that the edited occurrence is the effective one. Lesson: when a roadmap-editing tool assumes "the" field with a given name is unique within a mapping, that assumption should be enforced (raise on a duplicate) rather than silently relied on -- a line-oriented YAML editor that never re-parses the whole document before locating its target is exactly the shape of tool that can drift from what a real YAML parser would resolve.
- 2026-09-26 `storybook/t-069` — A new mechanical checker (verifyVerifierFilenameReferences.mjs, t-068) that ships with only a --self-test on synthetic strings can still be badly broken on real repo state -- running it for real, as part of wiring it into CI, found it flagging 16 lines across the actual utils/scripts/ directory (2 genuine stale doc references plus 14 false positives from self-test/.test.ts fixtures and a multi-line historical-context miss). Before wiring any new "scan every file for X" guard into CI, run it once against the real tree, not just its own unit self-test, since the self-test only proves the matching function works on hand-picked strings.
- 2026-09-26 `conductor/t-196` — set_task_field.py's ALLOWED_FIELDS is a single shared allow-list -- close_task.py's --set imports and gates through the exact same constant rather than keeping a second copy, so a field gap the task description worded as "extend both scripts" only needed one edit. Confirmed by reading close_task.py's own import line before touching anything, rather than assuming the docstring's "both scripts" implied two allow-lists to keep in sync.
- 2026-09-26 `conductor/t-195` — A recurring task's "status stuck at claimed" drift was not a write-atomicity bug in claim_task.py/close_task.py (both always write status+claimed_by+claimed_at together) -- it was a merge-conflict resolution that took origin/main's whole conflicted hunk instead of resolving per-task, discarding this task's own just-written status fix while correctly keeping an unrelated task's genuinely newer claim from the same hunk. The reliable mechanical check is the invariant itself (a claimed status with claimed_by/claimed_at both null can never come from a live claim), not parsing recurring-task note prose for "re-arming to ready".
- 2026-09-26 `kind-robots/t-123` — A repo-wide doc fix from a kaizen suggestion is worth doing in the same session even when it ranks below the top priority.yaml project -- the priority order picks which project to work when several have real ready work, it is not a rule against picking up a quick, reversible, already-scoped kaizen task once the higher-ranked project's only ready task is a recurring monitor that was already re-checked minutes earlier with no change.
- 2026-09-26 `kind-robots/t-122` — A stranded worker branch (implementation done, PR never opened because a prior session's create_pull_request call hit a connector write-safety block) is safe to open as-is without reimplementing -- but re-verify it against a full CI run before merging, not just the one purpose-built verifier the original author ran locally. CI caught a real gap the original commit missed -- verifyMaturityPrivacyContract.ts still pinned the pre-change "activeTab.value !== 'gallery'" substring the diff had removed, even though the author had already updated the sibling verifyGalleryProgressiveRendering.ts for the same rename. One file's test being updated is not evidence every file pinning the same string was.
- 2026-09-25 `animation-manager/t-007` — A background subagent asked to poll its own PR's CI and hand back when green can loop its SubagentHandback if it runs its own internal Monitor task -- tell it up front to cancel that Monitor before the final handback, not just to stop when done, or the coordinator ends up re-processing the same report repeatedly.
- 2026-09-25 `storybook/t-068` — A closed-review task with no implementation_pr recorded is invisible to merged-PR drift checks that hit a lookup failure elsewhere (here, an unrelated 403 on a same-task-id lookup in a different repo) -- always record implementation_pr at close-out time so a later drift check has something to verify against directly instead of falling back to a repo-guessing search.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-26T14:02:07Z_
