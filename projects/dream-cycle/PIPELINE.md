# Daily Dream pipeline

This is the canonical end-to-end contract for the Daily Dream. There is one object-creation path and one ordered morning cycle.

## The path

```text
Daily Digest morning cycle
    ↓
author today's six-asset steering proposal
    ↓
build the now-eligible prior proposal
    ↓
scripts/build_dream_records.py
    ↓
kind_robots rows + built-data ledger + six stable art requests
    ↓
scripts/apply_daily_dream_facets.py
    ↓
scripts/submit_daily_dream_art.py
    ↓
six durable Kind Robots ArtJobs with recorded IDs
    ↓
commit proposal/build/ArtJob evidence
    ↓
build and send the digest
    ↓
older completed bundle WITH art
then the just-built bundle WITHOUT empty art space
```

In shorthand, the workflow contract is:

**author → build → Facets → submit ArtJobs → commit → digest**

There is no second authoring step after the email.

## 1. Author today's next proposal

At the start of the scheduled morning cycle, `scripts/author_dream_proposal.py` ensures that the current Pacific date has one canonical six-asset proposal:

- one dream vibe
- one dream location
- one Character
- one ITEM Reward
- one SKILL Reward
- one Scenario, authored from the completed preceding elements

The proposal is steering input for the **next** build. It creates no database objects and is not shown as a third Daily Dream showcase in that morning's email.

Silas may still add notes, park, or veto a proposal during its steering day. The authoring command is idempotent, so an already-authored proposal is left alone.

## 2. Build the prior eligible proposal

`scripts/build_dream_records.py` is the **sole object writer** for Daily Dream objects.

After authoring today's proposal, `daily-digest.yml` invokes the builder exactly once. The builder selects the oldest pinned retry when one exists; otherwise it selects the newest valid proposal whose Pacific proposal date is earlier than today.

The builder creates the complete six-object bundle transactionally, records every resulting ID in `built-data`, writes exactly six stable art requests to `projects/art-prompts.yaml`, and rolls back partial creation when an API write fails. No agent manually reproduces its REST calls.

Immediately afterward, `scripts/apply_daily_dream_facets.py` attaches the proposal's persisted Facets to the completed records.

## 3. Submit art before the email

The six builder-created art requests are a Conductor staging ledger, not yet Kind Robots ArtJobs.

`scripts/submit_daily_dream_art.py` closes that boundary before the digest is built. It processes only `source: dream-cycle` requests, submits each to the Kind Robots ArtJob queue, and immediately records `last_art_job_id` back on the durable request row. It does **not** wait for renders to finish.

Daily Dream ArtJobs use the reserved priority tier and stable request IDs. The normal relay/art pipeline renders them after submission and writes Kind Robots media targets directly when complete.

## 4. Commit evidence, then render the digest

The workflow commits the newly authored proposal, built-data changes, Facet evidence, staged request changes, and recorded ArtJob IDs before constructing the email. The digest therefore reports durable state rather than optimistic in-process state.

The email has two Daily Dream showcase sections in this order:

1. **Previous completed output**: the completed bundle before the one built this morning. This is the art-rich section because its renders have had a full cycle to finish. Missing art is reported honestly when necessary.
2. **Just built this cycle**: the bundle built moments ago. It shows the six records, summaries, and seed Facets in a compact layout with **no reserved image boxes**. Its newly submitted art belongs to the next cycle's art-rich section.

Today's newly authored steering proposal is retained in digest JSON for diagnostics but is not rendered as another near-identical card grid.

## 5. Hourly Conductor is report-only

Hourly Conductor no longer creates Daily Dream objects, attaches Daily Dream Facets, or submits Daily Dream art. Its workflow calls `scripts/build_conductor_summary_report_only.py`, which preserves the existing health-report implementation while neutralizing its historical `ensure_records()` side effect.

This prevents midnight and other hourly runs from building a proposal before the ordered morning sequence.

## Failure and retry behavior

The Daily Digest retry watchdog may rerun the same workflow after a failed or missing run. Every creation boundary is designed to be retry-safe:

- authoring is idempotent by proposal date;
- the builder pins failed proposals and adopts exact matching partial identities where appropriate;
- art request IDs are stable;
- Daily Dream ArtJobs use stable idempotency keys;
- recorded `last_art_job_id` values prevent the digest from claiming a request is queued before a real ArtJob exists.

A failed morning cycle should be retried as a cycle, rather than letting Hourly Conductor quietly advance only one piece of it.

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
