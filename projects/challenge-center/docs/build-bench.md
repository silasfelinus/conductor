# Build Bench — image-generation A/B test bench

date: 2026-07-23
status: active

## What it is

A focused head-to-head **test bench** for image-generation *builds*, distinct from
the public voting arena (`/challenges`). Where the arena lets the community vote on
already-produced submissions, the Build Bench is a **builder's tool**: configure two
full builds, render both, eyeball them side by side, and pick the winner yourself.

- **A build** = a complete generation spec: engine + prompt + negative + steps + cfg
  + guidance + seed + width/height + sampler + scheduler + LoRA.
- **A matchup** = Build A vs Build B (exactly two), you pick the winner (manual).
- **Clone** = copy one side's entire build onto the other, so you can then change a
  single knob — the controlled-comparison move ("clone A→B, double B's steps", or
  "clone A→B, swap B's engine to Flux.2, same seed").

## Where it lives

- **Front-end (kind_robots):** `/build-bench` route + `components/art/build-bench.vue`
  + `stores/buildBenchStore.ts`, registered as an admin **Build Bench** tab in the
  art channel (`stores/helpers/dashboardHelper.ts`). Local-first: bench state and
  saved matchups persist to `localStorage`; rendered images are real ArtImages in
  the gallery.
- **No new backend.** It drives the existing `POST /api/art/enqueue` →
  `GET /api/art/queue/:id` → `GET /api/art/image/:id` pipeline. Bench jobs are
  enqueued at high `priority` so they jump the shared queue.

## Engines

Selectable per side, mapped to the enqueue dispatcher's engines:

| Bench label | enqueue `engine` | native cadence |
|---|---|---|
| Krea 2 Turbo | `krea2` | 8 steps, cfg 1, euler/simple |
| Flux.2 Klein | `flux2` | 4 steps, cfg 1, euler/simple |
| SDXL | `sdxl` → `comfy` | ~25 steps, cfg 6, euler/normal |
| Flux dev | `flux` | 30 steps, cfg 1, euler/beta |

`sdxl` is an enqueue alias for the default `comfy` SD/SDXL graph.

## CLI parity (conductor)

`scripts/challenge_matchup.py` can also drive the new engines for arena ART
challenges: `ART_GENERATORS` now maps `comfy-krea2→krea2`, `comfy-flux2→flux2` (plus
bare `krea2`/`flux2`/`sdxl`/`flux`), and the enqueue allow-list passes `loraName`,
`loraStrength`, and `jsonPrompt` (Flux.2's structured prompt).

## Not in v1

DB-backed matchup history / a "best build" leaderboard (kept local-first for now),
auto-judging via the vision curator, and >2 contestants. All are natural follow-ups
if the manual 2-up bench proves useful.
