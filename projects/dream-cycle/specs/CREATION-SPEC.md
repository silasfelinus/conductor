# CREATION-SPEC.md — the creation loop contract

**Task:** dream-cycle/t-004 · **Canonical daily-dream pipeline:** `../PIPELINE.md`

This is the type-agnostic contract for dream-cycle's idle capacity. Per-type mechanics live in `specs/<type>.md`. When this file and a playbook conflict, this file governs queueing and ownership; the playbook governs only the type-specific work.

## When the loop runs

dream-cycle sits last in `projects/priority.yaml`, so its recurring task is selected only when no other active project has ready work. It consumes leftover capacity rather than competing with ordinary product work.

## One daily-dream object path

`type: dream` is not a staged REST build anymore. Daily-dream objects follow one path only:

1. The morning Daily Digest cycle ensures today's six-asset proposal exists.
2. Today's proposal remains steering input for the next build.
3. The same workflow invokes `scripts/build_dream_records.py` once for the now-eligible prior proposal.
4. The builder creates the whole bundle transactionally, writes `built-data`, and stages six unique art requests.
5. `scripts/apply_daily_dream_facets.py` enriches that same recorded bundle.
6. `scripts/submit_daily_dream_art.py` converts the staged dream-cycle requests into durable Kind Robots ArtJobs and records their IDs without waiting for renders.
7. The workflow commits that evidence, then renders the digest.
8. Hourly Conductor remains report-only and never advances Daily Dream creation.

The full contract and ownership boundaries are in `../PIPELINE.md`.

**Hard rule:** no agent or playbook manually calls the Dream, Character, Reward, Scenario, DreamRelation, or PitchSheet creation endpoints for daily dreams. `scripts/build_dream_records.py` is the sole object writer. A failed bundle is retried by the builder, not continued by hand.

## What the recurring task may do for dreams

During an idle cycle, dream-cycle/t-006 may:

- scan proposal and idea files for new Notes from Silas,
- inspect today's proposal and replenish idea inventory,
- adapt a legacy idea outline into the canonical six-asset proposal shape,
- inspect the builder's durable success/retry status,
- verify Facet, ArtJob, and art completion,
- repair pipeline drift without manually creating dream objects.

It must not advance a dream through direct object-creation stages.

## Queue and steering

### Daily proposals

Exactly one proposal may exist per Pacific date. Proposal files are selected by the scheduled morning builder only after their steering day. Their meaningful states are:

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

## Digest presentation contract

The email intentionally shows two completed generations, not the new steering proposal:

1. the older completed bundle with art, because its renders have had a full cycle to finish;
2. the bundle just built that morning in a compact text/Facet layout with no reserved image boxes.

The art submitted for the just-built bundle is expected to graduate into the art-rich section on the next cycle.

## Playbook requirement

A delegated type is buildable only when `specs/<type>.md` exists. An idea with no playbook waits without blocking other work. `specs/dream.md` documents the canonical proposal pipeline rather than a second implementation.

## Reversibility and evidence

Daily-dream rows are traceable through the builder's `designer`, source metadata, and `built-data` ledger. Every successful bundle records its actual model IDs before enrichment. Every failure records a retry marker and leaves no claimed success. Art request IDs are stable and unique, and submitted ArtJob IDs are recorded durably before the digest is built.

For delegated file-based creations, retain equivalent source, prompt, and provenance metadata in the home project.

## Backlog replenishment

Keep at least five usable dream ideas or active delegated scheduler cards available. Replenishment creates outlines, not database rows. A new idea becomes live content only after it is adapted into a dated canonical proposal and built by the sole writer.

## Hard gates

Publishing, POD accounts, store listings, spend, billing, production deploys, secrets, DNS, schema changes, and destructive cleanup remain human-gated. Internal generated art is reversible and pre-approved under `AGENTS.md`; originality and licensing rules still apply.

## Health guard

`python scripts/check_daily_dream_pipeline.py` verifies the single-writer boundary and ordered morning sequence in Daily Dream Contract CI. Any reintroduction of a parallel direct-REST dream playbook is a contract failure.
