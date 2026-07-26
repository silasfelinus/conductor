import assert from 'node:assert/strict'
import { test } from 'node:test'
import { seedData } from '../schema.js'
import { HaversineMatrixProvider } from './matrixProvider.js'
import { collectEligibleStops, planRoute, RoutePlanError } from './planRoute.js'
import type { RoutePlanRequest } from './types.js'

const START = { lat: 40.8021, lng: -124.1637, label: 'Shop' }
const provider = new HaversineMatrixProvider()

test('planRoute explicit mode routes exactly the requested customers and excludes the rest', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'explicit', customerIds: ['cus-rivera', 'cus-nguyen', 'cus-brooks'] },
    start: START,
  }

  const plan = await planRoute(request, seedData, provider)

  assert.equal(plan.stops.length, 3)
  const routedIds = plan.stops.map((s) => s.customerId).sort()
  assert.deepEqual(routedIds, ['cus-brooks', 'cus-nguyen', 'cus-rivera'])

  // Sequence numbers are contiguous starting at 1.
  assert.deepEqual(plan.stops.map((s) => s.sequence), [1, 2, 3])

  // Every eligible-but-unselected customer for this date shows up as excluded, not silently dropped.
  const excludedIds = plan.excluded.map((e) => e.customerId).sort()
  assert.ok(excludedIds.includes('cus-park'))
  assert.equal(plan.routingProvider, 'haversine-fallback')
})

test('planRoute excludes a customer whose property has no coordinates on file, with a warning', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'explicit', customerIds: ['cus-alvarez'] },
    start: START,
  }

  await assert.rejects(() => planRoute(request, seedData, provider), RoutePlanError)
})

test('planRoute fill-to-n mode picks the top N by earliest-due and lists the rest as skipped', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'fill-to-n', count: 2, sortBy: 'earliest-due' },
    start: START,
  }

  const plan = await planRoute(request, seedData, provider)
  assert.equal(plan.stops.length, 2)
  assert.ok(plan.excluded.length >= 1)
  for (const excluded of plan.excluded) {
    if (excluded.customerId !== 'cus-alvarez') {
      assert.match(excluded.reason, /fill-to-N/)
    }
  }
})

test('planRoute fill-to-n mode sorted by proximity favors the stop nearest the start point', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'fill-to-n', count: 1, sortBy: 'proximity' },
    start: START, // Eureka coordinates -- prop-rivera-home is also in Eureka, should win.
  }

  const plan = await planRoute(request, seedData, provider)
  assert.equal(plan.stops.length, 1)
  assert.equal(plan.stops[0]!.customerId, 'cus-rivera')
})

test('planRoute honors a locked stop position even when it is not the greedy nearest-neighbor choice', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'explicit', customerIds: ['cus-rivera', 'cus-nguyen', 'cus-brooks'] },
    start: START,
    locked: [{ customerId: 'cus-brooks', position: 0 }],
  }

  const plan = await planRoute(request, seedData, provider)
  assert.equal(plan.stops[0]!.customerId, 'cus-brooks')
  assert.equal(plan.stops[0]!.locked, true)
  assert.equal(plan.stops[1]!.locked, false)
})

test('planRoute computes monotonically increasing cumulative distance/duration and a finish time after crew start', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'fill-to-n', count: 3, sortBy: 'earliest-due' },
    start: START,
    crewStartTime: '2026-07-28T08:00:00Z',
  }

  const plan = await planRoute(request, seedData, provider)

  let prevDistance = -1
  let prevDuration = -1
  for (const stop of plan.stops) {
    assert.ok(stop.cumulativeDistanceMeters > prevDistance)
    assert.ok(stop.cumulativeDurationSeconds > prevDuration)
    prevDistance = stop.cumulativeDistanceMeters
    prevDuration = stop.cumulativeDurationSeconds
    assert.ok(Date.parse(stop.eta) >= Date.parse('2026-07-28T08:00:00Z'))
  }

  assert.ok(plan.totals.distanceMeters > 0)
  assert.ok(Date.parse(plan.totals.estimatedFinishTime) > Date.parse('2026-07-28T08:00:00Z'))
})

test('planRoute throws when the selection resolves to zero stops', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'explicit', customerIds: [] },
    start: START,
  }

  await assert.rejects(() => planRoute(request, seedData, provider), RoutePlanError)
})

test('planRoute filters by neighborhood', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    filter: { neighborhood: 'Cutten' },
    selection: { mode: 'fill-to-n', count: 5 },
    start: START,
  }

  const plan = await planRoute(request, seedData, provider)
  assert.equal(plan.stops.length, 1)
  assert.equal(plan.stops[0]!.customerId, 'cus-nguyen')
})

test('planRoute reports a null polyline for the haversine-fallback provider (straight-line only)', async () => {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'explicit', customerIds: ['cus-rivera'] },
    start: START,
  }

  const plan = await planRoute(request, seedData, provider)
  assert.equal(plan.polyline, null)
})

test('collectEligibleStops returns eligible stops for a date and reports missing-coordinate customers separately', () => {
  const { eligible, missingCoordinates } = collectEligibleStops(seedData, '2026-07-28', undefined)

  const eligibleIds = eligible.map((s) => s.customerId).sort()
  assert.deepEqual(eligibleIds, ['cus-brooks', 'cus-nguyen', 'cus-park', 'cus-rivera'])

  const missingIds = missingCoordinates.map((c) => c.customerId)
  assert.ok(missingIds.includes('cus-alvarez'))
})

test('collectEligibleStops applies the same neighborhood/frequency filter as planRoute', () => {
  const { eligible } = collectEligibleStops(seedData, '2026-07-28', { neighborhood: 'Cutten' })
  assert.deepEqual(eligible.map((s) => s.customerId), ['cus-nguyen'])
})
