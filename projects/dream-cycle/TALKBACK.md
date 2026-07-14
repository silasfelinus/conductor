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
