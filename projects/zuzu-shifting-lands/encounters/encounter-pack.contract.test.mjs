import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readPack, readWorld, readSchema, validatePack, previewSelect } from './encounter-pack.contract.mjs'

const pack = readPack()
const world = readWorld()
const schema = readSchema()
const altered = (fn) => {
  const other = structuredClone(pack)
  fn(other)
  return validatePack(other, world, schema)
}
test('machine-readable v1 schema and canonical v2 geography are compatible', () => {
  assert.deepEqual(validatePack(pack, world, schema), [])
  assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema')
  assert.equal(schema.$defs.encounter.properties.choices.minItems, 2)
  assert.equal(schema.$defs.roll.properties.dice_count.const, 2)
  assert.equal(pack.locations.length, 3)
  assert.equal(pack.encounters.length, 12)
  assert.deepEqual(pack.locations.map((loc) => [loc.location_id, loc.encounter_ids.length]), [
    ['border-farm', 4], ['old-well', 4], ['wayside-refuge', 4],
  ])
  assert.equal(pack.encounters.reduce((sum, e) => sum + e.choices.length, 0), 24)
  assert.equal(pack.encounters.reduce((sum, e) => sum + e.choices.length * 2, 0), 48)
})
test('each location mixes favorable, dangerous and ambiguous authored situations', () => {
  for (const loc of pack.locations) {
    const pool = pack.encounters.filter((e) => e.location_id === loc.location_id)
    assert.deepEqual(new Set(pool.map((e) => e.polarity)), new Set(['good', 'bad', 'mixed']))
    assert.ok(pool.every((e) => e.art.status === 'design-only' && e.art.art_ref === null))
    assert.ok(pool.every((e) => e.choices.length >= 2))
  }
})
test('species/occupation is fixed to each illustrated card, not assembled at draw time', () => {
  for (const card of pack.encounters) {
    assert.equal(card.art.cast.length, 1)
    assert.ok(card.art.cast[0].species)
    assert.ok(card.art.cast[0].occupation)
    assert.equal(card.art.cast[0].locked_character_id, null)
    assert.doesNotMatch(card.title.toLowerCase(), /\b(rabbit|otter|fox|mouse|goat|badger|coyote)\b/)
  }
  const rabbit = pack.encounters.find((e) => e.id === 'family-at-the-fence')
  assert.equal(rabbit.art.cast[0].species, 'rabbit')
  assert.equal(rabbit.art.cast[0].occupation, 'homesteaders')
})
test('preview sampler is reproducible, location-constrained and never rerolls a cast', () => {
  for (let seed = 1; seed <= 100; seed++) {
    for (const location of pack.locations) {
      const one = previewSelect(pack, seed, location.location_id)
      const two = previewSelect(pack, seed, location.location_id)
      assert.equal(one.id, two.id)
      assert.equal(one.location_id, location.location_id)
      assert.ok(location.encounter_ids.includes(one.id))
      const replacement = previewSelect(pack, seed, location.location_id, [one.id])
      assert.ok(replacement && replacement.id !== one.id)
      assert.notEqual(one.art.cast[0].identity, replacement.art.cast[0].identity)
    }
  }
  assert.equal(previewSelect(pack, 1, 'border-farm', pack.locations[0].encounter_ids), null)
  assert.throws(() => previewSelect(pack, 1, 'unknown'), /Unknown location/)
})
test('authored prose, outcomes and draw safety reject malformed content', () => {
  assert.ok(altered((m) => { m.encounters[0].choices = m.encounters[0].choices.slice(0,1) }).some((e)=>e.includes('fewer than two')))
  assert.ok(altered((m) => { m.encounters[0].art.cast[0].species = '' }).some((e)=>e.includes('visual casting')))
  assert.ok(altered((m) => { m.encounters[0].art.art_ref = 'not-verified' }).some((e)=>e.includes('design-only')))
  assert.ok(altered((m) => { m.locations[0].encounter_ids.push(m.locations[1].encounter_ids[0]) }).some((e)=>e.includes('membership')))
  assert.ok(altered((m) => { m.encounters[0].title = 'Rabbit Homesteaders' }).some((e)=>e.includes('species belongs in art')))
  assert.ok(altered((m) => { m.encounters[0].choices[0].roll.dice_count = 1 }).some((e)=>e.includes('2d6')))
  assert.ok(altered((m) => { m.encounters[0].choices[0].success.add_flags = ['WRONG'] }).some((e)=>e.includes('consequence')))
  assert.ok(altered((m) => { m.encounters[0].location_id = 'made-up' }).some((e)=>e.includes('membership')))
})
