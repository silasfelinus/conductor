# Zuzu: Ghost Trail — Ten-Hour Campaign North Star

**Direction:** Silas, 2026-10-10 PT: keep developing the current graphical/gameplay upgrade; the hour-long adventure is the first layer of an eventual **ten-hour game**.

**Status:** Forward-looking design target. Only the current four-trail prototype is playable today. The six-stage Act I and later books below are not implemented and must never be reported as shipped.

## Development ladder

| Layer | What exists when the layer is *actually* finished | Time target |
| --- | --- | --- |
| Current prototype | Four short trails, core controls, gear, enemies and bosses; now being extended with persistent per-run secrets and a finite preview ending | No claimed duration |
| **Act I — The Bell Road** | Six distinct authored stages, first coherent conclusion with the Abbess, secret routes, unique bosses, cinematic art, resume/checkpoints and a clear credits/result screen | 75–100 minutes for an unfamiliar successful clear |
| **Five-book campaign** | Approximately 28–30 substantial authored stages over five books; systemic progression, relationships, world changes, optional routes and meaningful branching endings | Approximately **10 hours of authored main-path gameplay**, before replay hunting |
| Replay depth | Hard/New Game+ and alternate outcomes change encounters and player choices, not just enemy HP or item colors | Optional, *not* counted toward the ten hours |

**Do not inflate playtime through** waiting, lockout timers, repetitive enemy waves, forced grinding, invisible checkpoints, identical recolored rooms or excessive boss health. The ten-hour bar is supported by encounter variety, authored spaces, player decisions and exploration. An expert should be able to speedrun much faster.

## Five books: production outline, not fixed plot canon

| Book | Est. stages | Target main-path time | Theme and signature progression |
| --- | ---: | ---: | --- |
| I. The Bell Road | 6 | 90 min | Ghost Town, Bone Yard, Drowned Watering Hole, Storm Crow Pass, Bell Tower, abbey undercrypt. An encounter with the Abbess provides an ending for this *book* but not necessarily the world. |
| II. The Fractured Border | 5–6 | 120 min | Pursuit beyond the familiar weird west, negotiable faction relationships, Coyote Vagrant and fennec sibling threads, frontier trails that diverge and rejoin. |
| III. The Vanished World | 5–6 | 125 min | Hazy remnants of former humanity, environmental mysteries and vertical ruins; carefully distinguish clues from authoritative answers about what went wrong. |
| IV. Lands That Move | 5–6 | 125 min | Geography shifts in response to recorded player choices. Routes and encounter configurations transform while earned progress and rescue choices remain persistent. |
| V. Across the Last Gate | 6 | 140 min | Revisit saved consequences, assemble allies and relics, multiple authored late-game confrontations and a final branching resolution that pays off the campaign's mysteries without claiming all questions are answered. |
| **Total** | **27–30** | **~600 min** | Main successful playthrough with authored combat/traversal/cinematic beats; timed unfamiliar-player evidence required. |

Books II–V are candidate narrative trajectories; the Zuzu world registry and later owner direction determine actual canon. The Abbess's long-running stolen-children ritual and cosmic horror are in-scope fictional spoilers and remain Book I material. Do not manufacture a second world-ending villain solely to lengthen the game.

## Grow the engine without turning it into a 20,000-line monster

The current `utils/arcade/games/zuzuGhostTrail.ts` is already an oversized single module. New content belongs in **data manifests and focused systems**, not another thousand-line `switch`:

1. **Campaign catalog**: `bookId`, `stageId`, order, authored acts/rooms, level-art manifest, geometry, enemy/secret placement, boss, exits and optional routes. Each unique stage/route has a stable ID. Reading the manifest alone should show whether a route is implemented or planned.
2. **Encounter reducer**: deterministic seeded triggers, finite spawn budgets, encounter outcomes, one-time rewards and enemy states; no recurring spawn while standing still. Boss behavior is separately testable (telegraph/attack/recovery), then configured per stage.
3. **Run state / checkpoint adapter**: seeded run ID, book/stage/act IDs, character kit, relic/secret IDs, allies/choices, resolved encounter IDs, stage time/deaths, boss clears and completed chapters. Persisted versions require migration-friendly parsing and sane behavior when content is added in an update.
4. **Presentation**: independent layer assets (sky/parallax, collision tiles/props, animated sprite atlases, VFX, HUD); Pixel/HD share gameplay geometry. ArtJobs supply references, but do not assume a background illustration supplies collision. All media URLs are verified before being enabled; retain a procedural fallback.
5. **Narrative**: book introductions, ending interludes, stage context and authored decisions use pre-generated text, audio and art. No LLM calls during live play.
6. **Progression**: unlockables must broaden meaningful strategy (tools, shortcuts, viable play styles); a replay may offer a different path but cannot award the same secret twice by suicide/checkpoint reload. Gate story chapters by actual progression, not XP grinding.
7. **Metrics**: deterministic bot/seed probes detect softlocks, illegal checkpoints, hidden-score farms and unreachable secrets. Manual sessions record elapsed time, checkpoints, death count, routes and endings. The first successful clear and skilled replay durations are tracked separately.

## Near-term implementation ownership

- `kr-arcade/t-013`: inspect delivered concept/backplate ArtJobs, produce correctly pivoted, game-ready Zuzu and enemy atlases.
- `kr-arcade/t-014`: make the Ghost Town look and move like the accepted mockup, with working collisions.
- `kr-arcade/t-015`: begin the versionable campaign state system; as an immediate playable first slice, one-time traversal secrets and a **finite preview ending** replace an endless four-stage loop. That ending is **not** the six-stage Act I finish.
- `kr-arcade/t-016` through `t-020`: finish and time-test the six-stage Act I.
- **After Act I acceptance**: add the new book manifests and dedicated, reviewable tasks for the 10-hour expansion, preferably one authored stage or linked pair per PR. Do not falsely mark Act I complete because a future outline exists.

**Acceptance rule:** report *observed duration*, not an authored time estimate. Each stage must justify its runtime with unique traversal, encounter design, secrets, boss pattern, and narrative consequences. No generated art or planned runtime counts as playable content.
