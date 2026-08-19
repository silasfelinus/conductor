# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-19T16:29:54Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **694**
- Outcomes: blocked: 15, cancelled: 1, done: 678
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 15 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 36 | 100% |
| kind-economy | 5 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 70 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 13 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 678 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-19 `kind-economy/t-009` — A new dashboard page's content/*.md frontmatter can declare background* art routes that verifyPageBackdrop.ts requires a matching PageSeed entry in stores/seeds/pageBackdropArtPrompts.ts for -- easy to miss in a sandbox with no live DB/browser to catch the 404 directly, but caught reliably by CI's contract check. Worth adding "does this page need a backdrop seed entry" to the standard pre-PR checklist for any task creating a new page.

- 2026-08-19 `kind-economy/t-008` — Clean first-pass Worker output on a genuinely ambiguous accounting task: the roadmap note left two real judgment calls open (a documented rounding rule for the 3-way split, and how to treat a per-transaction payment-processing fee when tokens are purchased in batches but spent fungibly later) and the Worker resolved both with a named constant, an inline rationale, and a 20,000-iteration property test proving the sum-to-gross invariant holds exactly including negative-margin rows -- rather than picking a plausible number and moving on. It also independently re-verified the task note's own claim ("costUsd is never reconciled against real billing") by grepping every gate.commit() call site itself instead of taking the note at face value, and surfaced it as a flagged follow-up rather than baking a false assumption into the schema doc comments. Reviewed the migration.sql line-by-line (additive CREATE TABLE + one FK only) before merging, per this repo's financial-ledger convention -- the Worker's own PR body correctly left the PR unmerged for exactly that reason instead of assuming a non-gate_human task meant no review was needed.

- 2026-08-19 `kind-economy/t-007` — Clean first-pass Worker output: additive-only migration (ADD COLUMN IF NOT EXISTS / CREATE INDEX matching the repo's established convention), a resolver that never throws (a lookup failure degrades to "no attribution" rather than failing the charge), and both open policy questions (mission-share fallback on unresolved creatorUserId, self-attribution recorded but not decided) handled exactly as the task note specified rather than guessed at. Reviewed the actual diff (schema, migration.sql, manaAttribution.ts, manaGate.ts wiring) rather than trusting the PR description alone.

- 2026-08-19 `kind-economy/t-005` — A flat "donate a third" plan does not net to zero for tax purposes by default -- gross receipts and a charitable deduction are separate line items whose offset depends entirely on entity type and itemization, and for a sole prop/LLC taking the standard deduction the offset is worth nothing. The fix has to be structural (keep the mission third out of gross receipts entirely via a direct customer-to-charity donation) rather than a bigger deduction. Also: when researching a compliance question, the framing in the task note ("check these N states") can undersell the real exposure -- a broader, newer category of law (California's charitable-fundraising-platform registration, which reads broadly enough to plausibly cover an embedded donate-at-checkout flow) was more directly on point than the originally-flagged commercial-co-venture states, and surfaced a concrete design lever (redirect to the donation platform's own hosted page vs. embedding it) worth flagging even though this task's scope was research-only.

- 2026-08-19 `kapowarr/t-056` — Provider abstraction is incomplete while one provider's identifier remains a schema requirement; keep compatibility IDs nullable and route refresh through each entity's durable provider identity.
- 2026-08-19 `kind-economy/t-004` — When a live claim on the site outpaces the mechanism behind it, "future tense" is nearly always the right default over "leave it and document the gap" -- it costs nothing, is fully reversible, and removes a live credibility risk immediately. Also: a CI job stuck `queued` with the parent run auto-concluding `failure` (no logs, zero jobs actually run) is a transient infra stall, not a real check failure -- confirm by running the same commands locally before trusting the red state, then retry the workflow run to verify before merging.\n

- 2026-08-19 `kapowarr/t-038` — A provider abstraction does not by itself remove a legacy provider monopoly: database NOT NULL columns and Add-form assumptions remain product boundaries. Metron fallback was therefore shipped through its explicit ComicVine cross-links with durable Metron provenance, while native-only records were withheld from a knowingly broken Add path. Also, never follow an authenticated API's pagination URL verbatim; reconstruct the next page on the configured origin so credentials cannot cross an origin boundary.

- 2026-08-19 `kapowarr/t-055` — Human-triggered bulk operations should preserve successes and return item-level failures; background jobs can keep strict exception semantics for checkpointed retries.
- 2026-08-19 `kapowarr/t-037` — Separate stable external identity from provider credentials and UI policy; additive maps let alternate metadata coexist without destabilizing legacy libraries.
- 2026-08-19 `kapowarr/t-054` — Bound remote metadata resolution as a whole and pair every loading state with success and rejection exits; source health data should be visible before acquisition.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-19T16:29:54Z_
