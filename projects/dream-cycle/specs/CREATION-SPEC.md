# CREATION-SPEC.md — the creation loop contract

**Task:** dream-cycle/t-004 · **Date:** 2026-07-16

The type-agnostic contract the recurring build task (dream-cycle/t-006) follows for
**every** creation type. Per-type mechanics live in `specs/<type>.md` playbooks
(`specs/dream.md`, `specs/coloring-book.md`); this file is the loop those playbooks
plug into. When a rule here and a playbook seem to conflict, this file governs the
loop (queue, one-building rule, ledger) and the playbook governs the stages.

## When the loop runs — "nothing better to do"

dream-cycle sits **last** in `projects/priority.yaml`. Its recurring build task is
therefore only picked when no other active project has a `ready` task — that is the
"idle fallback" contract, enforced by placement, not by a scheduler change. The
Worker runs hourly; a creation takes ~6–8 idle cycles ≈ one day.

The parallel **daily-dream fast lane** (`build_dream_records.py`, t-012) is NOT this
loop — it builds a dated proposal straight to `built` on a separate track. This
contract is about the single hand-curated `building` creation advanced one stage per
idle cycle.

## Each cycle — the fixed sequence

1. **Fold in Silas's steering first.** Scan every backlog file for new content in
   `## Notes from Silas` and for frontmatter flips (`status`, `priority`). Fold notes
   in before any build step; **never edit or delete** the Notes section (it is
   Silas-owned, append-only for agents). A card at `status: parked` or `vetoed` is
   never selected; `building` at the top of the queue is resumed.
2. **Advance the active creation, or promote the next one:**
   - If a card is `status: building`, advance it **exactly one stage** per its type's
     playbook, then append its `## Build log`.
   - Else promote the top queued outline to `building` and run its first stage.
3. **On ship** (final stage reached): verify the playbook's checklist, flip the card
   to `built`, write the `SHIPPED.md` ledger entry, and replenish the backlog if
   needed (below).

### The one-building invariant
**Only one creation may be `status: building` at any time, ever.** "One task in
flight" applies at the creation level. The loop never starts a second creation while
one is building — not even of a different type.

## Queue order

Across all types, pick the next creation to promote by, in order:
1. `status: approved` before `status: outline` (approved = Silas-blessed),
2. then higher `priority` (`high` > `normal` > `low`),
3. then oldest `created` date.

**Playbook requirement:** a type is only buildable if `specs/<type>.md` exists. An
outline whose `type` has no playbook is skipped in the queue (it waits, it does not
block) until someone writes the playbook. This is how new types come online: land a
`specs/<type>.md` PR, and outlines of that type become buildable.

## Home-project delegation

Some types' output belongs to a **home project** (e.g. `coloring-book` → the
coloring-book project's `sets/<slug>/`). For those:
- The backlog card is the **scheduler/steering surface only** — it names the home
  target, tracks the next stage, and carries Silas's notes. The home project's files
  are authoritative; the card summarizes them.
- **One owner per task, never double-claim.** If the Worker is already actively
  building the home project's task through normal priority, the idler does **not**
  claim it — it picks the next queued creation instead. An idler day for a delegating
  type only ever absorbs *leftover* capacity on work no one else is driving.
- The playbook keeps BOTH records in sync each stage: the home roadmap's task status
  **and** the card's Build log. The scheduler-card drift check
  (`scripts/check_scheduler_drift.py`, t-010) fails CI if the card and home set diverge.

Types whose output is self-contained kind_robots content (e.g. `dream`) create rows
directly; there is no home project to delegate to.

## Content creation is reversible by construction

Content-writing stages create **content rows or set files, never backend code**:
- via the kind_robots REST API with `KR_API_TOKEN` where an endpoint exists
  (see `docs/api-surface.md`, all dream-build models are api-ready), or
- as seed-data / set-file PRs where no endpoint applies.

Every created row carries `designer` (`"dream-cycle"`) and source metadata (the
originating slug / `proposalDate`) so a whole creation is **traceable and removable** —
this is what keeps the loop reversible. kind_robots backend code stays
read-only/external: a missing endpoint becomes a kind_robots roadmap task or pitch,
never a direct backend edit.

## Build log & ledger duties

- **Build log** (per card, every stage): append one line —
  `YYYY-MM-DD | <stage> | what was created where | PR`. This is how Silas sees progress
  without reading PRs.
- **SHIPPED.md ledger** (once, at ship): append one entry per completed creation in the
  format the file documents (slug, type, date, PRs, what was created where). Append-only.
- **LEARNING.yaml**: a creation that blocked or taught something gets a record on close,
  per AGENTS.md (recurring cycles don't each get one).

## Backlog replenishment — keep the runway full

The loop's final ship stage checks the backlog: if fewer than **5 buildable outlines**
remain (`outline`/`approved` with a playbook-backed type, excluding `parked`/`vetoed`),
generate new outlines to top it back up — a standing runway of future developments
(dream-cycle/t-005 is the batch version of this). Warn in the cycle's PR when the
buildable count is low.

## Hard gates (unchanged)

Anything outward-facing stays a hard `needs-human` gate and is never auto-fired:
publishing, POD accounts, store listings, spend/billing, production deploys, secrets,
DNS, schema changes. The loop lands creations as site content or set inventory under
existing flags only. Generated internal art is pre-approved (AGENTS.md, 2026-07-06);
originality/IP guardrails still apply per each playbook.
