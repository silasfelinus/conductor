# Cthulhuquarium — The Fun Loop (m4, t-079)

date: 2026-10-10 · status: spec for t-080 to t-083 · numbers: `data/economy.yaml` `fun_loop` ·
pace check: `data/simulate_fun_loop.py`

## Why this exists

Silas, 2026-10-10, declining the game at t-065:

> "the gameplay loop is still lackluster. we can get about four or five fish out, there is nothing really
> to do, and the general page needs tightening. like the work done with the characters and fish
> animations though. what we need is an actually fun loop. in the inspiration game insaniquarium, fish
> spawned coins which allowed making more fish. we need some sort of clickable thing, that doesn't seem
> to be happening, and we aren't allowing enough fish in a tank. I think we should ditch the breeding and
> secret stats part of the game as well, simplify. we want a fun gameplay loop first."

What the code did when he played it (kind_robots, 2026-10-10):

| Symptom he named | Cause in the code |
|---|---|
| "nothing really to do" | One scale sheds for the **whole tank** every 15 s regardless of fish count (`server/utils/aquariumCollect.ts` `COLLECT_BASE_SPAWN_SECONDS`). A perfect clicker earns ~4.5 coins/min early on, so a 50-coin fish is ~11 minutes away. More fish only make each scale worth more; they never add scales. |
| "four or five fish" | Room is counted in fish **size** against `Aquarium.sizeCap` (default 10), species sizes run 1-10, only one of each species is allowed, and nothing a player can buy raises room (milestones raise set-piece slots only). |
| "no clickable thing" | The scales exist but are small, few and slow; tapping a fish only startles it. |
| feeding feels like a tax | Feeding costs 20% of the fish's unlock price. |
| complexity | Breeding, eggs, six hidden stats, stat-based sell prices and "best seen" stats sit between the player and the loop. |

## The loop

**Fish drop coins. Click coins. Buy more fish. Fill the tank. Buy a bigger tank. Trade up.**

That is the whole game for m4. Everything that does not serve it is removed or moved off the main screen.

### 1. Every fish drops coins (t-080)

- Each fish drops one coin every **15 s** on its own timer (`coin_drop_seconds_per_fish`), staggered so
  drops don't arrive in waves. The drop-speed upgrade shortens that interval (same +25%/level track as
  today, now applied per fish).
- Coin value is set by the fish's rarity: COMMON 3, UNCOMMON 8, RARE 20, EPIC 50, LEGENDARY 125,
  MYTHIC 300 (`coin_value_by_tier`). Bigger fish, bigger and shinier coins.
- A coin spawns at its fish, drifts down for ~8 s, rests on the gravel for ~4 s, then fades
  (`coin_visible_seconds: 12`). A coin that isn't clicked is gone.
- Click or tap a coin to collect: a clear sound, a "+N" pop, the coin flies to the coin counter. Tap
  targets are at least 44 px on phones. A tap on a fish still startles it, so a missed coin tap near a fish
  stays playful.
- A **starving** fish (hunger 0) drops nothing. Hunger no longer scales coin value; debris and rivalry
  do not touch coin drops at all (they keep affecting only the small passive income below). One rule a
  player can see: fed fish drop coins.
- Passive / offline income (`settleTick`, 0.5x, 8 h cap) is unchanged and is now small next to clicking,
  which is the point.

**Server-authoritative, in value rather than count.** The client reports the total value of the coins it
clicked. The server accrues value from `Aquarium.collectAnchorAt` at the tank's current drop rate
(sum over fed fish of `coin_value / drop_seconds`), caps what it will credit at `coin_visible_seconds`
of accrual (coins older than that have faded on screen anyway), credits
`min(claimed, accrued)`, floors to whole coins, and advances the anchor by `credited / rate`. A client
that lies can only claim value the clock already owed it, exactly as today's `collectAllowance`
guarantees for scales. This replaces the scale count model; the anchor column is reused, so no
migration.

### 2. A tank that fills up (t-081)

- **Room counts fish, not size.** Every fish takes one slot regardless of species size.
- A new tank has **12** fish slots (`starting_fish_slots`). **Tank expansions** add 4 slots each, bought
  with coins, in order: 400, 1,200, 3,000, 7,500, 18,000, 40,000, 90,000 — **40 fish** at the top. The
  `extra_species_slot` set piece still adds +1.
- **Copies are allowed.** Buying a species you already own adds another one at its normal unlock cost.
  The bestiary and its milestones still count **distinct** species, so collecting stays a goal.
- **Release** a fish for a flat 50% of its unlock cost (`release_refund_factor_of_unlock_cost`). With a
  full tank this is how a player trades up from commons to rarer fish, which is the mid-game.
- Schema: one additive column for purchased expansions (e.g. `Aquarium.tankExpansions Int @default(0)`).
  `sizeCap` stays in the table but stops gating fish. Existing tanks keep every fish they have; their
  slots start at the new 12.
- The canvas must stay readable and smooth at 40 fish on a phone: scale sprites by tank population, cap
  simultaneous coin sprites, cull off-screen work.

### 3. Feeding is a cheap click

- Feeding costs **2%** of the fish's unlock cost, minimum 1 (`feed_cost_factor_of_unlock_cost`): a
  COMMON costs 1 coin, a RARE 15. One **Feed all hungry** button is the main control; per-fish feeding
  can stay in the fish drawer.
- Hunger keeps its 100-minute decay, so a session-long player feeds every hour or so and a returning
  player feeds once.

### 4. Removed (t-082)

Breeding, eggs and hatching, the six hidden stats, stat rolls, stat-based sell prices, the
Ichthyonomicon's "best seen" stats, and their routes, store actions, dialogs and tests. The Prisma
columns and the `AquariumEgg` table **stay** (kind_robots AGENTS.md: no destructive drop inside the
auto-deploy window); a separate staged cleanup task removes them once the new loop is live.

What stays: the 151-fish roster and its sprites and swim clips, Charlotte and Wilbur and their story
scenes, backgrounds, decorations, set pieces, the milestone ladder, the Ichthyonomicon as a picture
book, the leaderboard, the finale.

### 5. The page is the tank (t-083)

The tank is the first and largest thing on the page. Above or over it, one compact HUD:

- coin counter (where collected coins fly to);
- **Buy a fish** (opens the shop as a sheet; the cheapest useful buy is one tap);
- **Feed all hungry** (with its price);
- room as `fish / slots` with **Expand tank** when affordable;
- the next drop-speed or food upgrade when affordable.

Everything else (decorate, backgrounds, set pieces, Ichthyonomicon, leaderboard, visibility) moves behind
one drawer or tab row under the tank. The per-fish card grid becomes a compact roster in that drawer,
grouping copies (`Brass Tack Goby ×4`). Character dialogue and barks stay, over the tank.

## Pace targets and the simulated result

`python3 projects/cthulhuquarium/data/simulate_fun_loop.py` (attentive player: clicks 80% of coins, at
most 1.5 per second; feeds when any fish drops below 50; buys greedily; expands when full; releases the
worst fish to trade up):

| Target | Simulated |
|---|---|
| Second fish within about a minute | 1:03 |
| A dozen fish inside the first session | 11:35 |
| First tank expansion | 24:07 |
| 25 fish (medium-term goal) | ~79 min |
| Tank mix at 2 h | 28 slots, EPIC and LEGENDARY fish, ~1.9 coin drops/s |

At a full late-game tank, coin drops outrun a comfortable click rate (~1.9/s against the simulated 1.5).
That is deliberate pressure for a later "collector" upgrade (for example The Sexton sweeping coins that
reach the gravel), not something m4 needs to ship.

## Acceptance for the milestone

Silas plays a fresh tank on a phone and on desktop and finds it fun: coins to chase within seconds, a
second fish inside a minute, a dozen fish in one sitting, a reason to come back for the next expansion.
That verdict is t-069.
