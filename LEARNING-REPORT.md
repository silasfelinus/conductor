# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-28T22:23:25Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **414**
- Outcomes: blocked: 13, cancelled: 1, done: 400
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 55 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 12 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 21 | 100% |
| conductor | 55 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 16 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 9 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 37 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
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
| software | 399 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 9 |
| quality | 7 |
| transient | 6 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `quality` — 7 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-28 `media-watchlist/t-016` — Confirms the t-015 lesson: select_role.py reported candidate_reviewable_pr_count: 0 and github_api_unreachable: true, but mcp__github__list_pull_requests/pull_request_read found this claude/* PR (and its kind_robots counterpart) fully green and ready to merge. A prior session did the implementation and left status: review with a clear PROGRESS note; this session only needed to verify CI and merge both PRs in order (implementation repo first, then the conductor tracking PR), matching the "Notes for reviewer" instructions left in the PR body.
- 2026-07-28 `media-watchlist/t-015` — select_role.py's direct api.github.com calls keep 403ing in this sandbox (recurred 3+ times same day); always cross-check with mcp__github__list_pull_requests directly before trusting a "0 reviewable PRs" result. Also confirmed: GET /api/media-entries already supported an unfiltered take/sort call for free (every filter param is optional and simply omitted when unset) -- worth checking existing route flexibility before assuming a backend change is needed for a "fixed global view" spec.
- 2026-07-28 `model-builder/t-029` — Before dispatching a fresh explore-and-fix pass, actually run any regression guard a prior cycle's kaizen suggestion produced (e.g. verifyModelBuilderLinkCoverage.ts) rather than trusting the roadmap note's "unconfirmed" framing -- it may already be closed by an intervening task chain. Also: singleton-ownership-race fixes (guarding concurrent in-flight state) and stage-approval-gate fixes (guarding against overwriting already-reviewed/settled state) are distinct bug classes in this store -- batchDraftField/ batchSetField needed the latter, not another instance of the former.
- 2026-07-28 `coloring-book/t-036` — Distinguishing a credential-wall semantic_gate_error (ANTHROPIC_API_KEY is required) from a recoverable job-timeout or transient-enqueue one by message content -- rather than lumping all semantic_gate_error entries into one retry_safe check -- lets automation short-circuit "don't bother retrying, it's the same infra gate" instead of a human/agent re-deriving it from raw queue state each cycle.

- 2026-07-28 `model-builder/t-035` — Extending an existing schema-relation-vs-config-eligibility guard for a second failure direction (join-table-only relation claimed as CREATE-linkable) is clean on the first functional pass, but a naive "any model referencing both types" join-table heuristic false-positives on broad hub models (ArtImage) -- require the actual structural signature real join tables use in this schema (@@id([...]) composite key) before accepting a match. Separately: a green vue-tsc run does not guarantee a green CI, since this repo also runs a heuristic (non-type-checking) capture-group-guard linter that only recognizes specific guard shapes textually -- read that linter's own source for its recognized shapes rather than guessing when it flags new code TypeScript itself accepted.
- 2026-07-28 `coloring-book/t-035` — Clean first-pass fix, same shape as t-032's recovery-path fix but for the fresh-submission branch of the same loop: record_semantic_gate_error() now stamps the newly enqueued ArtJob's id onto the stored error whenever the message does not already carry a "job N" reference, so a missing-credential verification failure after a successful render stays recoverable instead of forcing a duplicate resubmission. Mirrors t-032's own regression test shape closely enough that reusing that test as a template for the new fresh-submission case caught the right edge cases (double-stamp avoidance, enqueue()-failure leaving the field unstamped) on the first attempt.
- 2026-07-28 `ai-art-academy/t-052` — Closed without a separate diff -- its content (PUBLIC-DOMAIN-POLICY.md §1.3 vs §2 distinction) shipped in the same continuous-improvement-checklist.md edit as t-051 (PR #1344). See t-051's record for the reusable lesson about combining same-paragraph kaizen tasks.
- 2026-07-28 `ai-art-academy/t-051` — Small kaizen-generated checklist tasks (t-051, t-052) that land in the same rotation-instructions paragraph are cheaper to merge as one edit than as two sequential PRs -- worth checking a freshly filed kaizen task against other open kaizen tasks for the same project before implementing, in case they share a landing spot.
- 2026-07-28 `ai-art-academy/t-050` — Passing PUBLIC-DOMAIN-POLICY.md paragraph 1.3 (artist died 70+ years ago AND work predates the US cutoff year) does not guarantee an institution has released an accepted-license image under paragraph 2 -- these are separate checks. A prior cycle added Fauvism to academyStyles.ts reasoning only from paragraph 1.3 (Matisse/Derain/Dufy all clear the death-date threshold, core works 1904-1908 well before 1930), which is fully valid for that entry's actual use (prompt-only style reference under paragraph 4 rule 1, no displayed artwork image) but does not by itself clear the stricter bar this curriculum doc's "Example works" require. Direct Met/AIC API queries this cycle found a verified public-domain Matisse work (Still Life with Geranium, 1906, AIC object 87045) but zero for Derain or Dufy despite both clearing paragraph 1.3 with equal margin -- every institution-held Fauvist-period Derain/Dufy work checked came back isPublicDomain/is_public_domain: false. Lesson: always run the per-work museum-API check before treating a death-date-cleared artist as curriculum-ready, and ship with fewer verified example works rather than assume prong-1 clearance implies image availability.
- 2026-07-28 `model-builder/t-034` — Kaizen-chain closeout: t-033 exposed t-034 (Facet recipe chip visibly selectable but functionally empty), and this task closed cleanly first pass by checking Prisma schema relations directly rather than guessing -- DreamFacet/ ScenarioFacet are tag-attachment joins, not parent->child creation links, so dropping relationship-expansion from Facet was correct over fabricating a fake relation. kind_robots PR #1108 (7/7 checks green) merged same cycle as the conductor bookkeeping close-out.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-28T22:23:25Z_
