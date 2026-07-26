import assert from 'node:assert/strict'
import { test } from 'node:test'
import { HaversineMatrixProvider, OSRMMatrixProvider, haversineDistanceMeters } from './matrixProvider.js'

test('haversineDistanceMeters returns 0 for identical points', () => {
  const p = { lat: 40.8021, lng: -124.1637 }
  assert.equal(haversineDistanceMeters(p, p), 0)
})

test('haversineDistanceMeters returns a plausible distance for two known Humboldt-area points', () => {
  const eureka = { lat: 40.8021, lng: -124.1637 }
  const fortuna = { lat: 40.5982, lng: -124.1573 }
  const distance = haversineDistanceMeters(eureka, fortuna)
  // Eureka -> Fortuna is roughly 23 km straight-line; assert a generous but meaningful bound.
  assert.ok(distance > 15_000 && distance < 35_000, `expected ~15-35km, got ${distance}`)
})

test('HaversineMatrixProvider builds a symmetric-ish matrix with zero diagonal', async () => {
  const provider = new HaversineMatrixProvider(30)
  const points = [
    { lat: 40.8021, lng: -124.1637 },
    { lat: 40.7629, lng: -124.1462 },
    { lat: 40.8129, lng: -124.1275 },
  ]
  const matrix = await provider.getMatrix(points)

  for (let i = 0; i < points.length; i++) {
    assert.equal(matrix.distancesMeters[i]![i], 0)
    assert.equal(matrix.durationsSeconds[i]![i], 0)
  }
  assert.ok(matrix.distancesMeters[0]![1]! > 0)
  assert.ok(matrix.durationsSeconds[0]![1]! > 0)
})

test('HaversineMatrixProvider.getRouteGeometry returns no polyline and one instruction per leg', async () => {
  const provider = new HaversineMatrixProvider()
  const geometry = await provider.getRouteGeometry([
    { lat: 40.8021, lng: -124.1637 },
    { lat: 40.7629, lng: -124.1462 },
    { lat: 40.8021, lng: -124.1637 },
  ])
  assert.equal(geometry.polyline, null)
  assert.equal(geometry.instructions.length, 2)
})

test('OSRMMatrixProvider.getMatrix builds the expected table URL and parses a response', async (t) => {
  const calls: string[] = []
  const originalFetch = globalThis.fetch
  t.after(() => {
    globalThis.fetch = originalFetch
  })

  globalThis.fetch = (async (input: RequestInfo | URL) => {
    calls.push(String(input))
    return {
      ok: true,
      status: 200,
      statusText: 'OK',
      json: async () => ({
        code: 'Ok',
        distances: [
          [0, 100],
          [100, 0],
        ],
        durations: [
          [0, 10],
          [10, 0],
        ],
      }),
    } as Response
  }) as typeof fetch

  const provider = new OSRMMatrixProvider('http://localhost:5000')
  const matrix = await provider.getMatrix([
    { lat: 40.8021, lng: -124.1637 },
    { lat: 40.7629, lng: -124.1462 },
  ])

  assert.equal(calls.length, 1)
  assert.match(calls[0]!, /^http:\/\/localhost:5000\/table\/v1\/driving\//)
  assert.match(calls[0]!, /annotations=distance,duration/)
  assert.deepEqual(matrix.distancesMeters, [
    [0, 100],
    [100, 0],
  ])
})

test('OSRMMatrixProvider.getMatrix throws on a non-Ok response code', async (t) => {
  const originalFetch = globalThis.fetch
  t.after(() => {
    globalThis.fetch = originalFetch
  })
  globalThis.fetch = (async () =>
    ({
      ok: true,
      status: 200,
      statusText: 'OK',
      json: async () => ({ code: 'NoRoute' }),
    }) as Response) as typeof fetch

  const provider = new OSRMMatrixProvider('http://localhost:5000')
  await assert.rejects(() => provider.getMatrix([{ lat: 0, lng: 0 }, { lat: 1, lng: 1 }]))
})
