# Playbook: `type: dream`

**Canonical pipeline:** `../PIPELINE.md`  
**Sole object writer:** `scripts/build_dream_records.py`

A daily dream is a coherent six-asset bundle. This playbook governs authoring, steering, creation evidence, and reporting. It does not authorize a second implementation of the object builder.

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

## Stage A — author one proposal

A sweeping agent checks current state:

```bash
python scripts/build_dream_proposal.py --check --fetch
```

If the date is missing, the agent:

1. reads `python scripts/build_dream_proposal.py --brief`,
2. authors one coherent JSON object matching the exact six-asset contract,
3. validates and writes it with `--from-json`,
4. commits the resulting backlog file promptly so the origin/main duplicate-date guard can protect concurrent sessions.

The proposal file is the steering artifact and contains `proposal-data`. Authoring it creates no kind_robots objects.

## Stage B — steering day

Until the proposal date has passed in Pacific time:

- Silas may add notes, change priority, park, or veto the proposal.
- Agents read and fold in Notes from Silas without editing the Notes section itself.
- No database object creation occurs.

A proposal with substantive notes is not built until an agent has incorporated them into the proposal data. Parked and vetoed proposals are never selected.

## Stage C — one transactional object build

Hourly Conductor runs `scripts/build_conductor_summary.py`, which invokes `build_dream_records.ensure_records()` exactly once. `scripts/build_dream_records.py` alone owns all model writes and relationship wiring for the bundle.

The builder must:

- choose one eligible proposal or pinned retry,
- create the complete six-asset bundle and its grouping metadata,
- link dependent records to the world and main vibe,
- record every resulting ID in `built-data`,
- queue one stable, unique card-art request for each of the six assets,
- roll back a partial attempt,
- leave a durable retry marker and failed workflow result when completion fails.

**Do not manually continue, repair, or imitate a partial build through direct REST calls.** Repair the builder or its input, then let the same transaction retry.

## Stage D — Facets and art

Immediately after the bundle ledger exists, the hourly workflow runs `scripts/apply_daily_dream_facets.py` against those recorded targets. This enriches the completed bundle; it does not create a second one.

The shared art pipeline renders the six queued requests. Later builder attachment passes update each real model when its public asset is available. Request IDs prevent repeated sweeps from duplicating queue entries.

## Stage E — digest reporting

The daily digest reads committed proposal and `built-data` evidence, enriches the six cards with Facets and art state, validates the payload, and renders the email. It never receives `KR_API_TOKEN` and never calls an object-writing script.

Report states honestly:

- proposed and waiting for its steering day,
- pinned retry / creation failed,
- built with recorded object IDs,
- art queued,
- art rendered,
- art attached.

Do not substitute the newest historical success when the exact prior Pacific date failed or is missing.

## Slugs, metadata, and reversibility

The world proposal owns the bundle slug. Element slugs and art paths are generated consistently by the builder. Autonomous output uses `creationSource: "AI"`; use `HYBRID` only when Silas materially seeded the proposal.

Every completed bundle must be traceable through `designer: "dream-cycle"`, proposal date, source slug, recorded model IDs, Facet targets, and stable art-request IDs. Cleanup or reconciliation is separately scoped; the normal pipeline never performs broad deletion.

## Legacy staged experiment

The former eight-stage manual playbook was retired on 2026-08-02 because it was a parallel object writer. It partially created Lantern Post before the canonical six-asset transaction existed. That card is parked and retained as historical evidence. No future agent resumes its Character, Reward, Scenario, narrator, or art stages.

A useful concept from any legacy outline may inspire a future dated proposal, but the future bundle must enter through `build_dream_proposal.py` and be created only by `build_dream_records.py`.

## Verification

Run:

```bash
python scripts/check_daily_dream_pipeline.py
python -m pytest -q tests/test_daily_dream_pipeline_contract.py tests/test_daily_dream_bundle_art_queue.py tests/test_build_dream_records.py tests/test_build_digest.py tests/test_enrich_daily_dream_digest.py
```

Daily Dream Contract CI runs the single-writer guard plus the broader proposal, builder, Facet, digest, and email contracts.
