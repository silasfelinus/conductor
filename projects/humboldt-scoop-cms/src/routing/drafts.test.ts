import assert from 'node:assert/strict'
import { test } from 'node:test'
import { seedData } from '../schema.js'
import { HaversineMatrixProvider } from './matrixProvider.js'
import { planRoute } from './planRoute.js'
import { __resetDraftsForTest, getDraft, listDrafts, saveDraft } from './drafts.js'
import type { RoutePlanRequest } from './types.js'

const START = { lat: 40.8021, lng: -124.1637, label: 'Shop' }
const provider = new HaversineMatrixProvider()

async function planForTest() {
  const request: RoutePlanRequest = {
    date: '2026-07-28',
    selection: { mode: 'explicit', customerIds: ['cus-rivera', 'cus-nguyen'] },
    start: START,
  }
  return planRoute(request, seedData, provider)
}

test('saveDraft assigns an id and stores the full plan, retrievable by getDraft', async () => {
  __resetDraftsForTest()
  const plan = await planForTest()
  const draft = saveDraft(plan, 'Morning run')

  assert.ok(draft.id)
  assert.equal(draft.label, 'Morning run')
  assert.deepEqual(getDraft(draft.id)?.plan, plan)
})

test('listDrafts returns saved drafts newest first', async () => {
  __resetDraftsForTest()
  const plan = await planForTest()
  const first = saveDraft(plan)
  const second = saveDraft(plan, 'second')

  const ids = listDrafts().map((d) => d.id)
  assert.deepEqual(ids, [second.id, first.id])
})

test('getDraft returns undefined for an unknown id', () => {
  __resetDraftsForTest()
  assert.equal(getDraft('does-not-exist'), undefined)
})
