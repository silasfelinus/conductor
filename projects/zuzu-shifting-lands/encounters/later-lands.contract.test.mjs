import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import {
  readPack,
  readWorld,
  readSchema,
  validatePack,
  previewSelect,
} from './encounter-pack.contract.mjs'

const sourceRoot = new URL('./', import.meta.url)
const world = readWorld()
const schema = readSchema()
const later = [
  ['dustwater', 'DUSTWATER-9.json'],
  ['tablelands', 'TABLELANDS-9.json'],
  ['cave', 'STORM-CROW-9.json'],
  ['verge', 'BLACK-VERGE-9.json'],
]
const packs = later.map(([landId, filename]) => ({
  landId,
  pack: JSON.parse(readFileSync(new URL(filename, sourceRoot), 'utf8')),
}))
const all = [readPack(), ...packs.map((entry) => entry.pack)]
const allCards = all.flatMap((pack) => pack.encounters)

test('all five lands have three canonical locations and three or more authored identities per location', () => {
  assert.equal(world.lands.length, 5)
  assert.equal(all.reduce((sum, pack) => sum + pack.locations.length, 0), 15)
  assert.equal(allCards.length, 48)
  assert.equal(new Set(allCards.map((card) => card.id)).size, 48)
  assert.equal(
    allCards.reduce((count, card) => count + card.choices.length, 0),
    96,
  )
  for (const { landId, pack } of packs) {
    assert.deepEqual(validatePack(pack, world, schema, landId), [])
    const expected = world.lands.find((land) => land.id === landId)
    assert.ok(expected)
    assert.deepEqual(
      new Set(pack.locations.map((location) => location.location_id)),
      new Set(expected.locations.map((location) => location.id)),
    )
    assert.equal(pack.encounters.length, 9)
    for (const location of pack.locations) {
      assert.equal(location.encounter_ids.length, 3)
      const cards = pack.encounters.filter((card) => card.location_id === location.location_id)
      assert.deepEqual(new Set(cards.map((card) => card.polarity)), new Set(['good', 'bad', 'mixed']))
      assert.equal(cards.reduce((n, card) => n + card.choices.length, 0), 6)
    }
  }
})

test('each card has deliberate cast and safe source-only art provenance', () => {
  for (const card of allCards) {
    assert.equal(card.art.status, 'design-only')
    assert.equal(card.art.art_ref, null)
    assert.equal(card.art.cast.length, 1)
    assert.equal(card.art.cast[0].locked_character_id, null)
    assert.ok(card.art.brief.length >= 50)
    assert.ok(card.flavor_text.length >= 90)
    assert.ok(card.choices.length >= 2)
    assert.doesNotMatch(card.title, /\b(rabbit|otter|mouse|fox|badger|goat|coyote|crow|gorilla|lynx|wolf|tortoise|eagle)\b/i)
    assert.doesNotMatch(card.flavor_text, /cosmic horror|former humanity|former humans|ritual sacrifice|abbess ritual/i)
    assert.ok(card.choices.every((choice) =>
      choice.roll.dice_count === 2 &&
      choice.roll.die_sides === 6 &&
      choice.success.text !== choice.failure.text &&
      choice.success.text.length >= 30 &&
      choice.failure.text.length >= 30
    ))
  }
  const guardian = packs.find((entry) => entry.landId === 'cave').pack.encounters
    .find((card) => card.id === 'the-forgotten-pledge')
  assert.equal(guardian.art.cast[0].species, 'gorilla')
  assert.match(guardian.flavor_text, /imposed by a ritual, not his ancestry/)
})

test('every location reproducibly draws fixed identities with no reroll farming', () => {
  for (const { pack } of packs) {
    for (const location of pack.locations) {
      const observed = new Set()
      for (let seed = 1; seed <= 300; seed++) {
        const card = previewSelect(pack, seed, location.location_id)
        assert.equal(card, previewSelect(pack, seed, location.location_id))
        assert.equal(card.location_id, location.location_id)
        assert.ok(location.encounter_ids.includes(card.id))
        observed.add(card.id)
        const second = previewSelect(pack, seed, location.location_id, [card.id])
        assert.ok(second && second.id !== card.id)
        assert.notEqual(second.art.cast[0].identity, card.art.cast[0].identity)
        assert.equal(
          previewSelect(pack, seed, location.location_id, location.encounter_ids),
          null,
        )
      }
      assert.ok(observed.size >= 2, 'seed draws must vary among identities')
    }
  }
})

test('causal shifts are authored and never replace earlier history', () => {
  for (const { landId, pack } of packs) {
    const shifting = pack.encounters.flatMap((card) =>
      card.choices.filter((choice) =>
        choice.success.map_effect === 'recorded-prospective-shift' ||
        choice.failure.map_effect === 'recorded-prospective-shift',
      ).map((choice) => ({ card, choice })),
    )
    assert.ok(shifting.length >= 1, landId + ' must include a causal shift possibility')
    for (const { choice } of shifting)
      assert.equal(choice.failure.map_effect, 'none', 'failure cannot silently trigger a successful route alteration')
  }
})

test('later-land packs remain independent design drafts, not unverified runtime or ArtImage claims', () => {
  assert.ok(packs.every(({ pack }) => pack.status === 'draft-not-imported'))
  assert.ok(packs.every(({ pack }) => pack.source_world_manifest.schema_version === 2))
  const malformed = structuredClone(packs[0].pack)
  malformed.encounters[0].art.art_ref = 'unverified-live-id'
  assert.ok(
    validatePack(malformed, world, schema, 'dustwater')
      .some((message) => message.includes('design-only')),
  )
  const swapped = structuredClone(packs[0].pack)
  swapped.locations[0].encounter_ids[0] = packs[1].pack.encounters[0].id
  assert.ok(
    validatePack(swapped, world, schema, 'dustwater')
      .some((message) => message.includes('membership')),
  )
})
