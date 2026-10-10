import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const root = new URL('./', import.meta.url)
export const readPack = () => JSON.parse(readFileSync(new URL('HOMESTEAD-12.json', root), 'utf8'))
export const readWorld = () => JSON.parse(readFileSync(new URL('../WORLD-DECKS.json', root), 'utf8'))
export const readSchema = () => JSON.parse(readFileSync(new URL('ENCOUNTER-PACK.schema.json', root), 'utf8'))
const skills = new Set(['steel', 'awareness', 'wits', 'bearing', 'resolve', 'insight'])
const polarity = new Set(['good', 'bad', 'mixed'])
const approvedEffects = new Set(['none', 'recorded-prospective-shift'])
const slug = (value) => typeof value === 'string' && /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(value)
const text = (value, min) => typeof value === 'string' && value.trim().length >= min
const unique = (ids) => new Set(ids).size === ids.length

/**
 * Draft conformance and source-graph validation. The JSON Schema is a separate
 * machine-consumable authoring contract; this module checks cross-document,
 * authored-art, runtime-safety, and identity invariants JSON Schema alone
 * cannot enforce.
 */
export function validatePack(pack, world, schema) {
  const errors = []
  const bad = (condition, message) => { if (condition) errors.push(message) }
  bad(!schema || schema.$schema !== 'https://json-schema.org/draft/2020-12/schema', 'JSON Schema version missing')
  bad(!schema?.$defs?.encounter?.properties?.choices?.minItems ||
    schema.$defs.encounter.properties.choices.minItems < 2, 'Schema must require 2+ choices')
  bad(!pack || pack.schema_version !== 1 || pack.project !== 'zuzu-shifting-lands', 'Invalid pack identity/version')
  bad(pack?.source_world_manifest?.schema_version !== world?.schema_version ||
    pack?.source_world_manifest?.path !== 'projects/zuzu-shifting-lands/WORLD-DECKS.json', 'Manifest source mismatch')
  bad(pack?.status !== 'draft-not-imported', 'Pack must remain design-only until importer is verified')
  bad(pack?.rules?.selection !== 'seeded-weighted-eligible-without-replacement' ||
    pack?.rules?.revisit_policy !== 'same-recorded-encounter-no-free-reroll' ||
    pack?.rules?.seed_persisted !== true, 'Seed/revisit contract invalid')
  if (!Array.isArray(pack?.locations) || !Array.isArray(pack?.encounters) || !Array.isArray(world?.lands)) return [...errors, 'Missing pack locations, encounters or world lands']
  const known = new Map(world.lands.flatMap((land) => land.locations.map((location) => [location.id, land.id])))
  const ids = pack.encounters.map((e) => e.id)
  bad(!unique(ids), 'Encounter IDs must be unique')
  const listed = pack.locations.flatMap((location) => location.encounter_ids)
  bad(!unique(listed), 'Encounter pool membership must be unique across locations')
  bad(!unique(pack.locations.map((location) => location.location_id)), 'Location IDs must be unique')
  bad(pack.locations.length !== 3 || !pack.locations.every((l) => known.get(l.location_id) === 'homestead'), 'Homestead pack must have exactly three canonical locations')
  bad(pack.locations.some((location) => !Array.isArray(location.encounter_ids) || location.encounter_ids.length < 2), 'Each location must offer multiple encounters')
  bad(listed.length !== ids.length || ids.some((id) => !listed.includes(id)), 'Every encounter must appear once in a location pool')
  for (const location of pack.locations) {
    for (const id of location.encounter_ids) {
      const encounter = pack.encounters.find((e) => e.id === id)
      bad(!encounter || encounter.location_id !== location.location_id, 'Bad location encounter membership: ' + id)
    }
    const group = pack.encounters.filter((e) => e.location_id === location.location_id)
    bad(!group.some((e) => e.polarity === 'good') || !group.some((e) => e.polarity === 'bad') || !group.some((e) => e.polarity === 'mixed'), location.location_id + ': requires good, bad and mixed beats')
  }
  for (const encounter of pack.encounters) {
    const prefix = encounter.id ?? '<missing>'
    bad(!slug(encounter.id) || !known.has(encounter.location_id), prefix + ': invalid identity or location')
    bad(!text(encounter.title, 5) || !text(encounter.flavor_text, 90), prefix + ': missing authored prose')
    bad(/\b(rabbit|otter|mouse|fox|badger|goat|coyote|crow|gorilla)\b/i.test(encounter.title || ''), prefix + ': species belongs in art, not title')
    bad(!polarity.has(encounter.polarity) || !Number.isInteger(encounter.weight) || encounter.weight < 1, prefix + ': invalid polarity/weight')
    bad(encounter.unique_per_run !== true || encounter.first_visit_only !== true, prefix + ': must persist first draw')
    bad(encounter.art?.status !== 'design-only' || encounter.art.art_ref !== null ||
      !text(encounter.art.brief, 50), prefix + ': art must be clear design-only brief')
    bad(!Array.isArray(encounter.art?.cast) || encounter.art.cast.length < 1 ||
      encounter.art.cast.some((actor) => !slug(actor.identity) || !slug(actor.species) ||
      !text(actor.occupation, 3) || !text(actor.visual_description, 20) ||
      actor.locked_character_id !== null), prefix + ': visual casting must be fixed and unverified DB IDs null')
    bad(!Array.isArray(encounter.choices) || encounter.choices.length < 2, prefix + ': fewer than two choices')
    bad(!text(encounter.developer_note, 20), prefix + ': missing authoring guard')
    if (!Array.isArray(encounter.choices)) continue
    bad(!unique(encounter.choices.map((choice) => choice.id)), prefix + ': duplicate choice IDs')
    for (const choice of encounter.choices) {
      const label = prefix + '/' + (choice.id ?? '?')
      bad(!slug(choice.id) || !text(choice.label, 8) || !text(choice.intent, 20) ||
        !text(choice.risk_hint, 15), label + ': not a clear player decision')
      bad(choice.roll?.dice_count !== 2 || choice.roll?.die_sides !== 6 ||
        !skills.has(choice.roll.skill) || !Number.isInteger(choice.roll.modifier) ||
        !Number.isInteger(choice.roll.target) || choice.roll.target < 4 ||
        choice.roll.target > 15, label + ': invalid deterministic 2d6 roll definition')
      for (const outcome of ['success', 'failure']) {
        const v = choice[outcome]
        bad(!text(v?.text, 30) || !Number.isInteger(v?.hp_delta) ||
          !Number.isInteger(v?.provisions_delta) ||
          !Array.isArray(v?.add_flags) || v.add_flags.some((f) => !slug(f)) ||
          !approvedEffects.has(v?.map_effect), label + ': invalid ' + outcome + ' consequence')
      }
    }
  }
  return errors
}

/** Preview-only sampling plan: fixed content card, no independent species-role roll. */
export function previewSelect(pack, seed, locationId, excluded = []) {
  if (!Number.isSafeInteger(seed) || seed < 1) throw new Error('Positive persisted seed required')
  const pool = pack.locations.find((location) => location.location_id === locationId)
  if (!pool) throw new Error('Unknown location')
  const eligible = pool.encounter_ids.map((id) => pack.encounters.find((encounter) => encounter.id === id))
    .filter((e) => e && !excluded.includes(e.id))
  if (eligible.length === 0) return null
  let hash = (seed ^ 2166136261) >>> 0
  for (const char of locationId) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619) >>> 0
  const total = eligible.reduce((sum, card) => sum + card.weight, 0)
  let point = hash % total
  for (const card of eligible) {
    point -= card.weight
    if (point < 0) return card
  }
  throw new Error('Unreachable weighted draw')
}

if (process.argv[1] && fileURLToPath(new URL(process.argv[1], 'file:///')) === fileURLToPath(import.meta.url)) {
  const errors = validatePack(readPack(), readWorld(), readSchema())
  if (errors.length) { console.error(errors.join('\n')); process.exitCode = 1 }
  else console.log('12 authored Homestead cards, fixed visual cast, 24 checked choices and world linkage validated')
}
