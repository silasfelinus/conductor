# TALKBACK.md — media-watchlist

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-17 | Reviewer → Worker | media-watchlist/t-007 | pattern

**Decision:** merged (Silas-directed session; task created and completed same-session after Silas
shared the real log)

**What was good:**
- The t-001/t-002 design docs held up: PARSER-RULES.md's regex patterns and field-priority rules
  were directly implementable — the importer's core loop is the doc, translated.

**What to improve:**
- The design docs were written from the 2025/2026 sample only and undersold the real file's
  variance by a wide margin: 5 extra media types, 2 unheadered year blocks, a reversed year
  header, mixed-case sections, a stats table, and prose retrospectives. When a design task says
  "parse X" and X is a decade of hand-maintained log, sample the OLDEST years too before
  freezing a schema. Recorded so the next importer-design task starts from the whole corpus.

**Pattern note:** the log's own declared counts (section headers, TYPE table) made excellent
free validation targets — worth repeating on any future hand-log import: diff parsed totals
against the human's own tallies and report drift instead of trusting either side blindly.

## 2026-07-20 | Reviewer (agent run) | media-watchlist/t-008 | done (docs-only, conductor repo)

**Decision:** implemented and self-merged (session claude-conductor-agent-20260720T1515Z).

**Failure category:** none — clean first pass.

**What was good:**
- Claimed via `claim_task.py` against fresh `origin/main` before writing anything, per the
  rotation-collision rule — no other session had touched t-008 today.
- Rather than trusting SCHEMA-PROPOSAL.md's 2025/2026-sample-only proposal at face value,
  reconciled it line-by-line against the actual `data/media-entries.json` (t-007's real
  2440-entry import) and caught a real discrepancy: BROWSE-UX.md specced `rewatch` as a
  `Boolean`, but the importer emits an `Int` (source `"x2"` marker parses to `rewatch: 2`,
  total watch count). Only 1/2440 entries is populated, which is exactly the kind of thing
  that's easy to miss without checking the actual data distribution — verified via a direct
  `Counter` over the JSON rather than assuming the doc was still accurate.
- Delegated research into kind_robots' actual Prisma/API house conventions (response wrapper
  shape, Prisma singleton import path, enum validation pattern, groupBy-based stats routes) to
  an Explore agent against live `silasfelinus/kind_robots` main via the GitHub MCP tools, then
  used those concrete examples (`server/api/facets/index.get.ts`, `server/api/logs/index.get.ts`,
  `server/api/art/queue/stats.get.ts`) to pattern-match the new route contracts instead of
  inventing a shape that would need rework at implementation time.
- Kept `line`/`raw` (import-provenance-only JSON fields) out of the Prisma model rather than
  reflexively carrying every JSON key into columns — documented why (no durable meaning after
  import; re-derivable from the source `.md` files if ever needed).
- Specced an idempotency guard for the one-time seed rather than assuming `skipDuplicates`
  alone was safe — there's no unique constraint to dedupe on, since two genuine same-day
  re-watches without an explicit marker are valid distinct rows.
- `python scripts/audit_roadmaps.py` — 0 errors before and after, same 11-warning/46-info
  baseline.

**What to improve:** none this cycle.

**Kaizen task:** media-watchlist/t-009 — build the MediaEntry migration, the two GET routes,
and wire the browse/stats UI to real data per t-008's spec. This is the actual next blocker
for milestone m3.

## 2026-07-20 | Reviewer (conductor agent-run session) | media-watchlist/t-009 | pattern

**Decision:** merged — kind_robots PR #696 (squash 9d77ea2f).

**What was good:**
- t-008's spec doc (final schema + route contracts) made t-009 a clean, self-contained
  implementation pass with no open design questions — every field, route param, and edge
  case (the `rewatch Int?` correction, no `User` relation) was already resolved before
  writing any code.
- Followed existing house conventions closely (facets/logs route shape, art/queue/stats
  groupBy pattern, Todo model's nullable-userId-no-relation precedent) rather than
  inventing new patterns, and verified against 7 existing contract scripts locally in
  addition to vue-tsc/eslint/prettier.

**What to improve:**
- The "minimal browse UI" scope call (deferring Entry Detail, Review Editor, and CSV
  export) is reasonable for a first pass but means BROWSE-UX.md's private-review-editor
  promise — the actual differentiator over just browsing a spreadsheet — still doesn't
  exist. Filed as t-010 rather than left implicit.
- MySQL/MariaDB's lack of a `nulls: 'last'` Prisma option for the `date_asc` sort mode was
  discovered and documented rather than worked around with raw SQL; worth a second look if
  the ASC sort ever becomes a commonly-used path in practice, not just the default.

**Kaizen task:** media-watchlist/t-010 — Entry detail view + private review editor
(BROWSE-UX.md sections 3/5), the two write routes it needs, admin-gated.

## 2026-07-21 | Reviewer (conductor scheduled agent) | media-watchlist/t-010 | pattern

**Decision:** implemented, self-merged (kind_robots PR #749, squash `704bb43f`).

**Failure category:** null (clean first pass).

**What was good:**
- t-010's own kaizen note (filed by t-009's cycle) fully specified the UI/API
  contract and the schema fields (`review`/`reviewPublic`/`rating`/`externalId`/
  `externalUrl`) already existed from t-008 — zero open design questions before
  writing code, same pattern noted for t-009 following t-008.
- Noticed the existing `GET /api/media-entries` list route has no `select`
  clause, so every entry already carries the full row (review, rating, external
  links, etc.) — reused that instead of adding a second per-entry `GET` fetch
  the task's own note half-suggested ("e.g. PATCH ... for edits" implied a
  fetch might be needed too). Kept the diff to one new write route.
- Ran the full local verification bar (`npm run test` vue-tsc, eslint, prettier)
  via `provision_kind_robots_deps.sh` rather than skipping it as "sandbox can't
  reach DB" — that limitation only affects live browser/DB smoke, not static
  verification, and this session had that script available.
- After `prettier --write`, confirmed via `git diff` that only self-authored
  lines changed on the one pre-existing file touched (`watchlist-browse.vue`) —
  the TALKBACK-documented risk of prettier reformatting ~200 unrelated lines on
  a not-fully-clean file didn't apply here, but checked anyway before committing.

**What to improve:**
- `rating` got a validated write path but no UI control — BROWSE-UX.md's Entry
  Detail mockup doesn't show one explicitly, so it was correctly left out
  rather than guessed at, but that leaves a half-wired field. Filed as t-011.

**Kaizen task:** media-watchlist/t-011 — add a rating (1-10) control to the
Entry Detail panel now that the write path exists.

## 2026-07-21 | Reviewer (conductor scheduled agent) | media-watchlist/t-011 | pattern

**Decision:** merged | kind_robots PR #775 (squash 8037e267), task set to `done`.

**Failure category:** none — clean first pass.

**What was good:**
- Task note left zero open design questions: the server route already validated
  `rating` (1-10 or null), the `MediaEntryDetail` type already carried the field,
  and BROWSE-UX.md's silence on a specific widget shape was already flagged as
  "left out on purpose," not an oversight to second-guess. Picking this task
  meant implementation, not design.

**What to improve:**
- Nothing specific to this task — see the pattern note below, which is really
  about task *selection* upstream of this one.

**Kaizen task:** media-watchlist/t-006 (Polish and upgrade Media Watchlist
front-end surface) still has its own step (1) art-generation sub-step blocked
on the same down home relay confirmed again this cycle (15 consecutive
PENDING/unclaimed jobs spanning 2+ hours as of ~07:12 UTC) — no new task filed,
just noting the blocker is still live for whoever next checks it.

**Pattern note:** with ai-art-academy (t-019/t-035) and kind-robots (t-033,
4 consecutive clean rechecks the same day) both effectively unpickable this
cycle — one on a down relay, the other a no-new-evidence watch task — this
session dropped to media-watchlist/t-011 in priority order rather than
re-running kind-robots/t-033's sweep a 5th time for no new information. Same
judgment call as the 2026-07-20 cycle that picked t-010 for the identical
reason (see this file's t-010 entry). Worth naming as standing practice: a
recheck-only task with N consecutive clean results in the same day is lower
value than the next genuinely workable ready task, even if it's technically
"first" in priority order.
