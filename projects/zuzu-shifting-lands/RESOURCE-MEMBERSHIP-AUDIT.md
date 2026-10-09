# Shifting Lands: resource identity and membership audit

**Scope:** Zuzu world reuse, `zuzu-shifting-lands/t-004`, private admin-only draft.
**Source of candidate truth:** [worlds/zuzu/resource-submissions.json](../../worlds/zuzu/resource-submissions.json), schema 1, `prepared-not-applied`.
**Source of lore truth:** [worlds/zuzu/catalog.json](../../worlds/zuzu/catalog.json), Book One, latest Cast Picks, Video Guardrails, and Silas's world guide. A candidate or database row is not automatically canon.

## Count the candidates, not imaginary database rows

The current **submission** lists 9 named Character candidates, 5 Scenario candidates, 5 Reward candidates, and 5 LoRA/Resource candidates: **24 proposed identities**. These counts are verified from source JSON, **not** counts from the live database. Do not copy these into runtime data without owner-scoped reconciliation.

The Kind Robots Zuzu World Studio now has a read-only, admin-only `/api/worlds/zuzu/resource-audit` endpoint and an in-place "Resource identity audit" disclosure. It reads Conductor's submitted identities and compares them with the **authenticated administrator's owned, active, maturity-eligible rows**. A slug match is a candidate record to inspect, not license to overwrite its story text; a name-only or LoRA-trigger match must be explicitly reviewed. Ambiguous and missing matches must never be auto-created. IDs are displayed only inside the authenticated Admin studio, not fabricated into this repository.

This source audit cannot validate currently deployed counts or confirm any live resource ID. It becomes an operational audit **only when run against an authenticated live Kind Robots database**. A failed Conductor source fetch is an error, not zero candidates; limited maturity/ownership visibility is not proof that the resource does not exist.

## Stable membership without schema duplication

| Asset | Existing source of truth | Zuzu-world membership | Role in encounters |
| --- | --- | --- | --- |
| Species, occupations, roles, archetypes, settings | `Facet` and `FacetProfile` | `FacetProfile.metadata.worlds=["zuzu"]`, optional `landIds`, `randomWeight` and scope provenance | Separately drawn SPECIES + OCCUPATION/ROLE; affiliation, secret conditions and disposition are orthogonal |
| Named cast | Owned `Character` + `CharacterFacet` | Existing identified Character, explicit source/canon record and optionally Facet relations | Stable identity; **never** a random clone of Zuzu, Abbess or an established named actor |
| Encounter templates | Owned `Scenario` + `ScenarioFacet` | Source-backed Scenario ID/slug and world/lane Facet relations | Validated location conditions; hidden plot truth withheld from player until discovery |
| Gear, techniques, skills | Owned `Reward` + `RewardFacet` | Source-backed Reward ID/slug and world/role Facet relations | Equipment or persistent capability; run-level status and knowledge flags stay in save state |
| Artwork and video | Existing `ArtImage` and `ProjectArtImage` | Link a source ArtImage into the Shifting Lands Project | Illustration and media provenance, not a new copied image record |
| LoRA/checkpoint resources | Existing `Resource` | Verified owned Resource ID, slug/name/trigger and type | Reference for paid/allowed art pipeline; **never** treat a documented training-set recipe as a trained live Resource |

`metadata.worlds` records *eligibility for the world's reusable pool*, never canon authority. Provenance belongs alongside the tagged entity and the canonical Conductor source reference, not in a new parallel Zuzu database. Multiple worlds may reuse the same art or Facet, and an item may be tagged for Zuzu but still noncanonical/provisional. Admin tools should link and unlink the existing join rows, preserve source ownership and history, and require explicit identity-aware selection before any write.

### Matching and safe-change protocol

1. Load the 24 current candidates from the canonical submission file. Query only owned records in the authenticated session with content/maturity access enforced.
2. Compare **exact slugs**, then **exact display names**, then whole-token LoRA trigger words. Surface matching ID(s), source and ambiguity. Never infer an ID from old Dreams, generated lore, name fragments or legacy art filenames.
3. Confirm a source-backed actual row and the intended owner before patching. Preserve row ID, art links, private state, provenance, history and unrelated relations.
4. Propose Zuzu tags and `ProjectFacet` / `ScenarioFacet` / `RewardFacet` / `ProjectArtImage` joins as reversible changes. Make no automatic mass writes from the audit screen.
5. Every game encounter composes species, role and motive independently. Named Character snapshots retain known identity; anonymous compositional participants remain inside a saved run, never new Character rows.
6. Do not convert the Abbess's hidden agenda, missing-humanity mystery or player-facing clues into initial face-up cards; GitHub lore is fully readable to agents, while gameplay discovery must still be earned.
7. Only after authenticated live confirmation, record the confirmed IDs in an access-controlled implementation manifest or run-specific state; **never** copy guessed IDs or private runtime listings into public source.

## Verification gap and handoff

The source-ledger inventory and Kind Robots API implementation were inspected in GitHub. No `KR_API_TOKEN` was available in the execution environment for an authenticated production audit. Therefore **no live Character, Facet, Reward, Scenario, Resource, LoRA or ArtImage ID is claimed verified in this document**. The private admin UI supplies the missing live read after source merge/deploy. That operational confirmation and any tag edits remain follow-up work; `t-012` owns the eventual safe tagging/import API, not this read-only audit.
