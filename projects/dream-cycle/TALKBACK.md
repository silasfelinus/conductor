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
