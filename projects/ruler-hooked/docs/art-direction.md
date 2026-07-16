# The Ruler is Hooked — Art Direction & Landscape Prompt Pack

date: 2026-07-16
task: ruler-hooked/t-008
status: spec complete — PROMPTS ONLY, no art generated (KR_API_TOKEN unset)
related: docs/compositing.md (t-005 — regions/states/time matrix these prompts fill),
docs/data-model.md (t-004 — content bundle asset paths),
docs/decks.md (t-006 — card & character art), DESIGN-BRIEF.md (art references)

> **No images were generated for this task.** `KR_API_TOKEN` is unset, and the
> brief routes asset generation through the normal conductor art pipeline
> (`art-prompts.yaml` / `ART-PROMPTS.md`), never committed agent binaries. This
> doc pins the *look* and ships the *first landscape-layer prompt pack* as text.
> The queued entries live in `projects/art-prompts.yaml`.

## 1. The look (the pin)

**Cartoony, goofy, warm.** Exaggerated good-and-evil archetypes with wry twists,
and characters who are nuanced underneath the archetype. It should read as a
storybook that knows it's funny. Reference points (from Silas):

- **Monkey Island** — comedic adventure staging, readable silhouettes, a wink in
  every scene.
- **Ralph Bakshi** — loose, characterful linework; unpolished-on-purpose energy;
  expressive crowds.
- **Treasure Planet** — painterly depth, warm cinematic lighting, "lived-in
  fantasy" texture.
- **Steven Universe** — soft rounded shape language, generous color, emotional
  legibility.
- **She-Ra: Princess of Power (2018)** — bold heroic-yet-goofy fantasy, clean
  color blocking, big feelings.
- **Prime Monster** (primary UI/structure ref) — pre-baked navigable screens that
  feel *alive without a steerable avatar*; honestly-evil decisions played straight.

The through-line: **charming, hand-illustrated, decision-weighty, never grimdark.**
Villainy is comically frank (a warlock land-developer with a genuinely good pitch),
virtue is a little smug — both are lovable.

## 2. Visual language (the rules that make layers stack cleanly)

Because the play screen is composited from independent region layers (t-005), the
art direction must guarantee layers *combine* into one coherent frame. These are
binding constraints on every generated layer:

- **Shape & line.** Rounded, confident storybook shapes; visible but soft linework
  (Bakshi looseness, Steven-Universe roundness). Avoid photoreal detail — it breaks
  the cartoon register and bloats file size.
- **Palette.** Warm, saturated, slightly-faded-storybook. A **nature-vs-development
  hue axis** carries the core theme visually: preserved land skews lush greens /
  golden warmth; developed land skews cooler greys, tin-roof browns, warlock-purple
  accents. Time-of-day shifts value/temperature, never the base palette identity.
- **Lighting is layer-consistent.** Every layer of a given `(time)` shares one key-
  light direction and color temperature (day = warm high key from screen-left;
  night = cool low key, moon from screen-right; golden = long warm rake; dawn =
  soft cool-to-warm with dew glow). This is what lets a `treeline-logged-night`
  layer sit convincingly in front of a `far_shore-industrial-night` layer.
- **Flat-ish depth, banded.** Each region occupies a horizontal depth band (sky →
  far shore → treeline → village → castle grounds → near bank → ruler). Layers are
  authored with **everything-but-their-band transparent** at full play-screen
  resolution (t-005 §5.1), so they register perfectly on one canvas.
- **Silhouette-first composition.** Each region must read at a glance by silhouette
  alone (Monkey-Island clarity) — a swap from `wild` to `logged` should be obvious
  in thumbnail.
- **No baked-in characters in environment layers.** Region layers are *scenery*;
  the ruler and card characters are their own layers/slides (t-006). Crowds/critters
  in environment layers are tiny, ambient, and non-interactive.
- **Always:** no readable text, logos, watermarks, contact sheets, or collages
  (matches the `art-prompts.yaml` prompt standard).

## 3. Character art direction (for deck cards)

Characters use the kind_robots **Character** model (t-006); their art follows the
same look with these notes:

- **Archetype-then-twist.** Read the archetype instantly (warlock = purple, horns-
  of-industry, blueprint; druid = leaf-cloaked, serene), then undercut it (the
  warlock is weirdly reasonable; the druid is a bit of a zealot).
- **Diverse, kind casting** per the art-prompts standard: vary gender, race, age,
  body size/shape, presentation, and species across the cast; mix humans, critters,
  and fantasy beings naturally, never tokenized.
- **The ruler** (player character, region `ruler` layer) is customizable and
  cosmetic-only (t-004 `ruler.cosmetics`): any gender/species, honorific King/Queen/
  other, happily oblivious, rod in hand. Portrait framing consistent across
  cosmetics so the layer swaps cleanly.
- Card art keys are referenced by the deck (`art: card-<id>`); character portraits
  by `Character.slug`.

## 4. The prompt-template scheme (region × state × time)

t-005 defines a variant matrix: every drawable `(region, state)` may provide per-
time variants, addressed as `asset(region, state, time)` and named
`{region}-{state}[-{time}].webp`. Hand-writing every cell doesn't scale, so prompts
are authored as **templates** with slot substitution. One template per `(region,
state)`; the `{time}` clause is composed from a shared time-of-day modifier table.

### 4.1 Template shape

```
PROMPT(region, state, time) =
  BASE[region][state]                        # the scene content & framing
  + ", " + TIME_MOD[time]                    # lighting/temperature/treat
  + ", " + STYLE_TAIL                         # shared house-style + layer rules
```

- **STYLE_TAIL** (appended to every layer prompt, constant):
  > cartoony storybook illustration, soft confident linework, rounded shapes,
  > warm saturated slightly-faded palette, Monkey Island / Bakshi / Treasure
  > Planet / Steven Universe / She-Ra energy, single horizontal depth band with
  > the rest of the frame fully transparent, full-scene registration, strong
  > readable silhouette, no readable text, no logos, no watermark, no collage

- **TIME_MOD** (shared, one row per time key; treats fall back to their settle per
  t-005 §4.2):

  | time    | modifier clause |
  |---------|-----------------|
  | `day`   | warm high-key daylight from screen-left, clear midday color, gentle ambient shadows |
  | `night` | cool low-key moonlight from screen-right, deep blue shadows, small warm window/lantern glows |
  | `dawn`  | soft cool-to-warm sunrise, low mist, glistening morning dew highlights (brief treat look) |
  | `golden`| long warm golden-hour rake light, amber rim-lighting, dust motes (brief treat look) |
  | `dusk`  | fading violet-orange sky, elongated cool shadows, first lanterns (brief treat look) |

- **BASE[region][state]** (the per-cell content): the scene description for that
  region in that state, framed to its depth band. Examples below (§5) are the
  authored BASE strings; the generator expands each across the `time` set it wants.

### 4.2 Why templates

- **Scales without hand-writing every combination** (the roadmap's requirement):
  `regions(~8) × states(~3–4) × times(~2–5)` cells come from a few dozen BASE
  strings + one TIME_MOD table + one STYLE_TAIL.
- **Consistency:** STYLE_TAIL guarantees every layer shares the house look and the
  transparency/registration rules; TIME_MOD guarantees lighting agreement across a
  `(time)` so layers composite (t-005 §2 lighting rule).
- **Coverage is optional per t-005 §4.2 fallback:** author `day`/`night` for every
  cell first; add `dawn`/`golden`/`dusk` treats only where the polish pays off.
  Missing cells degrade to the nearest settle, never a hole.

## 5. First landscape-layer prompt pack (BASE strings)

These are the first authored BASE strings for the highest-value cells — the ones
the PoC needs to prove live compositing (t-005 §6, the warlock/druid swap) across
day/night plus a couple of treats. The generator expands each over `{time}` using
§4. The corresponding queue entries are added to `projects/art-prompts.yaml` (§6).

**sky** (single-state; time-led)
- `BASE[sky][open]` = "wide empty storybook sky over a lakeside kingdom, soft
  clouds, distant birds, nothing but atmosphere in the top depth band"

**far_shore**
- `[pristine]` = "the far bank of a calm lake seen across the water: untouched
  wild shoreline, reeds, a heron, soft forest edge, mid-distance depth band"
- `[farmed]` = "the far bank as tidy patchwork farmland rolling to the waterline,
  little fences and haystacks, friendly and cultivated, mid-distance depth band"
- `[industrial]` = "the far bank crowded with goofy warlock-financed development:
  crooked smokestacks, tin roofs, purple-tinged smog puffs, comically over-built,
  mid-distance depth band"

**treeline**
- `[wild]` = "a lush overgrown forest band behind the lakeside foreground, tall
  tangled trees, dappled canopy, hidden critter eyes, thriving"
- `[tended]` = "a groomed woodland band, spaced healthy trees, a tidy path, a druid
  cairn, cared-for and calm"
- `[logged]` = "a thinned forest band with fresh stumps and stacked timber, a few
  survivor trees, wistful, mid-transformation"
- `[overbuilt]` = "the former forest band replaced by cheerful cramped cottages and
  scaffolding, one lonely ornamental tree, goofy sprawl"

**village_edge**
- `[hamlet]` = "a tiny cluster of thatched rooftops at the settlement fringe, smoke
  curls, a well, sleepy and small, lower-mid depth band"
- `[township]` = "a growing village edge: more rooftops, a market awning, a cart,
  busier and prosperous, lower-mid depth band"
- `[boomtown]` = "a bustling overgrown town edge crammed with mismatched buildings,
  cranes, banners, comically booming, lower-mid depth band"

**castle_grounds**
- `[humble]` = "modest royal grounds beside the lake: a small tidy castle, a
  vegetable garden, laundry line, cozy and unpretentious, foreground-mid band"
- `[flourishing]` = "well-kept royal grounds, blooming gardens, banners, a fountain,
  content and thriving, foreground-mid band"
- `[gaudy]` = "wildly over-decorated royal grounds, gold statues of the ruler
  fishing, too many fountains, endearingly tacky, foreground-mid band"

**lake** (time-led, choice-touchable)
- `[clear]` = "the sparkling near surface of the lake filling the lower frame,
  gentle ripples, reflections, jumping fish, foreground water band"

**fx** (additive overlays)
- `[fireflies]` = "a sparse drift of glowing fireflies as a transparent overlay,
  soft bokeh, nothing else in frame"
- `[dew-shimmer]` = "a subtle sparkle of morning-dew highlights as a transparent
  overlay, tiny glints, nothing else in frame"

## 6. Queue entries (art-prompts.yaml)

The first-pack layers are queued as `inspirations:` entries for `ruler-hooked` in
`projects/art-prompts.yaml`, targeting the kind_robots art-collection folder
(`public/images/artcollections/ruler-hooked/`) so they flow through the normal
distribute-images pipeline. Each entry is a fully-expanded prompt (BASE + TIME_MOD
+ STYLE_TAIL) at PoC layer resolution, `status: pending`. The already-queued
icon/card/hero project assets (2026-07-05) are untouched.

The first batch covers the warlock/druid swap the PoC must demonstrate:
`treeline` wild/logged (day+night), `far_shore` pristine/industrial (day), a
`sky` day/night pair, and one golden-hour treat — enough to composite two regions
with two states each into a live-responding screen (m2 exit criterion), with
day/night proving the time matrix.

## 7. Open questions for the art pass

- Final **play-screen resolution** and per-band crop rectangles (drives the exact
  export size for layer WebPs; icon/card/hero already sized).
- Whether the `ruler` layer ships a small pose set (idle/cast/reel) for subtle
  motion, or a single pose for the PoC (recommend single pose first).
- How many treat variants to author beyond the first golden-hour sample — gate on
  whether the day/night base reads well composited first.

None block generation: the templates (§4) + first pack (§5) are enough to start the
pipeline whenever `KR_API_TOKEN` is available and Silas green-lights a batch.
