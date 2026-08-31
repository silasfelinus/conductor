# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-31T04:31:01Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **838**
- Outcomes: blocked: 16, cancelled: 1, done: 821
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
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 87 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 41 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 20 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 93 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 53 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 9 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 12 | 100% |
| ruler-hooked | 11 | 100% |
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
| software | 822 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 12 |
| transient | 11 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-31 `rainbow-butterflies/t-029` — A "prepare launch content" task with real health/malaria claims in scope is a sourcing task before it is a writing task -- fetching WHO's fact sheet and the AMF/AMI fundraiser page live (rather than recalling figures from training) surfaced that the fundraiser's donation total/net count is itself live and would go stale within hours, so the draft cites the WHO figures directly but points at the live fundraiser page as the source of truth instead of a point-in-time dollar figure. Restating an existing ethics/moderation contract as an operational runbook (mapping ETHICS.md's autonomous- vs-human-gated boundaries onto concrete triage steps) is worth doing as its own deliverable even with zero new policy -- the contract existed but no one had turned it into a checklist a moderator could follow directly.
- 2026-08-30 `dream-cycle/t-006` — A backlog bundle's built-data block being internally self-consistent (its own art-request IDs, facet_assignments, and Build log all agreeing with each other) is not proof it still matches live reality -- an earlier remaster/revision pass can silently overwrite a different, already-published bundle's rows, leaving the victim's file looking coherent while actually pointing at someone else's live content. The tell is only visible by fetching the live API and comparing title/slug/description against the file, not by reading the file in isolation. Added a catalog-wide (model, entity_id) uniqueness CI guard (scripts/audit_dream_record_identity.py) so a future recurrence surfaces as a red required check instead of silent drift.
- 2026-08-30 `rainbow-butterflies/t-025` — Grepping for the project's own existing restriction/audit primitives (User.isRestricted + notInRestricted, the Log-backed logAdminAction helper) before designing new moderation machinery found that restriction was already wired into most content models except the forum -- a real, narrowly-scoped security gap (writes and every read path never checked it) rather than something needing new schema. All of report/flag, restriction, rate-limiting, duplicate rejection, escalation, and audit trail landed additively with zero migrations.
- 2026-08-30 `rainbow-butterflies/t-030` — The { kind, id } resolver stayed additive for a second extension in a row (CHARACTER after ArtImage/Project) -- Chat.characterId and its relation already existed on the schema, so no migration was needed, confirming the shape was designed for growth rather than just working for its first two kinds.
- 2026-08-30 `rainbow-butterflies/t-023` — An extensible typed reference shape ({ kind, id }) for cross-object embeds paid off immediately -- ArtImage and Project shared one resolver/serializer path with no per-kind schema branching, so the next object kind (t-030) is additive rather than a redesign.
- 2026-08-30 `rainbow-butterflies/t-022` — Companion API/discovery work should close only after both implementations are merged and task-specific contracts are verified separately from unrelated base-repository data failures.
- 2026-08-30 `interface-vision/t-104` — Slice 64 (kind_robots#2224) picked up the ~150-instance kr-note status-callout pool flagged exhausted-of-easy-wins by slice 62: found a sub-pool of 8 instances across 5 files that already matched the canonical border-{status}/40 bg-{status}/10 opacity values but omitted font-semibold, and used a trailing font-normal override to convert them without silently adding weight that wasn't there before. Also surfaced and correctly excluded a look-alike but unsafe sub-pool: several admin/*.vue "admin access required" gate panels share the same border+bg color classes but wrap a heading with no explicit text color of its own -- converting the wrapper would recolor the heading via CSS inheritance, a real visual change disguised as a mechanical one. Checking whether a matching-color-class instance's text color is stated explicitly (vs. inherited from the wrapper) is now a general filter worth applying before any kr-note/kr-panel conversion, not just this pool.
- 2026-08-30 `rainbow-butterflies/t-020` — forum-thread.vue had drifted entirely off the canonical /api/v1/forum/* endpoints onto a legacy chatStore path with a hardcoded, wrong channel list and an unimplemented reply handler -- the backend (server/utils/forumApi.ts) was already built and unused by any client. Worth checking, before starting a "build X" task, whether the backend already exists and only the frontend wiring is missing; the task note's own framing ("let humans and agents post through the same API") was the tell that a real API already existed to point at. Also: not every authorship kind a task note names has to be invented in the same slice -- HUMAN_AI and SYSTEM had no schema/backend concept behind them, so they were flagged as a follow-up needing a product decision rather than guessed at.
- 2026-08-30 `interface-vision/t-104` — Slice 63 (kind_robots#2220) was a clean, exact-match kr-panel substitution on project-front-page.vue's two raised-surface sections, following the same override convention prior slices established (kr-panel + trailing rounded-3xl/p-5 overrides for values that differ from kr-panel's rounded-2xl/p-6 defaults). Verified the CSS definition (assets/css/tailwind.css .kr-panel) before merging to confirm the override convention actually produces the same computed classes, rather than trusting the PR description's claim alone.
- 2026-08-30 `interface-vision/t-104` — Slice 62: the kr-note family (border-{status}/N + bg-{status}/M + text-{status}) is a much bigger candidate pool (~150+ raw grep hits) than any prior mechanical sweep, but padding/opacity/text-size/font-weight vary too widely across it to convert blindly -- unlike kr-container/kr-surface/kr-panel-flat, where near-total instances matched the canonical shape exactly. Scoping the slice to only instances where every differing attribute was explicit in the original class list (never inferring an ambient/inherited text-size or font-weight) kept the substitution provably byte-for-visual-identical at the cost of converting only 7 of ~150 instances this slice. Also worth noting: a family of otherwise-identical pills/badges sharing one non-kr-note color (stage-manager.vue's primary/success/warning trio) should be skipped as a set rather than partially converted, since fixing two of three fragments what was a visually consistent group.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-31T04:31:01Z_
