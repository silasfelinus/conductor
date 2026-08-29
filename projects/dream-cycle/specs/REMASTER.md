# REMASTER.md — the Daily Dream catalog freshness pass

**Issue:** [conductor#3184](https://github.com/silasfelinus/conductor/issues/3184) ·
**Canonical daily pipeline:** [../PIPELINE.md](../PIPELINE.md) ·
**Creative rules:** [../CREATIVE-SEED-CONTRACT.md](../CREATIVE-SEED-CONTRACT.md)

The Daily Dream catalog is mutable creative material, not sacred sunk work. This spec
covers the recurring pass that re-reads the whole built catalog under *today's* rules and
improves it in place — and the guard that stops old proposals from re-entering the build
lane as if nothing had been learned since they were written.

It does not replace `PIPELINE.md`. The morning cycle still owns creation, and
`build_dream_records.py` is still the only object writer. The remaster only ever
**patches** rows that already exist, **stages** art through the same
`projects/art-prompts.yaml` ledger a normal day uses, and **retires** what no longer
deserves to survive.

## 1. Poisoned proposals

An ordinary unbuilt proposal older than the two-day freshness window is poisoned as a
build artifact. `scripts/run_daily_dream_build.py` refuses to select it
(`MAX_AUTOBUILD_AGE_DAYS`), and every candidate — fresh, pinned retry, or explicit
`--date` backfill alike — is re-run through `check_dream_creative_contract.py` at build
time, so age is not the only thing an old proposal has to survive.

Two exceptions, both narrow:

* a **pinned retry** may be older than the window, because it represents a transaction
  that already started; it still re-clears the creative contract;
* an **explicit `--date` backfill** may name an older proposal on purpose; it also still
  re-clears the creative contract.

A poisoned proposal is not worthless — it is idea inventory. Mine its kernel into a fresh
dated proposal through the current contract. Never resurrect one wholesale.
`audit_dream_catalog.py` lists them under `poisoned_unbuilt` every run.

## 2. Audit — `scripts/audit_dream_catalog.py`

Read-only. Never calls Kind Robots. Writes:

* `projects/dream-cycle/remaster/catalog-audit.json` — the machine-readable manifest;
* `projects/dream-cycle/remaster/CATALOG-AUDIT.md` — the reviewable report.

Every built bundle is scored on signals the live contract cannot see, because the live
contract only ever judges one unbuilt proposal against a short history window:

| Signal | What it catches |
| --- | --- |
| Motif families (`dream_creative_ruts.py`) | ledgers, archives, cozy markets/workshops, towers and lighthouses, repeated occupational archetypes — weighted ×3 when the motif reached an asset *name* |
| Catalog saturation | a family carried by ≥30% of the catalog counts against a bundle **even when that day's Facets asked for it**; the fifteenth permit office is still the fifteenth permit office |
| Premise echo | distinctive-vocabulary overlap against the whole catalog, not a 12-day window |
| Naming | ornamental noun surnames, civil-service honorifics, catalog-wide name vocabulary reuse |
| Facet fusion | an assigned Facet whose vocabulary never reaches the prose was pasted on |
| Visual fields | missing, thin, materially empty, or person-shaped `look` / `art_direction` — the failure CREATIVE-SEED-CONTRACT.md documents |

Scores map to the issue's four bands: `keep` (≤2), `light-refresh` (3–5),
`substantial-rewrite` (6–8), `retire-replace` (≥9).

**Art carries its own verdict**, computed independently of the text one:

* `regenerate` — the text is changing, the renders came from weak visual fields, or the
  renders never attached;
* `restyle` — the prose and images are fine, but the world sits in an overcrowded style
  lane and should move to a different visual language;
* `keep-art`.

A bundle whose proposal predates the version-2 shape is marked `legacy_shape`. It cannot
take an ordinary in-place revision (see wave 2 below) and routes to the legacy
canonicalization lane instead.

## 3. Remaster — `scripts/remaster_dream_catalog.py`

Dry-run by default; every applied batch leaves a receipt under
`projects/dream-cycle/remaster/receipts/`.

```bash
python scripts/audit_dream_catalog.py                    # manifest first, always
python scripts/remaster_dream_catalog.py plan            # group into waves
python scripts/remaster_dream_catalog.py stubs --apply   # emit rewrite stubs
python scripts/remaster_dream_catalog.py art --apply     # stage replacement renders
python scripts/submit_daily_dream_art.py                 # canonical ArtJob submission
python scripts/remaster_dream_catalog.py verify          # post-pass validation
```

### Wave 1 — rewrite in place

`stubs` writes one `<date>-remaster-<slug>-stub.json` per bundle into
`projects/dream-cycle/revisions/`, carrying the current proposal and the audit's specific
complaints. An authoring pass rewrites `proposal`, then renames the file to
`-request.json`; only then will `apply_dream_revision.py` pick it up, patch the live rows,
supersede the old art, and queue six replacement renders. A half-finished rewrite is inert
by construction.

Rewrites must preserve `seed_facets` byte-for-byte and keep the technical world `slug`
(the rows and their image directory are keyed to it). Everything else — names, prose,
premise, visual direction — is fair game. Renaming the same premise is not a rewrite.

### Wave 2 — legacy canonicalization

The four 2026-07 bundles left over from the retired eight-stage experiment are not
six-asset bundles at all: each carries a second vibe Dream, two locations, three
characters, two Scenarios, and a narrator Bot, and none of them has a `seed_facets` block.
Two rules therefore cannot both be honoured — "preserve `seed_facets` exactly" is
unsatisfiable for a bundle that never had one, and "patch the canonical six rows" is
unsatisfiable for a bundle that has eleven.

A request carrying `"legacy_reseed": true` resolves both, and only for bundles that
genuinely predate the contract:

* the seed exemption applies **only** when the old proposal fails today's schema on
  `seed_facets`, and the replacement must itself be a valid version-2 block. The plan is
  not invented: `build_dream_proposal.facet_seed_plan(day)` is deterministic per date, so
  a legacy bundle receives exactly the Facets its own date would draw today;
* the patcher remasters the canonical six rows — world, first live location, first live
  character, both Rewards, first live Scenario — skipping any row whose record has since
  been deleted;
* every superseded row (the second vibe Dream, extra locations, extra characters, the
  second Scenario) is **retired, not deleted**: `isActive` and `isPublic` go false, and
  each is recorded under `retired_legacy_rows` in `built-data` with its reason;
* narrator Bots are left alone and merely recorded under `legacy_narrator_left_in_place`,
  because they belong to the separately scoped cleanup PIPELINE.md describes;
* `built-data.records` is rewritten to the canonical six, so the bundle is an ordinary
  bundle from then on and never needs this lane again.

The technical world `slug` is preserved here exactly as in wave 1.

### Wave 3 — art only

For bundles whose prose survives. The lane rebuilds all six prompts against a deliberately
different visual language — `visual_language()` combines one of twelve media with one of
ten camera/palette/light treatments, and the remaster walks a world one or two lanes off
its default so a restyle never lands back where it started — appends the requests to
`projects/art-prompts.yaml` with `entity_type`/`entity_id`/`entity_field` bound to the live
rows, and moves the previous evidence into `superseded_art` in `built-data`. Prose is not
touched. `submit_daily_dream_art.py` carries the requests into real ArtJobs, exactly as on
a normal morning.

Art generation is in-house and effectively free, so this lane does not preserve renders to
save generation. It *does* refuse to spend renders on a bundle that is about to be
rewritten or retired — that is thrift about coherence, not cost. Pass `--include-rewrites`
to override.

### Wave 4 — keep

Left alone, and recorded as such, so the next pass can tell "reviewed and kept" from
"never looked at."

## 4. Verify

`remaster_dream_catalog.py verify` re-reads every recorded entity (`--offline` checks local
evidence only), confirming the row still resolves, still carries an `imagePath`, and that
each bundle has art evidence in `built-data`. It exits non-zero when anything is missing,
so a wave can be checked before the next one starts.

## 5. Reversibility

Text mutations move through `apply_dream_revision.py`, which validates before it PATCHes
and leaves an `-applied.json` receipt. Every superseded render stays listed in
`superseded_art`, and each art wave records its stamp, variant, and request IDs under
`remasters` in `built-data`. Retiring or replacing a Scenario or Reward is explicitly
allowed by the issue; gratuitous identity churn is not — preserve record IDs wherever an
in-place remaster stays coherent.
