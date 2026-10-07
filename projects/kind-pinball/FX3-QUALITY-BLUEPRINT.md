# Kind Pinball — FX3-Class Quality Blueprint

Date: 2026-10-07  
Task: kind-pinball/t-017  
Status: implementation blueprint

## Decision

**Kind Pinball needs an engine-class upgrade, not another coat of paint.**

The current game is a good rules prototype trapped inside the wrong rendering contract for the requested quality bar. `utils/arcade/games/kindPinball.ts` is a fixed 288×416 Canvas 2D game built from gradients, strokes, circles and rectangles. `arcade-cabinet.vue` obtains a 2D context directly and every arcade game implements `render(CanvasRenderingContext2D)`. The shared sound layer is deliberately chiptune-oriented. That architecture is excellent for the rest of the retro arcade. It is also the reason Kind Pinball reads as Atari rather than a modern simulated machine.

The target is **FX3-class presentation and Williams-class play**, using original Kind Robots themes and assets. We should keep the rules work, shot vocabulary, cabinet/leaderboard integration and the already-claimed t-003 layout/style prototype. We should stop treating the 2D renderer as the final renderer after that pass.

The proposed final stack is:

- **Three.js** for a real 3D playfield and camera.
- **Rapier 3D** for rigid-body physics, CCD, flippers, ramps and toys.
- **glTF** table/toy assets plus generated playfield art and texture maps.
- **PBR materials**, environment reflections, baked AO, emissive inserts and restrained bloom.
- **A 2D DMD texture** rendered into the physical backbox.
- **A pure rules state machine** driven by shot events, independent of geometry.
- **Spatial WebAudio** for mechanical sounds, callouts and mode music.
- Lazy loading so the 3D stack is paid only when Kind Pinball opens.

This is not “make the current canvas fancier.” It is “keep the game, replace the stage.”

## What the screenshots are telling us

The present screen is clean and playable, but nearly every visual cue is symbolic: a line means rail, a flat polygon means ramp, a circle means bumper, a gradient means playfield. The reference screenshot communicates the opposite: physical depth, stacked mechanisms, material response, toys, shadows, wires, plastic, metal, decals and lighting all explain the table before the player reads a word.

The gap is therefore structural:

| Current Kind Pinball | FX3-class target |
|---|---|
| 288×416 logical canvas | full-resolution responsive WebGL stage |
| orthographic flat diagram | perspective view of a dimensional table |
| strokes for walls/rails | chrome rails, posts, plastics and wireforms with thickness |
| ramp as a drawn path | elevated geometry with entry, travel, exit and occlusion |
| color changes = lighting | emissive inserts + local flashers + GI + bloom |
| flat ball | reflective steel sphere with contact shadow and light response |
| generic shapes | modeled toys, targets, posts, switches and hardware |
| oscillator bleeps | mechanical samples/synthesis layers + spatial mix + music |
| rule HUD painted over table | physical DMD/backbox plus minimal play HUD |
| fixed framing | camera presets and subtle tracking by play state |
| 2D collision math | rigid-body world with continuous collision detection |

## Quality pillars

### 1. Physical presence

The table must look built, not diagrammed. Every major object needs height, thickness and a material. A ramp casts a shadow. A ball passes under a wireform. Plastics overlap posts. The upper playfield is visibly above the main field. The playfield has clearcoat and receives reflections.

### 2. Ball feel

The ball should feel heavy and dangerous. Required behaviors:

- cradle on a held flipper;
- live catch;
- post pass;
- controlled tap vs full-power flip;
- realistic sling/pop impulses;
- spinner acceleration and decay;
- drop targets with physical reset motion;
- kickback and ball save;
- nudge with two warnings and a real tilt lockout;
- no tunnelling through posts, walls or flippers at maximum speed.

Physics must be deterministic enough for repeatable tests, even if the renderer runs at a different frame rate.

### 3. Shot readability

A player should know what to shoot from light and geometry alone. Every major shot gets a named insert and a unique physical mouth:

1. left orbit;
2. left ramp;
3. upper-playfield feed;
4. lock/scoop;
5. center bank / spinner lane;
6. right ramp;
7. right orbit;
8. side award scoop or stand-up bank.

Rules light shots. Art decorates them. Art must never bury them.

### 4. Light choreography

The table needs two lighting systems working together:

- **GI**: low, warm/cool general illumination that gives the machine its default mood;
- **show lights**: inserts, flashers, domes and toy lights that animate with rules.

Big events should visibly change the room: multiball drops GI and fires flashers, jackpot chases the rails, wizard mode raises the whole table into a new palette. The bloom pass should make bright things feel bright without turning the screen into neon soup.

### 5. Mechanical spectacle

Table 1 needs at least three memorable toys, not just targets:

- a village hut bank that lights one building at a time;
- a net-delivery plane or drone moving on a rail/wireform;
- an AMI robot head / beacon at the lock scoop;
- optional upper-playfield gate or bridge as the fourth signature element.

Each toy must affect either a shot, a rule, or a mode. Decorative motion alone is garnish.

### 6. DMD and audio drama

The DMD is part of the machine, not a debug HUD. It lives in the backbox as a 128×32 amber dot texture, with a scene queue for skill shot, lock, multiball, jackpot, mode start/end, bonus, tilt, extra ball, wizard mode and match.

Audio should layer:

- cabinet mechanics: flipper clack, solenoid, sling, pop, drop, spinner, lock, drain;
- ball material: wood/clearcoat roll, metal rail, plastic ramp;
- localized toy sounds;
- short original callouts;
- loopable mode music stems and multiball escalation.

### 7. Camera that serves pinball

Default camera: a high three-quarter cabinet view, roughly 28–34° vertical FOV, with enough perspective to show ramp height but not so much that shots distort.

Camera motion is restrained:

- small dolly/zoom on plunge;
- gentle focus shift when the ball enters the upper playfield;
- wider framing for multiball;
- a two-second celebration move only after the ball is safely held/drained or in a non-interactive award moment.

No cinematic camera should ever make a live shot harder.

## Technical architecture

### Keep the Arcade shell, add a specialized renderer lane

Do not turn the whole Arcade into Three.js. Existing games are intentionally lightweight Canvas 2D.

Add a render-mode discriminator to game metadata/module contracts:

```ts
type ArcadeRenderMode = 'canvas2d' | 'webgl'
```

The cabinet owns **two layered canvases**:

1. `stageCanvas`: WebGL-only, hidden for ordinary games;
2. `uiCanvas`: existing 2D arcade UI, attract screens, pause overlays, initials and ordinary games.

This avoids the browser rule that a canvas which has acquired a 2D context cannot later become a WebGL canvas. Kind Pinball mounts Three.js onto `stageCanvas`; the current arcade lifecycle and score flow continue on `uiCanvas`.

A WebGL game instance adds only the lifecycle it needs:

```ts
interface ArcadeWebGLGameInstance {
  readonly score: number
  readonly level: number
  readonly lives: number
  readonly over: boolean
  mount(canvas: HTMLCanvasElement): void
  resize(width: number, height: number, dpr: number): void
  update(input: InputFrame): void
  render(): void
  dispose(): void
}
```

The existing Canvas game interface remains valid and unchanged for every other cabinet.

### Proposed module tree

```text
utils/arcade/pinball/
  runtime.ts
  types.ts
  tableDef.ts
  physics/
    world.ts
    ball.ts
    flipper.ts
    mechanisms.ts
    sensors.ts
  render/
    scene.ts
    camera.ts
    materials.ts
    lights.ts
    post.ts
    assets.ts
  rules/
    engine.ts
    events.ts
    scoring.ts
  dmd/
    display.ts
    scenes.ts
    font.ts
  audio/
    mixer.ts
    mechanical.ts
    music.ts
  tables/
    ami-village/
      table.ts
      rules.ts
      assets.ts
      shots.ts
```

`kindPinball.ts` becomes a thin Arcade adapter that creates the AMI Village table runtime.

## Physics specification

Use real-world-ish units so tuning is intelligible:

- playfield approximately 0.56 m wide × 1.07 m long;
- standard ball diameter approximately 0.027 m;
- playfield pitch 6.5° default, configurable per table;
- fixed physics step: **1/120 s**;
- ball rigid body: dynamic, CCD on, continuous rotation;
- ramps and rails: static trimesh/compound colliders;
- flippers: kinematic/servo-driven rigid bodies around fixed pivots;
- toys/drop targets: constrained dynamic or kinematic bodies only where motion matters.

The Arcade loop can stay at 60 Hz. Each `update()` executes two 1/120 s physics steps. Rendering remains once per `requestAnimationFrame`. If 120 Hz proves insufficient for maximum ball speed, increase only the physics substep count, not the game-state clock.

Physics and scoring are separate. Invisible sensor volumes emit semantic events such as `shot:left-ramp`, `orbit:right`, `scoop:lock`, `spinner:tick`. Rules listen to those events. Geometry can be retuned without rewriting the rules machine.

### Physics acceptance tests

- 500 maximum-speed shots at a standard post: zero tunnelling.
- cradle test: a slowly descending ball settles on a held flipper for five seconds.
- post-pass test: reproducible transfer between flippers within a tolerance window.
- ramp test: entry velocity below threshold rejects; above threshold completes without clipping.
- multiball soak: ten simulated minutes with three balls, no permanent stuck state.
- tilt test: two warnings, third nudge disables flippers until drain.

## Rendering specification

### Materials

- playfield: clearcoat PBR, subtle normal map, baked AO;
- steel ball: metalness 1, low roughness, environment reflections;
- rails/posts: chrome or brushed steel variants;
- rubbers: matte, slightly soft normal response;
- plastics: translucent/clearcoat material with printed art on top;
- inserts: emissive mesh plus optional low-cost point light when actively flashing;
- wood/cabinet: textured rough material, not flat gradients.

### Lighting

- one primary overhead area/directional source;
- baked ambient/AO for static depth;
- environment map for metal response;
- pooled dynamic point/spot lights for flashers and major inserts;
- ACES tone mapping;
- subtle bloom;
- desktop can enable higher shadow quality; mobile uses baked/contact shadows and fewer dynamic casters.

### Art assets

Generated art is ideal for **textures and concepts**, not for faking depth in a single flattened image.

For each table:

- 2048×4096 playfield diffuse/albedo source, no baked text and no fake lighting;
- separate roughness/normal/AO maps where useful;
- glTF toys/mechanisms with UVs;
- decal/inserts atlas for text and symbols;
- DMD animation assets remain procedural or sprite-atlas based;
- KTX2/Basis compression for production textures when the pipeline is stable.

The first vertical slice may use primitive meshes for toys. Final acceptance does not.

## Table 1 visual direction: AMI Village Rescue

The table should feel like a hopeful night-flight machine, not a charity brochure.

Palette: deep indigo/navy base, warm village amber, cyan navigation lights, saturated magenta/yellow event accents. Chrome and clear plastics keep it grounded as a machine.

Visual hierarchy:

- backbox/DMD: amber, high contrast;
- top third: village skyline and upper playfield;
- middle: pop cluster around a glowing “map hub”;
- left/right ramps create a large visual loop around the field;
- lower third stays mechanically clean so the flippers and return lanes read instantly.

The “rainbow” motif becomes a physical light chase and lane accent, not six painted arcs across the whole field.

## Responsive plan

### Desktop / landscape tablet

Use almost the full cabinet screen. The table is centered at a perspective angle with a narrow backbox/DMD band above. Physical controls are keyboard/gamepad. No giant virtual D-pad.

### Portrait tablet / phone

The camera moves closer and becomes slightly more top-down. The playfield occupies the full width. Touch controls are **edge zones**, not arcade buttons floating beside the table:

- left bottom half = left flipper;
- right bottom half = right flipper;
- two-finger tap or short upward swipe = nudge;
- launch lane drag = plunger;
- small pause/mute affordances outside active shot areas.

Touch zones may flash on first launch, then become nearly invisible.

## Performance budget

Target the weakest device we actually support, not a desktop GPU demo.

- 60 FPS target on modern phone/tablet and desktop;
- 30 FPS is a temporary degraded mode, not the design target;
- DPR capped at 2;
- dynamic lights budgeted and pooled;
- no per-frame allocations in physics/render hot paths;
- lazy-load Three.js, Rapier and table assets only when entering the pinball cabinet;
- first table asset payload target: under ~8 MB compressed after the first engine chunk, with a lower-quality texture set for constrained devices if necessary;
- automatic quality tier based on measured frame time, never UA sniffing.

## Rules architecture

The rules engine is pure state. It receives semantic events and returns effects:

```ts
type PinballEvent =
  | { type: 'ball:launch' }
  | { type: 'shot'; shot: ShotId }
  | { type: 'target'; target: TargetId }
  | { type: 'spinner'; ticks: number }
  | { type: 'ball:drain' }
  | { type: 'timer'; id: TimerId }

type RuleEffect =
  | { type: 'score'; value: number }
  | { type: 'light'; id: string; state: LightState }
  | { type: 'dmd'; scene: string }
  | { type: 'audio'; cue: string }
  | { type: 'mechanism'; id: string; action: string }
  | { type: 'serve-ball'; count: number }
```

This is how Table 2 and Table 3 become new tables rather than copies of a 1,300-line class.

## DMD system

Render a logical 128×32 display into a tiny 2D canvas, then use it as a Three.js `CanvasTexture` on the backbox DMD mesh.

Required scene contract:

```ts
interface DmdScene {
  id: string
  priority: number
  durationMs: number
  render(ctx: DmdContext, elapsedMs: number): void
}
```

Gameplay-critical timers and score have priority over celebration scenes. A jackpot animation can interrupt a low-priority idle scene but not hide a mode countdown for five seconds.

## Asset and production workflow

1. **Blockout:** table geometry from primitive meshes, exact shot clearances, no polish.
2. **Physics lock:** tune flippers, slings, pops, ramps and outlanes until shots are satisfying.
3. **Art map:** export top-down UV/template from geometry; generate/paint playfield art to that template.
4. **Mechanism pass:** replace hero primitives with glTF toys and detailed rails/plastics.
5. **Material pass:** PBR maps, clearcoat, chrome, rubber, transparent plastics.
6. **Lighting pass:** GI mood, insert colors, flashers and lamp shows.
7. **Audio/DMD pass:** score feedback, callouts, mode music and DMD scenes.
8. **Polish:** particles, screen shake, ball trail only at high speed, camera transitions.
9. **Device pass:** phone/tablet/desktop screenshots and performance trace.

## Roadmap reset

The current t-003 remains useful and should finish: it gives the existing game an immediate visual jump and proves the expanded shot map. **After t-003, stop investing in the old 2D renderer as the final destination.**

Recommended sequence:

1. **3D shell + cabinet integration**: dual-canvas Arcade support, lazy Three.js/Rapier, empty table scene.
2. **Greybox vertical slice**: one ball, flippers, slings, pops, two ramps, two orbits, scoop; all physical and playable.
3. **Physics acceptance**: cradle/post-pass/CCD/tilt/soak tests.
4. **Hero material + lighting pass**: playfield texture, chrome, plastics, inserts, flashers, ball reflections.
5. **Rules + DMD + audio**: Table 1 reaches full feature depth.
6. **Signature toys + upper playfield**.
7. **Table 1 acceptance**: Silas plays it on desktop and touch.
8. **Only then** build Tables 2 and 3 on the proven engine.

Building three tables before Table 1 feels premium would multiply mediocre work. One great table is the engine specification.

## Acceptance bar

A build does not get called “FX3-class” because it contains 3D meshes. Table 1 is ready for Silas's verdict when all of these are true:

- perspective camera and visible vertical depth;
- reflective ball, dimensional rails, plastics, ramps and posts;
- at least two ramps, two orbits, a scoop, spinner, drop bank and upper-playfield feed;
- no tunnelling or common stuck-ball state in a ten-minute demo soak;
- cradle and post pass are intentionally possible;
- inserts clearly direct every timed mode;
- DMD has real scene transitions, score, timers and award animations;
- multiball has a distinct light show, music state and jackpot presentation;
- at least three table toys animate as mechanisms;
- 60 FPS target met at tablet and desktop test widths, with a viable mobile quality tier;
- touch play no longer depends on the giant generic arcade D-pad;
- screenshots look like a physical pinball machine at a glance, before any label is read.

That final line is the key. If the screenshot still needs an explanation to say “pinball machine,” the bridge is not crossed yet.
