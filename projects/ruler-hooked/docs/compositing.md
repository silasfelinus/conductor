# The Ruler is Hooked — Environment-Layer Compositing Spec

date: 2026-07-16
task: ruler-hooked/t-005
status: spec complete (no code; design doc only)
related: docs/data-model.md (t-004 — region states live in the save state),
docs/art-direction.md (t-008 — how the layer prompts are written),
DESIGN-BRIEF.md (core loop, time pillar)

## 0. What this spec is

The play screen is **one image the player sees**, but it is assembled at runtime
from a stack of independent, swappable **region layers**. This doc names the
regions, the states each region can hold, how kingdom-health sliders map to those
states, how the layers merge into a single frame, and how the time-of-day cycle
multiplies the whole thing without ever gating content.

It is deliberately data-first (see t-004): the compositor reads a small
`SceneState` object and looks up image assets by a **deterministic naming
convention**. No art path is ever hard-coded in logic; adding a region, a state,
or a time variant is an asset-drop plus a data entry, never a code change. This
is what lets the same content survive the Unreal migration (t-009) — DOM/canvas
layer stacking is the only piece that gets re-implemented; the region/state/time
addressing scheme ports verbatim.

## 1. Regions (the layer stack)

The scene is a fixed set of **named regions**, painted back-to-front. Each region
is one horizontal band or zone of the composited landscape. The PoC ships this
set (exact art framing TBD with the art pass, but the names are the contract):

| z | region key   | what it is                                    | swappable? |
|---|--------------|-----------------------------------------------|------------|
| 0 | `sky`        | backdrop: sky, sun/moon, weather mood         | yes (time-led) |
| 1 | `far_shore`  | the opposite bank across the lake             | yes |
| 2 | `treeline`   | the forest band behind the near ground        | yes |
| 3 | `village_edge` | rooftops / development at the settlement fringe | yes |
| 4 | `castle_grounds` | the royal grounds and castle silhouette     | yes |
| 5 | `lake`       | the water surface (reflections, sparkle)      | yes (time-led) |
| 6 | `near_bank`  | the grassy foreground the ruler sits on       | rarely |
| 7 | `ruler`      | the player-character fishing (pose/cosmetics) | cosmetic only |
| 8 | `fx`         | transient overlays: dew sparkle, fireflies, birds | additive |

Rules:

- **z-order is fixed.** Regions never reorder; only their *state* and *time
  variant* change. A compositor bug can never put the lake in front of the ruler.
- Regions 0–6 are the **environment** — they respond to kingdom state. Region 7
  (`ruler`) responds only to cosmetic/customization choices, never to sliders.
  Region 8 (`fx`) is an **additive** layer group (0..n overlays), not a single
  swap.
- **Not every region has to be present** in a given theme/biome. A region with no
  asset for the current `(state, time)` resolves to a transparent no-op, so the
  set can grow (e.g. a future `harbor` region) without touching existing scenes.

## 2. Region states

Each swappable region declares a small closed set of **states** — the visually
distinct versions of that band. States are authored, not procedural. The PoC's
pitch example (warlock development vs. druid preservation) lives mostly in
`treeline`, `village_edge`, and `far_shore`:

```
treeline:       wild | tended | logged | overbuilt
far_shore:      pristine | farmed | industrial
village_edge:   hamlet | township | boomtown | ruins
castle_grounds: humble | flourishing | fortified | gaudy
lake:           clear | murky | teeming        # cosmetic-ish, but choice-touchable
sky:            (state is time-of-day only — see §4)
near_bank:      grassy | worn                   # very slow to change
```

- A region's states are an **ordered ramp** where it makes sense (e.g. `treeline:
  wild → tended → logged → overbuilt` runs the preservation↔development axis), so
  a slider can pick a state by thresholding. Where there is no natural order
  (branching cosmetic variants), states are a plain set chosen by explicit rule.
- States are **content data**, defined in a `regions.yaml`-style manifest
  (shipped inside the game bundle), not in code:

```yaml
# regions manifest (illustrative)
regions:
  treeline:
    z: 2
    driver: { slider: nature, ramp: [wild, tended, logged, overbuilt] }
    states: [wild, tended, logged, overbuilt]
  village_edge:
    z: 3
    driver: { slider: development, ramp: [hamlet, township, boomtown] }
    states: [hamlet, township, boomtown, ruins]   # 'ruins' set by event effect, not the ramp
```

## 3. Sliders → states (the mapping)

Kingdom health is a set of continuous **sliders** (the axes are fully specified in
t-004's data model; this doc only needs their names and 0–100 range). Each
ramp-driven region names one **driver slider** and an **ordered ramp**; the
current slider value selects a state by even thresholding across the ramp:

```
state_index = clamp(floor(slider_value / (100 / ramp.length)), 0, ramp.length-1)
# nature=0..24 → wild, 25..49 → tended, 50..74 → logged, 75..100 → overbuilt
```

Refinements:

- **Hysteresis.** To stop a region flickering between two states when a slider
  sits on a threshold, transitions use a small dead-band (e.g. must cross
  threshold ± 4 to flip). The last committed state is stored per region in the
  save (t-004), so a reload is visually stable.
- **Event overrides.** Some states are not on any ramp (`village_edge: ruins`,
  `castle_grounds: gaudy`). An event/choice effect can **pin** a region to a
  specific state for the rest of the run (or until another event releases it),
  independent of its slider. Pins are recorded in the save as
  `regionOverrides: { village_edge: "ruins" }` and take precedence over the ramp
  computation.
- **Multiple sliders, one region:** a region names exactly one driver for the
  ramp. If a second axis should influence it, model that as an event override or
  as a separate region layer, not as a two-axis lookup — keeps the mapping
  inspectable and the asset matrix bounded.

The compositor is therefore a pure function:

```
resolveScene(saveState) -> SceneState {
  for each region:
    state = regionOverrides[region] ?? rampState(region.driver.slider, region.ramp)
  time = cyclePosition(saveState.turnCount)     # see §4, turn-driven, never wall-clock
  return { regionStates, time, fx: activeFx(saveState) }
}
```

`SceneState` is deterministic from the save — no randomness in compositing, so the
same save always renders the same frame (important for save/load parity and for
the offline guarantee).

## 4. Time-of-day dimension

Per the design pillar (Silas, 2026-07-05): **time is a cosmetic cycle position
advanced by actions, never a clock, and nothing keys off it.** Compositing honors
this by treating time as *one more coordinate on the asset lookup*, orthogonal to
region state.

### 4.1 The cycle

```
cyclePosition = f(turnCount)   # a turn-driven index, 0..N around a loop
```

Settle states (long-lived): **`day`**, **`night`**.
Transitional "treat" states (short-lived, surprise-and-delight): **`dawn`**
(morning dew), **`golden`** (golden hour), optionally **`dusk`**. A treat shows
for a **short beat** (one or two turns / a brief animated blend) before settling
into the neighboring `day` or `night`. The cycle is purely presentational:

```
... day → golden → dusk → night → dawn → day ...
       (treat)         (settle)  (treat) (settle)
```

- **Hard rule: no content keys off `time`.** No event, choice, reward, or region
  *state* is ever gated, spawned, or expired by cycle position. If a future
  "golden-hour fish" idea appears, it must also be catchable outside golden hour
  (the treat is a *look*, not a *window*). Compositing enforces this by design:
  `time` only ever selects which **variant of an already-chosen state** to draw.
- The player can sit mid-decision for a month; on return the scene renders at
  whatever `cyclePosition` the save holds, unchanged.

### 4.2 The variant matrix

Every drawable `(region, state)` may provide per-time variants. The lookup is:

```
asset(region, state, time)
```

with **graceful fallback** so the matrix never has to be exhaustive:

```
1. exact:   {region}-{state}-{time}.webp        e.g. treeline-logged-night.webp
2. settle:  {region}-{state}-{day|night}.webp   (treat → its neighboring settle)
3. base:    {region}-{state}.webp               (time-agnostic art)
```

So a region can ship only `day`/`night` and still participate in the cycle (treats
fall back to the nearest settle); a fully-authored region adds `dawn`/`golden`
variants for extra polish. This keeps `region × state × time` **generatable but
optional** — the art pass (t-008) writes prompts as `region + state + time`
templates, and any missing cell degrades to a coarser look instead of a hole.

### 4.3 Asset naming convention (the contract)

```
{region}-{state}[-{time}][@2x].webp
  region  ∈ region keys (§1)
  state   ∈ that region's states (§2)   (omit for single-state regions)
  time    ∈ day | night | dawn | golden | dusk   (omit for time-agnostic art)
  @2x     optional hi-dpi variant
```

Examples: `sky-night.webp`, `treeline-wild-dawn.webp`,
`village_edge-boomtown-day.webp`, `castle_grounds-gaudy.webp` (time-agnostic),
`fx-fireflies-night.webp`. FX overlays use the same scheme with the `fx-` prefix
and are composited additively on top.

## 5. The merge (how layers become one frame)

### 5.1 PoC (web) technique

- **Stacked transparent layers.** Each resolved `asset(region, state, time)` is a
  transparent-background WebP/PNG drawn in z-order into a single canvas (or
  absolutely-positioned `<img>`/`<div>` stack). Foreground regions (`near_bank`,
  `ruler`) carry their own alpha so the lake and sky read behind them.
- **Full-frame layers, not tiles.** Every region art is authored at the full
  play-screen resolution with everything-but-its-band transparent. This trades a
  little file size for zero registration math — layers always line up because
  they share one canvas. (A future atlas/tiling optimization is a build-time
  concern, invisible to the content.)
- **Crossfade on change.** When a region's resolved `(state,time)` changes, the
  compositor crossfades old→new over ~300–500 ms rather than hard-cutting, so a
  choice's effect *reads* as the world shifting. Crossfade is per-region, so only
  the changed band animates.
- **Optional subtle motion.** `fx` overlays and a few region variants may be
  lightweight looping animations (sprite-sheet or CSS): lake sparkle, treeline
  sway, firefly drift, dawn-dew shimmer. These are cosmetic and skippable
  (respect `prefers-reduced-motion`); the game is fully legible as stills.

### 5.2 Layer compositing order (pseudocode)

```
frame = blankCanvas()
for region in regionsByZAscending:        # sky first … fx last
    state = scene.regionStates[region] or single-state
    src   = resolveAsset(region, state, scene.time)   # §4.2 fallback
    if src: frame.draw(src, crossfadeIfChanged(region))
for overlay in scene.fx:                   # additive, on top
    frame.draw(resolveAsset("fx", overlay, scene.time), blend=screen/normal)
present(frame)
```

### 5.3 Determinism & performance

- Preload the **current** `(state,time)` per region plus the **adjacent time
  variant** (the next cycle step) so transitions never pop. Adjacent *states* are
  loaded lazily on choice, behind the card-resolution beat (there's always a slide
  transition to hide the fetch).
- The full working set is small: `regions (≈8) × states (≈3–4) × times (≈2–4)`
  full-frame WebPs, streamed from the offline bundle. No region needs more than
  its own state ramp resident at once.

## 6. Worked example — the warlock/druid choice

The pitch's signature decision, expressed entirely through this system:

1. Card resolves: player picks **"Let the warlock develop the north woods."**
2. Choice effect (t-006 deck data): `nature -= 20`, `development += 15`,
   plus an explicit override `far_shore: industrial` (a non-ramp state pinned by
   the event).
3. Next `resolveScene`:
   - `treeline` ramp on `nature` drops `wild → tended` (or `→ logged` if it
     crossed the next threshold): the forest visibly thins.
   - `village_edge` ramp on `development` rises `hamlet → township`: rooftops
     multiply at the settlement fringe.
   - `far_shore` is **pinned** to `industrial` by the override: smokestacks on the
     opposite bank, regardless of any slider.
4. Compositor crossfades exactly those three bands (sky/lake/ruler untouched),
   over the current `time` variant. Choose the druids instead and the same three
   bands ramp the other way (`treeline → tended/wild`, `far_shore → pristine`),
   with a different override for the preservation set.

Two regions, multiple visible states each, one merged screen that responds to
choices and re-renders identically on reload — this is exactly the m2 exit
criterion for the environment layer.

## 7. Open questions for the build (t-007)

- Final region **framing/parallax**: do bands get slight parallax on pointer move,
  or stay flat? (Flat is safer for the PoC; parallax is a polish-pass add.)
- Whether `lake`/`sky` motion ships in the PoC or waits — stills are the bar.
- Exact **ramp thresholds** per region once the slider axes are playtested (the
  even-thresholding in §3 is a starting default, tunable in `regions.yaml`).
- FX inventory for the PoC (dew shimmer + fireflies is plenty to prove the layer).

None of these block t-004/t-006; they are build-time tuning, not format changes.
