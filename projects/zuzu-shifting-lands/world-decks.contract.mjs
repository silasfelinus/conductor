import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const manifestPath = new URL('./WORLD-DECKS.json', import.meta.url)
const knownSkills = new Set(['steel', 'awareness', 'wits', 'bearing', 'resolve', 'insight'])
const forbiddenFacetFields = ['alignment', 'morality', 'disposition', 'secret', 'agenda']
const has = (object, name) => Object.prototype.hasOwnProperty.call(object, name)
const isRecord = (value) => value !== null && typeof value === 'object' && !Array.isArray(value)
const unique = (items) => new Set(items).size === items.length
const strings = (items) => Array.isArray(items) && items.length > 0 && items.every((value) => typeof value === 'string' && value.length > 0)
const keys = (items) => (Array.isArray(items) ? items.map((item) => item?.key) : [])

export function loadWorldDecks(path = manifestPath) {
  return JSON.parse(readFileSync(path, 'utf8'))
}

/** Validate graph references, taxonomy, chapter order, art provenance and spoiler-safe fronts. */
export function validateWorldDecks(m) {
  const errors = []
  const check = (ok, message) => { if (!ok) errors.push(message) }
  if (!isRecord(m)) return ['World deck manifest must be an object']
  check(m.schema_version === 2, 'schema_version must equal 2')
  check(m.world_id === 'zuzu' && m.world_tag === 'zuzu', 'World identity must be zuzu')
  check(m.conductor_project === 'zuzu-shifting-lands', 'Wrong project join')
  check(m.status === 'design-manifest-not-imported', 'Design catalog must not claim live import')
  check(isRecord(m.source_contract) && m.source_contract.world_registry === 'worlds/zuzu/catalog.json', 'World registry provenance missing')
  check(isRecord(m.journey) && m.journey.lands === 5 && m.journey.encounters_per_land === 3 && m.journey.major_challenges === 5 && m.journey.seed_persisted === true, 'Journey counts or seed contract invalid')
  if (!isRecord(m.facet_pools)) return [...errors, 'facet_pools missing']
  const { species, roles, dispositions, conditions } = m.facet_pools
  for (const [label, pool, validTaxonomies] of [
    ['species', species, ['SPECIES']],
    ['roles', roles, ['OCCUPATION', 'ROLE', 'ARCHETYPE']],
  ]) {
    check(Array.isArray(pool) && pool.length > 0, label + ' Facet pool missing')
    if (!Array.isArray(pool)) continue
    check(unique(keys(pool)), label + ' Facet keys must be unique')
    for (const entry of pool) {
      check(isRecord(entry) && typeof entry.key === 'string' && entry.key.length > 0, label + ' invalid key')
      if (!isRecord(entry)) continue
      check(validTaxonomies.includes(entry.taxonomy), label + ':' + entry.key + ' taxonomy invalid')
      check(strings(entry.biomes), label + ':' + entry.key + ' biomes missing')
      check(Number.isInteger(entry.weight) && entry.weight > 0, label + ':' + entry.key + ' weight invalid')
      check(forbiddenFacetFields.every((field) => !has(entry, field)), label + ':' + entry.key + ' hardcodes morality/agenda')
    }
  }
  check(strings(dispositions) && unique(dispositions), 'Disposition pool must be independent and nonempty')
  check(strings(conditions) && unique(conditions), 'Conditions pool invalid')
  const refs = new Map()
  if (!Array.isArray(m.art_refs)) errors.push('art_refs missing')
  for (const art of m.art_refs ?? []) {
    if (!isRecord(art)) { errors.push('Invalid art reference'); continue }
    check(!refs.has(art.key), 'Duplicate artwork key ' + art.key)
    refs.set(art.key, art)
    check(art.status === 'repository-file' && art.source_repo === 'silasfelinus/kind_robots', 'Art has unverified source ' + art.key)
    check(typeof art.repo_path === 'string' && /^public\\/zuzu-gamebook\\/scenes\\/[a-z0-9-]+\\.webp$/.test(art.repo_path), 'Art path does not match vetted public scenes: ' + art.key)
    check(art.art_image_id === null, 'Repo-file does not establish a live ArtImage ID: ' + art.key)
  }
  const checkRuntimeRefs = (items, model, name) => {
    if (!Array.isArray(items)) { errors.push(name + ' missing'); return new Set() }
    const catalog = new Set()
    for (const ref of items) {
      if (!isRecord(ref)) { errors.push(name + ' malformed entry'); continue }
      check(typeof ref.key === 'string' && !catalog.has(ref.key), name + ' duplicate/invalid key ' + ref.key)
      catalog.add(ref.key)
      check(ref.model === model && ['design-only', 'verified'].includes(ref.status), name + ' type/status mismatch ' + ref.key)
      check(ref.status === 'design-only' ? ref.runtime_id === null : Number.isSafeInteger(ref.runtime_id) && ref.runtime_id > 0, name + ' identity is unverified ' + ref.key)
    }
    return catalog
  }
  const scenarios = checkRuntimeRefs(m.scenario_refs, 'Scenario', 'scenario_refs')
  const rewards = checkRuntimeRefs(m.reward_refs, 'Reward', 'reward_refs')
  if (!Array.isArray(m.lands) || m.lands.length !== 5) return [...errors, 'Expected five land definitions']
  const ids = [], locations = [], bosses = [], usedArt = new Set()
  for (const [index, land] of m.lands.entries()) {
    if (!isRecord(land)) { errors.push('Invalid land at ' + index); continue }
    check(land.chapter === index + 1, 'Nonsequential chapter ' + land.id)
    check(typeof land.id === 'string' && typeof land.name === 'string' && land.biome === land.id, 'Land identity/biome invalid ' + land.id)
    ids.push(land.id)
    for (const [label, pool, used] of [['species', species, land.species], ['roles', roles, land.roles]]) {
      check(strings(used) && unique(used), 'Missing/duplicate ' + label + ' in land ' + land.id)
      for (const key of used ?? []) {
        check(Array.isArray(pool) && pool.some((entry) => entry.key === key && entry.biomes?.includes(land.biome)), 'Incompatible ' + label + ':' + key + ' in ' + land.id)
      }
    }
    if (!Array.isArray(land.locations) || land.locations.length !== 3) { errors.push('Land requires three locations: ' + land.id); continue }
    for (const loc of land.locations) {
      if (!isRecord(loc)) { errors.push('Malformed location in ' + land.id); continue }
      locations.push(loc.id)
      check(typeof loc.label === 'string' && loc.label.length > 0 && typeof loc.id === 'string', 'Location identity missing in ' + land.id)
      check(scenarios.has(loc.template), 'Unknown Scenario design reference ' + loc.template)
      check(knownSkills.has(loc.skill) && [7, 9, 11].includes(loc.difficulty), 'Invalid check at ' + loc.id)
      check(Array.isArray(loc.possible_rewards) && loc.possible_rewards.length > 0 && loc.possible_rewards.every((key) => rewards.has(key)), 'Invalid Reward reference at ' + loc.id)
      check(typeof loc.front_teaser === 'string' && loc.front_teaser.length > 8 && !/ritual|sacrifice|cosmic horror|child(?:ren)? harm/i.test(loc.front_teaser), 'Unsafe card-front teaser ' + loc.id)
      if (loc.art_ref !== null) { check(refs.has(loc.art_ref), 'Unknown source artwork ' + loc.art_ref); usedArt.add(loc.art_ref) }
    }
    const boss = land.major_challenge
    if (!isRecord(boss)) { errors.push('Missing boss slot in ' + land.id); continue }
    bosses.push(boss.id)
    check(typeof boss.id === 'string' && typeof boss.label === 'string' && strings(boss.outcome_modes) && unique(boss.outcome_modes), 'Boss identity/modes invalid in ' + land.id)
    check(typeof boss.front_teaser === 'string' && boss.front_teaser.length > 8 && !/ritual|sacrifice|cosmic horror|child(?:ren)? harm/i.test(boss.front_teaser), 'Unsafe boss card-front in ' + land.id)
    if (boss.art_ref !== null) { check(refs.has(boss.art_ref), 'Unknown boss artwork ' + boss.art_ref); usedArt.add(boss.art_ref) }
  }
  check(unique(ids), 'Duplicate land IDs')
  check(unique(locations) && locations.length === 15, 'Locations must be globally unique and total fifteen')
  check(unique(bosses) && bosses.length === 5, 'Boss slots must be globally unique and total five')
  check(usedArt.size === refs.size, 'Unreferenced artwork pointer in design manifest')
  if (!Array.isArray(m.named_exceptions)) errors.push('Named exceptions missing')
  else for (const entry of m.named_exceptions) {
    check(ids.includes(entry.land_id) && entry.source === 'worlds/zuzu/WORLD-GUIDE.md', 'Named exception missing provenance/land')
    check(entry.runtime_character_id === null, 'Unverified live Character ID in named exceptions')
    if (has(entry, 'locked_art_image_id')) check(Number.isSafeInteger(entry.locked_art_image_id) && entry.locked_art_source === 'worlds/zuzu/catalog.json', 'Locked cast anchor missing registry provenance')
  }
  return errors
}

export function assertValidWorldDecks(manifest) {
  const errors = validateWorldDecks(manifest)
  if (errors.length) throw new Error('Shifting Lands manifest invalid:\\n' + errors.join('\\n'))
  return manifest
}

/** Explicit field allowlist. Never serialise the full developer manifest to the player. */
export function toPlayerBoard(manifest, { activeChapter = 1, completedLocationIds = [] } = {}) {
  assertValidWorldDecks(manifest)
  if (!Number.isInteger(activeChapter) || activeChapter < 1 || activeChapter > 5) throw new Error('Invalid chapter')
  if (!Array.isArray(completedLocationIds) || completedLocationIds.some((id) => typeof id !== 'string')) throw new Error('Invalid resolved locations')
  const arts = new Map(manifest.art_refs.map((ref) => [ref.key, '/' + ref.repo_path.replace(/^public\\//, '')]))
  const image = (key) => key === null ? null : arts.get(key) ?? null
  return {
    schema_version: 2,
    world_id: 'zuzu',
    active_chapter: activeChapter,
    lands: manifest.lands.map((land) => {
      if (land.chapter > activeChapter) return { id: land.id, chapter: land.chapter, revealed: false }
      const allFinished = land.locations.every((loc) => completedLocationIds.includes(loc.id))
      return {
        id: land.id,
        chapter: land.chapter,
        revealed: true,
        name: land.name,
        locations: land.locations.map((loc) => ({
          id: loc.id, label: loc.label, front_teaser: loc.front_teaser, art_url: image(loc.art_ref),
        })),
        major_challenge: allFinished ? {
          id: land.major_challenge.id,
          label: land.major_challenge.label,
          front_teaser: land.major_challenge.front_teaser,
          art_url: image(land.major_challenge.art_ref),
        } : null,
      }
    }),
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const manifest = loadWorldDecks()
  assertValidWorldDecks(manifest)
  console.log('Shifting Lands manifest v2 valid: 5 lands, 15 encounter slots, 5 boss gates; source art and player projection checked')
}
