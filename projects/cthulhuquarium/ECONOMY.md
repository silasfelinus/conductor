# Cthulhuquarium — Economy and Progression Spec (t-004)

date: 2026-08-24
status: draft v1 — confirm-or-tune with Silas before t-009 (server API) builds against it
companion to: `DESIGN-BRIEF.md` (tone, scope, decided questions) and `SYSTEMS.md`
(the design reasoning this document turns into numbers)
data file: `data/economy.yaml` — the actual tunable constants; this document is the
rationale for each one, not a duplicate of the numbers themselves

---

## What "data-driven, tunable without a deploy" means here

Every number a balance pass would ever want to change lives in `data/economy.yaml`,
not in code. The intent (per the task title and `AquariumEvent`'s own schema comment
in `prisma/schema.prisma`, which already points back to this file) is that once t-009
(server API) and t-026/t-027 (sets, debris) are built, changing a fish's income rate,
a set's bonus, or the offline-income cap is a data commit — either a re-seed of that
YAML into a small config table, or a direct read of the file at request time — never a
code change or a redeploy. This document does not implement that read path; it defines
what the data looks like so t-009 can build the read path against a settled shape.

Nothing below invents a new rule. Every number is a concrete instantiation of a
decision already made in `DESIGN-BRIEF.md` or `SYSTEMS.md`; where I picked a specific
constant (an unlock cost, a decay rate) that neither document stated numerically, it's
flagged as **[v1 estimate]** — safe defaults to build against, not settled balance.

## The two currencies, made concrete

`SYSTEMS.md`'s "Two economies, pacing each other" table is the spine:

| Currency | Buys | Earned by | This spec's mechanism |
|---|---|---|---|
| **Coins** | fish, food, set pieces — breadth | producing and clicking | `rarity_tiers[*].income_per_tick`, accrued once per `economy.tick_seconds` (60s) |
| **Milestones** | tank capacity — room | landmark events | `milestones[*]`, each a one-time `AquariumEvent` |

Coins are a continuous rate; milestones are discrete, authored events. That asymmetry
is deliberate and already decided — it's what keeps the catalogue open while the tank
stays finite (`SYSTEMS.md`, "Two economies, pacing each other").

## Rarity tiers: six, matching the schema exactly

`Character.Rarity` already has six values (`COMMON` → `MYTHIC`). `economy.yaml`'s
`rarity_tiers` gives each one an `income_per_tick` and `unlock_cost` on a **[v1
estimate]** curve: roughly ×2.5 income and ×4 cost per tier. That ratio is deliberate —
cost outpaces income per tier, so a player is never fully "caught up"; there is always
a next tier worth saving for, which is what sustains the collection hook past the first
few species. No fish bible content existed yet at spec time (t-003 is still open,
blocked on `cthulhuquarium` repo access this session doesn't have — see Flags below),
so this curve is intentionally bible-agnostic: it keys purely on `Rarity`, and t-003
only needs to assign each species a tier, not a bespoke number.

**Collection, not copies.** Unlocking a species adds exactly one instance to the
bestiary and the tank. This wasn't stated explicitly anywhere but follows directly from
"the bestiary is the actual progression spine" (`SYSTEMS.md`, decision 3) — a game about
collecting distinct species has no reason to sell duplicates, and allowing them would
let coin-grinding substitute for exploring the catalogue, undermining the exact
progression spine that decision establishes.

## Hunger: rate gate only, exactly as decided

`DESIGN-BRIEF.md` decision 1 is unambiguous — "fish do not die," hunger "survives as a
rate gate only." `economy.yaml`'s `hunger` block is that decision as a curve:
`AquariumStock.hunger` (already an `Int` 0–100 in the live schema, `t-007`, merged)
decays 1/tick, and a four-band multiplier table scales production down to exactly zero
at hunger 0 — paused, never negative, resumes at full rate the tick after feeding. Feed
cost scales with the fish's own unlock-cost curve (**[v1 estimate]** 20%) so a MYTHIC
costs more to keep than a COMMON, mirroring the unlock economy instead of introducing a
second, unrelated cost curve.

**The food is alive** (decision 2) is a content/rendering requirement — food items
squirm on the way down and stop when eaten — not an economy number, so it isn't
represented in `economy.yaml`. Flagged here so whichever task authors food items (a
`sets/`-shaped or `fish/`-adjacent data set, likely alongside t-003's bible work in the
`cthulhuquarium` repo) doesn't lose the requirement between documents.

## Debris: throttles rate, never holdings, and it's tank-wide

`SYSTEMS.md` #2 gives debris the identical shape to hunger — rate throttle, never a
loss — but scoped to the whole tank rather than one fish, and deliberately *generated
faster with more occupants* so a fuller, more successful tank is also messier. That's
the mechanic that turns "come back later" into "something to click," per `SYSTEMS.md`'s
own framing ("the reward for coming back becomes something to do, not just a number
that went up"). `economy.yaml`'s `debris` block encodes: **[v1 estimate]** 0.5
accrual/tick per occupant, a four-band multiplier bottoming out at 0.25× (never 0× —
matches the "never fully dies" spirit even though the letter of the never-degrade rule
only requires "rate, not holdings"), and three independently-tunable clear rates for
the three routes `SYSTEMS.md` insists stay co-viable: manual clicking (fastest,
instant, no cooldown by design — it's the interaction), the debris set piece, and The
Sexton. The Sexton clears marginally faster than the set piece **[v1 estimate]** so a
player who's found and fed the snail gets a visibly better outcome than one who
hasn't, without either route being strictly dominant (both are passive-only; clicking
alone can out-pace either).

## Offline income: idling rewarded, active play still faster

`DESIGN-BRIEF.md` MVP point 6 requires both halves at once — offline income exists, and
it's capped so active play stays ahead. `economy.yaml` picks **[v1 estimate]** 50% of
the live rate, capped at 8 hours of accrual, computed once at login against the tank's
hunger/debris state *at logout* (not replayed tick-by-tick) so the calculation stays a
single multiply. This is the same shape `SYSTEMS.md` #3 requires of the idle-collection
set piece, generalized to the baseline every player gets — the set piece then stacks a
*further*, smaller, explicitly-capped bonus on top (`idle_hoarder`, below), never
replacing this baseline.

## Slots: the master gate, exactly as decided

`SYSTEMS.md` "Gate capacity, not access" and t-025's decision 1 (one shared pool for
fish and set pieces) are both direct inputs here, not reinterpreted. `economy.yaml`'s
`slots` block: a **[v1 estimate]** starting cap of 4, growing only through the four
`bestiary_N` milestones at +2 each, landing at 12 by `bestiary_20` — enough room to
build a real, contested tank at the MVP's 20-species bar without ever being able to
hold the whole catalogue at once, which is the entire point of the gate (`SYSTEMS.md`:
"you always own more than you have room for, permanently"). **`slotsCap` is not yet a
live `Aquarium` column** — `t-007`'s migration (merged) didn't include it, since the
number didn't exist yet when that schema landed. Flagged as a small additive follow-up
migration needed before `t-009` (or a set-piece task) can persist it; this file is the
data that migration should seed from.

## Rivalry: both authored and emergent, exactly as decided

t-025's decision 2 settles this as "both," with an emergent tag-driven table for scale
and an authored override list for the actual jokes. `economy.yaml`'s `rivalry` block
gives the emergent table two rules — predator/prey (**[v1 estimate]** −30% each, the
strongest pairing, matching `SYSTEMS.md`'s framing of it as the central rivalry
example) and anchor/school (**[v1 estimate]** −15% each, gentler, more common) — plus a
default magnitude (−40%) for an authored `rivals:` entry that doesn't specify one, so
`t-003`'s bible authors can write `rivals: [some-slug]` without also having to invent a
number. Recovery is instant on separation, per `SYSTEMS.md`'s "the moment you separate
them, both recover fully" — no cooldown, because a cooldown would itself be a form of
degradation this game's central rule forbids.

## Set pieces: keyed to fish properties, not flat buffs

Every set in Silas's seed list (`SYSTEMS.md`'s table) gets a concrete `effect` +
`value` pair in `economy.yaml`, chosen so bonuses attach to *what a fish is* rather
than being flat percentages — the synergy rule `SYSTEMS.md` states directly. Two
worth flagging:

- **`roaming_collector` must visibly move** (Silas's own note, both in the original
  pitch and `SYSTEMS.md`). That's a rendering/animation requirement for whichever task
  builds it, not an economy number — flagged in the data file's comment so it isn't
  lost between here and implementation.
- **Non-stacking idle effects.** `SYSTEMS.md` #3's hard constraint ("never everything")
  is about the tank's *total* passive rate, not any one set in isolation. Two
  individually-bounded idle-ish effects (`roaming_collector`'s auto-click,
  `idle_hoarder`'s away-bonus) could still combine past what the rule intends if both
  were equipped at once. `economy.yaml` names this explicitly
  (`no_stack_idle_effects`) rather than trusting each cap alone to hold the line —
  whichever task builds set equipping should enforce it as a real constraint (e.g. a
  slot-category exclusivity check), not just document it.

## Milestones: landmarks, not thresholds

t-025 decision 4's concrete v1 list — first full tank, first evolution, first spotless
tank, first rivalry resolved, and the four bestiary breakpoints — is reproduced
verbatim as `economy.yaml`'s `milestones` list, each mapped to the `AquariumEvent`
shape `t-007`'s schema already supports (`kind: 'milestone'`, a `payload` naming which
landmark fired) with no new model needed, exactly as t-025 concluded. Only the
bestiary breakpoints carry a `slots_cap_delta` — the other four are pure story beats
(a background, delivered by Charlotte), matching `SYSTEMS.md`'s point that not every
milestone needs to move a mechanical number.

## Two-hour simulation: is active play actually faster than idle?

`data/simulate_economy.py` runs both scenarios from the task note ("simulate the first
two hours of play... a spec nobody simulated is a guess") against the numbers above: an
**active** player who feeds a hungry fish, clicks debris down, and buys the next
affordable COMMON fish whenever a slot is free, versus an **idle** tank left completely
alone, both starting from one COMMON fish and zero coins.

**First result, and a methodology correction it forced.** Comparing raw coin *balance*
at minute 120 initially showed idle *ahead* of active (63.8 vs 42.6) — which looks like
a real violation of DESIGN-BRIEF's MVP point 6 ("idling is rewarded, but active play is
still faster"). It isn't one: raw balance conflates *spending* with *losing*. The active
player's lower balance is coins converted into fish (an investment), not coins lost —
exactly what the game asks a player to do with them. The fair comparison is **net worth**
(coins on hand + the unlock cost of every fish owned) and **gross income earned**
(cumulative production, before any spending) — both ignore *how* a player chose to hold
their wealth and measure only how much the tank actually produced.

| minute | active: net worth | active: gross income | idle: net worth | idle: gross income |
|---|---|---|---|---|
| 10 | 10.0 | 10.0 | 10.0 | 10.0 |
| 20 | 20.0 | 20.0 | 20.0 | 20.0 |
| 30 | 30.0 | 30.0 | 30.0 | 30.0 |
| 40 | 40.0 | 40.0 | 40.0 | 40.0 |
| 50 | 49.8 | 49.8 | 48.0 | 48.0 |
| 60 | 49.6 | 59.6 | 52.4 | 52.4 |
| 70 | 68.4 | 78.4 | 56.4 | 56.4 |
| 80 | 88.4 | 98.4 | 60.4 | 60.4 |
| 90 | 111.8 | 121.8 | 62.2 | 62.2 |
| 100 | 141.2 | 151.2 | 63.8 | 63.8 |
| 110 | 164.2 | 184.2 | 63.8 | 63.8 |
| 120 | 192.6 | 222.6 | 63.8 | 63.8 |

By net worth and gross income, active play pulls decisively ahead once the second fish
is affordable (~minute 70) and the gap widens for the rest of the run — **3.0x net
worth, 3.5x gross income by minute 120** — because active reinvestment compounds
(more fish → more income → afford the next fish sooner) while the untouched idle fish's
hunger bottoms out at minute 100 and its production flatlines at exactly zero from
there on (it is never fed again; per the never-degrade rule this is a *pause*, not a
loss — its 63.8 held balance never decreases, it simply stops growing). **The v1
numbers satisfy DESIGN-BRIEF's requirement**, but the shape of *why* is worth carrying
forward: the compounding comes entirely from reinvestment (buying more fish), not from
the hunger/debris curves themselves — a tank that only fed and cleaned without ever
buying a second fish would track much closer to idle. Worth keeping in mind when tuning
`unlock_cost` — if it's raised much past the v1 curve, that reinvestment loop slows and
the active/idle gap this simulation found could shrink or invert again. Re-run the
script after any change to `rarity_tiers`, `hunger`, or `debris` in `economy.yaml`
rather than assuming the ratio still holds.

This scenario deliberately does not model `offline_income`'s separate 50%/8h formula
(that only applies while logged out, not to an "idle-but-logged-in" tank) or set pieces
(none owned yet at this stage of a fresh account) — both are natural next scenarios for
this same script once t-026/t-009 give them a shape to simulate against.

## t-019 balance pass (2026-09-07): milestone ladder + offline-income check

t-019 asked for a real-play-data retuning pass. No live DB, telemetry endpoint, or
actual player sessions exist to retune against (same access gap this file's "where it
lives" section below already documents), and Silas's 2026-09-07 policy on the task
explicitly substitutes a **conservative, data-and-design-driven pass** for a personal
playtest rather than blocking further: extend the milestone ladder using the
simulation, the design docs, and the numbers already on record, and treat real
telemetry as future iterative tuning rather than a prerequisite. This section is that
pass.

**Milestone ladder, extended past bestiary_20.** The four original bestiary
breakpoints (5/10/15/20, +2 slots each) were sized for a 20-species MVP; the bible
closed at 151 species (t-037), so those four breakpoints now cover only 13% of the
collection and the remaining 131 species pay no capacity reward at all — a gap t-019's
own task note records was deliberately deferred here rather than guessed at. The fix is
not more +2 breakpoints at the same 5-species cadence: a linear continuation would push
`slots_cap` past 50 by bestiary_100, and once a tank can hold most of what a player
owns, the size-weighted packing problem `SCHEMA.md` was built around stops applying —
the exact failure mode the task note warns against. `economy.yaml`'s `milestones` list
now adds seven new bestiary breakpoints that decelerate on both axes at once — spacing
widens (5 → 10 → 15 → 20 → 25 → 25 → 26) and the per-breakpoint reward shrinks (+2 → +1
→ +1 → +1 → +1 → +1 → +0) — landing on a **final `slots_cap` of 19**: comfortably under
the ~50 threshold already identified as trivializing, and nowhere near the 524 tank
units a fully-stocked collection would require, so meaningful curation stays a live
decision for the entire life of the game rather than only its first 13%. The terminal
breakpoint, `bestiary_151` (full collection), is background-only with
`slots_cap_delta: 0` — the same "reward the moment, not more room" shape
`last_aquarium` already uses for the game's actual ending — so completing the bestiary
reads as a collector's achievement, not a mechanical payout that would need its own
re-balance later. Full breakdown and rationale live as a comment directly above the new
entries in `economy.yaml`, next to the numbers they explain.

**Hunger/debris/offline-income: re-verified, not re-tuned.** The task also asked
whether "the first 10 minutes engage with zero upgrades," whether the mid-game stalls,
and whether offline income is tuned so a day away feels rewarding but never better than
playing. Nothing here changed `rarity_tiers`, `hunger`, or `debris` — re-running
`simulate_economy.py` against the milestone-ladder edit reproduces the exact table
above unchanged (the two-hour, single-fish-line scenario never reaches a bestiary
breakpoint, so it can't be affected either way), confirming no regression and that the
existing 3.0x net-worth / 3.5x gross-income active-vs-idle gap still holds. Two
specific checks worth recording rather than re-deriving next time:

- **Offline income is strictly worse than active play by construction, not just by this
  simulation's numbers.** `offline_income.rate_multiplier` (0.5) applies to production
  computed at whatever hunger/debris the tank had *at the moment of logout*, held fixed
  for the whole offline window (hunger/debris do not continue decaying or accruing
  while offline — see the `offline_income` section above). Active play always runs at
  the *un-discounted* rate (multiplier 1.0 at full hunger) plus the reinvestment
  compounding this simulation measured, and offline income never benefits from either.
  So for any elapsed duration, offline income is bounded above by `0.5 ×` what the same
  time spent active would earn from production alone, before compounding — it cannot
  cross over into "better than playing" without a change to `rate_multiplier` itself.
  This holds regardless of how long the ladder above makes a player's tank, so it did
  not need re-simulating for this pass.
- **First-10-minutes engagement and mid-game stall are real questions this data-only
  pass cannot fully settle.** The active-scenario table shows the *first* affordable
  purchase (a second COMMON fish, 50 coins) landing around minute 70 once the one
  starting fish's own upkeep (a feed around minute 50) is paid for — meaning roughly the
  first hour has no purchase decision available yet, only feeding and debris-clicking.
  Whether that reads as "quiet but engaged" or "stalled" is a game-feel judgment this
  script's numbers alone cannot make; per the task's 2026-09-07 policy, this is
  intentionally left as the first thing to revisit once real play sessions exist, rather
  than moved blind. If it turns out to feel slow, the more targeted lever is
  `rarity_tiers.COMMON.unlock_cost` (currently 50) or the COMMON `income_per_tick`
  (currently 1), not the hunger/debris curves — both of which are already validated
  against the idle/active ratio above and would need re-simulating if touched.

**Net effect of this pass:** one data commit (`economy.yaml`'s milestone list only),
zero code changes (per the task's own "data commit only, or the economy leaked out of
YAML somewhere" framing), simulation re-run and unchanged, and two explicit findings —
one closed (offline-vs-active ordering is structurally guaranteed), one deliberately
left open for real telemetry (early-game pacing feel) rather than guessed at.

## A note on where this file lives

The task note asked for `economy/balance.yaml` in the `silasfelinus/cthulhuquarium`
repo (the portable data-canon repo `DESIGN-BRIEF.md` establishes). This session's
GitHub access is scoped to `kind_robots`, `conductor`, `kapowarr`, and
`humboldtscoopsolutions` only — it does not include `cthulhuquarium` — so per
`AGENTS.md`'s cross-repo task protocol, this spec lives here in the conductor project
folder (`projects/cthulhuquarium/ECONOMY.md` + `data/economy.yaml` +
`data/simulate_economy.py`) as a complete, ready-to-move handoff rather than a partial
attempt at the intended location. Whichever session next has `cthulhuquarium` repo
access should relocate `data/` verbatim into that repo's `economy/` directory (a file
move, not a rewrite — nothing here depends on conductor-repo paths except the
simulation script's own `pathlib` lookup of its sibling `economy.yaml`, which moves
with it unchanged) and update this document's path references accordingly.

## What this task did not do (explicitly out of scope)

- **No fish bible content.** t-003 (fish bible v1) lives in the same out-of-reach
  `cthulhuquarium` repo (see above). This spec is deliberately bible-agnostic — it keys
  on `Rarity` and two ecological tags (`diet_role`, `school_role`) that t-003 needs to
  assign per species, not on any specific fish.
- **No Prisma migration.** The missing `Aquarium.slotsCap` column (and a debris-level
  column, likely `Aquarium.debrisLevel`) are flagged above as follow-up work for
  whichever task next touches the schema — not added here, since t-004's scope is the
  data spec, not the persistence layer.
- **No server API or UI.** t-009 (server API, not yet claimed) is the right place to
  turn this file into a live read path; nothing here is wired to a route.

## Flags for Reviewer

- Every constant marked **[v1 estimate]** above is a placeholder tuned for internal
  consistency (curve shapes, ratios between related numbers) rather than playtested
  balance — expected to move once `t-009`/`t-026`/`t-027` actually run this economy and
  Silas can feel the pacing. Nothing here should be read as a final balance pass.
- t-003 (fish bible) is the load-bearing blocker for `t-008` (seed script) and
  therefore for any real playtesting of these numbers — this session could not attempt
  it directly (repo access, above). Worth a cross-repo handoff task if no future
  session has `cthulhuquarium` repo access either.

### Kaizen suggestion
A small `scripts/validate_economy_yaml.py` (mirroring `validate_roadmaps.py`'s shape)
that checks `data/economy.yaml` for internal consistency — every `rarity_tiers` key is
a real `Rarity` enum value, `debris_skimmer.value` matches
`debris.clean.debris_set_clears_per_tick`, milestone `slots_cap_delta` sums plus
`slots.starting_cap` land on a sane final number — would catch the "two numbers that
are supposed to stay in sync silently drift" class of bug before it reaches a real
balance pass, the same problem CI's `validate_roadmaps.py` solves for roadmap YAML.
