# Daily Dream pipeline

This is the canonical end-to-end contract for the Daily Dream. There is one object-creation path and one ordered morning cycle.

## The path

```text
Daily Digest morning cycle
    ↓
author today's six-asset steering proposal
    ↓
build digest JSON/email from the most recent ALREADY BUILT bundle
    ↓
freeze today's email payload
    ↓
build TODAY'S proposal into six live records for TOMORROW
    ↓
attach Facets + submit six durable priority ArtJobs
    ↓
commit proposal/build/ArtJob evidence
    ↓
send the already-frozen digest
    ↓
~24 hours of render runway before those ArtJobs appear in tomorrow's digest
```

In shorthand, the workflow contract is:

**author → freeze digest → build today for tomorrow → Facets → submit ArtJobs → commit → send frozen digest**

There is still one writer and one morning workflow. The difference is temporal ownership:
the bundle shown in today's email was prepared by the prior cycle, while today's newly
authored proposal is prepared immediately after the email payload is frozen so its art has
roughly a full day to render.

## 1. Author today's proposal

At the start of the scheduled morning cycle, `scripts/author_dream_proposal.py` ensures
that the current Pacific date has one canonical six-asset proposal. Authoring is
idempotent and creates no database objects by itself.

## 2. Freeze today's digest from prior completed work

Before any records or ArtJobs are created for today's proposal, the workflow runs
`build_digest.py`, `enrich_daily_dream_digest.py`,
`annotate_daily_dream_art_queue.py`, validation, and the email renderer. The resulting
payload therefore describes work that already existed before this morning's preparation
step. Its ArtJobs normally have had about 24 hours to render.

This ordering is deliberate. A longer same-cycle wait is not a substitute for the
one-day pipeline: digest morning must not be the generation starting gun for the art it
is about to showcase.

## 3. Build today's proposal for tomorrow

After the email payload is frozen, `scripts/run_daily_dream_build.py --date <today>`
delegates to `scripts/build_dream_records.py`, the **sole object writer**. The explicit
Pacific date allows the proposal to be built during its own morning cycle rather than
waiting until it becomes "prior" the next day.

The builder creates the complete six-object bundle transactionally, records every
resulting ID in `built-data`, and writes exactly six stable art requests to
`projects/art-prompts.yaml`. Immediately afterward,
`scripts/apply_daily_dream_facets.py` attaches the persisted Facets.

## 4. Submit tomorrow's art immediately

`scripts/submit_daily_dream_art.py` submits the six newly staged `source: dream-cycle`
requests to Kind Robots and records each durable `last_art_job_id`. It does not wait
for those renders, because they are not needed by the already-frozen email. The normal
renderer now has the rest of the day and overnight to complete them.

## 5. Persist evidence, then send the frozen email

The workflow commits today's proposal/build/Facet/ArtJob evidence before sending the
payload that was frozen in step 2. Sidecar preparation failures remain warnings so a
problem preparing tomorrow cannot erase today's otherwise valid digest.

The next morning, that prepared bundle becomes the newest completed output and its public
art paths are probed for the digest. Missing or failed art remains visible as an honest
status rather than being silently replaced or re-enqueued.

## 6. Hourly Conductor remains report-only

Hourly Conductor does not create Daily Dream objects, attach Daily Dream Facets, or submit
Daily Dream art. Keeping the morning workflow as the sole writer preserves the
single-writer/race-safety repair while the reordered cycle restores the intended
generation runway.

## Failure and retry behavior

The Daily Digest retry watchdog may rerun the same workflow after a failed or missing run. Every creation boundary is designed to be retry-safe:

- authoring is idempotent by proposal date;
- the builder pins failed proposals and adopts exact matching partial identities where appropriate;
- art request IDs are stable;
- Daily Dream ArtJobs use stable idempotency keys;
- recorded `last_art_job_id` values prevent the digest from claiming a request is queued before a real ArtJob exists.

A failed morning cycle should be retried as a cycle. Stable request IDs and recorded ArtJob IDs make tomorrow-preparation idempotent without letting Hourly Conductor quietly advance only one piece of it.

## Freshness: old proposals are poisoned, not queued

An ordinary unbuilt proposal older than the two-day freshness window is a poisoned build
artifact and is never built as written. `scripts/run_daily_dream_build.py` owns that
policy (`MAX_AUTOBUILD_AGE_DAYS`) and re-runs `check_dream_creative_contract.py` against
every candidate at build time — pinned retries and explicit `--date` backfills included,
so neither exception can smuggle an old proposal past today's creative rules.

Poisoned proposals stay useful as idea inventory. Mine the kernel into a fresh dated
proposal; never resurrect one wholesale.

## Remastering what is already built

The built catalog is mutable creative material. `specs/REMASTER.md` documents the
recurring freshness pass: `scripts/audit_dream_catalog.py` classifies every built bundle
under today's rules, and `scripts/remaster_dream_catalog.py` applies the result in waves —
in-place text revisions through `apply_dream_revision.py`, art-only regeneration staged
through the same `projects/art-prompts.yaml` ledger a normal morning uses, and a legacy
canonicalization lane that remasters the six canonical rows of a pre-v2 staged bundle and
retires its leftover rows rather than deleting them.

The remaster creates no objects. It patches existing rows and stages art;
`build_dream_records.py` remains the sole object writer.

## Legacy staged builds

The former eight-stage `type: dream` playbook was retired on 2026-08-02. It was a second object writer and had already left partial creations. Legacy non-proposal outlines remain useful as idea inventory, but they are never resumed with direct API calls. To reuse one, adapt its concept into a canonical six-asset proposal.

Existing rows from historical partial builds are retained unless a separately scoped cleanup explicitly reconciles them.

## Continuous health check

Run:

```bash
python scripts/check_daily_dream_pipeline.py
```

CI enforces that:

- Daily Digest authors exactly once at the start;
- only Daily Digest invokes the Daily Dream object writer and ArtJob submitter;
- authoring, build, Facets, ArtJob submission, evidence commit, and digest rendering occur in that order;
- Hourly Conductor uses the report-only entrypoint;
- active dream specs still identify `build_dream_records.py` as the sole object writer;
- retired direct-REST stage instructions do not return.
