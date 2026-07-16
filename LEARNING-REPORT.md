# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-16T19:00:02Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **199**
- Outcomes: blocked: 12, done: 187
- Success rate: **94%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 17 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 18 | 100% |
| digital-storefront | 6 | 100% |
| dream-cycle | 10 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 3 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 22 | 95% |
| kindrobots-unraid | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 27 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 5 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 15 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 184 | 98% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 5 |
| quality | 3 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 5 occurrences; look for the shared cause across its records
- failure category `quality` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-16 `newsfeed/t-004` — When a design brief documents an "Audit findings" section with exact file paths and line numbers for the conventions a new module must follow (here: stores/helpers/<domain>.ts for types, a private safeGetLocalStorage/ safeSetLocalStorage pair per store instead of a shared util or DB table), trust it literally rather than re-deriving the pattern from scratch — it was written by a prior session that already did the archaeology. Attempting live verification of candidate external URLs before committing them (even when it fails, as it did here with a 403 from the sandbox's egress allowlist on every probe) is worth the two minutes: it turns "these RSS URLs are probably fine" into an explicit, auditable `verified: false` plus a follow-on task, instead of a silent assumption baked into the registry.

- 2026-07-16 `superkate-hairstyle-ai/t-017` — A task can be fully implemented and merged (kind_robots PR #317) while still sitting at roadmap status: claimed — the Reviewer sweep found it only by checking the open-PR list directly, not roadmap state. This is the second instance of a Silas-directed claude/* session finishing work without flipping the task through status: review first (see project TALKBACK 2026-07-10 entry); filed superkate-hairstyle-ai/t-020 to close the gap going forward.

- 2026-07-16 `global-ui/t-018` — Cross-repo kaizen tasks that extend an already-shipped computed pattern (here, t-015's doneTasksByMilestone done/active split) are cheapest to verify against the widest-blast-radius check available even when the change is tiny: running the full-project vue-tsc --noEmit (not just the touched file) caught that this environment's freshly-installed prettier version reformats unrelated pre-existing union-type lines on save, which would have silently expanded the diff's blast radius if not checked for and manually reverted before committing.

- 2026-07-16 `conductor/t-052` — When a kaizen task offers two design options and explicitly recommends the lighter one ("pick whichever is less roadmap-schema churn"), take that steer literally rather than re-litigating it — the append-only single-ledger design (EGRESS-BLOCKERS.md, mirroring TALKBACK.md's existing convention) needed zero roadmap.yaml schema changes and no new task fields, while the alternative (a `blocked_by_egress` task field) would have touched every affected task's schema for the same practical outcome. Verifying the new tool against a real known-good host (registry.npmjs.org) and a real known-blocked host (metmuseum.org) in the same session, rather than only unit-testing with mocks, caught that the sandbox proxy surfaces the block as an HTTPS CONNECT tunnel 403 (not a bare connection reset) — useful detail for the log line's `detail` text that a mocked-only test run would not have surfaced.

- 2026-07-16 `ai-art-academy/t-023` — A reusable lesson-scaffold beat (Try It / Reflect) can stay data-model-light by keying copy off an existing coarse field (remix.mode, prompt vs lora) instead of porting a large per-style table (teaching-notes.md's 21-row failure-mode list) into the TS seed — keeps the PR additive and scoped when the fine-grained data doesn't already live in the seed.
- 2026-07-16 `ai-art-academy/t-024` — A cross-file slug "mismatch" is not always a bug — verify each divergence individually before forcing exact-match; three of this file pair's divergences were intentional (an artist/technique-specific LoRA entry narrower than the general curriculum movement), so the right fix was a documented mapping table, not renaming slugs to force equality.
- 2026-07-16 `kind-robots/t-034` — When a lookaround-anchoring fix is applied to one token pattern in a file (t-030's bare-token pattern), sibling patterns in the same file sharing the old plain-\b anchoring (here, the extension-based runStepTokenPattern) should be audited in the same pass rather than deferred to a separate kaizen task — they share the identical failure mode.
- 2026-07-16 `ai-art-academy/t-020` — Curriculum-mirroring tasks (outline → academyStyles.ts) are cleanly landable without external egress when they only copy already-verified outline text; keep image-fetch work (t-008/t-013) split from pure data-mirroring work (t-020) so museum-egress blocks never stall the latter.
- 2026-07-16 `dream-cycle/t-005` — New backlog outlines must be cross-checked against ALL existing slugs/themes (seeds, daily proposals, home sets, parked cards) before naming to stay non-duplicative.
- 2026-07-16 `dream-cycle/t-009` — A delegating creation type's playbook should make the backlog card a pure scheduler/steering surface and explicitly forbid double-claiming a home task the Worker already holds.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-16T19:00:02Z_
