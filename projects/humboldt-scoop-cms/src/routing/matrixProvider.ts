import type { Coordinates } from '../schema.js'
import type { DistanceMatrix, RouteGeometry, RouteMatrixProvider } from './types.js'

const EARTH_RADIUS_METERS = 6_371_000

function toRadians(deg: number): number {
  return (deg * Math.PI) / 180
}

/** Great-circle distance between two points, in meters. */
export function haversineDistanceMeters(a: Coordinates, b: Coordinates): number {
  const dLat = toRadians(b.lat - a.lat)
  const dLng = toRadians(b.lng - a.lng)
  const lat1 = toRadians(a.lat)
  const lat2 = toRadians(b.lat)

  const sinLat = Math.sin(dLat / 2)
  const sinLng = Math.sin(dLng / 2)
  const h = sinLat * sinLat + Math.cos(lat1) * Math.cos(lat2) * sinLng * sinLng
  const c = 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h))
  return EARTH_RADIUS_METERS * c
}

/**
 * Deterministic straight-line fallback used whenever no OSRM instance is
 * configured (OSRM_BASE_URL unset) -- e.g. local dev, tests, or before Silas
 * stands up the self-hosted OSRM/VROOM services from t-006's approved stack.
 * Distance is true great-circle distance; duration is estimated from a fixed
 * average in-town driving speed rather than a real road network, so it is
 * always a rough estimate, never a live-traffic figure.
 */
export class HaversineMatrixProvider implements RouteMatrixProvider {
  readonly name = 'haversine-fallback'
  private readonly avgSpeedMetersPerSecond: number

  constructor(avgSpeedKmh = 30) {
    this.avgSpeedMetersPerSecond = (avgSpeedKmh * 1000) / 3600
  }

  async getMatrix(points: Coordinates[]): Promise<DistanceMatrix> {
    const n = points.length
    const distancesMeters: number[][] = Array.from({ length: n }, () => new Array(n).fill(0))
    const durationsSeconds: number[][] = Array.from({ length: n }, () => new Array(n).fill(0))

    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (i === j) continue
        const distance = haversineDistanceMeters(points[i]!, points[j]!)
        distancesMeters[i]![j] = distance
        durationsSeconds[i]![j] = distance / this.avgSpeedMetersPerSecond
      }
    }

    return { distancesMeters, durationsSeconds }
  }

  async getRouteGeometry(orderedPoints: Coordinates[]): Promise<RouteGeometry> {
    const instructions = orderedPoints.slice(1).map((point, idx) => {
      const from = orderedPoints[idx]!
      const km = (haversineDistanceMeters(from, point) / 1000).toFixed(1)
      return `Drive to stop ${idx + 1} (~${km} km straight-line -- no road-network geometry, haversine-fallback provider).`
    })
    return { polyline: null, instructions }
  }
}

type OSRMTableResponse = {
  code: string
  distances?: (number | null)[][]
  durations?: (number | null)[][]
}

type OSRMRouteResponse = {
  code: string
  routes?: Array<{
    geometry?: string
    legs?: Array<{ steps?: Array<{ maneuver?: { type?: string }; name?: string; distance?: number }> }>
  }>
}

function coordsToOSRMPath(points: Coordinates[]): string {
  return points.map((p) => `${p.lng},${p.lat}`).join(';')
}

/**
 * Talks to a self-hosted OSRM instance (t-006's approved v1 stack: OSRM for
 * the road-network matrix/polyline, VROOM for stop-order optimization --
 * this provider covers the OSRM half; ordering itself is done by
 * ../optimizer.ts per the spec's "nearest-neighbor + 2-opt for v1" note).
 * Configure via OSRM_BASE_URL, e.g. http://localhost:5000 for a local
 * osrm-backend container. No API key: this is a self-hosted, unmetered
 * service, never a paid third-party routing API.
 */
export class OSRMMatrixProvider implements RouteMatrixProvider {
  readonly name = 'osrm'

  constructor(private readonly baseUrl: string) {}

  async getMatrix(points: Coordinates[]): Promise<DistanceMatrix> {
    const path = coordsToOSRMPath(points)
    const url = `${this.baseUrl}/table/v1/driving/${path}?annotations=distance,duration`
    const res = await fetch(url)
    if (!res.ok) {
      throw new Error(`OSRM table request failed: ${res.status} ${res.statusText}`)
    }
    const body = (await res.json()) as OSRMTableResponse
    if (body.code !== 'Ok' || !body.distances || !body.durations) {
      throw new Error(`OSRM table response not Ok: ${body.code}`)
    }
    const n = points.length
    const distancesMeters = body.distances.map((row) => row.map((v) => v ?? Number.POSITIVE_INFINITY))
    const durationsSeconds = body.durations.map((row) => row.map((v) => v ?? Number.POSITIVE_INFINITY))
    if (distancesMeters.length !== n || durationsSeconds.length !== n) {
      throw new Error('OSRM table response size mismatch')
    }
    return { distancesMeters, durationsSeconds }
  }

  async getRouteGeometry(orderedPoints: Coordinates[]): Promise<RouteGeometry> {
    const path = coordsToOSRMPath(orderedPoints)
    const url = `${this.baseUrl}/route/v1/driving/${path}?overview=full&geometries=polyline&steps=true`
    const res = await fetch(url)
    if (!res.ok) {
      throw new Error(`OSRM route request failed: ${res.status} ${res.statusText}`)
    }
    const body = (await res.json()) as OSRMRouteResponse
    const route = body.routes?.[0]
    if (body.code !== 'Ok' || !route) {
      throw new Error(`OSRM route response not Ok: ${body.code}`)
    }
    const instructions =
      route.legs?.flatMap(
        (leg) =>
          leg.steps?.map((step) => {
            const km = ((step.distance ?? 0) / 1000).toFixed(1)
            return `${step.maneuver?.type ?? 'continue'} on ${step.name || 'unnamed road'} (~${km} km)`
          }) ?? [],
      ) ?? []
    return { polyline: route.geometry ?? null, instructions }
  }
}

/**
 * Picks the routing/matrix provider from environment configuration.
 * Unset OSRM_BASE_URL -> Haversine fallback (no network, no keys, safe
 * default for dev/test and for any install before Silas stands up OSRM).
 */
export function getConfiguredMatrixProvider(): RouteMatrixProvider {
  const baseUrl = process.env.OSRM_BASE_URL
  if (baseUrl) {
    return new OSRMMatrixProvider(baseUrl.replace(/\/+$/, ''))
  }
  return new HaversineMatrixProvider()
}
