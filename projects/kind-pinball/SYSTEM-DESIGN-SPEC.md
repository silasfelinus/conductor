# Kind Pinball — System Design Spec

Date: 2026-10-07  
Companion to: `FX3-QUALITY-BLUEPRINT.md`

## Purpose

This document converts the quality blueprint into implementation boundaries. It is deliberately specific enough that an implementation task can begin without re-deciding the architecture.

## Architectural rule

**Simulation, rules, rendering and presentation are separate layers.**

```text
Arcade input
    ↓
Pinball runtime ─────────────→ score/lives/over → Arcade shell
    ├─ physics world ────────→ contacts + sensor events
    ├─ rules machine ────────→ score/light/DMD/audio/mechanism effects
    ├─ mechanism controller ─→ flippers, gates, drops, toys
    ├─ DMD queue ────────────→ 128×32 texture
    ├─ audio mixer ──────────→ spatial mechanical + music + callouts
    └─ renderer ─────────────→ Three.js scene + camera + post FX
```

No layer reaches sideways into another layer's mutable internals.

## Arcade integration

### Metadata

Add an optional field, defaulting to current behavior:

```ts
export type ArcadeRenderMode = 'canvas2d' | 'webgl'

export type ArcadeGameMeta = {
  // existing fields...
  renderMode?: ArcadeRenderMode
}
```

`kind-pinball` sets `renderMode: 'webgl'`. Every existing game omits it.

### Cabinet DOM

Inside `.cabinet-screen`, stack:

```html
<canvas class="cabinet-stage" />
<canvas class="cabinet-canvas" />
```

`cabinet-stage` is visible only for a WebGL game during demo/play. `cabinet-canvas` stays above it and handles title/how-to/score/pause/initials UI. The WebGL context is never requested from the UI canvas.

### Instance types

Keep the current `ArcadeGameInstance`. Add a second explicit interface rather than weakening the current one with many optionals:

```ts
export interface ArcadeWebGLGameInstance {
  readonly renderMode: 'webgl'
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

export type ArcadePlayableInstance = ArcadeGameInstance | ArcadeWebGLGameInstance
```

`ArcadeGameModule.create()` returns `ArcadePlayableInstance`. Type guards keep all old call sites straightforward.

## Runtime lifecycle

```text
create
  ↓
mount(stage canvas)
  ↓
load table definition + assets
  ↓
create physics world
  ↓
create renderer scene
  ↓
serve initial ball
  ↓
fixed update @ 60 Arcade Hz
  ├─ input edge processing
  ├─ 2 × physics substep @ 120 Hz
  ├─ collect sensor events
  ├─ advance rules timers
  └─ apply rule effects
  ↓
render @ requestAnimationFrame
  ↓
dispose all GPU/audio/physics resources on cabinet exit
```

## Table definition

The engine should accept data plus small behavior hooks, not a god-class.

```ts
export type Vec3 = readonly [number, number, number]

export type MaterialId =
  | 'playfield'
  | 'chrome'
  | 'rubber'
  | 'plastic-clear'
  | 'plastic-printed'
  | 'wood'

export interface ShotDef {
  id: string
  kind: 'ramp' | 'orbit' | 'scoop' | 'lane' | 'target-bank' | 'spinner'
  sensor: string
  entryDirection?: Vec3
  insertIds: string[]
  displayName: string
}

export interface FlipperDef {
  id: string
  pivot: Vec3
  length: number
  side: 'left' | 'right'
  restAngle: number
  activeAngle: number
  strokeMs: number
  returnMs: number
}

export interface TableDef {
  id: string
  title: string
  physical: {
    widthM: number
    lengthM: number
    pitchDeg: number
    ballRadiusM: number
  }
  camera: CameraPreset[]
  meshes: MeshDef[]
  colliders: ColliderDef[]
  flippers: FlipperDef[]
  shots: ShotDef[]
  inserts: InsertDef[]
  mechanisms: MechanismDef[]
  audio: AudioBankDef
}
```

Table art, rule state and render implementation are separate imports so test code can instantiate rules without WebGL.

## Coordinate system

Use meters.

- X: left/right across playfield.
- Y: vertical height above local playfield.
- Z: down-table/up-table axis.
- origin: center of flipper line on the local playfield plane.

The table root is rotated by `pitchDeg` in world space. Visual and physics transforms share the same root transform.

## Physics world

Use Rapier 3D.

### Ball

- dynamic rigid body;
- sphere collider;
- CCD enabled;
- modest linear/angular damping;
- restitution/friction set per contacted material using interaction groups/hooks if needed;
- sleep disabled while ball is in live play;
- hard speed cap only as a safety fuse, not normal tuning.

### Flippers

A flipper is a rigid body constrained to one rotational axis. Drive it with a servo/motor toward rest/active angle. Input controls target angle, not teleportation.

The motor profile has a fast initial stroke and finite torque. This makes shots near the flipper base stronger without hand-coded “if ball here, add velocity” cheats.

### Slings and pops

Collision contact plus a sensor/switch determines when the mechanism fires. Apply a calibrated impulse from the mechanism center/normal, animate the rubber/cap, emit sound and light events.

### Ramps and rails

Visible ramp mesh and collision mesh may differ. Collision geometry should be simplified, closed, and free of tiny triangles. Use compound primitives where possible; use trimesh only for static complex shapes.

### Sensors

Every scoring shot has a dedicated sensor volume. A shot counts only when the ball crosses in the required direction and sequence. Do not infer a completed ramp from raw ball coordinates scattered through rule code.

## Simulation events

Physics emits low-level switch events:

```ts
type SwitchEvent =
  | { type: 'sensor-enter'; id: string; ballId: number }
  | { type: 'sensor-exit'; id: string; ballId: number }
  | { type: 'contact'; id: string; ballId: number; impulse: number }
```

A shot recognizer turns those into semantic events:

```ts
type ShotEvent = {
  shotId: string
  ballId: number
  speed: number
  comboEligible: boolean
}
```

Rules consume only semantic events.

## Rules state

Table 1's state should be serializable plain data:

```ts
interface AmiRulesState {
  score: number
  ball: number
  bonus: number
  bonusMultiplier: number
  villagesLit: number
  lockCount: number
  multiball: 'off' | 'ready' | 'running'
  mode: ModeState | null
  completedModes: string[]
  combo: ComboState | null
  extraBallLit: boolean
  kickbackLit: boolean
  tiltWarnings: number
  tilted: boolean
  wizardReady: boolean
}
```

A reducer-like step returns `{ state, effects }`. Unit tests can replay a sequence of shots and compare exact state/effects.

## Mechanism effects

Rules do not move meshes. They request mechanisms:

```ts
{ type: 'mechanism', id: 'lock-gate', action: 'open' }
{ type: 'mechanism', id: 'village-07', action: 'light' }
{ type: 'mechanism', id: 'net-plane', action: 'deliver', payload: { village: 7 } }
```

A mechanism controller coordinates physics body, animation, sound and light.

## Rendering

### Scene graph

```text
Scene
  TableRoot (pitched)
    PlayfieldMesh
    StaticHardware
    Ramps
    Plastics
    Inserts
    DynamicMechanisms
    Balls
  BackboxRoot
    DmdMesh
  Lights
  FX
```

### Renderer settings

- `WebGLRenderer` with antialiasing where performance allows;
- output color space sRGB;
- ACES filmic tone mapping;
- renderer pixel ratio controlled by quality manager, max 2;
- shadow map quality selected by tier;
- EffectComposer with restrained bloom; avoid a mandatory expensive SSAO pass on mobile.

### Quality tiers

`high`, `medium`, `low` are selected by measured frame time over a rolling window.

High:
- dynamic shadows from hero mechanisms;
- more active flasher lights;
- full texture resolution;
- bloom at full stage resolution.

Medium:
- only ball + major toy shadow casters;
- fewer dynamic lights;
- reduced bloom buffer.

Low:
- baked/contact shadows only;
- flashers become emissive-only where possible;
- half-resolution heavy post effect buffers;
- lower texture mip bias.

All tiers retain the same geometry, rules and physics.

## Camera system

Camera presets are named data:

```ts
type CameraPresetId =
  | 'main'
  | 'plunge'
  | 'upper-playfield'
  | 'multiball'
  | 'award'
```

Transitions are critically damped interpolation, not linear snap. The camera controller gets play state and ball centroid, but gameplay presets clamp movement so the flippers stay visible unless the ball is entirely in a dedicated upper playfield.

## DMD

A dedicated 128×32 logical canvas renders amber dots. Scale to a power-of-two texture internally if needed but preserve the dot grid.

The DMD queue supports:

- priority;
- preemption;
- resumable timers;
- minimum display time;
- interruptible idle scenes.

The 3D backbox uses the DMD canvas as an emissive texture. A subtle glass layer sits over it.

## Audio

Create a pinball-specific mixer, not more entries in the generic arcade beep preset.

Buses:

```text
master
  mechanical
  ball
  callout
  music
  ambience
```

Mechanical and ball sounds can use positional PannerNodes. Music/callouts stay centered. Each bus has gain control; the existing arcade mute controls master.

## Input

Desktop/gamepad:

- left/right: individual flippers;
- A: both flippers fallback;
- Down hold/release: plunger until dedicated analog/plunger input exists;
- Up: nudge;
- Start/P: pause.

Touch:

- left/right lower screen zones: flippers;
- drag in launch lane: analog plunger strength;
- short upward swipe outside launch lane: nudge;
- no persistent D-pad for pinball.

## Assets

Recommended production folder:

```text
public/images/arcade/pinball/ami-village/
  table.glb
  playfield.webp
  playfield-normal.webp
  playfield-roughness.webp
  decals.webp
  environment.webp
  audio/
    flipper-*.ogg
    pop-*.ogg
    rail-*.ogg
    callout-*.ogg
    music-*.ogg
```

Do not put generated text into playfield art. Table labels, inserts and DMD text should be crisp engine-rendered assets.

## Automated verification

### Engine tests

- deterministic rule reducer snapshots;
- shot recognizer direction/sequence tests;
- flipper motor and cradle regression tests;
- CCD post-collision stress test;
- ramp entry/exit tests;
- ball-save and multiball serve tests;
- tilt state transition tests.

### Visual contract

Capture fixed-seed screenshots for:

- attract/table idle;
- skill shot;
- mode active;
- multiball + jackpot;
- upper playfield;
- phone portrait;
- tablet landscape;
- desktop.

The screenshots are regression aids, not a substitute for human visual acceptance.

### Performance contract

A demo-pilot route should produce:

- average frame time;
- 95th percentile frame time;
- physics step overrun count;
- active balls;
- draw calls;
- triangles;
- texture memory estimate.

The soak fails on a stuck ball, NaN transform, physics overrun streak or unrecoverable camera state.

## Migration strategy

The old Canvas game remains playable until the 3D vertical slice passes its acceptance tests. Development can live behind a `kind-pinball-3d` module/feature switch initially. When the 3D version reaches feature parity on core shots and scoring, switch the registry loader; keep the old module for one release as a rollback path, then delete it in a separate cleanup task after verification.

This prevents a long rewrite branch and lets t-003 land without becoming throwaway work: its shot layout and rules feedback directly inform the 3D geometry.
