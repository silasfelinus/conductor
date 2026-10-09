/** Version 2 is a source-design contract, not a claim that Kind Robots DB rows exist. */
export type Skill = 'steel' | 'awareness' | 'wits' | 'bearing' | 'resolve' | 'insight'
export type Taxonomy = 'SPECIES' | 'OCCUPATION' | 'ROLE' | 'ARCHETYPE'
export type FacetPoolEntry = {
  key: string
  taxonomy: Taxonomy
  biomes: string[]
  weight: number
  traits?: string[]
}
export type RuntimeReference = {
  key: string
  model: 'Scenario' | 'Reward'
  status: 'design-only' | 'verified'
  runtime_id: number | null
}
export type ArtworkReference = {
  key: string
  source_repo: 'silasfelinus/kind_robots'
  repo_path: string
  status: 'repository-file'
  art_image_id: null
}
export type LocationEntry = {
  id: string
  label: string
  template: string
  skill: Skill
  difficulty: 7 | 9 | 11
  possible_rewards: string[]
  front_teaser: string
  art_ref: string | null
}
export type BossEntry = {
  id: string
  label: string
  outcome_modes: string[]
  front_teaser: string
  art_ref: string | null
  boss_source?: string
  canon_motivation?: string
  presentation?: string
  reveal_rule?: string
}
export type LandEntry = {
  id: string
  name: string
  chapter: number
  biome: string
  provisional?: boolean
  species: string[]
  roles: string[]
  locations: [LocationEntry, LocationEntry, LocationEntry]
  major_challenge: BossEntry
}
export type WorldDecksV2 = {
  schema_version: 2
  world_id: 'zuzu'
  conductor_project: 'zuzu-shifting-lands'
  world_tag: 'zuzu'
  status: 'design-manifest-not-imported'
  source_contract: Record<string, string>
  editorial_rules: Record<string, string>
  player: Record<string, unknown>
  journey: {
    lands: 5
    encounters_per_land: 3
    major_challenges: 5
    seed_persisted: boolean
    repeatability: string
    mutations: string
  }
  facet_pools: {
    species: FacetPoolEntry[]
    roles: FacetPoolEntry[]
    dispositions: string[]
    conditions: string[]
  }
  scenario_refs: RuntimeReference[]
  reward_refs: RuntimeReference[]
  art_refs: ArtworkReference[]
  named_exceptions: Array<{
    id: string
    source: string
    type: string
    land_id: string
    runtime_character_id: number | null
    rule: string
    locked_art_image_id?: number
    locked_art_source?: string
  }>
  lands: [LandEntry, LandEntry, LandEntry, LandEntry, LandEntry]
  world_mysteries: Array<Record<string, string>>
}
/** Intentionally allowlisted player payload: developer secrets never flow into it. */
export type PlayerLocation = Pick<LocationEntry, 'id' | 'label' | 'front_teaser'> & { art_url: string | null }
export type PlayerLand = {
  id: string
  chapter: number
  revealed: boolean
  name?: string
  locations?: PlayerLocation[]
  major_challenge?: { id: string; label: string; front_teaser: string; art_url: string | null } | null
}
export type PlayerBoard = {
  schema_version: 2
  world_id: 'zuzu'
  active_chapter: number
  lands: PlayerLand[]
}
