#!/usr/bin/env bash
# Fetches a Humboldt County-scale OpenStreetMap extract and preprocesses it
# for osrm-backend (extract -> partition -> customize, multi-level Dijkstra
# per SPEC.md section 3a / route-planner/SPEC.md). Run this once before the
# first `pm2 start ecosystem.config.cjs`, and again whenever refreshing the
# OSM data -- SPEC.md suggests quarterly is plenty for a service area this
# size (roads don't change that often).
#
# Requires: docker, curl.
#
# ---- VERIFY ON THE ACTUAL HOST -- not runnable/testable from a conductor
# sandbox session (no docker or outbound OSM access there; see
# projects/humboldt-scoop-cms/TALKBACK.md, t-012 filing note) ----

set -euo pipefail

cd "$(dirname "$0")"
mkdir -p data

REGION="${OSM_REGION:-humboldt-county}"
PBF_PATH="data/${REGION}.osm.pbf"

# Humboldt County, CA bounding box (generous padding -- a few extra miles of
# neighboring county roads costs almost nothing at this scale and avoids
# clipping a route that starts/ends near the county line).
#   south=39.95 west=-124.45 north=41.48 east=-123.30
BBOX="39.95,-124.45,41.48,-123.30"

if [ ! -f "$PBF_PATH" ]; then
  echo "==> Fetching OSM data for bbox ${BBOX} via Overpass API"
  # Overpass's standard "export everything in a bbox" pattern: grab every
  # node in the box, then recurse up (<;) to pull in the ways/relations that
  # reference them, so the extract is topologically complete for routing
  # (not just points -- roads and their connectivity).
  curl -sS -g \
    --data-urlencode "data=[out:xml][timeout:180][bbox:${BBOX}];(node;<;);out meta;" \
    -o "data/${REGION}.osm" \
    "https://overpass-api.de/api/interpreter"

  echo "==> Converting to .osm.pbf via osmium"
  docker run --rm -v "$(pwd)/data:/data" stefda/osmium-tool \
    osmium cat "/data/${REGION}.osm" -o "/data/${REGION}.osm.pbf" --overwrite
  rm -f "data/${REGION}.osm"
else
  echo "==> ${PBF_PATH} already present -- delete it first to force a re-fetch"
fi

echo "==> osrm-extract (car profile)"
docker run --rm -v "$(pwd)/data:/data" osrm/osrm-backend \
  osrm-extract -p /opt/car.lua "/data/${REGION}.osm.pbf"

echo "==> osrm-partition"
docker run --rm -v "$(pwd)/data:/data" osrm/osrm-backend \
  osrm-partition "/data/${REGION}.osrm"

echo "==> osrm-customize"
docker run --rm -v "$(pwd)/data:/data" osrm/osrm-backend \
  osrm-customize "/data/${REGION}.osrm"

echo "==> Done. Start the services with: pm2 start ecosystem.config.cjs"
