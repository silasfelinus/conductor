# CREATION-SPEC.md — the creation loop contract

**Task:** dream-cycle/t-004 · **Canonical daily-dream pipeline:** `../PIPELINE.md`

This is the type-agnostic contract for dream-cycle's idle capacity. Per-type mechanics live in `specs/<type>.md`. When this file and a playbook conflict, this file governs queueing and ownership; the playbook governs only the type-specific work.

## When the loop runs

dream-cycle sits last in `projects/priority.yaml`, so its recurring task is selected only when no other active project has ready work. It consumes leftover capacity rather than competing with ordinary product work.

## One daily-dream object path

`type: dream` is not a staged REST build anymore. Daily-dream objects follow one path only:

1. An agent authors one committed six-asset proposal with `scripts/build_dream_proposal.py`.
2. The proposal remains editable for its Pacific steering day.
3. Hourly Conductor invokes `scripts/build_dream_records.py` once through `build_conductor_summary.py`.
4. The builder creates the whole bundle transactionally, writes `built-data`, and queues six unique art requests.
5. The Facet sidecar and art attachment passes enrich that same recorded bundle.
6. The daily digest reads and reports committed state. It never creates objects.

The full contract and ownership boundaries are in `../PIPELINE.md`.

**Hard rule:** no agent or playbook manually calls the Dream, Character, Reward, Scenario, DreamRelation, or PitchSheet creation endpoints for daily dreams. `scripts/build_dream_records.py` is the sole object writer. A failed bundle is retried by the builder, not continued by hand.

## What the recurring task may do for dreams

During an idle cycle, dream-cycle/t-006 may:

- scan proposal and idea files for new Notes from Silas,
- author today's missing proposal from `build_dream_proposal.py --brief`,
- adapt a legacy idea outline into the canonical six-asset proposal shape,
- inspect the builder's durable success/retry status,
- verify Facet and art completion,
- replenish the idea runway.

It must not advance a dream through direct object-creation stages.

## Queue and steering

### Daily proposals

Exactly one proposal may exist per Pacific date. Proposal files are selected by the scheduled builder only after their steering day. Their meaningful states are:

- `outline` or `approved`: waiting for the canonical builder,
- `parked` or `vetoed`: never selected,
- `built`: completed bundle recorded in `built-data`,
- retry evidence: pinned in `build-attempt-data` while remaining eligible.

Daily proposals do not use `status: building`; the transaction is owned by the builder and either completes or rolls back.

### Legacy dream outlines

Non-proposal dream outlines are idea inventory. Agents may mine them when authoring a future proposal, but they are not independently buildable and never receive direct API stages. The partially created Lantern Post card is parked as the historical record of the retired staged experiment.

### Delegated creation types

Types whose output belongs to a home project, such as `coloring-book`, may still use a multi-cycle playbook. For those only:

- the backlog card is the scheduler and steering surface,
- the home project's files and roadmap are authoritative,
- only one delegated creation may be `building`,
- never double-claim a home task already held by another Worker,
- keep the card Build log and home project state synchronized.

The one-building invariant applies to these delegated multi-stage types, not to daily-dream database writes.

## Playbook requirement

A delegated type is buildable only when `specs/<type>.md` exists. An idea with no playbook waits without blocking other work. `specs/dream.md` documents the canonical proposal pipeline rather than a second implementation.

## Reversibility and evidence

Daily-dream rows are traceable through the builder's `designer`, source metadata, and `built-data` ledger. Every successful bundle records its actual model IDs before enrichment. Every failure records a retry marker and leaves no claimed success. Art request IDs are stable and unique.

For delegated file-based creations, retain equivalent source, prompt, and provenance metadata in the home project.

## Backlog replenishment

Keep at least five usable dream ideas or active delegated scheduler cards available. Replenishment creates outlines, not database rows. A new idea becomes live content only after it is adapted into a dated canonical proposal and built by the sole writer.

## Hard gates

Publishing, POD accounts, store listings, spend, billing, production deploys, secrets, DNS, schema changes, and destructive cleanup remain human-gated. Internal generated art is reversible and pre-approved under `AGENTS.md`; originality and licensing rules still apply.

## Health guard

`python scripts/check_daily_dream_pipeline.py` verifies the single-writer boundary and runs in Daily Dream Contract CI. Any reintroduction of a parallel direct-REST dream playbook is a contract failure.
