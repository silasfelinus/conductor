# The Ruler is Hooked — Unreal / Steam Migration Path (research note)

date: 2026-07-16
task: ruler-hooked/t-009
status: research note only — NO engine work, NO Steam page, NO deploy
related: docs/data-model.md (t-004), docs/compositing.md (t-005),
docs/decks.md (t-006), docs/art-direction.md (t-008), DESIGN-BRIEF.md

> **Scope guard.** This is a forward-looking note to keep the web PoC honest about
> the eventual Steam/Unreal target (a stated future goal in the brief). It is not a
> commitment to build in Unreal, and nothing here touches an engine, a Steamworks
> account, billing, or a store page — all of which remain hard human gates. The
> point is: **build the PoC so the content survives the port.** Written from
> engine/Steamworks domain knowledge; no external calls were made.

## 1. TL;DR

The PoC's **data-first content** (decks, regions, saves, characters, rewards)
ports to Unreal almost verbatim — it's engine-agnostic JSON/YAML by design (t-004
§0.2). What does **not** port is the **web rendering/compositing layer** (DOM/canvas
`<img>` stacks, IndexedDB, CSS crossfades) — that's re-implemented against Unreal's
UI and texture systems. Because the game is a **slideshow of composited still
layers with no real-time simulation, no clock, and seeded determinism**, it is an
unusually *cheap* thing to port: there is no physics, no networking, no frame-rate-
sensitive gameplay to re-tune. Effort is dominated by re-doing presentation, not
logic.

## 2. What ports cleanly (keep doing this)

| PoC asset | Why it ports | Unreal home |
|-----------|-------------|-------------|
| **Deck/card/arc YAML** (t-006) | Pure declarative data; no web APIs | Import as **DataTables** (CSV/JSON) or read raw JSON via `FJsonObjectConverter`; a card = a row struct |
| **regions.yaml** manifest (t-005) | Region/state/time addressing is just strings | DataTable of region defs; `asset(region,state,time)` → a texture-lookup by name |
| **RunSave document** (t-004) | Self-contained JSON, engine-neutral | Serialize to Unreal **SaveGame** (`USaveGame` + `UGameplayStatics::SaveGameToSlot`) *or* keep the exact JSON and store it as a string field — the format is identical |
| **Effects grammar** (t-006 §6) | Closed, additive, deterministic reducer | Port `applyEffects()` 1:1 as a Blueprint-callable C++ function or pure Blueprint |
| **Trigger predicates** (t-006 §3) | Small closed comparator set, no time | Port the evaluator 1:1; same predicate data |
| **Seeded selection** (t-006 §5) | Deterministic RNG from `seed` | Use `FRandomStream(seed)` — same seed → same draws; parity preserved |
| **Character / Reward data** | Mirrors kind_robots fields; plain data | DataTable rows; art by slug |
| **Kingdom sliders / counters** | Numbers in a struct | Struct fields on the save |
| **Art layers (WebP)** | Transparent full-frame images | Transcode to PNG/`.uasset` textures (build step); naming convention unchanged |

The whole **content bundle** (t-004 §6: `regions/`, `decks/`, `characters/`,
`rewards/`, `endings/`, `assets/`) becomes an Unreal **content directory + DataTables
+ a texture set**. The authoring workflow (t-006 §8, "add an arc = drop a YAML")
survives if the Unreal build ingests the same YAML/JSON at cook time. That is the
single most valuable thing to protect: **keep the content out of code in the PoC so
the port is an importer, not a rewrite.**

## 3. What does NOT port (re-implement in Unreal)

| Web PoC mechanism | Unreal replacement | Notes |
|-------------------|--------------------|-------|
| **DOM/canvas layer stack** (t-005 §5.1) | **UMG** `Image` widgets z-ordered in a `CanvasPanel`, **or** a single material with layered texture samples, **or** **Paper2D** sprite layers | UMG stack is the closest 1:1 to the CSS `<img>` stack and the simplest port; a layered material gives cheaper draw + shader crossfades |
| **CSS per-region crossfade** (t-005 §5.1) | UMG **animation** (opacity lerp) per widget, or a material `Lerp` on a blend param | Same 300–500 ms crossfade, driven by an animation timeline instead of CSS |
| **IndexedDB save store** (t-004 §2.1) | Unreal **SaveGame** slots on disk | Multiple named slots map directly to named SaveGame files; `SaveIndex` → a small index SaveGame |
| **Optional subtle motion** (sparkle, sway) | UMG material anims / Niagara for FX overlays | `fx` layer group (t-005 §1) → a few lightweight Niagara systems or animated materials |
| **Web fonts / HTML UI chrome** | UMG widgets + a font asset | Cards, sliders, slot picker rebuilt as UMG |
| **WebP decode** | Cook-time transcode to engine textures | One-time asset pipeline step |
| **Browser audio** | Unreal audio (`USoundBase`, MetaSounds) | Not in the PoC scope but noted for completeness |

None of these are *logic* — they are presentation and storage adapters. The game
*rules* live entirely in the ported data + reducer.

## 4. How the design pillars map to Unreal

- **Offline at runtime** (no live LLM) — already the shipping posture; Unreal is
  natively offline. The optional kind_robots account-sync (t-004 §2.1) would be an
  HTTP call from Unreal (`FHttpModule`) at the same non-gameplay-critical boundary,
  or dropped entirely for the Steam build. **No gameplay depends on it either way.**
- **No clock / turn-driven** (t-004 §0.3) — a gift for porting: no `Tick`-based
  timers to reconcile, no delta-time tuning. `turnCount` advances on input events
  (button presses), identical to the web loop. Time-of-day stays a cosmetic cycle
  index. This is why the port is cheap: **there is no real-time simulation to
  re-balance.**
- **Seeded determinism** (t-004 §0.5) — `FRandomStream(seed)` reproduces draws; the
  append-only `choiceLog` reconstructs a run. Save/load parity holds the same way it
  does on web.
- **Multiple named saves** — Unreal SaveGame slots are a direct fit.

## 5. Steam considerations (research level only)

Not for this milestone; captured so the PoC doesn't paint into a corner. All of
these are **hard gates** (Steamworks account, the $100/app Steam Direct fee,
billing, a store page, external publishing) — none are actionable now.

- **Steamworks SDK / Online Subsystem Steam** — Unreal ships `OnlineSubsystemSteam`;
  wiring it up is a plugin + config task, not architectural. The game needs almost
  nothing from it: no multiplayer, no matchmaking.
- **Achievements** — map cleanly from our endings + `LifeAchievement`-style unlocks
  (t-006 §7, t-004) to Steam achievements. This is the main Steam-specific content
  surface and it's small.
- **Steam Cloud** — could back the save slots for cross-device continuity (opt-in),
  layered over the local SaveGame files; not required.
- **No microtransactions / no live service** — the offline, single-player, no-LLM
  design means no Steam Inventory/economy integration and no server costs. Simplest
  possible Steam footprint.
- **Deck verification / controller support** — worth designing card UI for gamepad
  navigation early (Prime-Monster-style navigable screens already imply this), but
  it's a UMG input-mapping concern, not a data one.

## 6. Rough effort tiers

Relative sizing for the *eventual* port, assuming the PoC honored the data-first
rule. Not a schedule, not a commitment.

- **T1 — Content import (small).** Write a cook-time importer for the existing
  YAML/JSON → DataTables; transcode WebP layers → textures. Mostly mechanical
  because the schemas are already engine-neutral. *Risk: low.*
- **T2 — Reducer + selection port (small–medium).** Reimplement `applyEffects`,
  trigger evaluation, and seeded selection in C++/Blueprint from the specs
  (t-004/006). Deterministic and well-specified. *Risk: low — it's a spec-to-code
  transcription with golden-save parity tests.*
- **T3 — Presentation rebuild (medium).** UMG card/slide/slot UI + the region layer
  compositor (UMG stack or layered material) + crossfades + FX. This is the bulk of
  the work and the only genuinely new engineering. *Risk: medium — art integration
  and UI polish.*
- **T4 — Steam wrap (small, gated).** Online Subsystem Steam, achievements mapping,
  optional Steam Cloud, packaging. *Risk: low technically; gated on account/store/
  billing decisions that are Silas-only.*

The ordering that de-risks everything: **protect T1/T2 during the PoC** (keep
content as data, keep the reducer pure and deterministic) so that when/if the port
happens, only T3 is real new work.

## 7. Recommendations for the web PoC (t-007) to stay portable

1. **No game rule in a framework idiom.** Keep `applyEffects`, trigger evaluation,
   and selection as **pure, framework-free functions** (t-004 §8) so they transcribe
   to C++ without untangling Vue/React. No rules inside components.
2. **All content in `content/<version>/` data files** — never inline a card, region,
   or reward in code. The importer target is the payoff.
3. **Seeded RNG behind one interface** (`nextRandom(stream)`), so swapping to
   `FRandomStream` is a one-file change and parity is testable.
4. **Save = one serializable JSON document** (already the design) — don't scatter
   state across web storage keys; one blob → one SaveGame.
5. **Asset naming is the contract** (t-005 §4.3) — the compositor looks up by
   `{region}-{state}-{time}`; keep it string-addressed so Unreal can resolve the
   same names against textures.
6. **Keep a golden-save fixture** — a save + its expected rendered `SceneState` and
   choice outcomes — as the cross-engine parity test. If the Unreal port reproduces
   the golden saves, the logic port is correct.

## 8. Open questions (for whenever a port is actually greenlit)

- UMG widget stack vs. single layered material for the compositor (lean UMG for
  fidelity to the web stack; material for performance if layer count grows).
- Whether to keep runtime JSON parsing or bake DataTables at cook time (bake for
  ship builds; JSON for iteration).
- Unreal version + 2D toolchain choice (Paper2D vs. pure UMG) — deferred; the PoC
  imposes no constraint either way because it ships nothing but data + textures.

None of this blocks the web PoC; it only argues for discipline the specs already
call for (data-first, pure reducer, string-addressed assets, seeded determinism).
