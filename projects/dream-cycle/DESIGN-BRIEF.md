# Dream Cycle — current design brief

**Current contract:** `PIPELINE.md`
**Original project direction:** 2026-07-10
**Canonicalized:** 2026-08-02

## Purpose

Dream Cycle is Conductor's idle-capacity project. When no higher-priority work is ready, it keeps the creative machinery warm without inventing a second product pipeline.

It now has two clearly separated responsibilities:

1. maintain the rolling Daily Dream proposal, creation, art, and digest pipeline;
2. coordinate delegated, non-dream creation types whose real work lives in another project, such as coloring books.

## Daily Dream product

A dated Daily Dream proposal contains exactly six assets:

- one dream vibe,
- one dream location,
- one Character,
- one ITEM Reward,
- one SKILL Reward,
- one Scenario authored last from the preceding assets.

Daily bundles do not include a narrator. The deterministic creative constraints come from `scripts/build_dream_proposal.py --brief` and are persisted as `seed_facets` in the proposal data.

## One creation path

The proposal file is the human steering surface. It creates no database rows.

After one Pacific steering day, Hourly Conductor reaches `scripts/build_dream_records.py` through `scripts/build_conductor_summary.py`. That builder is the sole Daily Dream object writer. It creates the complete bundle transactionally, records every ID in `built-data`, and queues six stable art requests. Facet assignment and art attachment enrich that recorded bundle afterward.

The daily digest is read-only. It reports committed proposal, build, Facet, and art evidence and never creates or repairs objects.

Full ownership and ordering rules live in `PIPELINE.md`. Active implementation details live in `specs/dream.md` and `specs/CREATION-SPEC.md`.

## Steering and idea inventory

Dated files with `proposal: true` are the only Daily Dream inputs eligible for object creation. Silas can edit priority, add notes, park, or veto them during their steering day.

Older non-proposal `type: dream` files are idea inventory only. They may inspire a future dated six-asset proposal, but no agent advances them through API stages. `_template.md` creates this lightweight idea-inventory shape.

## Delegated creation types

A delegated type such as `coloring-book` may use a multi-cycle `status: building` scheduler card because its authoritative content and production stages live in its home project. Dream Cycle never forks that content into a second source of truth.

## Operational truth

- `PIPELINE.md` is the current end-to-end contract.
- Proposal `built-data` is the durable creation ledger.
- `projects/art-prompts.yaml` is the art queue.
- The digest reports state; it does not mutate it.
- `SHIPPED.md` points readers to durable evidence rather than maintaining a competing manual ledger.

The original eight-stage, multi-character, optional-narrator Dream experiment is retired. Its history remains in git, TALKBACK, and parked cards such as Lantern Post, not in active instructions.
