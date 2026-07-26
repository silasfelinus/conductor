import type { Coordinates, SeedData, YardSize } from '../schema.js'
import { getConfiguredMatrixProvider, haversineDistanceMeters } from './matrixProvider.js'
import { optimizeStopOrder } from './optimizer.js'
import type {
  ExcludedCustomer,
  PlannedStop,
  RouteMatrixProvider,
  RoutePlanRequest,
  RoutePlanResponse,
  StopCandidate,
} from './types.js'

export const SERVICE_DURATION_MINUTES_BY_YARD_SIZE: Record<YardSize, number> = {
  small: 10,
  medium: 15,
  large: 20,
  'extra-large': 30,
}

class RoutePlanError extends Error {
  readonly status: number
  constructor(message: string, status = 400) {
    super(message)
    this.status = status
  }
}

function collectEligibleStops(
  seedData: SeedData,
  date: string,
  filter: RoutePlanRequest['filter'],
): { eligible: StopCandidate[]; missingCoordinates: ExcludedCustomer[] } {
  const datePrefix = date.slice(0, 10)
  const eligible: StopCandidate[] = []
  const missingCoordinates: ExcludedCustomer[] = []

  for (const visit of seedData.visits) {
    if (visit.status !== 'scheduled') continue
    if (!visit.scheduledFor.startsWith(datePrefix)) continue

    const customer = seedData.customers.find((c) => c.id === visit.customerId)
    const property = seedData.properties.find((p) => p.id === visit.propertyId)
    const plan = seedData.servicePlans.find((sp) => sp.id === visit.servicePlanId)
    if (!customer || !property) continue

    if (filter?.neighborhood && property.city.toLowerCase() !== filter.neighborhood.toLowerCase()) continue
    if (filter?.frequency && plan?.frequency !== filter.frequency) continue

    const candidate: StopCandidate = {
      customerId: customer.id,
      customerName: customer.displayName,
      visitId: visit.id,
      propertyId: property.id,
      propertyLabel: property.label,
      neighborhood: property.city,
      yardSize: property.yardSize,
      coordinates: property.coordinates ?? null,
    }

    if (!candidate.coordinates) {
      missingCoordinates.push({
        customerId: customer.id,
        customerName: customer.displayName,
        reason: 'Property has no coordinates on file -- cannot be routed until one is added.',
      })
      continue
    }

    eligible.push(candidate)
  }

  return { eligible, missingCoordinates }
}

function applySelection(
  eligible: StopCandidate[],
  request: RoutePlanRequest,
  seedData: SeedData,
): { selected: StopCandidate[]; excluded: ExcludedCustomer[] } {
  const { selection, date } = request
  const excluded: ExcludedCustomer[] = []

  if (selection.mode === 'explicit') {
    const byId = new Map(eligible.map((s) => [s.customerId, s]))
    const selected: StopCandidate[] = []
    const requested = new Set(selection.customerIds)

    for (const customerId of selection.customerIds) {
      const stop = byId.get(customerId)
      if (stop) {
        selected.push(stop)
      } else {
        const customer = seedData.customers.find((c) => c.id === customerId)
        excluded.push({
          customerId,
          customerName: customer?.displayName ?? customerId,
          reason: `No eligible scheduled visit for ${date} matching the given date/filter.`,
        })
      }
    }

    for (const stop of eligible) {
      if (!requested.has(stop.customerId)) {
        excluded.push({
          customerId: stop.customerId,
          customerName: stop.customerName,
          reason: 'Eligible this run but not selected (explicit mode).',
        })
      }
    }

    return { selected, excluded }
  }

  // fill-to-n
  const count = Math.max(0, Math.floor(selection.count))
  const sortBy = selection.sortBy ?? 'earliest-due'

  const visitsById = new Map(seedData.visits.map((v) => [v.id, v]))
  const sorted = eligible.slice().sort((a, b) => {
    if (sortBy === 'proximity') {
      const da = haversineDistanceMeters(request.start, a.coordinates!)
      const db = haversineDistanceMeters(request.start, b.coordinates!)
      if (da !== db) return da - db
    } else {
      const va = visitsById.get(a.visitId)?.scheduledFor ?? ''
      const vb = visitsById.get(b.visitId)?.scheduledFor ?? ''
      if (va !== vb) return va < vb ? -1 : 1
    }
    return a.customerId < b.customerId ? -1 : a.customerId > b.customerId ? 1 : 0
  })

  const selected = sorted.slice(0, count)
  const skipped = sorted.slice(count)
  for (const stop of skipped) {
    excluded.push({
      customerId: stop.customerId,
      customerName: stop.customerName,
      reason: `Eligible this run but not among the top ${count} by ${sortBy} (fill-to-N mode).`,
    })
  }

  return { selected, excluded }
}

async function planRouteWithProvider(request: RoutePlanRequest, seedData: SeedData, provider: RouteMatrixProvider): Promise<RoutePlanResponse> {
  const warnings: string[] = []
  const { eligible, missingCoordinates } = collectEligibleStops(seedData, request.date, request.filter)
  const { selected, excluded: selectionExcluded } = applySelection(eligible, request, seedData)
  const excluded = [...missingCoordinates, ...selectionExcluded]

  if (missingCoordinates.length > 0) {
    warnings.push(`${missingCoordinates.length} eligible customer(s) excluded for missing property coordinates.`)
  }

  if (selected.length === 0) {
    throw new RoutePlanError('No stops selected -- nothing to route. Check date/filter/selection.', 422)
  }

  const start: Coordinates & { label?: string } = { lat: request.start.lat, lng: request.start.lng, label: request.start.label }
  const end: Coordinates & { label?: string } = request.end ?? { ...start }

  const points: Coordinates[] = [start, ...selected.map((s) => s.coordinates as Coordinates), end]
  const matrix = await provider.getMatrix(points)

  const lockedPositions: { position: number; stopIdx: number }[] = []
  for (const lock of request.locked ?? []) {
    const stopArrayIndex = selected.findIndex((s) => s.customerId === lock.customerId)
    if (stopArrayIndex === -1) {
      warnings.push(`Locked stop for customer ${lock.customerId} ignored -- not part of this run's selected stops.`)
      continue
    }
    lockedPositions.push({ position: lock.position, stopIdx: stopArrayIndex + 1 })
  }

  const optimized = optimizeStopOrder({
    distancesMeters: matrix.distancesMeters,
    stopCount: selected.length,
    lockedPositions,
  })

  if (optimized.ignoredLocks.length > 0) {
    warnings.push(`${optimized.ignoredLocks.length} locked-stop position(s) were out of range or collided and were ignored.`)
  }

  const orderedStops = optimized.order.map((matrixIdx) => selected[matrixIdx - 1]!)
  const geometry = await provider.getRouteGeometry([start, ...orderedStops.map((s) => s.coordinates as Coordinates), end])

  const crewStartTime = request.crewStartTime ?? `${request.date.slice(0, 10)}T08:00:00Z`
  const crewStartMs = Date.parse(crewStartTime)
  if (Number.isNaN(crewStartMs)) {
    throw new RoutePlanError(`Invalid crewStartTime: ${crewStartTime}`, 400)
  }

  const lockedStopIndices = new Set(lockedPositions.map((l) => l.stopIdx).filter((stopIdx) => !optimized.ignoredLocks.includes(stopIdx)))
  const fullMatrixOrder = [0, ...optimized.order, selected.length + 1]

  const stops: PlannedStop[] = []
  let cumulativeDistanceMeters = 0
  let cumulativeDurationSeconds = 0

  for (let i = 1; i < fullMatrixOrder.length - 1; i++) {
    const prevIdx = fullMatrixOrder[i - 1]!
    const thisIdx = fullMatrixOrder[i]!
    const legDistanceMeters = matrix.distancesMeters[prevIdx]![thisIdx]!
    const legDurationSeconds = matrix.durationsSeconds[prevIdx]![thisIdx]!

    cumulativeDistanceMeters += legDistanceMeters
    cumulativeDurationSeconds += legDurationSeconds

    const stop = selected[thisIdx - 1]!
    const eta = new Date(crewStartMs + cumulativeDurationSeconds * 1000).toISOString()

    stops.push({
      sequence: i,
      customerId: stop.customerId,
      customerName: stop.customerName,
      propertyLabel: stop.propertyLabel,
      neighborhood: stop.neighborhood,
      coordinates: stop.coordinates as Coordinates,
      locked: lockedStopIndices.has(thisIdx),
      legDistanceMeters,
      legDurationSeconds,
      cumulativeDistanceMeters,
      cumulativeDurationSeconds,
      eta,
    })

    cumulativeDurationSeconds += SERVICE_DURATION_MINUTES_BY_YARD_SIZE[stop.yardSize] * 60
  }

  // Final leg: last stop -> end.
  const lastStopIdx = fullMatrixOrder[fullMatrixOrder.length - 2]!
  const endIdx = fullMatrixOrder[fullMatrixOrder.length - 1]!
  cumulativeDistanceMeters += matrix.distancesMeters[lastStopIdx]![endIdx]!
  cumulativeDurationSeconds += matrix.durationsSeconds[lastStopIdx]![endIdx]!

  return {
    date: request.date.slice(0, 10),
    routingProvider: provider.name,
    start,
    end,
    stops,
    totals: {
      distanceMeters: Math.round(cumulativeDistanceMeters),
      durationSeconds: Math.round(cumulativeDurationSeconds),
      estimatedFinishTime: new Date(crewStartMs + cumulativeDurationSeconds * 1000).toISOString(),
    },
    warnings,
    excluded,
    instructions: geometry.instructions,
  }
}

export async function planRoute(request: RoutePlanRequest, seedData: SeedData, provider: RouteMatrixProvider = getConfiguredMatrixProvider()): Promise<RoutePlanResponse> {
  return planRouteWithProvider(request, seedData, provider)
}

export { RoutePlanError }
