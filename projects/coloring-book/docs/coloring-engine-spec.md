# Shared Coloring Engine Spec

date: 2026-07-10
task: coloring-book/t-003
status: draft for review
inputs: kind_robots PR #135 (`/mural` color studio), projects/mural-design/WONDERLAB-COLORING-SPEC.md,
projects/mural-design/roadmap.yaml (t-007 note), projects/coloring-book/DESIGN-BRIEF.md
related: coloring-book t-004 (generation pipeline — owns the final SVG-vs-raster region decision),
coloring-book t-005 (app surface), mural-design t-002 (real fence assets)

This document specs how the shipped kind_robots mural color studio generalizes into one
shared coloring engine consumed by both **mural-design** (fence paint planning) and
**coloring-book** (the coloring book app). Coordinate, don't fork: `/mural` keeps working
through every step.

---

## 1. What exists today (the shipped mural implementation)

Shipped in kind_robots PR #135 (`feat(mural): add WonderLab color studio`, commit
`1fc7d581`), with asset and bridge follow-ups in PR #139. All paths below are in
`/home/user/kind_robots`.

### 1.1 File map

| File | Role |
|---|---|
| `stores/muralStore.ts` | Pinia setup store: palette, sections, selection, fills, localStorage persistence. All logic lives here. |
| `components/wonderlab/mural-manager.vue` | The whole UI: inline SVG canvas + palette sidebar + groups/sections sidebar. Talks only to the store. |
| `content/mural.md` | Nuxt Content page for route `/mural` (rendered by the `pages/[...slug].vue` catch-all via `ContentRenderer`; body is just `:mural-manager`). Frontmatter: `dashboardKey: wonder`, `dashboardTab: wonder-lab`, `cards: labCards`. |
| `stores/helpers/labCards.ts` | The **temporary WonderLab card bridge**: `LAB_CARDS` = cards derived from `dashboardConfigs.wonder.tabs` **plus** a hand-built `muralTab` card appended via `deriveNavCard(muralTab, …)` pointing at `/mural`. |
| `stores/helpers/tutorialCards.ts` | Tutorial wiring: `ExtraTutorialKey = 'conductor' | 'mural'`, a `mural` tutorial channel entry, and `tutorialRouteMap.mural = '/mural'`. |
| `public/images/dashboard-tabs/wonder/mural.webp` | Card image (256 KB real webp — PR #139 replaced the original 55-byte placeholder). |
| `public/images/tutorials/mural/mural.webp` | Tutorial hero — byte-identical copy of the card image. |

Important negative findings:

- **Mural is NOT in the canonical `dashboardConfigs.wonder.tabs` registry**
  (`stores/helpers/dashboardHelper.ts` wonder tabs are only memory-dungeon,
  wonder-lab, screen-fx). It reaches WonderLab cards solely through the labCards
  bridge — commit `2a0ea521` deliberately kept the bridge "until canonical tab lands".
  Removing the bridge is an open follow-up from mural t-007.
- **None of the WONDERLAB-COLORING-SPEC asset pipeline exists.** There is no
  `public/data/` directory at all, no `mural-environment.webp`, no `mural-lineart.svg`,
  no `mural-section-map.svg`, no `mural-sections.json`, no `mural-palette.json`. The
  canvas is not derived from `firstdraft.jpg` in any way.

### 1.2 Region/section data model — hand-authored inline SVG

The coloring surface is a single inline `<svg viewBox="0 0 960 540">` in
`mural-manager.vue`. It renders one `<path>` per section, `fill` bound to the section's
resolved color, plus one static non-interactive black stroke path for decorative
linework (whiskers, smiles). There is no raster underlay, no image layer, no locked
colored environment — everything on screen is these paths.

Sections are **20 hardcoded objects** in `muralStore.ts` (`defaultSections`), each with a
hand-written path `d` string approximating the mural composition (wine sky, ivy portal,
Totoro body/belly, Catbus body/roof/face/eyes, 3 windows, 2 robots, 3 butterflies, soot
sprites, alien ground, portal glow):

```ts
export interface MuralSection {
  id: string        // stable, e.g. 'catbus-window-1'
  label: string
  groupId: string   // 'background' | 'foliage' | 'catbus' | 'windows' | ...
  colorId: string   // current fill, by palette id — never raw hex
  d: string         // SVG path data
}
```

Groups are **derived, not stored**: a `groups` computed buckets sections by `groupId`
in first-seen order, title-cases the id into a label, and reports `colorId: 'mixed'`
(sentinel) when a group's sections disagree. There is no separate group entity to keep
in sync — a good property worth keeping.

Note the shipped model is a *simplification* of WONDERLAB-COLORING-SPEC's `MuralSection`
(no `defaultColorId`, no `pathId` — path data is inline; defaults live in the
`defaultSections` constant itself).

### 1.3 Color/swatch model

```ts
export interface MuralColor {
  id: string     // role id, e.g. 'wine-red', 'leaf-true'
  name: string
  value: string  // '#rrggbb', validated/normalized to '#ffffff' on bad input
}
```

13 default swatches matching Silas's PPG palette direction (wine-red, three greens,
catbus orange/brown, window teal, butterfly purple/violet, warm yellow, soft white,
robot gray, line black). Sections reference **color ids, never hex** — recoloring a
swatch would restyle every section using it (the key indirection the paint-planning
workflow needs). Users can add swatches (id = name slug + base36 timestamp) and remove
them (sections using a removed color are reassigned to the first surviving swatch;
removal blocked when only one swatch remains). The spec'd `ppgName`/`ppgCode`/`locked`
fields did not ship.

### 1.4 Store shape and persistence

`stores/muralStore.ts`, Pinia setup store id `'muralStore'`:

- **State**: `colors: MuralColor[]`, `sections: MuralSection[]`, `activeColorId`,
  `selectedSectionId`, `initialized`.
- **Computeds**: `colorMap`, `activeColor`, `selectedSection`, `groups`.
- **Actions**: `initialize(force?)`, `setActiveColor`, `selectSection`,
  `setSectionColor(sectionId, colorId = active)`, `setGroupColor(groupId, colorId = active)`,
  `addSavedColor`, `removeSavedColor`, `resetMural`.
- **Persistence**: single localStorage key **`kindRobotsMuralState`**, whole-state JSON
  (`{colors, sections, activeColorId, selectedSectionId}`) rewritten by a `sync()` call
  after every mutation. Guarded for SSR (`typeof window` check) and wrapped in
  try/catch both ways. `initialize()` is called from the component's `onMounted`.

One design decision in `initialize()` matters a lot for the shared engine: **saved
sections contribute only their `colorId`** — geometry is always rebuilt from
`defaultSections`, with saved fills merged on by id. Stored state is a *fill diff*, not
a page copy, so shipping new/edited paths never fights stale localStorage. Saved
*colors*, by contrast, wholly replace the default palette (a saved-state array
overwrites `defaultColors`), which is why swatch state survives across visits. Keep the
fill-diff pattern; make the palette merge additive in the shared engine (defaults +
user additions) rather than replace-all.

### 1.5 Fill interactions (shipped)

1. Pick an active swatch in the left sidebar.
2. **Click a path in the SVG** → `setSectionColor(id)`: paints it with the active color
   *and* selects it (selection shown by thicker stroke in the active color + drop shadow).
3. **Fill group** button per group → `setGroupColor`: floods every section in the group.
4. **Per-section override**: badge buttons under each group select a section without
   painting (`selectSection`); a "Paint selected with active color" button applies.
5. **Reset** → `resetMural()`: restores default colors, sections, active/selected, and
   persists the reset.
6. Add/remove saved swatches (see 1.3).

Not shipped (vs WONDERLAB-COLORING-SPEC and vs coloring-book needs): multi-select,
global color-id **swap**, editing an existing swatch's hex (recolor-everywhere),
palette/assignment JSON **import/export**, named paint schemes, **undo** (reset is the
only recovery), and export-to-image.

### 1.6 Placeholder vs real — honest inventory

| Piece | Status |
|---|---|
| Store logic, persistence, fill interactions | **Real** and solid; patterns worth extracting as-is. |
| Section geometry | **Placeholder-quality by design**: hand-drawn approximations, not traced from `firstdraft.jpg`. t-007 note calls the whole thing "a starter/manual UI scaffold". |
| Default palette | Real direction (matches Silas's PPG roles) but hex values are provisional until the PPG swatch task (mural t-004). |
| Card/tutorial webp images | Real artwork since PR #139 (originally 55-byte placeholders), though the same file is duplicated in both locations. |
| Coloring assets (environment backplate, lineart, section map, data JSON) | **Do not exist.** Blocked on mural t-002 (Kontext asset generation). |
| WonderLab registration | Temporary labCards bridge; canonical `dashboardConfigs.wonder.tabs` entry still pending. |
| API surface | None — fully client-side, no server routes involved (consistent with the spec's store-only rule). |

---

## 2. Shared engine proposal

Extract the generic 80% of the mural studio into a reusable pair, both living in
kind_robots:

- **`components/coloring/coloring-canvas.vue`** (`ColoringCanvas`) — the interactive
  coloring surface. Renders artwork layers + fillable regions, handles hit-testing and
  paints, emits events. Presentational: no persistence, no routing, no page chrome.
- **`stores/coloringStore.ts`** (`useColoringStore`) — page-keyed coloring state:
  fills, palette additions, selection, undo, persistence, export. One store instance
  manages many pages (keyed map), so the library view and an open page share state.

Consumers:

- **coloring-book** wraps them in the library/app surface (t-005).
- **mural-design** keeps `/mural` and `mural-manager.vue` as a thin specialization:
  its locked-environment/fence-only rule, paint-planning sidebars, PPG naming, and
  assignment-JSON export are wrapper concerns. The mural is just one coloring page
  definition with extra chrome.

### 2.1 Page definition (the component's data contract)

```ts
export interface ColoringColor {
  id: string           // stable role id ('wine-red') or generated id
  name: string
  value: string        // '#rrggbb'
  locked?: boolean     // not removable/editable (mural env colors, line black)
}

export interface ColoringRegion {
  id: string           // stable within the page
  label?: string       // optional; coloring-book pages usually omit
  group?: string       // group-fill bucket; omitted regions form no group
  defaultColorId?: string // starting fill; default 'blank' (white/paper)
  d: string            // SVG path data (svg mode)
}

export interface ColoringPageDefinition {
  id: string           // globally unique: '<setSlug>/<pageId>' or 'mural/fence-v1'
  version: 1
  viewBox: { width: number; height: number }
  mode: 'svg-regions' | 'raster-flood'   // final v1 choice comes from t-004
  layers: {
    underlay?: string  // asset path, drawn beneath fills (mural's locked colored environment)
    lineArt?: string   // asset path, drawn ABOVE fills (crisp black outlines)
    decor?: string     // inline SVG path data stroked above fills (mural whiskers/smiles)
  }
  // svg-regions mode:
  regions?: ColoringRegion[]
  // raster-flood mode (see section 3.2):
  fillBase?: string    // asset path to the white-regions bitmap the canvas floods
  regionMap?: string   // optional indexed-region PNG for stable region ids
  palette: ColoringColor[]  // default palette for this page
}
```

Design rules carried over from the mural implementation:

- Fills reference **color ids, not hex** — recolor-swatch-everywhere and global swap
  stay cheap.
- Groups stay **derived** from `region.group`; no stored group entity.
- Geometry/assets always come from the page definition; persisted state is a diff.

### 2.2 `ColoringCanvas` props and events

```ts
// Props
page: ColoringPageDefinition        // required
fills: Record<string, string>       // regionId -> colorId (controlled by the store/wrapper)
activeColorId: string
selectedRegionIds?: string[]        // selection ring rendering
interactive?: boolean               // default true; false = pure preview/thumbnail
paletteResolver?: (colorId: string) => string  // wrapper overrides hex lookup if needed

// Events
'region-click'   (regionId: string)             // canvas hit; wrapper/store decides paint vs select
'region-filled'  ({ regionId, colorId })        // after a paint is applied
'export-ready'   (blob: Blob, type: 'image/png' | 'image/webp')
```

The canvas is **controlled**: it renders `fills` and emits intents; `coloringStore`
owns mutation, undo, and persistence. That keeps the mural wrapper free to intercept
(e.g. refuse clicks on locked environment regions) without forking the canvas.

In `svg-regions` mode it renders `underlay` (if any) as an `<image>`, one `<path>` per
region with `fill` resolved from `fills`/palette, `decor` stroke paths, then `lineArt`
on top. In `raster-flood` mode it renders a `<canvas>` seeded from `fillBase`, performs
flood fill on click, and composites `lineArt` above.

### 2.3 `coloringStore` shape

```ts
interface PageColoringState {
  fills: Record<string, string>        // regionId -> colorId (svg mode)
  fillOps?: FillOp[]                   // raster mode: replayable {x, y, colorId} ops
  customColors: ColoringColor[]        // user-added swatches (additive over page palette)
  activeColorId: string
  selectedRegionIds: string[]
  undoStack: PatchEntry[]              // bounded, e.g. last 50 ops; in-memory only
  updatedAt: string
}

// store state: pages: Record<pageId, PageColoringState>, currentPageId: string | null
```

Actions (generalizing the mural set): `openPage(def)`, `paintRegion`, `paintGroup`,
`setActiveColor`, `select/deselectRegion`, `addColor`, `removeColor`, `editColor`
(recolor everywhere), `swapColors(aId, bId)` (global swap — the mural spec item that
never shipped), `undo`, `resetPage`, `exportImage(def, opts)`, `exportAssignments(def)`
(JSON of regionId → colorId + palette — the mural paint-spec artifact),
`importAssignments`.

### 2.4 Persistence — keyed per page

One localStorage entry **per page**, not one global blob:

- `kindRobots:coloring:<pageId>` → serialized `PageColoringState` minus `undoStack`
  (fills diff + custom colors + activeColorId only).
- `kindRobots:coloring:index` → `{ pageIds: string[], updatedAt }` for the library's
  "in progress" badges without deserializing every page.

Merge semantics on load (lesson from `muralStore.initialize`): stored fills apply only
where the region id still exists in the definition; stored custom colors are appended
to (never replace) the page palette; unknown color ids in fills fall back to the
region's default. Same SSR guards and try/catch as today. Account-synced persistence
later is a swap of the read/write functions behind the same interface — the storage
key becomes the sync record key.

Migration shim: on first open of the mural page, if `kindRobotsMuralState` exists and
`kindRobots:coloring:mural/fence-v1` does not, translate the old blob (sections'
colorId → fills, colors → customColors delta) and leave the old key in place for one
release before cleanup.

### 2.5 Export-to-image

All client-side, no server route:

- **svg-regions mode**: serialize the rendered SVG (`XMLSerializer`), inline the
  underlay/lineArt images as data URIs, load into an `Image` via Blob URL, draw to an
  offscreen `<canvas>` at export scale (2–4x viewBox for shareable quality; the
  print-ready master comes from the t-004 pipeline, not from this export), then
  `canvas.toBlob('image/png')`.
- **raster-flood mode**: the working canvas already is the image; composite `lineArt`
  on top and `toBlob`.
- Both modes also support `exportAssignments()` JSON (mural's paint-spec need, and a
  cheap "save file" format users could reimport).

---

## 3. Page format (v1 coloring-page package)

Static data under kind_robots `public/` (no DB in v1), following the existing
public-asset conventions:

```
public/data/coloring-book/sets/<setSlug>/manifest.json
public/data/coloring-book/sets/<setSlug>/pages/<pageId>.json
public/images/coloring-book/<setSlug>/<pageId>/lineart.webp     (always)
public/images/coloring-book/<setSlug>/<pageId>/regions.svg      (svg mode)
public/images/coloring-book/<setSlug>/<pageId>/fillbase.png     (raster mode)
public/images/coloring-book/<setSlug>/<pageId>/regionmap.png    (raster mode, optional)
public/images/coloring-book/<setSlug>/<pageId>/thumb.webp
```

The mural's package lives at `public/data/mural-design/` per WONDERLAB-COLORING-SPEC
(same schema, different folder — it is not a coloring-book set).

### 3.1 Page package (`pages/<pageId>.json`)

```jsonc
{
  "id": "kind-robots-p01",
  "setSlug": "kind-robots",
  "title": "AMI Among the Butterflies",
  "version": 1,
  "viewBox": { "width": 1700, "height": 2200 },   // 8.5x11 proportion for print parity
  "lineArt": "/images/coloring-book/kind-robots/p01/lineart.webp",
  "thumb": "/images/coloring-book/kind-robots/p01/thumb.webp",
  "regionDefinition": { /* ONE of the two shapes below */ },
  "palette": [
    { "id": "sky-blue", "name": "Sky Blue", "value": "#7ec8e3" }
    // ... suggested palette; users add their own on top
  ],
  "metadata": {
    "sourceImage": "public/images/bots/ami.webp",  // or null for prompt-only
    "prompt": "convert to coloring book line art: clean black outlines, ...",
    "model": "flux-kontext | <lora id>",
    "generatedAt": "2026-07-12T00:00:00Z",
    "printMaster": "/images/coloring-book/kind-robots/p01/print-2550x3300.png"
  }
}
```

`metadata` satisfies the generated-art rule (traceable prompt/model/source) and gives
the storefront/POD path (t-009) its print-ready original.

### 3.2 Region definition — BOTH shapes (t-004 picks which ships in v1)

The engine treats `regionDefinition` as a tagged union so either pipeline output slots
in without touching the component contract:

**Shape A — SVG regions** (reuses the mural interaction model directly):

```jsonc
{
  "kind": "svg",
  "regions": [
    { "id": "r-001", "group": "sky", "defaultColorId": "blank", "d": "M0 0H1700..." }
    // ...one entry per closed region; ids stable across regenerations when possible
  ]
  // OR, for large pages: "asset": ".../regions.svg" where each fillable <path> carries
  // id / data-group attributes and the loader parses it into the same regions array.
}
```

Pros: crisp hit-testing, per-region ids for free (stable persistence, group fills,
palette-spec export). Cost: requires vectorization (potrace-style) or generation-time
region maps in the pipeline.

**Shape B — raster flood fill** (cheapest thing that ships; every casual coloring app):

```jsonc
{
  "kind": "raster-flood",
  "fillBase": "/images/coloring-book/kind-robots/p01/fillbase.png", // white regions, black lines
  "tolerance": 24,            // flood-fill color-distance tolerance
  "regionMap": "/images/coloring-book/kind-robots/p01/regionmap.png" // OPTIONAL
}
```

Without `regionMap`, region identity is implicit: persistence stores replayable
`fillOps: [{x, y, colorId}]` instead of `fills` (still a small diff; replay on load is
fast). With a `regionMap` (an indexed-color PNG where each region has a unique index —
producible at generation time), the engine gets stable region ids (`"idx-<n>"`) and the
same `fills` record, group metadata, and assignment export as SVG mode. Recommendation
to t-004: if raster wins, biasing toward emitting a regionMap keeps the two modes
nearly behaviorally identical and keeps save data robust against page re-exports.

Group fills and labeled sections are optional in both shapes — coloring-book pages can
ship as ungrouped regions (pure tap-to-fill), while the mural page uses groups heavily.

### 3.3 Set manifest (`manifest.json`)

```jsonc
{
  "slug": "kind-robots",
  "title": "Kind Robots",
  "description": "Color the Kind Robots crew.",
  "cover": "/images/coloring-book/kind-robots/cover.webp",
  "rating": "all-ages",
  "pages": [
    { "id": "kind-robots-p01", "title": "AMI Among the Butterflies",
      "thumb": ".../p01/thumb.webp", "file": "pages/kind-robots-p01.json" }
  ],
  "attribution": [
    { "pageId": "kind-robots-p01", "source": "kind_robots asset public/images/bots/ami.webp",
      "note": "Kontext line-art conversion; prompt/model in page metadata" }
  ],
  "access": { "tier": "free" }   // or { "tier": "purchase", "sku": "..." } — economy detail
                                 // deferred to t-008; field reserved so manifests don't churn
}
```

---

## 4. Migration steps (ordered, small, reversible — `/mural` never breaks)

Each step is one small kind_robots PR, independently revertable, with `/mural`
functional at every merge point. Steps 1–5 are the extraction; 6–8 are cleanups and
capabilities; 9–10 belong to other tasks but are sequenced here for clarity.

1. **Extract shared types + storage helpers.** New `stores/helpers/coloring.ts` with
   `ColoringColor`/`ColoringRegion`/`ColoringPageDefinition`, the per-page storage
   key scheme, and the safeRead/safeWrite/normalize/makeId helpers lifted from
   `muralStore.ts`. `muralStore` imports them; zero behavior change.
2. **Add `stores/coloringStore.ts`.** Page-keyed state and generic actions per section
   2.3 (including undo, editColor, swapColors, assignment import/export). Nothing
   mounts it yet; pure addition.
3. **Add `components/coloring/coloring-canvas.vue`.** Controlled SVG-mode renderer per
   section 2.2. Not referenced by any page yet; pure addition.
4. **Move mural geometry to data.** Author `public/data/mural-design/mural-page.json`
   from today's `defaultSections`/`defaultColors` (the mural becomes page id
   `mural/fence-v1`, with its decorative stroke path as `layers.decor`). `muralStore`
   loads it with the inline constants kept as fallback. Behavior identical; revert =
   delete the JSON.
5. **Swap the canvas.** `mural-manager.vue` replaces its inline `<svg>` with
   `<ColoringCanvas>` driven by `coloringStore`, keeping its sidebars/chrome intact.
   Includes the one-time `kindRobotsMuralState` → `kindRobots:coloring:mural/fence-v1`
   migration shim (old key left in place). This is the only step with user-visible
   risk; the shim makes rollback safe.
6. **Shrink `muralStore` to a wrapper.** Delete the now-duplicated paint/palette logic;
   what remains is mural-specific: locked-environment handling, PPG fields, paint-spec
   export defaults. (Alternatively retire it entirely and let `mural-manager.vue` use
   `coloringStore` directly — decide by wrapper size at that point.)
7. **Canonical registration cleanup** (already flagged in mural t-007): promote mural
   into `dashboardConfigs.wonder.tabs` in `stores/helpers/dashboardHelper.ts` and
   delete the temporary `muralTab` bridge in `stores/helpers/labCards.ts`.
8. **Add export-to-image** (section 2.5) to `coloringStore`/`ColoringCanvas`. Serves
   both mural (share the paint plan) and coloring-book (save your art).
9. **Raster-flood mode** — only if t-004 selects it: additive `mode: 'raster-flood'`
   branch in `ColoringCanvas` + `fillOps` persistence in the store. SVG mode untouched.
10. **Coloring-book surface (t-005)** consumes the engine: set manifests + page
    packages under `public/data/coloring-book/`, library view, and an art-channel tab
    registered in the canonical `dashboardConfigs.art.tabs` registry (no bridges,
    per the t-005 note). Real mural fence assets (mural t-002) later replace the
    hand-authored `mural-page.json` regions without any engine change — that is the
    point of step 4.

### Open decisions routed elsewhere

- **SVG regions vs raster flood fill for coloring-book v1** → t-004
  (docs/generation-pipeline.md). Both shapes are specced above; the engine contract is
  identical either way except fill persistence (`fills` vs `fillOps`).
- **Palette hex finalization (PPG swatches) for mural** → mural-design t-004.
- **Set access/economy fields** → coloring-book t-008 (manifest reserves `access`).
