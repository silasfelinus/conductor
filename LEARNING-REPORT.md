# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-18T05:22:20Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **256**
- Outcomes: blocked: 12, done: 244
- Success rate: **95%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 27 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 34 | 100% |
| digital-storefront | 11 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 10 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 26 | 96% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 16 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 241 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-18 `digital-storefront/t-017` — A design task blocked on two cross-project note-level dependencies (invisible to resolve_deps.py/claim_task.py, which only check in-project depends_on) should re-verify each blocker's live status directly before claiming, per CONTROL.md's cross-project-collision note -- both packmaker/t-003 and kind-robots/t-008 were genuinely done here, but the task's own note explicitly warned not to trust the resolver's blind promotion.
- 2026-07-18 `conductor/t-055` — yaml.safe_dump round-tripping a human-edited YAML file silently strips every comment and blank-line separator on write -- any registration/patch helper that touches a file agents don't exclusively own (priority.yaml, project-overrides.yaml) should do targeted text-surgery (regex/line insertion, mirroring register_control_block) instead of load-mutate-dump, even when the mutation itself is a one-line append.
- 2026-07-18 `global-ui/t-024` — A DB-record fallback path that reuses the same rendered field/badge as the primary conductor-sourced path needs an explicit provenance flag (hasConductorTaskCounts), not just a truthiness guard on the value itself -- a zero-but-real-conductor-count and a nonzero-but-wrong-source count both need distinct handling, and .length/truthiness on the value alone can't tell them apart.
- 2026-07-18 `digital-storefront/t-018` — A task's in-file depends_on note can go stale in a good way, not just a bad one -- t-017/t-018 both carried explicit 'do not trust the resolver, verify these cross-project blockers by hand' warnings written when the blockers were genuinely unmet; by the time this cycle picked t-018 up, every named blocker (coloring-book t-006/t-007/t-009, kind-robots t-008, packmaker t-003) had independently reached done. Always re-check cited blockers live before either claiming or reverting a resolver-promoted task -- the warning note itself can be outdated.
- 2026-07-18 `conductor/t-063` — A plain YAML scalar containing an unescaped colon+space (e.g. a parenthetical like "(confirmed here: 9 minutes later)") is invalid mid-value -- always quote or block-scalar a hand-appended lesson/note field with any ': ' in it. Also: before implementing a task note's suggested root cause, verify it against the actual code path -- the note assumed the live append writer needed a quoting fix, but it already auto-quotes via yaml.safe_dump; the real bad entry was a hand-appended plain scalar that bypassed that writer entirely.
- 2026-07-18 `ai-art-academy/t-031` — When a recurring never-idle task (t-010) files a small, concrete, independently-landable follow-up task, prefer claiming that follow-up over re-running the recurring task again the same rotation -- it's real shippable work instead of another lane pass.
- 2026-07-17 `conductor/t-062` — When de-flaking a red-CI detector's cancelled-run false positive, compare against the branch's latest run of ANY status, not just the latest completed one -- the superseding run frequently hasn't finished yet at the moment the detector polls (confirmed here: 9 minutes later), so a completed-only comparison would still miss the exact race it's meant to catch.
- 2026-07-17 `coloring-book/t-022` — Two workflows sharing a mutable resource (queue file + single-worker render backend) need the SAME concurrency.group, not just any group — a uniquely-named group only prevents self-collision, not collision with a sibling workflow hitting the same backend in parallel.
- 2026-07-17 `conductor/t-061` — git commit-tree does not inherit commit.gpgsign the way porcelain git commit does -- any direct-to-ref plumbing helper that signs on this repo's behalf needs an explicit -S read from git config, or every commit it makes silently lands Unverified despite full signing config being present.
- 2026-07-17 `packmaker/t-010` — Reusing an established hermetic-VM contract-test pattern (t-008's validatePackManifest test) for a sibling function made a same-cycle kaizen pickup fast and low-risk — the one wrinkle was that assert.deepEqual on objects returned from vm.runInNewContext fails on cross-realm prototype mismatch even when data is structurally identical; round-trip through JSON.parse(JSON.stringify(...)) to normalize before comparing.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-18T05:22:20Z_
