# Daily Dream pipeline

This is the canonical end-to-end contract for the Daily Dream. There is one object-creation path and one ordered morning cycle.

## 2026-10-13 PT: fourteen-asset cutover (current)

The existing **sole object writer** remains `scripts/build_dream_records.py`.
The original Daily Dream continues as a complete six-asset linked mini-world
(vibe, its location, character, ITEM/SKILL rewards and scenario, one coherent
visual style). In **addition**, version-3 proposals create two Zuzu locations,
two characters, two rewards and two consequential-choice scenarios, one in each
category for Zuzu Gamebook and Emperor of Dust, with independent catalog Facets
and actual Arthemy/Illustrious SDXL checkpoint ArtJobs.

Exactly **14 distinct record ArtJobs** are staged and their targets retained in
`built-data`. One transaction, one rollback policy, one morning workflow;
historic built six-asset proposals stay readable and immutable. Future-dated
unbuilt six-asset buffered files remain idea inventory, without being erased
or silently promoted to a partial 14-asset run. The original Daily Dream keeps
its Krea art lane and Zuzu receives separate provenance and digest headings.
The operational ordering below is unchanged; old references to six requests
in its historical sections describe the version-2 lane only.

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

If the most recent completed Dream is already two or more Pacific calendar days
old, its art and records remain available in digest diagnostics, but its cards are
**not** resent as another newly featured Daily Dream. The email instead reports
that no fresh Dream was completed, including the actual last build date. Other
new daily project deliveries still appear as normal. A green digest-delivery run
must not be mistaken for a fresh creation.

## 3. Build today's proposal for tomorrow

After the email payload is frozen, `scripts/run_daily_dream_build.py --date <today>`
(with `DAILY_DREAM_SCHEDULED=1`) delegates to `scripts/build_dream_records.py`,
the **sole object writer**. It builds today's proposal when present. If today's
no-cost authoring step skips the date because the five-proposal buffer is full,
the scheduled builder instead consumes the oldest eligible, unbuilt proposal
from an earlier day. Manual `--date` calls still target only the requested date.
This prevents repeated completed worlds while valid proposals wait in the buffer,
without discarding earlier creative work or spending API credits.

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


## New-playbook daily challenge (2026-10-26 PT)

Separate from both the original 14-asset Daily Dream and the five **already-built**
daily project upgrades, each Pacific day's digest offers exactly three
unapproved, **evolving** game-playbook concepts for Silas to consider. The owner is the
Conductor session creative-docket step in `CLAUDE.md`, not a second scheduled
object creator. The digest workflow reads the dated, committed proposal file
`pitches/playbook-challenges/YYYY-MM-DD.yaml` through
`scripts/daily_playbook_challenge.py`, then renders the resulting budget and
seed/prose/art interactions in its own email section.

Before authoring: inspect the **current** Kind Robots `utils/playbook/games.ts`
registry and relevant Conductor active-project briefs, including Prom of Doom
and This Means Warp. Use `--brief` to see the eight-game baseline, the
full-history concept-memory shelf and genre-gap shortlist; use `--memory`
to inspect the indexed concept ancestry and editorial decisions in detail. **Silas's 2026-10-26 calibration is genre
first**: broad missing paradigms matter more than isolated clever mechanics.
Already represented genres include Weird West, post-apocalypse, superheroes,
slice of life, theatre of place, dark humor and psychedelia. Current missing
pillars: original family-friendly nonsense/literary children's adventure,
cyberpunk with evolved embodiment/identity rights mechanically represented,
and Heaven/Hell eternal soul-judgment simulator with cases, evidence, appeals
and downstream eternal consequences.

Each proposal must justify its genre gap, intended audience, full-act world
scope and emotional promise, plus **three or more genre-scale systems**. Then
explain the core loop, practical opening choices and disjoint playable/NPC/
follower cast counts. Count portraits by emotion and evolution, maps,
illustrations, friendship scenes (important for child-safe games), optional
romance, villain/conflict scenes, transformative moments, finale frames,
interface art and authored text beats; add model-pass estimates separately.
Identify at least three places where seed-driven state controls actual
prose and finished/generative art choices **and** changes what happens next.
Avoid borrowing named authors' exact styles, characters or stories. The
rejected first-pass 2026-10-26 concepts are preserved in the archive; the
live dated docket contains the three revised genre-calibrated pitches.

**Versioned creative memory:** dated dockets are preserved unchanged as
historical creative snapshots. Each pitch includes permanent `concept_id`,
`mode: new|expand|meld`, `parents` (prior `YYYY-MM-DD/slug` snapshots),
`evolution` (substantive new design work), `preserve`, `challenge` and
at least two specific `next_questions`. `expand` keeps the same concept ID
and cites exactly one earlier version; `meld` establishes a NEW ID and cites
at least two earlier DIFFERENT families; `new` has no ancestors. All three
modes occupy one of the day's three pitches. A date after a seed docket must
advance at least one existing lineage; do not force a merger where no
complementary premises exist. `pitches/playbook-challenges/MEMORY.yaml` is
the separate human/editorial ledger of statuses, strengths, guardrails,
creative tags and next moves, including rejected older attempts; it does
not edit or secretly endorse a historical proposal. Do not erase disagreements.

`scripts/playbook_pitch_memory.py` reads the **whole prior history**, builds
a stable version and concept tree, and ranks the curator shelf by explicit
editorial state and freshness, not arbitrary age-based forgetting. The
daily authoring brief uses that shelf, while each digest pitch shows its
`new/expand/meld` label, genealogy, changed/retained ideas and next questions.
`python scripts/daily_playbook_challenge.py --check --date YYYY-MM-DD`
enforces exactly **three** and rejects bad/missing ancestry, same-day
duplicates, historical copies masquerading as new, and rejected parents
without conscious editorial reactivation. `--payload` produces
`ready`, `invalid` or `missing`; only the exact Pacific-day `ready`
docket appears. An absent/invalid docket yields an honest notice and does
not recycle previous work. The system DOES NOT itself schedule or pay
for daily content authoring: a Conductor session must commit each day's
three versions before the morning digest. A concept is *not* a project,
approval, ArtJob, expense, or publication. Counts are planning estimates:
distinct render targets vs. optional multiple model passes per target and
authored scenes vs. editorial passes; no token or price guarantees.
