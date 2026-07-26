# Humboldt Scoop CMS — self-hosted routing stack (OSRM + VROOM)

Standup for t-006's approved v1 routing backend (`route-planner/SPEC.md`
section 3a/5): a self-hosted **OSRM** instance for the road-network
distance/duration matrix and turn-by-turn polyline, plus a **VROOM**
instance for future stop-order optimization. Filed as t-012 from t-007's
close-out kaizen; per Silas's t-006 approval note, this is meant to run as
pm2 processes on the same host box that already runs comfy / comfy-relay /
the serendipity-voice relay (mirrors `ops/home-server/ecosystem.config.js`
at the conductor repo root and `serendipity-voice/ecosystem.config.cjs`).

**Not runnable from a conductor sandbox session** — no Docker or outbound
OSM access there. Everything in this directory is scaffolding to run on the
actual host; verify image tags and paths against the live box before
trusting them blindly, same as the `VERIFY THESE PATHS` note at the top of
`ops/home-server/ecosystem.config.js`.

## What this does today

- `osrm-backend` serves `/table/v1/driving/...` and `/route/v1/driving/...`
  — the exact HTTP API `../../src/routing/matrixProvider.ts`'s
  `OSRMMatrixProvider` already calls. Once this is running and
  `OSRM_BASE_URL` is set on the CMS, `getConfiguredMatrixProvider()` picks
  it up automatically — no app code changes needed.
- `vroom` is stood up and reachable, but **not yet wired into the app**.
  `../../src/routing/optimizer.ts`'s nearest-neighbor + 2-opt optimizer is
  a complete v1 stop-order solver on its own (SPEC.md section 3a); full
  VROOM integration (locked-stop constraints via VROOM's job/priority and
  time-window fields) is future work, not required for t-007/t-008 to keep
  working.

Both services are optional at runtime: with `OSRM_BASE_URL` unset, the CMS
falls back to `HaversineMatrixProvider` (straight-line estimate, no
network dependency) — nothing breaks if this stack isn't running.

## One-time setup

Requires Docker on the host.

```bash
cd projects/humboldt-scoop-cms/ops/routing
./fetch-extract.sh
```

This downloads a Humboldt County-scale OSM extract via the Overpass API
(bbox `39.95,-124.45,41.48,-123.30` — generous padding around the county
line), converts it to `.osm.pbf`, and runs `osrm-extract` → `osrm-partition`
→ `osrm-customize` (multi-level Dijkstra) to produce the preprocessed
`.osrm` files `osrm-backend` serves. Re-run it whenever refreshing the OSM
data — SPEC.md suggests quarterly is plenty for a service area this size.
Output lands in `data/` (gitignored — regenerable, and OSM extracts don't
belong in the repo).

## Starting the services

```bash
cd projects/humboldt-scoop-cms/ops/routing
pm2 start ecosystem.config.cjs
pm2 save
```

Then point the CMS at it:

```bash
export OSRM_BASE_URL=http://localhost:5000
```

(or the box's Tailscale hostname, if the CMS runs elsewhere on the
tailnet). Both containers run with `--network host` so `osrm-backend`
binds directly to port 5000 and `vroom-config.yml`'s `host: localhost`
reaches it without cross-container DNS — this assumes a Linux Docker host
(true for unraid); swap to `-p host:container` port publishing plus a
real hostname in `vroom-config.yml` if this ever moves to a host where
`--network host` isn't available (e.g. Docker Desktop on macOS/Windows).

## Logs

`pm2 logs osrm-backend` / `pm2 logs vroom`, or tail `logs/*.log` directly
(gitignored, created on first start).

## Refreshing the OSM extract

Delete `data/humboldt-county.osm.pbf` (or the region-named file if
`OSM_REGION` was overridden) and re-run `./fetch-extract.sh`, then
`pm2 restart osrm-backend`.
