# Playbook: `type: dream`

**Canonical pipeline:** `../PIPELINE.md`  
**Sole object writer:** `scripts/build_dream_records.py`

A daily dream is a coherent six-asset bundle. This playbook governs authoring, steering, creation evidence, ArtJob handoff, and reporting. It does not authorize a second implementation of the object builder.

## Bundle contract

Every new daily proposal contains exactly:

1. one dream vibe,
2. one dream location,
3. one Character,
4. one ITEM Reward,
5. one SKILL Reward,
6. one Scenario authored last from the completed vibe, location, and Character.

Daily bundles do not include a narrator. Older, larger dream outlines remain idea inventory and may be adapted into this shape.

## Creative seed contract

Before authoring the world, use `scripts/build_dream_proposal.py --brief` to obtain the deterministic Facet plan for the Pacific date. The plan includes:

- two umbrella GENRE Facets,
- one ANIMAL or SPECIES Facet,
- one OCCUPATION Facet,
- one additional GENRE per dependent element,
- applicable MATERIAL and PERSONALITY Facets.

The Facets are creative constraints, not labels pasted on afterward. Each seed must materially affect the content and visible art direction. Avoid concepts that remain unchanged when the seeds are removed.

## Stage A — author today's next proposal

The scheduled morning Daily Digest cycle begins with:

```bash
python scripts/author_dream_proposal.py
```

That command is idempotent. When the current Pacific date already has a proposal it leaves it untouched; otherwise it uses the deterministic brief and canonical validator to create one coherent six-asset steering proposal.

The proposal file contains `proposal-data` and creates no kind_robots objects. It is the input for the **next** build, not one of the two showcase generations in the email sent moments later.

## Stage B — steering day

Until the proposal date has passed in Pacific time:

- Silas may add notes, change priority, park, or veto the proposal.
- Agents read and fold in Notes from Silas without editing the Notes section itself.
- No database object creation occurs.

A proposal with substantive notes is not built until an agent has incorporated them into the proposal data. Parked and vetoed proposals are never selected.

## Stage C — one transactional object build

After today's proposal has been ensured, the same morning workflow invokes `scripts/build_dream_records.py` exactly once. That script alone owns all model writes and relationship wiring for the bundle.

The builder must:

- choose one eligible prior proposal or pinned retry,
- create the complete six-asset bundle and its grouping metadata,
- link dependent records to the world,
- record every resulting ID in `built-data`,
- stage one stable, unique card-art request for each of the six assets,
- roll back a partial attempt,
- leave a durable retry marker and failed workflow result when completion fails.

**Do not manually continue, repair, or imitate a partial build through direct REST calls.** Repair the builder or its input, then let the same transaction retry.

## Stage D — Facets and ArtJob handoff

Immediately after the bundle ledger exists, the morning workflow runs `scripts/apply_daily_dream_facets.py` against those recorded targets. This enriches the completed bundle; it does not create a second one.

Then `scripts/submit_daily_dream_art.py` submits staged `source: dream-cycle` requests to the real Kind Robots ArtJob queue. The submitter records each returned `last_art_job_id` immediately and does **not** wait for rendering.

The relay owns those in-flight jobs. The broad auto-art consumer will not repost a Daily Dream request that already carries an ArtJob id unless its target media is live and the row is ready to be marked done.

## Stage E — commit, then digest reporting

The workflow commits proposal/build/art-request evidence before assembling the digest.

The email deliberately shows two completed generations with different layouts:

1. **Previous completed output** — the older completed bundle, with large art areas because its renders have had a full cycle to finish.
2. **Just built this cycle** — the newest completed bundle, with records, summaries, and seed Facets but no reserved image boxes. Its ArtJobs were only just submitted and its images belong in the next digest cycle.

Today's freshly authored steering proposal is retained in digest JSON for diagnostics but is not rendered as a third near-identical section.

Report missing art honestly in the older art-rich section. For the just-built section, report ArtJob submission count as text rather than drawing six empty image placeholders.

## Hourly Conductor

Hourly Conductor is report-only for Daily Dream. It does not build objects, attach Daily Dream Facets, or submit Daily Dream art. This prevents a midnight or other hourly sweep from getting ahead of the ordered morning cycle.

## Slugs, metadata, and reversibility

The world proposal owns the bundle slug. Element slugs and art paths are generated consistently by the builder. Autonomous output uses `creationSource: "AI"`; use `HYBRID` only when Silas materially seeded the proposal.

Every completed bundle must be traceable through `designer: "dream-cycle"`, proposal date, source slug, recorded model IDs, Facet targets, stable art-request IDs, and submitted ArtJob IDs. Cleanup or reconciliation is separately scoped; the normal pipeline never performs broad deletion.

## Legacy staged experiment

The former eight-stage manual playbook was retired on 2026-08-02 because it was a parallel object writer. It partially created Lantern Post before the canonical six-asset transaction existed. That card is parked and retained as historical evidence. No future agent resumes its Character, Reward, Scenario, narrator, or art stages.

A useful concept from any legacy outline may inspire a future dated proposal, but the future bundle must enter through the canonical proposal path and be created only by `build_dream_records.py`.

## Verification

Run:

```bash
python scripts/check_daily_dream_pipeline.py
python -m pytest -q tests/test_daily_dream_pipeline_contract.py tests/test_daily_dream_bundle_art_queue.py tests/test_build_dream_records.py tests/test_enrich_daily_dream_digest.py tests/test_build_digest_email_v2.py tests/test_submit_daily_dream_art.py
```

Daily Dream Contract CI runs the ordered-cycle guard plus the broader proposal, builder, Facet, digest, ArtJob, and email contracts.
