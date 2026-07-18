# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-18T01:07:40Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **252**
- Outcomes: blocked: 12, done: 240
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
| conductor | 33 | 100% |
| digital-storefront | 9 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 9 | 100% |
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
| software | 237 | 99% |

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

- 2026-07-18 `conductor/t-063` — A plain YAML scalar containing an unescaped colon+space (e.g. a parenthetical like "(confirmed here: 9 minutes later)") is invalid mid-value -- always quote or block-scalar a hand-appended lesson/note field with any ': ' in it. Also: before implementing a task note's suggested root cause, verify it against the actual code path -- the note assumed the live append writer needed a quoting fix, but it already auto-quotes via yaml.safe_dump; the real bad entry was a hand-appended plain scalar that bypassed that writer entirely.
- 2026-07-18 `ai-art-academy/t-031` — When a recurring never-idle task (t-010) files a small, concrete, independently-landable follow-up task, prefer claiming that follow-up over re-running the recurring task again the same rotation -- it's real shippable work instead of another lane pass.
- 2026-07-17 `conductor/t-062` — When de-flaking a red-CI detector's cancelled-run false positive, compare against the branch's latest run of ANY status, not just the latest completed one -- the superseding run frequently hasn't finished yet at the moment the detector polls (confirmed here: 9 minutes later), so a completed-only comparison would still miss the exact race it's meant to catch.
- 2026-07-17 `coloring-book/t-022` — Two workflows sharing a mutable resource (queue file + single-worker render backend) need the SAME concurrency.group, not just any group — a uniquely-named group only prevents self-collision, not collision with a sibling workflow hitting the same backend in parallel.
- 2026-07-17 `conductor/t-061` — git commit-tree does not inherit commit.gpgsign the way porcelain git commit does -- any direct-to-ref plumbing helper that signs on this repo's behalf needs an explicit -S read from git config, or every commit it makes silently lands Unverified despite full signing config being present.
- 2026-07-17 `packmaker/t-010` — Reusing an established hermetic-VM contract-test pattern (t-008's validatePackManifest test) for a sibling function made a same-cycle kaizen pickup fast and low-risk — the one wrinkle was that assert.deepEqual on objects returned from vm.runInNewContext fails on cross-realm prototype mismatch even when data is structurally identical; round-trip through JSON.parse(JSON.stringify(...)) to normalize before comparing.
- 2026-07-17 `packmaker/t-009` — A cross-cutting infra fix (suggest providers hardcoding max_tokens 512) surfaced naturally while building one feature's LLM call — landing it in the same PR benefited every suggest caller instead of needing a separate follow-up task.
- 2026-07-17 `digital-storefront/t-024` — Clean first-pass auth fix mirroring an existing correct sibling endpoint (cancel-subscription.post.ts) — copying a proven pattern in the same file family is a reliable way to close a security kaizen quickly.
- 2026-07-17 `packmaker/t-008` — Pure logic embedded in a Nuxt store may not import cleanly in lightweight CI; execute the exact source in a hermetic TypeScript VM or extract it into a dependency-light module rather than mocking or copying the implementation.
- 2026-07-17 `ai-art-academy/t-013` — A soft needs-human task blocked purely by a connector limitation (full-blob-only file replacement risking truncation) is not the same as a task blocked by missing data — the handoff doc already had fully sourced, license-verified, byte-exact content ready to apply. Any later session with a real local git checkout of the target repo should treat such a handoff as directly actionable, not re-park it at needs-human.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-18T01:07:40Z_
