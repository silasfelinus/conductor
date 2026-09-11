# Cthulhuquarium — Full Game Gap Audit

date: 2026-09-11
author: conductor scheduled Agent run, cthulhuquarium/t-068
basis: kind_robots `origin/main` @ `58ac058` (2026-09-11), the design brief
(`projects/cthulhuquarium/DESIGN-BRIEF.md`), a direct code read of
`server/utils/aquarium.ts`, `server/utils/aquariumEconomy.ts`,
`stores/cthulhuquariumTankStore.ts`, `components/cthulhuquarium/cthulhuquarium-game.vue`,
`prisma/schema.prisma`, every `server/api/aquarium/**` route, `utils/cthulhuquariumArt.ts`,
`utils/scripts/importCthulhuquariumArt.mjs`, and a live, unauthenticated
`curl https://kindrobots.org/play/aquarium` (production, this session).

## Why this exists

Silas audited Cthulhuquarium on 2026-09-11 and failed it: *"this is nothing like the
pitched experience except in the barest of bones,"* *"we need a much better design of
everything,"* *"there was no real style in the pics for our characters."* That happened
while the roadmap read 63/64 tasks done. This document is the honest accounting t-069
needs before anyone re-judges the game or marks the project finished: what the pitch
asked for, what actually exists in the shipped code, and what is genuinely missing —
credited and blamed in the right places, not inferred from a task-completion count.

Three fixes landed the same day as this audit and are folded in below rather than
treated as pending: **t-065** (deliver the 136 stranded art plates — landed as a
client-side fallback, see §3), **t-066** (stop rendering the project pitch as
player-facing page copy), **t-067** (fix the collapsed one-word-per-line sets row).

## 1. MVP scope, point by point

The brief's bar (verbatim): *"a fully working webpage where users can load and interact
with their aquariums."* Concretely, a signed-in player should be able to, at
`/play/aquarium`:

| # | Pitch point | Status | Evidence |
|---|---|---|---|
| 1 | See the tank, with fish swimming in it | **Shipped, but not with real art** | `cthulhuquarium-game.vue`'s canvas render loop (`render()`/`loop()`, ~1855-1990) is real and running, paused on a hidden tab. The fish themselves are still hand-drawn canvas primitives (`drawFish()`, 1664-1710) — the component's own header comment says so and remains true even after today's art delivery, because that delivery only reached the bestiary/catalog/reveal-dialog panels, not the swim view. |
| 2 | Click drifting collectibles for coins | **Deviated from the pitch, on purpose, documented in code** | `economy.yaml` has no click-for-coins income path; income is entirely server-tick-settled. A settled tick's `coinsEarned` spawns drifting motes as a *visual reveal* of coins already credited — clicking one dismisses it but earns nothing itself (component header comment, 9-16; `onCanvasPointerDown`, 2059-2096). Net coins are unaffected, but the literal mechanic in the pitch doesn't exist. |
| 3 | Spend coins on food; drop food; fish eat it; fish never die | **Shipped, in a simplified form** | Feeding is a button ("Feed hungriest" / per-fish), not drag-and-drop placement, but it does trigger a falling, wriggling food visual fish path toward (`onFeed`, 2123-2135; `FeedCreature`/`FOOD_FALL_SPEED`, ~1448-1450). Hunger only throttles income via `hungerMultiplier` bands — it never removes a fish. "Fish never die" is honored. |
| 4 | Upgrades: better food, faster drops, more tank slots | **Partially missing** | No food-tier or drop-speed system exists anywhere in `aquariumEconomy.ts` — one flat feed-cost formula, no choice. "More tank slots" is real, but only indirectly, via `SET_PIECE_CATALOG.extra_species_slot` and bestiary-count milestones (+2 slots at 5/10/15/20 species) — not a dedicated upgrade shop. |
| 5 | Buy/unlock a new species and watch it appear | **Shipped, fully wired** | Catalog panel → `tankStore.unlock()` → `purchaseSpeciesForUser` → one-shot reveal dialog with real art where available → tank list updates immediately. |
| 6 | Offline income, capped | **Shipped, fully wired** | `settleTick` floors (not rounds) coins, caps accrual at 8h (480×60s ticks), applies a flat 0.5x multiplier to every tick uniformly rather than a separate offline path (`aquariumEconomy.ts` 694-871). Loaded automatically on mount. |
| 7 | Browse other users' public tanks, read-only | **Shipped, fully wired** | `pages/play/aquarium/browse/index.vue` and `/browse/[username]/[slug].vue`, both explicitly read-only (no feed/click/write calls). |
| 8 | Persist server-side across devices | **Shipped, fully wired** | The store never touches `localStorage` for game state — every mutation is a `performFetch` to `/api/aquarium/*`; a prior localStorage prototype was deliberately removed. |

**Net: 5 of 8 MVP points are genuinely done end-to-end. Two (#2 collectibles, #4
upgrades) deviate from or fall short of the literal pitch, in ways the code documents
but the roadmap never surfaced as gaps. #1 (fish swimming with real art) is the one
that most explains Silas's "barest of bones" verdict** — the tank a player actually
watches is still primitive canvas shapes, independent of everything the art-delivery
work fixed elsewhere on the same page.

## 2. Species catalog

The bible (`silasfelinus/cthulhuquarium`, not checked out in this environment) is
seeded via `scripts/seed_bestiary.ts`, whose own comments assert 151 authored species
(`MIN_EXPECTED_SPECIES = 100` as a safety floor, "151 is the authored count"). This
audit could not run a live count against production (no `DATABASE_URL` in this
sandbox), so the 151 figure is taken from the seed script's own comments plus the
`05d227c` commit message quoted below, not a fresh query.

## 3. Art delivery (t-065) — what actually shipped, and what's still not real

**The root cause, in the delivery commit's own words** (`05d227c`, merged today):
*"Silas audited Cthulhuquarium on 2026-09-11 and failed it... verified live: 0 of 151
species had any art path."* Every `Monster` row in production carried `iconPath: null`
and `cardPath: null` — Silas was judging placeholder icons, not the art that had
actually been authored (138 Victorian-trade-card-style plates sitting unseen in the
conductor repo).

**What landed today:** `05d227c` copied 138 `.webp` plates into
`assets/images/cthulhuquarium/` as ordinary bundled Vite assets (119 fish, 7 sets, 6
eggs, 2 characters, 1 parlour background, 2 screens, 1 codex header). A new module,
`utils/cthulhuquariumArt.ts`, globs those bundled assets at build time and fills a
`Monster`'s `iconPath`/`cardPath`/`imagePath` **only when the database value is
null**, matching `cthulhuquarium-fish-<slug>` to the bundled filename. That fallback is
wired into the bestiary, catalog, and unlock/hatch/breed reveal-dialog `kr-art-plate`
calls in `cthulhuquarium-game.vue`.

**This audit independently verified the fix is live in production**, not just merged:
an unauthenticated `curl https://kindrobots.org/play/aquarium` today returned
`<link rel="prefetch">` tags for the fingerprinted, hashed asset URLs (e.g.
`/_nuxt/cthulhuquarium-fish-bailiff-eel.BRakQGdU.webp`,
`/_nuxt/cthulhuquarium-bg-parlour.QoRhD0Lx.webp`,
`/_nuxt/cthulhuquarium-char-charlotte-fishmonger.Bkwl_fIR.webp`,
`cthulhuquarium-egg-{common,uncommon,rare,epic,legendary,mythic}`,
`cthulhuquarium-screen-finale`, `cthulhuquarium-set-last-aquarium`), and a direct
fetch of one of those exact URLs returned `HTTP 200`, a real 17KB WebP file. That
confirms the code delivery has reached the production build, ahead of any Force
Update tracking normally required — **but it does not confirm what the tank canvas
itself looks like to a live visitor**, since `/play/aquarium` is a client-rendered
game and this route's SSR shell doesn't include the hydrated game state (see
AGENTS.md's own caveat on this class of check). That remaining visual confirmation is
exactly what t-065/t-069 already reserve for Silas.

**What did NOT land, despite the fix:**
- **`Monster.iconPath`/`cardPath`/`artImageId` in the actual database are still
  null.** The fallback is a client-side workaround, not a data fix — `cthulhuquarium-art.ts`'s
  own comment says as much: "If Monster rows ever gain genuine ArtImage records,
  `artFor*` yields to them automatically." Nobody has done that yet.
- **The in-tank swim view still shows no real art at all** (see §1.1) — the fallback
  only reaches bestiary/catalog/reveal panels.
- **32 of 151 species (mostly `-common` starters) have no plate at all** and fall
  through to a placeholder icon even with the fallback active.
- **`utils/scripts/importCthulhuquariumArt.mjs`, committed in a separate PR (#2622,
  `efb93e2`) the same day, is dead code relative to what actually shipped.** It writes
  to `assets/images/cthulhuquarium/generated/` — a directory that does not exist in
  the repo — while the real delivery landed flat in `assets/images/cthulhuquarium/`
  via a different commit. `utils/cthulhuquariumArt.ts`'s glob only reads the top-level
  directory, not `generated/**`, so running this script today would silently produce
  files the app never picks up.

## 4. Systems confirmed working correctly

- **Leaderboard** ranks by distinct species collected (`AquariumCodexEntry` group-by
  count), not coins — matches the design decision exactly
  (`server/utils/aquarium.ts:1939-1992`; excludes private tanks and restricted users).
- **Decor/tank layout editing (t-017)** is genuinely interactive: place from a catalog
  panel, then drag already-placed pieces to reposition, not just a static list.
- **Rare random events (t-016)** roll server-side once per real tick settle, log to
  `AquariumEvent`, and surface a dismissible client notice with the bonus folded into
  the payout — additive only, by explicit hard design constraint in the economy code.
- **The finale (t-039/t-054)**: the terminal 250,000-coin purchase triggers a
  permanent cosmetic re-render of the existing tank plus a one-time reveal of the real
  `screen-finale.webp` plate. "The eye at the window" is this reveal's own thematic
  name, not a second unbuilt mechanic — confirmed against the task's own title.
- **Breeding/genetics, shop rotation, sell-back**: all fully implemented end-to-end,
  matching their design docs (stat convergence toward the better parent, deterministic
  daily rotation, piecewise sell pricing off rolled stats).

## 5. Gaps this audit is filing as new tasks

- **t-070 — swim-canvas fish are still hand-drawn shapes, not the delivered art.**
  This is very likely the single biggest driver of "barest of bones": even after
  today's fix, the one thing a player watches continuously in the tank has no real
  art. Wire the same `utils/cthulhuquariumArt.ts` fallback (or the real per-fish art)
  into the canvas renderer in place of `drawFish()`'s primitives.
- **t-071 — reconcile the click-collectible and food/upgrade mechanics with the
  pitch, or amend the brief.** Click-to-collect earns nothing (cosmetic dismiss of
  coins already credited server-side) and there is no food-tier/drop-speed upgrade
  system, both undocumented as deviations anywhere Silas would see them. Either build
  the literal mechanics or have Silas confirm the shipped deviation is intentional and
  update `DESIGN-BRIEF.md` to say so — this is a design call, not a pure bug.
- **t-072 — fix or delete `importCthulhuquariumArt.mjs`** so a future session doesn't
  trust it to reproduce the delivered art (wrong target directory, not read by the
  glob that actually serves images), and wire real `Monster.iconPath`/`cardPath`/
  `artImageId` DB records for the 119 species that now have plates, so the fallback
  becomes real data rather than a permanent workaround.
- **t-073 — author and deliver art for the remaining 32 species** that still fall
  back to a placeholder icon even with the client-side fix active, using the same
  pipeline/process as the other 119.
- **t-074 — wire the two buildable remaining milestones** (`first_full_tank`,
  `first_spotless_tank` — both detectable from existing state) and decide/scope
  `first_evolution` and `first_rivalry_resolved`, which are blocked on subsystems
  that don't exist yet (see t-075). Currently only the 4 bestiary-count breakpoints
  of the 8 named in `economy.yaml` are wired.
- **t-075 — the rivalry subsystem is scaffolded but has zero runtime logic.**
  `Monster.dietRole`/`schoolRole` and a no-op `peace_ward` set piece all exist and are
  explicitly commented as waiting on this; nothing computes rivalry today. Worth a
  scope decision from Silas as much as a build task — this is a real, not-small
  feature, not a bug fix.

`t-022` (shared bestiary handshake with Ruler is Hooked) and `t-065`'s remaining
signed-out visual acceptance are already correctly tracked at `needs-human`/`ready`
and are not duplicated here. This audit independently confirmed t-022's code-level
gap is real and not silently done: `Monster.games` exists precisely as the sharing
mechanism, but Ruler is Hooked's own fish catalog is a hardcoded static array that
never touches `Monster` — no Prisma import, no `server/api/ruler*` routes at all.

## 6. What should NOT be inferred from this audit

- The backend is genuinely substantial and mostly correct: 25 API routes (not the
  stale "16" figure in earlier task notes — eggs/finale/decor subtrees grew since),
  8 Prisma models, offline income, breeding, shop rotation, sell-back, decor, rare
  events, and the finale are all real, wired, and match their design docs.
  "Barest of bones" is a real verdict about the *visible* experience, not an accurate
  description of what was actually built.
- Fixing t-070 (real fish art in the swim view) is likely to move the needle on
  Silas's verdict more than any other single item in this audit — prioritize it
  first when picking up the new tasks above.
