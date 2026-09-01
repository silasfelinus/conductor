# dream-cycle — TALKBACK

Append-only critique log for this project. Format per AGENTS.md.

## 2026-07-10 | Reviewer → Worker | dream-cycle/backlog-sync (PR #339) | critique

**Decision:** merged (squash 8d49570)

**What was good:**
- Card drift caught and reconciled proactively — backlog/monster-recast.md now matches the home set (34-concept pool, STYLE-GUIDE workflow, approved manifest, t-016 stage)
- Parked hollywood-recast-2 card is exactly the right shape: steering surface complete, idler-proof via status frontmatter
- Honest flag on the CONTROL.md ratings inference (superseding "launch sets are all-ages") with a one-bullet revert path

**What to improve:**
- Nothing significant; PR body template fully filled, verification section concrete

**Kaizen task:** dream-cycle/t-010 — scheduler-card drift check runnable in CI (from the Worker's own suggestion)

## 2026-07-14 | Reviewer → Silas | dream-cycle/t-011 | pattern

**Decision:** merged (PR #487, "Art-forward daily digest: proposals + scoring + pitch cards")

**Failure category:** none — clean first-pass merge, all 19 CI checks green.

**What was good:**
- Soft-fail design verified in code, not just claimed: `build_dream_proposal.py` falls
  back to `SAMPLE_PROPOSAL` on missing key or API exception (never raises); `curate_art.py
  --daily` writes an objective-only report (`verdict: needs-vision`) when no vision model
  is available. Both workflow steps also carry `continue-on-error: true` as a second layer.
- Direct-to-main commit step in `daily-digest.yml` (new `contents: write` + rebase-retry
  push) mirrors the existing `auto-art-generate.yml` pattern byte-for-byte rather than
  inventing a new escalation path.
- Roadmap diff was purely additive to dream-cycle's own tasks (t-011 done, t-012/t-013
  ready) — no drive-by edits to unrelated projects.
- PR wasn't from a `worker/*` branch or the standard handoff template (ad-hoc Silas-directed
  `claude/*` session), so I reviewed it to the same bar as a Worker PR per AGENTS.md's
  claude/* merge rule before merging.

**What to improve:**
- No "Flags for Reviewer" or "Kaizen suggestion" section since this wasn't produced via
  the Worker handoff template — not a defect, just noting the PR shape differs from the
  usual worker/* cycle output, which is expected for a Silas-directed session.

**Kaizen task:** none created this cycle — the PR itself already spawned t-012 ("Phase 2:
build the proposal into real records + art") and t-013 ("Phase 2: kind_robots Daily Dream
page") as its natural follow-ons, which cover the compounding-improvement slot for this
merge.

## 2026-07-14 | Reviewer → Worker | dream-cycle/t-011 | pattern

**Subject:** Two concurrent sessions each authored a separate daily-dream proposal for the
same Pacific date, with different slugs — the "one proposal per Pacific date" contract held
in spirit (both are well-formed) but was violated in fact.

**Detail:**
- Found during the 2026-07-14 23:xx hourly Reviewer sweep: `projects/dream-cycle/backlog/`
  contains both `2026-07-14-moth-hour-mechanics.md` and `2026-07-14-moth-orchard.md`, each
  with `proposal_date: '2026-07-14'` in frontmatter and `proposal: true`.
- Root cause: `scripts/build_dream_proposal.py`'s `proposal_exists_for(date)` /
  `write_proposal()` only check the local working tree at `--check`/`--from-json` time —
  there is no origin/main-fresh recheck immediately before the write, unlike
  `scripts/claim_task.py`'s fetch-fresh-then-write-with-retry pattern (see root AGENTS.md
  "Rotation collisions"). Two sessions running `--check` inside the same window both saw
  "no proposal yet" and both authored + wrote one. Because the two agents picked different
  slugs, the existing slug-dedup guard (`existing_slugs()`) never caught the collision —
  it only prevents *identical*-slug clashes, not two-different-slugs-same-date.
- Filed `dream-cycle/t-014` (ready) to harden the script against this race, mirroring
  `claim_task.py`'s approach. Left both duplicate files in place — they're harmless,
  well-formed, carry no Notes from Silas, and are not yet built — no cleanup needed, this
  is purely a prevent-recurrence task.

**Suggested action:** Worker: when picking up t-014, reuse the `claim_task.py` fetch/retry
primitives rather than inventing a new git-race pattern from scratch.

## 2026-07-16 | Worker → Reviewer | dream-cycle/t-014 | response
type: response

**Subject:** t-014 implemented reusing claim_task.py's git primitives, as suggested.

**Detail:**
- Reused `scripts/git_plumbing.py` (`run_git`, `read_file_at_ref`) — the same
  helpers `claim_task.py` uses — rather than inventing a new git-race pattern.
  `build_dream_proposal.py` now fetches origin/main and re-checks for any file
  with today's `proposal_date` immediately before writing (`remote_proposal_for`),
  mirroring claim_task's fetch-fresh-then-write recheck. On a landed same-date
  proposal the write aborts; best-effort, degrades to local-only when no origin
  is reachable (offline/sandbox).
- Scope note (honest boundary): I implemented the note's PRIMARY prescribed fix
  (the origin/main pre-check + abort), NOT a full atomic commit+push-with-retry
  loop like claim_task's. A residual window remains if two sessions both author
  locally before either commit/pushes; per the t-014 note that fully closing it
  belongs to the calling sweep step (pull-before-check / push-after-write), which
  is out of scope for this self-contained script+tests task. Documented in the
  script docstring and left as the recommended sweep ordering.
- Added `tests/test_build_dream_proposal.py` (11 tests) with a local bare+clone
  origin harness modeled on `test_claim_task.py` — proves the exact
  same-date/different-slug race (moth-hour-mechanics vs moth-orchard) is refused.
- The two existing 2026-07-14 duplicate files were left untouched per the note.

**Suggested action:** none — flagging the residual-window boundary for the
Reviewer to confirm the sweep-ordering follow-up (pull/push around --check /
--from-json) is tracked, or file it if not.

## 2026-07-21 | Worker (scheduled burst) | dream-cycle/t-006 | pattern

**Decision:** merged directly to main (recurring, no-PR bookkeeping task per convention)

**Failure category:** null (clean first-pass; monster-recast's block was pre-existing, not caused here)

**What was good:**
- Correctly deferred monster-recast (status: `approved`, top of the promotion order) after
  confirming — not assuming — its delegated home task is genuinely blocked: called the live
  relay-status API directly and got zero registered agents, matching coloring-book/t-022's
  own `needs-human` note.
- Picked the next candidate by the documented tie-break (oldest `created`, alphabetical among
  ties) rather than an arbitrary pick, and ran Stage 1 exactly as specced: no API calls, filled
  the two genuinely thin sections (character `Look`/`Drive`, reward `rewardType`), verified
  against the full Stage 1 checklist before flipping `status: building`.
- This cycle's task selection was itself a rotation pick (this session's broader goal), after
  two earlier picks this same hour turned out to be dead ends: `animation-studio/t-001` was
  claimed in error (project is retired — see root TALKBACK.md) and reverted before any PR, and
  `ruler-hooked/t-010` turned out to already be fully done except for the same art-relay block.
  dream-cycle's idle-fallback task was the one candidate this cycle that could produce genuine
  forward progress with zero external dependencies.

**Kaizen task:** none filed — Stage 1's thin-section-filling worked exactly as designed; no
gap found in the playbook itself this cycle.

## 2026-07-27 | Worker (conductor scheduled burst-mode rotation) | dream-cycle/t-018 | pattern

**Decision:** implemented and set `status: review`, opening a PR (not merging directly —
leaving the merge to a Reviewer pass per normal software-task flow, since this isn't a
recurring/no-PR bookkeeping task).

**Failure category:** null (clean first pass).

**What was good:**
- Confirmed the target API (`https://kind-robots.vercel.app/api/facets?taxonomy=GENRE`)
  was actually reachable and returned real, filterable GENRE-taxonomy data before writing
  any code, rather than assuming the shape from the task note alone.
- Kept the fallback path unconditional: `fetch_live_genre_facets()` returns `None` on any
  failure mode (network, HTTP, bad JSON, empty body), and `_genre_spark()` always falls back
  to the existing `GENRE_FAMILIES` list rather than raising — the daily sweep can never be
  blocked by the kind_robots API being down.
- Verified live end-to-end via `python scripts/build_dream_proposal.py --brief`, which
  printed real facets (Arabian Nights Redux, Mystery, Dark Academia) and correctly labeled
  the source, not just relying on unit tests with mocked responses.
- Added 8 new unit tests (fetch success/filtering/error paths, spark determinism, recency
  weighting, fallback-when-too-few-fresh) — full suite went from 608 to 616 collected
  (615 passed, 1 pre-existing skip).

**What to improve:**
- Did not add a live (non-mocked) integration test that hits the real API — deliberately,
  since conductor's test suite should stay network-independent, but worth a note for
  whoever next touches this: the mocked tests can't catch a future API response-shape
  change (e.g. `title` renamed) on their own; the `--brief` manual check is the fallback
  verification until/unless a smoke test is added elsewhere.

**Kaizen task:** deferred — no gap in the playbook surfaced; the existing "best-effort
external fetch, always degrade gracefully" pattern (already used by `fetch_main()`) applied
cleanly here.

## 2026-07-28 | Reviewer → Worker | dream-cycle/t-007 | response

**Decision:** merged (audited already-generated work, no new art request needed)

**Failure category:** null (this was a stale-state cleanup, not a failed pass).

**What was good:**
- Rotation pass (burst-mode cycle scanning for the oldest untouched `ready` task
  across all active projects) picked this up at 18 days stale rather than letting
  it keep resurfacing.
- Verified before writing anything: confirmed all three files
  (`projects/images/dream-cycle-{icon,card,hero}.webp`) already existed, checked
  actual dimensions with `file` (256x256 / 512x768 / 1280x720, all valid WebP)
  against the DEFAULT icon/card/hero spec in AGENTS.md's "Project art" section,
  and confirmed the ART-PROMPTS.md pending line was the only remaining loose end
  before touching the roadmap.

**What to improve:**
- The files landed via the auto art pipeline's "process task events" flow
  sometime before this task was ever picked up — the roadmap task and
  ART-PROMPTS.md pending entry both should have been closed out by whatever
  process generated the files, not left to a later unrelated session to notice.
  Worth checking whether `distribute_images.py` (or the task-events processor)
  can close a matching roadmap task automatically when it lands a project's
  full icon/card/hero trio, instead of relying on a human-shaped "note: remove
  the pending entry once files land" instruction that nothing enforces.

**Kaizen task:** conductor/t-087 — project icon/card/hero art has no provenance
metadata (prompt/model/source), unlike inspiration images' per-slug `gallery.json`;
extend the distribute pipeline to record it.

## 2026-07-29 | Worker → Reviewer | dream-cycle/t-019 | pattern

**Decision:** merged (PR #1419) — self-merged as a scoped, reversible, verified
software fix, standard Worker close-out.

**Failure category:** null (clean first-pass fix).

**What was good:**
- Didn't trust either the task note's original diagnosis or the newer shipped
  code at face value — cross-checked both against the actual live kind_robots
  folder layout (`/home/user/kind_robots/public/rewards/...` exists,
  `public/images/rewards/...` does not) before deciding which one was right.

**What to improve / pattern flagged:**
- An unrelated-looking PR (#1399, titled around an ai-art-academy TALKBACK
  entry) landed both `ops/home-server/relay_media_agent.py` and
  `tests/test_media_rewards.py` together, and the tests locked in a subtly
  wrong contract (folding `public/rewards/...` into the images root) as if it
  were the settled, correct behavior — complete with a test named
  `test_relay_uses_configured_image_root_without_sibling_mapping` that
  actively asserted the sibling-root idea (this task's own suggested fix) was
  wrong. A passing test suite is not proof a fix is correct when the test
  itself encodes the same misunderstanding as the code — it needs to be
  checked against the real external system (here: the actual target repo's
  folder structure), not just internal self-consistency. Worth watching for
  this pattern elsewhere: a "fix + matching tests, both green" PR bundle can
  still be confidently wrong if nobody cross-checks the premise against
  ground truth.

**Kaizen task:** dream-cycle/t-021 — add a startup-time config check to
`relay_media_agent.py` that logs which media roots (`images`, `rewards`) are
configured vs. missing, so a misconfigured box surfaces immediately in the
relay's own logs instead of only showing up as a failed job hours later.

## 2026-09-01 | Reviewer → Worker | dream-cycle/(unfiled, live-flagged) | pattern

**Decision:** merged (PR #3386, squash 5496788) — reversible, scoped, verified software fix,
Silas-directed (flagged live on a card), standard claude/* branch Reviewer merge.

**Failure category:** null (clean, already-verified fix; no rework needed).

**What was good:**
- Recomputing `backstory`/`desc` from their authored source fields to diff against live,
  instead of re-generating prose with a model, kept the fix deterministic and reviewable —
  the PR body shows the exact live/expected diff for both patched rows.
- Named the actual root cause precisely: the repair lane only rewrites `backstory` when it
  rewrites `carries`, so a builder fix that doesn't touch `carries` on a given bundle never
  reaches rows built before the fix. Framed as "right going forward, silently wrong in
  production" and explicitly tied to the same shape as three prior incidents in this
  project's history (frozen two-day window, unwired surname detector, unreachable publish)
  — a real pattern, not a one-off.
- Also caught and fixed a self-admitted prior miss: a `carries`-opens-on-the-formula check
  was skipped once on a single-card read ("reads fine unlabelled") instead of the
  catalog-wide census the project's own method requires; the PR adds the check plus tests
  for both the violation and the target register.
- CI: 22/23 checks green; the one outstanding (`Analyze (javascript-typescript)`) is the
  same known-slow/stalling CodeQL analyzer documented in conductor/t-106 and observed again
  today on kind_robots#2287's companion sweep — `mergeable_state: unstable` with no other
  check outstanding matches that established non-blocking precedent, so merged without
  spending a re-run on it.

**What to improve:**
- The fix reached production before the mechanism to catch a recurrence exists: `--verify-live`
  is a manual flag, not wired into anything scheduled. Filed as kaizen below rather than asking
  for a broader change in this PR — the two-row fix was itself already minimal and complete.

**Kaizen task:** dream-cycle/t-024 — wire `--verify-live --strict` into the recurring t-006
maintenance pass so the next builder fix that doesn't back-propagate to already-built rows is
caught automatically instead of waiting for a live-card report.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-01 | Reviewer → Worker | dream-cycle/(unfiled, live-flagged) | pattern

**Decision:** merged (PR #3390, squash 3647045) — reversible, scoped, well-tested software fix.

**Failure category:** null (clean, already-verified fix).

**What was good:**
- Correctly identified the atomicity unit was wrong: batch-level all-or-nothing was
  protecting against a state (a half-authored bundle) that per-bundle validation
  already prevents on its own, while costing 13 good repairs every time one bundle
  in a batch of 14 came back as an empty completion. Three batches in a row lost
  this way before the fix.
- Made the failure diagnosable instead of just retried: the prior `RuntimeError`
  discarded `stop_reason`/block types/`usage` on an empty completion, so six
  consecutive failures on one bundle taught nothing. Now reports enough to
  distinguish a transient flake from something bundle-specific.
- Two new tests covering exactly the two edge cases that matter: one bundle
  failing still repairs the rest (and records the failure), and nothing succeeding
  still raises loudly rather than silently reporting zero repairs as success.
- CI: 23/24 checks green; the one outstanding (`Analyze (javascript-typescript)`)
  is the same known-slow/stalling CodeQL analyzer from conductor/t-106, seen twice
  more today on this same session's other PRs — `mergeable_state: unstable` with no
  other check outstanding, so merged per that established precedent.

**What to improve:**
- The fix correctly stops discarding good work on a flaky bundle, but doesn't yet
  distinguish "flaky, will pass eventually" from "this bundle's content reliably
  fails" — such a bundle would now retry silently forever. Filed as kaizen below.

**Kaizen task:** dream-cycle/t-025 — track consecutive per-bundle authoring
failures across runs and surface a bundle explicitly once it crosses a small
threshold, instead of retrying it unnoticed indefinitely.

---
_Generated by [Claude Code](https://claude.ai/code)_
