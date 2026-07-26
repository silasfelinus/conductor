/**
 * Deterministic stop-order optimizer: nearest-neighbor construction plus
 * 2-opt improvement, per SPEC.md section 3's v1 recommendation ("nearest-
 * neighbor plus 2-opt for v1 or an approved OR-Tools service") -- no LLM
 * involvement, no randomness, same input always produces the same order.
 *
 * Operates on a fixed-endpoint open path: index 0 is the start point, the
 * last index is the end point, and every index in between is a stop to be
 * ordered. Locked stops are handled per SPEC.md section 4's simpler v1
 * approach: optimize the unlocked subset only, then splice locked stops
 * back in at their fixed position.
 */

export type LockRequest = {
  /** 0-based position among stops that this stop should be pinned to. */
  position: number
  /** Matrix index of the stop (1..stopCount). */
  stopIdx: number
}

export type OptimizeInput = {
  /** Full distance matrix indexed [start, ...stops, end]. */
  distancesMeters: number[][]
  /** Number of stops (excludes the start/end anchor rows/columns). */
  stopCount: number
  /** Requested locked positions, in priority order -- first request for a given position wins. */
  lockedPositions: LockRequest[]
}

export type OptimizeResult = {
  /** Matrix indices of stops, in visit order (length === stopCount). */
  order: number[]
  /** Locked positions that were out of range or collided and were ignored. */
  ignoredLocks: number[]
}

const STOP_OFFSET = 1 // matrix index 0 is the start anchor

function pathDistance(distancesMeters: number[][], startIdx: number, endIdx: number, order: number[]): number {
  let total = 0
  let prev = startIdx
  for (const idx of order) {
    total += distancesMeters[prev]![idx]!
    prev = idx
  }
  total += distancesMeters[prev]![endIdx]!
  return total
}

function nearestNeighborOrder(distancesMeters: number[][], startIdx: number, endIdx: number, candidateIndices: number[]): number[] {
  const remaining = new Set(candidateIndices)
  const order: number[] = []
  let current = startIdx

  while (remaining.size > 0) {
    let best: number | null = null
    let bestDistance = Number.POSITIVE_INFINITY
    // Deterministic tie-break: iterate candidates in their original (stable) order.
    for (const idx of candidateIndices) {
      if (!remaining.has(idx)) continue
      const d = distancesMeters[current]![idx]!
      if (d < bestDistance) {
        bestDistance = d
        best = idx
      }
    }
    if (best === null) break
    order.push(best)
    remaining.delete(best)
    current = best
  }

  return order
}

function twoOptImprove(distancesMeters: number[][], startIdx: number, endIdx: number, initialOrder: number[]): number[] {
  let order = initialOrder.slice()
  const n = order.length
  if (n < 2) return order

  let improved = true
  let passes = 0
  const MAX_PASSES = 50

  while (improved && passes < MAX_PASSES) {
    improved = false
    passes += 1

    for (let i = 0; i < n - 1; i++) {
      for (let j = i + 1; j < n; j++) {
        const a = i === 0 ? startIdx : order[i - 1]!
        const b = order[i]!
        const c = order[j]!
        const d = j === n - 1 ? endIdx : order[j + 1]!

        const before = distancesMeters[a]![b]! + distancesMeters[c]![d]!
        const after = distancesMeters[a]![c]! + distancesMeters[b]![d]!

        if (after < before - 1e-9) {
          const reversed = order.slice(0, i).concat(order.slice(i, j + 1).reverse(), order.slice(j + 1))
          order = reversed
          improved = true
        }
      }
    }
  }

  return order
}

/**
 * Optimizes stop visit order. Stop matrix indices run 1..stopCount
 * (STOP_OFFSET), with 0 = start and stopCount+1 = end.
 */
export function optimizeStopOrder(input: OptimizeInput): OptimizeResult {
  const { distancesMeters, stopCount, lockedPositions } = input
  const startIdx = 0
  const endIdx = stopCount + STOP_OFFSET

  const allStopIndices = Array.from({ length: stopCount }, (_, i) => i + STOP_OFFSET)

  const ignoredLocks: number[] = []
  const lockedByPosition = new Map<number, number>()
  for (const { position, stopIdx } of lockedPositions) {
    if (position < 0 || position >= stopCount || lockedByPosition.has(position)) {
      ignoredLocks.push(stopIdx)
      continue
    }
    lockedByPosition.set(position, stopIdx)
  }

  const lockedStopIndices = new Set(lockedByPosition.values())
  const unlockedIndices = allStopIndices.filter((idx) => !lockedStopIndices.has(idx))

  const nnOrder = nearestNeighborOrder(distancesMeters, startIdx, endIdx, unlockedIndices)
  const optimizedUnlocked = twoOptImprove(distancesMeters, startIdx, endIdx, nnOrder)

  const finalOrder: number[] = new Array(stopCount)
  for (const [position, stopIdx] of lockedByPosition.entries()) {
    finalOrder[position] = stopIdx
  }

  let cursor = 0
  for (let position = 0; position < stopCount; position++) {
    if (finalOrder[position] !== undefined) continue
    finalOrder[position] = optimizedUnlocked[cursor]!
    cursor += 1
  }

  return { order: finalOrder, ignoredLocks }
}

export { pathDistance }
