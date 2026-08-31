# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-31T13:06:55Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **844**
- Outcomes: blocked: 16, cancelled: 1, done: 827
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
| interface-vision | 95 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 54 | 98% |
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
| rainbow-butterflies | 15 | 100% |
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
| software | 828 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 15 |
| actionable | 12 |
| transient | 11 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-31 `rainbow-butterflies/t-013` — A prior session's claim on this task went stale (CLAIM_TTL_MINUTES expired) after 7 real implementation commits with no PR ever opened -- next_ready_task.py correctly surfaced it as reclaimable. Rather than re-implementing from scratch, fetched the actual worker/* branch, verified the existing diff was substantive real feature work (not scratch/placeholder), rebased it cleanly onto current main, fixed the lint/type issues it had never gotten past (eslint no-explicit-any and the resulting vue-tsc noUncheckedIndexedAccess fallout), and shipped it as kind_robots#2261. Preserving a stranded-but-real branch instead of discarding and redoing the work saved real effort and avoided a duplicate implementation. Also found the same session's CI run surfaced a genuinely broken base branch (Python test suite red on main from two malformed LEARNING.yaml records -- a YAML-breaking unescaped colon and an invalid failure_category enum value); root-caused and fixed both in a separate PR (#3316) rather than treating the failure as this PR's problem, confirming the fix by reproducing the original failure locally first.
- 2026-08-31 `interface-vision/t-104` — Slice 32 of the recurring kr-panel-flat consistency sweep -- pages/music-mentor.vue's feature-row div swapped hand-rolled "border border-base-300 bg-base-100" for the shared primitive, no geometry/behavior change; kind_robots#2256, 38/38 checks green. Also caught that check_pr_merged_drift.py's API-403 output was masking a genuine unreconciled gap, not just its usual unverifiable-transport false alarm: a separate, earlier slice (kind_robots#2253, Academy Timeline) had merged with zero note entry ever recorded for it. Cross-checked via the MCP connector rather than trusting the exit code alone, and backfilled the missing note before closing this cycle -- worth distinguishing "already reconciled, just can't verify from this sandbox" from "genuinely never reconciled" rather than assuming the former by default.
- 2026-08-31 `rainbow-butterflies/t-011` — A useful mission funnel can stay decision-grade without a visitor graph: bucket attribution into a fixed vocabulary, store event time only at the precision the decision needs, derive product activity from canonical records, and keep return-visit state browser-local instead of transmitting an identifier.
- 2026-08-31 `kind-robots/t-085` — A CI check flagging stale foreign-key-shaped ids (CHARACTER/BOT references in authored content batches) is worth checking against the live roster by name, not just id, before assuming a mechanical remap exists -- none of the 17 stale character names in this corpus existed anywhere in production's 240-row roster, meaning they were deleted/replaced outright rather than renumbered. When no remap exists and the content is voice-authored dialogue this session has no context for, pruning the specific violating items (rather than inventing new dialogue under time pressure) is the safer fix -- it gets CI green without risking a second round of creative-contract-shaped violations, and the dropped targets are recorded as a follow-up kaizen task (t-086) for a session that can invest in matching voice properly.
- 2026-08-31 `interface-vision/t-104` — Slice 80 of the recurring kr-panel-flat consistency sweep -- academy-timeline.vue's header and card-toggle surfaces swapped hand-rolled "border border-base-300 bg-base-100" for the shared primitive, no geometry/behavior change. Found via a fresh select_role.py run that flagged the sandbox's direct GitHub API calls all 403'ing (expected, MCP-only transport) but the underlying worker/reviewer signal was still readable once cross-checked against the MCP connector directly -- one open PR (kind_robots#2253), 37/37 checks green, posted a review-claim marker before merging per the rotation-collision protocol.
- 2026-08-31 `rainbow-butterflies/t-031` — A kaizen task that says "no new schema needed" is worth taking literally and verifying, not just trusting -- confirmed escalateHealthClaimFlagsIfNeeded() is the only code path that ever flips isPublic:false on a ToForum Chat row before building the admin queue query around that invariant, rather than adding a dedicated flag/reason column. Following an existing sibling admin review-queue (social-drafts) for the fetch/approve-reject store and page shape kept the new surface consistent with house style with no new conventions invented.
- 2026-08-31 `rainbow-butterflies/t-029` — A "prepare launch content" task with real health/malaria claims in scope is a sourcing task before it is a writing task -- fetching WHO's fact sheet and the AMF/AMI fundraiser page live (rather than recalling figures from training) surfaced that the fundraiser's donation total/net count is itself live and would go stale within hours, so the draft cites the WHO figures directly but points at the live fundraiser page as the source of truth instead of a point-in-time dollar figure. Restating an existing ethics/moderation contract as an operational runbook (mapping ETHICS.md's autonomous- vs-human-gated boundaries onto concrete triage steps) is worth doing as its own deliverable even with zero new policy -- the contract existed but no one had turned it into a checklist a moderator could follow directly.
- 2026-08-30 `dream-cycle/t-006` — A backlog bundle's built-data block being internally self-consistent (its own art-request IDs, facet_assignments, and Build log all agreeing with each other) is not proof it still matches live reality -- an earlier remaster/revision pass can silently overwrite a different, already-published bundle's rows, leaving the victim's file looking coherent while actually pointing at someone else's live content. The tell is only visible by fetching the live API and comparing title/slug/description against the file, not by reading the file in isolation. Added a catalog-wide (model, entity_id) uniqueness CI guard (scripts/audit_dream_record_identity.py) so a future recurrence surfaces as a red required check instead of silent drift.
- 2026-08-30 `rainbow-butterflies/t-025` — Grepping for the project's own existing restriction/audit primitives (User.isRestricted + notInRestricted, the Log-backed logAdminAction helper) before designing new moderation machinery found that restriction was already wired into most content models except the forum -- a real, narrowly-scoped security gap (writes and every read path never checked it) rather than something needing new schema. All of report/flag, restriction, rate-limiting, duplicate rejection, escalation, and audit trail landed additively with zero migrations.
- 2026-08-30 `rainbow-butterflies/t-030` — The { kind, id } resolver stayed additive for a second extension in a row (CHARACTER after ArtImage/Project) -- Chat.characterId and its relation already existed on the schema, so no migration was needed, confirming the shape was designed for growth rather than just working for its first two kinds.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-31T13:06:55Z_
