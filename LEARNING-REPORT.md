# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-17T07:49:14Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **218**
- Outcomes: blocked: 12, done: 206
- Success rate: **94%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 19 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 24 | 100% |
| digital-storefront | 6 | 100% |
| dream-cycle | 13 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 7 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 24 | 96% |
| kindrobots-unraid | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 27 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 5 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 15 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 203 | 99% |

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

- 2026-07-17 `global-ui/t-020` — Clean first-pass extraction of a shared component from two already-drifted copies: scoping the refactor to exactly the duplicated card (leaving the unrelated KAIZEN-category markup in conductor-page.vue untouched) kept the diff small and the CI green on the first try across both repos (kind_robots PR #344, conductor PR #678).

- 2026-07-17 `kind-robots/t-036` — A hermetic test's synthetic fixture data can itself trip a secret scanner if it's shaped like a real credential literal (mysql://user:pass@host) or uses a trigger-word identifier (a const literally named *PASSWORD*) even though it's fake test data. Assemble such fixtures from named constants via template literals (or .join for delimiter-containing pieces) rather than one quoted literal, and avoid secret-suggestive identifier names, to dodge false positives before they cost a round trip. Also: once a flagged literal lands in any commit, GitGuardian scans the whole PR's commit range, so a follow-up commit that removes it does not clear the check on its own — squash/rebase so the flagged text never appears in history.

- 2026-07-17 `kind-robots/t-032` — Task was claimed/worked under owner: reviewer even though it was implementation work (a doc PR), which the Security Model reserves for Worker. Harmless here since the output was correct and merged clean, but future burst-mode sessions doing doc/code work should claim as owner: worker regardless of which role slot the session is labeled.
- 2026-07-17 `global-ui/t-021` — A Worker session that just shipped a task can independently notice and fix a same-cycle staleness issue faster than the Reviewer can file and route a kaizen task for it -- kind_robots PR #340 landed 8 seconds after PR #338 merged, before the kaizen task even reached origin/main. No process gap here, just worth remembering that fast same-session follow-ups can outrun roadmap bookkeeping; check open PRs again after any merge before assuming the sweep is complete.
- 2026-07-17 `global-ui/t-017` — When a Worker session claims a task whose seed data references another in-flight task (t-017's manifest pointed at t-014 via acknowledgedGap), check whether the referenced task landed on main in the interim before merging — it may have shipped a real target (t-014's /for-you nav entry) that should replace the placeholder gap outright, saving a follow-up cycle.
- 2026-07-17 `global-ui/t-014` — kind_robots has two distinct Nuxt Content collections that both accept the same frontmatter shape (content.config.ts: "content" excludes channels/**, "channels" sources only channels/**) — a top-level content/*.md file is the real routable page, while content/channels/<key>/*.md is nav metadata only. Both commonly reuse the same tabKey. Easy to mistake for accidental duplication; confirm against content.config.ts before assuming a bug. New top-level nav surfaces need one file in each collection.
- 2026-07-16 `dream-cycle/t-016` — A multi-write build against an intermittent DB must be atomic: track created row ids and roll them back (DELETE, newest-first) on ANY failure, never mark a partial build complete. Bailing only on total failure silently ships incomplete, un-retried records during blips.
- 2026-07-16 `ai-art-academy/t-026` — Kaizen-verification tasks (diff-checking an adapted/paraphrased backfill against its cited source) are a cheap, high-value rotation pick when the project's primary task is egress-blocked — conductor#656 closed clean with zero drift found across 21 entries, no kind_robots PR needed. Missing from that PR: no LEARNING.yaml entry on close (added here by the merging Reviewer) — closing agents should append the ledger record in the same PR that sets status: done, not leave it for review to backfill.
- 2026-07-16 `ruler-hooked/t-011` — A vocab-drift guard for prose design docs should flag only code-token variants (far-shore/farshore for far_shore) not spaced prose ("far shore"), and must match camelCase tokens case-SENSITIVELY so the correct regionOverride does not match its own lowercased variant. Validate art-prompts inspirations against the exact field distribute_images.py reads (image_path), not a guessed schema.
- 2026-07-16 `ruler-hooked/t-003` — Check whether the target already exists before "creating" it — the kind_robots Project (id 95, conductorSlug=ruler-hooked) already existed, so t-003 reduced to setting goal. Record the friendly goal in the roadmap top-level `goal:` field (sync_projects.py source of truth) rather than only PATCHing live, so it survives a transient DB-write 503 and backfills on the next sync. Reads can succeed while writes 503 — "db is up" is not binary.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-17T07:49:14Z_
