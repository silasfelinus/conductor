# packmaker changelog

## 2026-07-05
- Project created from Silas's session direction (digital store relaunch): a
  repeatable, pipeline-aware generator for DLC packs and builder items
  (locations, genres, characters, rewards) with admin and user views.
- Launch pack working names set: Uncanny Valor (super-powers), Arcane Whimsy
  (magic-powers) — Silas may rename.
- Registered in project-overrides.yaml, projects/priority.yaml, CONTROL.md;
  icon/card/hero art queued in art-prompts.yaml.

## 2026-07-15
- t-001 done: SPEC.md design brief written. Maps pack item types onto
  existing kind_robots models (Dream, Facet, Character, Reward) with no new
  schema; generator reuses existing chat/art/dream endpoints; user view
  builds on the already-shipped `/packs` scaffold. Ownership/privacy stays
  interim (isPublic/isMature/isActive) pending kind-robots t-008; DLC
  purchases build on digital-storefront's existing Product/Entitlement
  design (t-009) rather than a new entitlement model.
