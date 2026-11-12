# Zuzu Gamebook art delivery gap audit — 2026-11-12

Source: `kind_robots/utils/zuzuGamebook/book.ts`, nine `acts/act*.ts`, `sectionArt.ts`, `art.ts`, and the checked-in `public/zuzu-gamebook/scenes` assets on 2026-11-12.

**This is a worklist, not a declaration that art is complete.** All 15 endings currently resolve through `sectionPlate(scene(id))` to an existing painted image (the water ending uses a purpose-rendered legacy `kasa-on-water.webp`); this is distinct from one *unique* plate for every page.

| Measure | Count | Meaning |
|---|---:|---|
| Authored section IDs found in the canonical `s(...)` declarations | 384 | Scenes in `book.ts` and acts I–IX |
| Exact `SECTION_PLATES` keys | 349 | Independently registered scene-specific images |
| Sections without their own exact registry entry | 35 | Some intentionally borrow shared art; others are missing a dedicated finished render |
| Existing files under `scenes/sections/` | 371 | Includes 22 shared environmental files; *not* all are unique registered scene plates |
| Endings with painted `sectionPlate` fallback or exact illustration | 15/15 | Includes existing purpose-painted water ending |

## Seven previously unqueued, newly authored/rewritten scene beats

`ROUND-20-FINAL-SCENE-GAPS.yaml` requests **two private Arthemy candidates per scene** (14 image jobs total, submission subject to automation). These were absent from `ROUND-1..19` art ledgers and do not have exact registered plates today.

- `a1-ridge-retreat`: wounded Zuzu climbs above the reeds as the one-eyed coyote covers his retreat
- `a4-well-scatter`: supplies thrown down at the dry well while the children escape into the rock cleft
- `a4-well-slip`: the sister distracts the bandits with a bandage and leads a narrow escape
- `a8-under-the-wall`: Zuzu returns alone through the dry drain under the midnight mission wall
- `a8-behind-the-altar`: the covert altar view, black candles, rope and cold gap behind the wall
- `a8-wounded-flight`: rope severed, children's escape up the stair, widening dark breach at the altar
- `a8-give-ground`: wounded Zuzu alone at the lowest stair, sword low, candles and dark behind him

The seven new requests **do not count as delivered artwork**. After ArtJob DONE, a visual reviewer must choose a scene-true candidate and record the ArtImage provenance, copy the real WebP under `scenes/sections/<id>.webp`, and register exact `SECTION_PLATES[id]`. Wrong subject/pose/objects must be rerolled, never quietly marked `fit: exact`. Each manifest remains `is_public: false`.

## Other exact-registration gaps

`standoff`, `coyote`, `crocodile`, `aftermath`, `parting`, `survivors`, `apple-tree`, `relic`, `wagon`, `supper`, `courtyard`, `tracks`, `chapel`, `dormitory`, `caught`, `morning`, `mission`, `posters`, `saloon`, `cellar`, `stabbed`, `abbess`, `rescue`, `ending-water`, `a2-wax`, `a2-bell-view`, `a3-apples-reach`, `a4-bloom`.

Before queuing any of those again, reconcile `ROUND-17`, `ROUND-18-KREA-COMPOSITION`, the current delivered files and the existing shared environmental art. Particularly:
- `a2-bell-view` and `a4-bloom` have reviewed stage-one composition candidates but Round-19 style conversion is still gated on the third `a2-gift` selection. Do not claim these complete.
- `a2-wax`, `apple-tree` and `a3-apples-reach` have generated Round-17 candidates. Inspect the actual render before assigning a scene plate.
- `ending-water` already has the purpose-rendered `kasa-on-water.webp` in the legacy `PLATES` registry. The engine does not need a new generated ending; it should not be disguised as `SECTION_PLATES['ending-water']` unless an identically named file is actually exported.
- Several other keys intentionally reuse older plates; only mark them finished when the explicit current acceptance policy considers scene fidelity adequate.

**Exit requirement:** art task `t-006` stays open until reviewed, delivered images and accurate registry entries are verified; final `t-009` art/device/ending QA follows. The final subjective acceptance gate is `t-017`, not the historical done `t-010`.
