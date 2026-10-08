# Kind Pinball 3D: device and performance pass

Measured 2026-10-08 for kind-pinball/t-010 in a cloud sandbox. The sandbox has no GPU: Chromium
draws through SwiftShader, a software renderer. That makes these numbers sound for what the CPU
does and for how much each tier draws, but not for real GPU frame times.

## The same game on every device

`runPinballDevices` (kind_robots `utils/scripts/verifyArcadeEngine.test.ts`) plays one seeded game
with the same scripted input for 30 seconds on four runtimes:
- a phone (390×844 at 2×, low tier);
- a tablet (820×1180, medium);
- a desktop (1440×900, high);
- one with no screen at all.

All four end on the same score, rules state and ball positions, to nine decimals. Physics steps
at a fixed 240 Hz whatever the screen, and the renderer only reads it, so screen size and quality
tier cannot change play. The test runs on every PR.

## CPU cost per game tick

One tick is 1/60 s of game: four physics steps, rules, toys and the DMD. Measured over 60 s of the
attract demo in Node:

| | Mean | p95 | p99 |
|---|---|---|---|
| Physics, rules and DMD only | 0.35 ms | 0.61 ms | 1.19 ms |
| With the scene updated (stub GL) | 0.48 ms | 0.87 ms | 2.20 ms |

The budget is 16.7 ms a frame, so the game logic uses under 3% of it on this machine. The first
tick takes 80 ms while it warms up; that cost is paid once.

## What each tier draws

From the real three.js renderer in Chromium. The scene is AMI Village with the generated
playfield art and the t-010 toys.

| Device | Tier | Draw calls | Triangles | Bloom | Shadow map | Trail | Sparks |
|---|---|---|---|---|---|---|---|
| Phone (390×844 @2×) | low | 124 | 17,368 | off | none (contact shadows) | off | 48 |
| Tablet (820×1180) | medium | 160 | 18,784 | ½ | 1024 | on | 120 |
| Desktop (1440×900) | high | 172 | 24,597 | full | 2048 | on | 240 |

The quality governor (`render/quality.ts`) picks the tier from measured frame time, never from the
user agent, and steps down when a device can't hold it.

## Still to measure on real hardware

GPU frame time on a real phone and tablet. SwiftShader takes about a second for each high-tier
frame, which says nothing about a real GPU. That measurement falls to Silas's play-test (t-016):
- desktop;
- one phone;
- one tablet.

The renderer's own stats show what it settled on: the tier, average and p95 frame time, draw calls
and triangles (`runtime.renderStats()`).

## Touch

The phone run above used the cabinet's touch layout (screenshots `t010-touch-phone-*.jpg`). There
is no d-pad over the table:
- flip from the lower corners;
- drag the lane strip down to pull the plunger;
- swipe up to nudge.

The hints fade after the first ball.
