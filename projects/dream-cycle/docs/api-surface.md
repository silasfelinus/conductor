# Daily Dream write surface

**Current contract:** `../PIPELINE.md`
**Writer:** `scripts/build_dream_records.py` only

This document describes the current six-asset transaction. It is not an instruction for agents to reproduce the calls manually.

## Authentication

The canonical builder uses `Authorization: Bearer <KR_API_TOKEN>`. The daily digest receives no write token.

## Current object transaction

| Model | Current use | Endpoint family |
|---|---|---|
| Dream | one PITCH world and one LOCATION | `/api/dreams` |
| PitchSheet | cards for the world and location | `/api/sheets/by-dream/{dreamId}` |
| DreamRelation | world CONTAINS location | `/api/dream-relations` |
| Character | one real Character linked to the world | `/api/characters` |
| Reward | one ITEM and one SKILL linked to the world | `/api/rewards` |
| Scenario | one real Scenario linked to the world and location | `/api/scenarios` |

The transaction records every resulting ID in proposal `built-data`. On a partial failure, rows owned by that attempt are rolled back and a durable retry marker remains.

## Facets and art

`scripts/apply_daily_dream_facets.py` assigns the proposal's persisted Facets to the recorded real models after the bundle ledger exists. This is enrichment, not another creator.

The builder queues one stable art request for each of the six assets. Later attachment passes patch each real model when its public image is available.

## Not in the current Daily Dream bundle

Narrator Bots, ExpressionMedia, ExpressionTransition, NarratorTopic, NarratorThread, shadow CHARACTER/REWARD/NARRATOR Dreams, and GENRE shadow Dreams are not part of the current dated Daily Dream contract.

Older API research and the retired eight-stage experiment remain available in git history. New work should use this document, `PIPELINE.md`, and the executable builder as the current surface.
