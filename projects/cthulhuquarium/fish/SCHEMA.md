# Fish bible schema (cthulhuquarium/t-003)

The catalogue lives in `fish/*.yaml`, one file per rarity tier (`common.yaml` …
`mythic.yaml`), because tier is the axis both the economy (`../data/economy.yaml`
`rarity_tiers`) and the escalation rule (DESIGN-BRIEF decision 4) are organized
around. `scripts/validate_fish.py` reads all of them and enforces this contract.

Every field here maps onto an existing `kind_robots` column — t-008 seeds these
straight into `Character` rows, so **do not invent a field that has nowhere to
land.** Where a field is bible-only (no Character column yet), that is called out
explicitly below.

## Per-species fields

```yaml
- slug: goldfish-common              # -> Character.slug (globally @unique — see "Slugs" below)
  name: "Common Goldfish"            # -> Character.name
  tier: COMMON                       # -> economy.yaml rarity_tiers key (see "Tier, not a second `rarity` field")
  stats:                             # -> Character.{charm,empathy,grace,luck,might,wits}
    charm: UNCOMMON
    empathy: COMMON
    grace: COMMON
    luck: COMMON
    might: COMMON
    wits: COMMON
  diet_role: neutral                 # predator | prey | neutral -- economy.yaml rivalry.emergent_rules
  school_role: school                # school | anchor | solitary -- economy.yaml rivalry.emergent_rules
  rivals: []                         # optional [slug, ...] -- authored overrides, economy.yaml rivalry.authored_default_multiplier_each
  size: 1                            # -> Character.size (tank-capacity weight against Aquarium.sizeCap, t-032)
  evolves_to: goldfish-elder         # optional slug -- bible-only, see "Evolution: two axes, one field"
  evolution_kind: growth             # growth | breeding -- required when evolves_to is set, omit otherwise
  field_note: >
    One-line museum-placard text, dry register. See "Voice" below.
  art_prompt: >
    Silhouette-forward prompt. See "Art prompts" below.
  games:                             # -> which shared-bestiary consumers seed this species
    - cthulhuquarium
```

## Tier, not a second `rarity` field

`Character.Rarity` (`COMMON`..`MYTHIC`) is the *only* rarity scale in this game —
ECONOMY.md is explicit that the six tiers match the schema enum exactly, and that
authoring "only needs to assign each species a tier, not a bespoke number" for
income/unlock cost. A fish's `tier` is that same enum value, and it does three jobs
at once: the species' collection rarity, the `economy.yaml` `rarity_tiers` lookup
key for `income_per_tick`/`unlock_cost`, and (scaled ~20%, per ECONOMY.md) its feed
cost. There is deliberately no second per-fish `rarity` field — a fish's six
`stats` are individually-tiered (a COMMON-tier fish can still roll an UNCOMMON
`charm`), which already gives every species texture without a redundant top-level
axis that would just restate `tier`. **No bespoke coin/feed numbers belong in a
fish entry** — `tier` alone resolves them via `economy.yaml`.

## The six stats

`charm`, `empathy`, `grace`, `luck`, `might`, `wits` — each one independently a
`Rarity` value, exactly mirroring `Character`'s own six columns. These are public,
per-species, and shared by every copy (SYSTEMS.md's species/individual split: the
bible describes the species, `AquariumStock.stat*` holds each owned individual's
own hidden rolled numbers, which are not part of this file). A stat need not match
the species' `tier` — an otherwise COMMON fish with a MYTHIC `luck` is exactly the
kind of texture this project's voice rewards. Authored by feel for v1 ("wrong on
purpose", per SYSTEMS.md's tuning-later scope call); a systematic pass is t-019's
job, not this one's.

## Evolution: two axes, one field

SYSTEMS.md names two *separate* evolution mechanisms that share one plumbing verb:
**growth** (a species matures into the next one — the goldfish line is the named
example) and **breeding** ("secret evolutions" that only appear by pairing two
owned individuals). Both are represented the same way in the bible:

- `evolves_to: <slug>` — the species this one becomes, or produces.
- `evolution_kind: growth | breeding` — which mechanism unlocks it. Required
  whenever `evolves_to` is set; omit both fields on a species with no further
  evolution (most LEGENDARY/MYTHIC entries are chain terminals).

**This is bible-only today, not yet a `Character` column.** No `evolvesTo`/
`evolutionKind` field exists on `Character` as of t-032 — the actual growth/
breeding *mechanics* (t-029's rolled-stat convergence, the trigger that fires an
evolution) are unbuilt, and adding the column now with nothing reading it yet
would be exactly the kind of unused-but-harmless addition SYSTEMS.md's "shapes
now, tuning later" section endorses in the schema, but here the shape is still
genuinely undecided (does the game read the bible file at runtime, or does t-008's
seed step need to copy `evolvesTo`/`evolutionKind` onto `Character` too?) — so it
stays data-only until whichever task builds the evolution trigger (t-029 or a
successor) makes that call with the runtime code in front of it. **FOR THE NEXT
IMPLEMENTER:** don't let this sit undecided past t-029 — flag it there rather than
letting the bible and the schema silently diverge on where evolution state lives.

A `breeding`-kind `evolves_to` describes what breeding CAN produce, not a
guarantee — the actual roll/convergence odds are t-029's. A species may be the
`evolves_to` target of more than one `growth` predecessor only if that is a
deliberate authored convergence; `validate_fish.py` doesn't forbid it, but nothing
in this bible currently does it.

## Ecological tags

`diet_role` and `school_role` drive `economy.yaml`'s `rivalry.emergent_rules`
table (`predator`+`prey` in the same tank: −30% production each; `school`+`anchor`:
−15% each). `neutral` and `solitary` opt a species out of the emergent side of
either axis respectively — they still take the `authored_default_multiplier_each`
hit if named in another species' `rivals:` list.

`rivals: [slug, ...]` is the authored override list — "these two specifically
loathe each other," no ecological justification required, per SYSTEMS.md's
"where the actual jokes live." A pair need not share tags to rival; the list is
one-directional in authoring but the game applies it both ways at placement time
(if fish A rivals B, B rivals A back) — write it on whichever species you're
authoring at the time, don't duplicate the entry on both.

## Slugs

`Character.slug` is globally `@unique` (not per-user — that constraint is
`Aquarium.slug`'s, fixed to `@@unique([userId, slug])` in t-032; species slugs are
shared across every player and must be unique across the *entire* catalogue).
Pattern: `{creature}-{tier-or-stage-word}`, lowercase, hyphenated, no spaces
(`goldfish-common`, `goldfish-elder`). `validate_fish.py` enforces both the
pattern and cross-file uniqueness.

## Voice

Field notes are one line, dry museum-placard register — Charlotte and Wilbur may
talk around the tank in whatever voice fits them, but the placard itself never
winks at the player. COMMON and UNCOMMON entries describe an actual fish, however
odd; RARE and above may cross into DESIGN-BRIEF decision 4's "clearly not a fish"
territory (too many joints, mostly eye, something wearing a fish), but even then
the placard reports it as flatly as it would report a real species, because the
deadpan delivery *is* the joke. Never gross-out; unsettling is the ceiling, and
the shape must still read as a legible silhouette (see "Art prompts").

## Art prompts

Silhouette-forward, per DESIGN-BRIEF's own reasoning: silhouettes survive Comfy's
inconsistency where detailed creature rendering would not. Every `art_prompt`
should name a clean, backlit or high-contrast silhouette treatment explicitly, one
or two distinguishing silhouette features (not surface detail — a shape a player
recognizes at a glance), and stay within the same escalation ceiling as the field
note for that tier.

## `games`

Which shared-bestiary consumer(s) seed this species. `[cthulhuquarium]` for
everything in v1 — `ruler-hooked` is named in the shared-bestiary goal
(`../roadmap.yaml`'s project `goal:`) but ruler-hooked's own reopening/handoff
work (see its roadmap) hasn't landed yet, so nothing in this file claims
`ruler-hooked` until that side is ready to actually consume it. Add it to a
species' `games:` list when that handoff task says to, not preemptively.
