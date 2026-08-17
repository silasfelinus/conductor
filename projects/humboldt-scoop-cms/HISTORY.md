# Humboldt Scoop Solutions — foundation history

This file is the archaeology index for the pre-consolidation `humboldt-scoop-cms` roadmap.

The complete verbose roadmap immediately before the 2026-08-17 consolidation is permanently available at Conductor commit [`ca8aa1f63930766d1a39384ff41174d4241ba825`](https://github.com/silasfelinus/conductor/blob/ca8aa1f63930766d1a39384ff41174d4241ba825/projects/humboldt-scoop-cms/roadmap.yaml). Do not restore that file as the active roadmap; use it when implementation provenance matters.

## Completed foundation tasks

- `t-001` — self-hostable Hono/TypeScript skeleton and stack recommendation.
- `t-002` — customer/property/pet/service data model.
- `t-003` — crew route-card specification.
- `t-004` — scaffold/health-check confirmation.
- `t-005` — seed customer and route-card API routes.
- `t-006` — deterministic route-planner specification; self-hosted OSRM + VROOM + Leaflet direction approved.
- `t-007` — deterministic route-plan API, Haversine fallback, OSRM integration point, nearest-neighbor + 2-opt optimizer; merged in Conductor PR #1132.
- `t-008` — dispatcher map UI, manual reorder/locks, route drafts, vendored Leaflet; merged in Conductor PR #1139.
- `t-009` — Android-first Flutter crew client with abstracted API/storage/navigation boundaries; merged in Conductor PR #1193.
- `t-010` — real-address/privacy/map-cost/launch review. It correctly found two prerequisite engineering gaps: authentication/capabilities and geocoding. Those are now explicit successor tasks rather than one ambiguous human gate.
- `t-011` — Kind Robots project/tutorial surface; merged in Kind Robots PR #273.
- `t-012` — checked-in self-hosted OSRM/VROOM + pm2 scaffolding; merged in Conductor PR #1144. The canonical copy now lives in `humboldtscoopsolutions/cms/ops/routing/`.

## Important archaeology already resolved

These are examples of why the project was consolidated instead of allowing more parallel copies:

- The Conductor `apps/humboldt-scoop-cms/` Flutter scaffold was a 22-line hello-world under the wrong package name. The real `field-client/` was the better implementation and was preserved.
- The WordPress theme named `humboldt-scoop-solutions` looked newer but had never been activated. The actual live theme was `hss-theme`; assuming the version number implied authority caused work to target the wrong copy.
- The old asset inventory incorrectly reported missing themes/plugins/uploads because it had only probed guessed paths. Later recursive/live reconciliation disproved it.
- The customer portal, quote REST handler, notification machinery, representative schema, route planner, and field client all existed before their surrounding wiring/UI made them discoverable.

The canonical implementation repo's `docs/INVENTORY.md`, `docs/INTEGRATION.md`, `docs/DATA-ARCHITECTURE.md`, and `docs/BACKLOG.md` are the current source for what is actually shipped versus merely present.
