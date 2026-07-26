import assert from 'node:assert/strict'
import { test } from 'node:test'
import { optimizeStopOrder, pathDistance } from './optimizer.js'

type Point = { x: number; y: number }

function euclideanMatrix(points: Point[]): number[][] {
  return points.map((a) => points.map((b) => Math.hypot(a.x - b.x, a.y - b.y)))
}

function permutations<T>(items: T[]): T[][] {
  if (items.length <= 1) return [items]
  const result: T[][] = []
  for (let i = 0; i < items.length; i++) {
    const rest = items.slice(0, i).concat(items.slice(i + 1))
    for (const perm of permutations(rest)) {
      result.push([items[i]!, ...perm])
    }
  }
  return result
}

function bruteForceOptimal(distancesMeters: number[][], startIdx: number, endIdx: number, stopIndices: number[]): number {
  let best = Number.POSITIVE_INFINITY
  for (const perm of permutations(stopIndices)) {
    const d = pathDistance(distancesMeters, startIdx, endIdx, perm)
    if (d < best) best = d
  }
  return best
}

test('optimizeStopOrder returns a valid permutation of all stops when nothing is locked', () => {
  // Fixed, deterministic layout -- no randomness.
  const points: Point[] = [
    { x: 0, y: 0 }, // start
    { x: 5, y: 5 },
    { x: 1, y: 4 },
    { x: 3, y: 1 },
    { x: 4, y: 0 }, // end
  ]
  const distancesMeters = euclideanMatrix(points)
  const result = optimizeStopOrder({ distancesMeters, stopCount: 3, lockedPositions: [] })

  assert.deepEqual(result.order.slice().sort(), [1, 2, 3])
  assert.equal(result.ignoredLocks.length, 0)
})

test('optimizeStopOrder finds the brute-force optimal order for a small deterministic 5-stop layout', () => {
  const points: Point[] = [
    { x: 0, y: 0 }, // start (idx 0)
    { x: 5, y: 0 }, // stop (idx 1)
    { x: 5, y: 5 }, // stop (idx 2)
    { x: 0, y: 5 }, // stop (idx 3)
    { x: 2, y: 2 }, // stop (idx 4)
    { x: 3, y: 3 }, // stop (idx 5)
    { x: 0, y: 0 }, // end (idx 6), round trip
  ]
  const distancesMeters = euclideanMatrix(points)
  const stopIndices = [1, 2, 3, 4, 5]

  const result = optimizeStopOrder({ distancesMeters, stopCount: 5, lockedPositions: [] })
  const optimalDistance = bruteForceOptimal(distancesMeters, 0, 6, stopIndices)
  const foundDistance = pathDistance(distancesMeters, 0, 6, result.order)

  assert.ok(
    Math.abs(foundDistance - optimalDistance) < 1e-6,
    `expected optimizer to match brute-force optimum ${optimalDistance}, got ${foundDistance}`,
  )
})

test('optimizeStopOrder pins a locked stop to its requested position', () => {
  const points: Point[] = [
    { x: 0, y: 0 },
    { x: 1, y: 0 },
    { x: 2, y: 0 },
    { x: 3, y: 0 },
    { x: 4, y: 0 },
  ]
  const distancesMeters = euclideanMatrix(points)

  // Without locks, nearest-neighbor from the start naturally visits 1,2,3 in
  // order. Force stop idx 3 (the farthest) into position 0 and confirm it wins
  // despite being a poor greedy choice.
  const lockedPositions = [{ position: 0, stopIdx: 3 }]
  const result = optimizeStopOrder({ distancesMeters, stopCount: 3, lockedPositions })

  assert.equal(result.order[0], 3)
  assert.deepEqual(result.order.slice().sort(), [1, 2, 3])
  assert.equal(result.ignoredLocks.length, 0)
})

test('optimizeStopOrder ignores an out-of-range locked position', () => {
  const points: Point[] = [
    { x: 0, y: 0 },
    { x: 1, y: 0 },
    { x: 2, y: 0 },
    { x: 3, y: 0 },
  ]
  const distancesMeters = euclideanMatrix(points)
  const lockedPositions = [{ position: 5, stopIdx: 2 }] // only positions 0,1 exist for 2 stops

  const result = optimizeStopOrder({ distancesMeters, stopCount: 2, lockedPositions })

  assert.deepEqual(result.ignoredLocks, [2])
  assert.deepEqual(result.order.slice().sort(), [1, 2])
})

test('optimizeStopOrder keeps the first lock and ignores a later one that collides on the same position', () => {
  const points: Point[] = [
    { x: 0, y: 0 },
    { x: 1, y: 0 },
    { x: 2, y: 0 },
    { x: 3, y: 0 },
  ]
  const distancesMeters = euclideanMatrix(points)
  const lockedPositions = [
    { position: 0, stopIdx: 1 },
    { position: 0, stopIdx: 2 }, // collides with the entry above -- first request wins, second is ignored
  ]

  const result = optimizeStopOrder({ distancesMeters, stopCount: 2, lockedPositions })
  assert.equal(result.order[0], 1)
  assert.deepEqual(result.ignoredLocks, [2])
  assert.deepEqual(result.order.slice().sort(), [1, 2])
})
