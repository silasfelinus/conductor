# Playbook: `type: coloring-book`

**Creation type:** coloring-book · **Task:** dream-cycle/t-009 · **Date:** 2026-07-16

The second dream-cycle creation type. Where a `dream` build creates kind_robots
content rows directly, a `coloring-book` day **delegates** to the coloring-book
project: an idle creation day drafts or advances **one book set** through that
project's production sequence. This file is the per-type playbook the recurring
build loop (dream-cycle/t-006) follows for coloring-book cards; it sits beside
the forthcoming type-agnostic `CREATION-SPEC.md` and `specs/dream.md` (t-004) and
defers to `CREATION-SPEC.md` for any rule not specific to this type.

## The delegation law — no second source of truth

Book sets live in `projects/coloring-book/sets/<slug>/` and obey the
**coloring-book project's** specs (t-003 shared engine, t-004 generation
pipeline) and originality guardrails. **Reference those specs; never fork them.**

The dream-cycle backlog card (`backlog/<slug>.md`, `type: coloring-book`) is the
**scheduler card and steering surface only**:
- it names the set (`home_set: projects/coloring-book/sets/<slug>/`),
- tracks which production stage is next,
- carries Silas's `## Notes from Silas`,
- records progress in its `## Build log`.

The set's actual content files (README, STYLE-GUIDE, homage/concept YAML,
`approved/manifest.yaml`, art) belong to coloring-book. The card summarizes; the
set is authoritative. (The scheduler-card drift check —
`scripts/check_scheduler_drift.py`, dream-cycle/t-010 — enforces that the card's
summary stays true to the set and fails CI when they diverge.)

### One owner per task — never double-claim
The coloring-book roadmap tasks are the real units of work. When the Worker is
already actively building a set's task through normal project priority
(coloring-book usually outranks dream-cycle, which sits last in
`projects/priority.yaml`), the idler **must not** claim that same task. It picks
the next queued creation instead. An idler coloring-book day only ever absorbs
**leftover** capacity on a set no one else is driving. One owner per task, always.

## Preconditions — run every coloring-book day, before any work

1. **Fold in Silas's notes.** Read the card's `## Notes from Silas`; if it has
   real content, fold it in first (and never edit that section). `status:
   parked` and `status: vetoed` cards are **never** selected — a parked card
   (e.g. `hollywood-recast-2`) is untouchable until Silas flips `status:` to
   `approved`.
2. **MANDATORY preflight.** Run `python scripts/coloring_approved_status.py
   --check` (add `--set-dir projects/coloring-book/sets/<slug>` for a specific
   set). It must pass. This surfaces broken manifest references, missing approved
   assets, and filename drift before you touch the set.
3. **Approved masters are frozen.** `approved/manifest.yaml`'s
   `confirmed_approvals` is the source of truth for confirmed designs. **Never
   regenerate an approved design for production** — reuse the approved colored
   master and its BW partner. The exploratory queue continues unchanged; a queued
   render for an already-approved concept is inspiration/alternate only unless
   Silas explicitly promotes it.
4. **Respect the per-set content rating.** It lives in the set's README
   (`content-rating:`); it is per set, not global (Monster Recast is progressive
   teen horror ≈PG-13, **not** all-ages). Honor it in every prompt and selection.

## Build stages — one per idle cycle

Each idle cycle advances the active set by **exactly one** stage of the
coloring-book production sequence, then appends the card's Build log and updates
the corresponding coloring-book roadmap task. Stages map onto the home project's
sequence (see `sets/monster-recast/README.md` and the coloring-book roadmap):

| # | Stage | Home-project work | Card/Build-log update |
|---|---|---|---|
| 1 | **Design** (new book only) | Create the set folder `sets/<slug>/` with README (concept + book shape + content rating), STYLE-GUIDE (paired-master rules), and a cast/page-plan YAML modeled on `sets/monster-recast/`. | Card created with `home_set` set; log "design: set scaffolded". |
| 2 | **Concept art** | Generate concept-art candidates from the concept pool (coloring-book t-007 for Monster Recast) via the generation pipeline (t-004). Originality checkpoint first (below). | Log candidates generated + where. |
| 3 | **Selection + finalization** | Rank studies; finalize which designs become pages; record chosen designs (coloring-book t-013). Confirmed masters go into `approved/manifest.yaml`. | Log selections; update approved-pair list the card cites. |
| 4 | **Character creation** | Create the kind_robots Character collection for the set (coloring-book t-014) — Characters stay private until the book is release-ready. | Log Character rows created. |
| 5 | **Coloring conversion** | Convert each **approved colored master** into its faithful B/W coloring page (coloring-book t-015), preserving pose, anatomy, identity, and hook per the STYLE-GUIDE. | Log pages converted. |
| 6 | **Book assembly** | Assemble the digital + print-ready package (coloring-book t-016). | Log package assembled. |
| 7 | **PAUSE** | Stop. Publishing, POD accounts, store listings, and any spend are **hard-gated** (`needs-human`) — never auto-fired. | Log "assembled; paused at publishing gate". |

The recurring loop promotes the top queued coloring-book card to `building` only
when its stage-1 set exists (or it IS the stage-1 design day). It advances one
stage per cycle until stage 7, then marks the card `built` (a shipped set = an
assembled, unpublished package) and writes the SHIPPED.md ledger entry.

### Paired-master production law (all art stages)
The canonical source is a **finished colored master first**; the B/W coloring
page is a faithful conversion of that same image with minimal compositional
change (`sets/monster-recast/STYLE-GUIDE.md`): thick black contours, flat bounded
color, no gradients/airbrush, strong silhouettes, structured detail, serious camp
not gag illustration. Never convert-first or paint-first.

### Originality-guardrail checkpoint — before ANY art generation
Every concept must clear the coloring-book project's originality guardrails
**before** a prompt is queued: original characters that evoke archetypes/lineages,
**never reproducing protected designs, names, logos, or commercial identities**.
Internal source-lineage names (in the concept YAML) are creative shorthand, not
final commercial identities — they must be replaced with original identities
before public art. If a concept can't clear this bar, it does not get generated;
note it in the Build log and move to the next candidate. (Generated internal
project art is otherwise pre-approved per AGENTS.md — this checkpoint is about
originality/IP, not the art-generation permission.)

## Per-stage verification

- **Design:** set folder exists with README (+ content-rating), STYLE-GUIDE, and
  a cast/page-plan YAML; `coloring_approved_status.py --check` passes on the new
  set; the card's `home_set` resolves and `check_scheduler_drift.py` is clean.
- **Concept art / conversion:** files landed where expected; each cleared the
  originality checkpoint; approved designs were **not** regenerated.
- **Selection:** new confirmed masters are recorded in `approved/manifest.yaml`
  and the card's approved-pair summary matches (drift check green).
- **Character creation:** Character rows exist and are **private**; art attached
  where available.
- **Assembly:** package contains every intended interior page + cover; page
  counts match the README's declared shape.
- **Every stage:** BOTH the coloring-book roadmap task status AND the card's
  Build log are updated; no task the Worker already holds was double-claimed.

## New-book outline → set folder

For a brand-new book idea (card authored from `backlog/_template-coloring-book.md`
with `home_set: null`): stage 1 creates `projects/coloring-book/sets/<slug>/` with
the README/STYLE-GUIDE/page-plan scaffold (modeled on `sets/monster-recast/`),
sets the card's `home_set` to that path, and files the set's production stages as
coloring-book roadmap tasks (or reuses the standing set-growth task). From then on
it is the same delegation as an existing set.

## Ship + ledger

At stage 7 (PAUSE): verify the full checklist above, mark the card `built`, set
`built_pr`, write the `SHIPPED.md` ledger entry (slug, type, date, PRs, what was
produced where), and — per `CREATION-SPEC.md`'s replenishment rule — top the
backlog back up to ≥ 5 buildable outlines if it dropped below. Publishing/POD
remain a separate, human-gated step outside the creation loop.

## First coloring-book creation

**Monster Recast** (`backlog/monster-recast.md`, `status: approved`, `priority:
high`). Its design stage is already complete in
`projects/coloring-book/sets/monster-recast/` (3 approved master pairs: Frieda
Krueger, TV Boy, Masking Up), so the idler's job is driving its **concept-art →
selection → Character → conversion → assembly** stages when idle capacity allows.
Once this playbook lands, that card becomes buildable by the dream-cycle t-006
loop.
