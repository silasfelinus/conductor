import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { loadWorldDecks, validateWorldDecks, assertValidWorldDecks, toPlayerBoard } from './world-decks.contract.mjs'

const source = loadWorldDecks()
const broken = (edit) => { const copy = structuredClone(source); edit(copy); return validateWorldDecks(copy) }

test('versioned five-land, 15-encounter, five-gate manifest references all design assets', () => {
  assert.equal(validateWorldDecks(source).length, 0)
  assert.equal(source.schema_version, 2)
  assert.equal(source.lands.length, 5)
  assert.equal(source.lands.flatMap((land) => land.locations).length, 15)
  assert.equal(source.lands.filter((land) => land.major_challenge).length, 5)
  assert.equal(source.art_refs.length, 4)
  assert.equal(source.art_refs.every((art) => art.art_image_id === null && art.status === 'repository-file'), true)
  assert.ok(source.named_exceptions.some((entry) => entry.id === 'abbess' && entry.locked_art_image_id === 242559))
  assert.ok(readFileSync(new URL('./world-decks.d.ts', import.meta.url), 'utf8').includes('WorldDecksV2'))
})

test('species and jobs are independent Facet layers, not morality presets', () => {
  assert.ok(source.facet_pools.species.every((entry) => entry.taxonomy === 'SPECIES'))
  assert.ok(source.facet_pools.roles.every((entry) => ['OCCUPATION', 'ROLE', 'ARCHETYPE'].includes(entry.taxonomy)))
  const land = source.lands[0]
  const rabbits = source.facet_pools.species.find((entry) => entry.key === 'rabbit')
  const otters = source.facet_pools.species.find((entry) => entry.key === 'otter')
  const homesteader = source.facet_pools.roles.find((entry) => entry.key === 'homesteader')
  assert.ok([rabbits, otters, homesteader].every((entry) => entry.biomes.includes(land.biome)))
  assert.ok(source.facet_pools.dispositions.includes('helpful'))
  assert.ok(source.facet_pools.dispositions.includes('predatory'))
  assert.ok(broken((m) => { m.facet_pools.species[0].morality = 'good' }).some((s) => s.includes('hardcodes morality')))
  assert.ok(broken((m) => { m.facet_pools.roles[0].taxonomy = 'SPECIES' }).some((s) => s.includes('taxonomy')))
})

test('broken graph, duplicate encounter, unsafe teaser and claimed live identity all fail', () => {
  assert.ok(broken((m) => { m.lands[1].locations[0].id = m.lands[0].locations[0].id }).some((s) => s.includes('globally unique')))
  assert.ok(broken((m) => { m.lands[0].locations[0].template = 'hallucinated-scenario' }).some((s) => s.includes('Scenario')))
  assert.ok(broken((m) => { m.lands[0].locations[0].possible_rewards = ['phantom'] }).some((s) => s.includes('Reward')))
  assert.ok(broken((m) => { m.lands[0].locations[0].art_ref = 'hallucinated-image' }).some((s) => s.includes('artwork')))
  assert.ok(broken((m) => { m.art_refs[0].art_image_id = 42 }).some((s) => s.includes('live ArtImage')))
  assert.ok(broken((m) => { m.lands[3].roles = ['ferrykeeper'] }).some((s) => s.includes('Incompatible')))
  assert.ok(broken((m) => { m.lands[0].locations[0].front_teaser = 'The ritual sacrifice of children is here.' }).some((s) => s.includes('Unsafe')))
  assert.ok(broken((m) => { m.schema_version = 3 }).some((s) => s.includes('schema_version')))
  assert.throws(() => assertValidWorldDecks({ schema_version: 3 }), /invalid/)
})

test('only an explicit public allowlist is exposed, with bosses gated by earned encounters', () => {
  const initial = toPlayerBoard(source)
  assert.equal(initial.lands.length, 5)
  assert.equal(initial.lands[0].locations.length, 3)
  assert.equal(initial.lands[0].major_challenge, null)
  assert.equal(initial.lands[1].revealed, false)
  assert.deepEqual(Object.keys(initial.lands[1]).sort(), ['chapter','id','revealed'])
  assert.equal(initial.lands[0].locations[0].art_url, '/zuzu-gamebook/scenes/apple-tree.webp')
  const afterThree = toPlayerBoard(source, {
    completedLocationIds: source.lands[0].locations.map((loc) => loc.id),
  })
  assert.equal(afterThree.lands[0].major_challenge.label, 'The Abbess')
  const all = toPlayerBoard(source, {
    activeChapter: 5, completedLocationIds: source.lands.flatMap((land) => land.locations.map((loc) => loc.id)),
  })
  const safe = JSON.stringify(all).toLowerCase()
  for (const forbidden of ['canon_motivation','world_mysteries','named_exceptions','cosmic horror','ritual','sacrific','disposition','template','scenario_refs','reward_refs','runtime_id','hidden_truth']) {
    assert.equal(safe.includes(forbidden), false, 'Spoiler or developer-only source leaked: ' + forbidden)
  }
  assert.throws(() => toPlayerBoard(source, { activeChapter: 9 }), /Invalid chapter/)
  assert.throws(() => toPlayerBoard(source, { completedLocationIds: 3 }), /Invalid resolved locations/)
})
